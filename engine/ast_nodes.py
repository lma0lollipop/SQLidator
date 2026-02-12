"""
AST Node Definitions
--------------------
Defines structure of parsed SQL statements.
"""


class SelectNode:
    def __init__(
        self,
        columns,
        from_table,
        where=None,
        group_by=None,
        having=None,
        order_by=None,
        limit=None
    ):
        self.type = "SELECT"
        self.columns = columns
        self.from_table = from_table
        self.where = where
        self.group_by = group_by
        self.having = having
        self.order_by = order_by
        self.limit = limit

    def __repr__(self):
        return (
            f"SelectNode(columns={self.columns}, "
            f"from={self.from_table}, "
            f"where={self.where}, "
            f"group_by={self.group_by}, "
            f"having={self.having}, "
            f"order_by={self.order_by}, "
            f"limit={self.limit})"
        )


class InsertNode:
    def __init__(
        self,
        table,
        columns,
        values
    ):
        self.type = "INSERT"
        self.table = table
        self.columns = columns
        self.values = values

    def __repr__(self):
        return (
            f"InsertNode(table={self.table}, "
            f"columns={self.columns}, "
            f"values={self.values})"
        )


class DeleteNode:
    def __init__(self, table, where=None):
        self.type = "DELETE"
        self.table = table
        self.where = where

    def __repr__(self):
        return f"DeleteNode(table={self.table}, where={self.where})"


class UpdateNode:
    def __init__(self, table, assignments, where=None):
        self.type = "UPDATE"
        self.table = table
        self.assignments = assignments
        self.where = where

    def __repr__(self):
        return (
            f"UpdateNode(table={self.table}, "
            f"assignments={self.assignments}, "
            f"where={self.where})"
        )
    


class CreateTableNode:
    def __init__(self, table, columns):
        self.type = "CREATE_TABLE"
        self.table = table
        self.columns = columns  # list of dicts

    def __repr__(self):
        return (
            f"CreateTableNode(table={self.table}, "
            f"columns={self.columns})"
        )


class AlterTableNode:
    def __init__(self, table, action):
        self.type = "ALTER_TABLE"
        self.table = table
        self.action = action  # dictionary describing operation

    def __repr__(self):
        return (
            f"AlterTableNode(table={self.table}, "
            f"action={self.action})"
        )


class DropTableNode:
    def __init__(self, table):
        self.type = "DROP_TABLE"
        self.table = table

    def __repr__(self):
        return f"DropTableNode(table={self.table})"


class CreateViewNode:
    def __init__(self, name, query):
        self.type = "CREATE_VIEW"
        self.name = name
        self.query = query  # This will be a SelectNode

    def __repr__(self):
        return f"CreateViewNode(name={self.name}, query={self.query})"


class DropViewNode:
    def __init__(self, name):
        self.type = "DROP_VIEW"
        self.name = name

    def __repr__(self):
        return f"DropViewNode(name={self.name})"
