def escape(s: str) -> str:
    chars = [("\\", "\\"), ("\"", "\""), ("\n", "n"), ("\t", "t")]
    for char in chars:
        s = s.replace(char[0], "\\" + char[1])
    return s


def to_nbt(value, hard_fail=True) -> str:
    type_name = type(value)

    if type_name is str:
        nbt = '"\\"{}\\""'.format(escape(value).replace("\\n", "\\\\n"))  # TODO clean up escaping
    elif type_name is bool:
        nbt = "1b" if value else "0b"
    elif type_name is int:
        nbt = str(value)
    elif type_name is float:
        nbt = str(value) + "f"
    elif value is None:
        nbt = "{}"
        type_name = "none"
    else:
        if hard_fail:
            raise Exception("Cannot convert {} to NBT".format(type_name))
        else:
            return "{}"

    return '{{v:{}, t:"{}"}}'.format(nbt, type_name)