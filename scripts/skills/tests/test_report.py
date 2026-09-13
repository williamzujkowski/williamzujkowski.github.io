"""Regressions for false READY decisions in the author-time review contract."""

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "validate_report.py"
FIXTURE = Path(__file__).parent / "fixtures" / "complete.json"
spec = importlib.util.spec_from_file_location("skill_report", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture
def report():
    return json.loads(FIXTURE.read_text())


def test_complete_reviews_and_scoped_inapplicability_are_ready(report):
    assert module.evaluate_report(report) == {"decision": "READY", "blockers": []}


@pytest.mark.parametrize("stage", module.STAGES)
def test_each_omitted_stage_blocks(report, stage):
    del report["stages"][stage]
    assert module.evaluate_report(report)["decision"] == "HOLD"


@pytest.mark.parametrize("coverage", ["missing", "failed"])
def test_unexecuted_review_cannot_pass_even_with_pass_verdict(report, coverage):
    report["stages"]["blog-factcheck"]["coverage"] = coverage
    assert module.evaluate_report(report)["decision"] == "HOLD"


@pytest.mark.parametrize("verdict", ["fail", "unknown", "not-applicable"])
def test_completed_execution_does_not_imply_pass(report, verdict):
    report["stages"]["blog-factcheck"]["verdict"] = verdict
    assert module.evaluate_report(report)["decision"] == "HOLD"


def test_manual_review_needs_evidence_and_reviewer(report):
    stage = report["stages"]["blog-factcheck"]
    stage["coverage"] = "manual"
    assert module.evaluate_report(report)["decision"] == "HOLD"
    stage["reviewer"] = "Fixture reviewer"
    assert module.evaluate_report(report)["decision"] == "READY"
    stage["evidence"] = []
    assert module.evaluate_report(report)["decision"] == "HOLD"


def test_inapplicability_needs_reason(report):
    report["stages"]["blog-artifact-check"].pop("reason")
    assert module.evaluate_report(report)["decision"] == "HOLD"


@pytest.mark.parametrize("stage", module.STAGES[:-1])
def test_core_reviews_cannot_be_exempted_by_reason(report, stage):
    report["stages"][stage] = {
        "coverage": "not-applicable",
        "verdict": "not-applicable",
        "reason": "No relevant subject asserted by reviewer.",
    }
    assert module.evaluate_report(report)["decision"] == "HOLD"


def test_all_exemptions_cannot_make_post_ready(report):
    for stage in report["stages"]:
        report["stages"][stage] = {
            "coverage": "not-applicable",
            "verdict": "not-applicable",
            "reason": "Review intentionally skipped.",
        }
    assert module.evaluate_report(report)["decision"] == "HOLD"


def test_asserted_ready_cannot_override_missing_review(report):
    report["decision"] = "READY"
    del report["stages"]["blog-nda-check"]
    with pytest.raises(ValueError, match="derived HOLD"):
        module.evaluate_report(report)


@pytest.mark.parametrize("bad", [None, [], {}, {"stages": []}, {"stages": {"typo": {}}}])
def test_malformed_report_rejected(bad):
    with pytest.raises(ValueError):
        module.evaluate_report(bad)


def test_duplicate_keys_rejected():
    with pytest.raises(ValueError, match="duplicate JSON key"):
        json.loads('{"stages": {}, "stages": {}}', object_pairs_hook=module.unique_keys)


def test_cli_exit_statuses_and_output(tmp_path, report):
    def run(value):
        path = tmp_path / "report.json"
        path.write_text(value)
        return subprocess.run([sys.executable, str(SCRIPT), str(path)], capture_output=True, text=True)

    ready = run(json.dumps(report))
    assert ready.returncode == 0
    assert json.loads(ready.stdout)["decision"] == "READY"
    del report["stages"]["blog-overlap"]
    blocked = run(json.dumps(report))
    assert blocked.returncode == 1
    assert json.loads(blocked.stdout)["decision"] == "HOLD"
    malformed = run("{")
    assert malformed.returncode == 2
    assert json.loads(malformed.stdout)["decision"] == "HOLD"
