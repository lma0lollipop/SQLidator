"""
SQL Lexer (Tokenizer)
---------------------
Converts raw SQL query into list of tokens.
"""

from engine.tokens import TokenType, Token, KEYWORDS
from engine.errors import SQLSyntaxError


class Lexer:
    def __init__(self, query, dialect="postgres"):
        self.query = query
        self.dialect = dialect
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens = []

    def tokenize(self):
        while self.position < len(self.query):
            char = self.current_char()

            if char in " \t":
                self.advance()

            elif char == "\n":
                self.advance_line()

            elif char == ",":
                self.add_token(TokenType.COMMA, ",")
                self.advance()

            elif char == ";":
                self.add_token(TokenType.SEMICOLON, ";")
                self.advance()

            elif char == "(":
                self.add_token(TokenType.PAREN_OPEN, "(")
                self.advance()

            elif char == ")":
                self.add_token(TokenType.PAREN_CLOSE, ")")
                self.advance()

            elif char == ".":
                self.add_token(TokenType.DOT, ".")
                self.advance()

            elif char == "*":
                self.add_token(TokenType.ASTERISK, "*")
                self.advance()

            elif char in "=<>!":
                self.tokenize_operator()

            elif char.isdigit():
                self.tokenize_number()

            elif char == "'":
                self.tokenize_string()

            elif char == '"':
                self.tokenize_quoted_identifier()

            elif char.isalpha() or char == "_":
                self.tokenize_identifier()

            elif char == "-" and self.peek() == "-":
                self.skip_single_line_comment()

            elif char == "/" and self.peek() == "*":
                self.skip_multi_line_comment()

            else:
                self.raise_error(f"Invalid character '{char}'")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens

    # ======================================================
    # TOKEN BUILDERS
    # ======================================================

    def tokenize_identifier(self):
        start_column = self.column
        value = ""

        while self.current_char() and (
            self.current_char().isalnum() or self.current_char() == "_"
        ):
            value += self.current_char()
            self.advance()

        upper_value = value.upper()

        if upper_value in KEYWORDS:
            self.tokens.append(Token(TokenType.KEYWORD, upper_value, self.line, start_column))
        else:
            self.tokens.append(Token(TokenType.IDENTIFIER, value, self.line, start_column))

    def tokenize_number(self):
        start_column = self.column
        value = ""
        dot_count = 0

        while self.current_char() and (self.current_char().isdigit() or self.current_char() == "."):
            if self.current_char() == ".":
                dot_count += 1
                if dot_count > 1:
                    self.raise_error("Invalid number format")
            value += self.current_char()
            self.advance()

        self.tokens.append(Token(TokenType.NUMBER, value, self.line, start_column))

    def tokenize_string(self):
        start_column = self.column
        value = ""
        self.advance()  # skip opening quote

        while self.current_char():
            if self.current_char() == "'":
                self.advance()
                self.tokens.append(Token(TokenType.STRING, value, self.line, start_column))
                return
            value += self.current_char()
            self.advance()

        self.raise_error("Unterminated string literal")

    def tokenize_quoted_identifier(self):
        start_column = self.column
        value = ""
        self.advance()  # skip opening quote

        while self.current_char():
            if self.current_char() == '"':
                self.advance()
                self.tokens.append(Token(TokenType.QUOTED_IDENTIFIER, value, self.line, start_column))
                return
            value += self.current_char()
            self.advance()

        self.raise_error("Unterminated quoted identifier")

    def tokenize_operator(self):
        start_column = self.column
        char = self.current_char()
        next_char = self.peek()

        if char + next_char in ["<=", ">=", "<>", "!="]:
            op = char + next_char
            self.advance()
            self.advance()
        else:
            op = char
            self.advance()

        self.tokens.append(Token(TokenType.OPERATOR, op, self.line, start_column))

    # ======================================================
    # COMMENTS
    # ======================================================

    def skip_single_line_comment(self):
        while self.current_char() and self.current_char() != "\n":
            self.advance()

    def skip_multi_line_comment(self):
        self.advance()  # skip /
        self.advance()  # skip *

        while self.current_char():
            if self.current_char() == "*" and self.peek() == "/":
                self.advance()
                self.advance()
                return
            if self.current_char() == "\n":
                self.advance_line()
            else:
                self.advance()

        self.raise_error("Unterminated multi-line comment")

    # ======================================================
    # HELPERS
    # ======================================================

    def current_char(self):
        if self.position >= len(self.query):
            return None
        return self.query[self.position]

    def peek(self):
        if self.position + 1 >= len(self.query):
            return None
        return self.query[self.position + 1]

    def advance(self):
        self.position += 1
        self.column += 1

    def advance_line(self):
        self.position += 1
        self.line += 1
        self.column = 1

    def add_token(self, type_, value):
        self.tokens.append(Token(type_, value, self.line, self.column))

    def raise_error(self, message):
        from engine.tokens import Token
        token = Token(None, self.current_char(), self.line, self.column)
        raise SQLSyntaxError(
            message,
            token=token,
            query=self.query,
            dialect=self.dialect
        )
