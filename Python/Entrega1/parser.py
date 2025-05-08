import ply.yacc as yacc
from scanner import tokens

"""
Un AST (Abstract Syntax Tree, 
o Árbol de Sintaxis Abstracta) es una 
estructura de datos en forma de árbol que 
representa la estructura lógica de un programa, 
despojando los detalles puramente sintácticos
(como paréntesis extra, puntos y comas,
comentarios) y quedándose solo con los elementos
significativos.
"""

# Parser
# Reglas para manejar ambigûedad
precedence = (
    ('left', '>', '<', 'NE'),
    ('left', '+', '-'),
    ('left', '*', '/')
)

"""
Programa id ; main Body end
Programa id VARS main Body end 
Programa id VARS FUNCS* main Body end 

#Body 
{ STATEMENT }
"""

# Simbolo de comienzo
def p_program(p):
    'program : PROGRAM ID ";" vars funcs MAIN body END'
    p[0] = ('programa',   # etiqueta del nodo raíz
    p[2],         # nombre del programa
    p[4],         # lista de vars
    p[5],         # lista de funcs
    p[7])         # cuerpo (sentencias)


"""
Pueden ser varios IDS vara las variables
"""
def p_id_list(p):
    'id_list : ID id_list_tail'
    # p[1]: El primer id, como el token ID
    # lo que devuelve el id_list_tail
    #  p[0] = [ p[1] ] + p[2]
    p[0] = [ p[1] ] + p[2]

def p_id_list_tail(p):
    '''id_list_tail : ',' ID id_list_tail | empty'''
    if len(p) == 4:
        p[0] = [ p[2] ] + p[3]  # p[2] es el siguiente ID, p[3] es la lista restante
    else:
        p[0] = []
        
"""
var id : TYPE ;
var id ,* id : TYPE ;
var id ,* id : TYPE ;  id ,* id : TYPE ;*
"""
# var id ,* id : TYPE ;
# ----------------
# 2) var_decl: id_list ':' TYPE
# ----------------
def p_var_decl(p):
    'var_decl : id_list COLON TYPE'
    # build a tuple or AST node however you like:
    p[0] = ('var_decl', p[1], p[3])

# ----------------
# 3) var_decls: var_decl ';' ( var_decl ';' )* 
# ----------------
def p_var_decls(p):
    '''var_decls : var_decl ';'
                 | var_decl ';' var_decls'''
    if len(p) == 3:
        # only one declaration
        p[0] = [ p[1] ]
    else:
        # one declaration + the rest
        p[0] = [ p[1] ] + p[3]

# ----------------  
# 4) vars: the whole block introduced by the keyword VAR
# ----------------
def p_vars(p):
    'vars : VAR var_decls'
    p[0] = p[2]

# ----------------
# 5) empty rule (for optional parts)
# ----------------
def p_empty(p):
    'empty :'
    p[0] = None

"""
TYPE =  int or float
"""
# Type 
def p_type(p):
    '''type : INT
             | FLOAT'''
    p[0] = ('type', p[1])

"""
FUNCS = VOID ID (F') [V' BODY] ;
F' = ID : TYPE F'' F''' or empty
F'' = , or empty
F''' = id : TYPE F'' F'''  or empty
V' = VARS V' or empty
"""
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

"""
BODY = { S' }
S' = STATEMENTS or empty
"""
# Body 
def p_body(p):
    'body : "{" stmt_list "}"'
    p[0] = p[2]

"""
STATEMENT ... 
| assign
| condition
| cycle
| f_call
| print_stmt
"""
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

"""
ASSIGN = id = EXPRESSION ;
"""
# Assignment
def p_assign(p):
    'assign : ID "=" expression ";"'
    p[0] = ('assign', p[1], p[3])

# Print 
"""
PRINT = PRINT ( P' ) ;
P' = EXPRESSION P'' 
P'' = , C' or empty 
C' CTE.STRING or empty 
"""
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

"""
CYCLE ...
WHILE ( EXPRESSION ) do CUERPO ;
"""
def p_cycle(p):
    'cycle : WHILE "(" expression ")" DO body ";"'
    p[0] = ('while', p[3], p[6])

"""
CONDITION ...
IF ( EXPRESSION ) BODY C' ;
C ' = else BODY or empty
"""
def p_condition(p):
    'condition : IF "(" expression ")" body else_part ";"'
    p[0] = (
        'if',  
        p[3],  # expression 
        p[5],  # body 
        p[6])  # else part 

def p_else_part(p):
    '''else_part : ELSE body
                 | empty'''
    if len(p) > 2:
        p[0] = p[2]
    else:
        p[0] = None

"""
F CALL ...
ID ( F' ) ;
F' = EXPRESSION F'' or empty 
F'' = , EXPRESSION F'' or empty
"""
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
        p[0] = (p[2], p[1], p[3])

# '*' and '/'
def p_term(p):
    '''term : term '*' factor
            | term '/' factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ('binop', p[2], p[1], p[3])


"""
FACTOR ... 
F ' or  ( EXPRESSION )
F ' = + or - F' F'' 
F'' = ID or CTE
"""
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

# Si usas la función tokenize() que te propuse:



# Construir el parser
parser = yacc.yacc()
