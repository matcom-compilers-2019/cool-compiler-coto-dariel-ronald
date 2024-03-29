import NodosAST as ast
from cil_hierarchy import *
import visitor
from built_in import *
from static_functions import *
from strings_visitor import StringVisitor
from cil_writer import *
from cool_utils import value_bultin_types
from cil_utils import CILScope


class COOLToCILVisitor:
    def __init__(self):
        self.dotdata = CILDataNode()
        self.dottypes = []
        self.dotcode = []
        self.static_functions = []
        self.current_type_attrs = []
        self.current_function_name = ""
        self.internal_count = 0
        self.label_count = 0

        self.types_index = []
        self.functions_index = []
        self.data_bultins_labels = {'Int': self.register_data('Int'),
                                    'Bool': self.register_data('Bool'),
                                    'String': self.register_data('String')
                                    }

    # ======================================================================
    # =[ UTILS ]============================================================
    # ======================================================================

    def build_internal_vname(self):
        vname = f'{self.internal_count}_{self.current_function_name}'
        self.internal_count += 1
        return vname

    def define_internal_local(self):
        vinfo = self.build_internal_vname()
        # local_node = CILLocalNode(vinfo)
        self.dotcode[-1].functions[-1].localvars.append(vinfo)
        return vinfo

    def register_instruction(self, instruction_type, *args):
        instruction = instruction_type(*args)
        self.dotcode[-1].functions[-1].instructions.append(instruction)
        return instruction

    def register_data(self, value):
        vname = f'data_{len(self.dotdata.data)}'
        data_node = CILDataElementNode(vname, value)
        self.dotdata.data.append(data_node)
        return data_node


    #user defined stuff
    def build_user_defined_vname(self,vname):
        name = f'{self.internal_count}_{self.current_function_name}_user_defined_{vname}'
        self.internal_count += 1
        return name

    def define_ud_internal_local(self, vinfo, scope: CILScope):
        alias = self.build_user_defined_vname(vinfo)
        scope.define_variable(vinfo, alias)
        self.dotcode[-1].functions[-1].localvars.append(alias)
        return alias

    
    #jump help methods
    #devuelve el índice de la próxima instrucción
    def next_instruction_index(self):
        return len(self.dotcode[-1].functions[-1].instructions)

    def next_label(self):
        self.label_count += 1
        return "L"+str(self.label_count)

    def get_full_local_name(self, name):
        for x in self.dotcode[-1].functions[-1].localvars:
            splitted = x.vinfo.split("_")
            if splitted[-1] == name:
                return x.vinfo
        return name

    # ======================================================================


    # ======================================================================
    # =[ VISIT ]============================================================
    # ======================================================================

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ast.ProgramNode)
    def visit(self, node: ast.ProgramNode, scope:CILScope):
        s_vis = StringVisitor()
        s_vis.visit(node)
        self.aux_dottypes = s_vis.dottypes
        self.dotdata.data = s_vis.dotdata

        self.dotcode.append(CILCodeNode())
        get_distance(self)
        get_closest_type(self)
        self.dotcode.remove(self.dotcode[-1])

        add_built_in(self)
        for program_class in node.classes:
            child_scope = scope.create_child_scope()
            self.visit(program_class,child_scope)
        
        result = CILProgramNode(self.dottypes, self.dotdata, self.dotcode, self.static_functions)
        writer = CILWriterVisitor()
        writer.visit(result)
        for x in writer.output:
            print(x)

        return result

    @visitor.when(ast.ClassNode)
    def visit(self, node: ast.ClassNode, scope: CILScope):
        self.dottypes.append(CILTypeNode(node.name, node.inherit))
        self.dotcode.append(CILCodeNode())

        self.current_type_attrs = set([n.id for n in node.attributes])

        constructor_method_name = f'{node.name}_cil_attributes_initializer'
        self.dottypes[-1].methods.append(constructor_method_name)
        self.current_function_name = constructor_method_name
        self.dotcode[-1].functions.append(CILFunctionNode(constructor_method_name))
        index = 'self'
        self.dotcode[-1].functions[-1].localvars.append(index)
        self.register_instruction(CILAssignNode, index, CILAllocateNode(node.name))
        for attr in node.attributes:
            child_scope = scope.create_child_scope()
            self.visit(attr, child_scope)
            if attr.value is not None:
                self.visit(attr.value, child_scope)
                self.register_instruction(CILSetAttributeNode, attr.id, index, attr.value.holder)
            else:
                if attr.type == "Int" or attr.type == "Bool":
                    self.register_instruction(CILSetAttributeNode, attr.id, index, 0)
                elif attr.type == "String":
                    self.register_instruction(CILSetAttributeNode, attr.id, index, 'void')
                else:
                    self.register_instruction(CILSetAttributeNode, attr.id, index, "")
        self.register_instruction(CILReturnNode, index)

        for method in node.methods:
            child_scope = scope.create_child_scope()
            self.visit(method,child_scope)

        # self.add_parent_attr()

    @visitor.when(ast.MethodNode)
    def visit(self, node: ast.MethodNode, scope: CILScope):
        name = f'{self.dottypes[-1].name}_{node.id}'
        self.current_function_name = name
        self.dottypes[-1].methods.append(name)
        self.dotcode[-1].functions.append(CILFunctionNode(name,["self"]))
        for x,_ in node.parameters:
            vinfo = self.build_user_defined_vname(x)
            self.dotcode[-1].functions[-1].params.append(vinfo)
            
        if type(node.expression) is ast.BlockNode:
            for expr in node.expression.expressions:
                self.visit(expr, scope)
            self.register_instruction(CILReturnNode, node.expression.expressions[-1].holder)
            node.holder = node.expression.expressions[-1].holder
        else:
            self.visit(node.expression,scope)
            self.register_instruction(CILReturnNode, node.expression.holder)
            node.holder = node.expression.holder

    @visitor.when(ast.AttributeNode)
    def visit(self, node:ast.AttributeNode, scope: CILScope):
        self.dottypes[-1].attributes.append(node.id)

    def make_boxing(self, variable, type_name, value):
        self.register_instruction(CILAssignNode, variable, CILAllocateNode(type_name))
        self.register_instruction(CILSetAttributeNode, 'attr_value', variable, value)

    def make_unboxing(self, variable, instance):
        self.register_instruction(CILAssignNode, variable, CILGetAttributeNode('attr_value', instance))

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode, scope:CILScope):

        self.visit(node.expression, scope)
        expression_type_name = node.expression.computed_type.name

        # si la asignacion es sobre un attr
        if node.variable.id in self.current_type_attrs:
            temp_local = node.expression.holder
            if expression_type_name in value_bultin_types and \
                            node.computed_type.name not in value_bultin_types:
                temp_local = self.define_internal_local()
                self.make_boxing(temp_local,expression_type_name,node.expression.holder)
            self.register_instruction(CILSetAttributeNode, node.variable.id,'self',temp_local)
            node.holder = node.variable.id
            return

        # si se le asigna a un objeto por referencia un objeto por valor
        # hacer boxing
        if expression_type_name in value_bultin_types and \
                node.computed_type.name not in value_bultin_types:
            self.make_boxing(node.variable.id, node.variable.computed_type.name,
                             node.expression.holder)
            return

        if not (node.variable in self.dotcode[-1].functions[-1].localvars):
            self.visit(node.variable,scope)

        self.register_instruction(CILAssignNode, node.variable.holder, node.expression.holder)
        node.holder = node.variable.id

    @visitor.when(ast.DispatchNode)
    def visit(self, node: ast.DispatchNode, scope: CILScope):
        self.visit(node.left_expression, scope)
        left_expression = 'self'

        for exp in node.parameters:
            self.visit(exp, scope)

        if node.left_expression is not None:
            left_expression = node.left_expression.holder
            left_expression_type_name = node.left_expression.computed_type.name

            # si es un tipo por valor la expresion izquierda, entonces hacemos boxing
            if left_expression_type_name == 'Int' or left_expression_type_name == 'Bool'\
                    or (left_expression_type_name == "String" and
                            (node.func_id != 'concat' and node.func_id != 'length' and node.func_id != 'substr')):
                vinfo = self.define_internal_local()
                self.make_boxing(vinfo, left_expression_type_name, left_expression)
                left_expression = vinfo

        # Se obtiene el tipo de la expresion izquierda
        # self.define_internal_local()
        if node.func_id == 'concat':
            my_call = CILBuiltInCallNode('String_concat')
            left_expression = node.left_expression.holder
        elif node.func_id == 'length':
            my_call = CILBuiltInCallNode('String_length')
            left_expression = node.left_expression.holder
        elif node.func_id == 'substr':
            my_call = CILBuiltInCallNode('String_substr')
            left_expression = node.left_expression.holder
        else:
            my_call = CILDynamicCallNode(node.func_id, left_expression)
        # aqui se ponen los params
        my_call.params.append(left_expression)
        for exp in node.parameters:
            my_call.params.append(exp.holder)

        # Llamado a la funcion

        holder = self.define_internal_local()
        self.register_instruction(CILAssignNode, holder, my_call)
        node.holder = holder

    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node: ast.StaticDispatchNode, scope:CILScope):
        self.visit(node.left_expression,scope)
        for x in node.parameters:
            self.visit(x,scope)

        left_expression = self.dottypes[-1].name
        if node.left_expression is not None:
            left_expression = node.left_expression.holder

        my_call = CILStaticCallNode(node.func_id, node.parent_type, left_expression)

        #aqui se ponen los params
        my_call.params.append(left_expression)
        for exp in node.parameters:
            my_call.params.append(exp.holder)

        #Llamado a la funcion
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, my_call)
        node.holder = holder

    @visitor.when(ast.ConditionalNode)
    def visit(self, node: ast.ConditionalNode,scope):
        self.visit(node.if_expression,scope)
        l_then = self.next_label()
        l_else = self.next_label()
        l_end = self.next_label()

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILGotoIfNode,node.if_expression.holder, l_then)
        self.register_instruction(CILGotoNode, l_else)
        self.register_instruction(CILLabelNode, l_then)

        self.visit(node.then_expression,scope)
        self.register_instruction(CILAssignNode, holder, node.then_expression.holder)
        
        self.register_instruction(CILGotoNode, l_end)
        self.register_instruction(CILLabelNode, l_else)

        self.visit(node.else_expression,scope)
        self.register_instruction(CILAssignNode, holder, node.else_expression.holder)

        self.register_instruction(CILLabelNode, l_end)

        node.holder = holder

    @visitor.when(ast.LoopNode)
    def visit(self, node: ast.LoopNode,scope:CILScope):
        l_condition = self.next_label()
        l_loop = self.next_label()
        l_end = self.next_label()
        self.register_instruction(CILLabelNode, l_condition)
        self.visit(node.while_expression, scope)

        self.register_instruction(CILGotoIfNode, node.while_expression.holder, l_loop)
        self.register_instruction(CILGotoNode, l_end)
        self.register_instruction(CILLabelNode, l_loop)

        self.visit(node.loop_expression,scope)
        self.register_instruction(CILGotoNode, l_condition)
        self.register_instruction(CILLabelNode,l_end)
        
        node.holder = 0

    @visitor.when(ast.LetVarNode)
    def visit(self, node: ast.LetVarNode, scope:CILScope):
        child_scope = scope.create_child_scope()
        for dec in node.declarations:
            declaration_type_name = dec[0][1]
            user_local = self.define_ud_internal_local(dec[0][0], child_scope)
            default_value = 'void'
            user_local_is_bultin = False
            if declaration_type_name in value_bultin_types:
                user_local_is_bultin = True
                if declaration_type_name == "Int" or declaration_type_name == "Bool":
                    default_value = 0
                else:
                    default_value = ''
            if dec[1] is not None:
                self.visit(dec[1], scope)
                rigth_expr_type_name = dec[1].computed_type.name

                # verificamos si hay que hacer boxing
                if not user_local_is_bultin and rigth_expr_type_name in value_bultin_types:
                    self.make_boxing(user_local,rigth_expr_type_name,dec[1].holder)
                    continue
                self.register_instruction(CILAssignNode,user_local, dec[1].holder)
            else:
                self.register_instruction(CILAssignNode, user_local, default_value)

        self.visit(node.in_expression,child_scope)
        node.holder = node.in_expression.holder

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode,scope: CILScope):
        # Se genera el codigo de la expresion inicial del case
        self.visit(node.case_expression,scope)
        expr0_value = node.case_expression.holder
        end_case_label = self.next_label()

        # verificamos si hay q hacer boxing
        expr0_type_name = node.case_expression.computed_type.name
        if expr0_type_name in value_bultin_types:
            vinfo = self.define_internal_local()
            self.make_boxing(vinfo,expr0_type_name,expr0_value)
            expr0_value = vinfo

        #Aqui se crea un array que tendra todos los tipos correpondientes a las variables de las implicaciones
        #en orden

        arr = self.define_internal_local()
        self.register_instruction(CILAssignNode, arr, CILArrayNode(len(node.implications)))
        for i in range(0, len(node.implications)):
            self.register_instruction(CILSetIndexNode, arr, i + 1, 'type_' + node.implications[i][0][1])

        #Aqui se obtiene el tipo del resultado de evaluar la expresion inicial del case
        expr0_type = self.define_internal_local()
        self.register_instruction(CILAssignNode, expr0_type, CILTypeOfNode(expr0_value))

        #Se realiza un llamado a la funcion estatica "get_closest_type", cuyo retorno se le asigna a closest_type_index
        closest_type_index = self.define_internal_local()
        bcall = CILBuiltInCallNode("__get_closest_type")
        bcall.params = [expr0_type, arr]
        self.register_instruction(CILAssignNode, closest_type_index, bcall)

        #Se crea un array que contendra los labels de las expresiones a visitar
        array_labels = self.define_internal_local()
        self.register_instruction(CILAssignNode, array_labels, CILArrayNode(len(node.implications)))
        labels = []
        local_user_vars = []
        for i in range(len(node.implications)):
            l_next = self.next_label()
            user_local = self.define_ud_internal_local(node.implications[i][0][0],scope)
            # temp_local = self.dotcode[-1].functions[-1].localvars[-1]
            local_user_vars.append(user_local)
            labels.append(l_next)
            self.register_instruction(CILSetIndexNode, array_labels, i + 1, l_next)

        #Se define en un goto a que label correspondiente a una de las expr se realizara el salto
        self.define_internal_local()
        label_index = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, label_index, CILGetIndexNode(array_labels, closest_type_index))
        self.register_instruction(CILGotoNode, label_index)

        self.define_internal_local()
        final_holder = self.dotcode[-1].functions[-1].localvars[-1]

        #Es generado el codigo de las expresiones de las implicaciones y se les asignan sus respectivos labels////
        for i in range(0, len(node.implications)):
            self.register_instruction(CILLabelNode, labels[i])
            implication = node.implications[i]
            # si el tipo de la rama es es por valor entonces hacemos unboxing
            if implication[0][1] in value_bultin_types:
                self.make_unboxing(local_user_vars[i], expr0_value)
                self.visit(node.implications[i][1],scope)
                self.register_instruction(CILAssignNode, final_holder, node.implications[i][1].holder)
                self.register_instruction(CILGotoNode, end_case_label)
                continue
            self.register_instruction(CILAssignNode, local_user_vars[i], expr0_value)
            self.visit(node.implications[i][1],scope)
            self.register_instruction(CILAssignNode, final_holder, node.implications[i][1].holder)
            self.register_instruction(CILGotoNode,end_case_label)
        self.register_instruction(CILLabelNode, end_case_label)
        node.holder = final_holder

    @visitor.when(ast.NewTypeNode)
    def visit(self, node: ast.NewTypeNode,scope:CILScope):
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        constructor_name = f'{node.type_name}_cil_attributes_initializer'
        self.register_instruction(CILAssignNode, holder, CILBuiltInCallNode(constructor_name))
        node.holder = holder

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILPlusNode(left, right))
        node.holder = holder

    @visitor.when(ast.MinusNode)
    def visit(self, node: ast.MinusNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILMinusNode(left, right))
        node.holder = holder

    @visitor.when(ast.StarNode)
    def visit(self, node: ast.StarNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILStarNode(left, right))
        node.holder = holder

    @visitor.when(ast.DivNode)
    def visit(self, node:ast.DivNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILDivNode(left, right))
        node.holder = holder

    @visitor.when(ast.NegationNode)
    def visit(self, node: ast.NegationNode,scope:CILScope):
        self.visit(node.expression,scope)
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILMinusNode(0, node.expression.holder))

        node.holder = holder

    @visitor.when(ast.NotNode)
    def visit(self, node: ast.NotNode,scope:CILScope):
        self.visit(node.expression,scope)
        self.define_internal_local()
        local_dest = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, local_dest, CILMinusNode(1,node.expression.holder))

        node.holder = local_dest

    @visitor.when(ast.LowerThanNode)
    def visit(self, node: ast.LowerThanNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        local_dest = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, local_dest, CILLowerThanNode(left, right))
        node.holder = local_dest

    @visitor.when(ast.LowerEqualThanNode)
    def visit(self, node: ast.LowerEqualThanNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        local_dest = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, local_dest, CILLowerEqualThanNode(left, right))
        node.holder = local_dest

    @visitor.when(ast.EqualThanNode)
    def visit(self, node: ast.EqualThanNode,scope:CILScope):
        self.visit(node.left_expression,scope)
        self.visit(node.right_expression,scope)

        left = node.left_expression.holder
        # if type(node.left_expression.holder) is cil.CILLocalNode:
        #     left = node.left_expression.holder

        right = node.right_expression.holder
        # if type(node.right_expression.holder) is cil.CILLocalNode:
        #     right = node.right_expression.holder

        self.define_internal_local()
        local_dest = self.dotcode[-1].functions[-1].localvars[-1]
        if node.left_expression.computed_type.name == "String" and node.right_expression.computed_type.name == "String":
            self.register_instruction(CILAssignNode, local_dest, CILEqualStrThanStr(left, right))
        else:
            self.register_instruction(CILAssignNode, local_dest, CILEqualThanNode(left, right))
        node.holder = local_dest

    @visitor.when(ast.ObjectNode)
    def visit(self, node: ast.ObjectNode, scope:CILScope):
        if node.id in self.current_type_attrs:
            local_dest = self.define_internal_local()
            self.register_instruction(CILAssignNode, local_dest, CILGetAttributeNode(node.id))
            node.holder = local_dest
            return

        # name = f'{self.internal_count}_{self.current_function_name}_user_defined_{node.id}'
        name = scope.get_variable_alias(node.id) if scope.is_defined(node.id) else None
        params = self.dotcode[-1].functions[-1].params
        if name is None:
            for x in params:
                if x.endswith(node.id):
                    name = x
                    break
        node.holder = name

    @visitor.when(ast.IsVoidNode)
    def visit(self, node:ast.IsVoidNode,scope:CILScope):
        self.visit(node.expression,scope)
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILIsVoidNode(node.holder))
        node.holder = holder

    @visitor.when(ast.BlockNode)
    def visit(self, node: ast.BlockNode,scope:CILScope):
        for exp in node.expressions:
            self.visit(exp,scope)
        node.holder = node.expressions[-1].holder

    @visitor.when(ast.IntegerComplementNode)
    def visit(self, node: ast.IntegerComplementNode, scope: CILScope):
        self.visit(node.expression, scope)
        holder = self.define_internal_local()
        node.holder = holder
        self.register_instruction(CILAssignNode, holder, CILIntegerComplementNode(node.expression.holder))

    @visitor.when(ast.IntNode)
    def visit(self, node:ast.IntNode,scope:CILScope):
        node.holder = node.value

    @visitor.when(ast.StrNode)
    def visit(self, node:ast.StrNode,scope:CILScope):
        local = ""
        for x in self.dotdata.data:
            if node.value == x.value:
                local = x.vname

        self.define_internal_local()
        load = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, load, CILLoadNode(local))
        node.holder = load
    
    @visitor.when(ast.BoolNode)
    def visit(self, node: ast.BoolNode,scope:CILScope):
        if node.value == 'true':
            node.holder = 1
        else:
            node.holder = 0
    # ======================================================================