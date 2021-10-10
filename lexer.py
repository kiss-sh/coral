
class Source:
    def __init__(self, _input, is_file=False):
        if is_file:
            self.source = open(_input, 'r')
            self.is_file = True
        else:
            self.source = list(_input)
            self.is_file = False

    def next(self):
        if self.is_file:
            return self.source.read(1)
        else:
            if len(self.source) > 0:
                c = self.source[0]
                del self.source[0]
                return c
            else:
                return ''

class Token:
    # types
    BREAK_LINE = 'break_line'               # '\n'
    CLOSE_BRACKETS = 'close_brackets'       # '}'
    CLOSE_PARANTHESIS = 'close_paranthesis' # ')'
    COLON = 'colon'                         # ':'
    COMMA = 'comma'                         # ','
    EQUAL = 'equal'                         # '='
    FLOAT = 'float'
    IDENTIFIER = 'identifier'
    INTEGER = 'integer'
    MULTIPLY = 'multiply'
    OPEN_BRACKETS = 'open_brackets'         # '{'
    OPEN_PARANTHESIS = 'open_paranthesis'   # '('
    PLUS = 'plus'                           # '+'
    STRING = 'string'
    INDENT = 'indent'                       # '    '

    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

# number of spaces for a unit indent
SIZE_OF_INDENT = 4

def tokenizer(source):
    token_buffer = []
    tokens = []

    c = source.next()
    while True:
        if c == '':
            break

        if c == '#':
            # ignore comments
            while True:
                c = source.next()
                if c == '\n' or c == '':
                    break

        elif c.isalpha() or c == '_':
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

        elif c == '"' or c == "'":
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

        elif c == '=':
            token = Token(Token.EQUAL)
            tokens.append(token)
            c = source.next()

        elif c == '+':
            token = Token(Token.PLUS)
            tokens.append(token)
            c = source.next()

        elif c == '*':
            token = Token(Token.MULTIPLY)
            tokens.append(token)
            c = source.next()

        elif c == '(':
            token = Token(Token.OPEN_PARANTHESIS)
            tokens.append(token)
            c = source.next()

        elif c == ')':
            token = Token(Token.CLOSE_PARANTHESIS)
            tokens.append(token)
            c = source.next()

        elif c == ':':
            token = Token(Token.COLON)
            tokens.append(token)
            c = source.next()

        elif c == ',':
            token = Token(Token.COMMA)
            tokens.append(token)
            c = source.next()

        elif c == ' ':
            token_buffer.append(c)
            count_space = 1

            while count_space <= SIZE_OF_INDENT:
                c = source.next()
                if c == ' ':
                    token_buffer.append(c)
                    count_space += 1
                else:
                    break

            if count_space == SIZE_OF_INDENT:
                token = Token(Token.INDENT)
                tokens.append(token)
            token_buffer = []


        elif c.isdecimal():
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

        elif c == '\n':
            token = Token(Token.BREAK_LINE)
            tokens.append(token)
            c = source.next()

        else:
            c = source.next()

    return tokens
