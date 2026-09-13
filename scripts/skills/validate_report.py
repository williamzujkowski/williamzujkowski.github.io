#!/usr/bin/env python3
"""Check author-time review coverage, not the truth of a review's evidence."""

import argparse
import json
from pathlib import Path

STAGES = (
    "blog-overlap",
    "blog-factcheck",
    "blog-llm-tells",
    "blog-nda-check",
    "blog-argument-shape",
    "blog-visuals",
    "blog-artifact-check",
)
COVERAGE = {"completed", "manual", "not-applicable", "missing", "failed"}
VERDICTS = {"pass", "fail", "unknown", "not-applicable"}


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def evaluate_report(report):
    """Return READY/HOLD and blockers; raise ValueError for malformed reports.

    Coverage describes execution. Verdict describes findings. Completed reviews
    may fail, and unavailable reviewers must not be reported as clean reviews.
    """
    if not isinstance(report, dict) or not isinstance(report.get("stages"), dict):
        raise ValueError("report must contain a stages object")
    stages = report["stages"]
    unknown = set(stages) - set(STAGES)
    if unknown:
        raise ValueError(f"unknown stages: {', '.join(sorted(unknown))}")
    blockers = []
    for name in STAGES:
        stage = stages.get(name)
        if stage is None:
            blockers.append(f"{name}: missing review")
            continue
        if not isinstance(stage, dict):
            raise ValueError(f"{name}: stage must be an object")
        coverage = stage.get("coverage")
        verdict = stage.get("verdict")
        if not isinstance(coverage, str) or coverage not in COVERAGE:
            raise ValueError(f"{name}: invalid coverage")
        if not isinstance(verdict, str) or verdict not in VERDICTS:
            raise ValueError(f"{name}: invalid verdict")
        evidence = stage.get("evidence", [])
        if not isinstance(evidence, list) or any(not nonempty(item) for item in evidence):
            raise ValueError(f"{name}: evidence must be a list of nonempty strings")
        if coverage in {"missing", "failed"}:
            blockers.append(f"{name}: review {coverage}")
        elif coverage == "not-applicable":
            if name != "blog-artifact-check":
                blockers.append(f"{name}: this stage requires review, including an inventory")
            elif verdict != "not-applicable" or not nonempty(stage.get("reason")):
                blockers.append(f"{name}: not-applicable needs matching verdict and reason")
        else:
            if verdict != "pass":
                blockers.append(f"{name}: verdict {verdict}")
            if not evidence:
                blockers.append(f"{name}: no review evidence")
            if coverage == "manual" and not nonempty(stage.get("reviewer")):
                blockers.append(f"{name}: manual review needs reviewer attribution")
    decision = "HOLD" if blockers else "READY"
    if "decision" in report and report["decision"] != decision:
        raise ValueError(f"declared decision does not match derived {decision}")
    return {"decision": decision, "blockers": blockers}


def unique_keys(pairs):
    """Reject ambiguous JSON instead of silently taking a duplicate's last value."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    try:
        report = json.loads(args.report.read_text(encoding="utf-8"), object_pairs_hook=unique_keys)
        result = evaluate_report(report)
    except (OSError, UnicodeError, ValueError) as error:
        print(json.dumps({"decision": "HOLD", "error": str(error)}))
        return 2
    print(json.dumps(result, indent=2))
    return 0 if result["decision"] == "READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
