"""Regression tests for simple-validator.py status classification.

Locks in the rule that bot-blocking / soft codes are 'needs_manual', NOT
'broken' -- only 404/410 and DNS failures are broken (issue #240).
"""
import pytest

from conftest import load_script

sv = load_script("simple-validator.py")
classify = sv.SimpleValidator.classify_status


@pytest.mark.parametrize("code,status", [
    (200, "valid"),
    (202, "valid"),   # accepted -> resource reachable
    (204, "valid"),
    (206, "valid"),   # ranged GET partial content
    (299, "valid"),
    (301, "redirect"),
    (302, "redirect"),
    (307, "redirect"),
    (308, "redirect"),
    (404, "broken"),
    (410, "broken"),
    # Soft / gatekeeping codes must NOT be broken.
    (403, "needs_manual"),
    (405, "needs_manual"),
    (415, "needs_manual"),
    (418, "needs_manual"),
    (429, "needs_manual"),
    (451, "needs_manual"),
    (500, "needs_manual"),
    (503, "needs_manual"),
])
def test_classify_status(code, status):
    assert classify(code)[0] == status


def test_only_dead_codes_are_broken():
    """No soft code should ever be classified broken."""
    soft = sorted(sv.SimpleValidator.SOFT_CODES) + [500, 502, 503]
    assert all(classify(c)[0] != "broken" for c in soft)
    assert classify(404)[0] == "broken"
    assert classify(410)[0] == "broken"


def test_issue_type_labels():
    assert classify(404)[1] == "not_found"
    assert classify(410)[1] == "gone"
    assert classify(403)[1] == "http_403"
    assert classify(200)[1] is None


def test_dns_error_detection():
    is_dns = sv.SimpleValidator._is_dns_error
    assert is_dns(Exception("Name or service not known")) is True
    assert is_dns(Exception("Connection reset by peer")) is False
