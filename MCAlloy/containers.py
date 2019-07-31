class Path:
    def __init__(self, namespace: str = None, module: str = None, frame: str = None, block: str = None):
        self.namespace = namespace
        self.module = module
        self.frame = frame
        self.block = block

        for i in range(0, 2):
            assert self[i] is not None or self[i+1] is None

    def altered(self, namespace="*", module="*", frame="*", block="*"):
        return Path(
            self.namespace if namespace == "*" else namespace,
            self.module if module == "*" else module,
            self.frame if frame == "*" else frame,
            self.block if block == "*" else block
        )

    def __getitem__(self, item):
        return [self.namespace, self.module, self.frame, self.block][item]

    def __str__(self):
        s = []

        d = [
            ("", self.namespace),
            (":", self.module),
            (".", self.frame),
            ("" if self.frame and self.frame.endswith("_") else "_", self.block)
        ]

        for pre, text in d:
            if text is not None:
                s.append(pre + text)

        return "".join(s)

    def file(self):
        s = ["data/"]

        if self.namespace is not None:
            s.append(self.namespace + "/functions/")
        if self.module is not None:
            s.append(self.module)
            if self.frame is not None:
                s.append("." + self.frame)
            if self.block is not None:
                s.append(("" if self.frame and self.frame.endswith("_") else "_") + self.block)

        return "".join(s)


class ILBlock:
    def __init__(self, path: Path):
        self.path = path
        self.instrs = []
        self.targets = []

    def push(self, command):
        self.instrs.append(command)

    def push_start(self, command):
        self.instrs.insert(0, command)


class ILFrame:
    def __init__(self, path: Path, code):
        self.path = path
        self.code = code
        self.root_block = None


class ILModule:
    def __init__(self, path: Path):
        self.path = path
        self.frames = []

    def push(self, frames: ILFrame):
        self.frames.append(frames)


class ILNamespace:
    def __init__(self, path: Path):
        self.path = path
        self.modules = []

    def push(self, module: ILModule):
        self.modules.append(module)
