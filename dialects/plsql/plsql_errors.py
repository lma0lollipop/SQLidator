"""
PL/SQL Error Handling Module
-----------------------------
Provides standardized error responses for PL/SQL dialect.
"""


def plsql_error(message: str, error_type: str = "SyntaxError") -> dict:
    """
    Generic PL/SQL error response.

    Parameters:
        message (str): Error message
        error_type (str): Type of error

    Returns:
        dict: structured error response
    """

    return {
        "status": "error",
        "dialect": "PL/SQL",
        "type": error_type,
        "message": message
    }


def plsql_syntax_error(message: str) -> dict:
    return plsql_error(message, "SyntaxError")


def plsql_semantic_error(message: str) -> dict:
    return plsql_error(message, "SemanticError")


def plsql_internal_error(message: str) -> dict:
    return plsql_error(message, "InternalError")
