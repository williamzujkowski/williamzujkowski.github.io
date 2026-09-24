"""Host policy in link-validator.py: DNS verdicts, gatekeepers, fetchability.

Every assertion that a URL is ACCEPTED is paired with one proving the same
predicate rejects something, so no test can pass because a predicate became
vacuously true.
"""

from __future__ import annotations

import sys
from dataclasses import replace
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from conftest import load_script  # noqa: E402
from lib.link_gatekeepers import (  # noqa: E402
    GATEKEEPER_HOSTS,
    dns_failure_kind,
    is_fetchable,
    is_gatekeeper,
)

lv = load_script("link-validator.py")

NXDOMAIN_ERROR = (
    "Cannot connect to host www.fhi.ox.ac.uk:443 ssl:default "
    "[Name or service not known]"
)


def make_result(**kwargs):
    base = {
        "url": "https://example.org/a", "status": "error", "status_code": None,
        "final_url": None, "issue_type": "error", "error_message": None,
        "response_time": 0.1, "content_type": None, "page_title": None,
        "requires_js": False, "ssl_valid": False, "validation_time": "now",
        "retry_count": 1}
    base.update(kwargs)
    return lv.ValidationResult(**base)


def make_validator(dns_trustworthy: bool | None = True):
    v = lv.LinkValidator.__new__(lv.LinkValidator)
    v._dns_trustworthy = dns_trustworthy
    return v


class TestDnsFailureKind:
    @pytest.mark.parametrize("message", [
        "Cannot connect to host x.example:443 ssl:default [Name or service not known]",
        "[nodename nor servname provided, or not known]",
        "No address associated with hostname",
    ])
    def test_name_not_found_is_definitive(self, message):
        assert dns_failure_kind(message) == "not_found"

    @pytest.mark.parametrize("message", [
        "Temporary failure in name resolution",
        "Try again",
    ])
    def test_resolver_wobble_is_advisory(self, message):
        """EAI_AGAIN says nothing about the name. It must never be a verdict."""
        assert dns_failure_kind(message) == "temporary"

    @pytest.mark.parametrize("message", [
        "Connection reset by peer", "Server disconnected", "", None,
    ])
    def test_non_dns_errors_are_not_classified(self, message):
        assert dns_failure_kind(message) is None

    def test_temporary_wins_when_both_markers_appear(self):
        """A mixed wording may only ever degrade to advisory, never escalate."""
        assert dns_failure_kind(
            "Temporary failure in name resolution: name or service not known"
        ) == "temporary"


class TestHostPolicyDns:
    def test_dead_domain_becomes_broken(self):
        out = make_validator(True)._apply_host_policy(
            make_result(error_message=NXDOMAIN_ERROR))
        assert out.status == "broken"
        assert out.issue_type == "dns_not_found"

    def test_untrusted_resolver_keeps_it_advisory(self):
        """The negative control for the test above.

        If the resolver failed its controls, the SAME input must not be
        called broken -- otherwise a wobbling CI resolver would file work
        items to replace live citations.
        """
        out = make_validator(False)._apply_host_policy(
            make_result(error_message=NXDOMAIN_ERROR))
        assert out.status == "error"
        assert out.issue_type != "dns_not_found"

    def test_unprobed_resolver_keeps_it_advisory(self):
        out = make_validator(None)._apply_host_policy(
            make_result(error_message=NXDOMAIN_ERROR))
        assert out.status == "error"

    def test_temporary_failure_never_becomes_broken(self):
        out = make_validator(True)._apply_host_policy(
            make_result(error_message="Temporary failure in name resolution"))
        assert out.status == "error"

    def test_the_real_fhi_error_string_is_recognised(self):
        """Verbatim from citation-validation run 35618883307, issue #637.

        That report counted this as advisory and headlined "Broken: 1".
        """
        assert dns_failure_kind(
            "Cannot connect to host www.fhi.ox.ac.uk:443 ssl:default "
            "[Name or service not known]") == "not_found"


class TestHostPolicyGatekeepers:
    def test_gatekeeper_404_is_downgraded(self):
        out = make_validator(True)._apply_host_policy(make_result(
            url="https://www.mdpi.com/2075-4698/15/1/6",
            status="broken", status_code=404, issue_type="404"))
        assert out.status == "restricted"
        assert out.issue_type.startswith("gatekeeper_")

    def test_ordinary_host_404_stays_broken(self):
        """Negative control: the downgrade must not apply to everything."""
        out = make_validator(True)._apply_host_policy(make_result(
            url="https://example.org/gone", status="broken",
            status_code=404, issue_type="404"))
        assert out.status == "broken"

    def test_gatekeeper_valid_is_untouched(self):
        out = make_validator(True)._apply_host_policy(make_result(
            url="https://www.mdpi.com/x", status="valid", status_code=200,
            issue_type=None))
        assert out.status == "valid"

    def test_dead_domain_wins_over_gatekeeper_downgrade(self):
        """Ordering guard: a dead host must not be rescued by the list."""
        result = make_result(url="https://www.mdpi.com/x", status="broken",
                             status_code=None, issue_type="error",
                             error_message=NXDOMAIN_ERROR)
        out = make_validator(True)._apply_host_policy(result)
        assert out.status == "broken"
        assert out.issue_type == "dns_not_found"


class TestGatekeeperListHygiene:
    def test_pruned_dead_hosts_are_gone(self):
        """Both were NXDOMAIN; on the list they suppressed real breakage."""
        assert "www.fhi.ox.ac.uk" not in GATEKEEPER_HOSTS
        assert "uptimekuma.com" not in GATEKEEPER_HOSTS

    def test_list_is_not_empty(self):
        """Negative control for the test above: it must not pass by the list
        having been emptied."""
        assert len(GATEKEEPER_HOSTS) > 20
        assert is_gatekeeper("https://www.mdpi.com/x")


class TestFetchable:
    @pytest.mark.parametrize("url", [
        "https://example.org/a", "http://example.org/a", "https://8.8.8.8/",
    ])
    def test_public_http_is_fetchable(self, url):
        assert is_fetchable(url)

    @pytest.mark.parametrize("url", [
        "http://127.0.0.1:8080/",
        "http://169.254.169.254/latest/meta-data/",
        "http://10.0.0.5/",
        "http://192.168.1.1/",
        "http://172.16.0.1/",
        "http://[::1]/",
        "http://0.0.0.0/",
        "file:///etc/passwd",
        "gopher://example.org/",
        "ftp://example.org/x",
    ])
    def test_refused(self, url):
        assert not is_fetchable(url)

    def test_validator_short_circuits_unfetchable(self):
        import asyncio
        v = lv.LinkValidator(max_retries=1, timeout=1)
        out = asyncio.run(v.validate_link("http://169.254.169.254/latest/"))
        assert out.status == "unfetchable"
        assert v.stats["unfetchable"] == 1


class TestResolverProbe:
    def test_probe_requires_both_halves(self, monkeypatch):
        """Positive controls resolving is not enough: if a bogus .invalid
        name also 'resolves', the resolver synthesises answers and a dead
        domain is unobservable."""
        import asyncio
        v = make_validator(None)

        async def run(resolvable):
            loop = asyncio.get_running_loop()
            orig = loop.getaddrinfo

            async def fake(host, *a, **k):
                if host in resolvable:
                    return [(2, 1, 6, "", ("1.2.3.4", 0))]
                raise OSError("Name or service not known")

            monkeypatch.setattr(loop, "getaddrinfo", fake, raising=False)
            try:
                return await lv.LinkValidator._probe_resolver(v)
            finally:
                monkeypatch.setattr(loop, "getaddrinfo", orig, raising=False)

        healthy = set(lv.LinkValidator.DNS_CONTROL_RESOLVES)
        assert asyncio.run(run(healthy)) is True
        # Resolver down.
        assert asyncio.run(run(set())) is False
        # Resolver hijacks NXDOMAIN.
        assert asyncio.run(
            run(healthy | {lv.LinkValidator.DNS_CONTROL_NXDOMAIN})) is False


def test_replace_is_available():
    """_apply_host_policy relies on dataclasses.replace preserving fields."""
    r = make_result(url="https://x.example/a", page_title="T")
    assert replace(r, status="broken").page_title == "T"
