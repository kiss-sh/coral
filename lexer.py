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

class Toker:
    def __init__(self, _type, value=None):
        self.type = _type
        self.value = value

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

        elif c.isalpha():
            token_buffer.append(c)

            while True:
                c = source.next()
                if c.isalnum():
                    token_buffer.append(c)
                else:
                    break

            token = Toker('identifier', value=''.join(token_buffer))
            tokens.append(token)
            token_buffer = []

        elif c == '=':
            token = Toker('equals or assigns')
            tokens.append(token)
            c = source.next()

        elif c == '+':
            token = Toker('plus')
            tokens.append(token)
            c = source.next()

        elif c == '*':
            token = Toker('multiply')
            tokens.append(token)
            c = source.next()

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

                    token = Toker('float', value=''.join(token_buffer))
                    token_buffer = []
                    tokens.append(token)

                else:
                    token = Toker('integer', value=''.join(token_buffer))
                    token_buffer = []
                    tokens.append(token)

        else:
            c = source.next()

    return tokens

def print_tokens(tokens):
    for token in tokens:
        print(f'type: {token.type}, value: {token.value}')
