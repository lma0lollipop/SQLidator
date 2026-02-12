"""
PostgreSQL Error Handling Module
---------------------------------
Provides standardized error responses for PostgreSQL dialect.
"""

def postgres_error(message: str, error_type: str = "SyntaxError") -> dict:
    """
    Generic PostgreSQL error response.

    Parameters:
        message (str): Error message
        error_type (str): Type of error

    Returns:
        dict: structured error response
    """

    return {
        "status": "error",
        "dialect": "PostgreSQL",
        "type": error_type,
        "message": message
    }


def postgres_syntax_error(message: str) -> dict:
    return postgres_error(message, "SyntaxError")


def postgres_semantic_error(message: str) -> dict:
    return postgres_error(message, "SemanticError")


def postgres_internal_error(message: str) -> dict:
    return postgres_error(message, "InternalError")
