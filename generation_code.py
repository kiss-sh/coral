from lexer import Token

def ast_to_code(ast):
    code = []

    if ast.right is not None:
        code.append(ast_to_code(ast.right))

    if ast.data.type == Token.EQUAL:
        code.append('=')
    elif ast.data.type == Token.PLUS:
        code.append('+')
    elif ast.data.type == Token.MULTIPLY:
        code.append('*')
    else:
        code.append(f'{ast.data.value}')

    if ast.left is not None:
        code.append(ast_to_code(ast.left))

    return ' '.join(code)
