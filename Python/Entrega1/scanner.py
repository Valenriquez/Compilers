import ply.lex as lex

"""
Hice la elección de PLY (Python Lex-Yacc) 
como herramienta para implementar un scanner 
(analizador léxico) y parser (analizador sintáctico)
en el procesamiento de lenguajes. PLY es una 
implementación popular de las herramientas 
tradicionales lex y yacc, adaptada al ecosistema Python.
"""

# Lexer

# Palabras reservadas
reserved = {
    'program': 'PROGRAM',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'void': 'VOID',
    'main': 'MAIN',
    'end': 'END',
    'print': 'PRINT',
    'while': 'WHILE',
    'do': 'DO',
    'if': 'IF',
    'else': 'ELSE'
}

# Tokens
tokens = [
    #NUMBERS
    'CINT',
    'CFLOAT',
    #IDS
    'ID',
    #STRINGS
    'STRING',
    #OPERATORS
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQUALS',
    'GREATER',
    'LESS',
    'NOTEQUAL',
    'COLON',
    'COMMA',
    #SYMBOLS
    'LPAREN',
    'RPAREN',
    'SEMICOLON',
    'LBRACE',
    'RBRACE',
    'LSQUARE',
    'RSQUARE',
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_LBRACE = r'{'
t_RBRACE = r'}'
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_EQUALS = r'='
t_GREATER = r'>'
t_LESS = r'<'
t_NOTEQUAL = r'!='
t_COLON = r':'
t_COMMA = r','

# Define a rule to skip all horizontal whitespace except newlines, so I can still count lines
t_ignore = ' \t\r'

# expresiones regulares
def t_STRING(t):
    r'\'[^\']*\'|\"[^\"]*\"'
    return t

def t_CFLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CINT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# !=
def t_NE(t):
    r'!='
    return t

# identificadores y palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

#lineas nuevas
def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la linea {t.lineno}")
    t.lexer.skip(1)


# Construir lexer
lexer = lex.lex()
data = 'program var x_ = 10.2; end'
lexer.input(data)
while True:
    tok = lexer.token()
    if tok.value == 'end': 
        break
    print(tok)

