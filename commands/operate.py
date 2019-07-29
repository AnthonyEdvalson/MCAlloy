from commands.base import Instr, TOS


class BinaryOp(Instr):
    def __init__(self, op):
        self.op = op

    def gen(self, i):
        yield "execute store result score t1 __asm__ run data get entity @s {}.v".format(repr(i))
        i.pop()
        yield "execute store result score t0 __asm__ run data get entity @s {}.v".format(repr(i))
        yield "scoreboard players operation t0 __asm__ {} t1 __asm__".format(self.op)
        yield "execute store result entity @s {}.v int 1 run scoreboard players get t0 __asm__".format(repr(i))

    def str(self):
        return "BIOP", TOS(), self.op


class CompareOp(Instr):
    def __init__(self, op):

        if op == "!=":
            self.op = "="
            self.invert = True
        else:
            self.op = op
            self.invert = False

    def gen(self, i):

        default = 1 if self.invert else 0
        i_default = 1 - default

        yield "execute store result score t1 __asm__ run data get entity @s {}.v".format(repr(i))
        i.pop()
        yield "execute store result score t0 __asm__ run data get entity @s {}.v".format(repr(i))
        yield "scoreboard players set t2 __asm__ {}".format(default)
        yield "execute if score t0 __asm__ {} t1 __asm__ run scoreboard players set t2 __ASM__ {}".format(self.op, i_default)
        yield "execute store result entity @s {}.v int 1 run scoreboard players get t2 __ASM__".format(repr(i))

    def str(self):
        return "COMP", TOS(), self.op


