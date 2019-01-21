
class Node:
    pass

class Program (Node):
    def __init__(self):
        self.classes = []


class Class(Node):
    def __init__(self):
        self.type = None
        self.inherit = None
        self.features = None


class Feature(Node):
    pass

class Features(Feature):
    def __init__(self):
        self.features = []

class Inherits(Feature):
    def __init__(self):
        self.type = None

class Method(Feature):
    def __init__(self):
        self.id = None
        self.parameters = None
        self.return_type = None
        self.expressions = None

class Attribute(Feature):
    def __init__(self):
        self.type = None
        self.value = None

class Formals(Node):
    def __init__(self):
        self.formals = []

class Formal(Node):
    def __init__(self):
        self.id = None
        self.type = None

class Expression(Node):
    pass

class Expressions(Node):
    def __init__(self):
        self.expressions = []

class Assign(Expression):
    def __init__(self):
        self.id = None
        self.expression = None

class Dispatch(Expression):
    def __init__(self):
        self.left_expression = None
        self.parent_type = None
        self.func_id = None
        self.parameters = None

class Conditional(Expression):
    def __init__(self):
        self.if_expression = None
        self.then_expression = None
        self.else_expression = None

class Loop(Expression):
    def __init__(self):
        self.while_expression = None
        self.loop_expression = None

class LetVar(Expression):
    def __init__(self):
        self.in_expression = None
        self.assigns = None


class Case(Expression):
    def __init__(self):
        self.case_expression = None
        self.implications = None

class NewType(Expression):
    def __init__(self):
        self.id = None
        self.type = None

class BinaryExpression(Expression):
    def __init__(self):
        self.operator = None
        self.left_expression = None
        self.right_expression = None

class UnaryExpression(Expression):
    def __init__(self):
        self.operator = None
        self.expression = None

class Id(Expression):
    def __init__(self,id):
        self.id = id

class Atom(Expression):
    def __init__(self):
        self.type = None
        self.value = None

class DeclarationList(Expression):
    def _init_(self):
        self.declarations = []

class Implications(Expression):
    def _init_(self):
        self.implications = []

class Implication(Expression):
    def _init_(self):
        self.id_type = None
        self.expression = None
