from instrs import SimpleInstr, Instr, TOS


class Direct(SimpleInstr):
    debug_before = True

    def __init__(self, command: str):
        super().__init__("/", "{}", command)


class Comment(Instr):
    def __init__(self, message):
        self.message = message

    def gen(self, i):
        pass

    def generate(self, i, gs):
        return self.comment_line(self.message, gs.warn_fail, gs.comment)

    def str(self):
        return "#", self.message


class Seek(Instr):
    print_tag = False

    def __init__(self, delta):
        self.delta = delta

    def gen(self, i):
        i.alter(self.delta)
        yield from []

    def str(self):
        return "SEEK", self.delta, TOS()


class NOOP(Instr):
    print_tag = False

    def __init__(self):
        pass

    def gen(self, i):
        yield from []

    def str(self):
        return "NOOP"
