from enum import Enum

# TreeNode class
class TreeNode:
    def __init__(self):
        self.child = [None]*3
        self.sibling = None
        self.expression = None
        self.value = None
        self.arr_size = None
        self.args_num = None
        self.params_num = None
        self.lineno = None

# TokenType
class TokenType(Enum):
    ENDFILE = '$'
    ERROR = 10
    # reserved words
    IF = 'if'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'
    # multicharacter tokens
    ID = 310
    NUM = 311
    # special symbols
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    OVER = '/'
    LT = '<'
    LT_OR_EQ = '<='
    GT = '>'
    GT_OR_EQ = '>='
    ASSIGN = '='
    EQEQ = '=='
    NOT_EQ = '!='
    SEMI = ';'
    COLON = ','
    L_PAREN = '('
    R_PAREN = ')'
    L_BRACKET = '['
    R_BRACKET = ']'
    L_BRACE = '{'
    R_BRACE = '}'
    COMMENT_START = '/*'
    COMMENT_END = '*/'

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


class StatementKind(Enum):
    While = 'While'
    Return = 'Return'
    If = 'If'
    Expr = 'Expression'
    Compound = 'Compound'
    Call = 'Call'
    Args = 'Arguments'

class DeclarationKind(Enum):
    LocalDeclaration = 'Local'

    
class ExpressionKind(Enum):
    Param = 'Param'
    Params = 'Params'