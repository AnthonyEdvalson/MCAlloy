from dis import Bytecode

from alloy_ast.nodes import Byte
from alloy_instructions.generators.block import assemble_block
from alloy_instructions.generators.util import FrameStub, BlockStub
from commands import InitFrame, Comment, NameIndex
from containers import ILFrame


def assemble_frame(stub: FrameStub):
    gen = ILFrameGenerator(stub)
    gen.assemble()
    return gen.frames


class ILFrameGenerator:
    def __init__(self, stub: FrameStub):
        self.path = stub.path
        self.ctx = stub.ctx
        self.args = stub.args

        self.frames = stub.frames
        self.frame = ILFrame(self.path)
        self.frames.append(self.frame)

        self.frame_stubs = []
        self.special_stack = []

    def write(self, command):
        self.frame.root_block.push(command)

    def write_start(self, command):
        self.frame.root_block.push_start(command)

    def assemble(self) -> ILFrame:
        stub = BlockStub(self.path, self.ctx)

        # TODO make this an actual Return node
        #ret = list(Bytecode(self.ctx.code))[-2:]
        #stub.ctx.alloy.frame.block.body.append(Byte(None, None, ret))

        block = assemble_block(stub)

        self.frame.root_block = block
        self.frame_start()
        self.frame_end()

        return self.frame

    def frame_start(self):
        self.ctx.frame_start(None)
        for arg in self.args:
            self.ctx.st.add_symbol(NameIndex(arg.name))

        self.write_start(Comment("Start Scope {}".format(self.path), 0))
        self.write_start(InitFrame(0))

    def frame_end(self):
        self.write(Comment("End Scope {}".format(self.path), None))
        self.ctx.frame_end()
