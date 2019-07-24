from abc import ABC

from alloy_instructions.asmcontext import AsmContext
from containers import Path, ILBlock


class Stub(ABC):
    def __init__(self, path: Path):
        self.path = path


class BlockStub(Stub):
    def __init__(self, path: Path,  ctx: AsmContext):
        super().__init__(path)
        self.ctx = ctx


class FrameStub(Stub):
    def __init__(self, path: Path, ctx: AsmContext, args, frames):
        super().__init__(path)
        self.ctx = ctx
        self.args = args
        self.frames = frames


class EvalFrameStub(FrameStub):
    def __init__(self, path: Path, ctx: AsmContext, frames):
        super().__init__(path, ctx, [], frames)


class Link:
    def __init__(self, target: ILBlock, conditional: bool):
        self.target = target
        self.conditional = conditional
