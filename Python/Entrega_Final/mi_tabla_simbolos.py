from mi_cubo_semantico import semantic_validation
from typing import Any, Dict, List
from pprint import pprint


class SymbolTable:

    def __init__(self):
        self.var_table = {}
        self.constant_table = {}

        self.semantic_cube = semantic_validation
        self.var_int = 0
        self.var_float = 100

        self.var_temp_int = 200
        self.var_temp_float = 300
        self.var_temp_bool = 400

        self.var_const_int = 500
        self.var_const_float = 600
        self.var_const_string = 700

        self.stack_operators = []
        self.stack_operands = []
        self.stack_types = []
        self.stack_jumps = []
        self.stack_quadruples = []
    
    def clear(self):
        # Resetear todos los stacks 
        self.var_table.clear()
        self.stack_operands.clear()
        self.stack_operators.clear()
        self.stack_types.clear()
        self.stack_jumps.clear()
        self.stack_quadruples.clear()
        self.constant_table.clear()

    def debug_stacks(self, etapa: str = ""):
        print(f"\n🧠 Estado de stacks {etapa}:")
        print(f"  🧱 Operandos     : {self.stack_operands}")
        print(f"  🧱 Tipos         : {self.stack_types}")
        print(f"  🔧 Operadores    : {self.stack_operators}")
        print(f"  🔁 Saltos        : {self.stack_jumps}")
        print(f"  🧾 Cuádruplos    :")
        for i, quad in enumerate(self.stack_quadruples):
            print(f"     {i}: {quad}")


    def push_operador(self, operator):
        # Añadir un operador a la pila de operadores
        self.stack_operators.append(operator)
        self.debug_stacks("después de push_operador")

    def push_variable(self, name, var_type):
        # Añadir una variable a la tabla de variables
        if name in self.var_table:
            raise ValueError(f"Variable '{name}' already exists in the var_table.")
        self.var_table[name] = {'type': var_type, 'memory_address': 0}
        self.add_memory_address(name)
        self.debug_stacks("después de push_variable")

    def get_variable(self, name):
        # Obtener una variable de la tabla de variables
        return self.var_table.get(name, None)
        self.debug_stacks("después de get_variable")

    def add_memory_address(self, name):
        # Añadir una dirección de memoria a la variable
        if self.var_table[name]['type'] == 'int':
            memory_address = self.var_int
            self.var_int += 1
        elif self.var_table[name]['type'] == 'float':
            memory_address = self.var_float
            self.var_float += 1
        self.var_table[name]['memory_address'] = memory_address

    def print_table(self):
        # Imprimir la tabla de variables
        for var_name, details in self.var_table.items():
            print(f"Variable: {var_name}, Type: {details['type']}")
            

    def push_operand(self, operand, is_cte=False):
        # Añadir un operando a la pila de operandos
        try:
            if is_cte:
                # Añadir la dirección de memoria de la constante
                tipo = type(operand).__name__
                if tipo == 'int':
                    if operand not in self.constant_table:
                        self.var_const_int += 1
                        self.constant_table[operand] = self.var_const_int

                    self.stack_operands.append(self.constant_table[operand])
                    self.stack_types.append(tipo)
                    self.debug_stacks("push_operand: int")

                elif tipo == 'float':
                    if operand not in self.constant_table:
                        self.var_const_float += 1
                        self.constant_table[operand] = self.var_const_float
                    self.stack_operands.append(self.constant_table[operand])
                    self.stack_types.append(tipo)
                    self.debug_stacks("push_operand: float")
            else:
                # Añadir la dirección de memoria de la variable
                variable = self.get_variable(operand)
                if variable is None:
                    raise KeyError(f"Variable '{operand}' was not declared.")
                tipo = variable["type"]
                dir_memoria = variable['memory_address']
                self.stack_operands.append(dir_memoria)
                self.stack_types.append(tipo)
                self.debug_stacks("not cte")
        except:
            raise KeyError(f"Variable '{operand}' was not declared.")

    def add_factor(self):
        # Añadir un factor (multiplicación o división)
        if self.stack_operators:
            op = self.stack_operators[-1]
            if op == '*' or op == '/':
                right_operand = self.stack_operands.pop()
                left_operand = self.stack_operands.pop()
                right_operand_tipo = self.stack_types.pop()
                left_operand_tipo = self.stack_types.pop()
                operator = self.stack_operators.pop()

                res_tipo = self.semantic_cube(operator, left_operand_tipo, right_operand_tipo)
                if res_tipo == 'error':
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")

                elif res_tipo == 'int':
                    res_address = self.var_temp_int
                    self.stack_operands.append(res_address)
                    self.var_temp_int += 1
                    self.stack_types.append(res_tipo)
                    self.stack_quadruples.append([operator, left_operand, right_operand, res_address])
                    self.debug_stacks("add_factor: int")
                elif res_tipo == 'float':
                    res_address = self.var_temp_float
                    self.stack_operands.append(res_address)
                    self.var_temp_float += 1
                    self.stack_types.append(res_tipo)
                    self.stack_quadruples.append([operator, left_operand, right_operand, res_address])
                    self.debug_stacks("add_facto:float")

    def add_termino(self):
        # Añadir un término (suma o resta)
        if self.stack_operators:
            op = self.stack_operators[-1]
            if op == '+' or op == '-':
                right_operand = self.stack_operands.pop()
                left_operand = self.stack_operands.pop()
                right_operand_tipo = self.stack_types.pop()
                left_operand_tipo = self.stack_types.pop()
                operator = self.stack_operators.pop()

                res_tipo = self.semantic_cube(operator, left_operand_tipo, right_operand_tipo)
                if res_tipo == 'error':
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")

                elif res_tipo == 'int':
                    res_address = self.var_temp_int
                    self.stack_operands.append(res_address)
                    self.var_temp_int += 1
                    self.stack_types.append(res_tipo)
                    self.stack_quadruples.append([operator, left_operand, right_operand, res_address])
                    self.debug_stacks("add_termino: int")
                elif res_tipo == 'float':
                    res_address = self.var_temp_float
                    self.stack_operands.append(res_address)
                    self.var_temp_float += 1
                    self.stack_types.append(res_tipo)
                    self.stack_quadruples.append([operator, left_operand, right_operand, res_address])
                    self.debug_stacks("add_termino: float")

    def add_expresion(self):
        # Añadir una expresión (comparación)
        if self.stack_operators:
            op = self.stack_operators[-1]
            if op == '>' or op == '<' or op == '!=':
                right_operand = self.stack_operands.pop()
                left_operand = self.stack_operands.pop()
                right_operand_tipo = self.stack_types.pop()
                left_operand_tipo = self.stack_types.pop()
                operator = self.stack_operators.pop()

                res_tipo = self.semantic_cube(operator, left_operand_tipo, right_operand_tipo)
                if res_tipo == 'bool':
                    self.var_temp_bool += 1
                    res_address = self.var_temp_bool
                    self.stack_operands.append(res_address)
                    self.stack_types.append(res_tipo)
                    self.stack_quadruples.append([operator, left_operand, right_operand, res_address])
                    self.debug_stacks("if bool add_expresion")
                else:
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")

    def add_assing(self):
        # Añadir una asignación
        if self.stack_operators:
            op = self.stack_operators[-1]
            if op == '=':
                right_operand, right_operand_tipo = self.stack_operands.pop(), self.stack_types.pop()
                left_operand, left_operand_tipo = self.stack_operands.pop() , self.stack_types.pop()
                operator = self.stack_operators.pop()

                res_tipo = self.semantic_cube(operator, left_operand_tipo, right_operand_tipo)
                self.debug_stacks("add_assing")

                if res_tipo != 'error':
                    self.stack_quadruples.append([operator, right_operand, None, left_operand])
                else:
                    raise ValueError(f"Invalid operation: {left_operand_tipo} {operator} {right_operand_tipo}")

    def add_print(self, string=[]):
        # Añadir una operación de impresión
        if string == []:
            right_operand = self.stack_operands.pop()
            right_operand_tipo = self.stack_types.pop()
            self.stack_quadruples.append(['print', right_operand, None, None])
        else:
            self.stack_quadruples.append(['print', string, None, None])

    def add_goto_false(self):
        # Añadir una instrucción GOTOF
        print("add_goto_false ----> ", self.stack_operands, self.stack_types)
        condition = self.stack_operands.pop()
        condition_type = self.stack_types.pop()

        if condition_type != 'bool':
            raise ValueError("Condition for if statement must be a boolean")

        self.stack_quadruples.append(['GOTOF', condition, None, None])
        self.stack_jumps.append(len(self.stack_quadruples) - 1)
        self.debug_stacks("add_goto_false")

    

    def add_goto(self):
        # Añadir una instrucción GOTO
        self.stack_quadruples.append(['GOTO', None, None, None])
        false_jump = self.stack_jumps.pop()

        self.stack_jumps.append(len(self.stack_quadruples) - 1)
        # Actualiza el ultimo campo, el destino del salto 
        self.stack_quadruples[false_jump][-1] = len(self.stack_quadruples)
        self.debug_stacks("add_goto")


    def add_goto_False_fill(self):
        # Completar una instrucción GOTO
        false_jump = self.stack_jumps.pop()
        self.stack_quadruples[false_jump][-1] = len(self.stack_quadruples)
        self.debug_stacks("add_goto_False_fill")


    def cycle_start(self):
        # puntero para luego regresarse 
        # Marcar el inicio del ciclo while
        self.stack_jumps.append(len(self.stack_quadruples))
        self.debug_stacks("cycle_start")

    
    def add_goto_true_while(self):
        # Añadir una instrucción GOTOV para el ciclo while
        condition = self.stack_operands.pop()
        condition_type = self.stack_types.pop()
        
        if condition_type != 'bool':
            raise ValueError("Condition for while statement must be a boolean")

        direccion_salto = self.stack_jumps.pop()
        self.stack_quadruples.append(['GOTOV', condition, None, direccion_salto])
        self.debug_stacks("add_goto_true_while")



    def add_goto_loop(self):
        # Recuperamos la “etiqueta_inicio” que guardamos en cycle_start()
        etiqueta_inicio = self.stack_jumps.pop() - 1   # esta stack_jumps era la primera que ingresó cycle_start()
        # Insertamos el GOTO
        self.stack_quadruples.append(['GOTO', None, None, etiqueta_inicio])
        # Ahora “etiqueta_fin” = len(cuadruplos) (la posicion a parchear)
        self.debug_stacks("add_goto_loop")


    def patch_gotof(self):
        self.debug_stacks("antes de: patch_gotof")

        # Recuperamos la posición del GOTOF que creamos en add_gotof_placeholder()
        pos_gotof = self.stack_jumps.pop() + 1
        # “etiqueta_fin” es la posición actual (primer cuadruplo fuera del cuerpo)
        etiqueta_fin = len(self.stack_quadruples)
        # Reemplazamos el “None” del destino con esa etiqueta
        self.stack_quadruples[pos_gotof][3] = etiqueta_fin
        self.debug_stacks("despues de: patch_gotof")

