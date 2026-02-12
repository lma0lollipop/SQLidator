"""
SQLidator Core Validator Engine
--------------------------------
This file acts as the central brain of the application.

Responsibilities:
- Normalize query
- Route to correct dialect
- Catch ALL errors
- Return structured response
- Prevent crashes
"""

from engine.normalizer import normalize_query

from dialects.mysql.mysql_validation import validate_mysql
from dialects.postgres.postgres_validation import validate_postgres
from dialects.plsql.plsql_validation import validate_plsql


def validate_query(query: str, dialect: str = "mysql") -> dict:
    """
    Main validation entry point.
    
    Parameters:
        query (str): SQL query input
        dialect (str): mysql | postgres | plsql

    Returns:
        dict: structured validation result
    """

    try:
        # Basic input validation
        if not isinstance(query, str):
            return _error_response("Query must be a string.")

        if not query.strip():
            return _error_response("Query cannot be empty.")

        # Normalize query
        query = normalize_query(query)

        dialect = dialect.lower()

        # Dialect routing
        if dialect == "mysql":
            return validate_mysql(query)

        elif dialect == "postgres":
            return validate_postgres(query)

        elif dialect == "plsql":
            return validate_plsql(query)

        else:
            return _error_response(f"Unsupported SQL dialect: {dialect}")

    except Exception as e:
        # Absolute fail-safe catch
        return {
            "status": "error",
            "dialect": dialect,
            "type": "InternalError",
            "message": str(e)
        }


def _error_response(message: str) -> dict:
    """
    Standard error response format.
    """
    return {
        "status": "error",
        "dialect": None,
        "type": "ValidationError",
        "message": message
    }
