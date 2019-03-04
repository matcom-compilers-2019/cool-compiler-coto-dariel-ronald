from coolex import lexer, data
from coolyacc import parser
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope
from error import ErrorLogger,SyntacticError


def compile_cool():
    ast = parser.parse(data, lexer,True)
    if ast is None:
        print(ErrorLogger([SyntacticError(0,0,'SyntaxError')]))
        return
    scope = Scope()
    tcv = TypeCollectorVisitor(scope)
    errors = []
    tcv.visit(ast, errors)

    tbv = TypeBuilderVisitor(scope)
    if not tbv.visit(ast, errors):
        errors.append('Exited code 1')
        print(str(ErrorLogger(errors)))
        return

    tchecv = TypeCheckerVisitor()
    if not tchecv.check_class_hierarchy(scope, errors):
        errors.append('Exited code 1')
        print(str(ErrorLogger(errors)))
        return
    #
    if not tchecv.visit(ast, scope, errors):
        errors.append('Exited code 1')
        print(str(ErrorLogger(errors)))
        return

    print(str(ErrorLogger(['Exited code 0'])))
compile_cool()






