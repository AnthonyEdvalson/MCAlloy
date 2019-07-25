from dis import Bytecode


class VMIndex:
    nbt = None

    def __init__(self, i):
        self.i = i

    def __repr__(self):
        return "ArmorItems[0].tag." + str(self)

    def __str__(self):
        return self.nbt.format(self.i)


class ConstIndex(VMIndex):
    nbt = "Consts[{}]"


class StackIndex(VMIndex):
    nbt = "Stack[{}]"

    def off(self, offset):
        return StackIndex(self.i + offset)

    def alter(self, offset):
        self.i += offset

    def push(self):
        self.alter(1)

    def pop(self):
        self.alter(-1)


class NameIndex(VMIndex):
    nbt = "Names.{}"
