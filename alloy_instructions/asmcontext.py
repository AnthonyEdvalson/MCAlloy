from symbol_table import SymbolTable


class AsmContext:
    def __init__(self, st: SymbolTable, doc, code, alloy):
        self.st = st
        self.doc = doc
        self.code = code
        self.alloy = alloy

    def frame_start(self, class_name):
        self.st.push_layer("Frame" if class_name is None else class_name)

    def frame_end(self):
        self.st.pop_layer()
