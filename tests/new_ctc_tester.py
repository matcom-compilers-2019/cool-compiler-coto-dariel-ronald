from NodosAST import *
from cil_hierarchy import *
from tools_for_testing import verify_cil_ast
import cool_to_cil
from static_functions import *

# def test_hello_world():
#     original = CILProgramNode([CILTypeNode("Object", "None", [], ["Object_abort", "Object_type_name", "Object_copy"]),
#                                CILTypeNode("IO", "Object", [],
#                                            ["IO_out_string", "IO_out_int", "IO_in_string", "IO_in_int"]),
#                                CILTypeNode("Int", "None"),
#                                CILTypeNode("String", "None", [], ["String_length", "String_concat", "String_substr"]),
#                                CILTypeNode("Bool", "None")],
#                               CILDataNode(), [],
#                               [CILFunctionNode("@@get_distance"), CILFunctionNode("@@get_closest_parent")])
#     visitor = cool_to_cil.COOLToCILVisitor()
#
#
#     program_ast = ProgramNode([ClassNode('Main', features=[
#         MethodNode('main', [], 'IO', DispatchNode('out_string', [StrNode('"Hello, World"')], None))
#     ], inherit='IO')])
#     program_code = '''
#
#     class Main inherits IO {
#          main(): IO {
# 	        out_string("Hello, World")
#     };
# };
#     '''
#     conversion_result = visitor.visit(program_ast)
#     expected = original
#     expected.dottypes.append(CILTypeNode('Main', 'IO',[],['main']))
#     expected.dotcode.append(CILCodeNode([CILFunctionNode('main')]))
#     a = verify_cil_ast(expected, conversion_result)


# def test_new_type_node_and_let_node():
#     program_ast = ProgramNode([ClassNode('Main', 'Object' ,features=[
#         MethodNode('main', [], 'Int',
#                    BlockNode([
#                         LetVarNode([(('io','IO'),NewTypeNode('IO'))],
#                                    DispatchNode('out_string',
#                                                 [StrNode('"Hello World"')],ObjectNode('io'))),
#                         IntNode(0)
#         ]))
#     ])])
#     program_code = '''
#    class Main {
#     main() : Int {
# 	{
# 	    let io: IO <- new IO in io.out_string("Hello World");
# 	    0;
# 	}
#     };
# };
#     '''
#     visitor = cool_to_cil.COOLToCILVisitor()
#     conversion_result = visitor.visit(program_ast)

# def test_new_type_node_and_let_node2():
#     program_ast = ProgramNode(
#         [ClassNode('Main', 'None',features=[
#             MethodNode('main', [], 'Int',
#                        BlockNode([
#                             LetVarNode([(('io','IO'),NewTypeNode('IO'))],
#                                        DispatchNode('out_string',
#                                                     [StrNode('"Hello World"')],ObjectNode('io'))),
#                             LetVarNode([(('a','A'),NewTypeNode("A")),(('b','Int'),None)],
#                                        PlusNode(DispatchNode('funk',[(BoolNode('true'))], ObjectNode('a')),
#                                                 ObjectNode('b')))
#             ]))
#     ]),
#          ClassNode('A', 'None',features=[
#                 MethodNode('funk',[('a','Bool')],'Int',
#                             LetVarNode([(('x','Int'),None)],
#                                        PlusNode(ObjectNode('x'),IntNode(1)))
#                            )
#             ])
#          ])
#     program_code = '''
#    class Main {
#     main() : Int {
#             {
#                 let io: IO <- new IO in io.out_string("Hello World");
#                 let a:A <- new A, b: Int in a.funk() + b;
#             }
#         };
#     };
#     class A {
#        funk():Int {
#             let x:Int in x + 1
#        };
#     };
#
#     '''
#     visitor = cool_to_cil.COOLToCILVisitor()
#     conversion_result = visitor.visit(program_ast)

#
# def test_conditional():
#         program_ast = ProgramNode(
#             [ClassNode('Main', 'None',features=[
#                 MethodNode('main', [], 'IO',
#                    BlockNode([
#                        ConditionalNode(LowerEqualThanNode(IntNode(2),IntNode(3)),
#                            LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                       DispatchNode('out_string',
#                                                    [StrNode('"True"')], ObjectNode('io'))),
#                            LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                       DispatchNode('out_string',
#                                                    [StrNode('"False"')], ObjectNode('io')))
#                        )
#                    ]))
#             ])
#              ])
#         program_code = '''
#        class Main {
#             main() : IO {
#                    {
#
#                         if 2<=3 then let io: IO <- new IO in io.out_string("True")
#                         else let io: IO <- new IO in io.out_string("False") fi;
#                    }
#             };
#         };
#
#         '''
#         visitor = cool_to_cil.COOLToCILVisitor()
#         conversion_result = visitor.visit(program_ast)
#
#
# def test_loop_check():
#     program_ast = ProgramNode(
#         [ClassNode('Main', 'None',features=[
#             MethodNode('main', [], 'Object',
#                 LoopNode(BoolNode('true'),
#                      BlockNode([
#                          ConditionalNode(LowerEqualThanNode(IntNode(2), IntNode(3)),
#                              BlockNode([
#                                  LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                             DispatchNode('out_string',
#                                                          [StrNode('"True"')], ObjectNode('io'))),
#                              ]),
#                              BlockNode([
#                                  LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                             DispatchNode('out_string',
#                                                          [StrNode('"False"')], ObjectNode('io')))
#                              ]))
#
#                      ])
#                  )
#                )
#             ])
#          ])
#
#     program_code = '''
#         class Main {
#             main() : Object {
#                 while true loop
#                {
#                     if 2<=3 then
#                     {
#                         let io: IO <- new IO in io.out_string("True");
#                     }
#                     else {
#                         let io: IO <- new IO in io.out_string("False");
#                     }
#                     fi;
#                } pool
#             };
#         };
#     '''
#     visitor = cool_to_cil.COOLToCILVisitor()
#     conversion_result = visitor.visit(program_ast)
#
#


# def test_case2():
#     program_ast = ProgramNode(
#         [ClassNode('Main', 'None', features=[
#             MethodNode('main', [], 'Object',
#                 LoopNode(BoolNode('true'),
#                      BlockNode([
#                          CaseNode(PlusNode(IntNode(1),IntNode(2)),
#                                   [
#                                       (('id1','Int'), PlusNode(ObjectNode('id1'),IntNode(5))),
#                                       (('id2', 'Object'), ObjectNode('id2')),
#                                       (('id3', 'String'), ObjectNode('id3'))
#                                   ]
#                                   ),
#                          ConditionalNode(LowerEqualThanNode(IntNode(2), IntNode(3)),
#                              BlockNode([
#                                  LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                             DispatchNode('out_string',
#                                                          [StrNode('"True"')], ObjectNode('io'))),
#                              ]),
#                              BlockNode([
#                                  LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                             DispatchNode('out_string',
#                                                          [StrNode('"False"')], ObjectNode('io')))
#                              ]))
#
#                      ])
#                  )
#                )
#             ]),
#              ClassNode('A', 'None', features=[
#                     AttributeNode('attr1','Int',IntNode(24)),
#                     MethodNode('attr1',[],'Int',
#                                ObjectNode('attr1')
#                                ),
#                  MethodNode('method2', [], 'Int',
#                             DispatchNode('attr1',[],None)
#                             ),
#                  MethodNode('method3', [('index','Int')], 'Int',
#                     ConditionalNode(EqualThanNode(ObjectNode('index'),IntNode(0)),
#                         DispatchNode('method2',[],None),
#                         BlockNode([
#                             LetVarNode([(('io', 'IO'), NewTypeNode('IO'))],
#                                        DispatchNode('out_string',
#                                                     [StrNode('"Call method3"')], ObjectNode('io'))),
#                             DispatchNode('method3',[MinusNode(ObjectNode('index'),IntNode(1))],None)
#                         ]))
#                 )
#                 ])
#              ])
#
#     program_code = '''
#         class Main {
#             main() : Object {
#                 while true loop
#                {
#                     case 1+2 of
#                         id1:Int => id1+5;
#                         id2:Object => id2;
#                         id3:String => id3;
#                     esac;
#                     if 2<=3 then
#                     {
#                         let io: IO <- new IO in io.out_string("True");
#                     }
#                     else {
#                         let io: IO <- new IO in io.out_string("False");
#                     }
#                     fi;
#                } pool
#             };
#         };
#         class A {
#             attr1:Int<-24;
#             attr1() : Int {attr1};
#             method2():Int {attr1()};
#             method3(index:Int):Int {
#                 if index = 0 then method2() else {
#                         let io: IO <- new IO in io.out_string("Call method3");
#                         method3(index - 1);
#                     }
#                 fi
#             };
#         };
#     '''
#     visitor = cool_to_cil.COOLToCILVisitor()
#     conversion_result = visitor.visit(program_ast)




def test_inheritance():
    program_ast = ProgramNode(
        [ClassNode('Main', 'None',features=[
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
         ClassNode('A', 'None',features=[ AttributeNode('attr5','Bool',BoolNode(1)),
                MethodNode('funk',[('a','Bool')],'Int',
                            LetVarNode([(('x','Int'),None)],
                                       PlusNode(ObjectNode('x'),IntNode(1)))
                           )
            ]),


         ClassNode('B', 'A', features=[ AttributeNode('attr3','Int',IntNode(24)),
             MethodNode('funk', [('a', 'Bool')], 'Int',
                        LetVarNode([(('x', 'Int'), None)],
                                   PlusNode(ObjectNode('x'), IntNode(1)))
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
    visitor = cool_to_cil.COOLToCILVisitor()
    conversion_result = visitor.visit(program_ast)