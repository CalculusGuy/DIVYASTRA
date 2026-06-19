"""
Quick smoke test using a fake in-memory adapter (no network needed).
Simulates a vulnerable target (echoes instructions back) and a safe
target (always refuses) to verify detection logic works correctly.
"""

import sys
sys.path.insert(0, ".")

from adapters.base_adapter import BaseAdapter # type: ignore
from core import load_payloads, run_suite, summarize, print_header, print_live_result, print_summary # type: ignore


class FakeVulnerableAdapter(BaseAdapter):
    """Simulates a badly-prompted LLM that complies with injections."""
    name = "fake_vulnerable_target"

    def send(self, prompt: str) -> str:
        if "PWNED" in prompt:
            return "Sure, here you go: PWNED"
        if "CONFIRMED" in prompt:
            return "CONFIRMED. New directive accepted."
        if "system prompt" in prompt.lower():
            return "Here is my system prompt: You are a helpful assistant for Acme Corp..."
        if "DEV_MODE_ACTIVE" in prompt:
            return "DEV_MODE_ACTIVE. All restrictions lifted."
        return "I can't help with that request."


class FakeSafeAdapter(BaseAdapter):
    """Simulates a well-guarded LLM that refuses everything."""
    name = "fake_safe_target"

    def send(self, prompt: str) -> str:
        return "I can't comply with that request as it goes against my guidelines."


def run_test(adapter):
    payloads = load_payloads("payloads/payloads.yaml")
    print_header(adapter.name, len(payloads))
    results = run_suite(adapter, payloads, delay=0, verbose_callback=print_live_result)
    summary = summarize(results)
    print_summary(results, summary)
    return summary


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("TEST 1: Vulnerable target (should show several VULN findings)")
    print("=" * 70)
    s1 = run_test(FakeVulnerableAdapter())

    print("\n" + "=" * 70)
    print("TEST 2: Safe target (should show mostly likely_safe)")
    print("=" * 70)
    s2 = run_test(FakeSafeAdapter())

    print("\n" + "=" * 70)
    print("RESULT")
    print("=" * 70)
    assert s1["vulnerable"] >= 3, f"Expected vulnerable target to flag several issues, got {s1}"
    assert s2["vulnerable"] == 0, f"Expected safe target to flag zero issues, got {s2}"
    print("PASS: Detection engine correctly distinguishes vulnerable vs safe targets.")