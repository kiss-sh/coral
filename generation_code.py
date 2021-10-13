from lexer import Token, SIZE_OF_INDENT

def tokens_to_code(tokens):
    code = ''

    for idx, token in enumerate(tokens):
        if token.type == Token.OPEN_PARANTHESIS:
            if idx > 0 and tokens[idx-1].type == Token.IDENTIFIER:
                code += '('
            else:
                code += ' ('

        elif token.type == Token.CLOSE_PARANTHESIS:
            code += ')'
        elif token.type == Token.EQUAL:
            if idx > 0 and tokens[idx-1].type == Token.EQUAL:
                code += '='
            else:
                code += ' ='

        elif token.type == Token.PLUS:
            code += ' +'
        elif token.type == Token.MULTIPLY:
            code += ' *'
        elif token.type == Token.COMMA:
            code += ','
        elif token.type == Token.OPEN_KEYS:
            code += ' {'
        elif token.type == Token.CLOSE_KEYS:
            if tokens[idx-1].type == Token.INDENT:
                code += ' }'
            else:
                code += '}'
        elif token.type == Token.BREAK_LINE:
            code += '\n'
        elif token.type == Token.INDENT:
            code += ' ' * SIZE_OF_INDENT

        elif idx > 0 and tokens[idx-1].type == Token.OPEN_PARANTHESIS:
            code += f'{token.value}'
        else:
            code += f' {token.value}'

    if '\n ' in code:
        code = code.replace('\n ','\n')
    return code.strip()
