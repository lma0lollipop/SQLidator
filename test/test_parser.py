from engine.lexer import Lexer
from engine.parser import Parser

query = """
DROP TABE users;
"""

try:
    lexer = Lexer(query)
    tokens = lexer.tokenize()

    parser = Parser(tokens, query)
    ast = parser.parse()

    for stmt in ast:
        print(stmt)

except Exception as e:
    print(e)
