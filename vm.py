

class VMIndex:
    nbt = None

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return "ArmorItems[0].tag." + str(self)

    def __str__(self):
        return self.nbt.format(self.index)


class ConstIndex(VMIndex):
    nbt = "Consts[{}]"


class StackIndex(VMIndex):
    nbt = "Stack[{}]"

    def off(self, offset):
        return StackIndex(self.index + offset)

    def alter(self, offset):
        self.index += offset

    def push(self, n=1):
        self.alter(n)

    def pop(self, n=1):
        self.alter(-n)


class NameIndex(VMIndex):
    nbt = "Names.{}"
