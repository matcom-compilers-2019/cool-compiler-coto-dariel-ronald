from coolex import lexer
from coolyacc import parser
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope
import fileinput
from cool_errors import CoolErrorLogger
from tqdm import tqdm


def main():
    print(CoolErrorLogger([]))
    print('Loading data...')
    data = ''
    for line in tqdm(fileinput.input()):
        data += line

    compile_cool(data)

def check_semantic(ast):

    scope = Scope()
    tcv = TypeCollectorVisitor(scope)
    tcv.visit(ast)

    tbv = TypeBuilderVisitor(scope)
    tbv.visit(ast)

    tchecv = TypeCheckerVisitor()
    tchecv.check_class_hierarchy(scope)
    tchecv.look_for_Main_Class(scope)
    tchecv.visit(ast, scope)


def compile_cool(data):
    ast = parser.parse(data, lexer, True)

    check_semantic(ast)









