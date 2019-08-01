from typing import Tuple, List

from vm import VMIndex
from instrs.base import CopyInstr, TOS, SimpleInstr, Instr


class LoadNBT(SimpleInstr):
    def __init__(self, nbt, target=TOS()):
        super().__init__("LNBT", "data modify entity @s {} set from value {}", target, nbt, stack_action="push")


class Load(CopyInstr):
    def __init__(self, index: VMIndex):
        super().__init__("LOAD", TOS(), index, stack_action="push")


class Store(CopyInstr):
    def __init__(self, index: VMIndex):
        super().__init__("SNAM", index, TOS(), stack_action="pop")


class SetASM(SimpleInstr):
    print_tag = False

    def __init__(self, key, val):
        super().__init__("SASM", "scoreboard players set {} __asm__ {}", key, val)


class CopyScore(SimpleInstr):
    def __init__(self, player, score="__asm__", attr="v", target=TOS()):
        cmd = "execute store result entity @s {}.{} int 1 run scoreboard players get {} {}"
        super().__init__("CSCO", cmd, target, attr, player, score)


class LoadAttr(Instr):
    def __init__(self, name_index):
        self.name_index = name_index

    def gen(self, i):
        yield "execute store result score t0 __asm__ run data get entity @s {}.v".format(repr(i))

        yield "tag @s add __target__"
        copy = "data modify set @e[tag=__target__,limit=1] {} from entity @s {}".format(repr(i), repr(self.name_index))
        yield "execute as @e[] run execute if score @s __ptr__ = t0 __asm__ run " + copy
        yield "tag @s remove __target__"

    def str(self):
        return "LATR", TOS(), self.name_index


class StoreAttr(Instr):
    def __init__(self, name_index):
        self.name_index = name_index

    def gen(self, i):
        yield "execute store result score t0 __asm__ run data get entity @s {}.v".format(repr(i))
        i.pop()
        yield "tag @s add __target__"
        copy = "data modify set @s {} from entity @e[tag=__target__,limit=1] {}".format(repr(self.name_index), repr(i))
        i.pop()
        yield "execute as @e[] run execute if score @s __ptr__ = t0 __asm__ run " + copy
        yield "tag @s remove __target__"

    def str(self):
        return "SATR", TOS(), self.name_index


class Shuffle(Instr):
    def __init__(self, assigns: List[Tuple[int, int]], seek):
        self.assigns = assigns
        self.seek = seek

    def gen(self, i):
        for assign in self.assigns:
            v0 = i.off(assign[0])
            v1 = i.off(assign[1])
            yield "data modify entity @s {} set from entity @s {}".format(repr(v0), repr(v1))
        i.alter(self.seek)

    def str(self):
        s = ", ".join(["{} < {}".format(*a) for a in self.assigns])
        return "SHFL", s, TOS()
