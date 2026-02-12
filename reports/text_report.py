"""
Professional Text Report Generator
-----------------------------------
Generates clean and structured SQL validation report.
"""

from datetime import datetime


def generate_text_report(query: str, result: dict, ai_result: dict | None = None) -> str:
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = []
        lines.append("=" * 70)
        lines.append("                     SQLidator Report")
        lines.append("=" * 70)
        lines.append(f"Generated On : {timestamp}")
        lines.append(f"Dialect      : {result.get('dialect')}")
        lines.append(f"Status       : {result.get('status').upper()}")
        lines.append("-" * 70)

        # -----------------------------
        # Query Section
        # -----------------------------
        lines.append("YOUR QUERY:")
        lines.append(query)
        lines.append("-" * 70)

        # -----------------------------
        # Validation Section
        # -----------------------------
        lines.append("VALIDATION RESULT:")

        if result.get("status") == "success":
            lines.append(f"Message : {result.get('message')}")
        else:
            lines.append(f"Error Type : {result.get('type')}")
            lines.append(f"Message    : {result.get('message')}")

        lines.append("-" * 70)

        # -----------------------------
        # AI Suggestions Section
        # -----------------------------
        lines.append("AI SUGGESTIONS:")

        if ai_result and ai_result.get("ai_status") == "success":
            lines.append(ai_result.get("ai_message"))
        else:
            lines.append("No AI suggestions available.")

        lines.append("=" * 70)

        return "\n".join(lines)

    except Exception:
        return "Failed to generate text report."
