import ast
import types

from alloy_instructions.asmcontext import AsmContext

from alloy_instructions.generators.util import BlockStub, FrameStub
from commands import Comment, InitContext, Call, Return, CopyArgs, LoadConst, \
    ConstIndex, NameIndex, LoadName, BinaryOp, CompareOp, Seek, StoreName, EndCall, NOOP
from commands.base import BaseInstr
from containers import ILBlock
from symbol_table import Func
from alloy_ast import nodes


def assemble_block(stub: BlockStub):
    gen = ILBlockGenerator(stub)
    return gen.assemble()


class ILBlockGenerator:
    def __init__(self, stub: BlockStub):
        self.path = stub.path
        self.ctx = stub.ctx
        self.block = ILBlock(self.path)

        self.frame_stubs = []
        self.block_stubs = []
        self.special_stack = []

        self.links = []

    def assemble(self) -> ILBlock:
        self.visit(self.ctx.alloy)
        return self.block

    def visit(self, node: nodes.AlloyNode):
        if node.line is not None and not hasattr(node, "body"):
            l = node.line
            s = "{}: {}".format(l, self.ctx.doc.split("\n")[l - 1])
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
            msg += "{}{}\n".format(pre, self.ctx.doc.split("\n")[node.lineno - 1])
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

    def assemble_module(self, node):
        self.visit(node.body)

    def assemble_block(self, node: nodes.Block):
        block_ctx = AsmContext(self.ctx.st, self.ctx.doc, self.ctx.code, node)
        stub = BlockStub(self.path.altered(block=name), block_ctx)
        self.block_stubs.append(stub)

        with CommentTags(self, node.name, node.line):
            for node in node.body:
                self.visit(node)

    def assemble_byte(self, node):
        write = self.write

        for instr in node.visit_exec:
            off = instr.offset

            op = instr.opname
            if op == "LOAD_CONST":
                write(LoadConst(ConstIndex(instr.arg), off))
            elif op == "LOAD_NAME" or op == "LOAD_FAST":
                sym = self.ctx.st.get_symbol(NameIndex(instr.argrepr))
                if isinstance(sym, Func):
                    self.special_stack.append(sym)
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
                func = self.special_stack.pop()
                self.call_function(func, False, off)
            elif op == "RETURN_VALUE":
                write(Return(off))
            elif op == "POP_TOP":
                write(Seek(-1, off))
            elif op == "STORE_NAME":
                ni = NameIndex(instr.argval)
                write(StoreName(ni, off))
                if not self.ctx.st.has_symbol(ni):
                    self.ctx.st.add_symbol(ni)
            elif op.startswith("POP_JUMP_IF_"):
                write(JumpIf(self.path, instr.arg, op.endswith("TRUE"), off))
            elif op == "JUMP_FORWARD":
                write(Jump(self.path, off + instr.arg + 2, off))
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

    def node_return(self, node, offset):
        self.assemble_line_as_byte(node.lineno)  # TODO handle Return in bytecode? then we could remove offset as an arg
        self.write(Return(offset))
        return True

    def assemble_if(self, node: nodes.If):
        self.visit(node.test)
        self.visit(node.true_path)
        self.visit(node.false_path)

        return True

    def node_pass(self, node):
        pass


class CommentTags:
    def __init__(self, ilbg: ILBlockGenerator, text: str, line: int):
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
