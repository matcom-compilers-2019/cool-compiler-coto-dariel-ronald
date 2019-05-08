from NodosAST import *
from coolyacc import parser
from .tools_for_testing import verify_asts

from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from utils import Scope


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


def test_first():
    program_ast = ProgramNode([ClassNode('Main', features=[
        MethodNode('main', [], 'SELF_TYPE',DispatchNode('out_string', [StrNode('"Hello, World"')], None))
    ], inherit='IO')])
    program_code = '''
    
    class Main inherits IO {
         main(): SELF_TYPE {
	        out_string("Hello, World")
    };
};
    '''
    parser_result = parser.parse(program_code)
    verify_asts(program_ast, parser_result, Node)

    check_semantic(program_ast)


