"""Regression tests for link-validator.py HTTP status classification.

Locks in that only a genuinely dead resource (404/410) is 'broken'. Everything
else -- bot challenges, rate limits, WAF rejections, paywalls and 5xx -- is
'restricted' (unverifiable, advisory).

This is the validator the citation-validation workflow actually runs, and it had
drifted from simple-validator.py's taxonomy: 400 and 5xx were both classified
broken. Measured false positives from the 2026-08-17 report:

  ai.meta.com/blog/deepfake-detection-challenge-results...  400  page is live
  tinyml.org                                                503  transient
  infonomics-society.org/icitst-2024/...                    500  origin erroring

A 5xx means the origin answered and erred. That is a bad afternoon for the
publisher, not a dead citation, and classifying it as broken feeds live sources
into the auto-repair queue.
"""
import pytest
from conftest import load_script

lv = load_script("link-validator.py")
classify = lv.LinkValidator.classify_http_status


@pytest.mark.parametrize("code,expected", [
    (200, "valid"),
    (404, "broken"),
    (410, "broken"),   # Gone -- the one non-404 that really means dead
    (403, "restricted"),
    (401, "restricted"),
    (202, "restricted"),   # IEEE anti-bot "Accepted" stall
    (418, "restricted"),   # IEEE "I'm a teapot" anti-bot
    (429, "restricted"),   # rate limited
    (999, "restricted"),   # LinkedIn / non-standard anti-bot
    (400, "restricted"),   # ai.meta.com rejects non-browser clients this way
    (405, "restricted"),   # HEAD not allowed
    (451, "restricted"),   # legal block -- the resource exists
    (500, "restricted"),   # origin erroring != citation dead
    (503, "restricted"),   # transient unavailability
])
def test_classify_http_status(code, expected):
    assert classify(code)[0] == expected


def test_antibot_codes_are_never_broken():
    """The #391 false positives: bot challenges must not read as broken."""
    for code in sorted(lv.LinkValidator.ANTIBOT_CODES):
        status, issue_type = classify(code)
        assert status == "restricted"
        assert issue_type == f"http_{code}"


def test_200_variants():
    assert classify(200) == ("valid", None)
    assert classify(200, has_paywall=True) == ("restricted", "paywall")
    assert classify(200, is_redirect=True) == ("redirect", "redirect")


def test_genuinely_dead_stays_broken():
    assert classify(404)[0] == "broken"
    assert classify(410)[0] == "broken"


def test_only_dead_codes_are_broken():
    """The taxonomy in one assertion: 404 and 410, and nothing else."""
    broken = {c for c in range(200, 600) if classify(c)[0] == "broken"}
    assert broken == {404, 410}


def test_matches_simple_validator_taxonomy():
    """The two validators must not disagree about what 'broken' means.

    They drifted once already: the #391 anti-bot fix landed on simple-validator
    while CI ran link-validator.
    """
    sv = load_script("simple-validator.py")
    for code in (200, 202, 301, 400, 403, 404, 410, 429, 451, 500, 503):
        a = classify(code)[0]
        b = sv.SimpleValidator.classify_status(code)[0]
        assert (a == "broken") == (b == "broken"), f"disagree on {code}: {a} vs {b}"
