from commands.base import Instr, TOS


class BinaryOp(Instr):
    def __init__(self, op, offset):
        super().__init__(offset)
        self.op = op

    def gen(self, i):
        yield "execute store result score t1 ..ASM run data get entity @s {}.v".format(repr(i))
        i.pop()
        yield "execute store result score t0 ..ASM run data get entity @s {}.v".format(repr(i))
        yield "scoreboard players operation t0 ..ASM {} t1 ..ASM".format(self.op)
        yield "execute store result entity @s {}.v int 1 run scoreboard players get t0 ..ASM".format(repr(i))

    def str(self):
        return "BIOP", TOS(), self.op


class CompareOp(Instr):
    def __init__(self, op, offset):
        super().__init__(offset)

        if op == "!=":
            self.op = "="
            self.invert = True
        else:
            self.op = op
            self.invert = False

    def gen(self, i):

        default = 1 if self.invert else 0

        yield "execute store result score t1 ..ASM run data get entity @s {}.v".format(repr(i))
        i.pop()
        yield "execute store result score t0 ..ASM run data get entity @s {}.v".format(repr(i))
        yield "scoreboard players set t2 ..ASM {}".format(default)
        yield "execute if score t0 ..ASM {} t1 ..ASM run scoreboard players set t2 ..ASM {}".format(self.op, 1 - default)
        yield "execute store result entity @s {}.v int 1 run scoreboard players get t2 ..ASM".format(repr(i))

    def str(self):
        return "COMP", TOS(), self.op
