def escape(s: str) -> str:
    chars = [("\\", "\\"), ("\"", "\""), ("\n", "n"), ("\t", "t")]
    for char in chars:
        s = s.replace(char[0], "\\" + char[1])
    return s
