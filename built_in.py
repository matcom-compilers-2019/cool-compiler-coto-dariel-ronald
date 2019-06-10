from cil_hierarchy import *


def add_builtin_mips_functions(output):
    pass


def mips_prefix(output):
    '''
    Recibe en $a0 el prefijo, y en $a1, el str.
    :param output:
    :return: Devuelve en $v0 1 si es prefijo, 0 en otro caso.
    '''
    output.append('''
    __get_if_its_prefix:
            lb $t0, 0($a0)
            lb $t1, 0($a1)
            beqz $t0, prefixTrue
            bne	 $t0, $t1, prefixFalse
            addu $a0,$a0,1
            addu $a1,$a1,1
            b __get_if_its_prefix:
        prefixFalse:
            li $v0, 0
            j $ra
        prefixTrue:
            li $v0, 1
            j $ra 
    ''')


def mips_strLen(output):
    '''
    Recibe en $a0 la direccion del string
    :param output:
    :return: devuelve en $v0 la longitud del string
    '''
    output.append('''
        __get_str_len:
            li $v0,0
            move $v1, $a0
        __lenLoop:
            lbu $t1, 0($v1)
            beq $t1,$0,__lenExit
            addu $v0,$v0,1
            addu $v1,$v1,1
            b __lenLoop
        __lenExit:
            j $ra
    ''')


def mips_copy_byte_by_byte(output):
    '''
    Esta funcion recibe como primer parametro el lugar donde se va a copiar,
    como segundo de donde se va a copiar y
    como tercero cuantos bytes se vana copiar.
    :return:
    '''
    output.append('''
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


def mips_substring(output):
    output.append('''
    #a0 string original
    #a1 pos inicial que se va a tomar
    #a2 length del substr
    
    __get_substring:
            # load arguments
            move $t5, $a0
            move $t3, $a1
            li $t4, 0
            move $t2, $a2
            
            # check for index out of range (IOR Error)
            move $a0, $a2
            
            move $a3, $ra
            jal __get_str_len
            move $ra, $a3
            
            bge $t2, $v0, __abort_substrig_with_IOR_error
            addu $t6, $t3, $t2
            bge $t6, $v0, __abort_substrig_with_IOR_error
            
            # create substring
            move $a0, $t2
            li $v0, 9
            syscall
            # tenemos en $v0 la direccion del nuevo string
            
            addu $t5, $t5, $t3
            
            
            subu $sp, $sp, 4
            sw $ra, 0($sp)
            subu $sp, $sp, 4
            sw $fp, 0($sp)
            move $fp,$sp
            subu $sp, $sp, 4
            sw $v0, 0($sp)                        
            subu $sp, $sp, 4
            sw $$t5, 0($sp)
            subu $sp, $sp, 4
            sw $t2, 0($sp)
            
            jal __copy_byte_by_byte
            move $sp,$fp
            
            lw $fp, 0($sp)
            addu $sp, 4

            lw $ra, 0($sp)
            addu $sp, 4
            
            addu $t9, $v0, $t2
            sw $0, 0($t9)            
            jr $ra
                        
            __abort_substrig_with_IOR_error:
            li $v0, 10
            la $a0, ior_msg_error
            syscall
            jr $ra
    ''')


def mips_concat(output):
    '''
    Recibe en $a0 str1 y en $a1 str2
    :param output:
    :return: devuelve en $v0 la direccion en memoria del nuevo string
    '''
    output.append('''
    __concat_strings:
    
        move $a3, $ra
        jal __get_str_len
        move $ra, $a3
        
        # guardamos en $t4, la longitud de str1
        move $t4, $v0
        el str1
        move $t5, $a0
        move $a0, $a1
        move $t8, $a1
        
        move $a3, $ra
        jal __get_str_len
        move $ra, $a3
    
        # reservamos espacio para el nuevo string
        # guardamos en $t7 la longitud de str2
        move $t7, $v0
        addu $v0, $t4, $v0
        addu $v0, $v0, 1
        move $t6, $v0
        li $a0, 9
        syscall
        
        # en $t5 esta str1, y en $t8, str2-------------------------
        
        # save str1 part------------------------------------------
        # push $ra
        subu $sp, $sp, 4
        sw $ra, 0($sp)
        # push $fp
        subu $sp, $sp, 4
        sw $fp, 0($sp)
        
        move $fp, $sp
        
        # push dest to copy pointer
        subu $sp, $sp, 4
        sw $v0, 0($sp)
        
        # push copy from
        subu $sp, $sp, 4
        sw $t5, 0($sp)
        
        # push how much to copy 
        subu $sp, $sp, 4
        sw $t4, 0($sp)
        
        jal __copy_byte_by_byte
        
        move $sp, $fp
        
        lw $fp, 0($sp)
        addu $sp, $sp, 4
        
        lw $ra, 0($sp)
        addu $sp, $sp, 4
        
        # save str2 part-------------
        # push $ra
        subu $sp, $sp, 4
        sw $ra, 0($sp)
        
        # push $fp
        subu $sp, $sp, 4
        sw $fp, 0($sp)
        
        move $fp, $sp
        
        # push where to copy
        move $t9, $v0
        addu $t0, $v0, $t4
        subu $sp, $sp, 4
        sw $t0, 0($sp)
        
        # push copy from 
        subu $sp, $sp, 4
        sw $t8, 0($sp)
        
        subu $sp, $sp, 4
        sw $t7, 0($sp)
        
        jal __copy_byte_by_byte
        
        move $sp, $fp
        
        lw $fp, 0($sp)
        addu $sp, $sp, 4
        
        lw $ra, 0($sp)
        addu $sp, $sp, 4
        
        addu $v0, $t7, $v0
        addu $v0, $v0, 1
        sw $0, 0($v0)
        
        move $v0, $t9       
    ''')


def add_built_in(cool_to_cil):
        #OBJECT
        cool_to_cil.dottypes.append(CILTypeNode("Object", "None", [], ["Object_abort","Object_type_name","Object_copy"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_abort",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "Object_abort"
        cool_to_cil.register_data("EXECUTION ABORTED")
        cool_to_cil.register_instruction(CILErrorMessageNode, cool_to_cil.dotdata.data[-1].vname)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_type_name",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "Object_type_name"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo,  CILTypeNameNode("self"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("Object_copy",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "Object_copy"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILCopyNode("self"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #IO
        cool_to_cil.dottypes.append(CILTypeNode("IO", "Object", [], ["IO_out_string","IO_out_int","IO_in_string","IO_in_int"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_out_string",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "IO_out_string"
        cool_to_cil.register_instruction(CILPrintStringNode, "self")
        cool_to_cil.register_instruction(CILReturnNode, "self")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_out_int",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "IO_out_int"
        cool_to_cil.register_instruction(CILPrintIntNode, "self")
        cool_to_cil.register_instruction(CILReturnNode, "self")

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_in_string",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "IO_in_string"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILReadStringNode())
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("IO_in_int",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "IO_in_int"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILReadIntNode())
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #Int
        cool_to_cil.dottypes.append(CILTypeNode("Int", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())

        #String
        cool_to_cil.dottypes.append(CILTypeNode("String", "None", [], ["String_length","String_concat",
                                                                       "String_substr"]))
        cool_to_cil.dotcode.append(CILCodeNode())

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_length",[CILArgNode("self")]))
        cool_to_cil.current_function_name = "String_length"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILLengthNode("self"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_concat",[CILArgNode("self"),
                                                                                  CILArgNode("s")]))
        cool_to_cil.current_function_name = "String_concat"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILConcatNode("self", "s"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        cool_to_cil.dotcode[-1].functions.append(CILFunctionNode("String_substr",[CILArgNode("self"),
                                                                                  CILArgNode("index"),
                                                                                  CILArgNode("length")]))
        cool_to_cil.current_function_name = "String_substr"
        cool_to_cil.define_internal_local()
        dest = cool_to_cil.dotcode[-1].functions[-1].localvars[-1]
        cool_to_cil.register_instruction(CILAssignNode, dest.vinfo, CILSubstringNode("self", "index", "length"))
        cool_to_cil.register_instruction(CILReturnNode, dest.vinfo)

        #Bool
        cool_to_cil.dottypes.append(CILTypeNode("Bool", "None"))
        cool_to_cil.dotcode.append(CILCodeNode())
