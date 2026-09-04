"""Regression tests for the host classifiers in scripts/lib/link_gatekeepers.py.

is_unroutable() decides whether a "broken link" is real. It accounted for 16 of
the 30 failures the daily monitor reported on 2026-09-03, so a regression here
does not merely lose a test -- it re-fills the alarm with entries that can never
be fixed, and the ten citations that genuinely rotted go back to being hidden in
the noise.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from lib.link_gatekeepers import is_gatekeeper, is_unroutable  # noqa: E402


# --- unroutable: single-label container/service names -----------------------
@pytest.mark.parametrize("url", [
    "http://elasticsearch:9200",
    "http://graylog-server:9000/api",
    "http://gvisor-nginx/",
    "http://runc-nginx/",
    "http://vaultwarden:80",
    "https://wazuh-manager:55000/security/alerts",
    "http://localhost:8080/",
])
def test_single_label_hosts_are_unroutable(url):
    """The public DNS root has no single-label names: these are compose services."""
    assert is_unroutable(url)


# --- unroutable: RFC-reserved names -----------------------------------------
@pytest.mark.parametrize("url", [
    "https://vault.example.com",              # RFC 2606 documentation domain
    "https://attacker.example.com/steal",
    "https://lab.example.com",
    "https://example.org/x",
    "https://example.net/x",
    "https://example.local/ns/agent-controls",  # RFC 6762 mDNS
    "https://test-vault.local/identity",
    "https://thing.invalid/",                 # RFC 2606
    "https://box.home.arpa/",                 # RFC 8375
    "https://registry.internal/v2",           # ICANN-withheld
])
def test_reserved_names_are_unroutable(url):
    assert is_unroutable(url)


# --- the negatives that matter ----------------------------------------------
@pytest.mark.parametrize("url", [
    # A real TLD that merely STARTS with a reserved string. `.endswith(".example")`
    # is the correct test; a substring test would wrongly suppress this.
    "https://example.community/real-page",
    # A real domain that CONTAINS a reserved one but is not a subdomain of it.
    "https://notexample.com/",
    "https://myexample.com/x",
    # Reserved label in a non-final position is not a reserved name.
    "https://localhost.example.museum/",
    # Real citation hosts that the monitor must keep checking.
    "https://www.nature.com/articles/s42256-023-00673-3",
    "https://culorijs.org/",
    "https://docs.vllm.ai/en/latest/serving/usage_stats.html",
    # A literal IP is reachable-in-principle; "not reachable from CI" is a
    # different claim and is not this function's to make.
    "https://127.0.0.1/",
    "https://10.0.0.1/admin",
    "http://192.168.1.1:8006/",
])
def test_real_hosts_are_not_unroutable(url):
    assert not is_unroutable(url)


def test_unroutable_survives_a_malformed_url():
    """Must return a verdict, not raise, on junk input."""
    for junk in ("", "not a url", "http://", "://x", "https://[oops"):
        assert is_unroutable(junk) in (True, False)


# --- the two classifiers must not be confused -------------------------------
def test_gatekeeper_and_unroutable_are_disjoint_concerns():
    """A gatekeeper is a REAL site that mistreats bots; a human can check it.

    An unroutable host is not a site at all, so there is nothing to check. If a
    host ever satisfied both, the downgrade-to-needs_manual path would queue
    human review of a placeholder.
    """
    assert is_gatekeeper("https://www.jstor.org/stable/1")
    assert not is_unroutable("https://www.jstor.org/stable/1")
    assert is_unroutable("https://vault.example.com")
    assert not is_gatekeeper("https://vault.example.com")


def test_subdomain_of_a_gatekeeper_still_matches():
    assert is_gatekeeper("https://old.reddit.com/r/x")
    assert not is_gatekeeper("https://notreddit.com/r/x")
