# grammar implementation for c-

from lexer import *
from globalTypes import *
from enum import Enum


token = None # holds current token
tokenString = None # holds the token string value 
Error = False
#lineno = 1
SintaxTree = None
indentno = 0

def recibeParser(prog, pos, long): # Recibe los globales del main
    globales(prog, pos, long, 1) # Para mandar los globales

class ExpressionType(Enum):
    Relop = 0 # <= | < | > | >= | == | !=
    Addop = 1 # + | -
    Mulop = 2 # * | /
    TypeSpecifier = 3 # int | void
    Num = 4 # 0123456789
    Empty = 5 # ' '
    Id = 6 # id
    Call = 7 # Function call
    Var = 8 # Var
    Expr = 9 # Expression
    If = 10 # If statement
    Assign = 11 # Assign Op =

# TreeNode class
class TreeNode:
    def __init__(self):
        # self.leftChild = None
        # self.rightChild = None
        self.child = [None]*3
        self.sibling = None
        self.expression = None
        self.value = None

# method to create new node
def newNode(type):
    node = TreeNode()
    if(node == None):
        print("No memory")
    else:
        node.expression = type
    return node

# syntax error method
def SyntaxError(errorMessage):
    print(f'>>> Syntax Error: {errorMessage}')

# print AST

def match(expected):
    global token, tokenString, lineno # return lineno
    if (token == expected):
        token, tokenString = getToken(False)
        #print("TOKEN:", token, lineno)
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        print("      ")


# 1. program → declaration-list
def program():
    root = declarationList()
    return root

# 2. declaration-list → declaration { declaration }
# def declaration_list():
#     subtree = declaration()
    # while token in 

#3. declaration → var-declaration | fun-declaration

# 4. var-declaration → type-specifier ID [ “[“ NUM “]” ]  ;

# def var_declaration():
#     if token==TokenType.INT or token==TokenType.VOID:
#         node = newNode(ExpressionType.TypeSpecifier)
#         node.value = token
#         match(token)
#     match()


#13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt

#15. selection-stmt →  if (expression) statement [ else statement ]
def selection_stmt():
    t = newNode(ExpressionType.If)
    t.value = StatementKind.If
    match(TokenType.IF)
    match(TokenType.L_PAREN)
    t.child[0] = expression()
    match(TokenType.R_PAREN)
    t.child[1] = statement()
    if token==TokenType.ELSE:
        match(TokenType.ELSE)
        t.child[2] = statement()
    return t

# 16. iteration-stmt → while (expression) statement
def iteration_stmt():
    t = newNode(StatementKind.While)
    match(TokenType.WHILE)
    match(TokenType.L_PAREN)
    t.child[0] = expression()
    match(TokenType.R_PAREN)
    t.child[1] = statement()
    return t

# 17. return-stmt → return [ expression ] ; 
def return_statement():
    t = newNode(StatementKind.Return)
    match(TokenType.RETURN)
    # check if expression is next
    if (token == TokenType.L_PAREN) or (token == TokenType.ID) or (token == TokenType.NUM):
        t.child[0] = expression()
    match(TokenType.SEMI)
    return t

# 18. expression →  {  var = }  simple-expression 
def expression():
    t = newNode(ExpressionType.Expr)
    t.value = StatementKind.Expr
    p = None
    b = None
    while (token==TokenType.ID):
    
        p = newNode(ExpressionType.Assign)
        p.child[0] = var()
        p.value = token
        b = p
        match(TokenType.ASSIGN)
    
    t.child[0] = b

    # child[0] could not be present
    if t.child[0] == None:
        t.child[0] = simple_expression()
    else:
        if p!=None:
            p.child[1] = simple_expression()
        # t.child[1] = simple_expression()

    return t
    

# 19. var → ID [ “[“ expression “]” ]
def var():
    t = newNode(ExpressionType.Var)

    # Match the ID (function name)
    if token != TokenType.ID:
        raise SyntaxError("Expected identifier in Var ")
    t.value = tokenString 
    match(TokenType.ID)

    # Check for array declaration
    if token==TokenType.L_BRACKET:
        match(TokenType.L_BRACKET)
        t.child[0] = expression()
        match(TokenType.R_BRACKET)
    
    return t

# 20. simple-expression → additive-expression [ relop additive-expression ]
def simple_expression():
    t = additive_expression()

    if (token==TokenType.LT_OR_EQ) or (token==TokenType.LT) or (token == TokenType.GT) or (token==TokenType.GT_OR_EQ) or (token==TokenType.EQEQ) or (token==TokenType.NOT_EQ):
        p = newNode(ExpressionType.Relop)
        p.value = token
        p.child[0] = t
        t = p
        match(token)
        t.child[1] = additive_expression()
    
    return t


# 22. additive-expression → term { addop term }
def additive_expression():
    t = term()
    while ((token==TokenType.PLUS) or (token==TokenType.MINUS)):
        p = newNode(ExpressionType.Addop)
        p.child[0] = t
        p.value = token
        t = p
        match(token)
        print("this is t: ", t)
        if t != None:
            t.child[1] = term()
    return t

#24. term → factor { mulop factor }
def term():
    t = factor()
    while((token==TokenType.TIMES) or (token==TokenType.OVER)):
        p = newNode(ExpressionType.Mulop)
        p.value = token
        p.child[0] = t
        t = p
        match(token)
        t.child[1] = factor()
    return t

#26. factor → ( expression ) | var | call | NUM
def factor():
    global token, prog, pos
    t = None
    # check if token is number
    if token==TokenType.NUM:
        t = newNode(ExpressionType.Num)
        t.value = int(tokenString)
        match(token)
    elif token == TokenType.ID:
        t = newNode(ExpressionType.Id)
        t.value = tokenString
        match(token)

        # check for call production
        if(token==TokenType.L_PAREN):
            pos-=1
            token=prog[pos]
            t = call()
        else:
            pos-=1
            token=prog[pos]
            t = var()
    # check if token is ( expression )
    elif token == TokenType.L_PAREN:
        match(TokenType.L_PAREN)
        t = expression()
        match(TokenType.R_PAREN)

    return t

#27. call → ID ( args )
def call():
    t = newNode(ExpressionType.Call)
    
    # Match the ID (function name)
    if token != TokenType.ID:
        raise SyntaxError("Expected identifier in function call")
    t.value = tokenString  # Store the function name
    match(TokenType.ID)

    # Match opening parenthesis
    if token != TokenType.L_PAREN:
        raise SyntaxError("Expected '(' in function call")
    match(TokenType.L_PAREN)

     # Parse arguments (args production)
    t.child[0] = args()  # args() will return a list of argument expressions
    
    # Match closing parenthesis
    if token != TokenType.R_PAREN:
        raise SyntaxError("Expected ')' in function call")
    match(TokenType.R_PAREN)
    
    return t

# 28. args → arg-list | empty
def args():
    t = None
    if token != TokenType.R_PAREN:
        t = arg_list()
    return t

# 29. arg-list → expression { , expression }
def arg_list():
    t = expression()
    p = t
    while (token==TokenType.COLON):
        match(TokenType.COLON)
        q = expression()
        p.sibling = q
        p = q
    return t


# main parse method
def parse(imprime = True):
    global token, tokenString
    token, tokenString = getToken(False)
    print(token)
    print(tokenString)
    t = expression()
    if (token != TokenType.ENDFILE):
        SyntaxError("Code ends before file\n")
    if imprime:
        printTree(t)
    return t, Error

# printSpaces indents by printing spaces */
def printSpaces():
    print(" "*indentno, end = "")


def printTree(tree):
    global indentno
    indentno+=2 # INDENT
    if tree != None:
        printSpaces()
        if tree.expression == ExpressionType.Addop:
            print("Addop: ", tree.value) # + | -
        elif tree.expression == ExpressionType.Mulop:
            print("Mulop: ", tree.value) # * | /
        elif tree.expression == ExpressionType.Relop:
            print("Relop: ", tree.value) # <= | < | > | >= | == | !=
        elif tree.expression == ExpressionType.Expr:
            print("Expr: ", tree.value)
        elif tree.expression == ExpressionType.Assign:
            print("Assign: ", tree.value)
        elif tree.expression == ExpressionType.Var:
            print("Var: ", tree.value)
        elif tree.expression == ExpressionType.Num:
            print("Num: ", tree.value) # NUM
        else:
            print("Unrecognized expression type")
        for child in tree.child:
            printTree(child)
    indentno-=2 #UNINDENT



