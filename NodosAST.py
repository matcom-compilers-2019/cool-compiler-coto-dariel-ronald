class Node:
    pass

from semantic import *
from utils import Scope


class ProgramNode(Node):
    def __init__(self, classes=[]):
        self.classes = classes

    def check_semantics(self):
        current_scope = Scope()
        errors = []

        type_collector = TypeCollectorVisitor(current_scope)
        type_collector.visit(self, errors)

        type_builder = TypeBuilderVisitor(current_scope)
        type_builder.visit(self, errors)

        type_checker = TypeCheckerVisitor()
        type_checker.visit(self, current_scope,errors)


class ClassNode(Node):
    def __init__(self,type,inherit,features=[]):
        self.name = type
        self.inherit = inherit
        self.methods = []
        self.attributes = []

        for feature in features:
            if isinstance(feature,MethodNode):
                self.methods.append(feature)
            else:
                self.attributes.append(feature)


class FeatureNode(Node):
    pass


class MethodNode(FeatureNode):
    def __init__(self,id,parameters,return_type,expr=None):
        self.id = id
        # aqui se guardan los formal (id,type)
        self.parameters = parameters
        self.return_type = return_type
        self.expressions = expr

    def __eq__(self, other):
        return isinstance(other,MethodNode) and \
        other.id == self.id and other.parameters == self.parameters and \
        other.return_type == self.return_type


class AttributeNode(FeatureNode):
    def __init__(self,id, type,value=None):
        self.type = type
        self.value = value
        self.id = id

    def __eq__(self, other):
        return isinstance(other,AttributeNode) and \
        other.id == self.id and other.type == self.type


# class FormalNode(Node):
#     def __init__(self):
#         self.id = None
#         self.type = None


class ExpressionNode(Node):
    computed_type = None
    pass


class AtomNode(ExpressionNode):
    pass


class AssignNode(ExpressionNode):
    def __init__(self,variable,expr):
        self.variable = variable
        self.expression = expr


class DispatchNode(AtomNode):
    def __init__(self,func_id,params,left_expr):
        self.left_expression = left_expr
        self.func_id = func_id
        self.parameters = params


class StaticDispatchNode(AtomNode):
    def __init__(self,func_id,params,left_expr,parent_type):
        self.left_expression = left_expr
        self.func_id = func_id
        self.parameters = params
        self.paren_type = parent_type


class ConditionalNode(AtomNode):
    def __init__(self,if_expr,then_expr,else_expr):
        self.if_expression = if_expr
        self.then_expression = then_expr
        self.else_expression = else_expr


class LoopNode(AtomNode):
    def __init__(self,while_expr,loop_exprs):
        self.while_expression = while_expr
        self.loop_expression = loop_exprs


class LetVarNode(AtomNode):
    def __init__(self,declarations,in_expr):
        self.in_expression = in_expr
        self.declarations = declarations


class CaseNode(AtomNode):
    def __init__(self,case_expr,implications):
        self.case_expression = case_expr
        self.implications = implications


class NewTypeNode(AtomNode):
    def __init__(self,type):
        self.type = type


class UnaryOperatorNode(ExpressionNode):
    '''
        Esta clase es para las operaciones de:
        - Not
        - Bcomlement
        - isvoid
        - \-
    '''
    def __init__(self,expr):
        self.expression = expr


class BinaryOperatorNode(ExpressionNode):
    '''
     Esta clase es para las operaciones aritméticas
     y para las comparaciones.
    '''
    def __init__(self,left_expr,right_expr):
        self.left_expression = left_expr
        self.right_expression = right_expr


class PlusNode(BinaryOperatorNode):
    pass


class MinusNode(BinaryOperatorNode):
    pass


class StarNode(BinaryOperatorNode):
    pass


class DivNode(BinaryOperatorNode):
    pass


class NegationNode(UnaryOperatorNode):
    pass


class NotNode(UnaryOperatorNode):
    pass


class LowerThanNode(BinaryOperatorNode):
    pass


class LowerEqualThanNode(BinaryOperatorNode):
    pass


class EqualThanNode(BinaryOperatorNode):
    pass


class Object(AtomNode):
    def __init__(self, id):
        self.id = id


class IsVoidNode(AtomNode):
    def __init__(self,expr):
        self.expression = expr


class BlockNode(AtomNode):
    def __init__(self,exprs):
        self.expressions = exprs


class BComplementNode(AtomNode):
    def __init__(self,expr):
        self.expression = expr


class IntNode(AtomNode):
    def __init__(self,value):
        self.value = value


class StrNode(AtomNode):
    def __init__(self,value):
        self.value = value


class BoolNode(AtomNode):
    def __init__(self,value):
        self.value = value


class AtomNode(ExpressionNode):
   pass

#
# class ImplicationNode(ExpressionNode):
#     def _init_(self):
#         self.id = None
#         self.type = None
#         self.expression = None
