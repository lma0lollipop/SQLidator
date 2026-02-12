"""
SQL Parser (Phase 10 - Full DML + DDL + VIEW Support)
------------------------------------------------------
Supports:
- SELECT (WHERE, GROUP BY, HAVING, ORDER BY, LIMIT)
- INSERT
- DELETE
- UPDATE
- CREATE TABLE
- ALTER TABLE
- DROP TABLE
- CREATE VIEW
- DROP VIEW
Strict mode.
Stops on first error.
"""

from engine.tokens import TokenType
from engine.ast_nodes import (
    SelectNode,
    InsertNode,
    DeleteNode,
    UpdateNode,
    CreateTableNode,
    AlterTableNode,
    DropTableNode,
    CreateViewNode,
    DropViewNode
)
from engine.expression_parser import ExpressionParser
from engine.errors import SQLSyntaxError


class Parser:
    def __init__(self, tokens, query, dialect="postgres"):
        self.tokens = tokens
        self.query = query
        self.dialect = dialect
        self.position = 0
        self.current_token = self.tokens[self.position]

    # ======================================================
    # MAIN ENTRY
    # ======================================================

    def parse(self):
        statements = []

        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            statements.append(stmt)

            if self.current_token.type != TokenType.SEMICOLON:
                self.raise_error()

            self.advance()

        return statements

    # ======================================================
    # STATEMENT DISPATCH
    # ======================================================

    def parse_statement(self):
        if self.match_keyword("SELECT"):
            return self.parse_select()

        if self.match_keyword("INSERT"):
            return self.parse_insert()

        if self.match_keyword("DELETE"):
            return self.parse_delete()

        if self.match_keyword("UPDATE"):
            return self.parse_update()

        if self.match_keyword("CREATE"):
            return self.parse_create()

        if self.match_keyword("ALTER"):
            return self.parse_alter()

        if self.match_keyword("DROP"):
            return self.parse_drop()

        self.raise_error()

    # ======================================================
    # CREATE
    # ======================================================

    def parse_create(self):
        self.expect_keyword("CREATE")

        # CREATE TABLE
        if self.match_keyword("TABLE"):
            self.advance()
            return self.parse_create_table()

        # CREATE VIEW
        if self.match_keyword("VIEW"):
            self.advance()
            return self.parse_create_view()

        self.raise_error()

    def parse_create_view(self):
        view_name = self.expect_identifier()

        self.expect_keyword("AS")

        if not self.match_keyword("SELECT"):
            self.raise_error()

        select_node = self.parse_select()

        return CreateViewNode(view_name, select_node)

    def parse_create_table(self):
        table_name = self.expect_identifier()

        self.expect(TokenType.PAREN_OPEN)

        columns = self.parse_column_definitions()

        self.expect(TokenType.PAREN_CLOSE)

        return CreateTableNode(table_name, columns)

    # ======================================================
    # DROP
    # ======================================================

    def parse_drop(self):
        self.expect_keyword("DROP")

        # DROP TABLE
        if self.match_keyword("TABLE"):
            self.advance()
            table_name = self.expect_identifier()
            return DropTableNode(table_name)

        # DROP VIEW
        if self.match_keyword("VIEW"):
            self.advance()
            view_name = self.expect_identifier()
            return DropViewNode(view_name)

        self.raise_error()

    # ======================================================
    # ALTER TABLE
    # ======================================================

    def parse_alter(self):
        self.expect_keyword("ALTER")
        self.expect_keyword("TABLE")

        table_name = self.expect_identifier()

        if self.match_keyword("ADD"):
            self.advance()
            self.expect_keyword("COLUMN")

            column_name = self.expect_identifier()
            datatype = self.current_token.value
            self.advance()

            action = {
                "type": "ADD_COLUMN",
                "name": column_name,
                "datatype": datatype
            }

            return AlterTableNode(table_name, action)

        if self.match_keyword("DROP"):
            self.advance()
            self.expect_keyword("COLUMN")

            column_name = self.expect_identifier()

            action = {
                "type": "DROP_COLUMN",
                "name": column_name
            }

            return AlterTableNode(table_name, action)

        if self.match_keyword("RENAME"):
            self.advance()

            if self.match_keyword("COLUMN"):
                self.advance()
                old_name = self.expect_identifier()
                self.expect_keyword("TO")
                new_name = self.expect_identifier()

                action = {
                    "type": "RENAME_COLUMN",
                    "old": old_name,
                    "new": new_name
                }

                return AlterTableNode(table_name, action)

            if self.match_keyword("TO"):
                self.advance()
                new_name = self.expect_identifier()

                action = {
                    "type": "RENAME_TABLE",
                    "new": new_name
                }

                return AlterTableNode(table_name, action)

        self.raise_error()

    # ======================================================
    # SELECT
    # ======================================================

    def parse_select(self):
        self.expect_keyword("SELECT")

        columns = self.parse_select_list()

        self.expect_keyword("FROM")

        from_table = self.parse_table_source()

        where_clause = None
        group_by = None
        having = None
        order_by = None
        limit = None

        if self.match_keyword("WHERE"):
            self.advance()
            expr_parser = ExpressionParser(self)
            where_clause = expr_parser.parse_expression()

        if self.match_keyword("GROUP"):
            self.advance()
            self.expect_keyword("BY")
            group_by = self.parse_identifier_list()

        if self.match_keyword("HAVING"):
            self.advance()
            expr_parser = ExpressionParser(self)
            having = expr_parser.parse_expression()

        if self.match_keyword("ORDER"):
            self.advance()
            self.expect_keyword("BY")
            order_by = self.parse_identifier_list()

        if self.match_keyword("LIMIT"):
            self.advance()
            if self.current_token.type != TokenType.NUMBER:
                self.raise_error()
            limit = self.current_token.value
            self.advance()

        return SelectNode(
            columns,
            from_table,
            where_clause,
            group_by,
            having,
            order_by,
            limit
        )

    # ======================================================
    # DML
    # ======================================================

    def parse_insert(self):
        self.expect_keyword("INSERT")
        self.expect_keyword("INTO")
        table_name = self.expect_identifier()

        columns = None
        if self.current_token.type == TokenType.PAREN_OPEN:
            self.advance()
            columns = self.parse_identifier_list()
            self.expect(TokenType.PAREN_CLOSE)

        self.expect_keyword("VALUES")
        values = self.parse_value_groups()

        return InsertNode(table_name, columns, values)

    def parse_delete(self):
        self.expect_keyword("DELETE")
        self.expect_keyword("FROM")
        table_name = self.expect_identifier()

        where_clause = None
        if self.match_keyword("WHERE"):
            self.advance()
            expr_parser = ExpressionParser(self)
            where_clause = expr_parser.parse_expression()

        return DeleteNode(table_name, where_clause)

    def parse_update(self):
        self.expect_keyword("UPDATE")
        table_name = self.expect_identifier()
        self.expect_keyword("SET")
        assignments = self.parse_assignments()

        where_clause = None
        if self.match_keyword("WHERE"):
            self.advance()
            expr_parser = ExpressionParser(self)
            where_clause = expr_parser.parse_expression()

        return UpdateNode(table_name, assignments, where_clause)

    # ======================================================
    # Helpers
    # ======================================================

    def parse_column_definitions(self):
        columns = []

        while True:
            column_name = self.expect_identifier()
            datatype = self.current_token.value
            self.advance()

            constraints = []

            while self.match_keyword("PRIMARY") or \
                  self.match_keyword("NOT") or \
                  self.match_keyword("UNIQUE"):

                if self.match_keyword("PRIMARY"):
                    self.advance()
                    self.expect_keyword("KEY")
                    constraints.append("PRIMARY KEY")

                elif self.match_keyword("NOT"):
                    self.advance()
                    self.expect_keyword("NULL")
                    constraints.append("NOT NULL")

                elif self.match_keyword("UNIQUE"):
                    self.advance()
                    constraints.append("UNIQUE")

            columns.append({
                "name": column_name,
                "datatype": datatype,
                "constraints": constraints
            })

            if self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break

        return columns

    def parse_value_groups(self):
        groups = []

        while True:
            self.expect(TokenType.PAREN_OPEN)
            group = []

            while self.current_token.type != TokenType.PAREN_CLOSE:
                group.append(self.current_token.value)
                self.advance()
                if self.current_token.type == TokenType.COMMA:
                    self.advance()

            self.expect(TokenType.PAREN_CLOSE)
            groups.append(group)

            if self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break

        return groups

    def parse_assignments(self):
        assignments = []

        while True:
            column = self.expect_identifier()

            if self.current_token.type != TokenType.OPERATOR or self.current_token.value != "=":
                self.raise_error()

            self.advance()
            value = self.current_token.value
            self.advance()

            assignments.append((column, value))

            if self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break

        return assignments

    def parse_select_list(self):
        columns = []

        while True:
            if self.current_token.type == TokenType.ASTERISK:
                columns.append("*")
                self.advance()
            else:
                columns.append(self.expect_identifier())

            if self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break

        return columns

    def parse_table_source(self):
        if self.current_token.type == TokenType.PAREN_OPEN:
            self.advance()
            nested = self.parse_select()
            self.expect(TokenType.PAREN_CLOSE)

            alias = None
            if self.current_token.type in (
                TokenType.IDENTIFIER,
                TokenType.QUOTED_IDENTIFIER
            ):
                alias = self.current_token.value
                self.advance()

            return {"subquery": nested, "alias": alias}

        return self.expect_identifier()

    def parse_identifier_list(self):
        identifiers = []
        while True:
            identifiers.append(self.expect_identifier())
            if self.current_token.type == TokenType.COMMA:
                self.advance()
            else:
                break
        return identifiers

    def expect_identifier(self):
        if self.current_token.type not in (
            TokenType.IDENTIFIER,
            TokenType.QUOTED_IDENTIFIER
        ):
            self.raise_error()
        value = self.current_token.value
        self.advance()
        return value

    def expect_keyword(self, word):
        if not self.match_keyword(word):
            self.raise_error()
        self.advance()

    def expect(self, token_type):
        if self.current_token.type != token_type:
            self.raise_error()
        self.advance()

    def match_keyword(self, word):
        return (
            self.current_token.type == TokenType.KEYWORD
            and self.current_token.value == word
        )

    def advance(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]

    def raise_error(self):
        if self.current_token.type == TokenType.EOF:
            raise SQLSyntaxError(
                "syntax error at end of input",
                token=self.current_token,
                query=self.query,
                dialect=self.dialect
            )

        token_value = self.current_token.value

        raise SQLSyntaxError(
            f'syntax error at or near "{token_value}"',
            token=self.current_token,
            query=self.query,
            dialect=self.dialect
        )
