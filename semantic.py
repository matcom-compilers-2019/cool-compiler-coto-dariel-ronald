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
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node):
        classes_names = set()
        for program_class in node.classes:
            if program_class.name in classes_names:
                throw_exception(TypeError, node.line, node.index, 'Type %s already defined' % program_class.name)
            classes_names.add(program_class.name)
            self.visit(program_class)

    @visitor.when(ast.ClassNode)
    def visit(self, node):
        if node.inherit != 'Object' and node.inherit in builtins_classes_names:
            throw_exception(TypeError, node.line, node.index, "Builtin type %s can't not be inherited" % node.inherit)
        if node.inherit == 'Main':
            throw_exception(TypeError, node.line, node.index, "Main class can't be inherited")
        self.context.create_type(node.name, node.inherit, node.line, node.index)


class TypeBuilderVisitor:
    def __init__(self,scope):
        self.context = scope
        self._current_type = None

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node):
        for program_class in node.classes:
            if program_class not in builtins_classes:
                self.visit(program_class)

    @visitor.when(ast.ClassNode)
    def visit(self, node):
        self._current_type = self.context.get_type(node.name)
        if not self._current_type.define_parent(self.context):
            throw_exception(TypeError,node.line,node.index,
                                    'Type %s is not defined'% self._current_type._parent_type_name)
        methods_names = set()
        for methoddef in node.methods:
            if methoddef.id in methods_names:
                throw_exception(TypeError,node.line, node.index, 'Method %s already defined' % methoddef.id)
            methods_names.add(methoddef.id)
            self.visit(methoddef)
        attr_names = set()
        for attrdef in node.attributes:
            if attrdef.id in attr_names:
                throw_exception(TypeError,node.line, node.index, 'Attr %s already defined' % attrdef.id)
            attr_names.add(attrdef.id)
            self.visit(attrdef)

    @visitor.when(ast.MethodNode)
    def visit(self, node):
        return_type = self.context.get_type(node.return_type)
        if return_type is None:
            throw_exception(TypeError,node.line, node.index, 'Return Type %s not defined' % return_type)
        params = []
        param_names = set()
        for id, type_name in node.parameters:
            type_class = self.context.get_type(type_name)
            if type_class is None:
                throw_exception(TypeError, node.line,node.index,'Param Type %s not defined' % type_name)
            if id in param_names:
                throw_exception(TypeError, node.line, node.index, 'Param Name %s already defined' % id)
            param_names.add(id)

            params.append((id, type_class))
        self._current_type.define_method(node.id,return_type,params)

    @visitor.when(ast.AttributeNode)
    def visit(self, node):
        attr_type = self.context.get_type(node.type)
        if attr_type is None:
            throw_exception(TypeError, node.line, node.index, 'Type %s not defined' % attr_type)
        self._current_type.define_attr(node.id, attr_type)


#Todo: tengo que verificar que el ProgramNode tiene una claseMain la cual tiene un metodo main()
class TypeCheckerVisitor:
    def __init__(self):
        self.current_class_name = ''

    # def check_methods_inheritence(self,scope):
    #     types_ = scope.scope_classes_dictionary.values()
    #     mask_types = {i:False for i in types_}
    #
    #     for _type in types_:
    #
    # def _checkup(self,_type:Type):
    #     if _type.name == 'Object':
    #
    def look_for_Main_Class(self,context):
        main_type = context.type_is_defined('Main')
        if main_type is not None:
            throw_exception(
                NameError,0, 0, "Can not find Main class")

        if main_type.parent_type_name != 'Object':
            throw_exception(TypeError, 0, 0, "Class Main can't inherits from other class")

        main_method = main_type.get_method('main')
        if main_method is None:
            throw_exception(TypeError, 0, 0, "Class Main does't have a main method")


    def check_class_hierarchy(self,context):
        classes = context._classes_global_field()

        for class_ in classes.values():
            if class_._checked_for_cycle:
                continue

            for current_type in class_.get_hierarchy_iterator():
                if current_type._checking_for_cycle:
                    throw_exception(SemanticError,current_type.line,current_type.index,
                                    'Ciclo en la jerarquía de %s' % current_type.name)
                current_type._checking_for_cycle = True

            for current_type in class_.get_hierarchy_iterator():
                current_type._checking_for_cycle = False

            for current_type in class_.get_hierarchy_iterator():
                current_type._checked_for_cycle = True

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node,scope):
        for cool_class in node.classes:
            self.visit(cool_class,scope)

    @visitor.when(ast.ClassNode)
    def visit(self, node,scope):

        self.current_class_name = node.name

        for attr in node.attributes:
            self.visit(attr,scope)

        for method in node.methods:
            child_scope = scope.create_child_scope()
            self.visit(method,child_scope)

    @visitor.when(ast.MethodNode)
    def visit(self, node, scope):

        # Añadimos los parametros como variables locales
        for param_name,param_type_name in node.parameters:
            vinfo = scope.define_variable(param_name,param_type_name)
            if vinfo is None:
                throw_exception(NameError, node.line,node.index,"Error in method {}: parameter {}".format(node.id,param_name))

        # Añadimos el objeto self del tipo current type
        scope.define_variable('self', self.current_class_name)

        self.visit(node.expressions,scope)

        if node.expressions[-1].computed_type.lower_equals(node.return_type):
            throw_exception(TypeError, node.line, node.index, "Error in method {}: return static type expected {}, founded:{}".
                          format(node.id,node.return_type,node.expressions[-1].computed_type))

    @visitor.when(ast.AttributeNode)
    def visit(self, node, scope):
        vinfo = scope.define_variable(node.id, node.type)
        if vinfo is None:
            throw_exception(NameError, node.line, node.index, 'Variable already defined %s' % node.id)
        if node.value is not None:
            self.visit(node.value, scope)

    @visitor.when(ast.AssignNode)
    def visit(self, node,scope):
        # Verificamos si existe este símbolo
        vinfo = scope.get_variable_info(node.variable.id)
        if vinfo is None:
            throw_exception(NameError, node.line, node.index, 'Error while assinging ' + node.variable.id + 'not defined')
        if vinfo.name == 'self':
            throw_exception(TypeError, node.line, node.index, 'self object can not be assign')
        self.visit(node.expression, scope)
        node.computed_type = vinfo.vtype

        if not node.expression.computed_type.lower_equals(node.computed_type):
            throw_exception(TypeError, node.line, node.index, 'Error between lvalue {} and rvalue {}'.format(vinfo.vtype.name,
                                                                                                        node.expression.computed_type))

    @visitor.when(ast.DispatchNode)
    def visit(self, node,scope):
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
        self.visit(node.left_expression,scope)

        dispatch_type = node.left_expression.computed_type
        if dispatch_type is None:
            throw_exception(TypeError, node.line,node.index,'Error type {} not defined in dispatch'.format(dispatch_type))
        # verificar primero que exista el metodo subiendo por el árbol de la jerarquía
        # ,luego q tenga la misma cnt de argumentos, verificar su tipo
        method = scope.get_params_from_method(dispatch_type.name,node.func_id)
        if method is None:
            throw_exception(TypeError,node.line,node.index,"Method %s doesn't exist on type %s" % (node.func_id,
                                                                                                   dispatch_type.name))
        if len(method.arguments) != len(node.parameters):
            throw_exception(TypeError, node.line, node.index, "Method %s expected to received %i params, founded: %i" %
                                                              (node.func_id, len(method.arguments), len(node.parameters)))

        for i, param in enumerate(node.parameters):
            self.visit(param, scope)
            if not param.computed_type.lower_equals(method.arguments[i][1]):
                throw_exception(TypeError, node.line, node.index, 'Error in dispatch node, type {} is not lower than {}'
                                .format(param.computed_type.name,
                                        method.arguments[i][1].name))
        node.computed_type = method.return_type

    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node, scope):
        self.visit(node.left_expression, scope)
        dispatch_type = node.left_expression.computed_type
        # if dispatch_type is None:
        #     throw_exception(TypeError, node.line,node.index,'Type {} not defined'.format(dispatch_type))

        parent_type = scope.get_type(node.parent_type)
        if parent_type is None:
            throw_exception(TypeError, node.line, node.index, 'Type {} not defined'.format(node.parent_type))

        if not dispatch_type.lower_equals(parent_type):
            throw_exception(TypeError, node.line,node.index,"Parent %s type defined is not lower than %s" % parent_type.name)

        method = scope.get_params_from_method(parent_type,node.func_id)
        for i, param in enumerate(node.parameters):
            self.visit(param, scope)

            if not param.computed_type.lower_equals(method.arguments[i][1]):
                throw_exception(TypeError, node.line,node.index,'Error in dispatch node, type {} is not lower than {}'.format(param.computed_type.name,
                                                                                            method.arguments[i][1].name))
        node.computed_type = method.return_type

    @visitor.when(ast.ConditionalNode)
    def visit(self, node, scope):
        '''
        Si e1 es de tipo bool, e2 de tipo T2 y e3 de tipo T3
        :param node:
        :param errors:
        :return: LCA de las expresiones e3 y e2
        '''
        then_child_scope = scope.create_child_scope()
        else_child_scope = scope.create_child_scope()

        self.visit(node.if_expression,scope)
        self.visit(node.then_expression,then_child_scope)
        self.visit(node.else_expression,else_child_scope)

        if node.if_expression.computed_type != scope.get_type('Bool'):
            throw_exception(TypeError, node.line,node.index,'Error. If Condition is not type bool')
        lca = node.then_expression.computed_type.get_lca(node.else_expression.computed_type)
        node.computed_type = lca

    @visitor.when(ast.CaseNode)
    def visit(self, node, scope):
        self.visit(node.case_expression,scope)

        id_s_types = set()
        lcas = []
        for id_typeName, expr in node.implications:
            implication_id_type = scope.get_type(id_typeName)
            if implication_id_type is None:
                throw_exception(TypeError, node.line, node.index,
                                'Type {} not defined'.format(id_typeName[1]))
            if id_typeName[1] in id_s_types:
                throw_exception(TypeError, node.line, node.index, 'Type {} already defined on Case Node'
                                .format(id_typeName[1]))

            id_s_types.add(id_typeName[1])
            child_scope = scope.create_child_scope()
            if child_scope.define_variable(*id_typeName) is None:
                throw_exception(TypeError, node.line, node.index, 'Variable definition {} not valid'
                                .format(id_typeName))

            self.visit(expr,child_scope)
            lcas.append(expr.computed_type)

        lca_joined = lcas[0]
        for lca in lcas[1:]:
            
            if lca.height > lca_joined.height:
                lca_joined = lca
        node.computed_type = lca_joined

    @visitor.when(ast.LoopNode)
    def visit(self, node,scope):
        self.visit(node.while_expression,scope)

        if node.while_expression.computed_type != scope.get_type('Bool'):
            throw_exception(TypeError, node.line,node.index,'Error in while Condition expression')

        child_scope = scope.create_child_scope()
        self.visit(node.loop_expression,child_scope)

        node.computed_type = scope.get_type('Object')


    @visitor.when(ast.NewTypeNode)
    def visit(self, node,scope):
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
            throw_exception(NameError, node.line,node.index,'Error type {} is not defined'.format(node.type_name))
        else:
            node.computed_type = new_intance_type

    @visitor.when(ast.BAritmeticOperationNode)
    def visit(self, node,scope):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es Int
        '''
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        if node.left_expression.computed_type == scope.get_type('Int') and \
                        node.right_expression.computed_type == scope.get_type('Int'):
            node.computed_type = scope.get_type('Int')
            return

        throw_exception(TypeError, node.line,node.index,"Error while checking types")


    # @visitor.when(ast.PlusNode)
    # def visit(self, node):
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
    # def visit(self, node):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass
    #
    # @visitor.when(ast.MinusNode)
    # def visit(self, node):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass
    #
    # @visitor.when(ast.DivNode)
    # def visit(self, node):
    #     '''
    #     <expr1> y <expr2> tienen que tener tipo Int
    #     :param node:
    #     :param errors:
    #     :return: el resultado es Int
    #     '''
    #     pass

    @visitor.when(ast.NegationNode)
    def visit(self, node, scope):
        '''
        <expr> tiene que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es Int
        '''
        self.visit(node.expression,scope)

        if node.expression.computed_type == scope.get_type("Int"):
            node.computed_type = scope.get_type('Int')
            return

        throw_exception(TypeError, node.line,node.index,"Error while checking_type")

    @visitor.when(ast.IsVoidNode)
    def visit(self, node, scope):
        self.visit(node.expression,scope)

        boolean = scope.get_type('Bool')
        if node.expression.computed_type is not boolean:
            throw_exception(TypeError, node.line,node.index,'Error, is void argument must be boolean')
        node.computed_type = boolean

    @visitor.when(ast.NotNode)
    def visit(self, node,scope):
        '''
        <expr> tiene que tener tipo bool
        :param node:
        :param errors:
        :return: devuelve tipo bool
        '''
        self.visit(node.expression,scope)

        if node.expression.computed_type == scope.get_type("Bool"):
            node.computed_type = scope.get_type('Bool')
            return
        throw_exception(TypeError, node.line,node.index,"Error while checking_type")

    @visitor.when(ast.LowerThanNode)
    def visit(self, node, scope):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es bool
        '''
        self.visit(node.left_expression,scope)

        if node.left_expression.computed_type == scope.get_type("Int"):
            node.computed_type = scope.get_type('Bool')
            return
        throw_exception(TypeError, node.line,node.index,"Error while checking_type")

    @visitor.when(ast.LowerEqualThanNode)
    def visit(self, node, scope):
        '''
        <expr1> y <expr2> tienen que tener tipo Int
        :param node:
        :param errors:
        :return: el resultado es bool
        '''
        self.visit(node.left_expression, scope)

        if node.left_expression.computed_type == scope.get_type("Int"):
            node.computed_type = scope.get_type('Bool')
            return
        throw_exception(TypeError, node.line, node.index, "Error while checking_type")

    @visitor.when(ast.EqualThanNode)
    def visit(self, node, scope):
        '''
        Si <expr1> o <expr2> son de tipo Int ,str or bool entonces el otro tiene que tener
        el mismo tipo. Para objetos no básicos, este símbolo chequea por la igualdad de punteros.
        Está definido para void.
        :param node:
        :param errors:
        :return:
        '''
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        def selector(expression):
            return expression.computed_type == scope.get_type('Int') or \
                    expression.computed_type == scope.get_type('String') or \
                    expression.computed_type == scope.get_type('Bool')

        if selector(node.left_expression) or selector(node.right_expression):
            if node.left_expression.computed_type == node.right_expression.computed_type:
                node.computed_type = scope.get_type('Bool')
                return
            throw_exception(TypeError(node.line, node.index, "Error while checking_type"))
        else:
            # Si se comparan dos clases no basicas hay que comparar los punteros
            pass
        node.computed_type = scope.get_type('Bool')

    @visitor.when(ast.IntegerComplementNode)
    def visit(self, node, scope):
        '''
        <expr> tiene que ser de tipo Int
        :param node:
        :param errors:
        :return: devuelve static type Int
        '''
        self.visit(node.expression,scope)

        if node.expression.computed_type == scope.get_type('Int'):
            node.computed_type = scope.get_type('Int')
            return
        throw_exception(TypeError(node.line, node.index, "Error while checking_type"))

    @visitor.when(ast.ObjectNode)
    def visit(self, node, scope):
        if not scope.is_defined(node.id):
            throw_exception(NameError, node.line,node.index,"Error, object {} does not exist".format(node.id))
        node.computed_type = scope.get_variable_info(node.id).vtype

    @visitor.when(ast.BlockNode)
    def visit(self, node,scope):
        child_scope = scope.create_child_scope()
        for expr in node.expressions:
            self.visit(expr,child_scope)

        node.computed_type = node.expressions[-1].computed_type

    @visitor.when(ast.LetVarNode)
    def visit(self, node, scope):
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
                throw_exception(TypeError, node.line,node.index,'Error in let. Type %s not defined'% id_type[1])

            if expr is not None:
                self.visit(expr,child_scope)

                if not expr.computed_type.lower_equals(vtype):
                    throw_exception(TypeError(node.line,node.index,"Error in let. Type %s isn't lower than %s"
                                              % (expr.computed_type.name, vtype.name)))

            child_scope.define_variable(id_type[0], id_type[1])

        self.visit(node.in_expression, child_scope)
        node.computed_type = node.in_expression.computed_type

    @visitor.when(ast.IntNode)
    def visit(self, node, scope):
        node.computed_type = scope.get_type('Int')

    @visitor.when(ast.BoolNode)
    def visit(self, node,scope):
        node.computed_type = scope.get_type('Bool')


    @visitor.when(ast.StrNode)
    def visit(self, node,scope):
        node.computed_type = scope.get_type('String')
