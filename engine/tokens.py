"""
Token Definitions for SQLidator v2
-----------------------------------
Defines token types and Token class.
"""

from enum import Enum


# ==========================================
# TOKEN TYPES
# ==========================================

class TokenType(Enum):
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    QUOTED_IDENTIFIER = "QUOTED_IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"
    OPERATOR = "OPERATOR"
    COMMA = "COMMA"
    SEMICOLON = "SEMICOLON"
    PAREN_OPEN = "PAREN_OPEN"
    PAREN_CLOSE = "PAREN_CLOSE"
    DOT = "DOT"
    ASTERISK = "ASTERISK"
    EOF = "EOF"


# ==========================================
# SQL KEYWORDS (Phase 1 - SELECT Focus)
# ==========================================

KEYWORDS = {
    # SELECT
    "SELECT",
    "FROM",
    "WHERE",
    "GROUP",
    "BY",
    "HAVING",
    "ORDER",
    "LIMIT",
    "JOIN",
    "INNER",
    "LEFT",
    "RIGHT",
    "FULL",
    "OUTER",
    "ON",
    "AS",
    "AND",
    "OR",
    "NOT",
    "IN",
    "EXISTS",
    "IS",
    "NULL",

    # INSERT
    "INSERT",
    "INTO",
    "VALUES",

    # DELETE
    "DELETE",

    # UPDATE
    "UPDATE",
    "SET",

    # CREATE
    "CREATE",
    "TABLE",
    "PRIMARY",
    "KEY",
    "NOT",
    "NULL",
    "UNIQUE",

    # ALTER
    "ALTER",
    "ADD",
    "COLUMN",
    "DROP",
    "RENAME",
    "TO",

    # DROP
    "DROP",

    "GROUP",
    "BY",
    "HAVING",
    "ORDER",
    "LIMIT",

    # VIEW
    "VIEW"
}



# ==========================================
# TOKEN CLASS
# ==========================================

class Token:
    def __init__(self, type_, value, line, column):
        self.type = type_
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        return f"Token({self.type}, '{self.value}', line={self.line}, col={self.column})"
