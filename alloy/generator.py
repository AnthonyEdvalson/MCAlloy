import ast
from ast import NodeVisitor
from dis import Bytecode

from alloy.nodes import *
import types


class AlloyGenerator(NodeVisitor):
    def __init__(self, mod_path):
        self.mod_path = mod_path
        self.module = None
        self.frame = None
        self.block = None

    def resolve(self, child):
        if isinstance(child, ast.AST):
            self.visit(child)
        if isinstance(child, list):
            for item in child:
                self.visit(item)

    def resolve_frame(self, nodes, code, name):
        old_frame = self.frame
        frame = Frame(self.mod_path, name, code)

        self.frame = frame
        root_block = self.resolve_block(nodes, None)
        self.frame.root_block = root_block

        self.frame = old_frame
        return frame

    def resolve_block(self, nodes, name):
        old_block = self.block
        block = Block(self.frame.path, name)

        self.block = block
        [self.visit(node) for node in nodes]
        self.block = old_block

        return block

    def start_block(self, parent_block, name):
        block = Block(self.frame.path, name)

        if parent_block is not None:
            block.bridge_to(parent_block.bridge)
            parent_block.bridge_to(block.path)
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
        frame = self.resolve_frame(node.body, compile(node, str(self.mod_path), "exec"), None)
        self.module.frames.append(frame)
        return self.module

    def find_function(self, name):
        for const in self.frame.code.co_consts:
            if isinstance(const, types.CodeType) and const.co_name == name:
                return const
        raise NameError("No function named " + name)

    def visit_FunctionDef(self, node):
        args = [Arg(arg.arg) for arg in node.args.args]
        code = self.find_function(node.name)
        frame = self.resolve_frame(node.body, code, node.name)
        self.module.frames.append(frame)
        self.write(FunctionDef(node.lineno, node.name, args, frame))

    def visit_Return(self, node):
        self.resolve(node.value)
        self.write(Return(node.lineno))
        self.start_block(self.block, "{}return".format(node.lineno))

    def visit_While(self, node):
        """ Pre => Test  Test -> While  Test => Cont  While => Test """
        line\
            = node.lineno
        parent_block = self.block

        test_block = self.resolve_block([node.test], "{}test".format(line))

        while_block = self.resolve_block(node.body, "{}while".format(line))

        self.start_block(test_block, "{}cont".format(line))
        cont_block = self.block

        parent_block.bridge_to(test_block)
        parent_block.target(test_block)
        test_block.bridge_to(cont_block)
        test_block.target(cont_block)
        test_block.target(while_block)
        while_block.bridge_to(test_block)

        # TODO current flow leaves a ton of stackframes behind, if the while loop run 100 times, those stackframes
        #  are not removed after exiting the loop, and will continue to accumulate as the program executes
        #  Current is  Pre => Test    Test -> While  Test => Cont  While => Test
        #  Better is   Pre call Test  Test -> While  Test => X     While => Test  Pre => Cont

        self.write(While(line, test_block.path, while_block.path, cont_block.path), test_block)

    def visit_If(self, node):
        """ Pre -> True  Pre -> False  Pre => Cont  True => X  False => X """
        line = node.lineno
        self.visit_eval(node.test)
        parent_block = self.block

        cont_path = self.start_block(parent_block, "{}cont".format(line))

        true_block = self.resolve_block(node.body, "{}true".format(line))
        false_block = self.resolve_block(node.orelse, "{}false".format(line))

        self.block.targets.append(true_block)
        self.block.targets.append(false_block)

        self.write(If(line, true_block.path, false_block.path, cont_path), parent_block)

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

    # Not Yet Implemented
    visit_IfExp = unsupported  # Should be identical to If

    visit_ClassDef = unsupported
    visit_Attribute = unsupported  # ClassDef

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

    # Impossible / Useless
    visit_Interactive = unsupported
    visit_Expression = unsupported
    visit_AsyncFunctionDef = unsupported
    visit_AsyncFor = unsupported
    visit_AsyncWith = unsupported
    visit_Await = unsupported
    visit_FormattedValue = unsupported
    visit_JoinedStr = unsupported
    visit_Bytes = unsupported

    # Ones I'll add if people ask for
    visit_Delete = unsupported  # Never used del, no idea why anyone would want it
    visit_ExtSlice = unsupported  # A bit much, I've never needed it, and it would probably be slow
    visit_Ellipsis = unsupported  # Didn't know it existed before starting this project, doesnt seem particularly useful






