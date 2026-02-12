"""
Expression AST Nodes
--------------------
Used for WHERE clause parsing.
"""


class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.type = "BINARY_OP"
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"


class UnaryOpNode:
    def __init__(self, operator, operand):
        self.type = "UNARY_OP"
        self.operator = operator
        self.operand = operand

    def __repr__(self):
        return f"({self.operator} {self.operand})"


class LiteralNode:
    def __init__(self, value):
        self.type = "LITERAL"
        self.value = value

    def __repr__(self):
        return f"{self.value}"


class IdentifierNode:
    def __init__(self, name):
        self.type = "IDENTIFIER"
        self.name = name

    def __repr__(self):
        return self.name
