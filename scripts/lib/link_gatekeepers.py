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
