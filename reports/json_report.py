"""
Professional JSON Report Generator
-----------------------------------
Generates structured JSON validation report.
"""

import json
from datetime import datetime


def generate_json_report(query: str, result: dict, ai_result: dict | None = None) -> str:
    try:
        report = {
            "metadata": {
                "generated_on": datetime.now().isoformat(),
                "dialect": result.get("dialect"),
                "status": result.get("status")
            },
            "query": query,
            "validation": {
                "message": result.get("message"),
                "error_type": result.get("type") if result.get("status") == "error" else None
            },
            "ai_suggestions": None
        }

        # -----------------------------
        # AI Structured Handling
        # -----------------------------
        if ai_result and ai_result.get("ai_status") == "success":

            # Try to parse AI JSON if returned in JSON mode
            try:
                parsed_ai = json.loads(ai_result.get("ai_message"))
                report["ai_suggestions"] = parsed_ai
            except Exception:
                # If parsing fails, store as plain text
                report["ai_suggestions"] = {
                    "raw_output": ai_result.get("ai_message")
                }

        return json.dumps(report, indent=4)

    except Exception:
        return json.dumps({
            "error": "Failed to generate JSON report."
        }, indent=4)
