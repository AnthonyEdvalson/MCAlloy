from abc import ABC, abstractmethod
from typing import Tuple, Union

from util import escape
from vm import StackIndex, VMIndex


class TOS:
    def __str__(self):
        return "TOS"


class BaseInstr(ABC):
    pass


class Instr(BaseInstr):
    debug_before = False
    warn_fail = True
    print_tag = True

    @abstractmethod
    def gen(self, i: StackIndex):
        yield from []

    @abstractmethod
    def str(self) -> Tuple:
        pass

    def debug_str(self, i: StackIndex) -> str:
        s = self.str()

        dat2 = ['{{"text":" >>> {: <5}"}}'.format(escape(str(s[0])))]
        for d in s[1:]:
            if type(d) is TOS:
                dat2.append('{{"text":"[{}]"}}'.format(i.index))
            else:
                dat2.append('{{"text":"{}"}}'.format(escape(str(d))))

        tellraw = 'execute if entity @a[scores={{..DEBUG=1..}}] run tellraw @a ["",{}]'
        yield tellraw.format(',{"text":"    "},'.join(dat2))

        if self.print_tag:
            yield tellraw.format(",".join([
                '{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag","entity":"@s"}',
                '{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}'
            ]))

    def generate(self, i: StackIndex, gs):
        buf = ' ' * 200

        pad = 43 if gs.warn_fail else 0

        if gs.debug and self.debug_before:
            for debug in list(self.debug_str(i)):
                yield buf + debug

        for command in list(self.gen(i)):
            is_comment = command[0] == "#"

            if is_comment:
                if gs.comment:
                    yield "#" * pad + command
                continue

            if self.warn_fail and gs.warn_fail:
                yield "execute store success score pass __asm__ run " + command
                fail = 'tellraw @a [{{"text": " !!!!!!!! FAIL: {}"}}]'.format(escape(command))
                yield buf + 'execute if score pass __asm__ matches 0 run {}'.format(fail)
            elif not self.warn_fail and gs.warn_fail:
                yield " " * pad + command
            else:
                yield command

        if gs.debug and not self.debug_before:
            for debug in list(self.debug_str(i)):
                yield buf + debug

    def __str__(self):
        dat = list(map(str, self.str()))
        fstr = "{: <6}" + "{: <14} " * (len(dat) - 1)
        return fstr.format(*dat)


class SimpleInstr(Instr):
    def __init__(self, name: str, form: str, *args, stack_action="none"):
        self.args = args
        self.form = form
        self.name = name
        self.stack_action = stack_action

    def gen(self, i):
        args = [i if isinstance(a, TOS) else a for a in self.args]
        args = [repr(a) if isinstance(a, VMIndex) else a for a in args]

        if self.stack_action == "push":
            i.push()

        yield self.form.format(*list(args))

        if self.stack_action == "pop":
            i.pop()

    def str(self):
        return [self.name, *self.args]


class CopyInstr(SimpleInstr):
    def __init__(self, name, target: Union[TOS, VMIndex], source: Union[TOS, VMIndex], stack_action="none"):
        form = "data modify entity @s {} set from entity @s {}"
        super().__init__(name, form, target, source, stack_action=stack_action)
