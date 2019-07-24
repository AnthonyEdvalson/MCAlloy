from typing import List

from containers import Path
from symbol_table import Arg


def indent(s, amt=2):
    space = " " * amt
    return space + str(s).replace("\n", "\n" + space)


class AlloyNode:
    def __init__(self, line):
        self.line = line

    def pprint(self):
        print(self)


class Block(AlloyNode):
    def __init__(self, frame_path, name):
        super().__init__(None)
        self.targets = []
        self.body = []
        self.path = frame_path.altered(block=name)

    def __str__(self):
        return str(self.path) + ":\n" + "\n".join([indent(item) for item in self.body])


class Frame(AlloyNode):
    def __init__(self, mod_path, name):
        super().__init__(None)
        self.root_block = None
        self.path = mod_path.altered(frame=name)

    def __str__(self):
        return str(self.path) + ":\n" + indent(self.root_block)


class Module(AlloyNode):
    def __init__(self, path):
        super().__init__(None)
        self.frames = []
        self.path = path

    def __str__(self):
        return str(self.path) + ":\n" + "\n".join([indent(block) for block in self.frames])


class Direct(AlloyNode):
    def __init__(self, line, command):
        super().__init__(line)
        self.command = command

    def __str__(self):
        return "Direct: " + self.command


class FunctionDef(AlloyNode):
    def __init__(self, line, name, args: List[Arg], frame_path: Path):
        super().__init__(line)
        self.name = name
        self.args = args
        self.frame_path = frame_path

    def __str__(self):
        return "\n".join([
            "FunctionDef: {}: ({})".format(self.name, ", ".join(map(str, self.args))),
            indent(self.frame_path)
        ])


class Return(AlloyNode):
    def __init__(self, line):
        super().__init__(line)

    def __str__(self):
        return "\n".join([
            "Return"
        ])


class If(AlloyNode):
    def __init__(self, line, true_path, false_path, cont_path):
        super().__init__(line)
        self.true_path = true_path
        self.false_path = false_path
        self.cont_path = cont_path

    def __str__(self):
        return "\n".join([
            "If:",
            "  True: " + str(self.true_path),
            "  False: " + str(self.false_path),
            "  Continue: " + str(self.cont_path)
        ])


class Byte(AlloyNode):
    def __init__(self, line, code, bytecode):
        super().__init__(line)
        self.code = code
        self.bytecode = bytecode

    def __str__(self):
        return "Byte:\n" + "\n".join([indent(instr) for instr in self.bytecode])
