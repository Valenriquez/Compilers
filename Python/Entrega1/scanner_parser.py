import ply.lex as lex
import ply.yacc as yacc

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
    'ID', 'CTE_INT', 'CTE_FLOAT', 'CTE_STRING', 'NE',
] + list(reserved.values())

# literales
literals = [';', ',', ':', '(', ')', '{', '}', '[', ']',
            '+', '-', '*', '/', '>', '<', '=']

# expresiones regulares
t_CTE_STRING = r'"([^\\\n]|(\\.))*?"'

def t_CTE_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_INT(t):
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

# caracteres ignorados
t_ignore = ' \t\r'

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

# Parser
# Reglas para manejar ambigûedad
precedence = (
    ('left', '>', '<', 'NE'),
    ('left', '+', '-'),
    ('left', '*', '/')
)

# Simbolo de comienzo
def p_program(p):
    'program : PROGRAM ID ";" vars funcs MAIN body END'
    p[0] = ('program', p[2], p[4], p[5], p[7])

# Vars - cero o más
def p_vars(p):
    '''vars : VAR id_list ":" type ";" vars
             | empty'''
    if len(p) > 2:
        p[0] = [('var_decl', p[2], p[4])] + p[6]
    else:
        p[0] = []

# Id list
def p_id_list(p):
    '''id_list : ID id_list_tail'''
    p[0] = [p[1]] + p[2]

def p_id_list_tail(p):
    '''id_list_tail : "," ID id_list_tail
                    | empty'''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

# Type

def p_type(p):
    '''type : INT
             | FLOAT'''
    p[0] = p[1]

#  Funciones - cero o más
def p_funcs(p):
    '''funcs : func funcs
             | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Función 
def p_func(p):
    'func : VOID ID "(" params ")" "[" vars body "]" ";"'
    p[0] = ('func', p[2], p[4], p[8], p[9])

#  Parámetros - cero o más
def p_params(p):
    '''params : ID ":" type params_tail
              | empty'''
    if len(p) > 2:
        p[0] = [(p[1], p[3])] + p[4]
    else:
        p[0] = []

def p_params_tail(p):
    '''params_tail : "," ID ":" type params_tail
                   | empty'''
    if len(p) > 2:
        p[0] = [(p[2], p[4])] + p[5]
    else:
        p[0] = []

# Body 
def p_body(p):
    'body : "{" stmt_list "}"'
    p[0] = p[2]

# Statement  - cero o más
def p_stmt_list(p):
    '''stmt_list : statement stmt_list
                  | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Statement tipos
def p_statement(p):
    '''statement : assign
                 | condition
                 | cycle
                 | f_call
                 | print_stmt'''
    p[0] = p[1]

# Assignment
def p_assign(p):
    'assign : ID "=" expression ";"'
    p[0] = ('assign', p[1], p[3])

# Print 
def p_print_stmt(p):
    'print_stmt : PRINT "(" print_list ")" ";"'
    p[0] = ('print', p[3])

def p_print_list(p):
    '''print_list : print_item print_list_tail'''
    p[0] = [p[1]] + p[2]

def p_print_item(p):
    '''print_item : expression
                  | CTE_STRING'''
    p[0] = p[1]

def p_print_list_tail(p):
    '''print_list_tail : "," print_item print_list_tail
                       | empty'''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

# While 
def p_cycle(p):
    'cycle : WHILE "(" expression ")" DO body ";"'
    p[0] = ('while', p[3], p[6])

# If 
def p_condition(p):
    'condition : IF "(" expression ")" body else_part ";"'
    p[0] = ('if', p[3], p[5], p[6])

def p_else_part(p):
    '''else_part : ELSE body
                 | empty'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

# Function 
def p_f_call(p):
    'f_call : ID "(" expr_list ")" ";"'
    p[0] = ('call', p[1], p[3])

def p_expr_list(p):
    '''expr_list : expression expr_list_tail
                 | empty'''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_expr_list_tail(p):
    '''expr_list_tail : "," expression expr_list_tail
                      | empty'''
    if len(p) > 2:
        p[0] = [p[2]] + p[3]
    else:
        p[0] = []

# Expresiones comparativas
def p_expression(p):
    '''expression : simple_expression
                  | simple_expression '>' simple_expression
                  | simple_expression '<' simple_expression
                  | simple_expression NE simple_expression'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('compare', p[2], p[1], p[3])

# Expresiones aritméticas
def p_simple_expression(p):
    '''simple_expression : simple_expression '+' term
                         | simple_expression '-' term
                         | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

# '*' and '/'
def p_term(p):
    '''term : term '*' factor
            | term '/' factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])

# Factor
def p_factor(p):
    '''factor : '(' expression ')'
              | '-' factor
              | '+' factor
              | ID
              | CTE_INT
              | CTE_FLOAT'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] in ('-', '+'):
        p[0] = ('unary', p[1], p[2])
    else:
        p[0] = p[2]

# Empty  
def p_empty(p):
    'empty :'
    p[0] = None

# Error para syntax errors
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} (value={p.value}) at line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Construir el parser
parser = yacc.yacc()

# TEST CASES
if __name__ == '__main__':
    data = '''program example;
      var x, y: int;
      void foo(a: int) [ var z: float; { x = a + z; } ];
      main { print(x, "hello"); }
    end'''
    result = parser.parse(data)
    print(result)

