from typing import List

from symbol_table import to_nbt
from vm import StackIndex, NameIndex
from commands.base import SimpleInstr, Instr, TOS


class InitContext(Instr):
    def __init__(self, code, obj_id=None):
        self.is_object = obj_id is not None
        self.obj_id = obj_id
        self.height = code.co_stacksize
        self.consts = code.co_consts

    def gen(self, i):
        parts = []
        if not self.is_object:
            parts.append('Tags:[".dest", ".volatile"]')
        else:
            parts.append('UUIDMost:0L,UUIDLeast:{}L,'.format(self.obj_id))

        cstr = ",".join(map(lambda c: to_nbt(c, False), self.consts))
        sstr = ",".join(["{}"] * self.height)

        parts.append('ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{'
                     'Stack:[' + sstr + '],Consts:[' + cstr + '],Names:{}}},{},{},{}]')

        nbt = "{" + ",".join(parts) + "}"
        yield 'summon minecraft:armor_stand ~ ~2 ~ ' + nbt

    def str(self):
        return "ICTX", "obj" if self.is_object else "stk", self.height, self.obj_id if self.obj_id is not None else ""


class InitFrame(SimpleInstr):
    def __init__(self):
        super().__init__("IFRM", "tag @s remove .dest")


class CopyArgs(Instr):
    def __init__(self, names: List[str]):
        self.names = names

    def gen(self, i):
        for name in self.names:
            target = NameIndex(name)
            yield "data modify entity @e[tag=.dest,limit=1] {} set from entity @s {}".format(repr(target), repr(i))
            i.pop()

    def str(self):
        return "CARG", TOS(), ",".join(map(str, self.names))


class EndCall(Instr):
    def __init__(self):
        pass

    def gen(self, i):
        i.push()
        yield "data modify entity @s {} set from entity @e[tag=.ret,limit=1] {}".format(repr(i), repr(StackIndex(0)))
        yield 'kill @e[tag=.ret,tag=.volatile,limit=1]'

    def str(self):
        return "ENDC", TOS()
