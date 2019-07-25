from vm import ConstIndex, NameIndex
from commands.base import CopyInstr, TOS, SimpleInstr


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
