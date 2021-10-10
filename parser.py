from lexer import Token

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

def replace_keywords(tokens):
    REPLACE_KEYWORDS = {
            'False': 'false',
            'None': 'null',
            'True': 'true',
            'print': 'console.log'
            }

    for token in tokens:
        if token.type == Token.IDENTIFIER and token.value in REPLACE_KEYWORDS:
            token.value = REPLACE_KEYWORDS[token.value]

def fix_variable_declaration(tokens):
    _index = 0
    while _index < len(tokens):
        if _index-1 >= 0 and \
           tokens[_index].type   == Token.EQUAL and \
           tokens[_index-1].type == Token.IDENTIFIER:
            var_keyword = Token(Token.IDENTIFIER, value='var')
            tokens.insert(_index-1, var_keyword)
            _index += 1
        _index += 1

def fix_code_blocks(tokens):
    _index = 0
    while _index < len(tokens):
        if tokens[_index].type == Token.IDENTIFIER and \
           (tokens[_index].value == 'if' or \
            tokens[_index].value == 'elif' or \
            tokens[_index].value == 'while'):
            tokens.insert(_index+1, Token(Token.OPEN_PARANTHESIS))

            _index2 = _index
            while _index2 < len(tokens):
                if tokens[_index2].type == Token.COLON:
                    tokens[_index2].type = Token.OPEN_BRACKETS
                    tokens.insert(_index2, Token(Token.CLOSE_PARANTHESIS))
                    break
                _index2 += 1

            _index2 = _index
            while _index2 < len(tokens):
                if tokens[_index2].type == Token.OPEN_BRACKETS and \
                   tokens[_index2+1].type == Token.BREAK_LINE:
                    cout_indents = 0
                    _index2 += 2
                    while tokens[_index2].type == Token.INDENT:
                        cout_indents += 1
                        _index2 += 1

                    while True:
                        if tokens[_index2].type == Token.BREAK_LINE:
                            if tokens[_index2+cout_indents-1].type == Token.INDENT:
                                _index2 += 1
                                continue
                            else:
                                for _ in range(cout_indents-1):
                                    tokens.insert(_index2+cout_indents, Token(Token.INDENT))
                                tokens.insert(_index2+cout_indents, Token(Token.CLOSE_BRACKETS))
                                break

                        _index2 += 1

                    break
                else:
                    _index2 += 1
        _index += 1
