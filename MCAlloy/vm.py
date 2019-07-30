

class VMIndex:
    nbt = None

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return "ArmorItems[0].tag.{}".format(self.nbt.format(self.index))

    def __str__(self):
        # Very often I would use str() instead of repr() on a VMIndex before using it in a command,
        # it used to be a huge pain to debug, so the angle brackets have been added so this function
        # returns invalid NBT, immediately breaking the mcfunction parser, rather than a runtime fail
        return "<{}>".format(self.nbt.format(self.index))


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


class PreIndex(VMIndex):
    nbt = "Pre[{}]"


class NameIndex(VMIndex):
    nbt = "Names.{}"
