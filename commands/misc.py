from commands.base import SimpleInstr, Instr, TOS


class Direct(SimpleInstr):
    debug_before = True

    def __init__(self, command: str, offset):
        super().__init__("/", "{}", offset, command)


class Comment(SimpleInstr):
    warn_fail = False

    def __init__(self, message, offset):
        super().__init__("#", "# {}", offset, message)


class Seek(Instr):
    def __init__(self, delta, offset):
        super().__init__(offset)
        self.delta = delta

    def gen(self, i):
        i.alter(self.delta)
        yield from []

    def str(self):
        return "SEEK", self.delta, TOS()


class NOOP(Instr):
    def __init__(self, offset):
        super().__init__(offset)

    def gen(self, i):
        yield from []

    def str(self):
        return "NOOP", self.offset if self.offset is not None else "-"
