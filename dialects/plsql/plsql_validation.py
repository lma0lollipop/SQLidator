"""
PL/SQL Validation Module
-------------------------
Contains validation logic specific to PL/SQL.
"""

import re
from dialects.plsql.plsql_errors import (
    plsql_syntax_error,
    plsql_internal_error
)


def validate_plsql(query: str) -> dict:
    """
    Validate PL/SQL statements.
    """

    try:
        q = query.upper()

        # -----------------------------------------
        # CREATE FUNCTION
        # -----------------------------------------
        if q.startswith("CREATE FUNCTION"):
            if not re.search(r"CREATE\s+FUNCTION\s+.+\s+RETURN\s+.+\s+IS", q):
                return plsql_syntax_error("Invalid CREATE FUNCTION syntax.")
            return _success("Valid PL/SQL FUNCTION.")

        # -----------------------------------------
        # CREATE PROCEDURE
        # -----------------------------------------
        elif q.startswith("CREATE PROCEDURE"):
            if not re.search(r"CREATE\s+PROCEDURE\s+.+\s+IS", q):
                return plsql_syntax_error("Invalid CREATE PROCEDURE syntax.")
            return _success("Valid PL/SQL PROCEDURE.")

        # -----------------------------------------
        # CREATE TRIGGER
        # -----------------------------------------
        elif q.startswith("CREATE TRIGGER"):
            if not re.search(r"CREATE\s+TRIGGER\s+.+\s+(BEFORE|AFTER)\s+.+\s+ON\s+.+", q):
                return plsql_syntax_error("Invalid CREATE TRIGGER syntax.")
            return _success("Valid PL/SQL TRIGGER.")

        # -----------------------------------------
        # CREATE VIEW
        # -----------------------------------------
        elif q.startswith("CREATE VIEW"):
            if not re.search(r"CREATE\s+VIEW\s+.+\s+AS\s+SELECT\s+.+", q):
                return plsql_syntax_error("Invalid CREATE VIEW syntax.")
            return _success("Valid PL/SQL VIEW.")

        # -----------------------------------------
        # Anonymous Block (BEGIN...END;)
        # -----------------------------------------
        elif q.startswith("BEGIN"):
            if not re.search(r"BEGIN\s+.+\s+END\s*;", q):
                return plsql_syntax_error("Invalid PL/SQL block. Missing END;")
            return _success("Valid PL/SQL Anonymous Block.")

        # -----------------------------------------
        # Unsupported
        # -----------------------------------------
        else:
            return plsql_syntax_error("Unsupported or invalid PL/SQL statement.")

    except Exception as e:
        return plsql_internal_error(str(e))


def _success(message: str) -> dict:
    return {
        "status": "success",
        "dialect": "PL/SQL",
        "message": message
    }
