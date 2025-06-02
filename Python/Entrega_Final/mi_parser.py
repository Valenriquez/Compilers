import ply.yacc as yacc
# →  importar el lexer 
from mi_lexer import tokens, reserved, lexer
# →  archivos
import pickle
# →  paths
from pathlib import Path
# →  ir observando movimientos 
import logging 
# →  entrar
import os

from mi_tabla_simbolos import SymbolTable
from mi_maquina_virtual import VirtualMachine

# →  inicializar la tabla de variables 
st = SymbolTable()

# →  Reglas para definir la precedencia, asociatividad de operadores, y manejar ambigÛedad
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LT', 'GT', 'NE')
)

# →  inicio de reglas gramaticales
def p_program(p):
    'program : PROGRAM ID SEMICOLON a_vars a_funcs MAIN_COURSE body ENDING'
    pass

# →  declarar varibales, podría ser como: ["x:int", "y:float", "z:int"]
# →  the_name = "x"
# →  the_type = "int"
def p_a_vars(p):
    '''a_vars : empty
              | vars'''
    variables_list = p[1]
    for var in variables_list:
        the_name, the_type = var.split(':')
        st.push_variable(the_name, the_type)

# →  declarar varibales
"""
VAR: palabra clave (por ejemplo var)
ID: nombre de variable (ej: x)
COLON: símbolo :
type: el tipo de la variable (int, float, etc.)
SEMICOLON: símbolo ;
list_vars: una lista adicional de variables declaradas después de esta
"""
def p_vars(p):
    '''vars : MY_VARS ID COLON type SEMICOLON list_vars'''
    list_vars = p[6]
    p[0] = (f'{p[2]}:{p[4]}', *list_vars.split(','))

# → convierte a "y:float,z:int" a  ["y:float", "z:int"]
# → Para una variable más en la declaración
""""
p[1] es la variable actual (y).
p[3] es el tipo (float).
p[5] son las variables adicionales que vienen después.
"""
def p_list_vars(p):
    '''list_vars : empty
                 | ID COLON type SEMICOLON list_vars'''
    if len(p) > 2:
        if p[5] != None:
            p[0] = f'{p[1]}:{p[3]},{p[5]}'
        else:
            p[0] = f'{p[1]}:{p[3]}'

# → Agregar tipos de datps
def p_type(p):
    '''type : INT
            | FLOAT'''
    p[0] = p[1]

# → Cuerpo de funciones y del programa principal 
# list_statements: Representa una secuencia de sentencias o declaraciones que se encuentran dentro del bloque.

def p_body(p):
    'body : LBRACE list_statements RBRACE'
    pass

""" 
EJEMPLO
statement: x = 5;
body_rep: y = 6; z = 7;
"""
# →  Manejar la lista de declaraciones
def p_list_statements(p):
    '''list_statements : statement body_rep
                       | empty
                       | statement'''
    pass

# → Manejar declaraciones adicionales en el cuerpo
def p_body_rep(p):
    '''body_rep : statement body_rep
                       | statement'''
    pass

# → Manejar una declaración (asignación, condición, ciclo, llamada a función, impresión)
def p_statement(p):
    '''statement : assignment
                 | condition
                 | do_cycle
                 | cycle
                 | f_call
                 | print_statement'''
    pass

# →  Manejar la declaración de impresión
def p_print_stmt(p):
    'print_statement : PRINT LPAREN list_expresion RPAREN SEMICOLON'
    pass

"""
ID: token a
push_operand: procesa a
EQUALS: token =
add_operador: procesa =
expresion: resuelve b + c, y deja el resultado en los stacks
finalmente: add_assing() genera el cuádruplo final
""" 
def p_assignment(p):
    'assignment : ID push_operand EQUALS add_operador expresion SEMICOLON'
    st.add_assing()
    pass

def p_push_operand(p):
    '''push_operand : '''
    st.push_operand(p[-1])

def p_add_operador(p):
    '''add_operador : '''
    st.push_operador(p[-1])


# →  Manejar la lista de expresiones en una impresión
# para expresion addPrint COMMA list_expresion -> print( X + 2, Y * 3, Z )
# para addPrint sólo para STRINGS o para varios strings ->  CTE_STRING addPrintString, CTE_STRING addPrintString COMMA list_expresion
def p_list_expresion(p):
    '''list_expresion : expresion addPrint
                    | expresion addPrint COMMA list_expresion
                    | CTE_STRING addPrintString
                    | CTE_STRING addPrintString COMMA list_expresion'''
    pass

# →  Operación de impresión, sómo invoca operación de tabla de símbolos
def p_addPrint(p):
    '''addPrint : '''
    st.add_print()

def p_addPrintString(p):
    '''addPrintString : '''
    st.add_print(string=p[-1])


def p_do_cycle(p):
    '''do_cycle : DO cycle_start body WHILE LPAREN expresion RPAREN goto_true'''
    # La primera línea es “while”
    # La segunda línea es tu “do‐while” original
    pass

def p_goto_true(p):
    '''goto_true : '''
    st.add_goto_true_while()

def p_cycle(p):
    '''cycle : WHILE cycle_start LPAREN expresion RPAREN goto_false body generate_goto finish_gotof'''
    pass


def p_goto_false(p):
    '''goto_false : '''
    st.add_goto_false()


def p_generate_goto(p):
    '''generate_goto :'''
    st.add_goto_loop()

def p_finish_gotof(p):
    '''finish_gotof :'''
    st.patch_gotof()


def p_cycle_start(p):
    '''cycle_start : '''
    st.cycle_start()



def p_condition(p):
    'condition : IF LPAREN expresion RPAREN goto_false body else_part'
    st.add_goto_False_fill()


def p_else_part(p):
    '''else_part : ELSE goto body
                 | empty'''
    pass

### SE MANDA A LLAMAR GO TO 
def p_goto(p):
    '''goto : '''
    st.add_goto()

def p_expresion(p):
    '''expresion : exp comparar_exp exp
                | exp'''
    st.add_expresion()

def p_comparar_exp(p):
    '''comparar_exp : LT
                    | GT
                    | NE'''
    st.push_operador(p[1])

def p_exp(p):
    '''exp : termino add_termino 
           | termino add_termino next_termino'''
    pass

def p_add_termino(p):
    '''add_termino : '''
    st.add_termino()

def p_next_termino(p):
    '''next_termino : sum_rest exp '''
    pass

def p_sum_rest(p):
    '''sum_rest : PLUS
                | MINUS'''
    st.push_operador(p[1])
    pass

def p_termino(p):
    '''termino : factor add_factor next_factor
               | factor add_factor'''
    pass

def p_next_factor(p):
    '''next_factor : mult_div termino'''
    pass

def p_mult_div(p):
    '''mult_div : TIMES
                | DIVIDE'''
    st.push_operador(p[1])
    pass

def p_factor(p):
    '''factor : LPAREN expresion RPAREN
              | id_cte'''
    pass

def p_add_factor(p):
    '''add_factor : '''
    st.add_factor()

def p_id_cte(p):
    '''id_cte : ID push_var
              | cte push_const'''
    pass

def p_push_const(p):
    '''push_const : '''
    st.push_operand(p[-1], True)

def p_push_var(p):
    '''push_var : '''
    st.push_operand(p[-1])

def p_cte(p):
    '''cte : CTE_INT
           | CTE_FLOAT'''
    p[0] = p[1]

def p_funcs(p):
    'funcs : VOID ID LPAREN list_parameters RPAREN LBRACE var_no_var body RBRACE SEMICOLON'
    pass

def p_a_funcs(p):
    '''a_funcs : empty
               | funcs b_funcs'''
    pass

def p_b_funcs(p):
    '''b_funcs : funcs b_funcs
                | funcs'''
    pass

def p_list_parameters(p):
    '''list_parameters : empty
                   | ID COLON type more_params'''
    pass

def p_more_params(p):
    '''more_params : empty
                   | COMMA ID COLON type more_params'''
    pass

def p_var_no_var(p):
    '''var_no_var : empty
                  | vars'''
    pass

def p_f_call(p):
    'f_call : ID LPAREN RPAREN SEMICOLON'
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (line {p.lineno})")
    else:
        print("Syntax error at EOF")

# # Construir el parser
def build_parser():
    return yacc.yacc(write_tables=False, debug=False)

