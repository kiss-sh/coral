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

        if node1.data.type == (Token.EQUAL or Token.MULTIPLY or Token.PLUS):
            node1.right = node0
            node1.left = create_ast(tokens)
            return node1

    else:
        return None
