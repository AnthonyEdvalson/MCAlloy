from instrs import *
from containers import ILBlock, ILFrame, ILModule
from alloy import nodes


def assemble_alloy(doc: str, alloy: nodes.AlloyNode):
    asm = AlloyAssembler(doc, alloy)
    return asm.assemble()


class AlloyAssembler:
    def __init__(self, doc: str, alloy: nodes.AlloyNode):
        self.alloy = alloy
        self.doc = doc
        self.module = None
        self.frame = None
        self.block = None

    def assemble(self):
        self.visit(self.alloy)
        return self.module

    def visit(self, node: nodes.AlloyNode):
        s = "---"

        if node.line is not None:
            s = "{}: {}".format(node.line, self.doc.split("\n")[node.line - 1])

        if self.block:
            self.write(Comment(s))
        print(s)

        visitor = getattr(self, "assemble_" + type(node).__name__.lower())
        visitor(node)

    def assemble_module(self, node: nodes.Module):
        self.module = ILModule(node.path)
        [self.visit(frame) for frame in node.frames]

    def assemble_frame(self, node: nodes.Frame):
        self.frame = ILFrame(node.path, node.code)
        self.module.frames.append(self.frame)
        self.visit(node.root_block)
        self.frame = None

    def assemble_block(self, node: nodes.Block):
        parent = self.block
        self.block = ILBlock(node.path)

        # Connect the new block into the block hierarchy
        if node.is_root:
            self.frame.root_block = self.block
            # TODO pull None from co_consts
            self.write(LoadConst(ConstIndex(0)))
            self.write(Return())
            self.write_start(StartFrame(self.frame.code, True))
        else:
            parent.targets.append(self.block)

        # Assemble body
        with CommentTags(self, str(node.path), node.line):
            [self.visit(n) for n in node.body]

        [self.visit(link) for link in node.links]

        self.block = parent

    def assemble_link(self, node: nodes.Link):
        if node.condition is None:
            self.write(BlockBridge(node.path))
        if node.condition is False:
            self.write(CallBlockIf(node.path, True))
        if node.condition is True:
            self.write(CallBlockIf(node.path))

        if node.block:
            parent = self.block
            [self.visit(item) for item in node.block.body]
            self.block = parent

    def assemble_byte(self, node: nodes.Byte):
        write = self.write

        for instr in node.bytecode:
            op = instr.opname
            if op == "LOAD_CONST":
                ci = ConstIndex(instr.arg)
                write(LoadConst(ci))

            elif op in ["LOAD_NAME", "LOAD_FAST"]:
                sym = NameIndex(instr.argrepr)
                write(LoadName(sym))

            elif op.startswith("BINARY_") or op.startswith("INPLACE_"):
                write(BinaryOp(binops[op.split("_", 1)[1]]))

            elif op == "COMPARE_OP":
                write(CompareOp(compops[instr.arg]))

            elif op == "CALL_FUNCTION":
                self.call_function(instr.arg)

            elif op == "RETURN_VALUE":
                write(Return())

            elif op == "POP_TOP":
                write(Seek(-1))

            elif op == "STORE_NAME":
                ni = NameIndex(instr.argval)
                write(StoreName(ni))

            elif op == "LOAD_ATTR":
                ni = NameIndex(instr.argval)
                write(LoadAttr(ni))

            elif op == "STORE_ATTR":
                ni = NameIndex(instr.argval)
                write(StoreAttr(ni))

            elif op == "DUP_TOP":
                write(Shuffle([(1, 0)], 1))

            elif op == "DUP_TOP_TWO":
                write(Shuffle([(2, 0), (1, -1)], 2))

            elif op == "ROT_TWO":
                write(Shuffle([(1, 0), (0, -1), (-1, 1)], 0))

            elif op == "ROT_THREE":
                write(Shuffle([(1, 0), (0, -1), (-1, -2), (-2, 1)], 0))

            else:
                raise Exception(self._error_msg(node, "Unknown op {}".format(op)))

    def assemble_functiondef(self, node: nodes.FunctionDef):
        self.write(LoadNBT('{{v: {}, t: "fptr"}}'.format(node.fptr)))
        self.write(StoreName(node.name))

    def assemble_classdef(self, node: nodes.ClassDef):
        pass

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

    def call_function(self, arg_count):
        self.write(InitContext(arg_count + 1))
        self.write(EndCall())

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