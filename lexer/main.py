from globalTypes import *
from lexer import *

f = open('sample.c-', 'r')
program = f.read() 		# lee todo el archivo a compilar
f.close()                       # cerrar el archivo con programa fuente
progLong = len(program) 	# longitud original del programa
program = program + '$' 	# agregar un caracter $ que represente EOF
position = 0 			# posición del caracter actual del string
lineno = 1

# función para pasar los valores iniciales de las variables globales
globales(program, position, progLong, lineno) # para mandar los globales

token, tokenString = getToken()
while (token != TokenType.ENDFILE):
    token, tokenString = getToken()
