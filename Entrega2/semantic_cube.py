"""
Un cubo semántico es una estructura de datos fundamental
en la fase de análisis semántico de un compilador, 
cuya misión es resolver el tipo de resultado (o detectar errores) 
de aplicar un operador a dos operandos de ciertos tipos. 


TipoResultado = Cube[TipoIzquierdo][TipoDerecho][Operador]

Determinará
- compatibilidad
- tipo de resultado
- detectará errores de combinaciones
"""

class SemanticCube:
    def __init__(self):
        self.types = ['int', 'float', 'bool']
        self.cube = self._build_cube()

    def _build_cube(self):
        cube = {}

        #  aritmetico
        for op in ['+', '-', '*', '/']:
            cube[op] = {
                t1: {
                    t2: self._arithmetic_result(t1, t2)
                    for t2 in self.types
                } for t1 in self.types
            }

        # logico
        for op in ['&&', '||']:
            cube[op] = {
                'bool': {'bool': 'bool'},
                'int': {'int': 'error', 'float': 'error', 'bool': 'error'},
                'float': {'int': 'error', 'float': 'error', 'bool': 'error'}
            }

        # comparacion
        for op in ['==', '!=', '>', '<', '>=', '<=']:
            cube[op] = {
                t1: {
                    t2: 'bool' if t1 == t2 else 'error'
                    for t2 in self.types
                } for t1 in self.types
            }

        return cube

    def _arithmetic_result(self, t1, t2):
        if t1 == 'int' and t2 == 'int':
            return 'int'
        elif t1 in ['int', 'float'] and t2 in ['int', 'float']:
            return 'float'
        else:
            return 'error'

    def get_type(self, op, t1, t2):
        return self.cube.get(op, {}).get(t1, {}).get(t2, 'error')


cube = SemanticCube()
print(cube.get_type('-', 'int', 'float'))   
print(cube.get_type('&&', 'int', 'bool'))  
print(cube.get_type('==', 'float', 'float'))  
