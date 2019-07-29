from typing import List

from containers import Path


def indent(s, amt=2):
    if isinstance(s, list):
        return "\n".join([indent(item, amt) for item in s])
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
        self.bridge = None
        self.targets = []
        self.body = []
        self.path = frame_path.altered(block=name)

    def __str__(self):
        return "\n".join([
            str(self.path) + ":",
            "  Body:",
            indent(self.body, 4),
            "  Bridge: " + str(self.bridge),
            "  Targets:",
            indent(self.targets, 4)
        ])

    def bridge_to(self, block):
        if isinstance(block, Block):
            self.bridge = block.path
        elif isinstance(block, Path):
            self.bridge = block
        elif block is None:
            self.bridge = None
        else:
            raise TypeError()

    def target(self, block):
        self.targets.append(block)


class Frame(AlloyNode):
    def __init__(self, mod_path, name, code):
        super().__init__(None)
        self.root_block = None
        self.path = mod_path.altered(frame=name)
        self.code = code
        self.args = []

    def __str__(self):
        return str(self.path) + ":\n" + indent(self.root_block)


class Module(AlloyNode):
    def __init__(self, path):
        super().__init__(None)
        self.frames = []
        self.path = path

    def __str__(self):
        return str(self.path) + ":\n" + indent(self.frames)


class Direct(AlloyNode):
    def __init__(self, line, command):
        super().__init__(line)
        self.command = command

    def __str__(self):
        return "Direct: " + self.command


class FunctionDef(AlloyNode):
    def __init__(self, line, name, args: List[str], frame):
        super().__init__(line)
        self.name = name
        self.args = args
        self.frame = frame

    def __str__(self):
        return "\n".join([
            "FunctionDef: {}: ({})".format(self.name, ", ".join(map(str, self.args))),
            indent(self.frame.path)
        ])


class ClassDef(AlloyNode):
    def __init__(self, line, name, frame):
        super().__init__(line)
        self.name = name
        self.frame = frame

    def __str__(self):
        return "\n".join([
            "ClassDef: {}".format(self.name),
            indent(self.frame.path)
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


class While(AlloyNode):
    def __init__(self, line, test_path, while_path, cont_path):
        super().__init__(line)
        self.test_path = test_path
        self.while_path = while_path
        self.cont_path = cont_path

    def __str__(self):
        return "\n".join([
            "While:",
            "  Test: " + str(self.test_path),
            "  While: " + str(self.while_path),
            "  Cont: " + str(self.cont_path),
        ])


class Byte(AlloyNode):
    def __init__(self, line, code, bytecode):
        super().__init__(line)
        self.code = code
        self.bytecode = bytecode

    def __str__(self):
        return "Byte:\n" + indent(self.bytecode)
