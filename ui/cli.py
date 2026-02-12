"""
SQLidator CLI
-------------
Supports:
- Direct query input
- .sql file input
- Dialect selection
- Optional AI suggestions (CLI mode)
- Report generation (TXT / JSON / CSV)
- Custom output filename
"""
import sys
import os

# Ensure project root is added to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import argparse

from engine.validator import validate_query
from reports.text_report import generate_text_report
from reports.json_report import generate_json_report
from reports.csv_report import generate_csv_report
from ai.groq_suggester import get_ai_suggestion


def show_banner():
    banner = r"""
   ███████╗ ██████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
   ██╔════╝██╔═══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
   ███████╗██║   ██║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝
   ╚════██║██║▄▄ ██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗
   ███████║╚██████╔╝███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
   ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                           
                    🚀 Modular SQL Validation Engine
    """
    print(banner)


def main():
    show_banner()

    parser = argparse.ArgumentParser(description="SQLidator CLI")

    parser.add_argument("--query", type=str, help="SQL query string")
    parser.add_argument("--file", type=str, help="Path to .sql file")
    parser.add_argument(
        "--dialect",
        type=str,
        default="mysql",
        choices=["mysql", "postgres", "plsql"],
        help="SQL dialect"
    )
    parser.add_argument("--ai", action="store_true",
                        help="Enable AI suggestions (CLI short mode)")
    parser.add_argument("--report", choices=["txt", "json", "csv"],
                        help="Generate report file")
    parser.add_argument("--output", type=str,
                        help="Custom output filename (without extension)")

    args = parser.parse_args()

    # --------------------------------------------------
    # Get Query
    # --------------------------------------------------
    if args.file:
        if not os.path.exists(args.file):
            print("❌ File not found.")
            sys.exit(1)

        with open(args.file, "r", encoding="utf-8") as f:
            query = f.read()

    elif args.query:
        query = args.query

    else:
        print("❌ Provide --query or --file")
        sys.exit(1)

    # --------------------------------------------------
    # Display Query
    # --------------------------------------------------
    print("\n" + "=" * 60)
    print("QUERY BEING VALIDATED:")
    # print("=" * 60)
    print(query)
    print("=" * 60)

    # --------------------------------------------------
    # Validate
    # --------------------------------------------------
    result = validate_query(query, args.dialect)

    # --------------------------------------------------
    # AI (CLI Mode)
    # --------------------------------------------------
    ai_result = None

    if args.ai:
        ai_result = get_ai_suggestion(query, result, mode="cli")

    # --------------------------------------------------
    # Print Validation Result
    # --------------------------------------------------
    print("\nVALIDATION RESULT:")
    print("-" * 60)
    print("Status  :", result.get("status").upper())
    print("Dialect :", result.get("dialect"))
    print("Message :", result.get("message"))

    if result.get("status") == "error":
        print("Type    :", result.get("type"))

    # --------------------------------------------------
    # AI Output
    # --------------------------------------------------
    if args.ai:
        print("\nAI SUGGESTIONS:")
        print("-" * 60)

        if ai_result and ai_result.get("ai_status") == "success":
            print(ai_result.get("ai_message"))
        else:
            print("No AI suggestions available.")

    # --------------------------------------------------
    # Report Generation
    # --------------------------------------------------
    if args.report:

        # Use different AI mode for reports
        report_ai_result = None
        if args.ai:
            if args.report == "json":
                report_ai_result = get_ai_suggestion(query, result, mode="json")
            elif args.report == "csv":
                report_ai_result = get_ai_suggestion(query, result, mode="csv")
            else:
                report_ai_result = get_ai_suggestion(query, result, mode="txt")

        if args.report == "txt":
            report_content = generate_text_report(query, result, report_ai_result)
            extension = "txt"

        elif args.report == "json":
            report_content = generate_json_report(query, result, report_ai_result)
            extension = "json"

        elif args.report == "csv":
            report_content = generate_csv_report(query, result, report_ai_result)
            extension = "csv"

        filename = args.output if args.output else "sqlidator_report"
        full_filename = f"{filename}.{extension}"

        with open(full_filename, "w", encoding="utf-8") as f:
            f.write(report_content)

        print(f"\n📄 Report saved successfully: {os.path.abspath(full_filename)}")


if __name__ == "__main__":
    main()
