from commands import SetASM
from commands.base import Instr, TOS
from containers import Path


class Call(Instr):
    debug_before = True

    def __init__(self, path: Path):
        self.path = path

    def gen(self, i):
        yield "execute as @e[tag=.dest] run function {}".format(self.path)

    def str(self):
        return "CALL", self.path


class CallBlock(Call):
    def __init__(self, path: Path):
        super().__init__(path)

    def gen(self, i):
        yield "function {}".format(self.path)


class BlockBridge(CallBlock):
    def __init__(self, path):
        super().__init__(path)

    def gen(self, i):
        yield "execute if score ret ..ASM matches 0 run function {}".format(self.path)

    def str(self):
        return "BRGE", self.path


class CallBlockIf(CallBlock):
    debug_before = True

    def __init__(self, path: Path, invert=False):
        super().__init__(path)
        self.invert = invert

    def gen(self, i):
        match = 0 if self.invert else 1
        yield "execute store result score test ..ASM run data get entity @s {}.v".format(repr(i))
        yield "execute if score test ..ASM matches {} run function {}".format(match, self.path)

    def str(self):
        return "CAL?", self.path, TOS(), "== 0" if self.invert else "== 1"


class Return(Instr):
    def __init__(self):
        pass

    def gen(self, i):
        yield from SetASM("ret", 1).gen(i)
        yield 'tag @s add .ret'

    def str(self):
        return "RTRN", TOS()
