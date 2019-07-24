import os
import shutil
from typing import List

from containers import ILNamespace, ILBlock
from vm import StackIndex


class DatapackGenerator:
    def __init__(self, gs):
        self.gs = gs

    def generate(self, dp_folder: str, namespaces: List[ILNamespace]):
        if not os.path.exists(dp_folder):
            os.makedirs(dp_folder)

        with open(dp_folder + "pack.mcmeta", "w+") as f:
            f.write('{\n')
            f.write('  "pack": {\n')
            f.write('    "pack_format": 3,\n')
            f.write('    "description": ""\n')
            f.write('  }\n')
            f.write('}\n')

        for namespace in namespaces:
            shutil.rmtree(dp_folder + namespace.path.file(), ignore_errors=True)
            for module in namespace.modules:
                for frame in module.frames:
                    si = StackIndex(-1)

                    self.generate_block(frame.root_block, dp_folder, si)

                    if si.i != 0:
                        raise Exception("WARNING: Alloy has compiled the stack to an invalid state ({})".format(si.i))

    def generate_block(self, block: ILBlock, dp_folder, si):
        file_name = dp_folder + block.path.file() + ".mcfunction"

        folder_path = os.path.dirname(file_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        print(file_name)

        with open(file_name, "w+") as output:
            for instr in block.instrs:
                print(instr)
                for command in instr.generate(si, self.gs):
                    output.write(command + "\n")

        prev_result_i = None

        for b in block.targets:
            si2 = StackIndex(si.i)
            self.generate_block(b, dp_folder, si2)

            if prev_result_i is not None and prev_result_i != si2.i:
                raise Exception("Branching path left stack in an undefined state")
            prev_result_i = si2.i

        if prev_result_i is not None:
            si.i = prev_result_i
