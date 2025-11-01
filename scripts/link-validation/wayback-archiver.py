#!/usr/bin/env -S uv run python3
"""
SCRIPT: wayback-archiver.py
PURPOSE: Wayback Machine Archiver
CATEGORY: utilities
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Wayback Machine Archiver. This script is part of the utilities
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/wayback-archiver.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/wayback-archiver.py

    # With verbose output
    python scripts/wayback-archiver.py --verbose

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

MANIFEST_REGISTRY: scripts/wayback-archiver.py
"""

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import argparse
import time

@dataclass
class ArchiveResult:
    """Result of archiving operation"""
    url: str
    archived: bool
    archive_url: Optional[str]
    timestamp: Optional[str]
    status_code: Optional[int]
    error: Optional[str]

@dataclass
class ArchiveStatus:
    """Status of a URL in the Wayback Machine"""
    url: str
    is_archived: bool
    latest_snapshot: Optional[str]
    snapshot_timestamp: Optional[str]
    total_snapshots: int
    first_snapshot: Optional[str]
    availability_score: float

class WaybackArchiver:
    """Archives URLs to Wayback Machine and retrieves archived versions"""

    def __init__(self):
        self.session = None
        self.base_url = "https://web.archive.org"
        self.save_url = "https://web.archive.org/save/"
        self.availability_url = "http://archive.org/wayback/available"
        self.stats = {
            'checked': 0,
            'already_archived': 0,
            'newly_archived': 0,
            'failed': 0,
            'retrieved': 0
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_availability(self, url: str) -> ArchiveStatus:
        """Check if URL is available in Wayback Machine"""
        params = {'url': url}
        self.stats['checked'] += 1

        try:
            async with self.session.get(self.availability_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    snapshots = data.get('archived_snapshots', {})

                    if snapshots and 'closest' in snapshots:
                        snapshot = snapshots['closest']
                        is_available = snapshot.get('available', False)

                        if is_available:
                            self.stats['already_archived'] += 1
                            return ArchiveStatus(
                                url=url,
                                is_archived=True,
                                latest_snapshot=snapshot.get('url'),
                                snapshot_timestamp=snapshot.get('timestamp'),
                                total_snapshots=1,  # API only returns closest
                                first_snapshot=snapshot.get('timestamp'),
                                availability_score=100 if is_available else 0
                            )

                    return ArchiveStatus(
                        url=url,
                        is_archived=False,
                        latest_snapshot=None,
                        snapshot_timestamp=None,
                        total_snapshots=0,
                        first_snapshot=None,
                        availability_score=0
                    )

        except Exception as e:
            print(f"Error checking availability for {url}: {e}")
            return ArchiveStatus(
                url=url,
                is_archived=False,
                latest_snapshot=None,
                snapshot_timestamp=None,
                total_snapshots=0,
                first_snapshot=None,
                availability_score=0
            )

    async def archive_url(self, url: str, force: bool = False) -> ArchiveResult:
        """Archive a URL to Wayback Machine"""
        # Check if already archived (unless force)
        if not force:
            status = await self.check_availability(url)
            if status.is_archived and status.snapshot_timestamp:
                # Check if recent (within 30 days)
                snapshot_date = datetime.strptime(status.snapshot_timestamp[:8], "%Y%m%d")
                if datetime.now() - snapshot_date < timedelta(days=30):
                    return ArchiveResult(
                        url=url,
                        archived=True,
                        archive_url=status.latest_snapshot,
                        timestamp=status.snapshot_timestamp,
                        status_code=200,
                        error=None
                    )

        # Archive the URL
        save_endpoint = self.save_url + url

        try:
            # Use POST request with capture_all parameter
            data = {
                'url': url,
                'capture_all': 'on'
            }

            async with self.session.post(save_endpoint, data=data,
                                        allow_redirects=True,
                                        timeout=30) as response:
                if response.status == 200 or response.status == 302:
                    # Extract archived URL from response
                    final_url = str(response.url)
                    if '/web/' in final_url:
                        self.stats['newly_archived'] += 1
                        # Extract timestamp from URL
                        timestamp = final_url.split('/web/')[1].split('/')[0]
                        return ArchiveResult(
                            url=url,
                            archived=True,
                            archive_url=final_url,
                            timestamp=timestamp,
                            status_code=response.status,
                            error=None
                        )

                self.stats['failed'] += 1
                return ArchiveResult(
                    url=url,
                    archived=False,
                    archive_url=None,
                    timestamp=None,
                    status_code=response.status,
                    error=f"HTTP {response.status}"
                )

        except asyncio.TimeoutError:
            self.stats['failed'] += 1
            return ArchiveResult(
                url=url,
                archived=False,
                archive_url=None,
                timestamp=None,
                status_code=None,
                error="Timeout"
            )
        except Exception as e:
            self.stats['failed'] += 1
            return ArchiveResult(
                url=url,
                archived=False,
                archive_url=None,
                timestamp=None,
                status_code=None,
                error=str(e)
            )

    async def retrieve_archived_version(self, url: str,
                                      timestamp: Optional[str] = None) -> Optional[str]:
        """Retrieve archived version of URL"""
        status = await self.check_availability(url)

        if status.is_archived and status.latest_snapshot:
            self.stats['retrieved'] += 1
            return status.latest_snapshot

        return None

    async def batch_archive(self, urls: List[str],
                          priority_domains: List[str] = None,
                          delay: float = 1.0) -> List[ArchiveResult]:
        """Archive multiple URLs with rate limiting"""
        results = []

        # Prioritize certain domains
        if priority_domains:
            priority_urls = [u for u in urls
                           if any(d in u for d in priority_domains)]
            regular_urls = [u for u in urls if u not in priority_urls]
            sorted_urls = priority_urls + regular_urls
        else:
            sorted_urls = urls

        for i, url in enumerate(sorted_urls):
            print(f"[{i+1}/{len(sorted_urls)}] Archiving: {url}")

            result = await self.archive_url(url)
            results.append(result)

            if result.archived:
                print(f"  ✅ Archived: {result.archive_url}")
            else:
                print(f"  ❌ Failed: {result.error}")

            # Rate limiting
            if i < len(sorted_urls) - 1:
                await asyncio.sleep(delay)

        return results

    async def find_alternatives_for_broken(self, broken_urls: List[str]) -> Dict[str, str]:
        """Find Wayback alternatives for broken URLs"""
        alternatives = {}

        for url in broken_urls:
            archived = await self.retrieve_archived_version(url)
            if archived:
                alternatives[url] = archived
                print(f"✅ Found archived version for: {url}")
                print(f"   Archive: {archived}")

        return alternatives

    def generate_archive_report(self, results: List[ArchiveResult],
                               statuses: List[ArchiveStatus],
                               output_file: Path):
        """Generate archiving report"""
        report = {
            'generated': datetime.now().isoformat(),
            'stats': self.stats,
            'archived_urls': [],
            'failed_urls': [],
            'archive_status': []
        }

        for result in results:
            if result.archived:
                report['archived_urls'].append({
                    'url': result.url,
                    'archive_url': result.archive_url,
                    'timestamp': result.timestamp
                })
            else:
                report['failed_urls'].append({
                    'url': result.url,
                    'error': result.error
                })

        for status in statuses:
            if status.is_archived:
                report['archive_status'].append(asdict(status))

        # Write JSON report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Generate markdown report
        md_file = output_file.with_suffix('.md')
        lines = []
        lines.append("# Wayback Machine Archive Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n## Statistics")
        lines.append(f"- **URLs Checked:** {self.stats['checked']}")
        lines.append(f"- **Already Archived:** {self.stats['already_archived']}")
        lines.append(f"- **Newly Archived:** {self.stats['newly_archived']}")
        lines.append(f"- **Failed:** {self.stats['failed']}")
        lines.append(f"- **Retrieved:** {self.stats['retrieved']}")

        if report['archived_urls']:
            lines.append(f"\n## Successfully Archived ({len(report['archived_urls'])})")
            for item in report['archived_urls'][:20]:
                lines.append(f"\n- **Original:** {item['url']}")
                lines.append(f"  **Archive:** {item['archive_url']}")

        if report['failed_urls']:
            lines.append(f"\n## Failed to Archive ({len(report['failed_urls'])})")
            for item in report['failed_urls'][:10]:
                lines.append(f"- {item['url']}: {item['error']}")

        with open(md_file, 'w') as f:
            f.write('\n'.join(lines))

        print(f"✅ Report saved to {md_file}")

async def archive_critical_links(links_file: Path, output_file: Path):
    """Archive critical links from blog posts"""
    # Define critical domains that should be archived
    CRITICAL_DOMAINS = [
        'arxiv.org',
        'doi.org',
        'github.com',
        'owasp.org',
        'nist.gov',
        'cisa.gov',
        'nvd.nist.gov',
        'cve.mitre.org'
    ]

    with open(links_file, 'r') as f:
        links_data = json.load(f)

    # Filter to critical links
    all_urls = list(set(link['url'] for link in links_data.get('links', [])))
    critical_urls = [
        url for url in all_urls
        if any(domain in url for domain in CRITICAL_DOMAINS)
    ]

    print(f"Found {len(critical_urls)} critical URLs to archive")

    async with WaybackArchiver() as archiver:
        # Check current archive status
        print("\n📊 Checking archive status...")
        statuses = []
        for url in critical_urls[:50]:  # Limit to avoid rate limiting
            status = await archiver.check_availability(url)
            statuses.append(status)

        # Archive URLs that need it
        not_archived = [s.url for s in statuses if not s.is_archived]
        old_archives = [
            s.url for s in statuses
            if s.is_archived and s.snapshot_timestamp and
            (datetime.now() - datetime.strptime(s.snapshot_timestamp[:8], "%Y%m%d")) > timedelta(days=90)
        ]

        to_archive = not_archived + old_archives
        print(f"\n📦 Archiving {len(to_archive)} URLs...")

        if to_archive:
            results = await archiver.batch_archive(to_archive[:20])  # Limit batch size
        else:
            results = []

        # Generate report
        archiver.generate_archive_report(results, statuses, output_file)

async def main():
    parser = argparse.ArgumentParser(description='Archive links to Wayback Machine')
    parser.add_argument('--links', type=Path, default=Path('links.json'),
                       help='JSON file with extracted links')
    parser.add_argument('--validation', type=Path, default=Path('validation.json'),
                       help='Validation results to find broken links')
    parser.add_argument('--archive-all', action='store_true',
                       help='Archive all links, not just critical ones')
    parser.add_argument('--find-alternatives', action='store_true',
                       help='Find archived alternatives for broken links')
    parser.add_argument('--output', type=Path, default=Path('archive-report.json'),
                       help='Output report file')

    args = parser.parse_args()

    if args.find_alternatives:
        # Find alternatives for broken links
        if not args.validation.exists():
            print(f"Validation file not found: {args.validation}")
            return 1

        with open(args.validation, 'r') as f:
            validation_data = json.load(f)

        broken_urls = [
            r['url'] for r in validation_data.get('results', [])
            if r.get('status') == 'broken'
        ]

        print(f"Finding archived alternatives for {len(broken_urls)} broken links...")

        async with WaybackArchiver() as archiver:
            alternatives = await archiver.find_alternatives_for_broken(broken_urls)

            # Save alternatives
            with open('wayback-alternatives.json', 'w') as f:
                json.dump(alternatives, f, indent=2)

            print(f"\n✅ Found {len(alternatives)} archived alternatives")

    else:
        # Archive links
        if not args.links.exists():
            print(f"Links file not found: {args.links}")
            return 1

        if args.archive_all:
            print("Archiving all links...")
            # Archive all links
            with open(args.links, 'r') as f:
                links_data = json.load(f)
            urls = list(set(link['url'] for link in links_data.get('links', [])))

            async with WaybackArchiver() as archiver:
                results = await archiver.batch_archive(urls[:50])  # Limit for testing
                archiver.generate_archive_report(results, [], args.output)
        else:
            # Archive critical links only
            await archive_critical_links(args.links, args.output)

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))