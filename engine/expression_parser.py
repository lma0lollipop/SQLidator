"""
Expression Parser (Phase 1)
----------------------------
Handles WHERE clause boolean expressions.
"""

from engine.tokens import TokenType
from engine.expression_nodes import (
    BinaryOpNode,
    UnaryOpNode,
    LiteralNode,
    IdentifierNode
)
from engine.errors import SQLSyntaxError


class ExpressionParser:
    def __init__(self, parser):
        # We reuse main parser's token stream
        self.parser = parser

    # ======================================================
    # ENTRY
    # ======================================================

    def parse_expression(self):
        return self.parse_or()

    # OR level
    def parse_or(self):
        node = self.parse_and()

        while self.parser.match_keyword("OR"):
            operator = self.parser.current_token.value
            self.parser.advance()
            right = self.parse_and()
            node = BinaryOpNode(node, operator, right)

        return node

    # AND level
    def parse_and(self):
        node = self.parse_not()

        while self.parser.match_keyword("AND"):
            operator = self.parser.current_token.value
            self.parser.advance()
            right = self.parse_not()
            node = BinaryOpNode(node, operator, right)

        return node

    # NOT level
    def parse_not(self):
        if self.parser.match_keyword("NOT"):
            operator = self.parser.current_token.value
            self.parser.advance()
            operand = self.parse_not()
            return UnaryOpNode(operator, operand)

        return self.parse_comparison()

    # Comparison level
    def parse_comparison(self):
        left = self.parse_primary()

        if self.parser.current_token.type == TokenType.OPERATOR:
            operator = self.parser.current_token.value
            self.parser.advance()
            right = self.parse_primary()
            return BinaryOpNode(left, operator, right)

        return left

    # Primary level
    def parse_primary(self):
        token = self.parser.current_token

        if token.type == TokenType.IDENTIFIER:
            self.parser.advance()
            return IdentifierNode(token.value)

        if token.type == TokenType.NUMBER:
            self.parser.advance()
            return LiteralNode(token.value)

        if token.type == TokenType.STRING:
            self.parser.advance()
            return LiteralNode(token.value)

        if token.type == TokenType.PAREN_OPEN:
            self.parser.advance()
            expr = self.parse_expression()

            if self.parser.current_token.type != TokenType.PAREN_CLOSE:
                self.parser.raise_error()

            self.parser.advance()
            return expr

        self.parser.raise_error()
