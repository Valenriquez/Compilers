class SymbolTable:
    def __init__(self):
        self.current_scope = 0
        self.variable_table = VariableTable()
        self.function_directory = FunctionDirectory()

        self.operadores = []
        self.operandos  = []
        self.tipos      = []
        self.saltos     = []
        self.cuadruplos = []

        self.operator_codes = {
            '+': 1, '-': 2, '*': 3, '/': 4,
            '=': 5, '==': 6, '!=': 7,
            '>': 8, '<': 9, '>=': 10, '<=': 11,
        }

    def push_sum(self):
        if len(self.operandos) < 2:
            raise IndexError("Not enough operands to perform addition.")
        right = self.operandos.pop()
        left  = self.operandos.pop()
        self.operadores.append('+')

    def push_factor(self, factor, tipo, is_constant=False):
        if is_constant:
            self.operandos.append(factor)
            self.tipos.append(tipo)
        else:
            var = self.variable_table.get_variable(factor)
            if not var:
                raise NameError(f"Variable '{factor}' not declared.")
            self.operandos.append(var['memory_address'])
            self.tipos.append(var['type'])

    def push_operand(self, address, tipo):
        self.operandos.append(address)
        self.tipos.append(tipo)

    def push_operator(self, op):
        if op not in self.operator_codes:
            raise KeyError(f"Operator '{op}' is not recognized.")
        self.operadores.append(op)

    def add_variable(self, name, var_type, scope=None):
        self.variable_table.add_variable(name, var_type, scope or self.current_scope)

    def get_variable(self, name):
        return self.variable_table.get_variable(name)

    def add_function(self, name, return_type, params):
        self.function_directory.add_function(name, self.current_scope, return_type, params)

    def get_function(self, name):
        return self.function_directory.get_function(name)

 
    def print_variables(self):
        self.variable_table.print_table()

    def print_functions(self):
        self.function_directory.print_directory()


class VariableTable:
    def __init__(self):
        self.table = {}

        self.var_global_int    = 0
        self.var_global_float  = 500
        self.var_global_string = 1000

        self.var_local_int     = 1500
        self.var_local_float   = 2000

        self.var_temp_int      = 2500
        self.var_temp_float    = 3000
        self.var_temp_bool     = 3500

        self.var_const_int     = 4000
        self.var_const_float   = 4500
        self.var_const_string  = 5000

    def add_variable(self, name, var_type, scope):
        if name in self.table:
            raise ValueError(f"Variable '{name}' already declared in this scope.")
        addr = self._allocate_address(var_type, scope)
        self.table[name] = {
            'type': var_type,
            'scope': scope,
            'memory_address': addr
        }

    def get_variable(self, name):
        return self.table.get(name)

    def _allocate_address(self, var_type, scope):
        """Choose the next free address based on type & scope."""
        if scope == 0:   
            if var_type == 'int':
                addr = self.var_global_int;    self.var_global_int += 1
            elif var_type == 'float':
                addr = self.var_global_float;  self.var_global_float += 1
            elif var_type == 'string':
                addr = self.var_global_string; self.var_global_string += 1
            else:
                raise TypeError(f"Unsupported global type '{var_type}'.")
        else:  # local
            if var_type == 'int':
                addr = self.var_local_int;     self.var_local_int += 1
            elif var_type == 'float':
                addr = self.var_local_float;   self.var_local_float += 1
            else:
                raise TypeError(f"Unsupported local type '{var_type}'.")
        return addr

    def print_table(self):
        for name, info in self.table.items():
            print(f"{name:15} | type: {info['type']:6} | scope: {info['scope']:2} | addr: {info['memory_address']}")


class FunctionDirectory:
    def __init__(self):
        self.directory = {}

    def add_function(self, name, scope, return_type, parameters):
        if name in self.directory:
            raise ValueError(f"Function '{name}' already declared.")
        self.directory[name] = {
            'scope':        scope,
            'return_type':  return_type,
            'parameters':   parameters,    
            'local_vars':   {}
        }

    def get_function(self, name):
        return self.directory.get(name)

    def print_directory(self):
        for fn, info in self.directory.items():
            params = ", ".join(f"{n}:{t}" for n, t in info['parameters'])
            print(f"{fn:15} | returns {info['return_type']:6} | params: ({params}) | scope {info['scope']}")

