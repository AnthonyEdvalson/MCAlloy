from instrs import SetASM, Instr, TOS, LoadNBT
from util import to_nbt
from containers import Path


class Call(Instr):
    print_tag = False
    debug_before = True

    def __init__(self, path: Path):
        """
        Make an absolute call as __dest__
        :param path: the path of the mcfunction to call
        """
        self.path = path

    def gen(self, i):
        yield "execute as @e[tag=__dest__,limit=1] run function {}".format(self.path)

    def str(self):
        return "CALL", self.path


class CallBlock(Call):
    print_tag = False

    def __init__(self, path: Path):
        """
        Make a call to another mcfunction without changing @s
        :param path: the path of the mcfunction to call
        """
        super().__init__(path)

    def gen(self, i):
        yield "function {}".format(self.path)


class BlockBridge(CallBlock):
    print_tag = False

    def __init__(self, path):
        """
        Make a bridge to another block, the target block will only be called if not returning
        :param path: the path of the mcfunction to call if not returning
        """
        super().__init__(path)

    def gen(self, i):
        yield "execute if score ret __asm__ matches 0 run function {}".format(self.path)

    def str(self):
        return "BRGE", self.path


class CallBlockIf(CallBlock):
    debug_before = True

    def __init__(self, path: Path, invert=False):
        """
        Call an mcfunction if TOS is True (!= 0)
        :param path: path of block to call
        :param invert: invert logic. If True, mcfunction will be called if TOS is False (== 0)
        """
        super().__init__(path)
        self.invert = invert

    def gen(self, i):
        match = 0 if self.invert else 1
        yield "execute store result score test __asm__ run data get entity @s {}.v".format(repr(i))
        yield "execute if score test __asm__ matches {} run function {}".format(match, self.path)

    def str(self):
        return "CAL?", self.path, TOS(), "== 0" if self.invert else "== 1"


class Return(Instr):
    print_tag = False

    def __init__(self, value=TOS()):
        """
        Return by setting ret flag and tagging @s with __ret__
        Can pass a constant value to be set as TOS
        """
        self.value = value

    def gen(self, i):
        for line in list(self._gen(i)):
            yield 'execute if score ret __asm__ matches 0 run ' + line

    def _gen(self, i):
        if not isinstance(self.value, TOS):
            yield from LoadNBT(to_nbt(self.value)).gen(i)
        yield 'tag @s add __ret__'
        yield from SetASM("ret", 1).gen(i)
        i.pop()

    def str(self):
        return "RTRN", self.value
