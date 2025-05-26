# C- Compilation to asm code
# File: prueba5
	.text
	.globl main
main:
	move $fp, $sp	# move operation
	sw $ra, 0($sp) 	# store return address
	addiu $sp, $sp, -4 	# add immediate unsigned
	lw $ra, 4($sp) 	# load ra
	addiu $sp, $sp, 8 	# addiu
	lw $fp, 0($sp) 	# load fp
	jr $ra 
	syscall
# End of execution.
