import types

from alloy_instructions.asmcontext import AsmContext

from alloy_instructions.generators.util import FrameStub
from commands import Comment, InitContext, Call, Return, CopyArgs, LoadConst, ConstIndex, NameIndex, LoadName, \
    BinaryOp, CompareOp, Seek, StoreName, EndCall, NOOP, CallBlockIf, BlockBridge
from commands.base import BaseInstr
from containers import ILBlock, Path, ILFrame, ILModule
from symbol_table import Func, SymbolTable
from alloy_ast import nodes


def assemble_alloy(path: Path, doc: str, alloy: nodes.AlloyNode):
    asm = AlloyAssembler(path, doc, alloy)
    return asm.assemble()


class AlloyAssembler:
    def __init__(self, path: Path, doc: str, alloy: nodes.AlloyNode):
        self.mod_path = path
        self.alloy = alloy
        self.doc = doc
        self.st = SymbolTable()
        self.module = None
        self.frame = None
        self.block = None

    def assemble(self):
        self.visit(self.alloy)
        return self.module

    def visit(self, node: nodes.AlloyNode):
        if node.line is not None:
            l = node.line
            s = "{}: {}".format(l, self.doc.split("\n")[l - 1])
            self.write(Comment(s, None))
            print(s)

        visitor = getattr(self, "assemble_" + type(node).__name__.lower())
        visitor(node)

    def write(self, command: BaseInstr):
        self.block.push(command)

    def write_start(self, command: BaseInstr):
        self.block.push_start(command)

    def _error_msg(self, node, detail):
        if node is None:
            return detail
        else:
            msg = "\n"
            pre = "[{}] ".format(node.lineno if hasattr(node, "lineno") else "?")
            msg += "{}{}\n".format(pre, self.doc.split("\n")[node.lineno - 1])
            if hasattr(node, "col_offset"):
                msg += " " * (node.col_offset + len(pre)) + "^\n\n"
            msg += detail
            return msg

    def call_function(self, func: Func, block: bool, offset: int):
        self.write(InitContext(func.code, offset))
        self.write(CopyArgs(func.args, None))
        self.write(Call(func.path, None))
        if not block:
            self.write(EndCall(None))

    def assemble_module(self, node: nodes.Module):
        self.module = ILModule(self.mod_path)
        self.st.push_layer(str(self.mod_path))
        [self.visit(frame) for frame in node.frames]
        self.st.pop_layer()

    def assemble_frame(self, node: nodes.Frame):
        self.frame = ILFrame(node.path)
        self.module.frames.append(self.frame)
        self.st.push_layer(str(self.frame.path))

        self.visit(node.root_block)

        self.st.pop_layer()
        self.frame = None

    def assemble_block(self, node: nodes.Block):
        parent = self.block

        self.block = ILBlock(node.path)
        if parent is None:
            self.frame.root_block = self.block
        else:
            parent.targets.append(self.block)

        with CommentTags(self, str(node.path), node.line):
            [self.visit(n) for n in node.body]

        if node.bridge is not None:
            self.write(BlockBridge(node.bridge, None))
        else:
            # TODO store code object in frame, pull None from co_consts
            self.write(LoadConst(ConstIndex(0), None))
            self.assemble_return(nodes.Return(None))

        for target in node.targets:
            self.assemble_block(target)

        self.block = parent

    def assemble_byte(self, node: nodes.Byte):
        write = self.write
        special_stack = []

        for instr in node.bytecode:
            off = instr.offset

            op = instr.opname
            if op == "LOAD_CONST":
                write(LoadConst(ConstIndex(instr.arg), off))
            elif op == "LOAD_NAME" or op == "LOAD_FAST":
                sym = self.st.get_symbol(NameIndex(instr.argrepr))
                if isinstance(sym, Func):
                    special_stack.append(sym)
                    write(NOOP(off))
                elif isinstance(sym, NameIndex):
                    write(LoadName(sym, off))
                else:
                    raise Exception("Unknown symbol type {}".format(type(sym)))
            elif op.startswith("BINARY_") or op.startswith("INPLACE_"):
                write(BinaryOp(binops[op.split("_", 1)[1]], off))
            elif op == "COMPARE_OP":
                write(CompareOp(compops[instr.arg], off))
            elif op == "CALL_FUNCTION":
                func = special_stack.pop()
                self.call_function(func, False, off)
            elif op == "RETURN_VALUE":
                write(Return(off))
            elif op == "POP_TOP":
                write(Seek(-1, off))
            elif op == "STORE_NAME":
                ni = NameIndex(instr.argval)
                write(StoreName(ni, off))
                if not self.st.has_symbol(ni):
                    self.st.add_symbol(ni)
            else:
                raise Exception(self._error_msg(None, "Unknown op {}".format(op)))

    def assemble_new_frame(self, path, body, args, ctx: AsmContext):
        stub = FrameStub(path, body, ctx, args, self.frames)
        self.frame_stubs.append(stub)

    def assemble_functiondef(self, node: nodes.FunctionDef):
        q = lambda x: isinstance(x, types.CodeType) and x.co_name == node.name
        func_code = list(filter(q, self.ctx.code.co_consts))[0]

        func = Func(self.path.altered(frame=node.name, block=0), node.args, func_code)
        self.ctx.st.add_symbol(func)
        func_ctx = AsmContext(self.ctx.st, self.ctx.doc, func.code, node)
        self.assemble_new_frame(func.path, node.frame, func.args, func_ctx)

    def assemble_return(self, node):
        # TODO handle Return in bytecode? then we could remove offset as an arg
        self.write(Return(None))
        return True

    def assemble_if(self, node: nodes.If):
        # test result is TOS
        self.write(CallBlockIf(node.true_path, None, False))
        self.write(CallBlockIf(node.false_path, None, True))
        self.write(Seek(-1, None))

        return True

    def node_pass(self, node):
        pass


class CommentTags:
    def __init__(self, ilbg: AlloyAssembler, text: str, line: int):
        self.ilbg = ilbg
        self.text = text
        self.line = line

    def __enter__(self):
        self.tag(True)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tag(False)

    def tag(self, start):
        if self.line is not None:
            s = "{}: ".format(self.line)
        else:
            s = ""

        s += "<{}{}>".format("" if start else "/", self.text)
        self.ilbg.write(Comment(s, None))
        print(s)


binops = {
    "ADD": "+=",
    "SUBTRACT": "-=",
    "MULTIPLY": "*=",
    "TRUE_DIVIDE": "/=",
    "MODULO": "%="
}

compops = {
    0: "<",
    1: "<=",
    2: "=",
    3: "!=",
    4: ">",
    5: ">="
}  # TODO Add other ops: 6: in 7: not in 8: is 9: is not 10: exception match 11: BAD
