"""
modulo responsavel pela extração de dados a partir do codigo fonte
de entrada
"""

class Source:
    """
    esta classe abstrai a origem do codigo, permitindo
    que tenha o mesmo comportamento caso o codigo esteja
    sendo lido a partir de um arquivo ou a partir da entrada
    de texto padrão
    """

    def __init__(self, _input, is_file=False):
        if is_file:
            self.source = open(_input, 'r')
            self.is_file = True
        else:
            self.source = list(_input)
            self.is_file = False

    def next(self):
        """
        retorna o proximo caractere do codigo ou uma string
        vazia quando não houver mais caracteres
        """
        if self.is_file:
            return self.source.read(1)

        if len(self.source) > 0:
            character = self.source[0]
            del self.source[0]
            return character

        return ''

class Token:
    """
    O proposito desta classe é ser uma struct para manter
    reunido algumas informações a cerca de um mesmo token
    """

    # types
    BREAK_LINE = 'break_line'               # '\n'
    CLOSE_BRACKETS = 'close_brackets'       # ']'
    CLOSE_KEYS = 'close_keys'               # '}'
    CLOSE_PARANTHESIS = 'close_paranthesis' # ')'
    COLON = 'colon'                         # ':'
    COMMA = 'comma'                         # ','
    EQUAL = 'equal'                         # '='
    FLOAT = 'float'
    IDENTIFIER = 'identifier'
    INDENT = 'indent'                       # '    '
    INTEGER = 'integer'
    MULTIPLY = 'multiply'
    OPEN_BRACKETS = 'open_brackets'         # '['
    OPEN_KEYS = 'open_keys'                 # '{'
    OPEN_PARANTHESIS = 'open_paranthesis'   # '('
    PLUS = 'plus'                           # '+'
    STRING = 'string'

    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

# number of spaces for a unit indent
SIZE_OF_INDENT = 4

def tokenizer(source):
    """
    gera uma lista de tokens a partir da analise de cacteres,
    a logica do funcionamento é muito semelhante com maquinas
    de estado em que o estado final encontrado indica o tipo de
    token
    """

    token_buffer = []
    tokens = []

    c = source.next()
    while True:
        if c == '':
            break

        if c == '#': # ignore comments
            while True:
                c = source.next()
                if c == '\n' or c == '':
                    break

        elif c.isalpha() or c == '_': # read indentifiers
            token_buffer.append(c)

            while True:
                c = source.next()
                if c.isalnum() or c == '_' or c == '.':
                    token_buffer.append(c)
                else:
                    break

            token = Token(Token.IDENTIFIER, value=''.join(token_buffer))
            tokens.append(token)
            token_buffer = []

        elif c == '"' or c == "'": # read strings
            token_buffer.append(c)

            while True:
                c = source.next()
                token_buffer.append(c)

                if c == token_buffer[0]:
                    break
                elif c == '':
                    exit('erro na analise da string')

            token = Token(Token.STRING, value=''.join(token_buffer))
            tokens.append(token)
            token_buffer = []
            c = source.next()

        elif c == '=': # read '=' character
            token = Token(Token.EQUAL)
            tokens.append(token)
            c = source.next()

        elif c == '+': # read '+' character
            token = Token(Token.PLUS)
            tokens.append(token)
            c = source.next()

        elif c == '*': # read '*' character
            token = Token(Token.MULTIPLY)
            tokens.append(token)
            c = source.next()

        elif c == '(': # read '(' character
            token = Token(Token.OPEN_PARANTHESIS)
            tokens.append(token)
            c = source.next()

        elif c == ')': # read ')' character
            token = Token(Token.CLOSE_PARANTHESIS)
            tokens.append(token)
            c = source.next()

        elif c == ':': # read ':' character
            token = Token(Token.COLON)
            tokens.append(token)
            c = source.next()

        elif c == ',': # read ',' character
            token = Token(Token.COMMA)
            tokens.append(token)
            c = source.next()

        elif c == '[': # read '[' character
            token = Token(Token.OPEN_BRACKETS)
            tokens.append(token)
            c = source.next()

        elif c == ']': # read ']' character
            token = Token(Token.CLOSE_BRACKETS)
            tokens.append(token)
            c = source.next()

        elif c == ' ': # read the indent using spaces
            token_buffer.append(c)

            while len(token_buffer) < SIZE_OF_INDENT:
                c = source.next()
                if c == ' ':
                    token_buffer.append(c)
                else:
                    break

            if len(token_buffer) == SIZE_OF_INDENT:
                token = Token(Token.INDENT)
                tokens.append(token)
            token_buffer = []


        elif c.isdecimal(): # read a number integer or float
            while c.isdecimal():
                token_buffer.append(c)
                c = source.next()
            else:
                if c == '.':
                    token_buffer.append(c)
                    c = source.next()

                    while c.isdecimal():
                        token_buffer.append(c)
                        c = source.next()

                    token = Token(Token.FLOAT, value=float(''.join(token_buffer)))
                    token_buffer = []
                    tokens.append(token)

                else:
                    token = Token(Token.INTEGER, value=int(''.join(token_buffer)))
                    token_buffer = []
                    tokens.append(token)

        elif c == '\n': # read a breakline
            token = Token(Token.BREAK_LINE)
            tokens.append(token)
            c = source.next()

        else:
            c = source.next()

    return tokens
