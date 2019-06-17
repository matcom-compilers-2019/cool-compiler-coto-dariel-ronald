import visitor
import NodosAST as ast
from cil_hierarchy import *


class StringVisitor:
    def __init__(self):
        self.dotdata = []
        self.dottypes = []

    def register_data(self, value):
        vname = f'data_{len(self.dotdata)}'
        data_node = CILDataElementNode(vname, value)
        self.dotdata.append(data_node)

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node:ast.ProgramNode):
        for program_class in node.classes:
            self.visit(program_class)

    @visitor.when(ast.ClassNode)
    def visit(self, node:ast.ClassNode):
        self.dottypes.append(CILTypeNode(node.name, node.inherit))
        for attr in node.attributes:
            self.visit(attr)
            if attr.value is not None:
                self.visit(attr.value)
        for method in node.methods:
            self.visit(method)
            
    @visitor.when(ast.MethodNode)
    def visit(self, node:ast.MethodNode):
        name = f'{self.dottypes[-1].name}_{node.id}'
        self.dottypes[-1].methods.append(name)
        if type(node.expression) is ast.BlockNode:
            for expr in node.expression.expressions:
                self.visit(expr)
        else:
            self.visit(node.expression)

    @visitor.when(ast.AttributeNode)
    def visit(self, node:ast.AttributeNode):
        self.dottypes[-1].attributes.append(node.id)

    @visitor.when(ast.AssignNode)
    def visit(self, node:ast.AssignNode):
        self.visit(node.expression)
        
    @visitor.when(ast.DispatchNode)
    def visit(self, node:ast.DispatchNode):
        self.visit(node.left_expression)
        for exp in node.parameters:
            self.visit(exp)

    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node:ast.StaticDispatchNode):
        self.visit(node.left_expression)
        for x in node.parameters:
            self.visit(x)

    @visitor.when(ast.ConditionalNode)
    def visit(self, node:ast.ConditionalNode):
        self.visit(node.if_expression)
        self.visit(node.then_expression)
        self.visit(node.else_expression)

    @visitor.when(ast.LoopNode)
    def visit(self, node:ast.LoopNode):
        self.visit(node.while_expression)
        self.visit(node.loop_expression)

    @visitor.when(ast.LetVarNode)
    def visit(self, node: ast.LetVarNode):
        for dec in node.declarations:
            if dec[1] is not None:
                self.visit(dec[1])
        self.visit(node.in_expression)

    @visitor.when(ast.CaseNode)
    def visit(self, node:ast.CaseNode):
        self.visit(node.case_expression)
        for i in range(0,len(node.implications)):
            self.visit(node.implications[i][1])

    @visitor.when(ast.NewTypeNode)
    def visit(self, node:ast.NewTypeNode):
        pass

    @visitor.when(ast.PlusNode)
    def visit(self, node:ast.PlusNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.MinusNode)
    def visit(self, node:ast.MinusNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.StarNode)
    def visit(self, node:ast.StarNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.DivNode)
    def visit(self, node:ast.DivNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.NegationNode)
    def visit(self, node:ast.NegationNode):
        self.visit(node.expression)

    @visitor.when(ast.NotNode)
    def visit(self, node:ast.NotNode):
        self.visit(node.expression)

    @visitor.when(ast.LowerThanNode)
    def visit(self, node: ast.LowerThanNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.LowerEqualThanNode)
    def visit(self, node: ast.LowerEqualThanNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.EqualThanNode)
    def visit(self, node:ast.EqualThanNode): 
        self.visit(node.left_expression)
        self.visit(node.right_expression)

    @visitor.when(ast.ObjectNode)
    def visit(self, node:ast.ObjectNode):
        node.holder = node.id

    @visitor.when(ast.IsVoidNode)
    def visit(self, node:ast.IsVoidNode):
        self.visit(node.expression)

    @visitor.when(ast.BlockNode)
    def visit(self, node:ast.BlockNode):
        for exp in node.expressions:
            self.visit(exp)

    @visitor.when(ast.IntegerComplementNode)
    def visit(self, node:ast.IntegerComplementNode):
        self.visit(node.expression)

    @visitor.when(ast.IntNode)
    def visit(self, node:ast.IntNode):
        pass

    @visitor.when(ast.StrNode)
    def visit(self, node:ast.StrNode):
        self.register_data(node.value)
    
    @visitor.when(ast.BoolNode)
    def visit(self, node:ast.BoolNode):
        pass