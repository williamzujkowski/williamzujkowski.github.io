"""Hosts that reject or throttle automated link checkers.

Ported from `.lycheeignore`, which was left behind when the lychee step was
removed from compliance-monitor.yml. The file itself was dead, but the list in
it was not: it is a couple of years of accumulated observation about which
publishers block, rate-limit or stall a checker, and deleting it would have
thrown that away (issue #503).

Why it matters HERE: `citation-validation.yml` opens a GitHub issue telling
the author to "find replacement sources" for anything it calls broken. A
publisher that answers a bot with 404 instead of 403 therefore produces a
work item to replace a citation that is perfectly fine. Soft codes (403, 429,
451, ...) are already handled by classify_status; this list covers the hosts
that lie about the status code instead.

The effect is deliberately narrow: a `broken` verdict on one of these hosts is
downgraded to `needs_manual`, so it still surfaces for a human but never
drives the alarm or the repair queue. Nothing is skipped or hidden.
"""

from __future__ import annotations

from urllib.parse import urlparse

# Publishers and platforms that actively block automated checkers.
BOT_BLOCKING = [
    "academic.oup.com",
    "cisa.gov",
    "coral.ai",
    "defense.gov",
    "dl.acm.org",
    "dodcio.defense.gov",
    "doi.org",
    "gym.openai.com",
    "jade.tilab.com",
    "jstor.org",
    "media.defense.gov",
    "openai.com",
    "orbilu.uni.lu",
    "partnershiponai.org",
    "platform.openai.com",
    "reddit.com",
    "researchgate.net",
    "sciencedirect.com",
    "search.ebscohost.com",
    "weforum.org",
    "www.cfr.org",
    "www.cisa.gov",
    "www.cloudflare.com",
    "www.enisa.europa.eu",
    "www.epa.gov",
    "www.fhi.ox.ac.uk",
    "www.gartner.com",
    "www.hhs.gov",
    "www.idc.com",
    "www.iea.org",
    "www.jstor.org",
    "www.linkedin.com",
    "www.mdpi.com",
    "www.nsa.gov",
    "www.redhat.com",
    "www.udacity.com",
]

# Sites that answer 429 or otherwise throttle a sweep.
RATE_LIMITING = [
    "backblaze.com",
    "nomadproject.io",
    "terraform.io",
    "vaultproject.io",
    "venturebeat.com",
    "www.backblaze.com",
    "www.nomadproject.io",
    "www.terraform.io",
    "www.vaultproject.io",
]

# Slow or intermittently unreachable.
SLOW_OR_FLAKY = [
    "azure.microsoft.com",
    "uptimekuma.com",
]

GATEKEEPER_HOSTS = frozenset(BOT_BLOCKING + RATE_LIMITING + SLOW_OR_FLAKY)


def is_gatekeeper(url: str) -> bool:
    """True if the URL's host is known to mistreat automated checkers.

    Matches the host and any subdomain of it, so "reddit.com" covers
    "old.reddit.com". Never matches a substring of a different domain --
    "notreddit.com" is not a match.
    """
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    if not host:
        return False
    return any(host == h or host.endswith("." + h) for h in GATEKEEPER_HOSTS)


# ---------------------------------------------------------------------------
# Hosts that are unroutable BY CONSTRUCTION, not by accident.
#
# 16 of the 30 "broken links" the daily monitor reported on 2026-09-03 were
# illustrative hostnames inside code examples: container service names
# (`wazuh-manager:55000`, `http://elasticsearch:9200`) and RFC-reserved
# example domains (`vault.example.com`, `test-vault.local`). None of them can
# ever resolve -- that is the entire point of the RFCs that reserve them --
# so reporting them as breakage is not a signal that decayed, it is a signal
# that was never true.
#
# It is not harmless noise. It is more than half the alarm, and it is the
# half that never changes, so a reader learns to skim the list and misses the
# ten citations that genuinely rotted.
#
# Distinct from GATEKEEPER_HOSTS above: those are real sites that mistreat
# bots (downgraded to `needs_manual` for a human to eyeball). These are not
# sites at all, so there is nothing for a human to check.

# TLDs reserved so they never resolve on the public internet.
#   RFC 2606 — .test, .example, .invalid, .localhost
#   RFC 6762 — .local  (mDNS, link-local only)
#   RFC 8375 — .home.arpa  (residential home networks)
#   RFC 6761 — .localhost
# `.internal` is not an RFC reservation but ICANN permanently withheld it
# from delegation in 2024 for exactly this purpose.
UNROUTABLE_SUFFIXES = (
    ".test",
    ".example",
    ".invalid",
    ".localhost",
    ".local",
    ".home.arpa",
    ".internal",
)

# RFC 2606 §3 reserves these second-level names for documentation.
UNROUTABLE_DOMAINS = (
    "example.com",
    "example.net",
    "example.org",
)


def is_unroutable(url: str) -> bool:
    """True if the URL's host can never resolve on the public internet.

    Three cases, all of which mean "this is a placeholder in a code example":

    1. A reserved TLD (`vault.example.com` is caught by case 3;
       `test-vault.local` and `foo.invalid` by this one).
    2. A bare hostname with no dot at all -- `elasticsearch`,
       `wazuh-manager`, `gvisor-nginx`. The public DNS root has no
       single-label names, so these are always container/compose service
       names. `localhost` is included here.
    3. An RFC 2606 documentation domain, or any subdomain of one.

    An IP literal is NOT unroutable: 127.0.0.1 and 10.0.0.1 are perfectly
    real addresses that simply are not reachable from CI, which is a
    different claim and belongs to whoever is doing the reaching.
    """
    try:
        host = (urlparse(url).hostname or "").lower()
    except ValueError:
        return False
    if not host:
        return False

    # Case 2: single-label hostname. Bracketed IPv6 and dotted IPv4 both
    # contain a separator, so neither reaches this branch.
    if "." not in host and ":" not in host:
        return True

    if host.endswith(UNROUTABLE_SUFFIXES):
        return True

    return any(host == d or host.endswith("." + d) for d in UNROUTABLE_DOMAINS)
