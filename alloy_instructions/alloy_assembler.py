from commands import Comment, InitContext, Call, Return, CopyArgs, LoadConst, ConstIndex, NameIndex, LoadName, \
    BinaryOp, CompareOp, Seek, StoreName, EndCall, NOOP, CallBlockIf, BlockBridge, Direct
from commands.base import BaseInstr
from containers import ILBlock, Path, ILFrame, ILModule
from symbol_table import Func, SymbolTable
from alloy import nodes


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
            line = node.line
            s = "{}: {}".format(line, self.doc.split("\n")[line - 1])
            self.write(Comment(s))
            print(s)

        visitor = getattr(self, "assemble_" + type(node).__name__.lower())
        visitor(node)

    def write(self, command: BaseInstr):
        self.block.push(command)

    def write_start(self, command: BaseInstr):
        self.block.push_start(command)

    def _error_msg(self, node: nodes.AlloyNode, detail):
        if node is None:
            return detail
        else:
            msg = "\n"
            pre = "[{}] ".format(node.line if hasattr(node, "line") else "?")
            msg += "{}{}\n".format(pre, self.doc.split("\n")[node.line - 1])
            msg += detail
            return msg

    def call_function(self, func: Func, block: bool):
        self.write(InitContext(func.code))
        self.write(CopyArgs(func.args))
        self.write(Call(func.path))
        if not block:
            self.write(EndCall())

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

        # TODO store code object in frame, pull None from co_consts
        self.frame.root_block.push(LoadConst(ConstIndex(0)))
        self.frame.root_block.push(Return())  # TODO repeated code, Return should go through assemble_return

        self.st.pop_layer()
        self.frame = None

    def assemble_block(self, node: nodes.Block):
        parent = self.block
        self.block = ILBlock(node.path)

        # Connect the new block into the block hierarchy
        if self.frame.root_block is None:
            self.frame.root_block = self.block
        else:
            parent.targets.append(self.block)

        # Assemble body
        with CommentTags(self, str(node.path), node.line):
            [self.visit(n) for n in node.body]

        # Add a bridge to the next block, if it exists
        if node.bridge is not None:
            self.write(BlockBridge(node.bridge))

        # Assemble children
        for target in node.targets:
            self.assemble_block(target)

        self.block = parent

    def assemble_byte(self, node: nodes.Byte):
        write = self.write
        special_stack = []

        for instr in node.bytecode:
            op = instr.opname
            if op == "LOAD_CONST":
                write(LoadConst(ConstIndex(instr.arg)))

            elif op == "LOAD_NAME" or op == "LOAD_FAST":
                sym = self.st.get_symbol(NameIndex(instr.argrepr))
                if isinstance(sym, Func):
                    special_stack.append(sym)
                elif isinstance(sym, NameIndex):
                    write(LoadName(sym))
                else:
                    raise Exception("Unknown symbol type {}".format(type(sym)))

            elif op.startswith("BINARY_") or op.startswith("INPLACE_"):
                write(BinaryOp(binops[op.split("_", 1)[1]]))

            elif op == "COMPARE_OP":
                write(CompareOp(compops[instr.arg]))

            elif op == "CALL_FUNCTION":
                func = special_stack.pop()
                self.call_function(func, False)

            elif op == "RETURN_VALUE":
                write(Return())

            elif op == "POP_TOP":
                write(Seek(-1))

            elif op == "STORE_NAME":
                ni = NameIndex(instr.argval)
                write(StoreName(ni))
                if not self.st.has_symbol(ni):
                    self.st.add_symbol(ni)

            else:
                raise Exception(self._error_msg(node, "Unknown op {}".format(op)))

    def assemble_functiondef(self, node: nodes.FunctionDef):
        self.st.add_symbol(Func(node.frame.path, node.args, node.frame.code))

    def assemble_return(self, node):
        self.write(Return())
        return True

    def assemble_if(self, node: nodes.If):
        # test result should be TOS
        self.write(CallBlockIf(node.true_path))
        self.write(CallBlockIf(node.false_path, True))
        self.write(Seek(-1))
        return True

    def assemble_while(self, node: nodes.While):
        self.write(CallBlockIf(node.while_path))
        self.write(Seek(-1))
        return True

    def assemble_direct(self, node: nodes.Direct):
        self.write(Direct(node.command))


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
        self.ilbg.write(Comment(s))
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
