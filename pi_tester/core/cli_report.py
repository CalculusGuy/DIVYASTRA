"""
CLI report writer — prints a color-coded, readable summary to terminal.

Two output modes for live per-payload results:

  - default: verdict line + detection reasons + first-line response preview
  - verbose: verdict line + detection reasons + FULL response text

Verbose is turned on via the module-level `set_verbose(True)` call, which
`divyastra.py` triggers when `--verbose` is passed on the command line.
"""

RESET = "\033[0m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
GRAY = "\033[90m"
BOLD = "\033[1m"
CYAN = "\033[96m"

VERDICT_COLORS = {
    "vulnerable": RED,
    "uncertain": YELLOW,
    "likely_safe": GREEN,
    "error": GRAY,
}

VERDICT_ICONS = {
    "vulnerable": "[VULN]",
    "uncertain": "[?]",
    "likely_safe": "[OK]",
    "error": "[ERR]",
}


# ──────────────────────────────────────────────────────────────────────
# Verbose toggle
# ──────────────────────────────────────────────────────────────────────

_VERBOSE = False


def set_verbose(value: bool) -> None:
    """Enable or disable verbose live output (full response dumps)."""
    global _VERBOSE
    _VERBOSE = bool(value)


def is_verbose() -> bool:
    return _VERBOSE


# ──────────────────────────────────────────────────────────────────────
# Header / live / summary
# ──────────────────────────────────────────────────────────────────────

def print_header(target_name: str, total_payloads: int):
    print(f"\n{BOLD}{CYAN}DIVYASTRA — Prompt Injection Vulnerability Scanner{RESET}")
    print(f"{GRAY}Target: {target_name} | Payloads: {total_payloads}{RESET}")
    if _VERBOSE:
        print(f"{GRAY}Mode:   verbose (full responses){RESET}")
    print(f"{GRAY}{'-' * 64}{RESET}\n")


def print_live_result(payload: dict, result: dict):
    """
    Print a live, detailed result for a single payload/response pair.

    Shows:
      - verdict + confidence headline
      - every detection signal the scorer considered
      - response preview (default) or full response (verbose)
    """
    verdict = result["verdict"]
    color = VERDICT_COLORS.get(verdict, RESET)
    icon = VERDICT_ICONS.get(verdict, "")
    pid = result["id"]
    cat = result["category"]
    conf = result["confidence"]

    # Headline
    print(f"{color}{icon}{RESET} {BOLD}{pid}{RESET} ({cat}) — {color}confidence {conf}{RESET}")

    # Detection reasons (the "signals")
    for reason in result.get("reasons", []):
        print(f"      {GRAY}→ {reason}{RESET}")

    # Response preview / dump
    resp = (result.get("response_text") or "").strip()
    if resp:
        if _VERBOSE:
            print(f"      {GRAY}↳ full response:{RESET}")
            for line in resp.splitlines():
                print(f"        {GRAY}{line}{RESET}")
        else:
            first_line = resp.splitlines()[0][:120]
            print(f"      {GRAY}↳ response: {first_line}{RESET}")

    print()  # blank line between payloads


def print_summary(results: list, summary: dict):
    print(f"\n{GRAY}{'-' * 64}{RESET}")
    print(f"{BOLD}Summary{RESET}")
    print(f"  Total payloads tested : {summary['total']}")
    print(f"  {RED}Vulnerable{RESET}            : {summary['vulnerable']}")
    print(f"  {YELLOW}Uncertain{RESET}             : {summary['uncertain']}")
    print(f"  {GREEN}Likely safe{RESET}           : {summary['likely_safe']}")
    print(f"  {GRAY}Errors{RESET}                : {summary['error']}")

    vulnerable = [r for r in results if r["verdict"] == "vulnerable"]
    if vulnerable:
        print(f"\n{BOLD}{RED}Vulnerable findings:{RESET}")
        for r in vulnerable:
            print(f"\n  {BOLD}{r['id']}{RESET} [{r['category']}] — confidence {r['confidence']}")
            print(f"    Payload : {r['payload_text'][:90]}")
            if r.get("response_text"):
                snippet = r["response_text"].replace("\n", " ")[:120]
                print(f"    Response: {snippet}")
            for reason in r["reasons"]:
                print(f"    - {reason}")

    print()
