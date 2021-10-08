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

def tokens_to_code(tokens):
    code = ''

    for idx, token in enumerate(tokens):
        if token.type == Token.OPEN_PARANTHESIS:
            if idx >= 0 and tokens[idx-1].type == Token.IDENTIFIER:
                code += '('
            else:
                code += ' ('

        elif token.type == Token.CLOSE_PARANTHESIS:
            code += ')'
        elif token.type == Token.EQUAL:
            code += ' ='
        elif token.type == Token.PLUS:
            code += ' +'
        elif token.type == Token.MULTIPLY:
            code += ' *'
        elif idx >= 0 and tokens[idx-1].type == Token.OPEN_PARANTHESIS:
            code += f'{token.value}'
        else:
            code += f' {token.value}'

    return code.strip()
