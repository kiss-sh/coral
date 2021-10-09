from lexer import Token

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
        elif token.type == Token.BREAK_LINE:
            code += '\n'
        elif idx >= 0 and tokens[idx-1].type == Token.OPEN_PARANTHESIS:
            code += f'{token.value}'
        else:
            code += f' {token.value}'

    return code.strip()
