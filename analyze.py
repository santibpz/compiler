from globalTypes import *
from symtab import *

Error = False
# counter for variable memory locations
location = 0

# scope variable
scope = 0

# Procedure traverse is a generic recursive 
# syntax tree traversal routine:
# it applies preProc in preorder and postProc 
# in postorder to tree pointed to by t

def traverse(t, preProc, postProc):
    if (t != None and isinstance(t, TreeNode)):
        preProc(t) # preProc is insertNode
        for i in range(3):
            traverse(t.child[i],preProc,postProc)
        postProc(t)
        traverse(t.sibling,preProc,postProc)

# nullProc is a do-nothing procedure to generate preorder-only or
# postorder-only traversals from traverse
def nullProc(t):
    None

# Procedure insertNode inserts identifiers stored in t into 
# the symbol table to insert a node in the current ST
def insertNode(t):
    global location, scope
    if t != None and isinstance(t, TreeNode):
        if t.expression == ExpressionType.VarDeclaration:
            if st_lookup(t.value, True) is None:
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location, size=t.arr_size)
                location += 1
            else:
                # already in table, so ignore location, 
                # add line number of use only
                print("symbol already in ST")
        
        elif t.expression == ExpressionType.Var or t.expression == ExpressionType.Call:
            if st_lookup(t.value) is None: # found symbol
                SemanticError(f"Undefined identifier '{t.value}'", t.lineno)
            else: 
                entry = st_lookup(t.value)
                entry["lines"].append(t.lineno)
                st_update(t.value, entry)

                # check that the number of arguments of a call function match the number of arguments the function definition expects
                if t.expression == ExpressionType.Call and t.child[0] is not None:
                    a_n = t.child[0].args_num
                    p_m = entry["params_num"]
                    if entry["params_num"] != a_n:
                        SemanticError(f"Expected {p_m} arguments but {a_n} were given.", t.lineno)
            
        elif t.expression == DeclarationKind.LocalDeclaration:
            scope += 1
            location += 1
            push_st('local')

        elif t.expression == ExpressionType.FunDeclaration:
            if (st_lookup(t.value) is None):
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location, params=True, params_num=t.params_num)
                location+=1
             
            else:
                # already in table, so ignore location, 
                # add line number of use only
                print("symbol already in ST")

        elif t.expression == ExpressionType.Param:
            
            if (st_lookup(t.value) is None):
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location)
                location += 1
            else:
                # already in table, so ignore location, 
                # add line number of use only
                print("symbol already in ST")
            
# Function buildSymtab constructs the symbol 
# table by preorder traversal of the syntax tree
def buildSymtab(syntaxTree, imprime):
    traverse(syntaxTree, insertNode, nullProc)
    if (imprime):
        print()
        print("Symbol table:")
        printSymbolTableStack()

def typeError(t, message):
    print("Type error at line", t.lineno, ":",message)
    Error = True

# syntax error method
def SemanticError(errorMessage, lineno):
    print(f">>> {errorMessage} at line {lineno}\n", end='')


# Procedure checkNode performs type checking at a single tree node
def checkNode(t):
    if t.expression == ExpressionType.Var or t.expression == ExpressionType.Call:
        entry = st_lookup(t.value)
        if entry is not None:
            exp_type = entry["type"]
            if exp_type == ExpType.Void.value:
                t.type = ExpType.Void
            elif exp_type == ExpType.Integer.value:
                t.type = ExpType.Integer

    elif t.expression == ExpressionType.Num:
        t.type = ExpType.Integer

    elif t.expression == ExpressionType.Assign:
        if ((t.child[0].type != ExpType.Integer) or (t.child[1].type != ExpType.Integer)):
             typeError(t,"Assignment of non-integer value")
    
    elif t.expression == ExpressionType.Addop or t.expression == ExpressionType.Mulop:
        if ((t.child[0].type != ExpType.Integer) or (t.child[1].type != ExpType.Integer)):
             typeError(t,f"Expected both operands of {t.value} to be of type {ExpType.Integer.value}, but type mismatch was found\n")
        else:
            t.type = ExpType.Integer
    
    elif t.expression == ExpressionType.Relop:
        if ((t.child[0].type != ExpType.Integer) or (t.child[1].type != ExpType.Integer)):
             typeError(t,f"Invalid operands to binary expression\n")
        else:
            t.type = ExpType.Integer

        

# Procedure typeCheck performs type checking 
# by a postorder syntax tree traversal


def typeCheck(syntaxTree):
    traverse(syntaxTree,nullProc,checkNode)
