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

    # Type definition example
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
        type_space_in_bytes = sum([len(attr_name)for attr_name in node.attributes]) + len(node.attributes)*5 + 14
        # type space
        self.emit(f'.word {type_space_in_bytes}')
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
        self.output += type_definition_creator.output

        vtable_creator = CollectMipsVtablesVisitor()
        vtable_creator.visit(node)
        self.output += vtable_creator.output

        self.emit('.text')
        for i in range(len(node.dottypes)):
            self.visit(node.dotcode[i])

    @visitor.when(cil_hierarchy.CILAbortNode)
    def visit(self,node: cil_hierarchy.CILAbortNode):
        self.emit(f'la $a0, {node.msg}')
        self.emit(f'li $v0, 4')
        self.emit('syscall')
        self.emit(f'li $v0, 10')
        self.emit(f'syscall')
    

    @visitor.when(cil_hierarchy.CILAllocateNode)
    def visit(self,node:cil_hierarchy.CILAllocateNode):
        pass

    @visitor.when(cil_hierarchy.CILArrayNode)
    def visit(self,node:cil_hierarchy.CILArrayNode):
        self.emit('li $v0, 9')
        self.emit(f'lw $a0, {node.size}')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILAssignNode)
    def visit(self,node:cil_hierarchy.CILAssignNode):
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


    @visitor.when(cil_hierarchy.CILDinamicCallNode)
    def visit(self,node:cil_hierarchy.CILDinamicCallNode):
        pass

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
    def visit(self,node:cil_hierarchy.CILErrorMessage):
        self.emit(f'la $a0, {node.msg}')
        self.emit('li $v0, 4')
        self.emit('syscall')
        self.emit('li $v0, 10')
        self.emit('syscall')

    @visitor.when(cil_hierarchy.CILFunctionNode)
    def visit(self,node:cil_hierarchy.CILFunctionNode):
        self.currentfuncv = node
        for inst in node.instructions:
            self.visit(inst)

    @visitor.when(cil_hierarchy.CILGetAttributeNode)
    def visit(self,node:cil_hierarchy.CILGetAttributeNode):
        pass

    @visitor.when(cil_hierarchy.CILGetIndexNode)
    def visit(self,node:cil_hierarchy.CILGetIndexNode):
        self.emit(f'lw $v0, ({node.id} + 4*{node.index})')

    @visitor.when(cil_hierarchy.CILGetParentNode)
    def visit(self,node:cil_hierarchy.CILGetParentNode):
        pass

    @visitor.when(cil_hierarchy.CILIntegerComplementNode)
    def visit(self,node:cil_hierarchy.CILIntegerComplementNode):
        pass

    @visitor.when(cil_hierarchy.CILIsVoidNode)
    def visit(self,node:cil_hierarchy.CILIsVoidNode):
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

    @visitor.when(cil_hierarchy.CILParamNode)
    def visit(self,node:cil_hierarchy.CILParamNode):
        self.macro_push(node.vinfo.name)

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
    def visit(self,node:cil_hierarchy.CILReturnNode):
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

    @visitor.when(cil_hierarchy.CILStaticCallNode)
    def visit(self,node:cil_hierarchy.CILStaticCallNode):
        self.emit(f'jal, {node.id}')
        self.emit('move $sp, $fp')
        self.macro_pop('$ra')
        self.macro_pop('$fp')

    @visitor.when(cil_hierarchy.CILSubstringNode)
    def visit(self,node:cil_hierarchy.CILSubstringNode):
        pass

    @visitor.when(cil_hierarchy.CILToStrNode)
    def visit(self,node:cil_hierarchy.CILToStrNode):
        pass

    @visitor.when(cil_hierarchy.CILTypeNameNode)
    def visit(self,node:cil_hierarchy.CILTypeNameNode):
        pass

    @visitor.when(cil_hierarchy.CILTypeNode)
    def visit(self,node:cil_hierarchy.CILTypeNode):
        self.emit(f'{node.name}:')


    @visitor.when(cil_hierarchy.CILTypeOfNode)
    def visit(self,node:cil_hierarchy.CILTypeOfNode):
        pass
    
    @visitor.when(cil_hierarchy.CILNegationNode)
    def visit(self,node:cil_hierarchy.CILNegationNode):
        if type(node.id) == int or type(node.id) == float:
            self.emit(f'li $t0, {node.id}')
        else:
            v = self.get_local_var_or_param_index(node.id)
            self.emit(f'lw $t0, {4*(v)}($fp)')
        self.emit(f'neg $t1, $t0')
        self.emit(f'move $v0, $t1')