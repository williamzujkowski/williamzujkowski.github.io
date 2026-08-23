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
        """Validate a batch of links"""
        results = []

        # Group by domain to respect rate limits
        domain_groups = {}
        for link in links:
            domain = self._extract_domain(link['url'])
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(link)

        # Process each domain group with rate limiting
        for _domain, domain_links in domain_groups.items():
            for link_data in domain_links:
                result = await self.validate_link(link_data['url'])
                results.append(result)

                # Rate limiting between requests to same domain
                if len(domain_links) > 1:
                    await asyncio.sleep(0.5)

        return results

    async def validate_link(self, url: str) -> ValidationResult:
        """Validate a single link"""
        self.stats['total'] += 1

        # Check cache
        if url in self.cache:
            self.stats['cached'] += 1
            return self.cache[url]

        start_time = time.time()
        result = None

        # Try different validation strategies
        for retry in range(self.max_retries):
            try:
                # First try with simple HTTP request
                result = await self._validate_http(url, retry)

                # If failed or suspicious, try with Playwright
                if result.status != 'valid' and PLAYWRIGHT_AVAILABLE:
                    playwright_result = await self._validate_playwright(url, retry)
                    if playwright_result.status == 'valid':
                        result = playwright_result

                if result.status == 'valid':
                    self.stats['valid'] += 1
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

        if result:
            # Update stats
            if result.status == 'broken':
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

    async def _validate_playwright(self, url: str, retry: int) -> ValidationResult:
        """Validate using Playwright for JavaScript-rendered content"""
        if not self.context:
            return None

        start_time = time.time()
        page = await self.context.new_page()

        try:
            # Navigate to the page
            response = await page.goto(
                url,
                wait_until='networkidle',
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
