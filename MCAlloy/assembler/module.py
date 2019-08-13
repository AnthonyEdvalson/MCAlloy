import ast

import error
from alloy.generator import AlloyGenerator
from assembler.alloy_assembler import assemble_alloy
from instrs import InitContext, Call
from containers import ILModule, ILFrame, ILBlock


def assemble_module(path, file_path, name):
    gen = ILModuleGenerator(path, file_path, name)
    return gen.assemble()


class ILModuleGenerator:
    def __init__(self, path, file_path, name):
        self.file_path = file_path
        self.path = path.altered(module=name)
        self.module = ILModule(self.path, file_path)
        self.mod_path = self.path.altered(frame="__module__")

    def assemble(self) -> ILModule:
        with open(self.file_path, "r") as f:
            source_text = f.read()

        # dis(source_text)
        try:
            tree = ast.parse(source_text)
        except SyntaxError as e:
            error.doc_error(e.lineno, source_text, e.msg)
            raise  # Never reached, since doc_error calls quit()

        gen = AlloyGenerator(self.mod_path, source_text, self.file_path)
        alloy = gen.visit(tree)
        # alloy.pprint()

        module = assemble_alloy(source_text, alloy)
        module.push(self.launch_frame())

        return module

    def launch_frame(self):
        frame = ILFrame(self.path, None)
        frame.root_block = ILBlock(self.path)
        frame.root_block.push(InitContext(0))
        frame.root_block.push(Call(self.mod_path))

        return frame
