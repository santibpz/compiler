# grammar implementation for c-

from enum import enum

class ExpressionType(Enum):
    Relop = 0 # <= | < | > | >= | == | !=
    Addop = 1 # + | -
    Mulop = 2 # * | /
    TypeSpecifier = 3 # int | void
    Num = 4 # 0123456789
    Empty = 5 # ' '
    Id = 6 # id

# TreeNode class
class TreeNode:
    def __init__(self):
        self.leftChild = None
        self.rightChild = None
        self.expression = None
        self.value = None

# method to create new node
def newNode(type):
    node = TreeNode()
    if(node == None):
        print("No memory")
    else:
        node.exp = type
    return node

# syntax error method
def syntaxError(errorMessage):
    print(f'>>> Syntax Error: {errorMessage}')

# print AST

# match method
def match(tok):
    # token is next
    global token, pos

    if token == tok:
        pos+=1
        if pos == len(cadena):
            token = '$'
        else:
            token = cadena[pos]
    else:
        syntaxError('unexpected token')

# 1. program → declaration-list
def program():
    root = declarationList()
    return root

# 2. declaration-list → declaration { declaration }
def declarationList():
    subtree = declaration()
    # while token in 

#3. declaration → var-declaration | fun-declaration

# 4. var-declaration → type-specifier ID [ “[“ NUM “]” ]  ;

def varDeclaration():
    if token in ["int", "void"]:
        node = newNode(ExpressionType.TypeSpecifier)
        node.value = token
        match(token)
    
    match()

