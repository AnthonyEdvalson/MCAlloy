from typing import List

from containers import Path
from errors import NotFoundError
from util import escape
from vm import NameIndex


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
