import json
from dataclasses import asdict
from pathlib import Path

from scanner.analyzer import AuthorizationResult


def write_json_report(
    results: list[AuthorizationResult],
    output_path: str = "research/report.json",
) -> None:

    path = Path(output_path)
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    findings = []

    finding_number = 1

    for result in results:

        if result.finding == "NONE":
            continue

        findings.append(
            {
                "finding_id": f"API-{finding_number:03d}",
                "endpoint": result.endpoint,
                "method": result.method,
                "role": result.role,
                "expected": result.expected,
                "observed": result.observed,
                "category": result.finding,
                "status_code": result.status_code,
                "confidence": "high",
            }
        )

        finding_number += 1

    report = {
        "findings": findings,
        "summary": {
            "total_cases": len(results),
            "findings": len(findings),
            "bola": sum(
                1
                for item in findings
                if item["category"] == "BOLA"
            ),
            "bfla": sum(
                1
                for item in findings
                if item["category"] == "BFLA"
            ),
        },
    }

    path.write_text(
        json.dumps(
            report,
            indent=2,
        ),
        encoding="utf-8",
    )
