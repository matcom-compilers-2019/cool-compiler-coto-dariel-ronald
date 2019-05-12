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


def test_hello_world():
    program_ast = ProgramNode([ClassNode('Main', features=[
        MethodNode('main', [], 'IO',DispatchNode('out_string', [StrNode('"Hello, World"')], None))
    ], inherit='IO')])
    program_code = '''
    
    class Main inherits IO {
         main(): IO {
	        out_string("Hello, World")
    };
};
    '''
    parser_result = parser.parse(program_code)
    verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)


def test_new_type_node_and_let_node():
    program_ast = ProgramNode([ClassNode('Main', features=[
        MethodNode('main', [], 'Int',
                   BlockNode([
                        LetVarNode([(('io','IO'),NewTypeNode('IO'))],
                                   DispatchNode('out_string',
                                                [StrNode('"Hello World"')],ObjectNode('io'))),
                        IntNode(0)
        ]))
    ])])
    program_code = '''
   class Main {
    main() : Int {
	{
	    let io: IO <- new IO in io.out_string("Hello World");
	    0;
	}
    };
};
    '''
    parser_result = parser.parse(program_code)
    verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)


def test_new_type_node_and_let_node2():
    program_ast = ProgramNode(
        [ClassNode('Main', features=[
            MethodNode('main', [], 'Int',
                       BlockNode([
                            LetVarNode([(('io','IO'),NewTypeNode('IO'))],
                                       DispatchNode('out_string',
                                                    [StrNode('"Hello World"')],ObjectNode('io'))),
                            LetVarNode([(('a','A'),NewTypeNode("A")),(('b','Int'),None)],
                                       PlusNode(DispatchNode('funk',[(BoolNode('true'))], ObjectNode('a')),
                                                ObjectNode('b')))
            ]))
    ]),
         ClassNode('A',features=[
                MethodNode('funk',[('a','Int')],'Int',
                            LetVarNode([(('x','Int'),None)],PlusNode(ObjectNode('x'),IntNode(1)))
                           )
            ])
         ])
    program_code = '''
   class Main {
    main() : Int {
            {
                let io: IO <- new IO in io.out_string("Hello World");
                let a:A <- new A, b: Int in a.funk() + b;
            }
        };
    };
    class A {
       funk():Int {
            let x:String in x + 1
       };
    };

    '''
    parser_result = parser.parse(program_code)
    # verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)


