import os
import logging
import ply.yacc as yacc
from mi_lexer import tokens, reserved, lexer
from mi_tabla_simbolos import SymbolTable
from mi_maquina_virtual import VirtualMachine
from mi_parser import st, build_parser

def invert_dict(d):
    return {v: k for k, v in d.items()}

def run_test(file_path):
    print(f"\n=== Ejecutando prueba: {file_path} ===")
    with open(file_path, 'r') as file:
        data = file.read()
        print(data)
    # Limpiar la tabla de símbolos y pilas antes de cada prueba
    st.clear() 
    parser = build_parser()

    #st.clear()
    parser.parse(data, tracking=True)
    print("stack_operands:", st.stack_operands)
    print("stack_operators:", st.stack_operators)
    print("stack_types:", st.stack_types)
    print("stack_jumps:", st.stack_jumps)
    print("stack_quadruples:", st.stack_quadruples)

    constant_table = invert_dict(st.constant_table)
    print(">>> Cuadruplos generados:")
    for i, q in enumerate(st.stack_quadruples):
        print(i, q)

    vm = VirtualMachine(constant_table)
     
    print("constantes : --------")
    print(constant_table.items())
    for address, value in constant_table.items():
        vm.set_memory(address, value)
 
    # print("------------Dump Memory---------------------------------------------")
    # print(vm.dump_memory())  

    vm.load_quadruples(st.stack_quadruples)
    print("------------Compilador----------------------------------------------------")
    vm.execute()

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    # Lista de archivos de prueba
    test_folder = os.path.join(os.path.dirname(__file__), "pruebas")

    for filename in os.listdir(test_folder):
        if filename.endswith(".txt"):
            path = os.path.join(test_folder, filename)
            try:
                run_test(path)

            except Exception as e:
                print(f"Hay un error en '{filename}': {e}")