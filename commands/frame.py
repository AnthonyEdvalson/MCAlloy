from containers import Path
from symbol_table import to_nbt
from vm import StackIndex, PreIndex, NameIndex
from commands.base import Instr, TOS


class InitContext(Instr):
    def __init__(self, copy_count):
        """
        Creates a new armor stand with basic NBT scaffolding, as well as __dest__ and __volatile__ tags
        Then copies over copy_count arguments from @s to __dest__'s Pre section without changing order
        """
        self.copy_count = copy_count

    def gen(self, i):
        pstr = ",".join(["{}"] * self.copy_count)
        nbt = '{Tags:["__dest__", "__volatile__"]},' \
              'ArmorItems:[{id:"minecraft:paper",Count:1b,tag:{Pre:[' + pstr + ']}},{},{},{}]'
        yield 'summon minecraft:armor_stand ~ ~1 ~ ' + nbt

        for index in list(reversed(range(0, self.copy_count))):
            target = PreIndex(index)
            yield "data modify entity @e[tag=__dest__,limit=1] {} set from entity @s {}".format(repr(target), repr(i))
            i.pop()

    def str(self):
        return "ICTX", TOS()


class StartFrame(Instr):
    def __init__(self, code, is_func):
        """
        Run at the start of a frame. Sets up @s NBT to store vm information like Stack, Consts, and Names
        removes __dest__, and calls function code if is_func is True
        :param code: code object of instructions that'll be run on this frame
        """
        self.consts = code.co_consts
        self.height = code.co_stacksize
        self.is_func = is_func
        self.var_names = list(code.co_varnames)

        if is_func:
            self.var_names.insert(0, "__fptr__")

    def gen(self, i):
        yield "tag @s remove __dest__"

        for i, var_name in enumerate(self.var_names):
            source = PreIndex(i)
            target = NameIndex(var_name)
            yield "data modify entity @s {} set from entity @s {}".format(repr(target), repr(source))

        cstr = ",".join(map(lambda c: to_nbt(c, False), self.consts))
        sstr = ",".join(["{}"] * self.height)
        cmd = 'data modify entity @s ArmorItems[0].tag set from value {{Stack:[{}],Consts:[{}],Names:{{}}}}'
        yield cmd.format(sstr, cstr)

        if self.is_func:
            yield 'function {}'.format(Path("__callfunc__"))

    def str(self):
        return "IFRM", self.height, self.consts


class StartCall(Instr):
    def __init__(self):
        pass

    def gen(self, i):
        super().gen(i)
        yield "execute store result score fptr __asm__ run data get entity @s {}".format(repr(i))
        yield "function {}".format(Path("__callfunc__"))

        i.pop()

    def str(self):
        return "XFNC"


class EndCall(Instr):
    def __init__(self):
        """
        Finish a function call. Takes BOS from __ret__ and pushes it to TOS of @s, simulating a return
        Then kills __ret__, assuming it is tagged volatile. TODO bottom of stack always okay?
        """

    def gen(self, i):
        i.push()
        yield "data modify entity @s {} set from entity @e[tag=__ret__,limit=1] {}".format(repr(i), repr(StackIndex(0)))
        yield 'kill @e[tag=__ret__,tag=__volatile__,limit=1]'

    def str(self):
        return "ENDC", TOS()
