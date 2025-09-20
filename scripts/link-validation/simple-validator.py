#!/usr/bin/env python3
"""
SCRIPT: simple-validator.py
PURPOSE: Simple Link Validator
CATEGORY: utilities
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Simple Link Validator. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/simple-validator.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/simple-validator.py

    # With verbose output
    python scripts/simple-validator.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in utilities category]

MANIFEST_REGISTRY: scripts/simple-validator.py
"""

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse
from urllib.parse import urlparse

class SimpleValidator:
    """Simple link validator using only aiohttp"""

    def __init__(self):
        self.session = None
        self.results = []
        self.stats = {
            'total': 0,
            'valid': 0,
            'broken': 0,
            'redirect': 0,
            'timeout': 0,
            'error': 0
        }

    async def __aenter__(self):
        timeout = aiohttp.ClientTimeout(total=10)
        self.session = aiohttp.ClientSession(timeout=timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def validate_url(self, url: str) -> Dict:
        """Validate a single URL"""
        result = {
            'url': url,
            'status': 'unknown',
            'status_code': None,
            'issue_type': None,
            'notes': ''
        }

        try:
            async with self.session.head(url, allow_redirects=True) as response:
                result['status_code'] = response.status

                if response.status == 200:
                    result['status'] = 'valid'
                    self.stats['valid'] += 1
                elif response.status == 404:
                    result['status'] = 'broken'
                    result['issue_type'] = 'not_found'
                    self.stats['broken'] += 1
                elif response.status in [301, 302, 303, 307, 308]:
                    result['status'] = 'redirect'
                    result['issue_type'] = 'redirect'
                    final_url = str(response.url)
                    if final_url != url:
                        result['notes'] = f"Redirects to: {final_url}"
                    self.stats['redirect'] += 1
                elif response.status >= 500:
                    result['status'] = 'broken'
                    result['issue_type'] = 'server_error'
                    self.stats['broken'] += 1
                else:
                    result['status'] = 'degraded'
                    result['issue_type'] = f'http_{response.status}'

        except asyncio.TimeoutError:
            result['status'] = 'timeout'
            result['issue_type'] = 'timeout'
            self.stats['timeout'] += 1
        except aiohttp.ClientError as e:
            result['status'] = 'error'
            result['issue_type'] = 'connection_error'
            result['notes'] = str(e)
            self.stats['error'] += 1
        except Exception as e:
            result['status'] = 'error'
            result['issue_type'] = 'unknown_error'
            result['notes'] = str(e)
            self.stats['error'] += 1

        self.stats['total'] += 1
        return result

    async def validate_batch(self, urls: List[str], batch_size: int = 10) -> List[Dict]:
        """Validate URLs in batches"""
        results = []
        unique_urls = list(set(urls))

        for i in range(0, len(unique_urls), batch_size):
            batch = unique_urls[i:i+batch_size]
            tasks = [self.validate_url(url) for url in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)

            # Progress indicator
            print(f"Validated {min(i+batch_size, len(unique_urls))}/{len(unique_urls)} URLs")

        self.results = results
        return results

    def get_broken_links(self) -> List[Dict]:
        """Get all broken links"""
        return [r for r in self.results if r['status'] == 'broken']

    def get_redirects(self) -> List[Dict]:
        """Get all redirected links"""
        return [r for r in self.results if r['status'] == 'redirect']

    def save_results(self, output_file: Path):
        """Save validation results"""
        data = {
            'validation_date': datetime.now().isoformat(),
            'stats': self.stats,
            'results': self.results
        }

        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\n✅ Validation complete!")
        print(f"  Total: {self.stats['total']}")
        print(f"  Valid: {self.stats['valid']}")
        print(f"  Broken: {self.stats['broken']}")
        print(f"  Redirects: {self.stats['redirect']}")
        print(f"  Timeouts: {self.stats['timeout']}")
        print(f"  Errors: {self.stats['error']}")

async def main():
    parser = argparse.ArgumentParser(description='Simple link validator')
    parser.add_argument('--links', type=Path, default=Path('links.json'))
    parser.add_argument('--output', type=Path, default=Path('validation.json'))

    args = parser.parse_args()

    if not args.links.exists():
        print(f"Links file not found: {args.links}")
        return 1

    # Load links
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    urls = [link['url'] for link in links_data.get('links', [])]
    print(f"Validating {len(set(urls))} unique URLs...")

    # Validate
    async with SimpleValidator() as validator:
        await validator.validate_batch(urls)
        validator.save_results(args.output)

        # Show broken links
        broken = validator.get_broken_links()
        if broken:
            print(f"\n❌ Found {len(broken)} broken links:")
            for link in broken[:10]:
                print(f"  - {link['url']}")
                if link.get('notes'):
                    print(f"    {link['notes']}")

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))