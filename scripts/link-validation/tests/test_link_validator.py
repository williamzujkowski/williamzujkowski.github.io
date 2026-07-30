"""Regression tests for link-validator.py HTTP status classification.

Locks in that anti-bot / rate-limit codes (202/418/429/999) are 'restricted'
(unverifiable), NOT 'broken' -- only 404 and 5xx are broken. This is the
validator the citation-validation workflow actually runs; IEEE Xplore's 202/418
bot challenges were inflating the broken count (issue #391, extends #366).
"""
import pytest

from conftest import load_script

lv = load_script("link-validator.py")
classify = lv.LinkValidator.classify_http_status


@pytest.mark.parametrize("code,expected", [
    (200, "valid"),
    (404, "broken"),
    (410, "broken"),   # falls through the <500 else -> broken
    (403, "restricted"),
    (401, "restricted"),
    (202, "restricted"),   # IEEE anti-bot "Accepted" stall
    (418, "restricted"),   # IEEE "I'm a teapot" anti-bot
    (429, "restricted"),   # rate limited
    (999, "restricted"),   # LinkedIn / non-standard anti-bot
    (500, "broken"),
    (503, "broken"),
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
    assert classify(500)[0] == "broken"
