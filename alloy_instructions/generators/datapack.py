import os
from typing import List

from alloy_instructions.generators.namespace import ILNamespaceGenerator
from containers import ILNamespace, Path


class ILDatapackGenerator:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.name = os.path.basename(os.path.normpath(self.folder_path))

    def assemble(self) -> List[ILNamespace]:
        namespaces = []
        for namespace in os.listdir(self.folder_path):
            ns_path = os.path.join(self.folder_path, namespace)
            path = Path(namespace)

            il_namespace_gen = ILNamespaceGenerator(path, ns_path)
            ns = il_namespace_gen.assemble()
            namespaces.append(ns)

        return namespaces