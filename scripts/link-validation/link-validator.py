#!/usr/bin/env -S uv run python3
"""
SCRIPT: link-validator.py
PURPOSE: Link Validator using Playwright
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

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
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in link_validation category]

MANIFEST_REGISTRY: scripts/link-validator.py
"""

import json
import asyncio
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
import ssl
import time
from urllib.parse import urlparse, urljoin

try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Using basic HTTP validation.")

import aiohttp
import certifi

@dataclass
class ValidationResult:
    """Result of link validation"""
    url: str
    status: str  # valid, broken, redirect, timeout, error
    status_code: Optional[int]
    final_url: Optional[str]
    issue_type: Optional[str]  # 404, 403, timeout, wrong_content, paywall, redirect, ssl_error
    error_message: Optional[str]
    response_time: float
    content_type: Optional[str]
    page_title: Optional[str]
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
        'browser': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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
            headers={'User-Agent': self.USER_AGENTS['bot']}
        )

        # Initialize Playwright if available
        if PLAYWRIGHT_AVAILABLE:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=True,
                args=['--disable-dev-shm-usage', '--no-sandbox']
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

    async def validate_batch(self, links: List[Dict]) -> List[ValidationResult]:
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
        for domain, domain_links in domain_groups.items():
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

                # Determine status and issue type
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
                elif response.status == 404:
                    status = 'broken'
                    issue_type = '404'
                elif response.status == 403:
                    status = 'broken'
                    issue_type = '403'
                elif response.status >= 500:
                    status = 'broken'
                    issue_type = f'{response.status}_error'
                else:
                    status = 'broken'
                    issue_type = f'http_{response.status}'

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

        except asyncio.TimeoutError:
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
        except:
            return 'unknown'

    async def save_results(self, results: List[ValidationResult], output_file: Path):
        """Save validation results to JSON"""
        data = {
            'validation_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': [r.to_dict() for r in results]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Validated {self.stats['total']} links")
        print(f"✔️  Valid: {self.stats['valid']}")
        print(f"❌ Broken: {self.stats['broken']}")
        print(f"↪️  Redirects: {self.stats['redirects']}")
        print(f"⏱️  Timeouts: {self.stats['timeouts']}")
        print(f"💾 Results saved to {output_file}")

import re  # Add import at top of file

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

    args = parser.parse_args()

    if not args.input.exists():
        print(f"❌ Input file not found: {args.input}")
        return 1

    # Load links
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    links = data['links']
    print(f"📋 Loaded {len(links)} links to validate")

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
        await validator.save_results(results, args.output)
    finally:
        await validator.cleanup()

    return 0

if __name__ == '__main__':
    asyncio.run(main())