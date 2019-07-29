from abc import ABC, abstractmethod
from typing import Tuple, Union

from containers import Path
from util import escape
from vm import StackIndex, VMIndex, NameIndex, ConstIndex


class TOS:
    def __str__(self):
        return "TOS"


class BaseInstr(ABC):
    pass


class Instr(BaseInstr):
    debug_before = False
    warn_fail = True

    @abstractmethod
    def gen(self, i: StackIndex):
        yield from []

    @abstractmethod
    def str(self) -> Tuple:
        pass

    def debug_str(self, i: StackIndex) -> str:
        s = self.str()

        tellraw = 'execute if entity @a[scores={{..DEBUG=1..}}] run tellraw @a ["",{}]'

        dat2 = ['{{"text":" >>> {: <5}"}}'.format(escape(str(s[0])))]
        for d in s[1:]:
            str_types = {str, bool, int, Path, NameIndex, ConstIndex, StackIndex}
            if type(d) in str_types:
                dat2.append('{{"text":"{}"}}'.format(escape(str(d))))
            elif type(d) is TOS:
                dat2.append('{{"text":"[{}]"}}'.format(i.index))
            else:
                raise Exception("Illegal type {} in debug() of {}".format(type(d), type(self)))

        vm_info = ",".join([
            '{"text":" >>> STACK: "},{"nbt":"ArmorItems[0].tag.Stack","entity":"@s"}',
            '{"text":"NAMES: "},{"nbt":"ArmorItems[0].tag.Names","entity":"@s"}',
            '{"text":"CONSTS: "},{"nbt":"ArmorItems[0].tag.Consts","entity":"@s"}',
            '{"text":"TAGS: "},{"nbt":"Tags","entity":"@s"}'
        ])

        yield tellraw.format(',{"text":"    "},'.join(dat2))
        yield tellraw.format(vm_info)

    def generate(self, i: StackIndex, gs):
        buf = ' ' * 200

        pad = 41 if gs.warn_fail else 0

        if gs.debug and self.debug_before:
            for debug in self.debug_str(i):
                yield buf + debug

        for command in self.gen(i):
            is_comment = command[0] == "#"

            if is_comment:
                if gs.comment:
                    yield "#" * pad + command
                continue

            if self.warn_fail and gs.warn_fail:
                yield "execute store success score pass ..ASM run " + command
                fail = 'tellraw @a [{{"text": " !!!!!!!! FAIL: {}"}}]'.format(escape(command))
                yield buf + 'execute if score pass ..ASM matches 0 run {}'.format(fail)
            elif not self.warn_fail and gs.warn_fail:
                yield " " * pad + command
            else:
                yield command

        if gs.debug and not self.debug_before:
            for debug in self.debug_str(i):
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
        args = map(lambda a: i if isinstance(a, TOS) else a, self.args)
        args = map(lambda a: repr(a) if isinstance(a, VMIndex) else a, args)

        if self.stack_action == "push":
            i.push()

        yield self.form.format(*args)

        if self.stack_action == "pop":
            i.pop()

    def str(self):
        return [self.name, *self.args]


class CopyInstr(SimpleInstr):
    def __init__(self, name, target: Union[TOS, VMIndex], source: Union[TOS, VMIndex], stack_action="none"):
        form = "data modify entity @s {} set from entity @s {}"
        super().__init__(name, form, target, source, stack_action=stack_action)
