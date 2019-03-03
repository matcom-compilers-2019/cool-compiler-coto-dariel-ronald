from coolex import lexer, data
from coolyacc import parser
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope
from error import ErrorLogger

ast = parser.parse(data,lexer,True)
scope = Scope()
tcv = TypeCollectorVisitor(scope)
errors = []
tcv.visit(ast,errors)

tbv = TypeBuilderVisitor(scope)
tbv.visit(ast,errors)

tchecv = TypeCheckerVisitor()
tchecv.visit(ast,scope,errors)

print(ErrorLogger(errors))






