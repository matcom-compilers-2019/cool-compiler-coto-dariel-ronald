from NodosAST import *
from coolyacc import parser
from .tools_for_testing import verify_asts
from coolex import lexer
from semantic import TypeCollectorVisitor, TypeBuilderVisitor, TypeCheckerVisitor
from cool_utils import Scope


def check_semantic(ast):

    scope = Scope()

    tchecv = TypeCheckerVisitor()
    tchecv.visit(ast, scope)


def test_hello_world():
    program_ast = ProgramNode([ClassNode('Main', features=[
        MethodNode('main', [], 'IO',DispatchNode('out_string', [StrNode('"Hello, World"')], None))
    ], inherit='IO')])
    program_code = '''
    
    class Main inherits IO {
         main(): IO {
            --Hola afafaf--
	        out_string("Hello, World")
    };
};
    '''
    parser_result = parser.parse(program_code,lexer=lexer)
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
    parser_result = parser.parse(program_code,lexer=lexer)
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
                MethodNode('funk',[('a','Bool')],'Int',
                            LetVarNode([(('x','Int'),None)],
                                       PlusNode(ObjectNode('x'),IntNode(1)))
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
            let x:Int in x + 1
       };
    };

    '''
    parser_result = parser.parse(program_code,lexer=lexer)
    # verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)

def test_conditional():
        program_ast = ProgramNode(
            [ClassNode('Main', features=[
                MethodNode('main', [], 'IO',
                   BlockNode([
                       ConditionalNode(LowerEqualThanNode(IntNode(2),IntNode(3)),
                           LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                      DispatchNode('out_string',
                                                   [StrNode('"True"')], ObjectNode('io'))),
                           LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                      DispatchNode('out_string',
                                                   [StrNode('"False"')], ObjectNode('io')))
                       )
                   ]))
            ])
             ])
        program_code = '''
       class Main {
            main() : IO {
                   {
                   
                        if 2<=3 then let io: IO <- new IO in io.out_string("True") 
                        else let io: IO <- new IO in io.out_string("False") fi;
                   }
            };
        };

        '''
        parser_result = parser.parse(program_code, lexer=lexer)
        verify_asts(program_ast, parser_result, Node)
        check_semantic(program_ast)


def test_loop_check():
    program_ast = ProgramNode(
        [ClassNode('Main', features=[
            MethodNode('main', [], 'Object',
                LoopNode(BoolNode('true'),
                     BlockNode([
                         ConditionalNode(LowerEqualThanNode(IntNode(2), IntNode(3)),
                             BlockNode([
                                 LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                            DispatchNode('out_string',
                                                         [StrNode('"True"')], ObjectNode('io'))),
                             ]),
                             BlockNode([
                                 LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                            DispatchNode('out_string',
                                                         [StrNode('"False"')], ObjectNode('io')))
                             ]))

                     ])
                 )
               )
            ])
         ])

    program_code = '''
        class Main {
            main() : Object {
                while true loop
               {
                    if 2<=3 then 
                    { 
                        let io: IO <- new IO in io.out_string("True");
                    } 
                    else {
                        let io: IO <- new IO in io.out_string("False");
                    } 
                    fi;
               } pool
            };
        };
    '''
    parser_result = parser.parse(program_code, lexer=lexer)
    verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)


def test_case():
    program_ast = ProgramNode(
        [ClassNode('Main', features=[
            MethodNode('main', [], 'Int',
                       BlockNode([
                LoopNode(LowerThanNode(IntNode(1),IntNode(2)),
                     BlockNode([
                         CaseNode(PlusNode(IntNode(1),IntNode(2)),
                                  [
                                      (('id1','Int'), PlusNode(ObjectNode('id1'),IntNode(5))),
                                      (('id2', 'Object'), ObjectNode('id2')),
                                      (('id3', 'String'), ObjectNode('id3'))
                                  ]
                                  ),
                         ConditionalNode(LowerEqualThanNode(IntNode(2), IntNode(3)),
                             BlockNode([
                                 LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                            DispatchNode('out_string',
                                                         [StrNode('True')], ObjectNode('io'))),
                             ]),
                             BlockNode([
                                 LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                            DispatchNode('out_string',
                                                         [StrNode('False')], ObjectNode('io')))
                             ]))

                     ])
                 ), IntNode(0)])
               )
            ]),
             ClassNode('A',features=[
                    AttributeNode('attr1','Int',IntNode(24)),
                    MethodNode('attr1',[],'Int',
                               ObjectNode('attr1')
                               ),
                 MethodNode('method2', [], 'Int',
                            DispatchNode('attr1')
                            ),
                 MethodNode('method3', [('index','Int')], 'Int',
                    ConditionalNode(EqualThanNode(ObjectNode('index'),IntNode(0)),
                        DispatchNode('method2'),
                        BlockNode([
                            LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
                                       DispatchNode('out_string',
                                                    [StrNode("Call method3")], ObjectNode('io'))),
                            DispatchNode('method3',[MinusNode(ObjectNode('index'), IntNode(1))])
                        ]))
                )
                ]),
         ClassNode('B', inherit='A',features=[
             MethodNode('method2', [], 'Int',
                        DispatchNode('attr1')
                        )
         ])
         ])

    program_code = '''
        class Main {
            main() : Int {
                {
                    while 1 < 2 loop
                   {
                        case 1+2 of 
                            id1:Int => id1+5;
                            id2:Object => id2;
                            id3:String => id3;
                        esac;
                        if 2<=3 then 
                        { 
                            let io: IO <- new IO in io.out_string("True");
                        } 
                        else {
                            let io: IO <- new IO in io.out_string("False");
                        } 
                        fi;
                   } pool;
                   0;
               }
            };
        };
        class A {
            attr1:Int<-24;
            attr1() : Int {attr1};
            method2():Int {attr1()};
            method3(index:Int):Int {
                if index = 0 then method2() else {
                        let io: IO <- new IO in io.out_string("Call method3");
                        method3(index - 1);
                    }
                fi
            };
        };
        class B inherits A {
            method2():Int {attr1()};
        };
    '''
    parser_result = parser.parse(program_code, lexer=lexer)
    verify_asts(program_ast, parser_result, Node)
    check_semantic(program_ast)