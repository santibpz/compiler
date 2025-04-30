# grammar implementation for c-

from lexer import *
from globalTypes import *
from enum import Enum


token = None # holds current token
tokenString = None # holds the token string value 
Error = False
lineno = 1
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
    Args = 12 # Arguments
    Return = 13 # Return
    VarDeclaration = 14 # var declaration
    Param = 15 # param
    Statement = 16 # statement
    Declaration = 17
    FunDeclaration = 18
    LocalDeclaration = 19
    While = 20

# TreeNode class
class TreeNode:
    def __init__(self):
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
    print(">>> Syntax error at line " + str(lineno) + ": " + errorMessage, end='')


def match(expected):
    global token, tokenString, lineno # return lineno
    if token == TokenType.COMMENT_START:
        handle_comment()
    if (token == expected):
        token, tokenString, lineno = getToken(False)
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        print("      ")

def handle_comment():
    global token, tokenString, lineno
    while (token!=TokenType.COMMENT_END):
        token, tokenString, lineno = getToken(False)
    token, tokenString, lineno = getToken(False)


# 1. program → declaration-list
def program():
    t = declaration_list()
    return t

# 2. declaration-list → declaration { declaration }
def declaration_list():
    t = declaration()
    if t!=None:
        p = t
        while(token != TokenType.ENDFILE and token != TokenType.SEMI and token != TokenType.R_BRACE):
            q = declaration()
            p.sibling = q
            p = q
    return t

#3. declaration → var-declaration | fun-declaration
def declaration():
    t = None
    
    next_token = peek(2)

    if next_token == TokenType.L_PAREN:
        t = fun_declaration()
    elif next_token == TokenType.SEMI or next_token == TokenType.L_BRACKET:
        t = var_declaration()
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        print("      ")
    return t



# 4. var-declaration → type-specifier ID [ “[“ NUM “]” ]  ;
def var_declaration():
    t = newNode(ExpressionType.VarDeclaration)
    
    if token == TokenType.INT:
        match(TokenType.INT)
    elif token == TokenType.VOID:
        match(TokenType.VOID)
    
    t.value = tokenString
    match(TokenType.ID)

    if token == TokenType.L_BRACKET:
        match(TokenType.L_BRACKET)
        match(TokenType.NUM)
        match(TokenType.R_BRACKET)
    
    match(TokenType.SEMI)
    
    return t

# 6. fun-declaration → type-specifier ID ( params )  compound-stmt
def fun_declaration():
    t = newNode(ExpressionType.FunDeclaration)
    
    if token == TokenType.INT:
        match(TokenType.INT)
    elif token == TokenType.VOID:
        match(TokenType.VOID)
    
    t.value = tokenString
    match(TokenType.ID)

    match(TokenType.L_PAREN)

    t.child[0] = params()

    match(TokenType.R_PAREN)

    t.child[1] = compound_stmt()

    return t

# 7. params → params-list | void
def params():
    t = None
    if token == TokenType.VOID or TokenType.INT:
        next_token = peek()
        if next_token == TokenType.ID:
            t = params_list()
        else:
            if token == TokenType.VOID:
                match(TokenType.VOID)
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        print("      ")

    return t

# 8. params-list → param  { , param }
def params_list():
    t = param()
    a = t
    p = None
    while token == TokenType.COLON:
        match(TokenType.COLON)
        p = param()
        t.sibling = p
        t = p
    return a

# 9. param → type-specifier ID [ “[“ “]” ]
def param():
    t = newNode(ExpressionType.Param)
    t.value = tokenString
    if token == TokenType.INT:
        match(TokenType.INT)
    elif token == TokenType.VOID:
        match(TokenType.VOID)
    match(TokenType.ID)
    if(token==TokenType.L_BRACKET):
        match(TokenType.L_BRACKET)
        match(TokenType.R_BRACKET)
    return t

# 10. compound-stmt →  “{“ local-declarations statement-list “}”
def compound_stmt():
    t = None
    match(TokenType.L_BRACE)
    t = local_declarations()
    if t != None:
        t.sibling = statement_list()
    else :
        t = statement_list()
    match(TokenType.R_BRACE)

    return t

# 11. local-declarations → empty { var-declaration }	
def local_declarations():
    t = None
    l = newNode(DeclarationKind.LocalDeclaration)
    while token == TokenType.INT or token == TokenType.VOID:
        q = var_declaration()
        if t != None:
            t.sibling = q
            t = q
        else:
            t = q
            l.child[0] = t
    
    if l.child[0] == None:
        l = None

    return l

# 12. statement-list → empty { statement }
def statement_list():
    t = None
    s = None
    while (token != TokenType.R_BRACE):
        q = statement()
        if s == None:
            s = t = q
        else:
            t.sibling = q
            t = q

    return s

#13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
def statement():
    t = None
    # compound statement
    if token == TokenType.L_BRACE:
        t = compound_stmt()
    # selection statement
    elif token == TokenType.IF:
        t = selection_stmt()
    # iteration statement
    elif token == TokenType.WHILE:
        t = iteration_stmt()
    # return statement
    elif token == TokenType.RETURN:
        t = return_stmt()
    # expression statement
    elif token == TokenType.SEMI or token == TokenType.L_PAREN or token == TokenType.ID or token == TokenType.NUM:
        t = expression_stmt()
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        print("      ")
    
    return t

# 14. expression-stmt → [ expression ] ; 
def expression_stmt():
    t = None
    if token != TokenType.SEMI:
        t = expression()
    match(TokenType.SEMI)
    return t

#15. selection-stmt →  if (expression) statement [ else statement ]
def selection_stmt():
    t = newNode(ExpressionType.If)
    t.value = tokenString
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
    t = newNode(ExpressionType.While)
    t.value = tokenString
    match(TokenType.WHILE)
    match(TokenType.L_PAREN)
    t.child[0] = expression()
    match(TokenType.R_PAREN)
    t.child[1] = statement()
    return t

# 17. return-stmt → return [ expression ] ; 
def return_stmt():
    t = newNode(ExpressionType.Return)
    t.value = tokenString
    match(TokenType.RETURN)
    # check if expression is next
    if (token == TokenType.L_PAREN) or (token == TokenType.ID) or (token == TokenType.NUM):
        t.child[0] = expression()
    match(TokenType.SEMI)
    return t

# 18. expression →  {  var = }  simple-expression 
def expression():
    t = None

    next_token = peek()

    if next_token != TokenType.ASSIGN:
        t = simple_expression()
    else: 
        a = None
        b = None
        while (token==TokenType.ID):
            next_token = peek()
            if next_token == TokenType.ASSIGN:
                p = newNode(ExpressionType.Assign)
                p.child[0] = var()
                p.value = tokenString
                if a != None:
                    a.child[1] = p
                    a = p
                else:
                    a = p
                    b = a
                match(TokenType.ASSIGN)
            else:
                break

        if b!=None:
            a.child[1] = simple_expression()
            t = b
        
    return t
    

# 19. var → ID [ “[“ expression “]” ]
def var():
    t = newNode(ExpressionType.Var)
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
        p.value = tokenString
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
        p.value = tokenString
        t = p
        match(token)
        if t != None:
            t.child[1] = term()
    return t

#24. term → factor { mulop factor }
def term():
    t = factor()
    while((token==TokenType.TIMES) or (token==TokenType.OVER)):
        p = newNode(ExpressionType.Mulop)
        p.value = tokenString
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
        next_token = peek()
        # check for call production
        if next_token==TokenType.L_PAREN:
            t = call()
        else:
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
    t.value = tokenString
    match(TokenType.ID)
    match(TokenType.L_PAREN)
    if token != TokenType.R_PAREN:
        t.child[0] = args()

    match(TokenType.R_PAREN)
    
    return t

# 28. args → arg-list | empty
def args():
    t = None
    if token != TokenType.R_PAREN:
        t = newNode(ExpressionType.Args)
        t.value = StatementKind.Args
        t.child[0] = arg_list()
    
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
    global token, tokenString, lineno
    token, tokenString, lineno = getToken(False)
    t = program()
    if (token != TokenType.ENDFILE):
        SyntaxError("Code ends before file\n")
    if imprime:
        printTree(t)
    return t, Error

# printSpaces indents by printing spaces */
def printSpaces():
    print(" "*indentno, end = "")


def printTree(tree, sameLevel=False):
    global indentno

    indentno+=2 # INDENT
    
    if tree != None:

        if sameLevel:
            indentno-=2
        
        printSpaces()
        if tree.expression == ExpressionType.Addop:
            print("Addop: ", tree.value) # + | -
        elif tree.expression == ExpressionType.Mulop:
            print("Mulop: ", tree.value) # * | /
        elif tree.expression == ExpressionType.Relop:
            print("Relop: ", tree.value) # <= | < | > | >= | == | !=
        elif tree.expression == ExpressionType.Assign:
            print("Assign: ", tree.value)
        elif tree.expression == ExpressionType.Var:
            print("Var: ", tree.value)
        elif tree.expression == ExpressionType.Return:
            print("Return: ", tree.value)
        elif tree.expression == ExpressionType.FunDeclaration:
            print("fn_declaration: ", tree.value)
        elif tree.expression == ExpressionType.VarDeclaration:
            print("var_declaration: ", tree.value)
        elif tree.expression == ExpressionType.If:
            print("If: ", tree.value)
        elif tree.expression == ExpressionType.While:
            print("While: ", tree.value)
        elif tree.expression == ExpressionType.Call:
            print("Call: ", tree.value)
        elif tree.expression == ExpressionType.Args:
            print("Arguments",)
        elif tree.expression == DeclarationKind.LocalDeclaration:
            print("local_declaration")
        elif tree.expression == ExpressionType.Param:
            print("Param: ", tree.value)
        elif tree.expression == ExpressionType.Num:
            print("Num: ", tree.value) # NUM
        else:
            print("Unrecognized expression type")

        for child in tree.child:
            printTree(child)
        if tree.sibling != None:
            printTree(tree.sibling, True)
            indentno+=2
        
    indentno-=2 #UNINDENT
