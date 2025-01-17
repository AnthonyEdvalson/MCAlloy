import ast
from ast import NodeVisitor
from dis import Bytecode
import error

from alloy.nodes import *
import types


class AlloyGenerator(NodeVisitor):
    def __init__(self, mod_path, doc, source_path):
        self.fptr_count = 0
        self.mod_path = mod_path
        self.module = None
        self.frame_stack = []
        self.block = None
        self.doc = doc
        self.source_path = source_path

        self.block_names = set()

    def frame_path(self):
        return self.frame_stack[-1].path

    def resolve_frame(self, nodes, code, name, args=None):
        self.frame_stack.append(Frame(self.module.path, name, code))
        old_block = self.block
        self.block = Block(self.frame_path(), None, True)
        self.frame_stack[-1].root_block = self.block
        self.bud(self.block, nodes, 0, None)
        self.frame_stack[-1].args = args or []
        self.block = old_block
        return self.frame_stack.pop()

    def bud(self, parent, nodes, line, name, condition=None):
        # iterate over all the nodes
        i = 0
        blocks_made = {None: 0, True: 0, False: 0}
        while i < len(nodes):
            full_name = self.make_block_name(line, condition, blocks_made, name)
            blocks_made[condition] += 1

            # Make a new block and link it to the parent
            self.block = Block(self.frame_path(), full_name)
            parent.links.append(Link(self.block, condition=condition))

            # Add nodes to the new bud block, unless it has to end (Return, If, While, etc.)
            # When the block has to end, break for the loop to make a new block
            while i < len(nodes):
                node = nodes[i]
                i += 1
                try:
                    if self.visit(node):
                        break
                except UnsupportedNodeException:
                    msg = "The '{}' feature is not supported by MCAlloy".format(type(node).__name__)
                    error.ast_error(node, self.doc, msg)

        return self.block  # Return the last block that was added

    @staticmethod
    def make_block_name(line, condition, blocks_made, name):
        blocks_label = blocks_made[condition] if blocks_made[condition] > 1 or condition is None else ""
        return "{}.{}".format(line, name or blocks_label)

    def write(self, node, target=None):
        target = target or self.block
        target.body.append(node)

    def visit_Module(self, node):
        self.module = Module(self.mod_path, self.source_path)
        module_code = compile(node, str(self.mod_path), "exec")
        frame = self.resolve_frame(node.body, module_code, "__module__")
        self.module.frames.append(frame)
        return self.module

    def find_code(self, node):
        name = node.name

        for const in self.frame_stack[-1].code.co_consts:
            if isinstance(const, types.CodeType) and const.co_name == name:
                return const

        raise NameError(error.ast_error(node, self.doc, "Cannot find code object for " + name))

    def visit_FunctionDef(self, node):
        parent = self.block

        args = [arg.arg for arg in node.args.args]
        code = self.find_code(node)
        frame_name = "{}.{}".format(self.frame_path().frame, node.name)
        frame = self.resolve_frame(node.body, code, frame_name, args)

        self.module.frames.append(frame)
        self.write(FunctionDef(node.lineno, frame_name, frame, self.get_fptr()), parent)

    def visit_ClassDef(self, node):
        self.unsupported(node)
        # code = self.find_code(node.name)
        # frame = self.resolve_frame(node.body, code, node.name)
        # self.module.frames.append(frame)
        # self.write(ClassDef(node.lineno, node.name, frame, self.get_fptr()))

    def visit_Return(self, node):
        self.visit(node.value)
        self.write(Return(node.lineno))
        return True

    def visit_While(self, node):
        """ Pre => Test  Test -> While  Test => Cont  While => Test """
        line = node.lineno

        pre = self.block
        test_block = self.bud(pre, [node.test], line, "test")
        while_block = self.bud(test_block, node.body, line, "while", True)
        while_block.links.append(Link(path=test_block.path))  # While always calls test when done
        return True

    def visit_If(self, node):
        """ Pre -> True  Pre -> False  Pre => Cont """
        line = node.lineno
        self.visit_eval(node.test)

        pre = self.block
        self.bud(pre, node.body, line, "true", True)
        self.bud(pre, node.orelse, line, "false", False)
        return True

    def visit_Expr(self, node):
        if isinstance(node.value, ast.Str) and node.value.s.startswith("/"):
            self.write(Direct(node.lineno, node.value.s[1:]))
        else:
            self.visit_exec(node)

    def visit_exec(self, node):
        code = compile(ast.Module(body=[node]), "", "exec")
        byte_code = list(Bytecode(code))[:-2]
        self.write(Byte(node.lineno, code, byte_code))

    def visit_eval(self, node):
        code = compile(ast.Expression(body=node, lineno=node.lineno, col_offset=node.col_offset), "", "eval")
        byte_code = list(Bytecode(code))[:-1]
        self.write(Byte(node.lineno, code, byte_code))

    def get_fptr(self):
        v = self.fptr_count
        self.fptr_count += 1
        return v

    def unsupported(self, node):
        raise UnsupportedNodeException(node)

    # Simple exec
    visit_Assign = visit_exec
    visit_AugAssign = visit_exec
    visit_AnnAssign = visit_exec
    visit_Pass = visit_exec

    # Simple eval
    visit_BoolOp = visit_eval
    visit_BinOp = visit_eval
    visit_UnaryOp = visit_eval
    visit_Compare = visit_eval
    visit_Call = visit_eval
    visit_Num = visit_eval
    visit_Str = visit_eval
    visit_NameConstant = visit_eval
    visit_Constant = visit_eval
    visit_Name = visit_eval
    visit_Attribute = visit_eval

    # Not Yet Implemented
    visit_IfExp = unsupported  # Should be identical to If, but tricky to implement since it's inside an eval

    visit_For = unsupported  # ClassDef
    visit_Break = unsupported
    visit_Continue = unsupported

    visit_With = unsupported  # ClassDef

    visit_Raise = unsupported  # ClassDef
    visit_Try = unsupported  # Raise
    visit_Assert = unsupported  # Raise
    visit_ExceptHandler = unsupported  # Try

    visit_Import = unsupported
    visit_ImportFrom = unsupported  # Import

    visit_Global = unsupported
    visit_Nonlocal = unsupported

    visit_Lambda = unsupported

    visit_Dict = unsupported  # Possible?
    visit_DictComp = unsupported  # Dict

    visit_Set = unsupported  # Possible?
    visit_SetComp = unsupported  # Set

    visit_GeneratorExp = unsupported  # Possible?
    visit_Yield = unsupported  # GeneratorExp
    visit_YieldFrom = unsupported  # Yield

    visit_Starred = unsupported

    visit_Tuple = unsupported  # ClassDef
    visit_List = unsupported  # ClassDef
    visit_ListComp = unsupported  # List
    visit_Subscript = unsupported  # List|Tuple
    visit_Slice = unsupported  # Subscript
    visit_Index = unsupported  # Subscript
    visit_Delete = unsupported  # List

    # Impossible
    visit_Interactive = unsupported
    visit_Expression = unsupported
    visit_AsyncFunctionDef = unsupported
    visit_AsyncFor = unsupported
    visit_AsyncWith = unsupported
    visit_Await = unsupported
    visit_FormattedValue = unsupported
    visit_JoinedStr = unsupported
    visit_Bytes = unsupported

    # Ones to add if people ask for
    visit_ExtSlice = unsupported  # A bit much, I've never needed it, and it would probably be slow
    visit_Ellipsis = unsupported  # Didn't know it existed before starting this project, doesnt seem particularly useful


class UnsupportedNodeException(Exception):
    def __init__(self, node):
        self.node = node
