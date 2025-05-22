# C- Compilation to asm code
# File: prueba5
	.text
	.globl main
main:
	sw $fp, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	li $a0, 5 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	li $a0, 2 	# load immediate value
	sw $a0, 0($sp) 	# store word
	addiu $sp, $sp, -4 	# add immediate unsigned
	jal add 
	syscall
# End of execution.
