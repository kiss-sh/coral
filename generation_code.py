"""Modulo responsavel por pela geracao do codigo destino
"""

from lexer import Token, SIZE_OF_INDENT

def tokens_to_code(tokens):
    """
    função responsavel por pegar uma lista de tokens e gerar uma string
    com o codigo em que é usado o significado de cada token para gerar o
    codigo correspondente
    """
    code = ''

    for idx, token in enumerate(tokens):
        if token.type == Token.OPEN_PARANTHESIS:
            if idx > 0 and tokens[idx-1].type == Token.IDENTIFIER:
                code += '('
            else:
                code += ' ('

        elif token.type == Token.CLOSE_PARANTHESIS:
            code += ')'
        elif token.type == Token.OPEN_BRACKETS:
            if idx > 0 and tokens[idx-1].type == Token.IDENTIFIER:
                code += '['
            else:
                code += ' ['

        elif token.type == Token.CLOSE_BRACKETS:
            code += ']'
        elif token.type == Token.EQUAL:
            if idx > 0 and tokens[idx-1].type == Token.EQUAL:
                code += '='
            else:
                code += ' ='

        elif token.type == Token.PLUS:
            code += ' +'
        elif token.type == Token.MULTIPLY:
            code += ' *'
        elif token.type == Token.MINUS:
            code += ' -'
        elif token.type == Token.PERCENTAGE:
            code += ' %'
        elif token.type == Token.GREATER_THAN:
            code += ' >'
        elif token.type == Token.LESS_THAN:
            code += ' <'
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

        elif idx > 0 and tokens[idx-1].type == Token.OPEN_BRACKETS:
            code += f'{token.value}'
        elif idx > 0 and tokens[idx-1].type == Token.OPEN_PARANTHESIS:
            code += f'{token.value}'
        else:
            code += f' {token.value}'

    if '\n ' in code:
        code = code.replace('\n ','\n')
    return code.strip()
