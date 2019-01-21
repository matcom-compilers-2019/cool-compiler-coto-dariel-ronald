
class Node:
    pass

class Program (Node):
    def __init__(self):
        self.classes = []


class Class(Node):
    def __init__(self):
        self.type = ""
        self.inherit = ""
        self.features = []


class Feature(Node):
    pass

class Method(Feature):
    def __init__(self):
        self.id = ""
        self.parameters = []
        self.return_type = ""
        self.expressions = []

class Attribute(Feature):
    def __init__(self):
        self.id = ""
        self.type = ""
        self.value = ""

class Formal(Node):
    def __init__(self):
        self.id = ""
        self.type = ""

class Expression(Node):
    pass

class Assign(Expression):
    def __init__(self):
        self.id = ""
        self.expression = ""

class Dispatch(Expression):
    def __init__(self):
        self.in_expression = ""
        self.parent_type = ""
        self.parent_id = ""
        self.parameters = []

class Conditional(Expression):
    def __init__(self):
        self.if_expression = ""
        self.then_expression = ""
        self.else_expression = ""

class Loop(Expression):
    def __init__(self):
        self.while_expression = ""
        self.loop_expression = ""

class LetVar(Expression):
    def __init__(self):
        self.in_expression = ""
        self.assigns = []


class Case(Expression):
    def __init__(self):
        self.case_expression = ""
        self.implications = []

class NewType(Expression):
    def __init__(self):
        self.type = ""

class BinaryExpression(Expression):
    def __init__(self):
        self.operator = ""
        self.left_expression = ""
        self.right_expression = ""

class UnaryExpression(Expression):
    def __init__(self):
        self.operator = ""
        self.expression = ""

class Id(Expression):
    def __init__(self):
        self.id = ""

class Atom(Expression):
    def __init__(self):
        self.type = ""
        self.value = ""


