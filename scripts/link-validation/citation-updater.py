#!/usr/bin/env -S uv run python3
"""
SCRIPT: citation-updater.py
PURPOSE: Citation Updater
CATEGORY: academic_research
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Citation Updater. This script is part of the academic research
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/citation-updater.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/citation-updater.py

    # With verbose output
    python scripts/citation-updater.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in academic_research category]

MANIFEST_REGISTRY: scripts/citation-updater.py
"""

import json
import re
import asyncio
import aiohttp
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict
import argparse

# Path setup for centralized logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)

@dataclass
class CitationUpdate:
    """Represents a citation update"""
    original_citation: str
    updated_citation: str
    url_old: str
    url_new: str
    reason: str
    confidence: float
    metadata: Dict

class CitationUpdater:
    """Updates citations to newer versions and better sources"""

    def __init__(self):
        self.session = None
        self.stats = {
            'total_citations': 0,
            'updated': 0,
            'already_current': 0,
            'no_update_found': 0,
            'errors': 0
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def check_arxiv_version(self, url: str) -> Optional[CitationUpdate]:
        """Check if arXiv paper has newer version"""
        # Extract arXiv ID
        match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)(?:v(\d+))?', url)
        if not match:
            return None

        arxiv_id = match.group(1)
        current_version = int(match.group(2)) if match.group(2) else 1

        # Check latest version via arXiv API
        api_url = f"http://export.arxiv.org/api/query?id_list={arxiv_id}"

        try:
            async with self.session.get(api_url) as response:
                if response.status == 200:
                    content = await response.text()

                    # Parse version from response
                    version_match = re.search(r'<arxiv:comment>.*v(\d+)', content)
                    if version_match:
                        latest_version = int(version_match.group(1))
                    else:
                        # Try alternative parsing
                        version_matches = re.findall(r'/abs/\d+\.\d+v(\d+)', content)
                        latest_version = max(int(v) for v in version_matches) if version_matches else current_version

                    if latest_version > current_version:
                        new_url = re.sub(r'(arxiv\.org/(?:abs|pdf)/\d+\.\d+)(?:v\d+)?',
                                       f'\\1v{latest_version}', url)

                        # Get paper title
                        title_match = re.search(r'<title>([^<]+)</title>', content)
                        title = title_match.group(1) if title_match else "Paper"

                        return CitationUpdate(
                            original_citation=f"[{title}]({url})",
                            updated_citation=f"[{title}]({new_url})",
                            url_old=url,
                            url_new=new_url,
                            reason=f"Updated to version {latest_version} (from v{current_version})",
                            confidence=95,
                            metadata={'latest_version': latest_version, 'old_version': current_version}
                        )

        except Exception as e:
            logger.error(f"Error checking arXiv version: {e}")

        return None

    async def resolve_doi(self, url: str) -> Optional[CitationUpdate]:
        """Resolve DOI to current URL"""
        # Check if it's a DOI URL
        doi_match = re.search(r'doi\.org/(10\.\d+/[^/\s]+)', url)
        if not doi_match:
            return None

        doi = doi_match.group(1)

        # Check current resolution
        try:
            async with self.session.get(url, allow_redirects=True) as response:
                final_url = str(response.url)

                if final_url != url and response.status == 200:
                    # Get metadata from CrossRef
                    crossref_url = f"https://api.crossref.org/works/{doi}"
                    async with self.session.get(crossref_url) as meta_response:
                        if meta_response.status == 200:
                            data = await meta_response.json()
                            title = data['message'].get('title', ['Unknown'])[0]
                            year = data['message'].get('published-print', {}).get('date-parts', [[None]])[0][0]

                            # Check if there's an open access version
                            if 'link' in data['message']:
                                for link in data['message']['link']:
                                    if link.get('content-version') == 'vor' and link.get('URL'):
                                        if 'open' in link.get('intended-application', '').lower():
                                            final_url = link['URL']
                                            reason = "Updated to open access version"
                                            break

                            return CitationUpdate(
                                original_citation=f"[{title}]({url})",
                                updated_citation=f"[{title}]({final_url})",
                                url_old=url,
                                url_new=final_url,
                                reason="DOI resolved to publisher URL",
                                confidence=90,
                                metadata={'doi': doi, 'year': year}
                            )

        except Exception as e:
            logger.error(f"Error resolving DOI: {e}")

        return None

    async def update_documentation_links(self, url: str) -> Optional[CitationUpdate]:
        """Update documentation links to latest versions"""
        updates = {
            # Python docs
            r'docs\.python\.org/(\d+)\.(\d+)/': {
                'latest': '3.12',
                'pattern': r'docs\.python\.org/(\d+)\.(\d+)/',
                'name': 'Python'
            },
            # Django docs
            r'docs\.djangoproject\.com/en/(\d+)\.(\d+)/': {
                'latest': '5.0',
                'pattern': r'docs\.djangoproject\.com/en/(\d+)\.(\d+)/',
                'name': 'Django'
            },
            # React docs
            r'reactjs\.org/docs/': {
                'new_domain': 'react.dev',
                'name': 'React'
            },
            # Node.js docs
            r'nodejs\.org/dist/latest-v(\d+)\.x/docs/': {
                'latest': '20',
                'pattern': r'nodejs\.org/dist/latest-v(\d+)\.x/docs/',
                'name': 'Node.js'
            }
        }

        for pattern, config in updates.items():
            if re.search(pattern, url):
                if 'new_domain' in config:
                    # Domain change
                    new_url = url.replace('reactjs.org', config['new_domain'])
                    return CitationUpdate(
                        original_citation=f"[{config['name']} Documentation]({url})",
                        updated_citation=f"[{config['name']} Documentation]({new_url})",
                        url_old=url,
                        url_new=new_url,
                        reason=f"{config['name']} documentation moved to new domain",
                        confidence=95,
                        metadata={'type': 'domain_change'}
                    )
                elif 'latest' in config:
                    # Version update
                    match = re.search(config['pattern'], url)
                    if match:
                        current_version = f"{match.group(1)}.{match.group(2)}"
                        if current_version != config['latest']:
                            new_url = re.sub(config['pattern'],
                                           config['pattern'].replace(r'(\d+)\.(\d+)',
                                                                    config['latest']),
                                           url)
                            return CitationUpdate(
                                original_citation=f"[{config['name']} {current_version} Documentation]({url})",
                                updated_citation=f"[{config['name']} {config['latest']} Documentation]({new_url})",
                                url_old=url,
                                url_new=new_url,
                                reason=f"Updated to latest {config['name']} version",
                                confidence=85,
                                metadata={'old_version': current_version, 'new_version': config['latest']}
                            )

        return None

    async def find_open_access_version(self, url: str, title: str = "") -> Optional[CitationUpdate]:
        """Find open access version of paywalled paper"""
        # Try Unpaywall API (no key required for small volume)
        if 'doi.org' in url:
            doi_match = re.search(r'doi\.org/(10\.\d+/[^/\s]+)', url)
            if doi_match:
                doi = doi_match.group(1)
                unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email=test@example.com"

                try:
                    async with self.session.get(unpaywall_url) as response:
                        if response.status == 200:
                            data = await response.json()
                            if data.get('is_oa'):
                                oa_url = data.get('best_oa_location', {}).get('url')
                                if oa_url and oa_url != url:
                                    return CitationUpdate(
                                        original_citation=f"[{title or 'Paper'}]({url})",
                                        updated_citation=f"[{title or 'Paper'}]({oa_url})",
                                        url_old=url,
                                        url_new=oa_url,
                                        reason="Found open access version",
                                        confidence=90,
                                        metadata={'oa_type': data.get('oa_status')}
                                    )
                except Exception:
                    pass

        return None

    async def update_citation(self, citation_data: Dict) -> Optional[CitationUpdate]:
        """Update a single citation"""
        url = citation_data.get('url', '')
        text = citation_data.get('text', '')

        # Try different update strategies
        update = None

        # 1. Check arXiv versions
        if 'arxiv.org' in url:
            update = await self.check_arxiv_version(url)

        # 2. Resolve DOIs
        if not update and 'doi.org' in url:
            update = await self.resolve_doi(url)

        # 3. Update documentation links
        if not update and any(d in url for d in ['docs.', 'documentation', 'developer.']):
            update = await self.update_documentation_links(url)

        # 4. Find open access versions
        if not update and 'doi.org' in url:
            update = await self.find_open_access_version(url, text)

        return update

    async def update_all_citations(self, citations: List[Dict]) -> List[CitationUpdate]:
        """Update all citations"""
        updates = []
        self.stats['total_citations'] = len(citations)

        # Process in batches to avoid overwhelming APIs
        batch_size = 10
        for i in range(0, len(citations), batch_size):
            batch = citations[i:i+batch_size]
            tasks = [self.update_citation(c) for c in batch]
            results = await asyncio.gather(*tasks)

            for result in results:
                if result:
                    updates.append(result)
                    self.stats['updated'] += 1
                else:
                    self.stats['no_update_found'] += 1

            # Small delay between batches
            await asyncio.sleep(1)

        return updates

    def apply_updates_to_file(self, file_path: Path, updates: List[CitationUpdate],
                             dry_run: bool = False) -> int:
        """Apply citation updates to a file"""
        if not updates:
            return 0

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Sort updates by position to maintain correct offsets
        for update in updates:
            if update.url_old in content:
                # Replace URL
                content = content.replace(update.url_old, update.url_new)
                changes_made += 1

                # Update citation text if needed
                if update.original_citation != update.updated_citation:
                    # Try to replace full citation
                    if update.original_citation in content:
                        content = content.replace(update.original_citation,
                                                update.updated_citation)

        if changes_made > 0 and not dry_run:
            # Create backup
            backup_path = file_path.with_suffix(f'.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)

            # Write updated content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            logger.info(f"✅ Updated {changes_made} citations in {file_path.name}")
            logger.info(f"   Backup saved to {backup_path.name}")

        elif dry_run:
            logger.info(f"Would update {changes_made} citations in {file_path.name}")

        return changes_made

    def generate_update_report(self, updates: List[CitationUpdate], output_file: Path):
        """Generate report of citation updates"""
        report = {
            'generated': datetime.now().isoformat(),
            'stats': self.stats,
            'updates': [asdict(u) for u in updates]
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Also generate markdown report
        md_file = output_file.with_suffix('.md')
        lines = []
        lines.append("# Citation Update Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"\n## Statistics")
        lines.append(f"- **Total Citations:** {self.stats['total_citations']}")
        lines.append(f"- **Updated:** {self.stats['updated']}")
        lines.append(f"- **Already Current:** {self.stats['already_current']}")
        lines.append(f"- **No Update Found:** {self.stats['no_update_found']}")

        if updates:
            lines.append(f"\n## Updates Available ({len(updates)})")

            # Group by reason
            by_reason = {}
            for update in updates:
                reason = update.reason
                if reason not in by_reason:
                    by_reason[reason] = []
                by_reason[reason].append(update)

            for reason, items in by_reason.items():
                lines.append(f"\n### {reason} ({len(items)} citations)")
                for update in items[:5]:  # Show first 5
                    lines.append(f"\n**Old:** {update.url_old}")
                    lines.append(f"**New:** {update.url_new}")
                    lines.append(f"**Confidence:** {update.confidence}%")

                if len(items) > 5:
                    lines.append(f"\n...and {len(items) - 5} more")

        with open(md_file, 'w') as f:
            f.write('\n'.join(lines))

        logger.info(f"✅ Report saved to {md_file}")

async def main():
    parser = argparse.ArgumentParser(
        description='Update citations to newer versions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update citations from links file
  python scripts/link-validation/citation-updater.py

  # Dry run to preview updates
  python scripts/link-validation/citation-updater.py --dry-run

  # Specify custom links file
  python scripts/link-validation/citation-updater.py --links custom-links.json

  # Quiet mode
  python scripts/link-validation/citation-updater.py --quiet
        """
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--links', type=Path, default=Path('links.json'),
                       help='JSON file with extracted links')
    parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                       help='Directory containing blog posts')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying files')
    parser.add_argument('--output', type=Path, default=Path('citation-updates.json'),
                       help='Output report file')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress output messages')

    args = parser.parse_args()

    try:
        if not args.links.exists():
            logger.error(f"❌ Error: Links file not found: {args.links}")
            return 1

    # Load links
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    # Filter to citations only
    citations = [
        link for link in links_data.get('links', [])
        if link.get('type') in ['citation', 'reference']
    ]

    logger.info(f"Found {len(citations)} citations to check")

    # Update citations
    async with CitationUpdater() as updater:
        updates = await updater.update_all_citations(citations)

        if updates:
            logger.info(f"\n📊 Found {len(updates)} citations that can be updated")

            # Group updates by file
            updates_by_file = {}
            for update in updates:
                # Find which file contains this citation
                for citation in citations:
                    if citation['url'] == update.url_old:
                        file_path = citation['file_path']
                        if file_path not in updates_by_file:
                            updates_by_file[file_path] = []
                        updates_by_file[file_path].append(update)
                        break

            # Apply updates to each file
            if not args.dry_run:
                logger.info("\n✏️ Applying updates...")
            else:
                logger.info("\n🔍 DRY RUN - No changes will be made")

            total_changes = 0
            for file_path, file_updates in updates_by_file.items():
                changes = updater.apply_updates_to_file(
                    Path(file_path), file_updates, args.dry_run
                )
                total_changes += changes

            logger.info(f"\n✅ Total citations updated: {total_changes}")

            # Generate report
        updater.generate_update_report(updates, args.output)

        return 0

    except FileNotFoundError as e:
        logger.error(f"❌ Error: File not found - {e}")
        return 1
    except Exception as e:
        logger.error(f"❌ Error: {e}")
        return 2

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))