import os
import shutil
from collections import OrderedDict
from typing import List

from containers import ILNamespace, ILBlock
from vm import StackIndex
import json


class DatapackGenerator:
    def __init__(self, gs):
        self.gs = gs
        self.stack_histories = OrderedDict()
        self.files_made = set()

    def generate(self, dp_folder: str, namespaces: List[ILNamespace]):
        if not os.path.exists(dp_folder):
            os.makedirs(dp_folder)

        with open(dp_folder + "pack.mcmeta", "w+") as f:
            json.dump({
                "pack": {
                    "pack_format": 3,
                    "description": ""
                }
            }, f)

        for namespace in namespaces:
            shutil.rmtree(dp_folder + namespace.path.file(), ignore_errors=True)
            for module in namespace.modules:
                for frame in module.frames:

                    si = StackIndex(-1)

                    self.generate_block(frame.root_block, dp_folder, si)

                    if si.index != -1:
                        stack_detail = ""
                        for file, hist in list(self.stack_histories.items()):
                            lines = [file]
                            lines.extend(["{}{}".format("|" * (i + 1), instr.str()[0]) for instr, i in hist])
                            stack_detail += "\n\n" + "\n".join(lines)
                        msg = "WARNING: Alloy has compiled the stack to an invalid state ({})\n{}"
                        raise Exception(msg.format(si.index, stack_detail))

                    self.stack_histories = OrderedDict()

    def generate_block(self, block: ILBlock, dp_folder, si: StackIndex):
        file_name = dp_folder + block.path.file() + ".mcfunction"

        folder_path = os.path.dirname(file_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        print()
        print(file_name)
        if file_name in self.files_made:
            raise Exception("{} has already been created".format(file_name))
        self.files_made.add(file_name)

        self.stack_histories[file_name] = []
        with open(file_name, "w+") as output:
            for instr in block.instrs:
                print(instr)
                for command in instr.generate(si, self.gs):
                    output.write(command + "\n")

                self.stack_histories[file_name].append((instr, si.index))

        for b in block.targets:
            si2 = StackIndex(si.index)
            self.generate_block(b, dp_folder, si2)
