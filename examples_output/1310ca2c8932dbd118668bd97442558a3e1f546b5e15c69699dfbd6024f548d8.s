.data
ior_msg_error: .asciiz "RuntimeError: Index out of range Error"
__void: .byte 0
std_in_data: .space 100
data_0: .asciiz "Hello World"

data_1: .asciiz "EXECUTION ABORTED"

__types_definitions: 


label_class_name_Object:
.asciiz "Object"
type_Object:
# espacio de definicion del tipo
.word 28
# puntero al padre en la jerarquia
.word __void
# puntero nombre de la clase
.word label_class_name_Object
# espacio que ocupa una instancia de esta clase
.word 12
# puntero a la misma clase
.word type_Object
# direccion de la vtable de la clase
.word __vtable_Object
# cantidad de atributos
.word 0


label_class_name_IO:
.asciiz "IO"
type_IO:
# espacio de definicion del tipo
.word 28
# puntero al padre en la jerarquia
.word type_Object
# puntero nombre de la clase
.word label_class_name_IO
# espacio que ocupa una instancia de esta clase
.word 12
# puntero a la misma clase
.word type_IO
# direccion de la vtable de la clase
.word __vtable_IO
# cantidad de atributos
.word 0


label_class_name_String:
.asciiz "String"
type_String:
# espacio de definicion del tipo
.word 28
# puntero al padre en la jerarquia
.word __void
# puntero nombre de la clase
.word label_class_name_String
# espacio que ocupa una instancia de esta clase
.word 12
# puntero a la misma clase
.word type_String
# direccion de la vtable de la clase
.word __vtable_String
# cantidad de atributos
.word 0


label_class_name_Bool:
.asciiz "Bool"
type_Bool:
# espacio de definicion del tipo
.word 28
# puntero al padre en la jerarquia
.word __void
# puntero nombre de la clase
.word label_class_name_Bool
# espacio que ocupa una instancia de esta clase
.word 12
# puntero a la misma clase
.word type_Bool
# direccion de la vtable de la clase
.word __vtable_Bool
# cantidad de atributos
.word 0


label_class_name_Main:
.asciiz "Main"
type_Main:
# espacio de definicion del tipo
.word 28
# puntero al padre en la jerarquia
.word type_Object
# puntero nombre de la clase
.word label_class_name_Main
# espacio que ocupa una instancia de esta clase
.word 12
# puntero a la misma clase
.word type_Main
# direccion de la vtable de la clase
.word __vtable_Main
# cantidad de atributos
.word 0
__vtables: 


label_method_name_Object_cil_attributes_initializer: 
.asciiz "cil_attributes_initializer"

label_method_name_Object_copy: 
.asciiz "copy"

label_method_name_Object_type_name: 
.asciiz "type_name"

label_method_name_Object_abort: 
.asciiz "abort"

__vtable_Object: 
.word 4
# method
.word label_method_name_Object_abort
.word Object_abort
# method
.word label_method_name_Object_type_name
.word Object_type_name
# method
.word label_method_name_Object_copy
.word Object_copy
# method
.word label_method_name_Object_cil_attributes_initializer
.word Object_cil_attributes_initializer

label_method_name_IO_copy: 
.asciiz "copy"

label_method_name_IO_type_name: 
.asciiz "type_name"

label_method_name_IO_abort: 
.asciiz "abort"

label_method_name_IO_cil_attributes_initializer: 
.asciiz "cil_attributes_initializer"

label_method_name_IO_in_int: 
.asciiz "in_int"

label_method_name_IO_in_string: 
.asciiz "in_string"

label_method_name_IO_out_int: 
.asciiz "out_int"

label_method_name_IO_out_string: 
.asciiz "out_string"

__vtable_IO: 
.word 8
# method
.word label_method_name_IO_out_string
.word IO_out_string
# method
.word label_method_name_IO_out_int
.word IO_out_int
# method
.word label_method_name_IO_in_string
.word IO_in_string
# method
.word label_method_name_IO_in_int
.word IO_in_int
# method
.word label_method_name_IO_cil_attributes_initializer
.word IO_cil_attributes_initializer
# method
.word label_method_name_IO_abort
.word Object_abort
# method
.word label_method_name_IO_type_name
.word Object_type_name
# method
.word label_method_name_IO_copy
.word Object_copy

label_method_name_String_substr: 
.asciiz "substr"

label_method_name_String_concat: 
.asciiz "concat"

label_method_name_String_length: 
.asciiz "length"

__vtable_String: 
.word 3
# method
.word label_method_name_String_length
.word String_length
# method
.word label_method_name_String_concat
.word String_concat
# method
.word label_method_name_String_substr
.word String_substr

__vtable_Bool: 
.word 0

label_method_name_Main_copy: 
.asciiz "copy"

label_method_name_Main_type_name: 
.asciiz "type_name"

label_method_name_Main_abort: 
.asciiz "abort"

label_method_name_Main_main: 
.asciiz "main"

label_method_name_Main_cil_attributes_initializer: 
.asciiz "cil_attributes_initializer"

__vtable_Main: 
.word 5
# method
.word label_method_name_Main_cil_attributes_initializer
.word Main_cil_attributes_initializer
# method
.word label_method_name_Main_main
.word Main_main
# method
.word label_method_name_Main_abort
.word Object_abort
# method
.word label_method_name_Main_type_name
.word Object_type_name
# method
.word label_method_name_Main_copy
.word Object_copy
.text
Object_cil_attributes_initializer:
subu $sp, $sp, 4
la $t0, type_Object
addu $t0, $t0, 8
li $t2, 0
lb $t2, 0($t0)
addu $t0,$t0,$t2
addu $t0,$t0,1
li $t1, 0
lb $t1, 0($t0)
addu $t0, $t0, 1
li $v0, 9
move $a0, $t1
syscall
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp,$sp
subu $sp, $sp, 4
sw $v0, 0($sp)
subu $sp, $sp, 4
sw $t0, 0($sp)
subu $sp, $sp, 4
sw $t1, 0($sp)
jal __copy_byte_by_byte
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -4($fp)
lw $v0, -4($fp)
jr $ra
Object_abort:
la $a0, data_1
li $v0, 4
syscall
li $v0, 10
syscall
Object_type_name:
subu $sp, $sp, 4
lw $a0, -4($fp)
lw $a0, 0($a0)
add $v0, $a0, 9
sw $v0, -8($fp)
lw $v0, -8($fp)
jr $ra
Object_copy:
subu $sp, $sp, 4
lw $a0, -4($fp)
lw $a1, 0($a0)
li $t3, 0
lb $t3, 8($a1)
addu $t3, $t3, 9
addu $a1, $a1, $t3
li $t0, 0
lb $t0, 0($a1)
li $v0, 9
move $a0, $t0
syscall
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
subu $sp, $sp, 4
sw $v0, 0($sp)
addu $a1, $a1, 1
subu $sp, $sp, 4
sw $a1, 0($sp)
subu $sp, $sp, 4
sw $t0, 0($sp)
jal __copy_byte_by_byte
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -8($fp)
lw $v0, -8($fp)
jr $ra
IO_cil_attributes_initializer:
subu $sp, $sp, 4
la $t0, type_IO
addu $t0, $t0, 8
li $t2, 0
lb $t2, 0($t0)
addu $t0,$t0,$t2
addu $t0,$t0,1
li $t1, 0
lb $t1, 0($t0)
addu $t0, $t0, 1
li $v0, 9
move $a0, $t1
syscall
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp,$sp
subu $sp, $sp, 4
sw $v0, 0($sp)
subu $sp, $sp, 4
sw $t0, 0($sp)
subu $sp, $sp, 4
sw $t1, 0($sp)
jal __copy_byte_by_byte
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -4($fp)
lw $v0, -4($fp)
jr $ra
IO_out_string:
lw $a0, -8($fp)
li $v0, 4
syscall
lw $v0, -4($fp)
jr $ra
IO_out_int:
lw $t0, -4($fp)
move $a0, $t0
li $v0, 1
syscall
lw $v0, -4($fp)
jr $ra
IO_in_string:
subu $sp, $sp, 4
li $v0, 8
la $a0, std_in_data
la $a1, 100
syscall
sw $v0, -8($fp)
lw $v0, -8($fp)
jr $ra
IO_in_int:
subu $sp, $sp, 4
li $v0, 5
syscall
sw $v0, -8($fp)
lw $v0, -8($fp)
jr $ra
String_length:
subu $sp, $sp, 4
subu $sp, $sp, 4
sw $ra, 0($sp)
lw $a0, -4($fp)
jal __get_str_len
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -8($fp)
lw $v0, -8($fp)
jr $ra
String_concat:
subu $sp, $sp, 4
subu $sp, $sp, 4
sw $ra, 0($sp)
lw $a0, -4($fp)
lw $a1, -8($fp)
jal __concat_strings
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -12($fp)
lw $v0, -12($fp)
jr $ra
String_substr:
subu $sp, $sp, 4
subu $sp, $sp, 4
sw $ra, 0($sp)
lw $a0, -4($fp)
lw $a1, -8($fp)
lw $a2, -12($fp)
jal __get_substring
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -16($fp)
lw $v0, -16($fp)
jr $ra
Main_cil_attributes_initializer:
subu $sp, $sp, 4
la $t0, type_Main
addu $t0, $t0, 8
li $t2, 0
lb $t2, 0($t0)
addu $t0,$t0,$t2
addu $t0,$t0,1
li $t1, 0
lb $t1, 0($t0)
addu $t0, $t0, 1
li $v0, 9
move $a0, $t1
syscall
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp,$sp
subu $sp, $sp, 4
sw $v0, 0($sp)
subu $sp, $sp, 4
sw $t0, 0($sp)
subu $sp, $sp, 4
sw $t1, 0($sp)
jal __copy_byte_by_byte
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -4($fp)
Main_main:
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
jal IO_cil_attributes_initializer
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -8($fp)
lw $v0, -8($fp)
sw $v0, -12($fp)
la, $v0, data_0
sw $v0, -16($fp)
lw $t1, -12($fp)
addu $t1,$t1,4
lw $t1, 0($t1)
move $t3, $t1
li $v0, 9
li $a0, 11
syscall
li $t1, 'o'
sb $t1, 0($v0)
li $t1, 'u'
sb $t1, 1($v0)
li $t1, 't'
sb $t1, 2($v0)
li $t1, '_'
sb $t1, 3($v0)
li $t1, 's'
sb $t1, 4($v0)
li $t1, 't'
sb $t1, 5($v0)
li $t1, 'r'
sb $t1, 6($v0)
li $t1, 'i'
sb $t1, 7($v0)
li $t1, 'n'
sb $t1, 8($v0)
li $t1, 'g'
sb $t1, 9($v0)
sb $0, 10($v0)
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
subu $sp, $sp, 4
sw $v0, 0($sp)
subu $sp, $sp, 4
sw $t3, 0($sp)
jal __resolve_name
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $t0, $fp
move $fp, $sp
lw $a0, 12($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
lw $a0, 16($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
jalr $v0
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -24($fp)
li $v0, 0
jr $ra
__get_distance:
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
lw $v0, -4($fp)
sw $v0, -12($fp)
li $v0, 0
sw $v0, -16($fp)
L1:
lw $t0, -12($fp)
lw $t1, -12($fp)
seq $v0, $t0, $t1
sw $v0, -20($fp)
lw $t0,-20($fp)
beqz $t0, L2
lw $t0, -12($fp)
lw $t1, -12($fp)
seq $v0, $t0, $t1
sw $v0, -24($fp)
lw $t0,-24($fp)
beqz $t0, L2
lw $a0, -12($fp)
lw $v0, 4($a0)
sw $v0, -12($fp)
lw $t0, 16($fp)
li $t1, 1
add $t2, $t0, $t1
move $v0, $t2
sw $v0, -16($fp)
b L1
L2:
lw $v0, -16($fp)
jr $ra
__get_closest_type:
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
subu $sp, $sp, 4
li $v0, 0
sw $v0, -12($fp)
li $v0, 0
sw $v0, -16($fp)
lw $t0, -8($fp)
lw $t1, -12($fp)
li $t2, -4
mul $t1,$t1, $t2
add $t0, $t0, $t1
lw $v0, 0($t0)
sw $v0, -20($fp)
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
lw $a0, 4($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
lw $a0, 20($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
jal __get_distance
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -24($fp)
L3:
subu $sp, $sp, 4
sw $ra, 0($sp)
lw $a0, -8($fp)
jal __get_str_len
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -32($fp)
lw $t0, -32($fp)
lw $t1, -32($fp)
sle $v0, $t0, $t1
sw $v0, -36($fp)
lw $t0,-36($fp)
beqz $t0, L5
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
lw $a0, 4($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
lw $a0, 20($t0)
subu $sp, $sp, 4
sw $a0, 0($sp)
jal __get_distance
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
sw $v0, -28($fp)
lw $t0, -28($fp)
lw $t1, -28($fp)
slt $v0, $t0, $t1
sw $v0, -40($fp)
lw $t0,-40($fp)
beqz $t0, L4
lw $t0, 12($fp)
li $t1, 1
add $t2, $t0, $t1
move $v0, $t2
sw $v0, -12($fp)
lw $t0, -8($fp)
lw $t1, -12($fp)
li $t2, -4
mul $t1,$t1, $t2
add $t0, $t0, $t1
lw $v0, 0($t0)
sw $v0, -20($fp)
b L3
L4:
lw $v0, -28($fp)
sw $v0, -24($fp)
lw $v0, -12($fp)
sw $v0, -16($fp)
b L3
L5:
lw $v0, -16($fp)
jr $ra

    __concat_strings:
    
        move $a3, $ra
        jal __get_str_len
        move $ra, $a3
        
        # guardamos en $t4, la longitud de str1
        move $t4, $v0
        # el str1
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
    
    __copy_byte_by_byte:
    lw $a0, -4($fp)
    lw $a1, -8($fp)
    lw $a2, -12($fp)
    
    move $v0, $a0
    
    __while_copy:
    beqz $a2, __end_copy
    
    xor $t0, $t0, $t0
    lb $t0, 0($a1)
    sb $t0, 0($a0), 
    
    subu $a2, $a2,1
    addu $a0, $a0,1
    addu $a1, $a1,1
    j __while_copy
    
    __end_copy:
    jr $ra
    
    __get_if_its_prefix:
            lb $t0, 0($a0)
            lb $t1, 0($a1)
            beqz $t0, prefixTrue
            bne	 $t0, $t1, prefixFalse
            addu $a0,$a0,1
            addu $a1,$a1,1
            b __get_if_its_prefix
        prefixFalse:
            li $v0, 0
            j $ra
        prefixTrue:
            li $v0, 1
            j $ra 
    
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
            sw $t5, 0($sp)
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
        

            __resolve_name:
            # guardamos en $a0 la direccion del string
            lw $a0, -4($fp)
            # guardamos en $a1 la direccion del vtable
            lw $a1, -8($fp)
            
            xor $t0,$t0,$t0
            # cargamos la longitud del array de metodos en $t0
            lb $t0, 0($a1)
            
            # t1 es el indice que se movera por el array
            li $t1, 0
            
            addu $a1, $a1, 1
            
            analize_method_name:
            li $t2, 0
            # nos paramos sobre el nombre del metodo
            addu $t2, $a1, 1
            
        
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
subu $sp, $sp, 4
sw $a0, 0($sp)
subu $sp, $sp, 4
sw $t2, 0($sp)
jal __compare_strings
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4

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
            
        
main: 
subu $sp, $sp, 4
sw $ra, 0($sp)
subu $sp, $sp, 4
sw $fp, 0($sp)
move $fp, $sp
jal Main_main
move $sp, $fp
lw $fp, 0($sp)
addu $sp, $sp, 4
lw $ra, 0($sp)
addu $sp, $sp, 4
