semantic_cube = {
    'int': {
        'int': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'int',
            '*': 'int',
            '/': 'float',
            '+': 'int',
            '-': 'int',
        },
        'float': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'int',
            '*': 'float',
            '/': 'float',
            '+': 'float',
            '-': 'float',
        },
        'bool': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'int',
            '*': 'int',
            '/': 'int',
            '+': 'int',
            '-': 'int',
        }
    },
    'float': {
        'int': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'float',
            '*': 'float',
            '/': 'float',
            '+': 'float',
            '-': 'float',
        },
        'float': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'float',
            '*': 'float',
            '/': 'float',
            '+': 'float',
            '-': 'float',
        },
        'bool': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'float',
            '*': 'float',
            '/': 'float',
            '+': 'float',
            '-': 'float',
        }
    },
    'bool': {
        'int': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'error',
            '*': 'int',
            '/': 'int',
            '+': 'int',
            '-': 'int',
        },
        'float': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'error',
            '*': 'float',
            '/': 'float',
            '+': 'float',
            '-': 'float',
        },
        'bool': {
            '<': 'bool',
            '>': 'bool',
            '<=': 'bool',
            '>=': 'bool',
            '==': 'bool',
            '!=': 'bool',
            '=': 'error',
            '*': 'int',
            '/': 'int',
            '+': 'int',
            '-': 'int',
        }
    }
}


def semantic_validation(left_operand, right_operand, operator):
    left_parts = left_operand.split('.')
    right_parts = right_operand.split('.')

    if not left_parts or not right_parts:
        raise ValueError(f"Malformed operand(s): '{left_operand}', '{right_operand}'")

    left_type = left_parts[-1]
    right_type = right_parts[-1]

    if operator not in semantic_cube:
        raise ValueError(f"Unknown operator: '{operator}'")

    operator_table = semantic_cube[operator]

    if right_type not in operator_table:
        raise ValueError(f"Operator '{operator}' does not support type '{right_type}' as right operand")

    if left_type not in operator_table[right_type]:
        raise ValueError(f"Operator '{operator}' does not support type '{left_type}' as left operand with right type '{right_type}'")

    result_type = operator_table[right_type][left_type]

    if result_type == 'error':
        print(f"Invalid operation: {right_type} {operator} {left_type}")

    return result_type
