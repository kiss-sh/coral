import copy
import unittest

from lexer import Source, tokenizer, Token
from parser import Node, replace_keywords, fix_variable_declaration, fix_code_blocks
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
                         '    pass')
        source = Source(original_code)
        tokens = tokenizer(source)

        self.assertTrue(len(tokens) == 6)
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


        original_code = ('if True:\n'
                         '    print(True)\n'
                         '\n'
                         '    if True:\n'
                         '        print(True)')
        source = Source(original_code)
        tokens = tokenizer(source)
        replace_keywords(tokens)
        #fix_code_blocks(tokens)
        new_code = tokens_to_code(tokens)

        expected_code = ('if(true) {\n'
                         '    console.log(true)\n'
                         '\n'
                         '    if(true) {\n'
                         '        console.log(true)\n'
                         '    }\n'
                         '}')
        #self.assertEqual(expected_code, new_code)

if __name__ == '__main__':
    unittest.main()
