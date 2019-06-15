import NodosAST as ast
from cil_hierarchy import *
import visitor
from built_in import *
from static_functions import *
from strings_visitor import StringVisitor
from cil_writer import *
from cool_utils import value_bultin_types


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
        self.data_bultins_labels = {'Int':self.register_data('Int'),
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

    def define_ud_internal_local(self, vinfo):
        vinfo = self.build_user_defined_vname(vinfo)
        # local_node = CILLocalNode(vinfo)
        self.dotcode[-1].functions[-1].localvars.append(vinfo)
        return vinfo

    
    #jump help methods
    #devuelve el índice de la próxima instrucción
    def next_instruction_index(self):
        return len(self.dotcode[-1].functions[-1].instructions)

    def next_label(self):
        self.label_count += 1
        return "L"+str(self.label_count)

    # def add_parent_attr(self):
    #     parent = self.dottypes[-1].parent_name
    #     for x in self.dottypes:
    #         if x.name == parent:
    #             for attr in x.attributes:
    #                 if attr not in self.dottypes[-1].attributes:
    #                     self.dottypes[-1].attributes.append(attr)

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
    def visit(self, node: ast.ProgramNode):
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
            self.visit(program_class)
        
        result = CILProgramNode(self.dottypes, self.dotdata, self.dotcode, self.static_functions)
        writer = CILWriterVisitor()
        writer.visit(result)
        for x in writer.output:
            print(x)

        return result

    @visitor.when(ast.ClassNode)
    def visit(self, node: ast.ClassNode):
        self.dottypes.append(CILTypeNode(node.name, node.inherit))
        self.dotcode.append(CILCodeNode())

        self.current_type_attrs = set([n.id for n in node.attributes])

        constructor_method_name = f'{node.name}_cil_attributes_initializer'
        self.dottypes[-1].methods.append(constructor_method_name)
        self.current_function_name = constructor_method_name
        self.dotcode[-1].functions.append(CILFunctionNode(constructor_method_name))
        self.define_internal_local()
        index = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, index, CILAllocateNode(node.name))
        for attr in node.attributes:
            self.visit(attr)
            if attr.value is not None:
                self.visit(attr.value)
                self.register_instruction(CILSetAttributeNode, attr.id, index, attr.value.holder)
            else:
                if attr.type == "Int" or attr.type == "Bool":
                    self.register_instruction(CILSetAttributeNode, attr.id, index, 0)
                elif attr.type == "String":
                    self.register_instruction(CILSetAttributeNode, attr.id, index, '__void')
                else:
                    self.register_instruction(CILSetAttributeNode, attr.id, index, "")
        self.register_instruction(CILReturnNode, index)

        for method in node.methods:
            self.visit(method)
        
        # self.add_parent_attr()

    @visitor.when(ast.MethodNode)
    def visit(self, node: ast.MethodNode):
        name = f'{self.dottypes[-1].name}_{node.id}'
        self.current_function_name = name
        self.dottypes[-1].methods.append(name)
        self.dotcode[-1].functions.append(CILFunctionNode(name,["self"]))
        for x,_ in node.parameters:
            vinfo = self.build_user_defined_vname(x)
            self.dotcode[-1].functions[-1].params.append(vinfo)
            
        if type(node.expression) is ast.BlockNode:
            for expr in node.expression.expressions:
                self.visit(expr)
            self.register_instruction(CILReturnNode, node.expression.expressions[-1].holder)
            node.holder = node.expression.expressions[-1].holder
        else:
            self.visit(node.expression)
            self.register_instruction(CILReturnNode, node.expression.holder)
            node.holder = node.expression.holder

    @visitor.when(ast.AttributeNode)
    def visit(self, node:ast.AttributeNode):
        self.dottypes[-1].attributes.append(node.id)

    def make_boxing(self, variable, type_name, value):
        self.register_instruction(CILAssignNode, variable, CILAllocateNode(type_name))
        self.register_instruction(CILSetAttributeNode, 'attr_value', variable, value)

    def make_unboxing(self, variable, instance):
        self.register_instruction(CILAssignNode, variable, CILGetAttributeNode('attr_value', instance))

    @visitor.when(ast.AssignNode)
    def visit(self, node: ast.AssignNode):

        self.visit(node.expression)
        expression_type_name = node.expression.computed_type.name

        # si la asignacion es sobre un attr
        if node.variable.id in self.current_type_attrs:
            self.register_instruction(CILSetAttributeNode, node.variable.id,'self',node.expression.holder)
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
            self.define_ud_internal_local(node.variable)

        self.register_instruction(CILAssignNode, node.variable.id, node.expression.holder)
        node.holder = node.variable.id

    @visitor.when(ast.DispatchNode)
    def visit(self, node: ast.DispatchNode):
        self.visit(node.left_expression)
        left_expression = 'self'

        for exp in node.parameters:
            self.visit(exp)

        if node.left_expression is not None:
            left_expression = node.left_expression.holder
            left_expression_type_name = node.left_expression.computed_type.name

            # si es un tipo por valor la expresion izquierda, entonces hacemos boxing
            if left_expression_type_name == 'Int' or left_expression_type_name == 'Bool':
                vinfo = self.define_internal_local()
                self.make_boxing(vinfo, left_expression_type_name, left_expression)
                left_expression = vinfo

        # Se obtiene el tipo de la expresion izquierda
        # self.define_internal_local()
        if node.func_id == 'concat':
            my_call = CILBuiltInCallNode('String_concat')
        elif node.func_id == 'length':
            my_call = CILBuiltInCallNode('String_length')
        elif node.func_id == 'substr':
            my_call = CILBuiltInCallNode('String_substr')
        else:
            my_call = CILDynamicCallNode(node.func_id, left_expression)
        # aqui se ponen los params
        my_call.params.append(left_expression)
        for exp in node.parameters:
            my_call.params.append(exp.holder)

        # Llamado a la funcion
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, my_call)
        node.holder = holder

    @visitor.when(ast.StaticDispatchNode)
    def visit(self, node: ast.StaticDispatchNode):
        self.visit(node.left_expression)
        for x in node.parameters:
            self.visit(x)

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
    def visit(self, node: ast.ConditionalNode):
        self.visit(node.if_expression)
        l_then = self.next_label()
        l_else = self.next_label()
        l_end = self.next_label()

        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILGotoIfNode,node.if_expression.holder, l_then)
        self.register_instruction(CILGotoNode, l_else)
        self.register_instruction(CILLabelNode, l_then)

        self.visit(node.then_expression)
        self.register_instruction(CILAssignNode, holder, node.then_expression.holder)
        
        self.register_instruction(CILGotoNode, l_end)
        self.register_instruction(CILLabelNode, l_else)

        self.visit(node.else_expression)
        self.register_instruction(CILAssignNode, holder, node.else_expression.holder)

        self.register_instruction(CILLabelNode, l_end)

        node.holder = holder

    @visitor.when(ast.LoopNode)
    def visit(self, node: ast.LoopNode):
        l_condition = self.next_label()
        l_loop = self.next_label()
        l_end = self.next_label()
        self.register_instruction(CILLabelNode, l_condition)
        self.visit(node.while_expression)
        self.register_instruction(CILGotoIfNode, node.while_expression.holder, l_loop)
        self.register_instruction(CILGotoNode, l_end)
        self.register_instruction(CILLabelNode, l_loop)
        self.visit(node.loop_expression)
        self.register_instruction(CILGotoNode, l_condition)
        self.register_instruction(CILLabelNode,l_end)
        
        node.holder = 0

    @visitor.when(ast.LetVarNode)
    def visit(self, node:ast.LetVarNode):
        for dec in node.declarations:
            if dec[1] is not None:
                self.visit(dec[1])
                self.define_ud_internal_local(dec[0][0])
                self.register_instruction(CILAssignNode,self.dotcode[-1].functions[-1].localvars[-1], dec[1].holder)
            else:
                self.define_ud_internal_local(dec[0][0])
                self.register_instruction(CILAssignNode,self.dotcode[-1].functions[-1].localvars[-1], 0)
        self.visit(node.in_expression)
        node.holder = node.in_expression.holder

    @visitor.when(ast.CaseNode)
    def visit(self, node: ast.CaseNode):
        # Se genera el codigo de la expresion inicial del case
        self.visit(node.case_expression)
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

        self.define_internal_local()
        arr = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, arr, CILArrayNode(len(node.implications)))
        for i in range(0, len(node.implications)):
            self.register_instruction(CILSetIndexNode, arr, i, 'type_'+node.implications[i][0][1])

        #Aqui se obtiene el tipo del resultado de evaluar la expresion inicial del case
        self.define_internal_local()
        expr0_type_name = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, expr0_type_name, CILTypeOfNode(expr0_value))

        #Se realiza un llamado a la funcion estatica "get_closest_type", cuyo retorno se le asigna a closest_type_index
        closest_type_index = self.define_internal_local()
        bcall = CILBuiltInCallNode("__get_closest_type")
        bcall.params = [expr0_type_name, arr]
        self.register_instruction(CILAssignNode, closest_type_index, bcall)

        #Se crea un array que contendra los labels de las expresiones a visitar
        array_labels = self.define_internal_local()
        self.register_instruction(CILAssignNode, array_labels, CILArrayNode(len(node.implications)))
        labels = []
        local_user_vars = []
        for i in range(len(node.implications)):
            l_next = self.next_label()
            user_local = self.define_ud_internal_local(node.implications[i][0][0])
            # temp_local = self.dotcode[-1].functions[-1].localvars[-1]
            local_user_vars.append(user_local)
            labels.append(l_next)
            self.register_instruction(CILSetIndexNode, array_labels, i, l_next)

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
                self.visit(node.implications[i][1])
                self.register_instruction(CILAssignNode, final_holder, node.implications[i][1].holder)
                self.register_instruction(CILGotoNode, end_case_label)
                continue
            self.register_instruction(CILAssignNode, local_user_vars[i], expr0_value)
            self.visit(node.implications[i][1])
            self.register_instruction(CILAssignNode, final_holder, node.implications[i][1].holder)
            self.register_instruction(CILGotoNode,end_case_label)
        self.register_instruction(CILLabelNode, end_case_label)
        node.holder = final_holder

    @visitor.when(ast.NewTypeNode)
    def visit(self, node: ast.NewTypeNode):
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        constructor_name = f'{node.type_name}_cil_attributes_initializer'
        self.register_instruction(CILAssignNode, holder, CILBuiltInCallNode(constructor_name))
        node.holder = holder

    @visitor.when(ast.PlusNode)
    def visit(self, node: ast.PlusNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.MinusNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.StarNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node:ast.DivNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.NegationNode):
        self.visit(node.expression)
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILMinusNode(0, node.expression.holder))

        node.holder = holder

    @visitor.when(ast.NotNode)
    def visit(self, node: ast.NotNode):
        self.visit(node.expression)
        self.define_internal_local()
        local_dest = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, local_dest, CILMinusNode(1,node.expression.holder))

        node.holder = local_dest

    @visitor.when(ast.LowerThanNode)
    def visit(self, node: ast.LowerThanNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.LowerEqualThanNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.EqualThanNode):
        self.visit(node.left_expression)
        self.visit(node.right_expression)

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
    def visit(self, node: ast.ObjectNode):
        if node.id in self.current_type_attrs:
            self.define_internal_local()
            local_dest = self.dotcode[-1].functions[-1].localvars[-1]
            self.register_instruction(CILAssignNode, local_dest, CILGetAttributeNode(node.id))
            node.holder = local_dest
            return

        name = f'{self.internal_count}_{self.current_function_name}_user_defined_{node.id}'
        for x in self.dotcode[-1].functions[-1].localvars + self.dotcode[-1].functions[-1].params:
            splitted = x.split("_")
            if splitted[-1] == node.id:
                name = x
        node.holder = name

    @visitor.when(ast.IsVoidNode)
    def visit(self, node:ast.IsVoidNode):
        self.visit(node.expression)
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILIsVoidNode(node.holder))
        node.holder = holder

    @visitor.when(ast.BlockNode)
    def visit(self, node:ast.BlockNode):
        for exp in node.expressions:
            self.visit(exp)
        node.holder = node.expressions[-1].holder

    @visitor.when(ast.IntegerComplementNode)
    def visit(self, node:ast.IntegerComplementNode):
        self.visit(node.expression)
        self.define_internal_local()
        holder = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, holder, CILIntegerComplementNode(node.holder))
        node.holder = holder

    @visitor.when(ast.IntNode)
    def visit(self, node:ast.IntNode):
        node.holder = node.value

    @visitor.when(ast.StrNode)
    def visit(self, node:ast.StrNode):
        local = ""
        for x in self.dotdata.data:
            if node.value == x.value:
                local = x.vname

        self.define_internal_local()
        load = self.dotcode[-1].functions[-1].localvars[-1]
        self.register_instruction(CILAssignNode, load, CILLoadNode(local))
        node.holder = load
    
    @visitor.when(ast.BoolNode)
    def visit(self, node: ast.BoolNode):
        if node.value == 'true':
            node.holder = 1
        else:
            node.holder = 0
    # ======================================================================