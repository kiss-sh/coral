from lexer import Token


REPLACE_KEYWORDS = {
        'False': 'false',
        'None': 'null',
        'True': 'true',
        'print': 'console.log'
        }

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

def replace_keywords(tokens):
    for token in tokens:
        if token.type == Token.IDENTIFIER and token.value in REPLACE_KEYWORDS:
            token.value = REPLACE_KEYWORDS[token.value]

def fix_variable_declaration(tokens):
    _index = 0
    while _index < len(tokens)-1:
        if _index-1 >= 0 and \
           tokens[_index].type   == Token.EQUAL and \
           tokens[_index-1].type == Token.IDENTIFIER:
            var_keyword = Token(Token.IDENTIFIER, value='var')
            tokens.insert(_index-1, var_keyword)
            _index += 1
        _index += 1
