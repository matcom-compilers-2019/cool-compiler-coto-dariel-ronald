from coolyacc import parser
from NodosAST import *
import json


class MyEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,Node):
            new_dict = obj.__dict__.copy()
            for field in new_dict:
                field_value = new_dict[field]
                if isinstance(field_value,Node):
                    field_value = self.default(field_value)
                elif isinstance(field_value,list) or isinstance(field_value,tuple):
                    new_field = [self.default(item)for item in field_value]
                    field_value = new_field if isinstance(field_value,list) else tuple(new_field)
                else:
                    field_value = json.dumps(field_value)
                new_dict[field] = field_value
            return json.dumps(new_dict)
        elif isinstance(obj,list) or isinstance(obj,tuple):
            new_field = [self.default(item)for item in obj]
            new_obj = new_field if isinstance(obj,list) else tuple(new_field)
            return json.dumps(new_obj)
        return json.dumps(obj)


def test_empty_class_definition():
    program = "class A { };"
    expected = ProgramNode([ClassNode('A', 'Object')])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                                      json.dumps(expected,cls=MyEncoder)
    assert parser_result == expected, \
                'Expected: "{}" and found "{}" '.format(expected, parser_result)


#
def test_class_definition_with_inherits():
    program = "class A inherits Top { };"
    expected = ProgramNode([ClassNode('A', 'Top')])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                                      json.dumps(expected,cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_class_with_uninitialized_attributes():
    program = """
    class A {
        attr1:AttrType;
        attr2:AttrType;
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    AttributeNode('attr1', 'AttrType'),
                    AttributeNode('attr2', 'AttrType'),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                                      json.dumps(expected,cls=MyEncoder)
    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_class_with_initialized_attributes():
    program = """
    class A {
        attr1:AttrType <- otherObj;
        attr2: AttrType <- initialObj;
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    AttributeNode('attr1', 'AttrType', ObjectNode('otherObj')),
                    AttributeNode('attr2', 'AttrType', ObjectNode('initialObj')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                                      json.dumps(expected,cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_class_with_method_without_formals():
    program = """class A { funk():ReturnType { returnvalue }; };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'ReturnType', ObjectNode('returnvalue')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_class_with_method_with_formals():
    program = """class A { funk(x:X, y:Y):ReturnType { x }; };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [('x', 'X'), ('y', 'Y')], 'ReturnType', ObjectNode('x')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_class_with_method_returning_int():
    program = """class A { funk():ReturnType { 12 }; };"""
    funk_method = MethodNode('funk', [], 'ReturnType', IntNode(12))
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    funk_method
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#Todo: me coge los strings como doble strings '"blabla"' en vez de "blabla"
def test_class_with_method_returning_str():
    program = """class A { funk():ReturnType { "blabla" }; };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'ReturnType', StrNode('"blabla"')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)


def test_class_with_method_with_block():
    program = """
    class A inherits WithVar {
       set_var(num : Int) : SELF_TYPE {
          {
                 self;
          }
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'WithVar',
                [
                    MethodNode('set_var', [('num', 'Int')], 'SELF_TYPE', BlockNode([ObjectNode('self')])),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_simple_dispatch_with_no_args():
    program = """
    class A {
       funk():Type {
            obj.method()
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type', DispatchNode('method', [],ObjectNode('obj')))
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_simple_dispatch_with_one_arg():
    program = """
    class A {
       funk():Type {
            obj.method(2)
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type', DispatchNode('method', [IntNode(2)],ObjectNode('obj')))
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)


def test_simple_dispatch_with_multiple_args():
    program = """
    class A {
       funk():Type {
            obj.method(2, "blabla", x)
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type', DispatchNode('method', [IntNode(2), StrNode('"blabla"'),
                                                                           ObjectNode('x')],
                                                                ObjectNode('obj')))
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

#
def test_static_dispatch_with_no_args():
    program = """
    class A {
       funk():Type {
            obj@Klass.method()
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type', StaticDispatchNode('method', [],ObjectNode('obj'),'Klass')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected, 'Expected: "{}" and found "{}" '.format(expected,parser_result)

# Este está comentado pq no se si por fin hay que implementar el self
# esto tengo q preguntárselo a juan pablo

# def test_self_dispatch_with_no_args():
#     program = """
#     class A {
#        funk():Type {
#             method()
#        };
#     };"""
#     expected = ProgramNode([ClassNode('A', 'Object',
#                 [
#                     MethodNode('funk', [], 'Type', DispatchNode('method', [],'self')),
#                 ]
#                 )])
#     assert parser.parse(program) == expected

#
def test_if_statements():
    program = """
    class A {
       funk():Type {
            if x < 0 then 1 else 2 fi
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                               ConditionalNode(LowerThanNode(ObjectNode('x'),
                                                             IntNode(0)),
                                               IntNode(1),
                                               IntNode(2))
                               ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert  parser_result == expected


def test_while_statements():
    program = """
    class A {
       funk():Type {
            while x < 0 loop 1 pool
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                               LoopNode(LowerThanNode(ObjectNode('x'), IntNode(0)), IntNode(1))
                               ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
def test_let_statement():
    program = """
    class A {
       funk():Type {
            let x:TypeX in x + 1
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        LetVarNode([(('x','TypeX'),None)],PlusNode(ObjectNode('x'), IntNode(1)))
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
def test_let_statement_with_assignment():
    program = """
    class A {
       funk():Type {
            let x:TypeX <- 5 in x + 1
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                               LetVarNode([(('x', 'TypeX'), IntNode(5))], PlusNode(ObjectNode('x'), IntNode(1)))
                               )
                ]
                )])

    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
def test_let_statement_with_two_vars():
    program = """
    class A {
       funk():Type {
            let x:TypeX <- 5,
                y:TypeY
                in x + 1
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        LetVarNode([(('x', 'TypeX'), IntNode(5)),
                                   (('y', 'TypeY'), None)],
                                PlusNode(ObjectNode('x'), IntNode(1))
                             )
                     )
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
def test_let_statement_with_three_vars():
    program = """
    class A {
       funk():Type {
            let x:TypeX,
                y:TypeY <- 3,
                z:ZType <- (2+2) * 5
                in x + 1
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        LetVarNode([(('x', 'TypeX'), None),
                                    (('y', 'TypeY'), IntNode(3)),
                                    (('z', 'ZType'), StarNode(PlusNode(IntNode(2), IntNode(2)), IntNode(5)))],
                                    PlusNode(ObjectNode('x'), IntNode(1))
                                )
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
# def test_let_statement_with_two_vars_error_in_first():
#     program = """
#     class A {
#        funk():Type {
#             let x <- 5,
#                 x:TypeX <- 5
#                 in x + 1
#        };
#     };"""
#     expected = ProgramNode([ClassNode('A', 'Object',
#                 [
#                     MethodNode('funk', [], 'Type',
#                         LetVarNode('x', 'TypeX', IntNode(5),
#                                 PlusNode(ObjectNode('x'), IntNode(1))
#                         )
#                      ),
#                 ]
#                 )])
#     assert parser.parse(program) == expected
#

#
def test_new():
    program = """
    class A {
       funk():Type {
            new B
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        NewTypeNode('B')
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert  parser_result == expected

#
def test_isvoid():
    program = """
    class A {
       funk():Type {
            isvoid b
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        IsVoidNode(ObjectNode('b'))
                     )
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected

#
def test_case():
    program = """
    class A {
       funk():Type {
            case 1 of
                x:Int => 10;
                x:String => 9;
                x:Guru => 8;
            esac
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        CaseNode(IntNode(1),
                         [(('x', 'Int'), IntNode(10)),
                          (('x', 'String'), IntNode(9)),
                          (('x', 'Guru'), IntNode(8))]
                         )
                     )
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected


def test_neg():
    program = """
    class A {
       funk():Type {
            case ~1 of
                x:Int => 10;
            esac
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        CaseNode(NegationNode(IntNode(1)),
                         [(('x', 'Int'), IntNode(10))]
                         )
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected


def test_not():
    program = """
    class A {
       funk():Type {
            case not 1 of
                x:Int => 10;
            esac
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                               CaseNode(NotNode(IntNode(1)),
                               [(('x', 'Int'), IntNode(10))]
                         )
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected


def test_two_classes_defined():
    program = """
    class A {
       funk():Type {
            a
       };
    };
    class B {
       funk():Type {
            a
       };
    };
    """
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type', ObjectNode('a')),
                ]
                ),
                ClassNode('B', 'Object',
                [
                    MethodNode('funk', [], 'Type', ObjectNode('a')),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected


def test_operator_precedence_in_if_statements():
    program = """
    class A {
       funk():Type {
            if 3 + 4 < 0 then 1 else 2 fi
       };
    };"""
    expected = ProgramNode([ClassNode('A', 'Object',
                [
                    MethodNode('funk', [], 'Type',
                        ConditionalNode(LowerThanNode(PlusNode(IntNode(3), IntNode(4)), IntNode(0)), IntNode(1), IntNode(2))
                     ),
                ]
                )])
    parser_result = parser.parse(program)
    parser_result, expected = json.dumps(parser_result, cls=MyEncoder), \
                              json.dumps(expected, cls=MyEncoder)

    assert parser_result == expected


