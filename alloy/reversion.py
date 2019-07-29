import ast
import pickle
import base64
import marshal
from subprocess import Popen, PIPE


#p = Popen(['Py34\\python.exe', 'alloy\\reverter.py'], stdout=PIPE, stdin=PIPE)


def reverted_bytes(node, mode):
    """
    Get the bytecode for the given ast in python 3.4
    :return:
    """

    args = None
    if mode == "exec":
        args = (ast.Module(body=[node]), "", "exec")
    elif mode == "eval":
        args = (ast.Expression(body=node, lineno=node.lineno, col_offset=node.col_offset), "", "eval")

    return compile(*args)

    content = base64.b85encode(pickle.dumps(args))

    try:
        p.stdin.write(content)
        p.stdin.write(b"\n")
        p.stdin.flush()
        result = p.stdout.read()
    except Exception as e:
        raise Exception("Failed to convert {} to bytecode".format(node)) from e

    code = marshal.loads(base64.b64decode(result))
    return code
