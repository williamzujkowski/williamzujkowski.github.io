#!/usr/bin/env python3
"""
SCRIPT: link-extractor.py
PURPOSE: Link Extractor for Blog Posts
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Link Extractor for Blog Posts. This script is part of the link validation
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/link-extractor.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/link-extractor.py

    # With verbose output
    python scripts/link-extractor.py --verbose

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

MANIFEST_REGISTRY: scripts/link-extractor.py
"""

import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib

@dataclass
class LinkContext:
    """Represents a link with its surrounding context"""
    url: str
    text: str
    type: str  # citation, reference, inline, resource
    context_before: str
    context_after: str
    file_path: str
    line_number: int
    position: int
    hash: str

    def to_dict(self):
        return asdict(self)

class LinkExtractor:
    """Extract and categorize links from markdown files"""

    # Link patterns
    PATTERNS = {
        'markdown_link': r'\[([^\]]+)\]\(([^)]+)\)',
        'reference_link': r'\[([^\]]+)\]\[([^\]]+)\]',
        'reference_def': r'^\[([^\]]+)\]:\s*(.+)$',
        'bare_url': r'(?:https?://[^\s<>"{}|\\^`\[\]]+)',
        'doi': r'(?:https?://)?(?:dx\.)?doi\.org/[^\s]+',
        'arxiv': r'(?:https?://)?arxiv\.org/(?:abs|pdf)/[\d.]+(?:v\d+)?'
    }

    # Link type classification patterns
    TYPE_PATTERNS = {
        'citation': [
            r'research', r'paper', r'study', r'analysis', r'journal',
            r'arxiv', r'doi\.org', r'pubmed', r'ieee', r'acm\.org',
            r'springer', r'sciencedirect', r'nature\.com'
        ],
        'documentation': [
            r'docs', r'documentation', r'api', r'reference', r'guide',
            r'readme', r'wiki', r'man page', r'tutorial'
        ],
        'resource': [
            r'github\.com', r'gitlab', r'bitbucket', r'npm', r'pypi',
            r'crates\.io', r'packagist', r'rubygems'
        ],
        'news': [
            r'news', r'article', r'blog', r'post', r'medium\.com',
            r'dev\.to', r'hackernews', r'reddit', r'twitter'
        ]
    }

    def __init__(self, posts_dir: Path):
        self.posts_dir = posts_dir
        self.links = []
        self.stats = {
            'total_files': 0,
            'total_links': 0,
            'by_type': {},
            'by_domain': {}
        }

    def extract_all(self) -> List[LinkContext]:
        """Extract links from all markdown files"""
        md_files = list(self.posts_dir.glob('*.md'))
        self.stats['total_files'] = len(md_files)

        for md_file in md_files:
            self._extract_from_file(md_file)

        self.stats['total_links'] = len(self.links)
        return self.links

    def _extract_from_file(self, file_path: Path):
        """Extract links from a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
            lines = content.split('\n')

            # Track reference definitions
            ref_defs = {}

            for line_num, line in enumerate(lines, 1):
                # Check for reference definitions first
                ref_match = re.match(self.PATTERNS['reference_def'], line)
                if ref_match:
                    ref_defs[ref_match.group(1)] = ref_match.group(2)

                # Extract inline links
                for match in re.finditer(self.PATTERNS['markdown_link'], line):
                    self._add_link(
                        url=match.group(2),
                        text=match.group(1),
                        file_path=file_path,
                        line_number=line_num,
                        position=match.start(),
                        lines=lines,
                        line_idx=line_num - 1
                    )

                # Extract reference links
                for match in re.finditer(self.PATTERNS['reference_link'], line):
                    ref_key = match.group(2)
                    if ref_key in ref_defs:
                        self._add_link(
                            url=ref_defs[ref_key],
                            text=match.group(1),
                            file_path=file_path,
                            line_number=line_num,
                            position=match.start(),
                            lines=lines,
                            line_idx=line_num - 1
                        )

                # Extract bare URLs
                for match in re.finditer(self.PATTERNS['bare_url'], line):
                    # Skip if this URL is part of a markdown link
                    if not self._is_part_of_markdown_link(line, match.group(0)):
                        self._add_link(
                            url=match.group(0),
                            text='',
                            file_path=file_path,
                            line_number=line_num,
                            position=match.start(),
                            lines=lines,
                            line_idx=line_num - 1
                        )

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def _is_part_of_markdown_link(self, line: str, url: str) -> bool:
        """Check if a URL is already part of a markdown link"""
        # Check if URL is within markdown link syntax
        patterns = [
            f']({url})',
            f']: {url}'
        ]
        return any(pattern in line for pattern in patterns)

    def _add_link(self, url: str, text: str, file_path: Path,
                  line_number: int, position: int, lines: List[str],
                  line_idx: int):
        """Add a link with its context"""
        # Get context (±50 words or ±3 lines)
        context_before = self._get_context(lines, line_idx, -3, 50)
        context_after = self._get_context(lines, line_idx, 3, 50)

        # Classify link type
        link_type = self._classify_link(url, text, context_before + context_after)

        # Create unique hash for the link occurrence
        hash_input = f"{file_path}:{line_number}:{position}:{url}"
        link_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]

        link_context = LinkContext(
            url=url.strip(),
            text=text,
            type=link_type,
            context_before=context_before,
            context_after=context_after,
            file_path=str(file_path),
            line_number=line_number,
            position=position,
            hash=link_hash
        )

        self.links.append(link_context)

        # Update statistics
        self.stats['by_type'][link_type] = self.stats['by_type'].get(link_type, 0) + 1
        domain = self._extract_domain(url)
        if domain:
            self.stats['by_domain'][domain] = self.stats['by_domain'].get(domain, 0) + 1

    def _get_context(self, lines: List[str], center_idx: int,
                     line_offset: int, word_limit: int) -> str:
        """Get context around a line"""
        if line_offset < 0:
            start_idx = max(0, center_idx + line_offset)
            end_idx = center_idx
        else:
            start_idx = center_idx + 1
            end_idx = min(len(lines), center_idx + line_offset + 1)

        context_lines = lines[start_idx:end_idx]
        context_text = ' '.join(context_lines)

        # Limit to word count
        words = context_text.split()
        if len(words) > word_limit:
            if line_offset < 0:
                words = words[-word_limit:]
            else:
                words = words[:word_limit]

        return ' '.join(words)

    def _classify_link(self, url: str, text: str, context: str) -> str:
        """Classify the type of link based on URL and context"""
        url_lower = url.lower()
        context_lower = (text + ' ' + context).lower()

        # Check URL patterns
        for link_type, patterns in self.TYPE_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, url_lower) or re.search(pattern, context_lower):
                    return link_type

        # Check if it's a reference section link
        if re.search(r'^\d+\.\s+', text) or 'reference' in context_lower:
            return 'reference'

        return 'inline'

    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        match = re.match(r'https?://([^/]+)', url)
        if match:
            domain = match.group(1)
            # Remove www prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        return None

    def save_results(self, output_file: Path):
        """Save extracted links to JSON file"""
        data = {
            'extraction_date': datetime.now().isoformat(),
            'stats': self.stats,
            'links': [link.to_dict() for link in self.links]
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Extracted {len(self.links)} links from {self.stats['total_files']} files")
        print(f"📊 By type: {self.stats['by_type']}")
        print(f"💾 Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Extract links from blog posts')
    parser.add_argument('--posts-dir', type=Path,
                       default=Path('src/posts'),
                       help='Directory containing blog posts')
    parser.add_argument('--output', type=Path,
                       default=Path('links.json'),
                       help='Output JSON file')
    parser.add_argument('--citations-only', action='store_true',
                       help='Extract only citation links (research papers, academic sources)')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')

    args = parser.parse_args()

    if not args.posts_dir.exists():
        print(f"❌ Posts directory not found: {args.posts_dir}")
        return 1

    extractor = LinkExtractor(args.posts_dir)
    all_links = extractor.extract_all()

    # Filter for citations only if requested
    if args.citations_only:
        citation_links = [link for link in all_links if link.type == 'citation']
        extractor.links = citation_links
        extractor.stats['total_links'] = len(citation_links)
        print(f"🔬 Filtered to {len(citation_links)} citation links (from {len(all_links)} total)")

    extractor.save_results(args.output)

    return 0

if __name__ == '__main__':
    exit(main())