from typing import List

from containers import Path
from errors import NotFoundError
from util import escape
from vm import NameIndex


class Arg:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Func:
    def __init__(self, path: Path, args: List[Arg], code):
        self.path = path
        self.args = args
        self.code = code
        self.i = path.frame

    def __str__(self):
        return "{}({})".format(self.i, ",".join(map(str, self.args)))


def to_nbt(value, hard_fail=True) -> str:
    type_name = type(value).__name__

    if type_name == "str":
        nbt = '"\\"{}\\""'.format(escape(value).replace("\\n", "\\\\n"))  # TODO clean up escaping
    elif type_name == "bool":
        nbt = "1b" if value else "0b"
    elif type_name == "int":
        nbt = str(value)
    elif type_name == "float":
        nbt = str(value) + "f"
    else:
        if hard_fail:
            raise Exception("Cannot convert {} to NBT".format(type_name))
        else:
            return "{}"

    return '{{v:{}, t:"{}"}}'.format(nbt, type_name)


class SymbolTable:
    def __init__(self):
        self.layers = []
        self.layer_names = []
        self.all_sym_names = set()

    def push_builtins(self):
        self.layers.append({})
        self.layer_names.append("Globals")

    def push_layer(self, name: str) -> int:
        self.layers.append({})
        self.layer_names.append(name)
        return len(self.layers) - 1

    def pop_layer(self) -> int:
        self.layers.pop(-1)
        self.layer_names.pop(-1)
        return len(self.layers) - 1

    def has_symbol(self, name: NameIndex):
        for layer in self.layers:
            if name.i in layer:
                return True
        return False

    def add_symbol(self, sym, layer_index: int=None):
        layer_index = -1 if layer_index is None else layer_index

        layer = self.layers[layer_index]
        name = sym.i
        if name in layer:
            raise Exception("{} Already exists".format(name))

        layer[name] = sym
        self.all_sym_names.add(sym.i)

    def get_symbol(self, name_index: NameIndex):
        name = name_index.i
        for layer in reversed(self.layers):
            if name in layer:
                return layer[name]
        raise NotFoundError("Cannot find {}".format(name))

    def get_all_symbol_names(self) -> set:
        return self.all_sym_names
