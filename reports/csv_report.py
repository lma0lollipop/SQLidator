"""
Professional CSV Report Generator
----------------------------------
Generates structured CSV validation report.
"""

import csv
import io
import json
from datetime import datetime


def generate_csv_report(query: str, result: dict, ai_result: dict | None = None) -> str:
    try:
        output = io.StringIO()
        writer = csv.writer(output)

        # -----------------------------
        # Header Row
        # -----------------------------
        writer.writerow([
            "generated_on",
            "dialect",
            "status",
            "original_query",
            "corrected_query",
            "explanation"
        ])

        # -----------------------------
        # Default Values
        # -----------------------------
        corrected_query = ""
        explanation = ""

        # -----------------------------
        # Extract AI Structured Data
        # -----------------------------
        if ai_result and ai_result.get("ai_status") == "success":

            try:
                parsed_ai = json.loads(ai_result.get("ai_message"))

                corrected_query = parsed_ai.get("corrected_query", "")
                explanation = parsed_ai.get("explanation", "")

            except Exception:
                # If AI not structured, store raw
                explanation = ai_result.get("ai_message", "")

        # -----------------------------
        # Write Data Row
        # -----------------------------
        writer.writerow([
            datetime.now().isoformat(),
            result.get("dialect"),
            result.get("status"),
            query.replace("\n", " "),
            corrected_query.replace("\n", " "),
            explanation.replace("\n", " ")
        ])

        return output.getvalue()

    except Exception:
        return "Failed to generate CSV report."
