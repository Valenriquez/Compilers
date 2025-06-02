import ply.lex as lex
from pathlib import Path

# Lista de nombres de tokens
tokens = [
    'ID',          # Identificador (por ejemplo: variable, nombre de función)
    'CTE_STRING',  # Constante de cadena (string) -> "hola", 'mundo'
    'CTE_INT',     # Constante entera -> 123, -5
    'CTE_FLOAT',   # Constante de punto flotante -> 3.14, -0.01
    'PLUS',        # Símbolo de suma: +
    'MINUS',       # Símbolo de resta: -
    'TIMES',       # Símbolo de multiplicación: *
    'DIVIDE',      # Símbolo de división: /
    'EQUALS',      # Símbolo de asignación o comparación: =

    'LPAREN',      # Paréntesis izquierdo: (
    'RPAREN',      # Paréntesis derecho: )
    'SEMICOLON',   # Punto y coma: ;
    'COLON',       # Dos puntos: :
    'COMMA',       # Coma: ,
    'LBRACE',      # Llave izquierda: {
    'RBRACE',      # Llave derecha: }
    'LT',          # Menor que: <
    'GT',          # Mayor que: >
    'NE'           # Diferente de (Not Equal): !=
]
# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'main_course': 'MAIN_COURSE',
    'ending': 'ENDING',
    'my_vars': 'MY_VARS',
    'int': 'INT',
    'float': 'FLOAT',
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE',
    'void': 'VOID',
    'while': 'WHILE',
    'do': 'DO'
}

tokens = tokens + list(reserved.values())

# Expresiones regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LT = r'<'
t_GT = r'>'
t_EQUALS = r'='
t_NE = r'!='
t_COLON = r':'
t_SEMICOLON = r';'
t_COMMA = r','
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Reglas de expresiones regulares con código de acción
def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CTE_STRING(t):
    r'("[^\n"]*")|(\'[^\n\']*\')'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Verificar palabras reservadas
    return t

# Una cadena que contiene caracteres ignorados (espacios y tabulaciones)
t_ignore = ' \t'

def t_COMMENT(t):
    r'\#.*'
    pass
    # No return value. Token discarded

# Definir una regla para nuevas líneas para rastrear los números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla de manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# →  construir lexer  
lexer = lex.lex(debug=True)
# data_path = Path(__file__).with_name("archivo.txt")

# with data_path.open("r", encoding="utf-8") as file:
#     data = file.read()
 
# # lexer.input(data)
# while True:
#     tok = lexer.token()
#     if tok.value == 'ending': 
#         break
#     print("Token: ", tok)

