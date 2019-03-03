import itertools as itl

import NodosAST as ast
import visitor
from utils import *
from error import *

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
        self.context.create_type(node.name,node.inherit,node.line,node.index)


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
        if return_type is None:
            errors.append(TypeError(node.line, node.index, 'Return Type %s not defined' % return_type))
        params = []
        for id, type_name in node.parameters:
            type_class = self.context.get_type(type_name)
            if type_class is None:
                errors.append(TypeError(node.line,node.index,'Param Type %s not defined' % type_name))
            params.append((id, type_class))
        self._current_type.define_method(node.id,return_type,params)

    @visitor.when(ast.AttributeNode)
    def visit(self, node, errors):
        attr_type = self.context.get_type(node.type)
        if attr_type is None:
            errors.append(TypeError(node.line, node.index, 'Type %s not defined' % attr_type))
        self._current_type.define_attr(node.id, attr_type)


#Todo: tengo que verificar que el ProgramNode tiene una claseMain la cual tiene un metodo main()
class TypeCheckerVisitor:

    def check_class_hierarchy(self,context,errors):
        classes = context._classes_global_field()

        for class_ in classes.values():
            if class_._checked_for_cycle:
                continue

            for current_type in class_.get_hierarchy_iterator():
                if current_type._checking_for_cycle:
                    errors.append(SemanticError(current_type.line,current_type.index,'Ciclo en la jerarquía de %s' % current_type.name))
                    return False
                current_type._checking_for_cycle = True

            for current_type in class_.get_hierarchy_iterator():
                current_type._checking_for_cycle = False

            for current_type in class_.get_hierarchy_iterator():
                current_type._checked_for_cycle = True

        return True

    @visitor.on('node')
    def visit(self, node, scope, errors):
        pass

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
                errors.append(NameError(node.line,node.index,"Error in method {}: parameter {}".format(node.id,param_name)))

        # Verificamos si está definido el tipo de retorno
        # return_type = scope.get_type(node.return_type)
        # if return_type is None:
        #     errors.append(TypeError(node.line,node.index,"Error in method {}: return type {} not defined".format(node.id,node.return_type)))

        # Recorremos el cuerpo del método
        for expr in node.expressions:
            self.visit(expr,scope,errors)


    @visitor.when(ast.AttributeNode)
    def visit(self, node, scope,errors):
        vinfo = scope.define_variable(node.id,node.type)
        if vinfo is None:
            errors.append(NameError(node.line,node.index,'Variable already defined %s'% node.id))
        if node.value is not None:
            self.visit(node.value,scope,errors)
    #     else que hago? le pongo valor por defecto

    @visitor.when(ast.AssignNode)
    def visit(self, node,scope,errors):
    #     Verificamos si existe este símbolo
        vinfo = scope.get_variable_info(node.variable.id)
        if vinfo is None:
            errors.append(NameError(node.line,node.index,'Error while assinging '+ node.variable.id + 'not defined'))

        self.visit(node.expression,scope,errors)
        node.computed_type = vinfo.vtype

        if not node.expression.computed_type.is_lower(node.computed_type):
            errors.append(TypeError(node.line,node.index,'Error between lvalue {} and rvalue {}'.format(vinfo.vtype.name,
                                                                                                        node.expression.computed_type)))

    @visitor.when(ast.DispatchNode)
    def visit(self, node,scope, errors):
        '''
        Para revisar el dispatch: e0.f(e1,...,en)
        1-calcular los tipos ei
        2-verificar si todos los tipos de están definidos
        3-verificar si el tipo de e0 tiene definido el metodo f con los
            parámetro respectivos.
            3.1-cada uno de los tipos q le pasamos como parámetro tiene
                que ser lower than the original
        4-devolver el tipo del resultado del método

        :param node:
        :param scope:
        :param errors:
        :return:
        '''
        self.visit(node.left_expression,scope,errors)
        dispatch_type = node.left_expression.computed_type
        if not scope.is_defined(dispatch_type):
            errors.append(TypeError(node.line,node.index,'Error type {} not defined in dispatch'.format(dispatch_type)))

        method = scope.get_params_from_method(dispatch_type,node.func_id)
        for i, param in enumerate(node.parameters):
            self.visit(param,scope,errors)
            if not param.computed_type.is_lower(method.arguments[i][1]):
                errors.append(TypeError(node.line,node.index,'Error in dispatch node, type {} is not lower than {}'.format(param.computed_type.name,
                                                                                            method.arguments[i][1].name)))
        node.computed_type = method.return_type


    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node,scope, errors):
        self.visit(node.left_expression,scope,errors)
        dispatch_type = node.left_expression.computed_type
        if not scope.is_defined(dispatch_type):
            errors.append(TypeError(node.line,node.index,'Error type {} not defined in dispatch'.format(dispatch_type)))

        parent_type = scope.get_type(node.parent_type)
        if not dispatch_type.is_lower(parent_type):
            errors.append(TypeError(node.line,node.index,"Error parent type defined is not lower in static dispatch"))

        method = scope.get_params_from_method(parent_type,node.func_id)
        for i, param in enumerate(node.parameters):
            self.visit(param,scope,errors)
            if not param.computed_type.is_lower(method.arguments[i][1]):
                errors.append(TypeError(node.line,node.index,'Error in dispatch node, type {} is not lower than {}'.format(param.computed_type.name,
                                                                                            method.arguments[i][1].name)))
        node.computed_type = method.return_type



    @visitor.when(ast.ConditionalNode)
    def visit(self, node, scope, errors):
        '''
        Si e1 es de tipo bool, e2 de tipo T2 y e3 de tipo T3
        :param node:
        :param errors:
        :return: LCA de las expresiones e3 y e2
        '''
        self.visit(node.if_expression,scope,errors)
        then_child_scope = scope.create_child_scope()
        else_child_scope = scope.create_child_scope()
        self.visit(node.then_expression,then_child_scope,errors)
        self.visit(node.else_expression,else_child_scope,errors)

        if node.if_expression.computed_type != scope.get_type('Bool'):
            errors.append(TypeError(node.line,node.index,'Error. If Condition is not type bool'))
        lca = node.then_expression.computed_type.get_lca(node.else_expression.computed_type)
        node.computed_type = lca

    @visitor.when(ast.CaseNode)
    def visit(self, node,scope, errors):
        self.visit(node.case_expression,scope,errors)
        case_expression_type = node.case_expression.computed_type
        lcas = []
        for id_type,expr in node.implications:
            self.visit(expr,scope,errors)
            if not expr.computed_type.is_lower(id_type[1]):
                errors.append(TypeError(node.line, node.index,
                                        'Error in case node, type {} is not lower than {}'.format(
                                            id_type[1].name,
                                            expr.computed_type.name)))
            vtype = scope.get_type(id_type[1])
            if vtype is None:
                errors.append(TypeError(node.line,node.index,'Error in case expression, type {} not defined'.format(id_type[1])))
                return
            lcas.append(case_expression_type.get_lca(vtype))

        lca_joined = scope.get_type('Object')
        for lca in lcas:
            if lca.height > lca_joined.height:
                lca_joined = lca.height

        node.computed_type = lca_joined




    @visitor.when(ast.LoopNode)
    def visit(self, node,scope, errors):
        self.visit(node.while_expression,scope,errors)
        if node.while_expression.computed_type != scope.get_type('Bool'):
            errors.append(TypeError(node.line,node.index,'Error in while Condition expression'))
        child_scope = scope.create_child_scope()
        self.visit(node.loop_expression,child_scope,errors)
        node.computed_type = scope.get_type('Object')

    @visitor.when(ast.NewTypeNode)
    def visit(self, node,scope, errors):
        '''
        Hay dos casos para new:
        1- si T es SELF_TYPE:
        2- en otro caso
        en cualquier caso ahora mismo devolver el mismo tipo T
        Para checkear ahora mismo lo único que me parece que hay que ver
        es si está definido el Tipo T
        :param node:
        :param errors:
        :return:
        '''
        new_intance_type = scope.get_type(node.type_name)
        if new_intance_type is None:
            errors.append(NameError(node.line,node.index,'Error type {} is not defined'.format(node.type_name)))
        else:
            node.computed_type = new_intance_type

    @visitor.when(ast.BAritmeticOperationNode)
    def visit(self, node,scope, errors):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es Int
        '''
        self.visit(node.left_expression,scope,errors)
        self.visit(node.right_expression,scope,errors)
        if node.left_expression.computed_type == scope.get_type('Int') and \
                        node.left_expression.computed_type == scope.get_type('Int'):
            return
        errors.append(TypeError(node.line,node.index,"Error while checking types"))
        node.computed_type = scope.get_type('Int')

    #
    # @visitor.when(ast.PlusNode)
    # def visit(self, node, errors):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #
    #     pass
    #
    # @visitor.when(ast.StarNode)
    # def visit(self, node, errors):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass
    #
    # @visitor.when(ast.MinusNode)
    # def visit(self, node, errors):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass
    #
    # @visitor.when(ast.DivNode)
    # def visit(self, node, errors):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass

    @visitor.when(ast.NegationNode)
    def visit(self, node,scope, errors):
        '''
        <expr> tiene que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es Int
        '''
        self.visit(node.expression,scope,errors)
        if node.expression.computed_type == scope.get_type("Int"):
            return
        errors.append(TypeError(node.line,node.index,"Error while checking_type"))
        node.computed_type = scope.get_type('Int')

    @visitor.when(ast.IsVoidNode)
    def visit(self, node, scope, errors):
        self.visit(node.expression,scope,errors)
        boolean = scope.get_type('Bool')
        if node.expression.computed_type is not boolean:
            errors.append(TypeError(node.line,node.index,'Error, is void argument must be boolean'))
        node.computed_type = boolean


    @visitor.when(ast.NotNode)
    def visit(self, node,scope, errors):
        '''
        <expr> tiene que tener tipo bool
        :param node:
        :param errors:
        :return: devuelve tipo bool
        '''
        self.visit(node.expression,scope,errors)
        if node.expression.computed_type == scope.get_type("Bool"):
            return
        errors.append(TypeError(node.line,node.index,"Error while checking_type"))
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.LowerThanNode)
    def visit(self, node, scope,errors):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es bool
        '''
        self.visit(node.left_expression,scope,errors)
        if node.left_expression.computed_type == scope.get_type("Int"):
            return
        errors.append(TypeError(node.line,node.index,"Error while checking_type"))
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.LowerEqualThanNode)
    def visit(self, node, scope, errors):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es bool
        '''
        self.visit(node.left_expression,scope,errors)
        if node.left_expression.computed_type == scope.get_type("Int"):
            return
        errors.append(TypeError(node.line, node.index, "Error while checking_type"))
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.EqualThanNode)
    def visit(self, node, scope, errors):
        '''
        Si <expr1> o <expr2> son de tipo Int ,str or bool entonces el otro tiene que tener
        el mismo tipo. Para objetos no básicos, este símbolo chequea por la igualdad de punteros.
        Está definido para void.
        :param node:
        :param errors:
        :return:
        '''
        self.visit(node.left_expression,scope,errors)
        self.visit(node.right_expression,scope,errors)

        def selector(expression):
            return expression.computed_type == scope.get_type('Int') or \
                    expression.computed_type == scope.get_type('String') or \
                    expression.computed_type == scope.get_type('Bool')

        if selector(node.left_expression) or selector(node.right_expression):
            if node.left_expression.computed_type == node.right_expression.computed_type:
                return
            errors.append(TypeError(node.line, node.index, "Error while checking_type"))
        else:
            # Si se comparan dos clases no basicas hay que comparar los punteros
            pass
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.IntegerComplementNode)
    def visit(self, node,scope, errors):
        '''
        <expr> tiene que ser de tipo Int
        :param node:
        :param errors:
        :return: devuelve static type Int
        '''
        self.visit(node.expression,scope,errors)
        if node.expression.computed_type == scope.get_type('Int'):
            return
        errors.append(TypeError(node.line, node.index, "Error while checking_type"))
        node.computed_type = scope.get_type('Int')

    @visitor.when(ast.ObjectNode)
    def visit(self, node, scope, errors):

        if not scope.is_defined(node.id):
            errors.append(NameError(node.line,node.index,"Error, object {} does not exist".format(node.id)))
            return
        node.computed_type = scope.get_variable_info(node.id)[1]

    @visitor.when(ast.BlockNode)
    def visit(self, node,scope, errors):
        child_scope = scope.create_child_scope()
        for expr in node.expressions:
            self.visit(expr,child_scope,errors)

        node.computed_type = node.expressions[-1].computed_type

    @visitor.when(ast.LetVarNode)
    def visit(self, node, scope, errors):
        '''

        :param node:
        :param scope:
        :param errors:
        :return:
        '''
        child_scope = scope.create_child_scope()
        for id_type, expr in node.declaration_list:
            vtype = scope.get_type(id_type[1])
            if vtype is None:
                errors.append(TypeError(node.line,node.index,'Error in let. type not defined'))
                return

            if expr is not None:
                self.visit(expr,child_scope,errors)
                if not expr.computed_type.is_lower(vtype):
                    errors.append(TypeError(node.line,node.index,"Error in let. "))
            child_scope.define_variable(id_type[0],id_type[1])
        self.visit(node.in_expression,child_scope,errors)
        node.computed_type = node.in_expression.computed_type


    @visitor.when(ast.IntNode)
    def visit(self, node, scope,errors):
        node.computed_type = scope.get_type('Int')

    @visitor.when(ast.BoolNode)
    def visit(self, node,scope, errors):
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.StrNode)
    def visit(self, node,scope, errors):
        node.computed_type = scope.get_type('Str')


# class CheckSemanticsVisitor:
#     @visitor.on('node')
#     def visit(self, node, scope, errors):
#         pass
#
#     @visitor.when(ast.ProgramNode)
#     def visit(self, node, scope, errors):
#         scope = Scope()
#         return self.visit(node.expr, scope, errors)
#
#     @visitor.when(ast.BinaryOperatorNode)
#     def visit(self, node, scope, errors):
#         rleft = self.visit(node.left, scope, errors)
#         rright = self.visit(node.right, scope, errors)
#         return rleft and rright
#
#     @visitor.when(ast.UnaryOperatorNode)
#     def visit(self, node, scope, errors):
#         return self.visit(node.expr, scope, errors)
#
#     @visitor.when(ast.LetVarNode)
#     def visit(self, node, scope, errors):
#         child_scope = scope.create_child_scope()
#         rtype = INTEGER
#         for declaration in node.declaration_list:
#             rtype &= self.visit(declaration, child_scope, errors)
#         rtype &= self.visit(node.expr, child_scope, errors)
#         return rtype
#
#     @visitor.when(ast.BlockNode)
#     def visit(self, node, scope, errors):
#         rtype = INTEGER
#         for expr in node.expr_list:
#             rtype = self.visit(expr, scope, errors)
#         return rtype
#
#     @visitor.when(ast.AssignNode)
#     def visit(self, node, scope, errors):
#         rtype = self.visit(node.expr, scope, errors)
#         vname = node.idx_token.text_token
#         if not scope.is_defined(vname):
#             errors.append('[line:%s,column:%s]: Variable \'%s\' not defined.' % (node.idx_token.col, vname))
#             return ERROR
#         node.variable_info = scope.get_variable_info(vname)
#         return rtype
#
#     @visitor.when(ast.IntNode)
#     def visit(self, node, scope, errors):
#         return INTEGER
#
#     @visitor.when(ast.VariableNode)
#     def visit(self, node, scope, errors):
#         vname = node.idx_token.text_token
#         if not scope.is_defined(vname):
#             errors.append('[line:%s,column:%s]: Variable \'%s\' not defined.' % (node.idx_token.row, node.idx_token.col, vname))
#             return ERROR
#         node.variable_info = scope.get_variable_info(vname)
#         return INTEGER

    # @visitor.when(ast.PrintIntegerNode)
    # def visit(self, node, scope, errors):
    #     return self.visit(node.expr, scope, errors)

    # @visitor.when(ast.PrintStringNode)
    # def visit(self, node, scope, errors):
    #     return INTEGER

    # @visitor.when(ast.ScanNode)
    # def visit(self, node, scope, errors):
    #     return INTEGER