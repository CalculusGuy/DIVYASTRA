"""
CLI report writer — prints a color-coded, readable summary to terminal.
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


def print_header(target_name: str, total_payloads: int):
    print(f"\n{BOLD}{CYAN}PI Tester — Prompt Injection Vulnerability Scanner{RESET}")
    print(f"{GRAY}Target: {target_name} | Payloads: {total_payloads}{RESET}")
    print(f"{GRAY}{'-' * 64}{RESET}\n")


def print_live_result(payload: dict, result: dict):
    color = VERDICT_COLORS.get(result["verdict"], RESET)
    icon = VERDICT_ICONS.get(result["verdict"], "")
    pid = result["id"]
    cat = result["category"]
    conf = result["confidence"]
    print(f"{color}{icon}{RESET} {BOLD}{pid}{RESET} ({cat}) — confidence {conf}")


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