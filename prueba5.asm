# C- Compilation to asm code
# File: prueba5
	.text
	.globl main
# 'max' Function Declaration
max:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
	lw $a0, 4($fp) 	# load argument
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	lw $a0, 8($fp) 	# load argument
	lw $t1, 4($sp) 	# load word
	addiu $sp, $sp, 4 	# add immediate unsigned
	bgt $a0 $t1 true_branch_0: 
false_branch_0:
	lw $a0, 8($fp) 	# load argument
	b end_if_0 
true_branch_0:
	lw $a0, 4($fp) 	# load argument
end_if_0:
	addiu $sp, $sp, 0 	# clear stack
	lw $ra, 4($sp) 	# load ra
	addiu $sp, $sp, 16 	# addiu
	lw $fp, 0($sp) 	# load fp
	jr $ra 
# 'main' Function Declaration
main:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
# Local declarations of  'main'
	li $a0, 0 	# initialize var maxV with 0
	sw $a0, 0($sp) 	# Var declaration 'maxV'
	addiu $sp, $sp, -4 	# update sp
# Assign Op in 'main'
# 'max' Function Call
	sw $fp, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
# Arguments
	li $a0, 2 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	li $a0, 6 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	jal max 
	sw $a0, -4($fp) 	# updating value of variable maxV
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
output:
	li $v0, 1 	# output result
	syscall
# End of execution.
