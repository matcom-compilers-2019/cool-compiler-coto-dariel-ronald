import visitor
import cil_hierarchy
from mips_utils import *


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
        self.emit('__vtables: ')

        cil_context = MipsTypeContext()
        cil_context.add_nodes(node.dottypes)
        cil_context.define_nodes_parent()
        cil_context.update_methods_inheritence()

        for node_type in node.dottypes:
            self.visit(node_type)

    # Vtable definition example
    # __vtable_X:
    # .byte (cnt_methods)
    # #method1
    # .byte (longitud del nombre del metodo)
    # .asciiz (nombre del metodo)
    # .word (puntero al metodo)

    @visitor.when(cil_hierarchy.CILTypeNode)
    def visit(self, node: cil_hierarchy.CILTypeNode):
        self.emit(f'__vtable_{node.name}: ')
        self.emit(f'.byte {len(node.methods)}')

        for method_name in node.methods:
            method_real_name = method_name.split('_', maxsplit=1)[1]
            self.emit(f'.asciiz "{method_real_name}"')
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
            self.visit(node_type)

    # Type definition example
    # type_X:
    # .word(tamaño de definicion)
    # .word(parent pointer)
    # .byte (nameLength)
    # .asciiz (typeName)
    # .byte(tamaño a reservar por cada instancia)
    # .word type_X(direccion del mismo tipo)
    # .word __vtable_{node.name}
    # .byte(cantidad de attrs)
    # # attr1
    # .byte(len attrname1)
    # .asciiz(name)
    # .space 4(value)

    @visitor.when(cil_hierarchy.CILTypeNode)
    def visit(self, node: cil_hierarchy.CILTypeNode):
        self.emit(f'type_{node.name}: ')
        type_space_in_bytes = sum([len(attr_name)for attr_name in node.attributes]) + len(node.attributes)*5 + 18
        # type space
        self.emit(f'.word {type_space_in_bytes}')
        # parent pointer
        self.emit(f'.word type_{node.parent_name}')
        # type Name length
        self.emit(f'.byte {len(node.name)}')
        # type Name
        self.emit(f'.asciiz "{node.name}"')
        # instance space
        self.emit(f'.byte {type_space_in_bytes - 5}')
        # type pointer
        self.emit(f'.word type_{node.name}')
        # vtableDirection pointer
        self.emit(f'.word __vtable_{node.name}')
        # cnt attrs
        self.emit(f'.byte {len(node.attributes)}')

        for attr in node.attributes:
            # length attr_name
            self.emit(f'.byte {len(attr)}')
            # attr_name
            self.emit(f'.asciiz "{attr}"')
            # value
            self.emit(f'.space 4')


class CILtoMIPSVisitor:
    def __init__(self):
        self.output = []
        self.currentfuncv = None
    
    def emit(self, msg):
        self.output.append(msg + '\n')

    def blank(self):
        self.output.append('')
    
    def get_local_var_or_param_index(self,name):
        for i,v in enumerate(self.currentfuncv.params + self.currentfuncv.localvars):
            if name == v.vinfo.name:
                return i
        raise ValueError
    
    def macro_push(self,reg):
        self.emit('subu $sp, $sp, 4')
        self.emit(f'sw {reg}, 0($sp)')
    
    def macro_pop(self,reg):
        self.emit(f'lw {reg} 0($sp)')
        self.emit('addu $sp, $sp, 4')

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(cil_hierarchy.CILProgramNode)
    def visit(self, node: cil_hierarchy.CILProgramNode):
        self.emit('.data')
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
            self.visit(node.dotcode[i])

    # @visitor.when(cil_hierarchy.CILAbortNode)
    # def visit(self,node: cil_hierarchy.CILAbortNode):
    #     self.emit(f'la $a0, {node}') #arreglar esto
    #     self.emit(f'li $v0, 4')
    #     self.emit('syscall')
    #     self.emit(f'li $v0, 10')
    #     self.emit(f'syscall')

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
        self.emit('addu $t0, $t0, 8')
        self.emit('li $t2, 0')
        self.emit('lb $t2, 0($t0)')
        self.emit('addu $t0,$t0,$t2')
        self.emit('addu $t0,$t0,1')
        # cargamos en $t1 el tamaño de la instancia
        self.emit('lb $t1, 0($t0)')

        # ponemos en $t0 el lugar a partir del cual se debe copiar
        # para crear una instancia
        self.emit('addu $t0, $t0, 1')
        self.emit('li $v0, 9')
        self.emit('mov $a0, $t1')
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

    def add_copy_byte_by_byte(self):
        '''
        Esta funcion recibe como primer parametro el lugar donde se va a copiar,
        como segundo de donde se va a copiar y
        como tercero cuantos bytes se vana copiar.
        :return:
        '''
        self.emit('''
        __copy_byte_by_byte:
        lw $a0, -4($fp)
        lw $a1, -8($fp)
        lw $a2, -12($fp)
        
        move $v0, $a0
        
        __while_copy:
        bnez $a2, __end_copy
        
        lb $t0, 0($a1)
        sb 0($a0), $t0
        
        subu $a2, $a2,1
        addu $a0, $a0,1
        addu $a1, $a1,1
        j __while_copy
        
        __end_copy:
        jr $ra
        ''')

    @visitor.when(cil_hierarchy.CILCopyNode)
    def visit(self, node: cil_hierarchy.CILCopyNode):
        local_var_index = self.get_local_var_or_param_index(node.type_to_copy)
        # guardamos en $a0 el puntero al objeto que se quiere copiar
        self.emit(f'lw $a0, {-4*local_var_index}($fp)')
        # accedemos al tipo
        self.emit('lw $a1, 0($a0)')
        # guardamos en $t3 el tamaño del nombre
        self.emit('li $t3, 0')
        self.emit('lb $t3, 8($a1)')
        self.emit('addu $t3, $t3, 9')

        # nos movemos hasta el campo que contiene el tamaño de cada instancia
        self.emit('addu $a1, $a1, $t3')
        self.emit('li $t0, 0')
        # guardamos en $t0 la cantidad que hay que reservar para crear una instancia del tipo deseado
        self.emit('lb $t0, 0($a1)')

        self.emit('li $v0, 9')
        self.emit('move $a0, $t0')
        self.emit('syscall')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit('move $fp, $sp')

        # pasamos el puntero del nuevo objeto como primer parametro
        self.macro_push('$v0')
        self.macro_push('$a0')
        self.macro_push('$t0')
        self.emit('jal __copy_byte_by_byte')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILArrayNode)
    def visit(self,node: cil_hierarchy.CILArrayNode):
        self.emit('li $v0, 9')
        self.emit(f'li $a0, {node.size}')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILAssignNode)
    def visit(self, node: cil_hierarchy.CILAssignNode):
        self.visit(node.source)
        v = self.get_local_var_or_param_index(node.dest)
        self.emit(f'sw, $v0, {4*v}($fp)')

    @visitor.when(cil_hierarchy.CILCodeNode)
    def visit(self,node:cil_hierarchy.CILCodeNode):
        for func in node.functions:
            self.visit(func)

    @visitor.when(cil_hierarchy.CILConcatNode)
    def visit(self,node:cil_hierarchy.CILConcatNode):
        pass

    @visitor.when(cil_hierarchy.CILDataNode)
    def visit(self, node: cil_hierarchy.CILDataNode):
        for data in node.data:
            self.visit(data)

    @visitor.when(cil_hierarchy.CILDataElementNode)
    def visit(self, node: cil_hierarchy.CILDataElementNode):
        self.emit(f'{node.vname}: .asciiz "{node.value}\n"')

    def save_string(self, name):
        # reservar el espacio del string, se guarda en $v0
        self.emit(f'li $v0, 9')
        self.emit(f'li $a0, {len(name)+1}')
        self.emit(f'syscall')

        for i,char in enumerate(name):
            self.emit(f'li $t1, {char}')
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
        puntero donde se encuentra el metodo correcto a llamar.
        :return:
        '''
        self.emit('''
            __resolve_name:
            # guardamos en $a0 la direccion del string
            lw $a0, -4($fp)
            # guardamos en $a1 la direccion del vtable
            lw $a1, -8($fp)
            
            # cargamos la longitud del array de metodos en $t0
            lb $t0, 0($a1)
            
            # t1 es el indice que se movera por el array
            li $t1, 0
            
            addu $a1, $a1, 1
            
            analize_method_name:
            li $t2, 0
            # nos paramos sobre el nombre del metodo
            addu $t2, $a1, 1
            
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
            
            # guardamos en $t3 la longitud del nombre del metodo
            lb $t3, 0($a0)
            addu $t3, $t3, 5
            # nos movemos al proximo metodo
            addu $a1, $a1, $t3 
            addu $t1,$t1,1
            bge $t1, $t0, end__resolve_name
            j analize_method_name
            
            end__resolve_name:
            li $v0, 0
            jr $ra
            
            founded_method:
            lb $t3, 0($a0)
            addu $t3, $t3, 1
            lw $v0, 0($t3)
            
        ''')

        # instance_x
        # .word (type pointer)
        # .word (vtable pointer)
        # .byte (cntattrs)
        #   .byte (attr1Namelen)
        #   .asciiz Name
        #   .word value
        #  ...

    @visitor.when(cil_hierarchy.CILBuiltinCallNode)
    def visit(self, node: cil_hierarchy.CILBuiltinCallNode):

        self.macro_push('$ra')
        self.macro_push('$fp')

        self.emit('move $fp, $sp')

        # pasamos los parametros del metodo
        for param in node.params:
            param_index = self.get_local_var_or_param_index(param)
            self.emit(f'lw $a0, {4*param_index}($t0)')
            self.macro_push('$a0')

        self.emit(f'jal {node.fid}')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILStaticCallNode)
    def visit(self, node: cil_hierarchy.CILStaticCallNode):
        # load instance pointer
        instance_index = self.get_local_var_or_param_index(node.localv)
        # cargamos en $t1 el puntero a la instancia
        self.emit(f'lw $t1, {-4*instance_index}($fp)')
        self.emit('addu $t1,$t1,4')
        # cargamos la tabla de metodos virtuales
        self.emit(f'lw $t1, 0($t1)')
        # resolve method address
        # call find_method_address function
        self.macro_push('$ra')
        self.macro_push('$fp')
        # ponemos en $v0 la direccion del string
        self.save_string(node.fid)
        # seteamos el frame del metodo que vamos a pasar
        self.emit('move $fp, $sp')
        # pasamos los parametros a la funcion
        self.macro_push('$v0')
        self.macro_push('$t1')
        # saltar a la funcion que busca el puntero al metodo correcto
        self.emit('jal __resolve_name')
        # tenemos en $v0 el puntero al metodo correcto
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit(f'mov $t0, $fp')
        self.emit(f'mov $fp, $sp')
        # pasamos los parametros del metodo
        for param in node.params:
            param_index = self.get_local_var_or_param_index(param)
            self.emit(f'lw $a0, {4*param_index}($t0)')
            self.macro_push('$a0')

        # llamamos al metodo
        self.emit(f'jalr $v0')
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')

    @visitor.when(cil_hierarchy.CILDinamicCallNode)
    def visit(self, node: cil_hierarchy.CILDinamicCallNode):
        # resolve method address
        # call find_method_address function
        self.macro_push('$ra')
        self.macro_push('$fp')
        # ponemos en $v0 la direccion del string
        self.save_string(node.fid)
        # seteamos el frame del metodo que vamos a pasar
        self.emit('move $fp, $sp')

        self.emit(f'lw $t2, type_{node.fType} + 4')
        self.emit('li $t3, 0')
        self.emit('lb $t3, 0($t2)')
        self.emit('addu $t2, $t2, $t3')
        self.emit('addu $t2,$t2,6')
        # guardamos en $t1 la direccion de memoria de la vtable del tipo definido por el nodo
        self.emit(f'lw $t1, 0($t2)')
        # pasamos los parametros a la funcion
        self.macro_push('$v0')
        self.macro_push('$t1')
        # saltar a la funcion que busca el puntero al metodo correcto
        self.emit('jal __resolve_name')
        # tenemos en $v0 el puntero al metodo correcto
        self.emit('move $sp, $fp')
        self.macro_pop('$fp')
        self.macro_pop('$ra')
        # ya tenemos en $v0 el metodo correcto!.

        self.macro_push('$ra')
        self.macro_push('$fp')
        self.emit(f'mov $t0, $fp')
        self.emit(f'mov $fp, $sp')
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
    def visit(self,node:cil_hierarchy.CILDivNode):
        l = node.left
        r = node.right                                                                                                                                                                                                                                                                                                                                                                                                                  
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        self.emit(f'(div $t3, $t0, $t2)')
        self.emit('move $v0, $t3')

    @visitor.when(cil_hierarchy.CILErrorMessage)
    def visit(self, node: cil_hierarchy.CILErrorMessage):
        self.emit(f'la $a0, {node.msg}')
        self.emit('li $v0, 4')
        self.emit('syscall')
        self.emit('li $v0, 10')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILFunctionNode)
    def visit(self,node: cil_hierarchy.CILFunctionNode):
        self.currentfuncv = node
        self.emit(f'{node.fname}:')
        for inst in node.instructions:
            self.visit(inst)

    @visitor.when(cil_hierarchy.CILGetAttributeNode)
    def visit(self,node:cil_hierarchy.CILGetAttributeNode):
        pass

    @visitor.when(cil_hierarchy.CILGetIndexNode)
    def visit(self,node:cil_hierarchy.CILGetIndexNode):
        self.emit(f'lw $v0, ({node.id} + 4*{node.index})')

    @visitor.when(cil_hierarchy.CILGetParentNode)
    def visit(self, node: cil_hierarchy.CILGetParentNode):
        localv_index = self.get_local_var_or_param_index(node.id)
        self.emit(f'lw $a0, {-4*localv_index}($fp)')
        self.emit('lw $v0, 4($a0)')


    @visitor.when(cil_hierarchy.CILIntegerComplementNode)
    def visit(self, node: cil_hierarchy.CILIntegerComplementNode):
        pass

    @visitor.when(cil_hierarchy.CILIsVoidNode)
    def visit(self, node: cil_hierarchy.CILIsVoidNode):
        try:
            v = self.get_local_var_or_param_index(node.is_void)
        except ValueError:
            self.emit('li, $v0, 0')
        else:
            self.emit(f'lw, $t0, {4*v}($fp)')
            self.emit('seq $v0, $t0, 0')
            #OJOJOJOJO poner esos labels por algun lado

    @visitor.when(cil_hierarchy.CILLabelNode)
    def visit(self,node:cil_hierarchy.CILLabelNode):
        self.emit(f'{node.label}:')

    @visitor.when(cil_hierarchy.CILLengthNode)
    def visit(self,node:cil_hierarchy.CILLengthNode):
        pass

    @visitor.when(cil_hierarchy.CILLoadNode)
    def visit(self,node:cil_hierarchy.CILLoadNode):
        self.emit(f'la, $v0, {node.msg}')

    @visitor.when(cil_hierarchy.CILMinusNode)
    def visit(self,node:cil_hierarchy.CILMinusNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        self.emit(f'neg $t2, $t1')
        self.emit(f'(add $t3, $t0, $t2)')
        self.emit('move $v0, $t3')

    # @visitor.when(cil_hierarchy.CILParamNode)
    # def visit(self,node: cil_hierarchy.CILParamNode):
    #     self.macro_push(node.vinfo.name)

    @visitor.when(cil_hierarchy.CILPlusNode)
    def visit(self,node:cil_hierarchy.CILPlusNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t0, {4*(v)}($fp)')

        self.emit(f'(add $t2, $t0, $t1)')
        self.emit('move $v0, $t2')

    @visitor.when(cil_hierarchy.CILPrefixNode)
    def visit(self,node:cil_hierarchy.CILPrefixNode):
        pass

    @visitor.when(cil_hierarchy.CILPrintStringNode)
    def visit(self,node:cil_hierarchy.CILPrintStringNode):
        try:
            v = self.currentfuncv.index(node.str_addr)
        except ValueError:
            self.emit(f'la $a0, {node.str_addr}')
        else:
            self.emit(f'lw $t0, ($sp + 4*{v})')
        self.emit('li $v0, 4')
        self.emit('syscall')

            
    @visitor.when(cil_hierarchy.CILPrintIntNode)
    def visit(self,node:cil_hierarchy.CILPrintIntNode):
        n = node.int_addr
        v = self.currentfuncv.index(n)
        self.emit(f'lw $t0, ($sp + 4*{v})')
        self.emit('move $a0, $t0')
        self.emit('li $v0, 1')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILReadStringNode)
    def visit(self,node:cil_hierarchy.CILReadStringNode):
        self.emit('li $v0, 8')
        self.emit('la $a0, std_in_data')
        self.emit('la $a1, std_in_data_size')
        self.emit('syscall')
    
    @visitor.when(cil_hierarchy.CILReadIntNode)
    def visit(self,node:cil_hierarchy.CILReadIntNode):
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
            local_index = self.get_local_var_or_param_index(node.value)
            self.emit(f'lw $v0, {-4*local_index}($fp)')
        self.emit('jr $ra')

    @visitor.when(cil_hierarchy.CILSetAttributeNode)
    def visit(self,node:cil_hierarchy.CILSetAttributeNode):
        pass

    @visitor.when(cil_hierarchy.CILSetIndexNode)
    def visit(self,node:cil_hierarchy.CILSetIndexNode):
        self.emit(f'lw {node.value}, ({node.id} + 4*{node.index})')

    @visitor.when(cil_hierarchy.CILStarNode)
    def visit(self,node:cil_hierarchy.CILStarNode):
        l = node.left
        r = node.right
        if type(l) == int or type(l) == float:
            self.emit(f'li $t0, {l}')
        elif type(l) == str:
            v = self.get_local_var_or_param_index(l)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        if type(r) == int or type(r) == float:
            self.emit(f'li $t1, {r}')
        elif type(r) == str:
            v = self.get_local_var_or_param_index(r)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        
        self.emit(f'(mul $t3, $t0, $t2)')
        self.emit('move $v0, $t3')

    @visitor.when(cil_hierarchy.CILSubstringNode)
    def visit(self,node:cil_hierarchy.CILSubstringNode):
        pass

    @visitor.when(cil_hierarchy.CILToStrNode)
    def visit(self, node: cil_hierarchy.CILToStrNode):
        pass

    @visitor.when(cil_hierarchy.CILTypeNameNode)
    def visit(self, node: cil_hierarchy.CILTypeNameNode):
        local_index = self.get_local_var_or_param_index(node.localv)
        # cargamos la direccion de la instancia
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        # cargamos la direccion del tipo
        self.emit('lw $a0, 0($a0)')
        self.emit('add $v0, $a0, 5')

    # todo??
    # @visitor.when(cil_hierarchy.CILTypeNode)
    # def visit(self, node: cil_hierarchy.CILTypeNode):
    #     self.emit(f'{node.name}:')

    # Todo
    @visitor.when(cil_hierarchy.CILTypeOfNode)
    def visit(self, node: cil_hierarchy.CILTypeOfNode):
        local_index = self.get_local_var_or_param_index(node.source)
        # cargamos la direccion de la instancia
        self.emit(f'lw $a0, {-4*local_index}($fp)')
        # cargamos la direccion del tipo
        self.emit('lw $v0, 0($a0)')
    
    @visitor.when(cil_hierarchy.CILNegationNode)
    def visit(self,node:cil_hierarchy.CILNegationNode):
        if type(node.id) == int or type(node.id) == float:
            self.emit(f'li $t0, {node.id}')
        else:
            v = self.get_local_var_or_param_index(node.id)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        self.emit(f'neg $t1, $t0')
        self.emit(f'move $v0, $t1')