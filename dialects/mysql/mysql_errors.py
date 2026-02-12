"""
MySQL Error Handling Module
----------------------------
Provides standardized error responses for MySQL dialect.
"""

def mysql_error(message: str, error_type: str = "SyntaxError") -> dict:
    """
    Generic MySQL error response.

    Parameters:
        message (str): Error message
        error_type (str): Type of error

    Returns:
        dict: structured error response
    """

    return {
        "status": "error",
        "dialect": "MySQL",
        "type": error_type,
        "message": message
    }


def mysql_syntax_error(message: str) -> dict:
    return mysql_error(message, "SyntaxError")


def mysql_semantic_error(message: str) -> dict:
    return mysql_error(message, "SemanticError")


def mysql_internal_error(message: str) -> dict:
    return mysql_error(message, "InternalError")
