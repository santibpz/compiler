# C- Compilation to asm code
# File: prueba5
	.text
	.globl main
testFn:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
	li $a0, 0 	# initialize var x with 0
	sw $a0, 0($sp) 	# Var declaration 'x'
	addiu $sp, $sp, -4 	# update sp
	lw $ra, 4($sp) 	# load ra
	addiu $sp, $sp, 16 	# addiu
	lw $fp, 0($sp) 	# load fp
	jr $ra 
	syscall
# End of execution.
