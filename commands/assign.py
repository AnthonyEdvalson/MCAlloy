from typing import Tuple, List

from vm import ConstIndex, NameIndex
from commands.base import CopyInstr, TOS, SimpleInstr, Instr


class LoadConst(CopyInstr):
    def __init__(self, const: ConstIndex):
        super().__init__("LCON", TOS(), const, stack_action="push")


class LoadName(CopyInstr):
    def __init__(self, name: NameIndex):
        super().__init__("LNAM", TOS(), name, stack_action="push")


class StoreName(CopyInstr):
    def __init__(self, name: NameIndex):
        super().__init__("SNAM", name, TOS(), stack_action="pop")


class SetASM(SimpleInstr):
    def __init__(self, key, val):
        super().__init__("SASM", "scoreboard players set {} ..ASM {}", key, val)


class LoadAttr(Instr):
    def __init__(self, name_index):
        self.name_index = name_index

    def gen(self, i):
        # TODO dereferencing is a very common instruction, but it's very slow, need to look into speeding it up
        yield "execute store result score t0 ..ASM run data get entity @s {}.v".format(repr(i))
        yield "execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref"
        yield "data modify set @s {} from entity @e[tag=.deref,limit=1] {}".format(repr(i), repr(self.name_index))
        yield "tag @e[tag=.deref,limit=1] remove .deref"

    def str(self):
        return "LATR", TOS(), self.name_index


class StoreAttr(Instr):
    def __init__(self, name_index):
        self.name_index = name_index

    def gen(self, i):
        yield "execute store result score t0 ..ASM run data get entity @s {}.v".format(repr(i))
        yield "execute as @e run execute if score @s ..addr = t0 ..ASM run tag @s add .deref"
        yield "data modify @e[tag=.deref,limit=1] {} from entity set @s {}".format(repr(self.name_index), repr(i))
        yield "tag @e[tag=.deref,limit=1] remove .deref"
        i.pop(2)

    def str(self):
        return "SATR", TOS(), self.name_index


class Shuffle(Instr):
    def __init__(self, assigns: List[Tuple[int, int]]):
        self.assigns = assigns

    def gen(self, i):
        for assign in self.assigns:
            v0 = i.off(assign[0])
            v1 = i.off(assign[1])
            yield "data modify entity @s {} set from entity @s {}".format(repr(v0), repr(v1))

    def str(self):
        s = ", ".join(["{} < {}".format(*a) for a in self.assigns])
        return "SHFL", s, TOS()

