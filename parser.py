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
    def fix_header_block(index_keyword, tokens):
        tokens.insert(index_keyword+1, Token(Token.OPEN_PARANTHESIS))

        idx = index_keyword
        while tokens[idx].type != Token.COLON:
            idx += 1
        tokens[idx].type = Token.OPEN_BRACKETS
        tokens.insert(idx, Token(Token.CLOSE_PARANTHESIS))

    def get_indent_level(tokens, index_start):
        while index_start < len(tokens):
            if tokens[index_start].type == Token.BREAK_LINE:
                indent_level = 0
                while tokens[index_start+1].type == Token.INDENT:
                    indent_level += 1
                    index_start += 1
                break
            else:
                index_start += 1

        return indent_level

    def find_end_block(tokens, _index2, indent_level):
        pass

    _index = 0
    while _index < len(tokens):
        if tokens[_index].type == Token.IDENTIFIER and \
           (tokens[_index].value == 'if' or \
            tokens[_index].value == 'elif' or \
            tokens[_index].value == 'while'):
            fix_header_block(_index, tokens)

        _index +=1
