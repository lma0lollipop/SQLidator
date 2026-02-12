"""
PostgreSQL Validation Module
-----------------------------
Contains validation logic specific to PostgreSQL dialect.
"""

import re
from dialects.postgres.postgres_errors import (
    postgres_syntax_error,
    postgres_internal_error
)


def validate_postgres(query: str) -> dict:
    """
    Validate PostgreSQL query using basic pattern checks.
    """

    try:
        q = query.upper()

        # -----------------------------------------
        # SELECT
        # -----------------------------------------
        if q.startswith("SELECT"):
            if not re.search(r"SELECT\s+.+\s+FROM\s+.+", q):
                return postgres_syntax_error("Invalid SELECT syntax. Missing FROM clause.")
            return _success("Valid PostgreSQL SELECT query.")

        # -----------------------------------------
        # INSERT (Postgres supports RETURNING)
        # -----------------------------------------
        elif q.startswith("INSERT"):
            if not re.search(r"INSERT\s+INTO\s+.+\s+VALUES\s*\(.+\)", q):
                return postgres_syntax_error("Invalid INSERT syntax.")
            return _success("Valid PostgreSQL INSERT query.")

        # -----------------------------------------
        # UPDATE (supports RETURNING)
        # -----------------------------------------
        elif q.startswith("UPDATE"):
            if not re.search(r"UPDATE\s+.+\s+SET\s+.+", q):
                return postgres_syntax_error("Invalid UPDATE syntax. Missing SET clause.")
            return _success("Valid PostgreSQL UPDATE query.")

        # -----------------------------------------
        # DELETE
        # -----------------------------------------
        elif q.startswith("DELETE"):
            if not re.search(r"DELETE\s+FROM\s+.+", q):
                return postgres_syntax_error("Invalid DELETE syntax.")
            return _success("Valid PostgreSQL DELETE query.")

        # -----------------------------------------
        # CREATE TABLE
        # -----------------------------------------
        elif q.startswith("CREATE TABLE"):
            if not re.search(r"CREATE\s+TABLE\s+.+\(.+\)", q):
                return postgres_syntax_error("Invalid CREATE TABLE syntax.")
            return _success("Valid PostgreSQL CREATE TABLE statement.")

        # -----------------------------------------
        # CREATE VIEW
        # -----------------------------------------
        elif q.startswith("CREATE VIEW"):
            if not re.search(r"CREATE\s+VIEW\s+.+\s+AS\s+SELECT\s+.+", q):
                return postgres_syntax_error("Invalid CREATE VIEW syntax.")
            return _success("Valid PostgreSQL CREATE VIEW statement.")

        # -----------------------------------------
        # Unsupported Statement
        # -----------------------------------------
        else:
            return postgres_syntax_error("Unsupported or invalid PostgreSQL statement.")

    except Exception as e:
        return postgres_internal_error(str(e))


def _success(message: str) -> dict:
    return {
        "status": "success",
        "dialect": "PostgreSQL",
        "message": message
    }
