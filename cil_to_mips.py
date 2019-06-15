import visitor
import cil_hierarchy
from mips_utils import *
from built_in import add_builtin_mips_functions


class CollectMipsVtablesVisitor:
    def __init__(self):
        self.output = []
        self.types_nodes = []

    def emit(self, msg):
        self.output.append(msg + '\n')

    def blank(self):
        self.output.append('')

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil_hierarchy.CILProgramNode)
    def visit(self, node: cil_hierarchy.CILProgramNode):
        self.emit('__vtables: \n')

        cil_context = MipsTypeContext()
        cil_context.add_nodes(node.dottypes)
        cil_context.define_nodes_parent()
        cil_context.update_methods_inheritence()

        for node_type in node.dottypes:
            self.emit('')
            self.visit(node_type)

    # Vtable definition example
    # __vtable_X:
    # .word (cnt_methods)
    # #method1
    # .word (puntero al nombre del metodo)
    # .word (puntero al metodo)

    @visitor.when(cil_hierarchy.CILTypeNode)
    def visit(self, node: cil_hierarchy.CILTypeNode):
        i = len(self.output) - 1
        self.emit(f'__vtable_{node.name}: ')
        self.emit(f'.word {len(node.methods)}')

        for method_name in node.methods:
            method_real_name = method_name.split('_', maxsplit=1)[1]
            label_method_name = f'label_method_name_{node.name}_{method_real_name}'
            self.output.insert(i, f'\n{label_method_name}: \n')
            self.output.insert(i+1, f'.asciiz "{method_real_name}"\n')
            self.emit('# method')
            self.emit(f'.word {label_method_name}')
            self.emit(f'.word {method_name}')


class CollectMipsTypesDefinitionsVisitor:
    def __init__(self):
        self.output = []
        self.types_nodes = []

    def emit(self, msg):
        self.output.append(msg + '\n')

    def blank(self):
        self.output.append('')

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil_hierarchy.CILProgramNode)
    def visit(self, node: cil_hierarchy.CILProgramNode):
        self.emit('__types_definitions: ')

        cil_context = MipsTypeContext()
        cil_context.add_nodes(node.dottypes)
        cil_context.define_nodes_parent()

        for node_type in node.dottypes:
            self.emit('')
            self.visit(node_type)

    # Type definition example
    # type_X:
    # .word (tamaño de definicion)
    # .word (parent pointer)
    # .word (pointer typeName)
    # .word (tamaño a reservar por cada instancia)
    # .word type_X(direccion del mismo tipo)
    # .word __vtable_{node.name}
    # .word (cantidad de attrs)
    # # attr1
    # .word (attr1name pointer)
    # .space 4(value)

    @visitor.when(cil_hierarchy.CILTypeNode)
    def visit(self, node: cil_hierarchy.CILTypeNode):
        label_str_class_name = f'label_class_name_{node.name}'
        self.emit(f'\n{label_str_class_name}:')
        self.emit(f'.asciiz "{node.name}"')
        self.emit(f'type_{node.name}:')
        i = len(self.output) - 1
        type_space_in_bytes = 28 + len(node.attributes)*8
        # type space
        self.emit('# espacio de definicion del tipo')
        self.emit(f'.word {type_space_in_bytes}')
        # parent pointer
        self.emit('# puntero al padre en la jerarquia')
        if node.parent_name == 'None':
            self.emit(f'.word __void')
        else:
            self.emit(f'.word type_{node.parent_name}')
        # type Name
        self.emit('# puntero nombre de la clase')
        self.emit(f'.word {label_str_class_name}')
        # instance space
        self.emit('# espacio que ocupa una instancia de esta clase')
        self.emit(f'.word {type_space_in_bytes - 16}')
        # type pointer
        self.emit('# puntero a la misma clase')
        self.emit(f'.word type_{node.name}')
        # vtableDirection pointer
        self.emit('# direccion de la vtable de la clase')
        self.emit(f'.word __vtable_{node.name}')
        # cnt attrs
        self.emit('# cantidad de atributos')
        self.emit(f'.word {len(node.attributes)}')

        for attr in node.attributes:
            label_attr_name = f'label_attr_name_{node.name}_{attr}'
            self.output.insert(i, f'\n{label_attr_name}:\n')
            self.output.insert(i+1, f'.asciiz "{attr}"\n')
            self.emit('# attr')
            # attr_name
            self.emit(f'.word {label_attr_name}')
            # value
            self.emit(f'.space 4')


class CILtoMIPSVisitor:
    def __init__(self):
        self.output = []
        self.currentfuncv = None
        self.current_type = None

    def set_mips_main(self):
        self.emit('main: ')
        self.visit(cil_hierarchy.CILBuiltInCallNode('Main_cil_attributes_initializer'))

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp, $sp')
        self.macro_push('$v0')
        self.emit('jal Main_main')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')
        self.emit('jr $ra')

    def get_mips_program_code(self):
        result = ''
        for text in self.output:
            result += text

        return result

    def emit(self, msg):
        self.output.append(msg + '\n')

    def blank(self):
        self.output.append('')
    
    def get_local_var_or_param_index(self, name):
        for i, v in enumerate(self.currentfuncv.params + self.currentfuncv.localvars):
            if name == v:
                return i + 1
        raise ValueError
    
    def macro_push(self,reg):
        self.emit('subu $sp, $sp, 4')
        self.emit(f'sw {reg}, 0($sp)')
    
    def macro_pop(self,reg):
        self.emit(f'lw {reg}, 0($sp)')
        self.emit('addu $sp, $sp, 4')

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil_hierarchy.CILProgramNode)
    def visit(self, node: cil_hierarchy.CILProgramNode):
        self.emit('.data')
        self.emit('ior_msg_error: .asciiz "RuntimeError: Index out of range Error"')
        self.emit('__void: .byte 0')
        self.emit('std_in_data: .space 100')
        self.visit(node.dotdata)
        type_definition_creator = CollectMipsTypesDefinitionsVisitor()
        type_definition_creator.visit(node)
        # add types definitions
        self.output += type_definition_creator.output

        vtable_creator = CollectMipsVtablesVisitor()
        vtable_creator.visit(node)

        # add vtables definitions
        self.output += vtable_creator.output

        self.emit('.text')
        for i in range(len(node.dottypes)):
            self.current_type = node.dottypes[i]
            self.visit(node.dotcode[i])

        for i in node.static_functions:
            self.visit(i)

        add_builtin_mips_functions(self.output)
        self.add_compare_strings_funct()
        self.add_resolve_name_function()
        self.set_mips_main()

    @visitor.when(cil_hierarchy.CILAllocateNode)
    def visit(self, node: cil_hierarchy.CILAllocateNode):
        '''
        el nodo contiene la propiedad type_id que contiene el nombre del tipo de la instancia que se quiere crear.
        Lo que hay que hacer es ir a la direccion de memoria del tipo, leer un byte a partir del 4to byte, reservar la
        cantidad de bytes que dice ese valor, y copiar byte a byte de una direccion de memoria a otra.
        :param node:
        :return:
        '''
        self.emit(f'la $t0, type_{node.type_id}')
        self.emit('addu $t0, $t0, 12')
        # cargamos en $t1 el tamaño de la instancia
        self.emit('xor $t1, $t1, $t1')
        self.emit('lw $t1, 0($t0)')

        # ponemos en $t0 el lugar a partir del cual se debe copiar
        # para crear una instancia
        self.emit('addu $t0, $t0, 4')
        self.emit('li $v0, 9')
        self.emit('move $a0, $t1')
        self.emit('syscall')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp,$sp')

        self.macro_push('$v0')
        self.macro_push('$t0')
        self.macro_push('$t1')

        self.emit('jal __copy_byte_by_byte')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILCopyNode)
    def visit(self, node: cil_hierarchy.CILCopyNode):
        local_var_index = self.get_local_var_or_param_index(node.localv)
        # guardamos en $a0 el puntero al objeto que se quiere copiar
        self.emit(f'lw $a0, {-4*local_var_index}($fp)')
        # accedemos al tipo
        self.emit('lw $a1, 0($a0)')


        # nos movemos hasta el campo que contiene el tamaño de cada instancia
        self.emit('addu $a1, $a1, 12')
        self.emit('xor $t0,$t0,$t0')
        # guardamos en $t0 la cantidad que hay que reservar para crear una instancia del tipo deseado
        self.emit('lw $t0, 0($a1)')

        self.emit('li $v0, 9')
        self.emit('move $a0, $t0')
        self.emit('syscall')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp, $sp')

        # pasamos el puntero del nuevo objeto como primer parametro
        self.macro_push('$v0')
        self.emit('addu $a1, $a1, 4')
        self.macro_push('$a1')
        self.macro_push('$t0')
        self.emit('jal __copy_byte_by_byte')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILArrayNode)
    def visit(self, node: cil_hierarchy.CILArrayNode):
        self.emit('li $v0, 9')
        self.emit(f'li $a0, {4*node.size}')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILAssignNode)
    def visit(self, node: cil_hierarchy.CILAssignNode):
        if type(node.source) is int:
            self.emit(f'li $v0, {node.source}')
        else:
            try:
                local_index = self.get_local_var_or_param_index(node.source)
                self.emit(f'lw $v0, {-4*local_index}($fp)')
            except ValueError:
                if node.source == 'void':
                    self.emit('la $v0, __void')
                elif node.source == "":
                    self.emit(''' li $v0, 9
                                  li $a0, 1
                                  syscall
                                  sb $0, 0($v0)
                             ''')
                else:
                    self.visit(node.source)
        v = self.get_local_var_or_param_index(node.dest)
        self.emit(f'sw $v0, {-4*v}($fp)')

    @visitor.when(cil_hierarchy.CILCodeNode)
    def visit(self, node: cil_hierarchy.CILCodeNode):
        for func in node.functions:
            self.visit(func)

    @visitor.when(cil_hierarchy.CILConcatNode)
    def visit(self, node: cil_hierarchy.CILConcatNode):
        self.macro_push('$ra')
        local_index = self.get_local_var_or_param_index(node.str1)
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        local_index = self.get_local_var_or_param_index(node.str2)
        self.emit(f'lw $a1, {-4*local_index}($fp)')
        self.emit('jal __concat_strings')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILDataNode)
    def visit(self, node: cil_hierarchy.CILDataNode):
        for data in node.data:
            self.visit(data)

    @visitor.when(cil_hierarchy.CILDataElementNode)
    def visit(self, node: cil_hierarchy.CILDataElementNode):
        name = node.value.replace('"','')
        self.emit(f'{node.vname}: .asciiz "{name}"\n')

    def save_string(self, name):
        # reservar el espacio del string, se guarda en $v0
        self.emit(f'li $v0, 9')
        self.emit(f'li $a0, {len(name)+1}')
        self.emit(f'syscall')

        for i, char in enumerate(name):
            self.emit(f"li $t1, '{char}'")
            self.emit(f'sb $t1, {i}($v0)')
        self.emit(f'sb $0, {len(name)}($v0)')

    def add_compare_strings_funct(self):
        '''
        Dado dos direcciones de memoria de strings, devuelve 1 si son iguales, 0 en otro caso.
        :return:
        '''

        self.emit('''
        __compare_strings:
        lw $s2, -4($fp)
        lw $s3, -8($fp)
        
        cmploop:
        lb $t2, ($s2)
        lb $t3, ($s3)
        bne $t2,$t3, cmpne

        beq $t2, $zero, cmpeq

        addi $s2, $s2, 1
        addi $s3, $s3, 1
        j cmploop

        cmpne:
        li $v0, 0
        jr $ra

        cmpeq:
        li $v0, 1
        jr $ra
        ''')

    def add_resolve_name_function(self):
        '''
        Este metodo resuelve dado una direccion de memoria de un string y de un vtable,
         devuelve el
        puntero donde se encuentra el puntero buscado con ese nombre
        Recibe como primer parametro la direccion del string con el cual
        se quiere comparar, y como segndo parametro, el array de los punteros
        que tiene como forma: [byte_1(cantidad de punteros),.., byte_i(longitud
        del nombre del puntero),(nombre del puntero),4bytes(puntero)]

        :return:
        '''
        self.emit('''
            __resolve_name:
            # guardamos en $a0 la direccion del string
            lw $a0, -4($fp)
            # guardamos en $a1 la direccion del vtable
            lw $a1, -8($fp)
            
            xor $t0,$t0,$t0
            # cargamos la longitud del array de punteros en $t0
            lw $t0, 0($a1)
            
            # t1 es el indice que se movera por el array
            li $t1, 0
            
            xor $v0, $v0, $v0
            add $a1,$a1,4
            
            analize_method_name:
            xor $t2,$t2,$t2
            # nos paramos sobre el nombre del metodo
            move $t2, $a1
            lw $t2, 0($t2)
            
        ''')
        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp, $sp')
        self.macro_push('$a0')
        self.macro_push('$t2')
        self.emit('jal __compare_strings')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')
        self.emit('''
            bnez $v0, founded_method
            
            move_next:
            
            # nos movemos al proximo metodo
            addu $a1, $a1, 8 
            addu $t1,$t1,1
            bge $t1, $t0, end__resolve_name
            j analize_method_name
            
            end__resolve_name:
            li $v0, 0
            jr $ra
            
            founded_method:
            move $t3, $a1
            addu $v0, $t3, 4
            jr $ra
            
        ''')

        # instance_x
        # .word (type pointer)
        # .word (vtable pointer)
        # .word (cntattrs)
        #   .word (attr1Name pointer)
        #   .word value
        #  ...

    @visitor.when(cil_hierarchy.CILBuiltInCallNode)
    def visit(self, node: cil_hierarchy.CILBuiltInCallNode):

        self.macro_push('$ra')
        self.macro_push('$fp')

        self.emit('move $t0, $fp')
        self.emit('move $fp, $sp')

        # pasamos los parametros del metodo
        for param in node.params:
            param_index = self.get_local_var_or_param_index(param)
            self.emit(f'lw $a0, {-4*param_index}($t0)')
            self.macro_push('$a0')

        self.emit(f'jal {node.fid}')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILDynamicCallNode)
    def visit(self, node: cil_hierarchy.CILDynamicCallNode):
        # load instance pointer
        instance_index = self.get_local_var_or_param_index(node.instance)
        # cargamos en $t1 el puntero a la instancia
        self.emit(f'lw $t1, {-4*instance_index}($fp)')
        self.emit('addu $t1,$t1,4')
        # cargamos la tabla de metodos virtuales
        self.emit(f'lw $t1, 0($t1)')
        self.emit('move $t3, $t1')
        # resolve method address
        # ponemos en $v0 la direccion del string
        self.save_string(node.fid)
        # call find_method_address function
        self.macro_push('$ra')
        self.macro_push('$fp')
        # seteamos el frame del metodo que vamos a pasar
        self.emit('move $fp, $sp')
        # pasamos los parametros a la funcion
        self.macro_push('$v0')
        self.macro_push('$t3')
        # saltar a la funcion que busca el puntero al metodo correcto
        self.emit('jal __resolve_name')
        # guardamos en $v0 el puntero al metodo correcto
        self.emit('lw $v0, 0($v0)')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit(f'move $t0, $fp')
        self.emit(f'move $fp, $sp')
        # pasamos los parametros del metodo
        for param in node.params:
            param_index = self.get_local_var_or_param_index(param)
            self.emit(f'lw $a0, {-4*param_index}($t0)')
            self.macro_push('$a0')

        # llamamos al metodo
        self.emit(f'jalr $v0')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILStaticCallNode)
    def visit(self, node: cil_hierarchy.CILStaticCallNode):
        # resolve method address
        # call find_method_address function
        self.macro_push('$ra')
        self.macro_push('$fp')
        # ponemos en $v0 la direccion del string
        self.save_string(node.fid)
        # seteamos el frame del metodo que vamos a pasar
        self.emit('move $fp, $sp')

        # guardamos en $t1 la direccion de memoria de la vtable del tipo definido por el nodo
        self.emit(f'lw $t1, type_{node.parent_type} + 20')

        # pasamos los parametros a la funcion
        self.macro_push('$v0')
        self.macro_push('$t1')
        # saltar a la funcion que busca el puntero al metodo correcto
        self.emit('jal __resolve_name')
        # guardamos en $v0 el puntero al metodo correcto
        self.emit('lw $v0, 0($v0)')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')
        # ya tenemos en $v0 el metodo correcto!.

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit(f'move $t0, $fp')
        self.emit(f'move $fp, $sp')
        # pasamos los parametros del metodo
        for param in node.params:
            param_index = self.get_local_var_or_param_index(param)
            self.emit(f'lw $a0, {-4*param_index}($t0)')
            self.macro_push('$a0')
        # llamamos al metodo
        self.emit(f'jalr $v0')

        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILDivNode)
    def visit(self, node: cil_hierarchy.CILDivNode):
        l = node.left
        r = node.right                                                                                                                                                                                                                                                                                                                                                                                                                  
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {-4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t1, {-4*(v)}($fp)')
        
        self.emit(f'div $t3, $t0, $t1')
        self.emit('move $v0, $t3')

    @visitor.when(cil_hierarchy.CILErrorMessageNode)
    def visit(self, node: cil_hierarchy.CILErrorMessageNode):
        self.emit(f'la $a0, {node.msg}')
        self.emit('li $v0, 4')
        self.emit('syscall')
        self.emit('li $v0, 10')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILFunctionNode)
    def visit(self,node: cil_hierarchy.CILFunctionNode):
        self.currentfuncv = node
        self.emit(f'{node.fname}:')
        for _ in node.localvars:
            self.emit('subu $sp, $sp, 4')
        for inst in node.instructions:
            self.visit(inst)

    @visitor.when(cil_hierarchy.CILGetAttributeNode)
    def visit(self, node: cil_hierarchy.CILGetAttributeNode):
        self._find_attr(node)
        # guardamos en $v0 el valor del attr
        self.emit('lw $v0, 0($v0)')

    @visitor.when(cil_hierarchy.CILGetIndexNode)
    def visit(self, node: cil_hierarchy.CILGetIndexNode):
        arr = self.get_local_var_or_param_index(node.localv)
        self.emit(f'lw $t0, {-4*arr}($fp)')

        if type(node.index) == int:
            self.emit(f'li $t1, {node.index}')
        else:
            index = self.get_local_var_or_param_index(node.index)
            self.emit(f'lw $t1, {-4*index}($fp)')

        self.emit(f'mul $t1,$t1, 4')
        self.emit('add $t0, $t0, $t1')
        self.emit(f'lw $v0, 0($t0)')

    @visitor.when(cil_hierarchy.CILGetParentNode)
    def visit(self, node: cil_hierarchy.CILGetParentNode):
        localv_index = self.get_local_var_or_param_index(node.parentLabel)
        # cargamos el puntero al tipo
        self.emit(f'lw $a0, {-4*localv_index}($fp)')
        self.emit('lw $v0, 4($a0)')

    @visitor.when(cil_hierarchy.CILIntegerComplementNode)
    def visit(self, node: cil_hierarchy.CILIntegerComplementNode):
        try:
            v = self.get_local_var_or_param_index(node.complement)
            self.emit(f'lw, $t0, {-4*v}($fp)')
        except ValueError:
            self.emit(f'li $t0, {node.complement}')
        self.emit('neg $t0,$t0')
        self.emit('addu $v0,$t0,1')

    @visitor.when(cil_hierarchy.CILIsVoidNode)
    def visit(self, node: cil_hierarchy.CILIsVoidNode):
        try:
            v = self.get_local_var_or_param_index(node.is_void)
            self.emit(f'lw, $t0, {-4*v}($fp)')
        except ValueError:
            self.emit('seq $v0, $t0, 0')

        self.emit('la $t1, __void')
        self.emit('seq $v0, $t0, $t1')

    @visitor.when(cil_hierarchy.CILLabelNode)
    def visit(self, node: cil_hierarchy.CILLabelNode):
        self.emit(f'{node.label}:')

    @visitor.when(cil_hierarchy.CILLengthNode)
    def visit(self,node:cil_hierarchy.CILLengthNode):
        self.macro_push('$ra')
        local_index = self.get_local_var_or_param_index(node.localv)
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        self.emit('jal __get_str_len')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILLoadNode)
    def visit(self,node:cil_hierarchy.CILLoadNode):
        self.emit(f'la $v0, {node.msg}')

    @visitor.when(cil_hierarchy.CILMinusNode)
    def visit(self, node: cil_hierarchy.CILMinusNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {-4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t1, {-4*(v)}($fp)')
        
        self.emit('sub $v0, $t0, $t1')

    @visitor.when(cil_hierarchy.CILPlusNode)
    def visit(self, node: cil_hierarchy.CILPlusNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {-4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t1, {-4*(v)}($fp)')

        self.emit(f'add $t2, $t0, $t1')
        self.emit('move $v0, $t2')

    @visitor.when(cil_hierarchy.CILPrefixNode)
    def visit(self, node: cil_hierarchy.CILPrefixNode):
        self.macro_push('$ra')
        local_index = self.get_local_var_or_param_index(node.sub_string)
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        local_index = self.get_local_var_or_param_index(node.full_string)
        self.emit(f'lw $a1, {-4*local_index}($fp)')
        self.emit('jal __get_if_its_prefix')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILPrintStringNode)
    def visit(self, node: cil_hierarchy.CILPrintStringNode):
        try:
            v = self.get_local_var_or_param_index(node.str_addr)
            self.emit(f'lw $a0, {-4*v}($fp)')
        except ValueError:
            # esto no deberia ocurrir
            self.emit(f'la $a0, {node.str_addr}')
        self.emit('li $v0, 4')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILPrintIntNode)
    def visit(self, node: cil_hierarchy.CILPrintIntNode):
        try:
            v = self.get_local_var_or_param_index(node.int_addr)
            self.emit(f'lw $t0, {-4*v}($fp)')
        except ValueError:
            self.emit(f'li $t0, {node.int_addr}')
        self.emit('move $a0, $t0')
        self.emit('li $v0, 1')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILReadStringNode)
    def visit(self, node:cil_hierarchy.CILReadStringNode):
        self.emit('li $v0, 8')
        self.emit('la $a0, std_in_data')
        self.emit('la $a1, 100')
        self.emit('syscall')
    
    @visitor.when(cil_hierarchy.CILReadIntNode)
    def visit(self, node:cil_hierarchy.CILReadIntNode):
        self.emit('li $v0, 5')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILReturnNode)
    def visit(self,node: cil_hierarchy.CILReturnNode):
        '''
        Carga lo que está en la direccion de memoria que le pasan a return
        y lo escribe en $v0
        :param node:
        :return:
        '''
        if node.value is not None:
            if node.value in self.current_type.attributes:
                a = cil_hierarchy.CILGetAttributeNode(node.value)
                self._find_attr(a)
                self.emit(f'lw $v0, 0($v0)')
                self.emit('jr $ra')
                return
            try:
                local_index = self.get_local_var_or_param_index(node.value)
                self.emit(f'lw $v0, {-4*local_index}($fp)')
            except ValueError:
                self.emit(f'li $v0, {node.value}')
        self.emit('jr $ra')

    def _find_attr(self, node):
        # load instance pointer
        instance_index = self.get_local_var_or_param_index(node.localv)
        # cargamos en $t1 el puntero a la instancia
        self.emit(f'lw $t1, {-4*instance_index}($fp)')
        self.emit('addu $t1, $t1, 8')
        # la direccion donde se encuentra la cnt attrs se guarda en $t3
        self.emit(f'move $t3, $t1')
        # resolve attr address
        # call find_attr_address function
        self.macro_push('$ra')
        self.macro_push('$fp')
        # ponemos en $v0 la direccion del string
        self.save_string(node.attrName)
        # seteamos el frame del metodo que vamos a pasar
        self.emit('move $fp, $sp')
        # pasamos los parametros a la funcion
        self.macro_push('$v0')
        self.macro_push('$t3')
        # saltar a la funcion que busca el puntero al attr correcto
        self.emit('jal __resolve_name')

        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')
    #     se tiene en $v0 la direccion donde se encuentra el valor del attr

    @visitor.when(cil_hierarchy.CILSetAttributeNode)
    def visit(self, node: cil_hierarchy.CILSetAttributeNode):
        self._find_attr(node)
        # tenemos en $v0 la direccion donde se encuentra el valor del attr

        try:
            local_ = self.get_local_var_or_param_index(node.value)
            self.emit(f'lw $t0, {-4*local_}($fp)')
        except ValueError:
            if node.value == "":
                self.emit('''
                    li $v0, 9
                    li $a0, 1
                    syscall
                    sb $0, 0($v0)
                    move $t0, $v0
                ''')
            elif node.value == 'void':
                self.emit('la $t0, __void')
            else:
                self.emit(f'li $t0, {node.value}')
        self.emit('sw $t0, 0($v0)')

    @visitor.when(cil_hierarchy.CILSetIndexNode)
    def visit(self,node: cil_hierarchy.CILSetIndexNode):
        # se asume q los valores que se pasan son labels
        local_index = self.get_local_var_or_param_index(node.localv)
        self.emit(f'lw $t0, {-4*local_index}($fp)')
        if type(node.index) is int:
            self.emit(f'li $t1, {node.index}')
        else:
            local_index = self.get_local_var_or_param_index(node.index)
            self.emit(f'lw $t1, {-4*local_index}($fp)')
        self.emit('mul $t1, $t1, 4')
        self.emit(f'addu $t0, $t0, $t1')

        self.emit(f'la $t1, {node.value}')
        self.emit(f'sw $t1, 0($t0)')

    @visitor.when(cil_hierarchy.CILStarNode)
    def visit(self, node: cil_hierarchy.CILStarNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {-4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t1, {-4*(v)}($fp)')
        
        self.emit(f'mul $t3, $t0, $t1')
        self.emit('move $v0, $t3')

    @visitor.when(cil_hierarchy.CILSubstringNode)
    def visit(self, node: cil_hierarchy.CILSubstringNode):

        self.macro_push('$ra')
        local_index = self.get_local_var_or_param_index(node.str1)
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        if type(node.index) is int:
            self.emit(f'li $a1, {node.index}')
        else:
            local_index = self.get_local_var_or_param_index(node.index)
            self.emit(f'lw $a1, {-4*local_index}($fp)')

        if type(node.length) is int:
            self.emit(f'li $a2, {node.length}')
        else:
            local_index = self.get_local_var_or_param_index(node.length)
            self.emit(f'lw $a2, {-4*local_index}($fp)')

        self.emit('jal __get_substring')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILTypeNameNode)
    def visit(self, node: cil_hierarchy.CILTypeNameNode):
        local_index = self.get_local_var_or_param_index(node.type_to_get)
        # cargamos la direccion de la instancia
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        # cargamos la direccion del tipo
        self.emit('lw $a0, 0($a0)')
        self.emit('lw $v0, 8($a0)')

    @visitor.when(cil_hierarchy.CILLowerEqualThanNode)
    def visit(self, node: cil_hierarchy.CILLowerEqualThanNode):
        l = node.left_expr
        r = node.right_expr
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            try:
                v = self.get_local_var_or_param_index(l)
                self.emit(f'lw $t0, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t0, {node.left_expr}')

        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')

        elif type(r) == str:
            try:
                v = self.get_local_var_or_param_index(r)
                self.emit(f'lw $t1, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t1, {node.left_expr}')
        self.emit('sle $v0, $t0, $t1')

    @visitor.when(cil_hierarchy.CILEqualThanNode)
    def visit(self, node: cil_hierarchy.CILEqualThanNode):
        l = node.left_expr
        r = node.right_expr
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            try:
                v = self.get_local_var_or_param_index(l)
                self.emit(f'lw $t0, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t0, {node.left_expr}')

        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')

        elif type(r) == str:
            try:
                v = self.get_local_var_or_param_index(r)
                self.emit(f'lw $t1, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t1, type_{node.right_expr}')
        self.emit('seq $v0, $t0, $t1')

    @visitor.when(cil_hierarchy.CILEqualStrThanStr)
    def visit(self, node: cil_hierarchy.CILEqualStrThanStr):
        l = node.left_expr
        r = node.right_expr
        # if type(l) == int or type(l) == float:
        #     self.emit(f'li $t0, {l}')
        if type(l) == str:
            try:
                v = self.get_local_var_or_param_index(l)
                self.emit(f'lw $a0, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $a0, {node.left_expr}')

        if type(r) == str:
            try:
                v = self.get_local_var_or_param_index(r)
                self.emit(f'lw $a1, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $a1, {node.right_expr}')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp, $sp')
        self.macro_push('$a0')
        self.macro_push('$a1')
        self.emit('jal __compare_strings')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILLowerThanNode)
    def visit(self, node: cil_hierarchy.CILLowerThanNode):
        l = node.left_expr
        r = node.right_expr
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            try:
                v = self.get_local_var_or_param_index(l)
                self.emit(f'lw $t0, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t0, {node.left_expr}')

        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')

        elif type(r) == str:
            try:
                v = self.get_local_var_or_param_index(r)
                self.emit(f'lw $t1, {-4*(v)}($fp)')
            except ValueError:
                self.emit(f'la $t1, type_{node.right_expr}')
        self.emit('slt $v0, $t0, $t1')

    @visitor.when(cil_hierarchy.CILTypeOfNode)
    def visit(self, node: cil_hierarchy.CILTypeOfNode):
        local_index = self.get_local_var_or_param_index(node.source)
        # cargamos la direccion de la instancia
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        # cargamos la direccion del tipo
        self.emit('lw $v0, 0($a0)')

    @visitor.when(cil_hierarchy.CILGotoIfNode)
    def visit(self, node: cil_hierarchy.CILGotoIfNode):

        if type(node.compare) is int:
            self.emit(f'li $t0, {node.compare}')
        else:
            v = self.get_local_var_or_param_index(node.compare)
            self.emit(f'lw $t0,{-4*v}($fp)')
        self.emit(f'bnez $t0, {node.label}')

    @visitor.when(cil_hierarchy.CILGotoNode)
    def visit(self, node: cil_hierarchy.CILGotoNode):
        try:
            local = self.get_local_var_or_param_index(node.label)
            self.emit(f'lw $t0, {-4*local}($fp)')
            self.emit('jr $t0')
        except ValueError:
            self.emit(f'b {node.label}')

            # @visitor.when(cil_hierarchy.CILNegationNode)
    # def visit(self, node: cil_hierarchy.CILNegationNode):
    #     if type(node.localv) == int or type(node.localv) == float:
    #         self.emit(f'li $t0, {node.localv}')
    #     else:
    #         v = self.get_local_var_or_param_index(node.localv)
    #         self.emit(f'lw $t0, {-4*(v)}($fp)')
    #     self.emit(f'neg $t1, $t0')
    #     self.emit(f'move $v0, $t1')