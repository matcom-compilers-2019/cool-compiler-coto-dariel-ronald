class Node:
    pass


class Program (Node):
    def __init__(self):
        self.classes = []


class Class(Node):
    def __init__(self):
        self.type = None
        self.inherit = None
        self.features = []


class Feature(Node):
    pass


class Method(Feature):
    def __init__(self):
        self.id = None
        # aqui se guardan los formal
        self.parameters = []
        self.return_type = None
        self.expressions = []


class Attribute(Feature):
    def __init__(self):
        self.type = None
        self.value = None


class Formal(Node):
    def __init__(self):
        self.id = None
        self.type = None


class Expression(Node):
    pass


class Assign(Expression):
    def __init__(self):
        self.id = None
        self.expression = None


class Dispatch(Expression):
    def __init__(self):
        self.left_expression = None
        self.dispatch_type = None
        self.func_id = None
        self.parameters = []


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
        self.declarations = []


class Case(Expression):
    def __init__(self):
        self.case_expression = None
        self.implications = []


class NewType(Expression):
    def __init__(self):
        # self.id = None
        self.type = None


class BinaryExpression(Expression):
    '''
     Esta clase es para las operaciones aritméticas
     y para las comparaciones.
    '''
    def __init__(self):
        self.operator = None
        self.left_expression = None
        self.right_expression = None


class UnaryExpression(Expression):
    '''
        Esta clase es para las operaciones de:
        - Not
        - Bcomlement
        - isvoid
    '''
    def __init__(self):
        self.operator = None
        self.expression = None


class Variable(Expression):
    def __init__(self,id):
        self.id = id


class Atom(Expression):
    '''
        Aqui entrarían:
        - integer
        - string
        - true and false
    '''
    def __init__(self):
        self.value = None


class Implication(Expression):
    def _init_(self):
        self.id = None
        self.id_type = None
        self.expression = None
