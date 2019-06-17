.data

msg1: .asciiz "hel"
msg2: .asciiz "hello"
msg3: .asciiz "world"

.text
    main:

    la, $a0, msg1
    la, $a1, msg2
    jal PrefixStr

    move $a0, $v0
    li $v0, 1
    syscall

    li $v0, 10
    syscall

    Here:
        li $a0, 100
        li $v0, 1
        syscall
        j $ra


    StrCmp:

        lbu $t0, 0($a0)
        lbu $t1, 0($a1)
        blt $t0,$t1,Minus
        bgt $t0,$t1,Plus
        beqz $t1,Zero
    continue:
        addi $a0,$a0,1
        addi $a1,$a1,1 
        b StrCmp
    Minus:
        li $v0,-1
        j $ra
    Plus:
        li $v0,1
        j $ra
    Zero:
        li $v0,0
        j $ra

    StrLem:
        li      $v0, 0
        move    $v1, $a0
    LenLoop:
        lbu     $t1, 0($v1)
        beq     $t1, $0, LenExit
        addi    $v0, $v0, 1
        addi    $v1, $v1, 1
        b		LenLoop			# branch to LenLoop
    LenExit:
        j $ra
    
    StrCpy:
        lbu		$t1,0($a0)		# Load a byte from the source string
        sb		$t1,0($a1)		# Store the byte in the destination string
        beq		$t1,$0,cpyExit	# Stop when th NULL is transferred.
        addi	$a0,$a0,1		# Increment both addresses.
        addi	$a1,$a1,1
        b		StrCpy
        
    cpyExit:
        j		$ra

    StrConcat:
        subu $sp, $sp, 4
        sw $a0, 0($sp)
        li $a0, 200
        li $v0, 9
        syscall
        lw $a0, 0($sp)
        addu $sp, $sp, 4

        subu $sp, $sp, 4
        sw $a0, 0($sp)
        subu $sp, $sp, 4
        sw $a1, 0($sp)
        subu $sp, $sp, 4
        sw $ra, 0($sp)
        move $a1, $v0
        jal StrCopy
        lw $ra, 0($sp)
        addu $sp, $sp, 4
        lw $a1, 0($sp)
        addu $sp, $sp, 4
        lw $a0, 0($sp)
        addu $sp, $sp, 4

        subu $sp, $sp, 4
        sw $a0, 0($sp)
        subu $sp, $sp, 4
        sw $a1, 0($sp)
        subu $sp, $sp, 4
        sw $ra, 0($sp)
        move $a0, $a1
        move $a1, $v1
        jal StrCopy
        lw $ra, 0($sp)
        addu $sp, $sp, 4
        lw $a1, 0($sp)
        addu $sp, $sp, 4
        lw $a0, 0($sp)
        addu $sp, $sp, 4

        j $ra

    StrCopy:
        or $t0, $a0, $zero
        or $t1, $a1, $zero
    StrCopyLoop:
        lb $t2, 0($t0)
        beq $t2, $zero, StrCopyEnd
        addi $t0, $t0, 1
        sb $t2, 0($t1)
        addi $t1, $t1, 1
        b StrCopyLoop
    
    StrCopyEnd:
        move $v1, $t1
        j $ra
    
    SubStr:
        move $t0, $a0
        move $t1, $a1
        li $t2, 0
        move $t3, $a2

    SubStrFirst:
        beq $t2, $a0,SubStrSaveSpace
        addi $t2, 1
        addi $t3, 1
        b SubStrFirst
    SubStrSaveSpace:

        subu $sp, $sp, 4
        sw $a0, 0($sp)
        move $a0, $a1
        li $v0, 9
        syscall
        lw $a0, 0($sp)
        addu $sp, $sp, 4
        move $t2, $v0
    SubStrCut:
       
       subu $sp, $sp, 4
       sw $a0, 0($sp)
       subu $sp, $sp, 4
       sw $a1, 0($sp)
       subu $sp, $sp, 4
       sw $ra, 0($sp)
       move $a0, $t3
       move $a1, $t2
       jal StrCopy
       lw $ra, 0($sp)
       addu $sp, $sp, 4
       lw $a1, 0($sp)
       addu $sp, $sp, 4
       lw $a0, 0($sp)
       addu $sp, $sp, 4

    SubStrExit:
        j $ra
    
    PrefixStr:
        lbu $t0, 0($a0)
        lbu $t1, 0($a1)
        beqz $t0, PrefixTrue
        bne		$t0, $t1,PrefixFalse
        addi $a0,$a0,1
        addi $a1,$a1,1 
        b PrefixStr
    PrefixTrue:
        li $v0, 1
        j $ra
    PrefixFalse:
        li $v0, -1
        j $ra
    



# subu $sp, $sp, 4
# sw $a0, 0($sp)
# subu $sp, $sp, 4
# sw $ra, 0($sp)
# jal Here
# lw $ra, 0($sp)
# addu $sp, $sp, 4
# lw $a0, 0($sp)
# addu $sp, $sp, 4
        