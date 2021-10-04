import unittest

from lexer import Source, tokenizer, Token

class Test(unittest.TestCase):
    def test_lexer_source_function(self):
        source = Source('test')
        self.assertEqual('t', source.next())
        self.assertEqual('e', source.next())
        self.assertEqual('s', source.next())
        self.assertEqual('t', source.next())
        self.assertEqual('',  source.next())

    def test_tokenizer_function(self):
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

if __name__ == '__main__':
    unittest.main()
