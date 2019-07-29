from typing import List

from symbol_table import to_nbt
from vm import StackIndex, NameIndex
from commands.base import SimpleInstr, Instr, TOS


class InitContext(Instr):
    def __init__(self, arg_count):
        self.arg_count = arg_count

    def gen(self, i):
        parts = [
            'Tags:[".dest", ".volatile"]',
            'ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{}},{},{},{}]'
        ]

        nbt = "{" + ",".join(parts) + "}"
        yield 'summon minecraft:armor_stand ~ ~1 ~ ' + nbt

        for index in range(0, self.arg_count):
            target = StackIndex(index)
            yield "data modify entity @e[tag=.dest,limit=1] {} set from entity @s {}".format(repr(target), repr(i))
            i.pop()

        target = NameIndex("__fptr__")
        yield "data modify entity @e[tag=.dest,limit=1] {} set from entity @s {}".format(repr(target), repr(i))
        i.pop()

    def str(self):
        return "ICTX", TOS()


class RunFrameCall(Instr):
    def __init__(self, code):
        self.consts = code.co_consts
        self.height = code.stack_height

    def gen(self, i):
        yield "execute store result score t0 ..ASM run data get entity @s {}.v".format(NameIndex("__fptr__"))
        cstr = ",".join(map(lambda c: to_nbt(c, False), self.consts))
        sstr = ",".join(["{}"] * self.height)

        cmd = 'data modify entity @s ArmorItems[0].tag set from value {{Stack:{},Consts:{},Names:{{}}}}'
        yield cmd.format(sstr, cstr)

        yield "function ???"

    def str(self):
        return "RFCL", self.height, self.consts


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
