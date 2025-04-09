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

b = ' \t\n$'
digit = '0123456789'
alphabet = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ'

# s = '(**/[)!=]/+-/*<56<= ;, 12 >>={}=== $'

s = '''
    int gcd(int u, int v) {
        if (v == 0) return u ;
        else return gcd(v, u-u/v*v);
        /* u-u/v*v == u mod v */
    } $
'''

estado = 0
p = 0

lexema = ''

while(s[p] != '$'):
  c = s[p] # current char
  if c in alphabet:
    col = 0
  elif c in digit:
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
  else:
    col = 19

#   print("estado -> ", estado)
#   print("col -> ", col)

  estado = tabla[estado][col]

#   print("char -> ", c)
#   print("estado -> ",estado)


  if estado == 10:

    if lexema == 'else':
        print(lexema, 'ELSE')
    elif lexema == 'if':
        print(lexema, 'IF')
    elif lexema == 'int':
        print(lexema, 'INT')
    elif lexema == 'return':
        print(lexema, 'RETURN')
    elif lexema == 'void':
        print(lexema, 'VOID')
    elif lexema == 'while':
        print(lexema, 'WHILE')
    else:
        print(lexema, 'ID')

    lexema = ''
    estado = 0
    p-=1
  
  elif estado == 11:
    print(lexema, 'NUM')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 12:
    lexema = c
    print(lexema, 'PLUS')
    lexema = ''
    estado = 0
 
  elif estado == 13:
    lexema = c
    print(lexema, 'MINUS')
    lexema = ''
    estado = 0

  elif estado == 14:
    print(lexema, 'OVER')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 15:
    lexema+=c
    print(lexema, 'COMMENT_START')
    lexema = ''
    estado = 0

  elif estado == 16:
    print(lexema, 'LT')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 17:
    lexema+=c
    print(lexema, 'LT_OR_EQ')
    lexema = ''
    estado = 0

  elif estado == 18:
    print(lexema, 'GT')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 19:
    lexema+=c
    print(lexema, 'GT_OR_EQ')
    lexema = ''
    estado = 0

  elif estado == 20:
    print(lexema, 'ASSIGN')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 21:
    lexema+=c
    print(lexema, 'EQEQ')
    lexema = ''
    estado = 0

  elif estado == 22:
    print(lexema, 'NOT_EQ')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 23:
    lexema = c
    print(lexema, 'SEMICOLON')
    lexema = ''
    estado = 0

  elif estado == 24:
    lexema = c
    print(lexema, 'COLON')
    lexema = ''
    estado = 0

  elif estado == 25:
    lexema = c
    print(lexema, 'L_PAREN')
    lexema = ''
    estado = 0

  elif estado == 26:
    lexema = c
    print(lexema, 'R_PAREN')
    lexema = ''
    estado = 0

  elif estado == 27:
    lexema = c
    print(lexema, 'L_BRACKET')
    lexema = ''
    estado = 0

  elif estado == 28:
    lexema = c
    print(lexema, 'R_BRACKET')
    lexema = ''
    estado = 0
  
  elif estado == 29:
    lexema = c
    print(lexema, 'L_BRACE')
    lexema = ''
    estado = 0
  
  elif estado == 30:
    lexema = c
    print(lexema, 'R_BRACE')
    lexema = ''
    estado = 0

  elif estado == 31:
    print(lexema, 'TIMES')
    lexema = ''
    estado = 0
    p-=1

  elif estado == 32:
    lexema+=c
    print(lexema, 'COMMENT_END')
    lexema = ''
    estado = 0

  elif estado == 33:
    print (' ERROR')
    p += 1

  if estado != 0:
    lexema += c

  p+=1
    

    
  

  