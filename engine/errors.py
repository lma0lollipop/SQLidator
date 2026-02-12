"""
SQL Error Formatting System
----------------------------
Generates SQL-style syntax errors.
Supports PostgreSQL-style and MySQL-style formatting.
"""

class SQLSyntaxError(Exception):
    def __init__(self, message, token=None, query=None, dialect="postgres"):
        self.message = message
        self.token = token
        self.query = query
        self.dialect = dialect
        super().__init__(self.format_error())

    def format_error(self):
        if not self.token or not self.query:
            return f"ERROR: {self.message}"

        if self.dialect.lower() == "mysql":
            return self._mysql_format()
        else:
            return self._postgres_format()

    def _postgres_format(self):
        line = self.token.line
        column = self.token.column
        lines = self.query.split("\n")

        error_line = lines[line - 1] if line <= len(lines) else ""
        pointer = " " * (column - 1) + "^"

        return (
            f"ERROR:  {self.message}\n"
            f"LINE {line}: {error_line}\n"
            f"{' ' * (6 + len(str(line)))}{pointer}"
        )

    def _mysql_format(self):
        line = self.token.line

        return (
            f"ERROR 1064 (42000): You have an error in your SQL syntax;\n"
            f"near '{self.token.value}' at line {line}"
        )
