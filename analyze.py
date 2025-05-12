from globalTypes import *
from symtab import *

Error = False
location = 0

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
            if st_lookup(t.value) is None:
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location, size=t.arr_size)
                location += 1
            else:
                # already in table, so ignore location, 
                # add line number of use only
                st_insert(t.name,t.lineno,0)

        elif t.expression == ExpressionType.FunDeclaration:
            if (st_lookup(t.value) is None):
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location, params=True)
                scope += 1
                location += 1
                push_st('fun_declaration')
            else:
                # already in table, so ignore location, 
                # add line number of use only
                st_insert(t.name,t.lineno,0)

        elif t.expression == ExpressionType.Param:
            
            if (st_lookup(t.value) is None):
                # not yet in table, so treat as new definition
                st_insert(t.value, t.child[0], scope, t.lineno, location)
                location += 1
            else:
                # already in table, so ignore location, 
                # add line number of use only
                st_insert(t.name,t.lineno,0)
            
    # elif t.nodekind == NodeKind.ExpK:
    #     if t.exp == ExpKind.IdK:
    #         if (st_lookup(t.name) == -1):
    #             # not yet in table, so treat as new definition */
    #             st_insert(t.name,t.lineno,location)
    #             location += 1
    #         else:
    #             # already in table, so ignore location, 
    #             # add line number of use only */ 
    #             st_insert(t.name,t.lineno,0)

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

# # Procedure checkNode performs type checking at a single tree node
# def checkNode(t):
#     if t.nodekind == NodeKind.ExpK:
#         if t.exp == ExpKind.OpK:
#             if ((t.child[0].type != ExpType.Integer) or (t.child[1].type != ExpType.Integer)):
#                 typeError(t,"Op applied to non-integer")
#             if ((t.op == TokenType.EQ) or (t.op == TokenType.LT)):
#                 t.type = ExpType.Boolean
#             else:
#                 t.type = ExpType.Integer
#         elif t.exp in [ExpKind.ConstK, ExpKind.IdK]:
#             t.type = ExpType.Integer
#     elif t.nodekind == NodeKind.StmtK:
#         if t.stmt == StmtKind.IfK:
#             if (t.child[0].type == ExpType.Integer):
#                 typeError(t.child[0],"if test is not Boolean")
#         elif t.stmt == StmtKind.AssignK:
#             if (t.child[0].type != ExpType.Integer):
#                 typeError(t.child[0],"assignment of non-integer value")
#         elif t.stmt == StmtKind.WriteK:
#             if (t.child[0].type != ExpType.Integer):
#                 typeError(t.child[0],"write of non-integer value")
#         elif t.stmt == StmtKind.RepeatK:
#             if (t.child[1].type == ExpType.Integer):
#                 typeError(t.child[1],"repeat test is not Boolean")

# Procedure typeCheck performs type checking 
# by a postorder syntax tree traversal


# def typeCheck(syntaxTree):
#     traverse(syntaxTree,nullProc,checkNode)
