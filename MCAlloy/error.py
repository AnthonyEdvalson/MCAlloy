import sys


def ast_error(node, doc, msg):
    if hasattr(node, "lineno"):
        line = node.lineno
    else:
        line = None
    return doc_error(line, doc, msg)


def alloy_error(node, doc, msg):
    return doc_error(node.line, doc, msg)


def doc_error(line, doc, msg, pad=2):
    lines = doc.split("\n")

    start = max(0, line - pad)
    stop = min(len(lines) - 1, line + pad)

    gutter_width = len(str(stop))

    msg += "\n\n"

    for l in range(start, stop + 1):
        msg += ">> " if l == line else "   "
        msg += ("{:0>" + str(gutter_width) + "} {}\n").format(l, lines[l-1])

    print(msg, file=sys.stderr)
    quit(1)
