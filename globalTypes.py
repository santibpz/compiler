from enum import Enum

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

class StatementKind(Enum):
    While = 'While'
    Return = 'Return'
    If = 'If'
    Expr = 'Expression'