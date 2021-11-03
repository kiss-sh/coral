from lexer import Token

def replace_keywords(tokens):
    """
    substituir palavras chaves da linguagem de origem por
    instruções equivalentes na linguagem de destino
    """
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
    """
    corrige a forma de declaração de variaveis,
    a logica para corrigir consister em simplesmente
    adicionar antes um token do tipo indentifier com valor 'var'

    exemplo: teste = 1 -> var teste = 1
    """

    idx = 0
    while idx < len(tokens):
        if idx-1 >= 0 and \
           tokens[idx].type   == Token.EQUAL and \
           tokens[idx+1].type != Token.EQUAL and \
           tokens[idx-1].type == Token.IDENTIFIER:
            var_keyword = Token(Token.IDENTIFIER, value='var')
            tokens.insert(idx-1, var_keyword)
            idx += 1
        idx += 1

def fix_code_blocks(tokens):
    """
    corrige o estilo de codigo usado em if/else e while,
    esta função contém muitas funções aninhadas reponsaveis
    por cada etapa da correção
    """

    def fix_header_block(index_keyword, tokens):
        """
        corrige o estilo da declaração de codigo,
        exemplo: while True: -> while(True){
        """
        tokens.insert(index_keyword+1, Token(Token.OPEN_PARANTHESIS))

        idx = index_keyword
        while tokens[idx].type != Token.COLON:
            idx += 1
        tokens[idx].type = Token.OPEN_KEYS
        tokens.insert(idx, Token(Token.CLOSE_PARANTHESIS))

    def get_indent_level(tokens, index_start):
        """retorna um inteiro que corresponde ao nivel de indentação"""
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
        """retorna o indice do proximo caractere de quebra de linha"""
        while index_start < len(tokens):
            if tokens[index_start].type == Token.BREAK_LINE:
                return index_start
            index_start += 1

    def find_end_block(tokens, index_start, indent_level):
        """retorna o indice do fim do bloco de codigo"""
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
        """
        usando o indice que representa o fim do bloco, aplica
        a correção que consiste em adicionar um token de fechamento de
        chave '}'
        """
        if index_end != len(tokens):
            if tokens[index_end].type == Token.CLOSE_KEYS:
                tokens.insert(index_end, Token(Token.BREAK_LINE))
            tokens.insert(index_end, Token(Token.CLOSE_KEYS))
            for _ in range(indent_level-1):
                tokens.insert(index_end, Token(Token.INDENT))
            tokens.insert(index_end, Token(Token.BREAK_LINE))
        else:
            del tokens[-1]
            for _ in range(indent_level-1):
                tokens.append(Token(Token.INDENT))
            tokens.append(Token(Token.BREAK_LINE))
            tokens.append(Token(Token.CLOSE_KEYS))

    idx = 0
    while idx < len(tokens):
        if tokens[idx].type == Token.IDENTIFIER and \
           (tokens[idx].value == 'if' or \
            tokens[idx].value == 'else if' or \
            tokens[idx].value == 'while'):
            fix_header_block(idx, tokens)
            indent_level = get_indent_level(tokens, idx)
            index_end = find_end_block(tokens, idx, indent_level)
            fix_end(index_end, tokens)

        elif tokens[idx].type == Token.IDENTIFIER and \
             tokens[idx].value == 'else':
            tokens[idx+1].type = Token.OPEN_KEYS
            indent_level = get_indent_level(tokens, idx)
            index_end = find_end_block(tokens, idx, indent_level)
            fix_end(index_end, tokens)

        idx +=1
