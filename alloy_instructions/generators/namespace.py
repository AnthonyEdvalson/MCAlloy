import os

from alloy_instructions.alloy_assembler import assemble_alloy
from alloy_instructions.generators.module import assemble_module
from containers import ILNamespace
from containers import Path


class ILNamespaceGenerator:
    def __init__(self, path: Path, folder_path: str):
        self.path = path
        self.folder_path = folder_path
        self.name = self.path.namespace
        self.namespace = ILNamespace(self.path)

    def assemble(self) -> ILNamespace:
        for file in os.listdir(self.folder_path):
            mod_name = os.path.splitext(os.path.basename(file))[0]
            mod_file_path = os.path.join(self.folder_path, file)

            mod_il = assemble_module(self.path, mod_file_path, mod_name)

            self.namespace.push(mod_il)

        return self.namespace
