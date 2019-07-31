from instrs import SimpleInstr, Instr, TOS


class Direct(SimpleInstr):
    debug_before = True

    def __init__(self, command: str):
        super().__init__("/", "{}", command)


class Comment(SimpleInstr):
    print_tag = False
    warn_fail = False

    def __init__(self, message):
        super().__init__("#", "# {}", message)


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
