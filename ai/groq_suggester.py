"""
Groq AI Suggestion Engine
--------------------------
Supports multiple output modes:
- cli       → short plain text (for terminal)
- markdown  → formatted markdown (for Streamlit)
- json      → structured JSON response
- csv       → single CSV row
- txt       → clean readable text
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "llama-3.3-70b-versatile"


def get_ai_suggestion(query: str, validation_result: dict, mode="cli") -> dict:

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {
            "ai_status": "disabled",
            "ai_message": "No AI suggestions available."
        }

    try:
        prompt = build_prompt(query, validation_result, mode)

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": MODEL_NAME,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        response = requests.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.status_code != 200:
            return {
                "ai_status": "error",
                "ai_message": "No AI suggestions available."
            }

        data = response.json()
        suggestion = data["choices"][0]["message"]["content"]

        return {
            "ai_status": "success",
            "ai_message": suggestion.strip()
        }

    except Exception:
        return {
            "ai_status": "error",
            "ai_message": "No AI suggestions available."
        }


def build_prompt(query: str, validation_result: dict, mode="cli"):

    status = validation_result.get("status")
    message = validation_result.get("message")

    # -------------------------------------
    # CLI MODE (Very Short + Strict Format)
    # -------------------------------------
    if mode == "cli":
        return f"""
You are a SQL expert.

SQL Query:
{query}

Validation:
Status: {status}
Message: {message}

Respond in STRICT plain text using this exact format:

Your Query:
{query}

Corrected Version:
<corrected query>

Explanation:
<short 1-2 sentence reason>

No markdown. No tables. Keep it short.
"""

    # -------------------------------------
    # MARKDOWN MODE (For Streamlit)
    # -------------------------------------
    if mode == "markdown":
        return f"""
You are a senior SQL expert.

Provide structured markdown response.

Include:
- Explanation
- Corrected version in SQL code block
- Short improvements section

SQL Query:
{query}

Validation:
{message}
"""

    # -------------------------------------
    # JSON MODE
    # -------------------------------------
    if mode == "json":
        return f"""
Return strictly valid JSON.

Fields:
original_query
corrected_query
explanation
improvements

SQL Query:
{query}

Validation:
{message}
"""

    # -------------------------------------
    # CSV MODE
    # -------------------------------------
    if mode == "csv":
        return f"""
Return response in this CSV format:

original_query,corrected_query,short_explanation

SQL Query:
{query}

Validation:
{message}
"""

    # -------------------------------------
    # TXT MODE
    # -------------------------------------
    return f"""
Provide clean readable explanation.

Format:

Your Query:
{query}

Corrected Version:
<corrected query>

Explanation:
<short explanation>

Improvements:
<bullet style text>
"""
