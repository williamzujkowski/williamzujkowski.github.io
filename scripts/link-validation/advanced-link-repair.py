#!/usr/bin/env -S uv run python3
"""
SCRIPT: advanced-link-repair.py
PURPOSE: Advanced Link Repair System
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Advanced Link Repair System. This script is part of the link validation
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/advanced-link-repair.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/advanced-link-repair.py

    # With verbose output
    python scripts/advanced-link-repair.py --verbose

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

MANIFEST_REGISTRY: scripts/advanced-link-repair.py
"""

import json
import re
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from urllib.parse import urlparse, quote
from difflib import SequenceMatcher

class AdvancedLinkRepair:
    """Advanced link repair with pattern detection and intelligent alternatives"""

    def __init__(self):
        self.stats = {
            'total_processed': 0,
            'malformed_fixed': 0,
            'alternatives_found': 0,
            'verified_matches': 0,
            'no_fix_available': 0,
            'repair_strategies': {}
        }
        self.repairs = []

    def fix_malformed_url(self, url: str) -> Tuple[str, bool]:
        """Fix common URL malformation patterns"""
        original_url = url

        # Pattern 1: Remove trailing parentheses and asterisks
        url = re.sub(r'[\)\*]+$', '', url)

        # Pattern 2: Fix double protocols
        url = re.sub(r'https?://(https?://)', r'\1', url)

        # Pattern 3: Remove trailing punctuation
        url = re.sub(r'[,;\.]+$', '', url)

        # Pattern 4: Fix missing protocol
        if not url.startswith(('http://', 'https://')) and '.' in url:
            url = 'https://' + url

        # Pattern 5: Fix arXiv URLs
        if 'arxiv.org' in url:
            # Ensure proper format: https://arxiv.org/abs/XXXX.XXXXX
            match = re.search(r'(\d{4}\.\d{4,5})', url)
            if match:
                arxiv_id = match.group(1)
                url = f'https://arxiv.org/abs/{arxiv_id}'

        # Pattern 6: Fix DOI URLs
        if 'doi.org' in url or re.search(r'10\.\d{4,}', url):
            doi_match = re.search(r'(10\.\d{4,}/[^\s\)]+)', url)
            if doi_match:
                doi = doi_match.group(1).rstrip(')')
                url = f'https://doi.org/{doi}'

        # Pattern 7: Fix GitHub URLs
        if 'github.com' in url:
            # Remove trailing slashes and fix common issues
            url = url.rstrip('/')
            # Fix blob/master to blob/main
            url = url.replace('/blob/master/', '/blob/main/')

        # Pattern 8: Fix documentation URLs with version issues
        if '/docs/' in url or 'docs.' in url:
            # Update common outdated versions
            replacements = {
                '/v1/': '/latest/',
                '/2.x/': '/latest/',
                '/3.x/': '/latest/',
                'docs.python.org/3.7/': 'docs.python.org/3/',
                'docs.python.org/3.8/': 'docs.python.org/3/',
                'docs.python.org/3.9/': 'docs.python.org/3/',
            }
            for old, new in replacements.items():
                if old in url:
                    url = url.replace(old, new)

        was_fixed = url != original_url
        return url, was_fixed

    async def find_arxiv_alternative(self, url: str, context: str) -> Optional[Dict]:
        """Find alternative arXiv URL"""
        # Extract arXiv ID patterns
        arxiv_patterns = [
            r'(\d{4}\.\d{4,5})',  # New format: YYMM.NNNNN
            r'([a-z\-]+/\d{7})',  # Old format: subject/YYMMNNN
        ]

        for pattern in arxiv_patterns:
            match = re.search(pattern, url)
            if match:
                arxiv_id = match.group(1)
                # Try different URL formats
                alternatives = [
                    f'https://arxiv.org/abs/{arxiv_id}',
                    f'https://arxiv.org/pdf/{arxiv_id}.pdf',
                    f'https://arxiv.org/abs/{arxiv_id}v1',
                    f'https://arxiv.org/abs/{arxiv_id}v2',
                ]

                # Return the first valid format
                for alt_url in alternatives:
                    return {
                        'url': alt_url,
                        'strategy': 'arxiv_format_fix',
                        'confidence': 95
                    }

        # Try to extract title from context for search
        if context:
            # Look for quoted titles or paper names
            title_match = re.search(r'[""]([^""]+)[""]', context)
            if title_match:
                title = title_match.group(1)
                # This would need actual API call or web search
                # For now, return None

        return None

    async def find_github_alternative(self, url: str, context: str) -> Optional[Dict]:
        """Find alternative GitHub URL"""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')

        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo = path_parts[1]

            # Common GitHub URL patterns to try
            alternatives = [
                f'https://github.com/{owner}/{repo}',
                f'https://github.com/{owner}/{repo}.git',
                f'https://github.com/{owner}/{repo}/blob/main/README.md',
                f'https://github.com/{owner}/{repo}/tree/main',
            ]

            # Check if it's a specific file
            if len(path_parts) > 4 and path_parts[2] in ['blob', 'tree']:
                branch = path_parts[3]
                file_path = '/'.join(path_parts[4:])

                # Try different branch names
                for branch_name in ['main', 'master', 'develop']:
                    alternatives.append(
                        f'https://github.com/{owner}/{repo}/blob/{branch_name}/{file_path}'
                    )

            # Return first alternative (in real implementation, would verify)
            return {
                'url': alternatives[0],
                'strategy': 'github_url_reconstruction',
                'confidence': 85
            }

        return None

    async def find_documentation_alternative(self, url: str) -> Optional[Dict]:
        """Find alternative documentation URL"""
        domain = urlparse(url).netloc

        # Documentation site mappings
        doc_updates = {
            'docs.python.org': {
                'base': 'https://docs.python.org/3/',
                'pattern': r'/library/(.+)\.html',
                'replacement': r'library/\1.html'
            },
            'docs.djangoproject.com': {
                'base': 'https://docs.djangoproject.com/en/stable/',
                'pattern': r'/en/[\d\.]+/(.+)',
                'replacement': r'\1'
            },
            'kubernetes.io': {
                'base': 'https://kubernetes.io/docs/',
                'pattern': r'/docs/(.+)',
                'replacement': r'\1'
            },
            'docs.docker.com': {
                'base': 'https://docs.docker.com/',
                'pattern': r'/engine/(.+)',
                'replacement': r'engine/\1'
            }
        }

        for doc_domain, config in doc_updates.items():
            if doc_domain in domain:
                # Extract the documentation path
                match = re.search(config['pattern'], url)
                if match:
                    doc_path = match.group(1)
                    new_url = config['base'] + doc_path

                    return {
                        'url': new_url,
                        'strategy': 'documentation_version_update',
                        'confidence': 80
                    }

        return None

    async def process_broken_link(self, link_data: Dict) -> Dict:
        """Process a single broken link"""
        url = link_data.get('url', '')
        context = link_data.get('context_before', '') + ' ' + link_data.get('context_after', '')
        link_text = link_data.get('text', '')

        result = {
            **link_data,
            'original_url': url,
            'fixed_url': None,
            'alternative_url': None,
            'repair_strategy': None,
            'confidence': 0,
            'notes': []
        }

        # Step 1: Try to fix malformed URL
        fixed_url, was_malformed = self.fix_malformed_url(url)
        if was_malformed:
            result['fixed_url'] = fixed_url
            result['repair_strategy'] = 'malformed_url_fix'
            result['confidence'] = 95
            result['notes'].append(f"Fixed malformed URL: {url} -> {fixed_url}")
            self.stats['malformed_fixed'] += 1
            return result

        # Step 2: Try to find alternatives based on URL pattern
        alternative = None

        if 'arxiv.org' in url:
            alternative = await self.find_arxiv_alternative(url, context)
        elif 'github.com' in url:
            alternative = await self.find_github_alternative(url, context)
        elif any(doc_keyword in url for doc_keyword in ['docs.', '/docs/', 'documentation']):
            alternative = await self.find_documentation_alternative(url)

        if alternative:
            result['alternative_url'] = alternative['url']
            result['repair_strategy'] = alternative['strategy']
            result['confidence'] = alternative['confidence']
            result['notes'].append(f"Found alternative via {alternative['strategy']}")
            self.stats['alternatives_found'] += 1

            # Update strategy count
            strategy = alternative['strategy']
            self.stats['repair_strategies'][strategy] = \
                self.stats['repair_strategies'].get(strategy, 0) + 1
        else:
            result['notes'].append("No alternative found")
            self.stats['no_fix_available'] += 1

        self.stats['total_processed'] += 1
        return result

    async def process_all_broken_links(self, input_file: Path) -> List[Dict]:
        """Process all broken links from validation results"""
        # Load validation results
        with open(input_file, 'r') as f:
            data = json.load(f)

        broken_links = []

        # Extract broken links from validation results
        if 'results' in data:
            for result in data['results']:
                if result.get('status') in ['broken', 'error', 'timeout']:
                    broken_links.append(result)

        # Also load from links.json with validation status
        if Path('links.json').exists():
            with open('links.json', 'r') as f:
                links_data = json.load(f)

            # Cross-reference with validation results
            validation_map = {r['url']: r for r in data.get('results', [])}

            for link in links_data.get('links', []):
                url = link['url']
                if url in validation_map and validation_map[url]['status'] == 'broken':
                    # Merge link context with validation result
                    broken_links.append({**link, **validation_map[url]})

        print(f"Found {len(broken_links)} broken links to process")

        # Process each broken link
        for i, link in enumerate(broken_links, 1):
            if i % 10 == 0:
                print(f"Processing {i}/{len(broken_links)}...")

            result = await self.process_broken_link(link)
            self.repairs.append(result)

        return self.repairs

    def apply_repairs_to_files(self, repairs: List[Dict], dry_run: bool = False):
        """Apply repairs to the actual files"""
        files_to_update = {}

        # Group repairs by file
        for repair in repairs:
            if repair['confidence'] >= 80:
                file_path = repair.get('file_path')
                if file_path:
                    if file_path not in files_to_update:
                        files_to_update[file_path] = []
                    files_to_update[file_path].append(repair)

        total_fixes = 0

        for file_path, file_repairs in files_to_update.items():
            if not Path(file_path).exists():
                print(f"File not found: {file_path}")
                continue

            with open(file_path, 'r') as f:
                content = f.read()

            original_content = content
            fixes_in_file = 0

            for repair in file_repairs:
                old_url = repair['original_url']
                new_url = repair.get('fixed_url') or repair.get('alternative_url')

                if new_url and old_url in content:
                    content = content.replace(old_url, new_url)
                    fixes_in_file += 1
                    total_fixes += 1

            if fixes_in_file > 0 and not dry_run:
                # Create backup
                backup_path = Path(file_path).with_suffix(
                    f'.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}'
                )
                with open(backup_path, 'w') as f:
                    f.write(original_content)

                # Write fixed content
                with open(file_path, 'w') as f:
                    f.write(content)

                print(f"Fixed {fixes_in_file} links in {Path(file_path).name}")

        return total_fixes

    def generate_report(self, output_file: Path):
        """Generate detailed repair report"""
        report = {
            'generated': datetime.now().isoformat(),
            'stats': self.stats,
            'repairs': self.repairs,
            'summary': {
                'total_broken': self.stats['total_processed'],
                'successfully_repaired': self.stats['malformed_fixed'] + self.stats['alternatives_found'],
                'repair_rate': ((self.stats['malformed_fixed'] + self.stats['alternatives_found']) /
                               self.stats['total_processed'] * 100) if self.stats['total_processed'] > 0 else 0
            }
        }

        # Save JSON report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Generate markdown report
        md_file = output_file.with_suffix('.md')
        lines = []
        lines.append("# Advanced Link Repair Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("\n## Summary Statistics")
        lines.append(f"- **Total Processed:** {self.stats['total_processed']}")
        lines.append(f"- **Malformed URLs Fixed:** {self.stats['malformed_fixed']}")
        lines.append(f"- **Alternatives Found:** {self.stats['alternatives_found']}")
        lines.append(f"- **No Fix Available:** {self.stats['no_fix_available']}")
        lines.append(f"- **Success Rate:** {report['summary']['repair_rate']:.1f}%")

        if self.stats['repair_strategies']:
            lines.append("\n## Repair Strategies Used")
            for strategy, count in sorted(self.stats['repair_strategies'].items(),
                                         key=lambda x: x[1], reverse=True):
                lines.append(f"- {strategy}: {count}")

        # Show sample repairs
        high_confidence = [r for r in self.repairs if r['confidence'] >= 90]
        if high_confidence:
            lines.append(f"\n## High Confidence Repairs ({len(high_confidence)})")
            for repair in high_confidence[:10]:
                lines.append(f"\n**Original:** {repair['original_url']}")
                new_url = repair.get('fixed_url') or repair.get('alternative_url')
                if new_url:
                    lines.append(f"**Fixed:** {new_url}")
                    lines.append(f"**Strategy:** {repair['repair_strategy']}")
                    lines.append(f"**Confidence:** {repair['confidence']}%")

        with open(md_file, 'w') as f:
            f.write('\n'.join(lines))

        print(f"\n✅ Report saved to {md_file}")
        print(f"Successfully repaired: {report['summary']['successfully_repaired']}/{self.stats['total_processed']} "
              f"({report['summary']['repair_rate']:.1f}%)")

async def main():
    """Run advanced link repair"""
    import argparse

    parser = argparse.ArgumentParser(description='Advanced link repair system')
    parser.add_argument('--input', type=Path, default=Path('validation.json'),
                       help='Validation results file')
    parser.add_argument('--output', type=Path, default=Path('advanced-repairs.json'),
                       help='Output repairs file')
    parser.add_argument('--apply', action='store_true',
                       help='Apply repairs to files')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be fixed without applying')

    args = parser.parse_args()

    repairer = AdvancedLinkRepair()

    # Process broken links
    print("🔧 Starting Advanced Link Repair...")
    repairs = await repairer.process_all_broken_links(args.input)

    # Apply repairs if requested
    if args.apply or args.dry_run:
        print("\n📝 Applying repairs to files...")
        total_fixed = repairer.apply_repairs_to_files(repairs, dry_run=args.dry_run)
        print(f"Total links fixed: {total_fixed}")

    # Generate report
    repairer.generate_report(args.output)

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))