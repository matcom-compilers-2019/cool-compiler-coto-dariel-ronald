.data
ior_msg_error: .asciiz "RuntimeError: Index out of range Error"
__void: .byte 0
std_in_data: .space 100
data_0: .asciiz "Hello World"
sep: .asciiz ","

data_1: .asciiz "EXECUTION ABORTED"

__types_definitions: 

__label:
.word 1
# esto es la tiza
.word 2
# esto es la tiza
.byte 5
# esto es la tiza
.asciiz "abcd"
# esto es la tiza
.byte 5
# esto es la tiza
.word __label
# esto es la tiza
.word __label_2
.byte 0

__label_2:
.byte 10

type_Object: 
# espacio de definicion del tipo
.word 26
# puntero al padre en la jerarquia
.word __void
# longitud del nombre de la clase
.byte 7
# nombre de la clase
.asciiz "Object"
# espacio que ocupa una instancia de esta clase
.byte 10
.byte 0
# puntero a la misma clase
.word type_Object
# direccion de la vtable de la clase
.word __vtable_Object
# cantidad de atributos
.byte 0

type_IO: 
# espacio de definicion del tipo
.word 22
# puntero al padre en la jerarquia
.word type_Object
# longitud del nombre de la clase
.byte 3
# nombre de la clase
.asciiz "IO"
# espacio que ocupa una instancia de esta clase
.byte 10
# puntero a la misma clase
.word type_IO
# direccion de la vtable de la clase
.word __vtable_IO
# cantidad de atributos
.byte 0

type_String_name:
.asciiz "String"

type_String: 
# espacio de definicion del tipo
.word 26
# puntero al padre en la jerarquia
.word __void
# longitud del nombre de la clase
.byte 7
# nombre de la clase
.asciiz type_String_name

# espacio que ocupa una instancia de esta clase
.byte 10
# puntero a la misma clase
.word type_String
# direccion de la vtable de la clase
.word __vtable_String
# cantidad de atributos
.byte 0

type_Bool: 
# espacio de definicion del tipo
.word 24
# puntero al padre en la jerarquia
.word __void
# longitud del nombre de la clase
.byte 5
# nombre de la clase
.asciiz "Bool"
# espacio que ocupa una instancia de esta clase
.byte 10
# puntero a la misma clase
.word type_Bool
# direccion de la vtable de la clase
.word __vtable_Bool
# cantidad de atributos
.byte 0

type_Main: 
# espacio de definicion del tipo
.word 24
# puntero al padre en la jerarquia
.word type_Object
# longitud del nombre de la clase
.byte 5
# nombre de la clase
.asciiz "Main"
# espacio que ocupa una instancia de esta clase
.byte 10
# puntero a la misma clase
.word type_Main
# direccion de la vtable de la clase
.word __vtable_Main
# cantidad de atributos
.byte 0

__vtables: 


__vtable_Object: 
.byte 4
# method
.byte 6
.asciiz "abort"
.word Object_abort
# method
.byte 10
.asciiz "type_name"
.word Object_type_name
# method
.byte 5
.asciiz "copy"
.word Object_copy
# method
.byte 27
.asciiz "cil_attributes_initializer"
.word Object_cil_attributes_initializer

__vtable_IO: 
.byte 8
# method
.byte 11
.asciiz "out_string"
.word IO_out_string
# method
.byte 8
.asciiz "out_int"
.word IO_out_int
# method
.byte 10
.asciiz "in_string"
.word IO_in_string
# method
.byte 7
.asciiz "in_int"
.word IO_in_int
# method
.byte 27
.asciiz "cil_attributes_initializer"
.word IO_cil_attributes_initializer
# method
.byte 6
.asciiz "abort"
.word Object_abort
# method
.byte 10
.asciiz "type_name"
.word Object_type_name
# method
.byte 5
.asciiz "copy"
.word Object_copy

__vtable_String: 
.byte 3
# method
.byte 7
.asciiz "length"
.word String_length
# method
.byte 7
.asciiz "concat"
.word String_concat
# method
.byte 7
.asciiz "substr"
.word String_substr

__vtable_Bool: 
.byte 0

__vtable_Main: 
.byte 5
# method
.byte 27
.asciiz "cil_attributes_initializer"
.word Main_cil_attributes_initializer
# method
.byte 5
.asciiz "main"
.word Main_main
# method
.byte 6
.asciiz "abort"
.word Object_abort
# method
.byte 10
.asciiz "type_name"
.word Object_type_name
# method
.byte 5
.asciiz "copy"
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
# la $a0, __vtable_IO
# li $v0, 1
# syscall

# xor $a0,$a0,$a0
# la $a0, data_0
# li $v0, 4
# syscall

xor $a0 ,$a0 ,$a0
la $a0, __label
li $v0, 1
syscall

la $a0, sep
li $v0, 4
syscall

xor $a0, $a0, $a0
la $a0, __label
add $a0, 16
lw $a0, 0($a0)
li $v0, 1
syscall

jr $ra
