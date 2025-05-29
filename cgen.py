from globalTypes import * 
from symtab import *
import sys


# accumulator
acc = '$a0'
# stack pointer
sp = '$sp'
# frame pointer
fp = '$fp'
# return address
ra = '$ra'
# temporary register
temp = '$t1'
# Int register
v0 = '$v0'
# offset
off = 0

# TM location number for current instruction emission
emitLoc = 0
# Highest TM location emitted so far for use in conjunction with emitSkip,
# emitBackup, and emitRestore
highEmitLoc = 0

# Procedure emitComment prints a comment line with comment c in the code file
def emitComment(c):
    if (TraceCode):
        print("# " + c)

# Procedure emitLI emits a Loas immediate value into register
# op = the opcode
# r = destination register
# imm = value
# c = a comment to be printed if TraceCode is TRUE
def emitLI( op, r, imm, c):
    # global emitLoc
    # global highEmitLoc
    print("\t%s %s, %d " % (op,r,imm), end='')
    # emitLoc += 1
    if (TraceCode):
        print("\t# " + c, end='')
    print()
    # if (highEmitLoc < emitLoc):
    #     highEmitLoc = emitLoc


# Procedure emitLW emits a load word in register 'dr' from address contained in 'sr'+offset
# op = the opcode
# sr = source register
# off = offset
# dr = destination register
# c = a comment to be printed if TraceCode is TRUE
def emitLW( op, dr, off, sr, c):
    # global emitLoc
    # global highEmitLoc
    print("\t%s %s, %s " % (op, dr, f"{off}({sr})"), end='')
    # emitLoc += 1
    if (TraceCode):
        print("\t# " + c, end='')
    print()
    # if (highEmitLoc < emitLoc):
    #     highEmitLoc = emitLoc}



# Procedure emitSW emits a store word in register 'sr' into RAM at address contained in 'dr'
# op = the opcode
# sr = source register
# off = offset
# dr = destination register
# c = a comment to be printed if TraceCode is TRUE
def emitSW( op, sr, off, dr, c):
    # global emitLoc
    # global highEmitLoc
    print("\t%s %s, %s " % (op, sr, f"{off}({dr})"), end='')
    # emitLoc += 1
    if (TraceCode):
        print("\t# " + c, end='')
    print()
    # if (highEmitLoc < emitLoc):
    #     highEmitLoc = emitLoc}


# Procedure emitADD emits add operation
# op = the opcode
# dr = destination register
# r1 = register 1
# r2 = register 2
# c = a comment to be printed if TraceCode is TRUE
def emitADD( op, dr, r1, r2, c):
    # global emitLoc
    # global highEmitLoc
    print("\t%s %s, %s, %s " % (op, dr, r1, r2), end='')
    # emitLoc += 1
    if (TraceCode):
        print("\t# " + c, end='')
    print()
    # if (highEmitLoc < emitLoc):
    #     highEmitLoc = emitLoc



# Procedure emitADDIU emits add immediate unsign to update sp
# op = the opcode
# dr = destination register
# sr = source register
# imm = value
# c = a comment to be printed if TraceCode is TRUE
def emitADDIU( op, dr, sr, imm, c):
    # global emitLoc
    # global highEmitLoc
    print("\t%s %s, %s, %d " % (op, dr, sr, imm), end='')
    # emitLoc += 1
    if (TraceCode):
        print("\t# " + c, end='')
    print()
    # if (highEmitLoc < emitLoc):
    #     highEmitLoc = emitLoc

# Procedure emitLI emits a Loas immediate value into register
# op = the opcode
# d = destination register
# s = source register
# c = a comment to be printed if TraceCode is TRUE
def emitMove( op, d, s, c):
    print("\t%s %s, %s" % (op, d, s), end='')
    if (TraceCode):
        print("\t# " + c, end='')
    print()

# Procedure to output int
def output():
    print(f"output:")
    emitLI('li', v0, 1, "output result")
    print(f"\tsyscall")


# Procedure genExp generates code at an expression node */
def genExp(tree):
    global tmpOffset
    if tree.exp == ExpKind.ConstK:
        if (TraceCode):
            emitComment("-> Const")
        # gen code to load integer constant using LDC */
        emitRM("LDC",ac,tree.val,0,"load const")
        if (TraceCode):
            emitComment("<- Const")
    elif tree.exp == ExpKind.IdK:
        if (TraceCode):
            emitComment("-> Id")
        loc = st_lookup(tree.name)
        emitRM("LD",ac,loc,gp,"load id value")
        if (TraceCode):
            emitComment("<- Id")
    elif tree.exp == ExpKind.OpK:
        if (TraceCode):
            emitComment("-> Op")
        p1 = tree.child[0]
        p2 = tree.child[1]
        # gen code for ac = left arg */
        cGen(p1);
        # gen code to push left operand */
        emitRM("ST",ac,tmpOffset,mp,"op: push left")
        tmpOffset-=1
        # gen code for ac = right operand */
        cGen(p2);
        # now load left operand */
        tmpOffset+=1;
        emitRM("LD",ac1,tmpOffset,mp,"op: load left")
        if tree.op == TokenType.PLUS:
            emitRO("ADD",ac,ac1,ac,"op +")
        elif tree.op == TokenType.MINUS:
            emitRO("SUB",ac,ac1,ac,"op -")
        elif tree.op == TokenType.TIMES:
            emitRO("MUL",ac,ac1,ac,"op *")
        elif tree.op == TokenType.OVER:
            emitRO("DIV",ac,ac1,ac,"op /")
        elif tree.op == TokenType.LT:
            emitRO("SUB",ac,ac1,ac,"op <")
            emitRM("JLT",ac,2,pc,"br if true") 
            emitRM("LDC",ac,0,ac,"false case") 
            emitRM("LDA",pc,1,pc,"unconditional jmp") 
            emitRM("LDC",ac,1,ac,"true case") 
        elif tree.op == TokenType.EQ:
            emitRO("SUB",ac,ac1,ac,"op ==")
            emitRM("JEQ",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp") 
            emitRM("LDC",ac,1,ac,"true case")
        else:
            emitComment("BUG: Unknown operator")
        if (TraceCode):
            emitComment("<- Op")

# Procedure to generate argument code
def genArgs(tree, scope_name=None): # tree should be ExpressionType.Num
    if tree != None:
        genArgs(tree.sibling)
        if tree.expression == ExpressionType.Num:
            # gen code to load integer constant using LDC */
            emitLI("li", acc, tree.value, "load immediate value")
            emitSW('sw', acc, 0, sp, "store word")
            emitADDIU("addiu", sp, sp, -4, "add immediate unsigned")
        else:
            cGen(tree, scope_name)
# Procedure cGen recursively generates code by tree traversal
def cGen(tree, scope_name=None):
    global off
    if (tree != None):
    
        if tree.expression == ExpressionType.Num:
            # gen code to load integer constant using LDC */
            emitLI("li", acc, tree.value, "load immediate value")

        elif tree.expression == ExpressionType.Var:
            offset = get_offset(scope_name, tree.value)
            # print("val: ", tree.value)
            # print("offset: ", get_offset(scope_name, tree.value))
            emitLW('lw', acc, offset, fp, "load argument")
        
        elif tree.expression == ExpressionType.VarDeclaration:
            if scope_name is not None:
                # set the offset (local variable allocation)
                e = tree
                while e is not None:
                    off -= 4 
                    upt_offset(scope_name, e.value, off)
                    emitLI('li', acc, 0, f"initialize var {e.value} with 0")
                    emitSW('sw', acc, 0, sp, f"Var declaration '{e.value}'")
                    emitADDIU("addiu", sp, sp, -4, "update sp")
                    e = e.sibling

        elif tree.expression == ExpressionType.Addop:
            e1 = tree.child[0]
            e2 = tree.child[1]

            cGen(e1, scope_name) 
            emitSW("sw", acc, 0, sp, "store word")
            emitADDIU("addiu", sp, sp, -4, "add immediate unsigned")
            cGen(e2, scope_name)
            emitLW('lw', temp, 4, sp, "load word")
            emitADD('add', acc, acc, temp, "add")
            emitADDIU("addiu", sp, sp, 4, "add immediate unsigned")
            # emitLI("li", v0, 1, "load immediate value")
        
        elif tree.expression == ExpressionType.Assign:
            print(f"# Assign Op in '{scope_name}'")
            v = tree.child[0] # variable
            e = tree.child[1] # right subtree
            if e is not None:
                cGen(e, scope_name) # process right subtree, result in $a0
                offset = get_offset(scope_name, v.value)
                emitSW("sw", acc, offset, fp, f"updating value of variable {v.value}")
            
            # generate code for other statements
            if tree.sibling is not None:
                cGen(tree.sibling, scope_name)

                
        elif tree.expression == ExpressionType.Param:
            if scope_name is not None:
                e = tree
                while e is not None:
                    off=off+4
                    upt_offset(scope_name, e.value, off)
                    e = e.sibling
            # emitLW('lw', acc, off, fp, "load argument")
            # emitSW('sw', acc, 0, sp, "store word")
            # emitADDIU('addiu', sp, sp, -4, "add immediate unsigned")
        
        elif tree.expression == ExpressionType.FunDeclaration: # calle
            print(f"# '{tree.value}' Function Declaration")
            z = 4 * tree.params_num + 8
            e1 = tree.child[1] # Param
            e2 = tree.child[2] # function body
            print(f"{tree.value}:")
            emitMove('move', fp, sp, "move operation")
            emitSW('sw', ra, 0, sp, "store return address")
            emitADDIU('addiu', sp, sp, -4, "add immediate unsigned")
            if e1 is not None:
                cGen(e1, tree.value)
                off = 0
            if e2 is not None:
                cGen(e2, tree.value) # local declarations
                # off = 0
                # generate code for statement_list
                if e2.sibling is not None:
                    cGen(e2.sibling, tree.value)
                
                emitADDIU('addiu', sp, sp, -off, 'clear stack')
                off = 0

            emitLW('lw', ra, 4, sp, 'load ra')
            emitADDIU('addiu', sp, sp, z, 'addiu')
            emitLW('lw', fp, 0, sp, 'load fp')
            print("\t%s %s " % ('jr', ra), end='\n')

            # generate code for other function or var declarations
            if tree.sibling is not None:
                cGen(tree.sibling)

        elif tree.expression == ExpressionType.Args: # arguments passed to called fn
            print(f"# Arguments")
            e = tree.child[0]
            if e is not None:
                genArgs(e, scope_name)
            # while e is not None:
            #     cGen(e)
            #     emitSW('sw', acc, 0, sp, "store word")
            #     emitADDIU("addiu", sp, sp, -4, "add immediate unsigned")
            #     e = e.sibling
        
        elif tree.expression == ExpressionType.Call:
            print(f"# '{tree.value}' Function Call")
            e = tree.child[0] # Args Node

            emitSW('sw', fp, 0, sp, "store word")
            emitADDIU('addiu', sp, sp, -4, "add immediate unsigned")
            if e is not None:
                cGen(e, scope_name)
            print("\t%s %s " % ('jal', f"{tree.value}"), end='\n')

        elif tree.expression == DeclarationKind.LocalDeclaration:
            print(f"# Local declarations of  '{scope_name}'")
            e = tree.child[0] # var declaration
            if e is not None:
                cGen(e, scope_name)
            
        elif tree.expression == ExpressionType.Return:
            e = tree.child[0]
            if e is not None and scope_name is not None:
                cGen(e, scope_name)

        # cGen(tree.sibling)

#********************************************
# the primary function of the code generator 
#********************************************
# Procedure codeGen generates code to a code
# file by traversal of the syntax tree. The
# second parameter (codefile) is the file name
# of the code file, and is used to print the
# file name as a comment in the code file
def codeGen(syntaxTree, codefile, trace):
    global TraceCode
    global code
    #print(BucketList) # ¿Por qué se mantiene esta variable si está declarada en symtab.py?
    TraceCode = trace # Si es True imprime comentarios
    stdout = sys.stdout
    sys.stdout = open(codefile + '.asm', 'w')
    s = "File: " + codefile
    emitComment("C- Compilation to asm code")
    emitComment(s)
    # main asm template
    print(f"\t.text")
    print(f"\t.globl main")

    # print("main:")
    
    # generate code for TINY program
    cGen(syntaxTree)
    output()
    # finish
    emitComment("End of execution.")
    sys.stdout.close()
    sys.stdout = stdout
    

