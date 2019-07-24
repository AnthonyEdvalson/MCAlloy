from vm import ConstIndex, NameIndex
from commands.base import CopyInstr, TOS, SimpleInstr


class LoadConst(CopyInstr):
    def __init__(self, const: ConstIndex, offset):
        super().__init__("LCON", offset, TOS(), const, stack_action="push")


class LoadName(CopyInstr):
    def __init__(self, name: NameIndex, offset):
        super().__init__("LNAM", offset, TOS(), name, stack_action="push")


class StoreName(CopyInstr):
    def __init__(self, name: NameIndex, offset):
        super().__init__("SNAM", offset, name, TOS(), stack_action="pop")


class SetASM(SimpleInstr):
    def __init__(self, key, val, offset):
        super().__init__("SASM", "scoreboard players set {} ..ASM {}", offset, key, val)
