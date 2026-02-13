"""
SQLidator CLI (Parser-Based Version)
------------------------------------
Supports:
- Direct query input
- .sql file input (multiple statements)
- Dialect selection
- Optional AI suggestions
- Report generation (TXT / JSON / CSV)
"""

import sys
import os
import argparse

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from engine.validator import validate_query
from reports.text_report import generate_text_report
from reports.json_report import generate_json_report
from reports.csv_report import generate_csv_report
from ai.groq_suggester import get_ai_suggestion


# ==========================================================
# ASCII Banner
# ==========================================================

def show_banner():
    banner = r"""
   ███████╗ ██████╗ ██╗     ██╗██████╗  █████╗ ████████╗ ██████╗ ██████╗ 
   ██╔════╝██╔═══██╗██║     ██║██╔══██╗██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
   ███████╗██║   ██║██║     ██║██║  ██║███████║   ██║   ██║   ██║██████╔╝
   ╚════██║██║▄▄ ██║██║     ██║██║  ██║██╔══██║   ██║   ██║   ██║██╔══██╗
   ███████║╚██████╔╝███████╗██║██████╔╝██║  ██║   ██║   ╚██████╔╝██║  ██║
   ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
                                                                           
                    🚀 SQLidator Parser Engine
    """
    print(banner)


# ==========================================================
# MAIN FUNCTION
# ==========================================================

def main():
    show_banner()

    parser = argparse.ArgumentParser(description="SQLidator CLI")

    parser.add_argument("--query", type=str, help="SQL query string")
    parser.add_argument("--file", type=str, help="Path to .sql file")
    parser.add_argument(
        "--dialect",
        type=str,
        default="postgres",
        choices=["postgres", "mysql", "plsql"],
        help="SQL dialect"
    )
    parser.add_argument("--ai", action="store_true", help="Enable AI suggestions")
    parser.add_argument("--report", choices=["txt", "json", "csv"], help="Generate report file")
    parser.add_argument("--output", type=str, help="Custom output filename (without extension)")

    args = parser.parse_args()

    # ------------------------------------------------------
    # Load Queries
    # ------------------------------------------------------
    queries = []

    if args.file:
        if not os.path.exists(args.file):
            print("❌ File not found.")
            sys.exit(1)

        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()

        # Split queries by semicolon and strip whitespace
        queries = [q.strip() + ';' for q in content.split(';') if q.strip()]
        print(f"\nFound {len(queries)} queries in file")

    elif args.query:
        queries = [args.query.strip()]

    else:
        print("❌ Provide --query or --file")
        sys.exit(1)

    all_results = []

    # ------------------------------------------------------
    # Process Each Query
    # ------------------------------------------------------
    for idx, query in enumerate(queries, 1):
        print("\n" + "=" * 60)
        print(f"QUERY {idx}:")
        print(query)
        print("=" * 60)

        # Validate query
        result = validate_query(query, args.dialect)
        all_results.append(result)

        # Print result
        print("\nRESULT:")
        print("-" * 60)
        status = result.get("status")
        print("Status  :", status.upper())
        print("Dialect :", result.get("dialect"))
        print("Message :", result.get("message"))
        if status == "error":
            print("Type    :", result.get("type"))

        # Print AST if success
        if status == "success":
            print("\nAST:")
            print("-" * 60)
            ast = result.get("ast")
            if isinstance(ast, list):
                for j, stmt in enumerate(ast, 1):
                    print(f"\nStatement {j}:")
                    print(stmt)
            else:
                print(ast)

        # AI suggestions
        if args.ai:
            print("\nAI SUGGESTIONS:")
            print("-" * 60)
            ai_result = get_ai_suggestion(query, result, mode="cli")
            if ai_result and ai_result.get("ai_status") == "success":
                print(ai_result.get("ai_message"))
            else:
                print("No AI suggestions available.")

    # ------------------------------------------------------
    # Report Generation
    # ------------------------------------------------------
    if args.report:
        report_ai_results = None
        if args.ai:
            # Generate AI suggestions for each query in report mode
            report_ai_results = [
                get_ai_suggestion(q, r, mode=args.report)
                for q, r in zip(queries, all_results)
            ]

        # Generate report content
        if args.report == "txt":
            content = generate_text_report(queries, all_results, report_ai_results)
            extension = "txt"
        elif args.report == "json":
            content = generate_json_report(queries, all_results, report_ai_results)
            extension = "json"
        elif args.report == "csv":
            content = generate_csv_report(queries, all_results, report_ai_results)
            extension = "csv"

        filename = args.output if args.output else "sqlidator_report"
        full_filename = f"{filename}.{extension}"

        with open(full_filename, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"\n📄 Report saved: {os.path.abspath(full_filename)}")


if __name__ == "__main__":
    main()