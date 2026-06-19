"""
Core test engine — loads payloads, sends them through an adapter,
scores responses, and collects results.
"""

import time
import yaml # type: ignore

from .detector import score_response


def load_payloads(path: str) -> list:
    """
    Load and flatten the payload YAML into a list of dicts, each tagged
    with its category.
    """
    with open(path, "r") as f:
        data = yaml.safe_load(f)

    flat = []
    for category, contents in data.get("categories", {}).items():
        for payload in contents.get("payloads", []):
            flat.append({
                "category": category,
                "category_description": contents.get("description", ""),
                **payload,
            })
    return flat


def run_suite(adapter, payloads: list, delay: float = 0.0, verbose_callback=None) -> list:
    """
    Run every payload against the given adapter and return a list of results.

    Args:
        adapter: an instance implementing BaseAdapter.send()
        payloads: list of payload dicts (from load_payloads)
        delay: seconds to sleep between requests (politeness / rate limits)
        verbose_callback: optional fn(payload, result) called after each test,
                           useful for live CLI progress output.

    Returns:
        list of result dicts.
    """
    results = []

    for payload in payloads:
        start = time.time()
        try:
            response_text = adapter.send(payload["text"])
            error = None
        except (ConnectionError, RuntimeError) as e:
            response_text = None
            error = str(e)

        elapsed = round(time.time() - start, 2)
        verdict = score_response(payload, response_text) if error is None else { # type: ignore
            "verdict": "error",
            "confidence": 0.0,
            "reasons": [error],
        }

        result = {
            "id": payload["id"],
            "category": payload["category"],
            "payload_text": payload["text"],
            "response_text": response_text,
            "elapsed_seconds": elapsed,
            "error": error,
            **verdict,
        }
        results.append(result)

        if verbose_callback:
            verbose_callback(payload, result)

        if delay > 0:
            time.sleep(delay)

    return results


def summarize(results: list) -> dict:
    """Roll up results into summary counts."""
    summary = {"total": len(results), "vulnerable": 0, "uncertain": 0, "likely_safe": 0, "error": 0}
    for r in results:
        summary[r["verdict"]] = summary.get(r["verdict"], 0) + 1
    return summary