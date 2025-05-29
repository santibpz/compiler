# C- Compilation to asm code
# File: prueba5
	.text
	.globl main

# 'main' Function Declaration
main:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
# Local declarations of  'main'
	li $a0, 0 	# initialize var res with 0
	sw $a0, 0($sp) 	# Var declaration 'res'
	addiu $sp, $sp, -4 	# update sp
# Assign Op in 'main'
# 'sum' Function Call
	sw $fp, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
# Arguments
	li $a0, 8 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	li $a0, 3 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	jal sum 
	sw $a0, -4($fp) 	# updating value of variable res
# 'output' Function Call
	sw $fp, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
# Arguments
	lw $a0, -4($fp) 	# load argument
	jal output 
	addiu $sp, $sp, 4 	# clear stack
	lw $ra, 4($sp) 	# load ra
	addiu $sp, $sp, 8 	# addiu
	lw $fp, 0($sp) 	# load fp
	jr $ra 

# 'sum' Function Declaration
sum:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
# Local declarations of  'sum'
	li $a0, 0 	# initialize var x with 0
	sw $a0, 0($sp) 	# Var declaration 'x'
	addiu $sp, $sp, -4 	# update sp
# Assign Op in 'sum'
	lw $a0, 4($fp) 	# load argument
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	lw $a0, 8($fp) 	# load argument
	lw $t1, 4($sp) 	# load word
	add $a0, $a0, $t1 	# add
	addiu $sp, $sp, 4 	# add immediate unsigned
	sw $a0, -4($fp) 	# updating value of variable x
	lw $a0, -4($fp) 	# load argument
	addiu $sp, $sp, 4 	# clear stack
	lw $ra, 4($sp) 	# load ra
	addiu $sp, $sp, 16 	# addiu
	lw $fp, 0($sp) 	# load fp
	jr $ra 

output:
	li $v0, 1 	# output result
	syscall
# End of execution.
