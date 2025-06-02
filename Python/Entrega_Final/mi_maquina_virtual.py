from typing import Any, Dict, List
from pathlib import Path

class VirtualMachine:
    def __init__(self, const_table):
        self.const_table = const_table
        self.memory = {}

        self.instruction_pointer = 0
        self.var_int = 0
        self.var_float = 100

        self.var_temp_int = 200
        self.var_temp_float = 300
        self.var_temp_bool = 400

        self.var_const_int = 500
        self.var_const_float = 600
        self.var_const_string = 700

        self.initialize_memory()

    def initialize_memory(self):
        segments = [
            (self.var_int, self.var_float, 0),       # global int
            (self.var_float, self.var_temp_int, 0.0),# global float
            (self.var_temp_int, self.var_temp_float, 0),    # temp int
            (self.var_temp_float, self.var_temp_bool, 0.0), # temp float
            (self.var_temp_bool, self.var_const_int, False),# temp bool
            (self.var_const_int, self.var_const_float, 0),  # const int
            (self.var_const_float, self.var_const_string, 0.0), # const float
            (self.var_const_string, self.var_const_string + 50, ""), # const string
        ]

        for start, end, default_value in segments:
            for address in range(start, end):
                self.memory[address] = default_value

    def load_quadruples(self, quadruples):
        # Cargar cuádruplos en la máquina virtual
        self.quadruples = quadruples

    def execute(self):
        # Ejecutar los cuádruplos
        while self.instruction_pointer < len(self.quadruples):
            quad = self.quadruples[self.instruction_pointer]
            op = quad[0]
            left = quad[1]
            right = quad[2]
            result = quad[3]

            if op == '+':
                self.memory[result] = self.memory[left] + self.memory[right]
            elif op == '-':
                self.memory[result] = self.memory[left] - self.memory[right]
            elif op == '*':
                self.memory[result] = self.memory[left] * self.memory[right]
            elif op == '/':
                self.memory[result] = self.memory[left] / self.memory[right]
            elif op == '=':
                self.memory[result] = self.memory[left]
            elif op == '!=':
                self.memory[result] = self.memory[left] != self.memory[right]
            elif op == '>':
                self.memory[result] = self.memory[left] > self.memory[right]
            elif op == '<':
                self.memory[result] = self.memory[left] < self.memory[right]
            elif op == 'GOTO':
                self.instruction_pointer = result
                continue
            elif op == 'GOTOV':   # go-to si Verdadero
                if self.memory[left]:
                    self.instruction_pointer = result
                    continue
            elif op == 'GOTOF':   # go-to si Falso
                if not self.memory[left]:
                    self.instruction_pointer = result
                    continue

            # ––––– Print –––––
            elif op == 'print':
                if isinstance(left, str):
                    print(left)
                else:
                    print(self.memory[left])

            else:
                raise Exception(f"VM: operador desconocido '{op}'")

            # Si no hubo salto, avanzamos al siguiente cuádruplo
            self.instruction_pointer += 1

    def set_memory(self, address, value):
        # Establecer un valor en una dirección de memoria específica
        self.memory[address] = value

    def get_memory(self, address):
        # Obtener el valor de una dirección de memoria específica
        return self.memory.get(address, None)
    
    def dump_memory(self) -> Dict[int, Any]:
        """Para depuración: devuelve copia ordenada de la memoria."""
        return dict(sorted(self.memory.items()))


 
