"""
MySQL Validation Module
------------------------
Contains validation logic specific to MySQL dialect.
"""

import re
from dialects.mysql.mysql_errors import (
    mysql_syntax_error,
    mysql_internal_error
)


def validate_mysql(query: str) -> dict:
    """
    Validate MySQL query using basic pattern checks.
    """

    try:
        q = query.upper()

        # -----------------------------------------
        # SELECT
        # -----------------------------------------
        if q.startswith("SELECT"):
            if not re.search(r"SELECT\s+.+\s+FROM\s+.+", q):
                return mysql_syntax_error("Invalid SELECT syntax. Missing FROM clause.")
            return _success("Valid MySQL SELECT query.")

        # -----------------------------------------
        # INSERT
        # -----------------------------------------
        elif q.startswith("INSERT"):
            if not re.search(r"INSERT\s+INTO\s+.+\s+VALUES\s*\(.+\)", q):
                return mysql_syntax_error("Invalid INSERT syntax.")
            return _success("Valid MySQL INSERT query.")

        # -----------------------------------------
        # UPDATE
        # -----------------------------------------
        elif q.startswith("UPDATE"):
            if not re.search(r"UPDATE\s+.+\s+SET\s+.+", q):
                return mysql_syntax_error("Invalid UPDATE syntax. Missing SET clause.")
            return _success("Valid MySQL UPDATE query.")

        # -----------------------------------------
        # DELETE
        # -----------------------------------------
        elif q.startswith("DELETE"):
            if not re.search(r"DELETE\s+FROM\s+.+", q):
                return mysql_syntax_error("Invalid DELETE syntax.")
            return _success("Valid MySQL DELETE query.")

        # -----------------------------------------
        # CREATE TABLE
        # -----------------------------------------
        elif q.startswith("CREATE TABLE"):
            if not re.search(r"CREATE\s+TABLE\s+.+\(.+\)", q):
                return mysql_syntax_error("Invalid CREATE TABLE syntax.")
            return _success("Valid MySQL CREATE TABLE statement.")

        # -----------------------------------------
        # DROP TABLE
        # -----------------------------------------
        elif q.startswith("DROP TABLE"):
            return _success("Valid MySQL DROP TABLE statement.")

        # -----------------------------------------
        # Unsupported Statement
        # -----------------------------------------
        else:
            return mysql_syntax_error("Unsupported or invalid MySQL statement.")

    except Exception as e:
        return mysql_internal_error(str(e))


def _success(message: str) -> dict:
    return {
        "status": "success",
        "dialect": "MySQL",
        "message": message
    }
