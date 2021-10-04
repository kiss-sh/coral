import unittest

from lexer import Source, tokenizer, Toker

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
        token0 = Toker('identifier', value='test')
        token1 = Toker('equals or assigns')
        token2 = Toker('integer', value='1')
        tokens = tokenizer(source)

        self.assertTrue(len(tokens) == 3)
        self.assertEqual(token0.type,  tokens[0].type)
        self.assertEqual(token0.value, tokens[0].value)
        self.assertEqual(token1.type,  tokens[1].type)
        self.assertEqual(token1.value, tokens[1].value)
        self.assertEqual(token2.type,  tokens[2].type)
        self.assertEqual(token2.value, tokens[2].value)

        source = Source('#teste')
        tokens = tokenizer(source)
        self.assertTrue(len(tokens) == 0)

if __name__ == '__main__':
    unittest.main()
