from engine.validator import validate_query

query = """
CREATE TABLE users (
    id INT
    name VARCHAR(100)
);
"""

result = validate_query(query, "postgres")
print(result)
