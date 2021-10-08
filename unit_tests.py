import copy
import unittest

from lexer import Source, tokenizer, Token
from parser import Node, create_ast, transform_ast
from generation_code import ast_to_code

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

        source = Source('"teste"')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 1)
        self.assertEqual(Token.STRING, tokens[0].type)
        self.assertEqual('"teste"', tokens[0].value)

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

    def test_create_ast_fn(self):
        source = Source('sum = 3.14 + 2 * 4')
        tokens = tokenizer(source)
        tokens_copy = copy.copy(tokens)

        ast = create_ast(tokens)
        self.assertEqual(tokens_copy[1], ast.data)
        self.assertEqual(tokens_copy[0], ast.right.data)
        self.assertEqual(tokens_copy[3], ast.left.data)
        self.assertEqual(tokens_copy[2], ast.left.right.data)
        self.assertEqual(tokens_copy[5], ast.left.left.data)
        self.assertEqual(tokens_copy[4], ast.left.left.right.data)
        self.assertEqual(tokens_copy[6], ast.left.left.left.data)

    def test_transform_ast_fn(self):
        source = Source('sum = 1')
        tokens = tokenizer(source)
        tokens_copy = copy.deepcopy(tokens)
        ast = create_ast(tokens)
        transform_ast(ast)

        self.assertEqual('var', ast.right.right.data.value)

    def test_ast_to_code_fn(self):
        original_code = 'sum = 3.14 + 2 * 4'
        source = Source(original_code)
        tokens = tokenizer(source)
        ast = create_ast(tokens)
        transform_ast(ast)
        new_code = ast_to_code(ast)

        self.assertEqual(new_code, f'var {original_code}')


if __name__ == '__main__':
    unittest.main()
