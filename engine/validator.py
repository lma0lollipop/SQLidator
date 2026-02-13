"""
SQLidator Core Validator Engine (Parser-Based)
----------------------------------------------
This is the central brain of SQLidator.

Flow:
    Query → Lexer → Parser → AST

Responsibilities:
- Run lexical analysis
- Run syntax parsing
- Catch SQL-style syntax errors
- Return structured response
- Prevent crashes
"""

from engine.lexer import Lexer
from engine.parser import Parser
from engine.errors import SQLSyntaxError


def validate_query(query: str, dialect: str = "postgres") -> dict:
    """
    Main validation entry point.

    Parameters:
        query (str): SQL query input
        dialect (str): postgres | mysql | plsql

    Returns:
        dict: structured validation result
    """

    try:
        # -----------------------------
        # Basic Input Validation
        # -----------------------------
        if not isinstance(query, str):
            return _error_response("Query must be a string.", dialect)

        if not query.strip():
            return _error_response("Query cannot be empty.", dialect)

        # -----------------------------
        # Lexical Analysis
        # -----------------------------
        lexer = Lexer(query)
        tokens = lexer.tokenize()

        # -----------------------------
        # Parsing
        # -----------------------------
        parser = Parser(tokens, query, dialect)
        ast = parser.parse()

        return {
            "status": "success",
            "dialect": dialect,
            "type": None,
            "message": "Query parsed successfully.",
            "ast": ast
        }

    except SQLSyntaxError as e:
        return {
            "status": "error",
            "dialect": dialect,
            "type": "SyntaxError",
            "message": str(e)
        }

    except Exception as e:
        return {
            "status": "error",
            "dialect": dialect,
            "type": "InternalError",
            "message": str(e)
        }


def _error_response(message: str, dialect: str) -> dict:
    return {
        "status": "error",
        "dialect": dialect,
        "type": "ValidationError",
        "message": message
    }
