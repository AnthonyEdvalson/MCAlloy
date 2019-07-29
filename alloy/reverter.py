# RUNS IN PYTHON 3.4
import pickle
import base64
import marshal
import sys

while True:
    text = sys.stdin.read()

    if text == b"":
        break

    args = pickle.loads(base64.b85decode(text[:-1]))
    code = compile(*args)
    sys.stdout.write(base64.b64encode(marshal.dumps(code)).decode())
    sys.stdout.write("\n")
    sys.stdout.flush()
