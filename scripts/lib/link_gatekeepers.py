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

import ipaddress
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
#
# Entries here suppress an alarm, so a dead host on this list is worse than
# no list at all: it converts "this citation is gone" into "this publisher is
# slow, ignore it". Two were removed on 2026-09-24 after every host on the
# list was resolved against a control set (github.com / example.com resolving,
# two bogus names returning NXDOMAIN, so the resolver was proven to
# discriminate before any result was believed):
#
#   www.fhi.ox.ac.uk  -- NXDOMAIN. The Future of Humanity Institute closed in
#                        April 2024 and the domain is gone. It was suppressing
#                        a genuinely dead citation in
#                        2025-08-09-ai-cognitive-infrastructure.md.
#   uptimekuma.com    -- NXDOMAIN, and cited by no post. The project lives at
#                        github.com/louislam/uptime-kuma.
SLOW_OR_FLAKY = [
    "azure.microsoft.com",
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


# ---------------------------------------------------------------------------
# A name that does not exist is a VERDICT, not a retry hint.
#
# citation-validation.yml's report files DNS failures under "Unresolved /
# errors / timeouts", whose own header reads: "These findings are advisory,
# not confirmed broken links." That is right for a timeout and wrong for a
# name that does not resolve.
#
# It cost a real citation. On 2026-09-21 the weekly report said "Broken: 1"
# while https://www.fhi.ox.ac.uk/reports/agi-timeline-surveys/ -- a domain
# that ceased to exist when the Future of Humanity Institute closed in April
# 2024 -- sat in the advisory bucket, cited for a specific quantitative claim.
# The checker saw it, described it correctly, and filed it under "retry this".
#
# getaddrinfo distinguishes the two cases and the distinction is the whole
# point:
#
#   EAI_NONAME  "Name or service not known", "nodename nor servname provided"
#               The name does not exist. Definitive. No retry will change it.
#   EAI_AGAIN   "Temporary failure in name resolution"
#               The RESOLVER could not answer. Says nothing about the name.
#               Stays advisory.
#
# Treating EAI_AGAIN as breakage would be the failure this module exists to
# prevent, one layer down: a wobbling CI resolver would mass-produce work
# items to replace citations that are perfectly fine.

# EAI_NONAME, across the wordings glibc, musl and macOS use.
DNS_NAME_NOT_FOUND_MARKERS = (
    "name or service not known",
    "nodename nor servname provided",
    "no address associated with hostname",
    "name does not resolve",
)

# EAI_AGAIN and friends: the resolver failed, not the name.
DNS_TEMPORARY_MARKERS = (
    "temporary failure in name resolution",
    "try again",
    "timed out",
)


def dns_failure_kind(error_message: str | None) -> str | None:
    """Classify a connection error as a DNS verdict, a DNS wobble, or neither.

    Returns 'not_found' (the name does not exist -- definitive),
    'temporary' (the resolver could not answer -- advisory), or None (this
    was not a DNS failure at all).

    Temporary is checked FIRST: "Temporary failure in name resolution"
    contains neither not-found marker today, but ordering it first means a
    future wording that contains both can only ever degrade to advisory.
    """
    if not error_message:
        return None
    lowered = error_message.lower()
    if any(marker in lowered for marker in DNS_TEMPORARY_MARKERS):
        return "temporary"
    if any(marker in lowered for marker in DNS_NAME_NOT_FOUND_MARKERS):
        return "not_found"
    return None


# ---------------------------------------------------------------------------
# What the checkers are allowed to fetch.
#
# These tools take URLs out of blog posts -- including, via link-monitor.yml's
# pull_request trigger, posts in a fork PR -- and fetch them. Nothing
# currently constrains the scheme or the destination address.
#
# The realistic blast radius here is small and worth stating so this is not
# mistaken for more than it is: no response body is read on the HTTP path, no
# custom headers can be set, and the report carries counts rather than
# response content. The worst case is a blind, header-less GET whose result
# the requester never sees. That is why this is a guard and not an incident.
#
# It closes two concrete holes:
#
#   1. Scheme. `file://` is rejected today only because aiohttp happens to
#      raise NonHttpUrlClientError -- an implementation detail this repo
#      neither asserts nor tests. The Playwright escalation path has no
#      scheme check at all.
#   2. Address literals. http://127.0.0.1:8080/, http://169.254.169.254/ and
#      http://10.0.0.5/ are all fetched today. is_unroutable() deliberately
#      does NOT cover these (an IP literal is a real address), so they need
#      their own predicate.
#
# NOT closed: a public hostname whose DNS answer is a private address. That
# needs a post-resolution check applied per redirect hop, which is a larger
# change to the fetch path -- tracked separately rather than half-done here.

ALLOWED_SCHEMES = frozenset({"http", "https"})


def is_fetchable(url: str) -> bool:
    """False if a link checker should refuse to request this URL at all.

    Rejects any non-http(s) scheme, and any host that is an IP literal in
    private, loopback, link-local, reserved or unspecified space.
    """
    try:
        parsed = urlparse(url)
    except ValueError:
        return False

    if parsed.scheme.lower() not in ALLOWED_SCHEMES:
        return False

    host = (parsed.hostname or "").strip()
    if not host:
        return False

    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        # Not an IP literal. Hostnames are resolved by the fetcher; see the
        # "NOT closed" note above.
        return True

    return not (
        address.is_private
        or address.is_loopback
        or address.is_link_local
        or address.is_reserved
        or address.is_multicast
        or address.is_unspecified
    )
