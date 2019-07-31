import ast
from dis import dis

from alloy.generator import AlloyGenerator
from assembler.alloy_assembler import assemble_alloy
from instrs import InitContext, Call, Load
from containers import ILModule, ILFrame, ILBlock
from vm import ConstIndex


def assemble_module(path, file_path, name):
    gen = ILModuleGenerator(path, file_path, name)
    return gen.assemble()


class ILModuleGenerator:
    def __init__(self, path, file_path, name):
        self.file_path = file_path
        self.path = path.altered(module=name)
        self.module = ILModule(self.path)
        self.mod_path = self.path.altered(frame="__module__")

    def assemble(self) -> ILModule:
        with open(self.file_path, "r") as f:
            source_text = f.read()
        dis(source_text)

        tree = ast.parse(source_text)

        gen = AlloyGenerator(self.mod_path)
        alloy = gen.visit(tree)
        alloy.pprint()

        return assemble_alloy(source_text, alloy)

    def launch_frame(self, mod_ctx):
        frame = ILFrame(self.path, mod_ctx.code)
        frame.root_block = ILBlock(self.path)
        frame.root_block.push(InitContext(mod_ctx.code))
        frame.root_block.push(Call(self.mod_path))
        frame.root_block.push(Load(ConstIndex(0)))

        return frame
