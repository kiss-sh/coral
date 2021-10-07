from lexer import Token

class Node:
    def __init__(self, data):
        self.data = data
        self.right = None
        self.left = None

def create_ast(tokens):
    if len(tokens) == 1:
        return Node(tokens[0])

    elif len(tokens) > 1:
        node0 = Node(tokens[0])
        node1 = Node(tokens[1])
        del tokens[:2]

        if node1.data.type == Token.EQUAL:
            node0.data.type = Token.IDENTIFIER_VARIABLE
            node1.right = node0
            node1.left = create_ast(tokens)
            return node1

        elif node1.data.type == Token.MULTIPLY or node1.data.type == Token.PLUS:
            node1.right = node0
            node1.left = create_ast(tokens)
            return node1

    else:
        return None

def transform_ast(node):
    if node.data.type == Token.IDENTIFIER_VARIABLE:
        node_var_word = Node(Token(Token.IDENTIFIER, value='var'))
        node.right = node_var_word

    if node.right is not None:
        transform_ast(node.right)
    if node.left is not None:
        transform_ast(node.left)
