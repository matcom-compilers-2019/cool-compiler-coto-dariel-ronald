import itertools as itl

import NodosAST as ast
import visitor
from utils import *

ERROR = 0
INTEGER = 1

# Todo: antes que todo,tengo que instalar los tipos fundamentales de cool al scope que le pase al primer visitor


class TypeCollectorVisitor:
    def __init__(self,scope):
        self.context = scope

    @visitor.on('node')
    def visit(self, node, errors):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, errors):
        for program_class in node.classes:
            self.visit(program_class,errors)

    @visitor.when(ast.ClassNode)
    def visit(self, node, errors):
        self.context.create_type(node.name,node.inherit)


class TypeBuilderVisitor:
    def __init__(self,scope):
        self.context = scope
        self._current_type = None


    @visitor.on('node')
    def visit(self, node, errors):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, errors):
        for program_class in node.classes:
            self.visit(program_class, errors)

    @visitor.when(ast.ClassNode)
    def visit(self, node, errors):
        self._current_type = self.context.get_type(node.name)
        self._current_type.define_parent(self.context)

        for methoddef in node.methods:
            self.visit(methoddef)

        for attrdef in node.attributes:
            self.visit(attrdef)

    @visitor.when(ast.MethodNode)
    def visit(self, node, errors):
        return_type = self.context.get_type(node.return_type)
        params = [(param_name, self.context.get_type(type_name))
                  for param_name, type_name in node.parameters]
        self._current_type.define_method(node.id,return_type,params)

    @visitor.when(ast.AttributeNode)
    def visit(self, node, errors):
        attr_type = self.context.get_type(node.type)
        self._current_type.define_attr(node.id, attr_type)


class TypeCheckerVisitor:

    def check_class_hierarchy(self,context,errors):
        classes = context._classes_global_field()

        for class_ in classes.values():
            if class_._checked_for_cycle:
                continue

            for current_type in class_.get_hierarchy_iterator():
                if current_type._checking_for_cycle:
                    errors.append('Founded Cycle')
                    return False
                current_type._checking_for_cycle = True

            for current_type in class_.get_hierarchy_iterator():
                current_type._checking_for_cycle = False

            for current_type in class_.get_hierarchy_iterator():
                current_type._checked_for_cycle = True

        return True

    @visitor.on('node')
    def visit(self, node, errors):
        pass

    # @visitor.when(ast.BinaryOperatorNode)
    # def visit(self, node, errors):
    #     self.visit(node.left_expression)
    #     self.visit(node.right_expression)
    #     if node.left_expression.computed_type != node.right_expression.computed_type:
    #         errors.append('Type missmatch, ')
    #         node.computed_type = None
    #     else:
    #         node.computed_type = node.left_expression.computed_type


    @visitor.when(ast.ProgramNode)
    def visit(self, node,scope, errors):
        for cool_class in node.classes:
            self.visit(cool_class,scope,errors)

    @visitor.when(ast.ClassNode)
    def visit(self, node,scope, errors):
        for attr in node.attributes:
            self.visit(attr,scope,errors)

        for method in node.methods:
            child_scope = scope.create_child_scope()
            self.visit(method,child_scope,errors)

    @visitor.when(ast.MethodNode)
    def visit(self, node, scope,errors):

        # Añadimos los parametros como variables locales
        for param_name,param_type_name in node.parameters:
            vinfo = scope.define_variable(param_name,param_type_name)
            if vinfo is None:
                errors.append("Error in method {}: parameter {}".format(node.id,param_name))

        # Verificamos si está definido el tipo de retorno
        return_type = scope.get_type(node.return_type)
        if return_type is None:
            errors.append("Error in method {}: type {} not defined".format(node.id,node.return_type))

        # Recorremos el cuerpo del método
        for expr in node.expressions:
            self.visit(expr,scope,errors)


    @visitor.when(ast.AttributeNode)
    def visit(self, node, scope,errors):
        vinfo = scope.define_variable(node.id,)

    @visitor.when(ast.AssignNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.DispatchNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.ConditionalNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.CaseNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.NewTypeNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.PlusNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.StarNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.MinusNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.DivNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.NegationNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.NotNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.LowerThanNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.LowerEqualThanNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.EqualThanNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.Object)
    def visit(self, node, errors):
     '''
     Para verificar si aqui todo está en talla tengo que buscar primeramente
     si está definido el objeto.
     Para poder verificar si está definido:
        -tengo que buscar en los parámetos del método.
        -buscar en los atributos de la clase
        -buscar en las variables del scope

     :param node:
     :param errors:
     :return:
     '''

    @visitor.when(ast.BlockNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.BComplementNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.IntNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.BoolNode)
    def visit(self, node, errors):
        pass

    @visitor.when(ast.StrNode)
    def visit(self, node, errors):
        pass





class CheckSemanticsVisitor:
    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node, scope, errors):
        scope = Scope()
        return self.visit(node.expr, scope, errors)

    @visitor.when(ast.BinaryOperatorNode)
    def visit(self, node, scope, errors):
        rleft = self.visit(node.left, scope, errors)
        rright = self.visit(node.right, scope, errors)
        return rleft and rright

    @visitor.when(ast.UnaryOperatorNode)
    def visit(self, node, scope, errors):
        return self.visit(node.expr, scope, errors)

    @visitor.when(ast.LetVarNode)
    def visit(self, node, scope, errors):
        child_scope = scope.create_child_scope()
        rtype = INTEGER
        for declaration in node.declaration_list:
            rtype &= self.visit(declaration, child_scope, errors)
        rtype &= self.visit(node.expr, child_scope, errors)
        return rtype

    @visitor.when(ast.BlockNode)
    def visit(self, node, scope, errors):
        rtype = INTEGER
        for expr in node.expr_list:
            rtype = self.visit(expr, scope, errors)
        return rtype

    @visitor.when(ast.AssignNode)
    def visit(self, node, scope, errors):
        rtype = self.visit(node.expr, scope, errors)
        vname = node.idx_token.text_token
        if not scope.is_defined(vname):
            errors.append('[line:%s,column:%s]: Variable \'%s\' not defined.' % (node.idx_token.row, node.idx_token.col, vname))
            return ERROR
        node.variable_info = scope.get_variable_info(vname)
        return rtype

    @visitor.when(ast.IntNode)
    def visit(self, node, scope, errors):
        return INTEGER

    @visitor.when(ast.VariableNode)
    def visit(self, node, scope, errors):
        vname = node.idx_token.text_token
        if not scope.is_defined(vname):
            errors.append('[line:%s,column:%s]: Variable \'%s\' not defined.' % (node.idx_token.row, node.idx_token.col, vname))
            return ERROR
        node.variable_info = scope.get_variable_info(vname)
        return INTEGER

    # @visitor.when(ast.PrintIntegerNode)
    # def visit(self, node, scope, errors):
    #     return self.visit(node.expr, scope, errors)

    # @visitor.when(ast.PrintStringNode)
    # def visit(self, node, scope, errors):
    #     return INTEGER

    # @visitor.when(ast.ScanNode)
    # def visit(self, node, scope, errors):
    #     return INTEGER