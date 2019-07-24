from dis import Bytecode


class VMIndex:
    pass


class ConstIndex(VMIndex):
    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return "ArmorItems[0].tag.Consts[{}]".format(self.i)

    def __str__(self):
        return "Const[{}]".format(self.i)


class StackIndex(VMIndex):
    def __init__(self, i):
        self.i = i

    def off(self, offset):
        return StackIndex(self.i + offset)

    def alter(self, offset):
        self.i += offset

    def push(self):
        self.alter(1)

    def pop(self):
        self.alter(-1)

    def __repr__(self):
        return "ArmorItems[0].tag.Stack[{}]".format(self.i)

    def __str__(self):
        return "Stack[{}]".format(self.i)


class NameIndex(VMIndex):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "ArmorItems[0].tag.Names.{}".format(self.name)

    def __str__(self):
        return "Names[{}]".format(self.name)


class FrameData:
    def __init__(self, code):
        self.code = code
        self.bytecode = Bytecode(code)

    def get_line_instrs(self, lineno):
        pass
