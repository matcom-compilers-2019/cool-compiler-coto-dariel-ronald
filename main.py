from coolex import lexer, data
from coolyacc import parser
from semantic import TypeCollectorVisitor

ast = parser.parse(data,lexer,True)

tcv = TypeCollectorVisitor()
tcv.visit(ast,None)

print(tcv.context._classes_field())


