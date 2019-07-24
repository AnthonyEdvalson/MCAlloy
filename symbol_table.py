from abc import ABC, abstractmethod
from typing import Tuple, List, Dict

from containers import Path
from errors import InvalidTypeError, NotFoundError
from util import escape
from vm import NameIndex


class Symbol(ABC):
    def __init__(self, name: str, type_name: str):
        self.name = name
        self.type_name = type_name

    def try_set_type(self, source_type: str):
        if self.type_name == "unset":
            self.type_name = source_type


class Arg:
    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return self.name


class Func(Symbol):
    def __init__(self, path: Path, args: List[Arg], code):
        super().__init__(path.frame, "func")
        self.path = path
        self.args = args
        self.code = code

    def __str__(self):
        return "{}({})".format(self.name, ",".join(map(str, self.args)))


class VMSymbol(Symbol):
    def __init__(self, name, type_name):
        super().__init__(name, type_name)

    @abstractmethod
    def nbt(self) -> str:
        pass

    def full_nbt(self, hard_fail=True) -> str:
        try:
            return '{{{}:{}, t:"{}"}}'.format(self.name, self.nbt(), self.type_name)
        except:
            if hard_fail:
                raise
            else:
                return "{}"


class Val(VMSymbol):
    def nbt(self):
        return "{}"


class Object(VMSymbol):
    def __init__(self, name, type_name, attributes: Dict[str, VMSymbol]):
        super().__init__(name, type_name)
        self.attributes = attributes

    def get(self, name):
        return self.attributes[name]

    def nbt(self):
        s = []
        for name, symbol in self.attributes.items():
            s.append("{}:{}".format(name, symbol.nbt()))
        return "{{{}}}".format(",".join(s))


class Const(VMSymbol):
    def __init__(self, value):
        type_name = type(value).__name__

        super().__init__("v", type_name)
        self.value = value

    def __str__(self):
        if self.type_name == "str":
            return '"{}"'.format(self.value)
        return self.nbt()

    def to_int(self):
        if self.type_name == "int":
            return self.value
        if self.type_name == "bool":
            return 1 if self.value else 0

        raise InvalidTypeError("int or bool", self.type_name)

    def nbt(self) -> str:
        if self.type_name == "str":
            return '"\\"{}\\""'.format(escape(self.value).replace("\\n", "\\\\n"))  # TODO clean up escaping
        elif self.type_name == "bool":
            return "1b" if self.value else "0b"
        elif self.type_name == "int":
            return str(self.value)
        elif self.type_name == "float":
            return str(self.value) + "f"
        else:
            raise Exception("Cannot convert {} to NBT".format(self.type_name))


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
            if name.name in layer:
                return True
        return False

    def add_symbol(self, sym: Symbol, layer_index: int=None) -> Tuple[Symbol, bool]:
        layer_index = -1 if layer_index is None else layer_index

        layer = self.layers[layer_index]
        name = sym.name
        if name in layer:
            raise Exception("{} Already exists".format(name))

        layer[name] = sym
        self.all_sym_names.add(sym.name)

    def get_symbol(self, name_index: NameIndex) -> Symbol:
        name = name_index.name
        for layer in reversed(self.layers):
            if name in layer:
                return layer[name]
        raise NotFoundError("Cannot find {}".format(name))

    def get_all_symbol_names(self) -> List[str]:
        return self.all_sym_names

    def copy(self):
        st = SymbolTable()
        for layer, name in zip(self.layers, self.layer_names):
            st.layers.append(layer.copy())
            st.layer_names.append(name)
        st.all_sym_names = self.all_sym_names
        return st

    def copy_layer(self, layer_index=-1):
        st = SymbolTable()
        st.layers.append(self.layers[layer_index])
        st.layer_names.append(self.layer_names[layer_index])
        st.all_sym_names = self.all_sym_names
        return st
