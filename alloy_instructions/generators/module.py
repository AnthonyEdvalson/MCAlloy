import ast
from dis import dis

import astpretty

from alloy_ast.converter import convert
from alloy_instructions.alloy_assembler import assemble_alloy
from alloy_instructions.asmcontext import AsmContext
from alloy_instructions.generators.util import EvalFrameStub
from alloy_instructions.generators.frame import assemble_frame
from commands import InitContext, Call, LoadConst
from containers import ILModule, ILFrame, ILBlock
from symbol_table import SymbolTable
from vm import ConstIndex


def assemble_module(path, file_path, name):
    gen = ILModuleGenerator(path, file_path, name)
    return gen.assemble()


class ILModuleGenerator:
    def __init__(self, path, file_path, name):
        self.file_path = file_path
        self.path = path.altered(module=name)
        self.module = ILModule(self.path)
        self.mod_path = self.path.altered(frame="_.module")

        self.ctx = None

    def assemble(self) -> ILModule:
        with open(self.file_path, "r") as f:
            source_text = f.read()
        dis(source_text)

        tree = ast.parse(source_text)
        astpretty.pprint(tree)
        alloy = convert(tree, self.mod_path)
        alloy.pprint()

        st = SymbolTable()
        st.push_builtins()
        self.ctx = AsmContext(st, source_text, compile(source_text, str(self.path), "exec"), alloy)

        return assemble_alloy(self.mod_path, source_text, alloy)
        """
        frames = []
        stub = EvalFrameStub(self.mod_path, self.ctx, frames)
        assemble_frame(stub)

        frames.append(self.launch_frame(self.ctx))

        for frame in frames:
            self.module.push(frame)

        return self.module
        """

    def launch_frame(self, mod_ctx):
        frame = ILFrame(self.path)
        frame.root_block = ILBlock(self.path)
        frame.root_block.push(InitContext(mod_ctx.code, 0))
        frame.root_block.push(Call(self.mod_path, 1))
        frame.root_block.push(LoadConst(ConstIndex(0), 2))

        return frame



"""
            mod_name = os.path.splitext(os.path.basename(file))[0]
            mod_file_path = os.path.join(self.folder_path, file)
            mod_path = self.path.altered(module=mod_name)

            with open(mod_file_path, "r") as f:
                source_text = f.read()
            dis(source_text)

            tree = ast.parse(source_text)
            astpretty.pprint(tree)
            alloy = convert(tree)
            alloy.pprint()

            st = SymbolTable()
            st.push_builtins()
            ctx = AsmContext(BareContext(st, source_text), alloy)
            stub = ModuleStub(mod_path, ctx)
            mod_il = assemble_module(stub)

            self.namespace.push(mod_il)"""