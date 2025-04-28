from globalTypes import *

# function to pass global variables
def globales(prog, pos, long, lineno, lstart = 0, lend = 0):
    global program
    global position
    global programLength
    global lineNumber
    global lineStart
    global lineEnd
    program = prog
    position = pos
    programLength = long
    lineNumber = lineno
    lineStart = lstart
    lineEnd = lend

tabla = [
    [1, 2, 12, 13, 3, 4, 5, 6, 7, 23, 24, 25, 26, 27, 28, 29, 30, 9, 0, 33],
    [1, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 33],
    [11, 2, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 33],
    [14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 14, 15, 14, 33],
    [16, 16, 16, 16, 16, 16, 16, 17, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 16, 33],
    [18, 18, 18, 18, 18, 18, 18, 19, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 33],
    [20, 20, 20, 20, 20, 20, 20, 21, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 33],
    [33, 33, 33, 33, 33, 33, 33, 8, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33, 33],
    [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 33],
    [31, 31, 31, 31, 32, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 31, 33]
]


'''                       
State table

c = [a-zA-Z]
d = [0-9]
b = ' \t\n$'

    0   1   2   3   4   5   6   7   8   9   10  11  12  13  14  15  16  17  18  19

    c   d   +   -   /   <   >   =   !   ;   ,   (   )   [   ]   {   }   *   b   other              
0   1   2   12  13  3   4   5   6   7   23  24  25  26  27  28  29  30  9   0   33
1   1   10  10  10  10  10  10  10  10  10  10  10  10  10  10  10  10  10  10  33
2   11  2   11  11  11  11  11  11  11  11  11  11  11  11  11  11  11  11  11  33
3   14  14  14  14  14  14  14  14  14  14  14  14  14  14  14  14  14  15  14  33
4   16  16  16  16  16  16  16  17  16  16  16  16  16  16  16  16  16  16  16  33
5   18  18  18  18  18  18  18  19  18  18  18  18  18  18  18  18  18  18  18  33
6   20  20  20  20  20  20  20  21  20  20  20  20  20  20  20  20  20  20  20  33
7   33  33  33  33  33  33  33  8   33  33  33  33  33  33  33  33  33  33  33  33
8   22  22  22  22  22  22  22  22  22  22  22  22  22  22  22  22  22  22  22  33
9   31  31  31  31  32  31  31  31  31  31  31  31  31  31  31  31  31  31  31  33      
                                       
'''

# definition for tab, next line and end of program
b = ' \t\n$'

# errors dictionary
errors = {}

# get token function
def getToken(imprime = True):
    global position, lineNumber, lineStart, lineEnd
    tokenString = "" # string for storing token
    currentToken = None # is a TokenType value
    estado = 0
    
    # read next position 
    while(position <= programLength): 
      c = program[position] # current char
      if c.isalpha():
        col = 0
      elif c.isdigit():
        col = 1
      elif c == '+':
        col = 2
      elif c == '-':
        col = 3
      elif c == '/':
        col = 4
      elif c == '<':
        col = 5
      elif c == '>':
        col = 6
      elif c == '=':
        col = 7
      elif c == '!':
        col = 8
      elif c == ';':
        col = 9
      elif c == ',':
        col = 10
      elif c == '(':
        col = 11
      elif c == ')':
        col = 12
      elif c == '[':
        col = 13
      elif c == ']':
        col = 14
      elif c == '{':
        col = 15
      elif c == '}':
        col = 16
      elif c == '*':
        col = 17
      elif c in b:
        col = 18
        if c == '$': # end of program
          currentToken = TokenType.ENDFILE

        # check if there is new line to print errors
        if c == '\n' or c == '$':
          if lineNumber == 1:
            lineStart = 0
          lineEnd = position-1

          # print("line number: ", lineNumber)
          # print("line starts at: ", lineStart)
          # print("char at line start: ", program[lineStart])
          # print("line ends at: ", lineEnd)
          # print("char at line end: ", program[lineEnd])

          if lineNumber in errors.keys():
            s_string = " " * ((lineEnd - lineStart) + 1)

            line_errors = errors[lineNumber]

            print('\n')
            for e in line_errors:
              print(f'Linea {lineNumber}: Caractér Invalido\n')
              print(program[lineStart:lineEnd+1])
              pos = e - lineStart
              tmp = s_string
              s_string = s_string[:pos] + '^' + s_string[pos+1:]
              print(s_string)
              s_string = tmp
              print('\n')

          s_string = ''
          lineStart = position+1
          lineEnd = 0
          lineNumber+=1
      else:
        col = 19

      # update state
      estado = tabla[estado][col]

      # check for different accept states
      if estado == 10:
        if tokenString == 'else':
            currentToken = TokenType.ELSE
        elif tokenString == 'if':
            currentToken = TokenType.IF
        elif tokenString == 'int':
            currentToken = TokenType.INT
        elif tokenString == 'return':
            currentToken = TokenType.RETURN
        elif tokenString == 'void':
            currentToken = TokenType.VOID
        elif tokenString == 'while':
            currentToken = TokenType.WHILE
        else:
            currentToken = TokenType.ID

        estado = 0
        position-=1
      
      elif estado == 11:
        currentToken = TokenType.NUM
        estado = 0
        position-=1

      elif estado == 12:
        tokenString = c
        currentToken = TokenType.PLUS
        estado = 0
    
      elif estado == 13:
        tokenString = c
        currentToken = TokenType.MINUS
        estado = 0

      elif estado == 14:
        currentToken = TokenType.OVER
        estado = 0
        position-=1

      elif estado == 15:
        tokenString+=c
        currentToken = TokenType.COMMENT_START
        estado = 0

      elif estado == 16:
        currentToken = TokenType.LT
        estado = 0
        position-=1

      elif estado == 17:
        tokenString+=c
        currentToken = TokenType.LT_OR_EQ
        estado = 0

      elif estado == 18:
        currentToken = TokenType.GT
        estado = 0
        position-=1

      elif estado == 19:
        tokenString+=c
        currentToken = TokenType.GT_OR_EQ
        estado = 0

      elif estado == 20:
        currentToken = TokenType.ASSIGN
        estado = 0
        position-=1

      elif estado == 21:
        tokenString+=c
        currentToken = TokenType.EQEQ
        estado = 0

      elif estado == 22:
        currentToken = TokenType.NOT_EQ
        estado = 0
        position-=1

      elif estado == 23:
        tokenString = c
        currentToken = TokenType.SEMI
        estado = 0

      elif estado == 24:
        tokenString = c
        currentToken = TokenType.COLON
        estado = 0

      elif estado == 25:
        tokenString = c
        currentToken = TokenType.L_PAREN
        estado = 0

      elif estado == 26:
        tokenString = c
        currentToken = TokenType.R_PAREN
        estado = 0

      elif estado == 27:
        tokenString = c
        currentToken = TokenType.L_BRACKET
        estado = 0

      elif estado == 28:
        tokenString = c
        currentToken = TokenType.R_BRACKET
        estado = 0
      
      elif estado == 29:
        tokenString = c
        currentToken = TokenType.L_BRACE
        estado = 0
      
      elif estado == 30:
        tokenString = c
        currentToken = TokenType.R_BRACE
        estado = 0

      elif estado == 31:
        currentToken = TokenType.TIMES
        estado = 0
        position-=1

      elif estado == 32:
        tokenString+=c
        currentToken = TokenType.COMMENT_END
        estado = 0

      # check error state
      elif estado == 33:
        currentToken = TokenType.ERROR

        # add error position to errors dictionary
        if lineNumber not in errors.keys():
          arr = []
          arr.append(position)
          errors[lineNumber] = arr
        else:
          arr = errors[lineNumber]
          arr.append(position)  
          errors[lineNumber] = arr    

        position += 1
        estado = 0

      # build token String
      if estado != 0:
        tokenString += c

      # move to next pos
      position+=1

      # print if currentToken has value
      if currentToken is not None:
            if imprime:
                print("(", currentToken , ",",f'"{" " if currentToken is TokenType.ERROR else tokenString}"', ")")
            return currentToken, tokenString

          
def peek():
    global position, program, programLength, lineNumber, lineStart, lineEnd
    # Save current state
    saved_pos = position
    saved_lineNumber = lineNumber
    saved_lineStart = lineStart
    saved_lineEnd = lineEnd
    
    # Get the next token (without printing)
    next_token, next_tokenString = getToken(imprime=False)
    
    # Restore state (so the actual token consumption isn't affected)
    position = saved_pos
    lineNumber = saved_lineNumber
    lineStart = saved_lineStart
    lineEnd = saved_lineEnd
    
    return next_token


        
      

      