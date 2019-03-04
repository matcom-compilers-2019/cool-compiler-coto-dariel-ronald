from coolex import lexer, data
from coolyacc import parser
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope
from error import ErrorLogger


def compile_cool():
    ast = parser.parse(data, lexer)
    scope = Scope()
    tcv = TypeCollectorVisitor(scope)
    errors = []
    tcv.visit(ast, errors)

    tbv = TypeBuilderVisitor(scope)
    if not tbv.visit(ast, errors):
        print(str(ErrorLogger(errors)))
        return

    tchecv = TypeCheckerVisitor()
    if not tchecv.check_class_hierarchy(scope, errors):
        print(str(ErrorLogger(errors)))
        return
    #
    if not tchecv.visit(ast, scope, errors):
        print(str(ErrorLogger(errors)))

compile_cool()






