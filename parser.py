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
            'print': 'console.log',
            'elif': 'else if',
            'pass': '// empty block'
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

    def get_index_next_breakline(index_start, tokens):
        while index_start < len(tokens):
            if tokens[index_start].type == Token.BREAK_LINE:
                return index_start
            index_start += 1

    def find_end_block(tokens, index_start, indent_level):
        while True:
            index_breakline = get_index_next_breakline(index_start, tokens)
            if index_breakline is not None:
                for id_level in range(indent_level):
                    if index_breakline+id_level+1 < len(tokens) and \
                       tokens[index_breakline+id_level+1].type != Token.INDENT:
                            if tokens[index_breakline+id_level+1].type == Token.BREAK_LINE and id_level == 0:
                               index_breakline = index_breakline+id_level+1
                            else:
                                return index_breakline + indent_level-1
                index_start = index_breakline+1
            else:
                return len(tokens)

    def fix_end(index_end, tokens):
        if index_end != len(tokens):
            tokens.insert(index_end, Token(Token.CLOSE_BRACKETS))
            for _ in range(indent_level-1):
                tokens.insert(index_end, Token(Token.INDENT))
            tokens.insert(index_end, Token(Token.BREAK_LINE))
        else:
            tokens.append(Token(Token.BREAK_LINE))
            for _ in range(indent_level-1):
                tokens.append(Token(Token.INDENT))
            tokens.append(Token(Token.CLOSE_BRACKETS))
            tokens.append(Token(Token.BREAK_LINE))

    _index = 0
    while _index < len(tokens):
        if tokens[_index].type == Token.IDENTIFIER and \
           (tokens[_index].value == 'if' or \
            tokens[_index].value == 'else if' or \
            tokens[_index].value == 'while'):
            fix_header_block(_index, tokens)
            indent_level = get_indent_level(tokens, _index)
            index_end = find_end_block(tokens, _index, indent_level)
            fix_end(index_end, tokens)

        elif tokens[_index].type == Token.IDENTIFIER and \
             tokens[_index].value == 'else':
            tokens[_index+1].type == Token.CLOSE_BRACKETS
            indent_level = get_indent_level(tokens, _index)
            index_end = find_end_block(tokens, _index, indent_level)
            fix_end(index_end, tokens)

        _index +=1
