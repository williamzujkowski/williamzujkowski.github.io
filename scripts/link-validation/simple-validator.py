#!/usr/bin/env -S uv run python3
"""
SCRIPT: simple-validator.py
PURPOSE: Simple Link Validator
CATEGORY: utilities
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Simple Link Validator. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    uv run python scripts/link-validation/simple-validator.py --links links.json --output validation.json

ARGUMENTS:
    --links: JSON file with extracted links (default: links.json)
    --output: Output report file (default: validation.json)
    --quiet/-q: Suppress progress messages

EXAMPLES:
    # Basic usage
    uv run python scripts/link-validation/simple-validator.py --links links.json --output validation.json

    # Quiet mode
    uv run python scripts/link-validation/simple-validator.py --links links.json --quiet

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/logging_config.py for shared logging

RELATED_SCRIPTS:
    - scripts/lib/logging_config.py: Shared logging
    - [Other related scripts in utilities category]

MANIFEST_REGISTRY: scripts/simple-validator.py
"""

import json
import asyncio
import aiohttp
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse
from urllib.parse import urlparse

# Setup logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

class SimpleValidator:
    """Simple link validator using only aiohttp.

    Only a dead resource (404/410) or an unresolvable host counts as 'broken'.
    Servers that gatekeep bots (403/429/451), answer HEAD oddly (202/405/415),
    or hiccup on the connection are recorded as 'needs_manual' -- a human should
    eyeball them, but they must not inflate the broken count or feed the
    auto-repair queue. See issue #240.
    """

    # A realistic browser identity. doi.org, nvlpubs.nist.gov, nature.com,
    # whitehouse.gov etc. WAF-block the default aiohttp User-Agent.
    BROWSER_HEADERS = {
        'User-Agent': (
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        ),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    # Codes that mean "the server is gatekeeping / picky", not "the link is dead".
    SOFT_CODES = {202, 403, 405, 406, 415, 418, 429, 451}
    DEAD_CODES = {404, 410}
    REDIRECT_CODES = {301, 302, 303, 307, 308}
    MIN_DOMAIN_INTERVAL = 0.4  # seconds between requests to the same host

    def __init__(self):
        self.session = None
        self.results = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'broken': 0,
            'redirect': 0,
            'timeout': 0,
            'error': 0,
            'needs_manual': 0,
        }
        self._domain_locks: Dict[str, asyncio.Lock] = {}
        self._domain_last: Dict[str, float] = {}

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=20)
        self.session = aiohttp.ClientSession(timeout=timeout, headers=self.BROWSER_HEADERS)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def _throttle(self, domain: str):
        """Space out requests to the same host so we don't trigger rate limits."""
        lock = self._domain_locks.setdefault(domain, asyncio.Lock())
        async with lock:
            loop = asyncio.get_event_loop()
            wait = self.MIN_DOMAIN_INTERVAL - (loop.time() - self._domain_last.get(domain, 0.0))
            if wait > 0:
                await asyncio.sleep(wait)
            self._domain_last[domain] = loop.time()

    @staticmethod
    def _is_dns_error(exc: Exception) -> bool:
        dns_cls = getattr(aiohttp, 'ClientConnectorDNSError', None)
        if dns_cls and isinstance(exc, dns_cls):
            return True
        msg = str(exc).lower()
        return 'name or service not known' in msg or 'nodename nor servname' in msg

    def _record(self, result: Dict, status: str, issue_type: Optional[str] = None):
        result['status'] = status
        result['issue_type'] = issue_type
        self.stats[status] = self.stats.get(status, 0) + 1
        return result

    async def validate_url(self, url: str) -> Dict:
        """Validate a single URL.

        HEAD first (cheap); on any non-final code, retry with a ranged GET using
        browser headers. Honor Retry-After once on 429. Classify the final code.
        """
        result = {'url': url, 'status': 'unknown', 'status_code': None,
                  'issue_type': None, 'notes': ''}
        domain = urlparse(url).netloc
        self.stats['total'] += 1

        try:
            await self._throttle(domain)
            async with self.session.head(url, allow_redirects=True) as resp:
                code, final_url = resp.status, str(resp.url)

            # HEAD is unreliable for anything that isn't a clean 2xx/redirect:
            # retry with a 1-byte ranged GET (real browsers GET, and many WAFs
            # only 403 HEAD requests).
            if code != 200 and code not in self.REDIRECT_CODES:
                code, final_url = await self._ranged_get(url, domain, code, final_url)

            # One polite retry on rate limiting, honoring Retry-After.
            if code == 429:
                code, final_url = await self._retry_after(url, domain, code, final_url)

            result['status_code'] = code
            if final_url != url:
                result['notes'] = f"Final URL: {final_url}"

            if 200 <= code < 300:
                self._record(result, 'valid')
            elif code in self.REDIRECT_CODES:
                self._record(result, 'redirect', 'redirect')
            elif code in self.DEAD_CODES:
                self._record(result, 'broken', 'not_found' if code == 404 else 'gone')
            else:
                # 403/429/451/5xx/etc. -- real server, just not a clean fetch.
                self._record(result, 'needs_manual', f'http_{code}')

        except asyncio.TimeoutError:
            self._record(result, 'timeout', 'timeout')
            result['notes'] = 'Request timed out'
        except aiohttp.ClientError as e:
            result['notes'] = str(e)
            if self._is_dns_error(e):
                self._record(result, 'broken', 'dns_error')
            else:
                # WAF reset, TLS quirk, transient blip -- not provably dead.
                self._record(result, 'needs_manual', 'connection_error')
        except Exception as e:
            result['notes'] = str(e)
            self._record(result, 'error', 'unknown_error')

        return result

    async def _ranged_get(self, url, domain, code, final_url):
        """Re-fetch with a ranged GET; returns the (possibly better) status."""
        try:
            await self._throttle(domain)
            async with self.session.get(
                url, allow_redirects=True, headers={'Range': 'bytes=0-0'}
            ) as gr:
                return gr.status, str(gr.url)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return code, final_url

    async def _retry_after(self, url, domain, code, final_url):
        """Sleep for Retry-After (capped) and GET once more on a 429."""
        try:
            await asyncio.sleep(2.0)  # conservative default backoff
            await self._throttle(domain)
            async with self.session.get(
                url, allow_redirects=True, headers={'Range': 'bytes=0-0'}
            ) as gr:
                return gr.status, str(gr.url)
        except (aiohttp.ClientError, asyncio.TimeoutError):
            return code, final_url

    async def validate_batch(self, urls: List[str], batch_size: int = 10, quiet: bool = False) -> List[Dict]:
        """Validate URLs in batches"""
        results = []
        unique_urls = list(set(urls))

        for i in range(0, len(unique_urls), batch_size):
            batch = unique_urls[i:i+batch_size]
            tasks = [self.validate_url(url) for url in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Progress indicator
            if not quiet:
                logger.info(f"Validated {min(i+batch_size, len(unique_urls))}/{len(unique_urls)} URLs")

        self.results = results
        return results

    def get_broken_links(self) -> List[Dict]:
        """Get all broken links"""
        return [r for r in self.results if r['status'] == 'broken']

    def get_redirects(self) -> List[Dict]:
        """Get all redirected links"""
        return [r for r in self.results if r['status'] == 'redirect']

    def save_results(self, output_file: Path, quiet: bool = False):
        """Save validation results"""
        data = {
            'validation_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        if not quiet:
            logger.info(f"\n✅ Validation complete!")
            logger.info(f"  Total: {self.stats['total']}")
            logger.info(f"  Valid: {self.stats['valid']}")
            logger.info(f"  Broken: {self.stats['broken']}")
            logger.info(f"  Needs manual review: {self.stats['needs_manual']}")
            logger.info(f"  Redirects: {self.stats['redirect']}")
            logger.info(f"  Timeouts: {self.stats['timeout']}")
            logger.info(f"  Errors: {self.stats['error']}")

async def main():
    parser = argparse.ArgumentParser(
        description='Simple link validator',
        epilog='''
Examples:
  %(prog)s --links links.json --output validation.json
  %(prog)s --links extracted-links.json --quiet
  %(prog)s --help
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--links', type=Path, default=Path('links.json'),
                       help='JSON file with extracted links')
    parser.add_argument('--output', type=Path, default=Path('validation.json'),
                       help='Output report file')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    if not args.links.exists():
        logger.error(f"Error: File not found: {args.links}")
        logger.error(f"Expected: {args.links.absolute()}")
        logger.error(f"Tip: Run from repository root or provide absolute path")
        sys.exit(2)

    # Load links
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    urls = [link['url'] for link in links_data.get('links', [])]
    if not args.quiet:
        logger.info(f"Validating {len(set(urls))} unique URLs...")

    # Validate
    async with SimpleValidator() as validator:
        await validator.validate_batch(urls, quiet=args.quiet)
        validator.save_results(args.output, quiet=args.quiet)

        # Show broken links
        broken = validator.get_broken_links()
        if broken and not args.quiet:
            logger.info(f"\n❌ Found {len(broken)} broken links:")
            for link in broken[:10]:
                logger.info(f"  - {link['url']}")
                if link.get('notes'):
                    logger.info(f"    {link['notes']}")

    return 0

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))