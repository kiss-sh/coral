import unittest

from lexer import Source, tokenizer, Token
from parser import  replace_keywords, fix_variable_declaration, fix_code_blocks
from generation_code import tokens_to_code

class Test(unittest.TestCase):
    def test_lexer_source_fn(self):
        source = Source('test')
        self.assertEqual('t', source.next())
        self.assertEqual('e', source.next())
        self.assertEqual('s', source.next())
        self.assertEqual('t', source.next())
        self.assertEqual('',  source.next())

    def test_tokenizer_fn(self):
        source = Source('test = 1')
        tokens = tokenizer(source)

        self.assertTrue(len(tokens) == 3)
        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual('test', tokens[0].value)

        self.assertEqual(Token.EQUAL, tokens[1].type)
        self.assertEqual(None,  tokens[1].value)

        self.assertEqual(Token.INTEGER, tokens[2].type)
        self.assertEqual(1, tokens[2].value)


        source = Source('#teste')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 0)


        source = Source("'teste'")
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 1)
        self.assertEqual(Token.STRING, tokens[0].type)
        self.assertEqual("'teste'", tokens[0].value)


        source = Source('print()')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 3)
        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual('print', tokens[0].value)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[1].type)
        self.assertEqual(None, tokens[1].value)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[2].type)
        self.assertEqual(None, tokens[2].value)


        source = Source('print(var)')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 4)
        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual('print', tokens[0].value)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[1].type)
        self.assertEqual(None, tokens[1].value)
        self.assertEqual(Token.IDENTIFIER, tokens[2].type)
        self.assertEqual('var', tokens[2].value)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[3].type)
        self.assertEqual(None, tokens[3].value)

        source = Source('2, 2')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 3)
        self.assertEqual(Token.COMMA, tokens[1].type)

        original_code = ('if True:\n'
                         '    if True:\n'
                         '        print(True)')
        source = Source(original_code)
        tokens = tokenizer(source)

        self.assertTrue(len(tokens) == 15)
        self.assertEqual(Token.INDENT, tokens[4].type)

    def test_replace_keywords_fn(self):
        source = Source('False')
        tokens = tokenizer(source)
        replace_keywords(tokens)
        self.assertEqual('false', tokens[0].value)

        source = Source('True')
        tokens = tokenizer(source)
        replace_keywords(tokens)
        self.assertEqual('true', tokens[0].value)

        source = Source('None')
        tokens = tokenizer(source)
        replace_keywords(tokens)
        self.assertEqual('null', tokens[0].value)

        source = Source('and')
        tokens = tokenizer(source)
        replace_keywords(tokens)
        self.assertEqual('&&', tokens[0].value)

        source = Source('or')
        tokens = tokenizer(source)
        replace_keywords(tokens)
        self.assertEqual('||', tokens[0].value)

    def test_fix_variable_declaration_fn(self):
        source = Source('sum = 1')
        tokens = tokenizer(source)
        fix_variable_declaration(tokens)

        self.assertTrue(len(tokens) == 4)
        self.assertEqual('var', tokens[0].value)

    def test_tokens_to_code_fn(self):
        original_code = 'sum = 3.14 + 2 * 4'
        source = Source(original_code)
        tokens = tokenizer(source)
        new_code = tokens_to_code(tokens)
        self.assertEqual(new_code, original_code)

        original_code = 'print()'
        source = Source(original_code)
        tokens = tokenizer(source)
        new_code = tokens_to_code(tokens)
        self.assertEqual(new_code, original_code)

        original_code = 'print(var)'
        source = Source(original_code)
        tokens = tokenizer(source)
        new_code = tokens_to_code(tokens)
        self.assertEqual(new_code, original_code)

    def test_fix_code_blocks(self):
        original_code = ('if True:\n'
                         '    print(True)')
        source = Source(original_code)
        tokens = tokenizer(source)
        replace_keywords(tokens)
        fix_code_blocks(tokens)

        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[1].type)
        self.assertEqual(Token.IDENTIFIER, tokens[2].type)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[3].type)
        self.assertEqual(Token.OPEN_KEYS, tokens[4].type)
        self.assertEqual(Token.BREAK_LINE, tokens[5].type)
        self.assertEqual(Token.INDENT, tokens[6].type)
        self.assertEqual(Token.IDENTIFIER, tokens[7].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[8].type)
        self.assertEqual(Token.IDENTIFIER, tokens[9].type)

        original_code = ('if True:\n'
                         '    print(True)\n'
                         '    if True:\n'
                         '        print(True)')
        source = Source(original_code)
        tokens = tokenizer(source)
        replace_keywords(tokens)
        fix_code_blocks(tokens)

        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[1].type)
        self.assertEqual(Token.IDENTIFIER, tokens[2].type)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[3].type)
        self.assertEqual(Token.OPEN_KEYS, tokens[4].type)
        self.assertEqual(Token.BREAK_LINE, tokens[5].type)
        self.assertEqual(Token.INDENT, tokens[6].type)
        self.assertEqual(Token.IDENTIFIER, tokens[7].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[8].type)
        self.assertEqual(Token.IDENTIFIER, tokens[9].type)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[10].type)
        self.assertEqual(Token.BREAK_LINE, tokens[11].type)
        self.assertEqual(Token.INDENT, tokens[12].type)
        self.assertEqual(Token.IDENTIFIER, tokens[13].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[14].type)
        self.assertEqual(Token.IDENTIFIER, tokens[15].type)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[16].type)
        self.assertEqual(Token.OPEN_KEYS, tokens[17].type)
        self.assertEqual(Token.BREAK_LINE, tokens[18].type)
        self.assertEqual(Token.INDENT, tokens[19].type)
        self.assertEqual(Token.INDENT, tokens[20].type)
        self.assertEqual(Token.IDENTIFIER, tokens[21].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[22].type)
        self.assertEqual(Token.IDENTIFIER, tokens[23].type)

        original_code = 'print(var)'
        source = Source(original_code)
        tokens = tokenizer(source)
        replace_keywords(tokens)
        fix_code_blocks(tokens)
        self.assertTrue(len(tokens) == 4)
        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual('console.log', tokens[0].value)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[1].type)
        self.assertEqual(None, tokens[1].value)
        self.assertEqual(Token.IDENTIFIER, tokens[2].type)
        self.assertEqual('var', tokens[2].value)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[3].type)
        self.assertEqual(None, tokens[3].value)

        original_code = ('def sum(a, b):\n'
                         '    return a + b')
        source = Source(original_code)
        tokens = tokenizer(source)
        replace_keywords(tokens)
        fix_code_blocks(tokens)

        self.assertEqual(Token.IDENTIFIER, tokens[0].type)
        self.assertEqual(Token.IDENTIFIER, tokens[1].type)
        self.assertEqual(Token.OPEN_PARANTHESIS, tokens[2].type)
        self.assertEqual(Token.IDENTIFIER, tokens[3].type)
        self.assertEqual(Token.COMMA, tokens[4].type)
        self.assertEqual(Token.IDENTIFIER, tokens[5].type)
        self.assertEqual(Token.CLOSE_PARANTHESIS, tokens[6].type)
        self.assertEqual(Token.OPEN_KEYS, tokens[7].type)
        self.assertEqual(Token.BREAK_LINE, tokens[8].type)

if __name__ == '__main__':
    unittest.main()
