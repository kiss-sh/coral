from lexer import Token

def ast_to_code(ast):
    code = ''

    if ast.right is not None:
        code += f'{ast.right.data.value}'

    if ast.data.type == Token.EQUAL:
        code += ' = '
    elif ast.data.type == Token.PLUS:
        code += ' + '
    elif ast.data.type == Token.MULTIPLY:
        code += ' * '
    else:
        code += f'{ast.data.value}'

    if ast.left is not None:
        code += ast_to_code(ast.left)

    return code
