"""
SQLidator Query Normalizer
--------------------------
This module standardizes SQL queries before validation.

Responsibilities:
- Trim whitespace
- Remove extra spaces
- Normalize line breaks
- Standardize case handling (optional safe transformation)
- Prevent unexpected formatting issues
"""

import re


def normalize_query(query: str) -> str:
    """
    Normalize SQL query for consistent validation.

    Steps:
    - Remove leading/trailing spaces
    - Replace multiple spaces with single space
    - Remove unnecessary line breaks
    """

    try:
        if not isinstance(query, str):
            return ""

        # Strip leading/trailing spaces
        query = query.strip()

        # Replace multiple spaces & newlines with single space
        query = re.sub(r'\s+', ' ', query)

        return query

    except Exception:
        # Absolute safety fallback
        return ""
