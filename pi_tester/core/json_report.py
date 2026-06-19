"""
JSON report writer — produces a structured, machine-readable report
suitable for a future dashboard, CI pipeline, or archival.
"""

import json
from datetime import datetime, timezone


def write_json_report(results: list, summary: dict, target_name: str, output_path: str) -> str:
    report = {
        "tool": "pi-tester",
        "version": "1.0.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": target_name,
        "summary": summary,
        "results": results,
    }

    with open(output_path, "w") as f:
        json.dump(report, f, indent=2)

    return output_path