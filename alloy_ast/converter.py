import ast
import astpretty

from alloy_ast.alloy_generator import AlloyGenerator


def convert(ast, path):
    astpretty.pprint(ast)
    gen = AlloyGenerator(path)

    alloy = gen.visit(ast)
    alloy.pprint()

    return alloy
