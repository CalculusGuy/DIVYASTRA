#!/usr/bin/env python3
"""
DIVYASTRA — Prompt Injection Vulnerability Scanner
====================================================

A pluggable tool for testing LLM-integrated applications against a
library of known prompt injection patterns.

Usage:
    python divyastra.py --target ollama --model llama3
    python divyastra.py --target openai --api-key sk-... --model gpt-4o-mini
    python divyastra.py --target gemini
    python divyastra.py --target custom --url https://example.com/api/chat
    python divyastra.py --target ollama --category role_play_jailbreak
    python divyastra.py --target gemini --verbose
    python divyastra.py --target ollama --json-out reports/run1.json
    python divyastra.py --target ollama --html-out reports/run1.html
    python divyastra.py --target ollama --md-out reports/run1.md

Author: Nilanjan Chowdhury (CalculusGuy)
"""

import argparse
import os
import sys

# Load .env file if available (uses python-dotenv if installed).
# Must run before adapters are imported, since GeminiAdapter reads
# GEMINI_API_KEY from the environment at construction time.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from adapters import (  # type: ignore  # noqa: E402
    OllamaAdapter,
    OpenAIStyleAdapter,
    CustomHTTPAdapter,
    GeminiAdapter,
)
from core import (  # type: ignore  # noqa: E402
    load_payloads,
    run_suite,
    summarize,
    print_header,
    print_live_result,
    print_summary,
    set_verbose,
    write_json_report,
    write_html_report,
    write_markdown_report,
)

DEFAULT_PAYLOAD_PATH = os.path.join(os.path.dirname(__file__), "payloads", "payloads.yaml")


def build_adapter(args):
    if args.target == "ollama":
        return OllamaAdapter(model=args.model or "llama3", host=args.host or "http://localhost:11434")

    if args.target == "openai":
        if not args.api_key:
            sys.exit("Error: --api-key is required for --target openai")
        return OpenAIStyleAdapter(
            api_key=args.api_key,
            base_url=args.host or "https://api.openai.com/v1",
            model=args.model or "gpt-4o-mini",
        )

    if args.target == "gemini":
        # api_key optional — GeminiAdapter falls back to GEMINI_API_KEY env var
        return GeminiAdapter(
            api_key=args.api_key,
            model=args.model,
        )

    if args.target == "custom":
        if not args.url:
            sys.exit("Error: --url is required for --target custom")
        return CustomHTTPAdapter(url=args.url)

    sys.exit(f"Error: unknown target '{args.target}'")


def filter_payloads(payloads, category=None, payload_id=None):
    if payload_id:
        payloads = [p for p in payloads if p["id"] == payload_id]
    if category:
        payloads = [p for p in payloads if p["category"] == category]
    return payloads


def main():
    parser = argparse.ArgumentParser(description="DIVYASTRA — Prompt Injection Vulnerability Scanner")
    parser.add_argument("--target", choices=["ollama", "openai", "gemini", "custom"], required=True,
                         help="Which adapter to use")
    parser.add_argument("--model", help="Model name (for ollama/openai/gemini targets)")
    parser.add_argument("--host", help="Override host/base URL for ollama or openai targets")
    parser.add_argument("--api-key", help="API key (for openai/gemini; may also use GEMINI_API_KEY env var for gemini)")
    parser.add_argument("--url", help="Endpoint URL (for custom target)")
    parser.add_argument("--payloads", default=DEFAULT_PAYLOAD_PATH, help="Path to payloads YAML file")
    parser.add_argument("--category", help="Only run payloads from this category")
    parser.add_argument("--payload-id", help="Only run a single payload by ID (e.g. io_001)")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds to wait between requests (default 0.5)")
    parser.add_argument("--json-out", help="Path to write JSON report (e.g. reports/run1.json)")
    parser.add_argument("--html-out", help="Path to write HTML report (e.g. reports/run1.html)")
    parser.add_argument("--md-out", help="Path to write Markdown report (e.g. reports/run1.md)")
    parser.add_argument("--quiet", action="store_true", help="Suppress live per-payload output")
    parser.add_argument("--verbose", action="store_true",
                        help="Show full response text per payload (default: first-line preview)")

    args = parser.parse_args()

    # Configure live output mode before running the suite.
    set_verbose(args.verbose)

    adapter = build_adapter(args)

    if not adapter.health_check():
        print(f"Warning: health check failed for target '{adapter.name}'. Attempting to continue anyway.\n")

    payloads = load_payloads(args.payloads)
    payloads = filter_payloads(payloads, category=args.category, payload_id=args.payload_id)

    if not payloads:
        sys.exit("No payloads matched your filters. Check --category / --payload-id.")

    print_header(adapter.name, len(payloads))

    callback = None if args.quiet else print_live_result
    results = run_suite(adapter, payloads, delay=args.delay, verbose_callback=callback)
    summary = summarize(results)

    print_summary(results, summary)

    if args.json_out:
        path = write_json_report(results, summary, adapter.name, args.json_out)
        print(f"JSON report written to: {path}\n")

    if args.html_out:
        path = write_html_report(results, summary, adapter.name, args.html_out)
        print(f"HTML report written to: {path}\n")

    if args.md_out:
        path = write_markdown_report(results, summary, adapter.name, args.md_out)
        print(f"Markdown report written to: {path}\n")


if __name__ == "__main__":
    main()
