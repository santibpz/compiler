* C- Compilation to TM Code
* File: prueba5
* Standard prelude:
* End of standard prelude.
li $a0 3 	load immediate value
sw $a0 0($sp) 	store word
addiu $sp $sp -4 	add immediate unsigned
li $a0 5 	load immediate value
lw $t1 4($sp) 	load word
add $a0 $a0 $t1 	add
addiu $sp $sp 4 	add immediate unsigned
* End of execution.
