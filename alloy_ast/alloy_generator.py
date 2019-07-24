import ast
from ast import NodeVisitor
from dis import Bytecode

from alloy_ast.nodes import *


class AlloyGenerator(NodeVisitor):

    def __init__(self, mod_path):
        self.mod_path = mod_path
        self.module = None
        self.frame = None
        self.block = None

        self.frame_stack = [None]

    def resolve(self, child):
        if isinstance(child, ast.AST):
            self.visit(child)
        if isinstance(child, list):
            for item in child:
                self.visit(item)

    def resolve_frame(self, nodes, name=None):
        self.frame = Frame(self.mod_path, name)
        path = self.frame.path
        self.module.frames.append(self.frame)
        self.frame_stack.append(self.frame)

        self.resolve_block(nodes, None, None)

        self.frame_stack.pop()
        self.frame = self.frame_stack[-1]
        return path

    def resolve_block(self, nodes, parent_block, name, next_block_path: Path):
        old_block = self.block
        path = self.start_block(parent_block, name)
        [self.visit(node) for node in nodes]
        self.visit()  # TODO
        self.block = old_block
        return path

    def start_block(self, parent_block, name):
        block = Block(self.frame.path, name)

        if parent_block is not None:
            parent_block.targets.append(block)
        else:
            self.frame.root_block = block

        self.block = block
        return block.path

    def write(self, node, target=None):
        if target is None:
            target = self.block
        target.body.append(node)

    def visit_Module(self, node):
        self.module = Module(self.frame)
        self.resolve_frame(node.body)
        return self.module

    def visit_FunctionDef(self, node):
        args = [Arg(arg.arg) for arg in node.args.args]
        frame_path = self.resolve_frame(node.body, node.name)
        self.write(FunctionDef(node.lineno, node.name, args, frame_path))

    def visit_Return(self, node):
        self.resolve(node.value)
        self.write(Return(node.lineno))
        self.start_block(self.block, "{}return".format(node.lineno))

    def visit_For(self, node):
        raise NotImplementedError(":(")

    def visit_While(self, node):
        raise NotImplementedError(":(")

    def visit_If(self, node):
        l = node.lineno
        self.visit_eval(node.test)
        parent_block = self.block

        cont_path = self.start_block(parent_block, "{}cont".format(l))
        true_path = self.resolve_block(node.body, parent_block, "{}true".format(l), cont_path)
        false_path = self.resolve_block(node.orelse, parent_block, "{}false".format(l), cont_path)

        self.write(If(l, true_path, false_path, cont_path), parent_block)

    def visit_Break(self, node):
        raise NotImplementedError(":(")

    def visit_Continue(self, node):
        raise NotImplementedError(":(")

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

    def unsupported(self, node):
        raise Exception("{} is not a supported AST node".format(type(node)))

    visit_Assign = visit_exec
    visit_AugAssign = visit_exec
    visit_AnnAssign = visit_exec

    visit_Interactive = unsupported
    visit_Expression = unsupported
    visit_AsyncFunctionDef = unsupported
    visit_ClassDef = unsupported
    visit_Delete = unsupported
    visit_AsyncFor = unsupported
    visit_With = unsupported
    visit_AsyncWith = unsupported
    visit_Raise = unsupported
    visit_Try = unsupported
    visit_Assert = unsupported
    visit_Import = unsupported
    visit_ImportFrom = unsupported
    visit_Global = unsupported
    visit_Nonlocal = unsupported
    visit_Pass = unsupported
