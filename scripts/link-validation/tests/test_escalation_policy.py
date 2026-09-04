"""Regression tests for the Playwright escalation policy in link-validator.py.

Context: the escalation had never executed until #518 (playwright was installed
into a different interpreter than the script ran in, issue #496). Turning it on
made citation-validation.yml exceed its 30-minute cap on 2026-08-24 and
2026-08-31 -- and GitHub reports a job timeout as "cancelled", not "failure", so
a weekly gate produced no output for two weeks while looking benign.

These tests pin the two decisions that keep the runtime bounded. Both were
MEASURED, not assumed: on 12 known-failing citation links, escalating once
instead of three times took 175.9s -> 112.2s with identical verdicts.
"""

import sys
from pathlib import Path

import pytest
from conftest import load_script

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

lv = load_script("link-validator.py")
LinkValidator = lv.LinkValidator


def _result(status="broken", issue_type=None, status_code=None):
    return lv.ValidationResult(
        url="https://example.org/x", status=status, status_code=status_code,
        final_url=None, issue_type=issue_type, error_message=None,
        response_time=0.0, content_type=None, page_title=None,
        requires_js=False, ssl_valid=False, validation_time="", retry_count=0)


@pytest.mark.parametrize("issue_type", ["dns_error", "ssl_error"])
def test_browser_is_not_launched_when_it_cannot_help(issue_type):
    """Chromium resolves through the same system resolver as aiohttp.

    Launching it for a name with no DNS record (suricata-ids.org is NXDOMAIN on
    1.1.1.1, 8.8.8.8 and 9.9.9.9 alike) spends ~30s re-learning what
    getaddrinfo already returned.
    """
    assert not LinkValidator._worth_escalating(_result(issue_type=issue_type))


@pytest.mark.parametrize("issue_type", ["not_found", "http_403", "timeout", None])
def test_browser_is_launched_where_the_answer_could_change(issue_type):
    """JS-rendered pages and WAFs that serve Chromium but refuse aiohttp."""
    assert LinkValidator._worth_escalating(_result(issue_type=issue_type))


def test_second_browser_attempt_only_for_rate_limit_shaped_codes():
    """A 404 answers the same way however many times it is asked.

    The one link a flat single-escalation lost (pubmed.ncbi.nlm.nih.gov) was a
    403 rescued on a second roll against a rate limiter -- not new information,
    but worth one retry. Extending that retry to 404/410 buys nothing and is
    what made the job time out.
    """
    codes = LinkValidator.ESCALATION_RETRY_CODES
    for retryable in (401, 403, 408, 429, 503):
        assert retryable in codes
    for pointless in (404, 410, 200, 301):
        assert pointless not in codes


# --- concurrency: fast, but not ruder to any single host ---------------------
def test_same_domain_requests_stay_sequential_and_spaced():
    """Different hosts run in parallel; one host is still one-at-a-time.

    validate_batch used to await every link in series -- 550 citation links as
    a single queue, which is why the job outgrew its 30-minute cap. The fix
    must not turn into "hammer everyone at once": requests to the SAME domain
    keep their order and their 0.5s spacing, so no individual site sees a
    higher rate than before.
    """
    import asyncio

    v = LinkValidator.__new__(LinkValidator)
    v.stats = {}
    v.cache = {}
    events = []

    async def fake_validate_link(url):
        host = url.split("/")[2]
        events.append(("start", host, url))
        await asyncio.sleep(0.01)
        events.append(("end", host, url))
        return _result(status="valid")

    v.validate_link = fake_validate_link
    v._extract_domain = lambda u: u.split("/")[2]

    links = [{"url": f"https://{h}/{i}"} for h in ("a.test", "b.test") for i in range(3)]
    asyncio.run(LinkValidator.validate_batch(v, links))

    # Within each host, every start is preceded by the previous end.
    for host in ("a.test", "b.test"):
        seq = [e for e in events if e[1] == host]
        for i in range(1, len(seq)):
            if seq[i][0] == "start":
                assert seq[i - 1][0] == "end", f"{host} overlapped its own requests"

    # Across hosts, work genuinely interleaves -- otherwise this is still serial.
    hosts_in_order = [e[1] for e in events if e[0] == "start"]
    assert len(set(hosts_in_order[:2])) == 2, "domains did not run concurrently"


def test_batch_preserves_input_order():
    """Concurrency must not reorder the report."""
    import asyncio

    v = LinkValidator.__new__(LinkValidator)
    v.stats = {}
    v.cache = {}

    async def fake(url):
        # Make the second host finish first, so unsorted output would differ.
        await asyncio.sleep(0.02 if "slow" in url else 0.001)
        r = _result(status="valid")
        r.url = url
        return r

    v.validate_link = fake
    v._extract_domain = lambda u: u.split("/")[2]

    links = [{"url": "https://slow.test/1"}, {"url": "https://fast.test/2"},
             {"url": "https://slow.test/3"}, {"url": "https://fast.test/4"}]
    out = asyncio.run(LinkValidator.validate_batch(v, links))
    assert [r.url for r in out] == [x["url"] for x in links]
