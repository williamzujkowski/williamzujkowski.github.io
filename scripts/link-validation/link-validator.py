#!/usr/bin/env -S uv run python3
"""
SCRIPT: link-validator.py
PURPOSE: Link Validator using Playwright
CATEGORY: link_validation
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Link Validator using Playwright. This script is part of the link validation
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/link-validator.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/link-validator.py

    # With verbose output
    python scripts/link-validator.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/logging_config.py for shared logging

RELATED_SCRIPTS:
    - scripts/lib/logging_config.py: Shared logging
    - [Other related scripts in link_validation category]

MANIFEST_REGISTRY: scripts/link-validator.py
"""

import argparse
import asyncio
import json
import logging
import re
import ssl
import sys
import time
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.link_gatekeepers import is_unroutable
from lib.logging_config import setup_logger

try:
    from playwright.async_api import TimeoutError as PlaywrightTimeout
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    # Will log this later when logger is available

import aiohttp
import certifi


@dataclass
class ValidationResult:
    """Result of link validation"""
    url: str
    status: str  # valid, broken, restricted, redirect, timeout, error
    status_code: int | None
    final_url: str | None
    issue_type: str | None  # 404, 403, http_401, timeout, wrong_content, paywall, redirect, ssl_error
    error_message: str | None
    response_time: float
    content_type: str | None
    page_title: str | None
    requires_js: bool
    ssl_valid: bool
    validation_time: str
    retry_count: int

    def to_dict(self):
        return asdict(self)

class LinkValidator:
    """Validate links using multiple strategies"""

    # Common paywall indicators
    PAYWALL_INDICATORS = [
        'subscribe to read',
        'subscription required',
        'paywall',
        'premium content',
        'members only',
        'sign up to continue',
        'create free account to read',
        'limit reached',
        'article limit'
    ]

    # User agents for different validation strategies
    USER_AGENTS = {
        'bot': 'Mozilla/5.0 (compatible; LinkValidator/1.0; +https://williamzujkowski.github.io)',
        'browser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    }

    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout * 1000  # Convert to milliseconds for Playwright
        self.session = None
        self.browser = None
        self.context = None
        self.cache = {}
        self.stats = {
            'total': 0,
            'valid': 0,
            'broken': 0,
            'restricted': 0,
            'redirects': 0,
            'timeouts': 0,
            'errors': 0,
            'cached': 0
        }

    async def initialize(self):
        """Initialize HTTP session and Playwright browser"""
        # Create aiohttp session
        connector = aiohttp.TCPConnector(
            ssl=ssl.create_default_context(cafile=certifi.where()),
            limit=10
        )
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers={'User-Agent': self.USER_AGENTS['browser']}
        )

        # Initialize Playwright if available
        if PLAYWRIGHT_AVAILABLE:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                # --no-sandbox removed: this navigates to URLs that FAILED plain
                # HTTP validation, i.e. the suspicious ones, and GitHub-hosted
                # runners support the renderer sandbox fine.
                args=['--disable-dev-shm-usage']
            )
            self.context = await self.browser.new_context(
                user_agent=self.USER_AGENTS['browser'],
                viewport={'width': 1920, 'height': 1080}
            )

    async def cleanup(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()
        if self.browser:
            await self.browser.close()

    # Anti-bot / rate-limit HTTP codes: the resource still exists for a human
    # reader, but CI can't verify it. IEEE Xplore answers automated checkers
    # with 202 ("Accepted") or 418 ("I'm a teapot"); LinkedIn returns 999;
    # generic rate limiting is 429. These must not inflate the broken count.
    # Codes that mean "the server answered, but not with the document" -- bot
    # challenges, rate limits, WAF rejections, method quibbles. Never 'broken'.
    # 400 is here because some CDNs (ai.meta.com) reject non-browser clients with
    # a Bad Request rather than a 403; the page loads fine in a browser.
    ANTIBOT_CODES = frozenset({202, 400, 405, 406, 415, 418, 429, 451, 999})

    @staticmethod
    def classify_http_status(status_code: int, has_paywall: bool = False,
                             is_redirect: bool = False):
        """Map a final HTTP status to (status, issue_type). Pure -- no network.

        Only a genuinely-dead resource is 'broken': 404 and 410 (plus ssl_error /
        dns_error / timeout, which callers handle separately). Everything else --
        403/401/paywall, anti-bot codes, and 5xx -- is 'restricted'
        (unverifiable, advisory) so the weekly citation report only alarms on
        real breakage rather than on publisher bot challenges. See #366 / #391.
        """
        if status_code == 200:
            if has_paywall:
                return 'restricted', 'paywall'
            if is_redirect:
                return 'redirect', 'redirect'
            return 'valid', None
        if status_code == 404:
            return 'broken', '404'
        if status_code == 403:
            return 'restricted', '403'
        if status_code == 401:
            return 'restricted', 'http_401'
        # Checked before the >=500 branch because 999 would otherwise be swept up.
        if status_code in LinkValidator.ANTIBOT_CODES:
            return 'restricted', f'http_{status_code}'
        if status_code == 410:
            return 'broken', 'gone'
        # 5xx means the origin is up and erroring -- a deploy, an overloaded box,
        # a transient outage. That is not a dead citation, and treating it as one
        # puts live sources into the broken count and the auto-repair queue.
        if status_code >= 500:
            return 'restricted', f'http_{status_code}'
        return 'restricted', f'http_{status_code}'

    async def validate_batch(self, links: list[dict]) -> list[ValidationResult]:
        """Validate a batch of links, one domain at a time but many domains at once.

        This method was `async` and awaited everything strictly one link after
        another -- a nested for-loop over domain groups with an `await` inside,
        and no gather anywhere. 550 citation links were checked serially, which
        is why citation-validation.yml outgrew its 30-minute cap: the shape of
        the work is 550 independent network round trips, and it was being done
        as one queue.

        Grouping by domain already existed and is the part worth keeping:
        requests to the SAME host stay sequential and keep the 0.5s spacing, so
        this is not more aggressive toward any individual site than before.
        What changes is that different hosts no longer wait for each other.
        MAX_CONCURRENT_DOMAINS caps the total in flight so a 300-domain corpus
        does not open 300 sockets at once.
        """
        # Group by domain to respect rate limits, preserving input order so the
        # output is deterministic regardless of which group finishes first.
        domain_groups: dict[str, list[dict]] = {}
        order: dict[str, int] = {}
        for i, link in enumerate(links):
            domain = self._extract_domain(link['url'])
            domain_groups.setdefault(domain, []).append(link)
            order.setdefault(link['url'], i)

        sem = asyncio.Semaphore(self.MAX_CONCURRENT_DOMAINS)

        async def run_group(domain_links: list[dict]) -> list[ValidationResult]:
            out = []
            async with sem:
                for n, link_data in enumerate(domain_links):
                    out.append(await self.validate_link(link_data['url']))
                    # Rate limiting between requests to the same domain. Only
                    # BETWEEN them -- the old code also slept after the last
                    # one, buying nothing.
                    if n < len(domain_links) - 1:
                        await asyncio.sleep(0.5)
            return out

        grouped = await asyncio.gather(
            *(run_group(g) for g in domain_groups.values()))
        results = [r for group in grouped for r in group]
        results.sort(key=lambda r: order.get(r.url, 0))
        return results

    async def validate_link(self, url: str) -> ValidationResult:
        """Validate a single link"""
        self.stats['total'] += 1

        # Check cache
        if url in self.cache:
            self.stats['cached'] += 1
            return self.cache[url]

        # Root-relative links (`/posts/...`, `/about/`) are not external URLs
        # and aiohttp cannot express one -- it raises InvalidURL, which lands
        # as a generic error and then, since #518 made escalation live, pays
        # for a full Chromium launch as well. They were 28 of the 73 non-valid
        # citation links: 38% of the most expensive set in the run, spent
        # asking the network about a path on our own disk.
        #
        # internal-link-check.py in a11y.yml resolves these against dist/ and
        # blocks on them (issue #502), so this is not a gap -- it is the same
        # check moved to the layer that can actually perform it.
        if not urlparse(url).scheme:
            result = ValidationResult(
                url=url, status='internal', status_code=None, final_url=None,
                issue_type='internal_link',
                error_message='Root-relative link; checked by internal-link-check.py',
                response_time=0.0, content_type=None, page_title=None,
                requires_js=False, ssl_valid=False,
                validation_time=datetime.now().isoformat(), retry_count=0)
            self.stats['internal'] = self.stats.get('internal', 0) + 1
            self.cache[url] = result
            return result

        # Placeholder hosts from code examples cannot resolve by design, so
        # a DNS failure is the correct answer rather than a defect to repair.
        # Answered before any network or browser cost -- see is_unroutable().
        if is_unroutable(url):
            result = ValidationResult(
                url=url, status='unroutable', status_code=None, final_url=None,
                issue_type='placeholder_host',
                error_message=('Reserved/placeholder host (RFC 2606/6761/8375 '
                               'or a single-label container name)'),
                response_time=0.0, content_type=None, page_title=None,
                requires_js=False, ssl_valid=False,
                validation_time=datetime.now().isoformat(), retry_count=0)
            self.stats['unroutable'] = self.stats.get('unroutable', 0) + 1
            self.cache[url] = result
            return result

        start_time = time.time()
        result = None
        counted_valid = False

        # Try different validation strategies
        for retry in range(self.max_retries):
            try:
                # First try with simple HTTP request
                result = await self._validate_http(url, retry)

                if result.status == 'valid':
                    self.stats['valid'] += 1
                    counted_valid = True
                    break

                # Exponential backoff for retries
                if retry < self.max_retries - 1:
                    await asyncio.sleep(2 ** retry)

            except Exception as e:
                result = ValidationResult(
                    url=url,
                    status='error',
                    status_code=None,
                    final_url=None,
                    issue_type='error',
                    error_message=str(e),
                    response_time=time.time() - start_time,
                    content_type=None,
                    page_title=None,
                    requires_js=False,
                    ssl_valid=False,
                    validation_time=datetime.now().isoformat(),
                    retry_count=retry + 1
                )

        # Browser escalation, after the HTTP retries are exhausted rather than
        # inside them.
        #
        # It used to sit in the retry loop, so a failing link paid for a full
        # Chromium page load on EVERY retry -- three browser launches, up to
        # 30s each, on top of three HTTP attempts. Nothing noticed, because the
        # escalation had never actually executed: playwright was installed into
        # a different interpreter than the one running the script, so
        # PLAYWRIGHT_AVAILABLE was always False (issue #496). Fixing that in
        # #518 turned the cost on for the first time, and citation-validation.yml
        # started hitting its 30-minute cap -- which GitHub reports as
        # "cancelled", not "failure", so a weekly gate stopped producing any
        # output at all and still read as benign in the run list.
        #
        # Why not a flat single attempt: measured on 12 known-failing citation
        # links, dropping straight from three escalations to one lost a link
        # (pubmed.ncbi.nlm.nih.gov, rescued by the old code on its second
        # attempt). _validate_playwright ignores the retry index entirely, so
        # that rescue was not new information -- it was a second roll against a
        # rate limiter. A second roll is still worth having, and is worth it
        # ONLY for the codes where a limiter is the plausible explanation:
        # a 404 answers the same way however many times it is asked.
        if result and result.status != 'valid' and PLAYWRIGHT_AVAILABLE:
            result = await self._escalate(url, result)

        if result:
            # Update stats. `valid` is counted here rather than only inside the
            # retry loop: a link rescued by the browser escalation above never
            # breaks out of that loop, so counting it there undercounted every
            # rescue -- the sample run reported stats.valid=1 against 2 actually
            # valid results, and citation-validation.yml publishes stats.valid
            # straight into the issue body.
            if result.status == 'valid' and not counted_valid:
                self.stats['valid'] += 1
            elif result.status == 'broken':
                self.stats['broken'] += 1
            elif result.status == 'restricted':
                self.stats['restricted'] += 1
            elif result.status == 'redirect':
                self.stats['redirects'] += 1
            elif result.status == 'timeout':
                self.stats['timeouts'] += 1
            elif result.status == 'error':
                self.stats['errors'] += 1

            # Cache result
            self.cache[url] = result

        return result

    async def _validate_http(self, url: str, retry: int) -> ValidationResult:
        """Validate using HTTP request"""
        start_time = time.time()

        try:
            timeout = aiohttp.ClientTimeout(total=30)
            async with self.session.get(
                url,
                timeout=timeout,
                allow_redirects=True,
                ssl=True
            ) as response:
                response_time = time.time() - start_time

                # Check for redirects
                final_url = str(response.url)
                is_redirect = final_url != url

                # Read content for paywall detection
                content = await response.text()
                content_lower = content.lower()

                # Check for paywall
                has_paywall = any(
                    indicator in content_lower
                    for indicator in self.PAYWALL_INDICATORS
                )

                # Extract page title
                title_match = re.search(r'<title>([^<]+)</title>', content, re.IGNORECASE)
                page_title = title_match.group(1) if title_match else None

                # Map the final HTTP status to a classification (see
                # classify_http_status for the broken-vs-restricted taxonomy).
                status, issue_type = self.classify_http_status(
                    response.status, has_paywall=has_paywall, is_redirect=is_redirect
                )

                return ValidationResult(
                    url=url,
                    status=status,
                    status_code=response.status,
                    final_url=final_url if is_redirect else None,
                    issue_type=issue_type,
                    error_message=None,
                    response_time=response_time,
                    content_type=response.headers.get('Content-Type'),
                    page_title=page_title,
                    requires_js=False,
                    ssl_valid=True,
                    validation_time=datetime.now().isoformat(),
                    retry_count=retry + 1
                )

        except TimeoutError:
            return ValidationResult(
                url=url,
                status='timeout',
                status_code=None,
                final_url=None,
                issue_type='timeout',
                error_message='Request timeout',
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except aiohttp.ClientSSLError as e:
            return ValidationResult(
                url=url,
                status='broken',
                status_code=None,
                final_url=None,
                issue_type='ssl_error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except Exception as e:
            return ValidationResult(
                url=url,
                status='error',
                status_code=None,
                final_url=None,
                issue_type='error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=False,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )

    # A browser gets a second roll only against these: they are the codes a
    # rate limiter or bot-challenge returns, where the same request a moment
    # later can legitimately succeed. 404 and 410 are excluded on purpose.
    # How many DOMAINS may be checked at once. Requests within one domain stay
    # sequential and keep their 0.5s spacing, so this never increases the rate
    # seen by any single host -- it only stops unrelated hosts from queueing
    # behind each other. Kept modest because a browser escalation can open a
    # page under any of these.
    MAX_CONCURRENT_DOMAINS = 8

    ESCALATION_RETRY_CODES = {401, 403, 408, 429, 503}

    @staticmethod
    def _worth_escalating(result: ValidationResult) -> bool:
        """True if a real browser could plausibly return a different answer.

        A browser helps with exactly two things: pages that need JS to render,
        and WAFs that refuse a bare HTTP client but serve Chromium. It cannot
        help with a name that has no DNS record -- Chromium resolves through
        the same system resolver, so launching it for `https://suricata-ids.org/`
        (NXDOMAIN on 1.1.1.1, 8.8.8.8 and 9.9.9.9 alike) spends ~30 seconds
        re-learning what getaddrinfo already said.
        """
        return result.issue_type not in {'dns_error', 'ssl_error'}

    async def _escalate(self, url: str, result: ValidationResult) -> ValidationResult:
        """Re-check a non-valid result in a real browser. Returns the better of the two."""
        if not self._worth_escalating(result):
            return result

        attempt = await self._validate_playwright(url, 0)
        if attempt and attempt.status == 'valid':
            return attempt

        # One more roll, but only where a rate limiter is the plausible cause.
        if result.status_code in self.ESCALATION_RETRY_CODES:
            await asyncio.sleep(2)
            attempt = await self._validate_playwright(url, 1)
            if attempt and attempt.status == 'valid':
                return attempt

        return result

    async def _validate_playwright(self, url: str, retry: int) -> ValidationResult:
        """Validate using Playwright for JavaScript-rendered content"""
        if not self.context:
            return None

        start_time = time.time()
        page = await self.context.new_page()

        try:
            # Navigate to the page
            # `load`, not `networkidle`.
            #
            # This one word was 91% of the runtime. Measured over the full
            # 550-link citation set: the sum of every link's own HTTP
            # response_time was 165s out of 1894s wall clock. The missing 1729s
            # was the browser waiting for `networkidle` -- which means "no
            # network request for 500ms", a condition that analytics beacons,
            # ad frames and polling widgets never satisfy, so the wait runs to
            # the full 30s timeout and then reports success anyway.
            #
            # Nothing downstream needs a settled network. This method asks
            # three questions -- did the server answer, does the body contain a
            # paywall marker, what is the title -- and all three are answerable
            # once the page's own resources are in.
            #
            # `domcontentloaded` was measured too and is not worth it: 42.2s vs
            # 43.7s on the sample -- inside the noise -- but it consistently
            # downgraded pubmed.ncbi.nlm.nih.gov from `valid` to `restricted`
            # (4 runs out of 4), because it snapshots the anti-bot challenge
            # page before the challenge resolves. `load` recovers that verdict
            # some of the time and never costs more.
            response = await page.goto(
                url,
                wait_until='load',
                timeout=self.timeout
            )

            response_time = time.time() - start_time

            # Get final URL after redirects
            final_url = page.url
            is_redirect = final_url != url

            # Get page content
            content = await page.content()
            content_lower = content.lower()

            # Check for paywall
            has_paywall = any(
                indicator in content_lower
                for indicator in self.PAYWALL_INDICATORS
            )

            # Get page title
            page_title = await page.title()

            # Determine status
            if response.status == 200:
                if has_paywall:
                    status = 'broken'
                    issue_type = 'paywall'
                elif is_redirect:
                    status = 'redirect'
                    issue_type = 'redirect'
                else:
                    status = 'valid'
                    issue_type = None
            else:
                status = 'broken'
                issue_type = f'http_{response.status}'

            result = ValidationResult(
                url=url,
                status=status,
                status_code=response.status,
                final_url=final_url if is_redirect else None,
                issue_type=issue_type,
                error_message=None,
                response_time=response_time,
                content_type=response.headers.get('content-type'),
                page_title=page_title,
                requires_js=True,
                ssl_valid=True,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )

        except PlaywrightTimeout:
            result = ValidationResult(
                url=url,
                status='timeout',
                status_code=None,
                final_url=None,
                issue_type='timeout',
                error_message='Page load timeout',
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=True,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        except Exception as e:
            result = ValidationResult(
                url=url,
                status='error',
                status_code=None,
                final_url=None,
                issue_type='error',
                error_message=str(e),
                response_time=time.time() - start_time,
                content_type=None,
                page_title=None,
                requires_js=True,
                ssl_valid=False,
                validation_time=datetime.now().isoformat(),
                retry_count=retry + 1
            )
        finally:
            await page.close()

        return result

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            return parsed.netloc
        except ValueError:
            return 'unknown'

    async def save_results(self, results: list[ValidationResult], output_file: Path, logger=None):
        """Save validation results to JSON"""
        data = {
            'validation_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': [r.to_dict() for r in results]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        if logger:
            logger.info(f"✅ Validated {self.stats['total']} links")
            logger.info(f"✔️  Valid: {self.stats['valid']}")
            logger.info(f"❌ Broken: {self.stats['broken']}")
            logger.info(f"🔒 Restricted (unverifiable): {self.stats['restricted']}")
            logger.info(f"↪️  Redirects: {self.stats['redirects']}")
            logger.info(f"⏱️  Timeouts: {self.stats['timeouts']}")
            logger.info(f"💾 Results saved to {output_file}")

async def main():
    parser = argparse.ArgumentParser(description='Validate links from extracted data')
    parser.add_argument('--input', type=Path,
                       default=Path('links.json'),
                       help='Input JSON file with extracted links')
    parser.add_argument('--output', type=Path,
                       default=Path('validation.json'),
                       help='Output JSON file')
    parser.add_argument('--max-retries', type=int, default=3,
                       help='Maximum retry attempts')
    parser.add_argument('--timeout', type=int, default=30,
                       help='Request timeout in seconds')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    # Log Playwright availability
    if not PLAYWRIGHT_AVAILABLE:
        logger.warning("⚠️  Playwright not installed. Using basic HTTP validation.")

    if not args.input.exists():
        logger.error(f"❌ Input file not found: {args.input}")
        return 1

    # Load links
    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)

    links = data['links']
    logger.info(f"📋 Loaded {len(links)} links to validate")

    # Initialize validator
    validator = LinkValidator(
        max_retries=args.max_retries,
        timeout=args.timeout
    )

    await validator.initialize()

    try:
        # Validate links
        results = await validator.validate_batch(links)

        # Save results
        await validator.save_results(results, args.output, logger)
    finally:
        await validator.cleanup()

    return 0

if __name__ == '__main__':
    asyncio.run(main())
