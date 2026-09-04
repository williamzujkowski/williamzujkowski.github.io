#!/usr/bin/env -S uv run python3
"""
SCRIPT: link-extractor.py
PURPOSE: Link Extractor for Blog Posts
CATEGORY: link_validation
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

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
    - scripts/lib/logging_config.py for shared logging

RELATED_SCRIPTS:
    - scripts/lib/logging_config.py: Shared logging
    - [Other related scripts in link_validation category]

MANIFEST_REGISTRY: scripts/link-extractor.py
"""

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

# Setup logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

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
        # Link destinations may contain BALANCED parens -- CommonMark allows
        # it, and real citations use it: the DoD Zero Trust RA lives at
        # .../Library/(U)ZT_RA_v2.0(U)_Sep22.pdf. `[^)]+` stopped at the first
        # `)` and reported the href as ".../Library/(U", a URL that appears
        # nowhere in the corpus, so there was nothing for a human to go and fix.
        # One level of nesting is enough for every real case.
        'markdown_link': r'\[([^\]]+)\]\(((?:[^()\s]|\([^()]*\))+)\)',
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

    def extract_all(self) -> list[LinkContext]:
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
                    # Clean trailing punctuation FIRST so the markdown-link check
                    # matches: the bare_url regex keeps a trailing ')' from
                    # "[text](url)", which would otherwise dodge the check and
                    # double-count the markdown link's URL.
                    bare = self._clean_trailing_punct(match.group(0))
                    if not self._is_part_of_markdown_link(line, bare):
                        self._add_link(
                            url=bare,
                            text='',
                            file_path=file_path,
                            line_number=line_num,
                            position=match.start(),
                            lines=lines,
                            line_idx=line_num - 1
                        )

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")

    def _is_part_of_markdown_link(self, line: str, url: str) -> bool:
        """Check if a URL is already part of a markdown link or reference def.

        Matches on PREFIX, not equality. The bare-URL pattern does not exclude
        `)`, so on a line like

            ... through [`culori`](https://culorijs.org/)'s OKLCH converter ...

        it captures `https://culorijs.org/)'s` -- past the closing paren and on
        into the possessive. An equality test never recognised that as the
        markdown link it came from, and _clean_trailing_punct could not rescue
        it either, because the string ends in `s`, which is not punctuation.

        So a site returning 200 was reported as a broken link every day, and
        the URL in the report appeared nowhere in the corpus: there was nothing
        for a human to go and fix. Two links were affected, not one -- the
        other was a Renovate docs anchor.

        Prefix matching is the correct test, because an over-captured bare hit
        always STARTS with the href it swallowed.
        """
        # Exact forms first -- cheap, and covers the ordinary case.
        if f']({url})' in line or f']: {url}' in line:
            return True
        # Then any markdown href that this hit merely extends.
        for m in re.finditer(self.PATTERNS['markdown_link'], line):
            href = m.group(2).strip()
            if href and url.startswith(href):
                return True
        ref = re.match(self.PATTERNS['reference_def'], line)
        if ref and url.startswith(ref.group(2).strip()):
            return True
        return False

    @staticmethod
    def _clean_trailing_punct(url: str) -> str:
        """Strip trailing prose punctuation that markdown bare-URL parsing absorbs.

        Bare URLs in prose ("see https://arxiv.org/abs/2408.13687).") pick up
        trailing ``)``, ``.``, ``,``, ``*`` etc., which then 404 as false
        positives. Closing brackets are only stripped when unbalanced, so real
        URLs like https://en.wikipedia.org/wiki/Foo_(bar) keep their tail.
        """
        url = url.strip()
        while url and url[-1] in ')].,;:!?\'"*`>':
            if url[-1] == ')' and url.count('(') >= url.count(')'):
                break
            if url[-1] == ']' and url.count('[') >= url.count(']'):
                break
            url = url[:-1]
        return url

    def _add_link(self, url: str, text: str, file_path: Path,
                  line_number: int, position: int, lines: list[str],
                  line_idx: int):
        """Add a link with its context"""
        url = self._clean_trailing_punct(url)
        # Get context (±50 words or ±3 lines)
        context_before = self._get_context(lines, line_idx, -3, 50)
        context_after = self._get_context(lines, line_idx, 3, 50)

        # Classify link type
        link_type = self._classify_link(url, text, context_before + context_after)

        # Create unique hash for the link occurrence
        hash_input = f"{file_path}:{line_number}:{position}:{url}"
        link_hash = hashlib.md5(hash_input.encode()).hexdigest()[:8]

        link_context = LinkContext(
            url=url,
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

    def _get_context(self, lines: list[str], center_idx: int,
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

        logger.info(f"✅ Extracted {len(self.links)} links from {self.stats['total_files']} files")
        logger.info(f"📊 By type: {self.stats['by_type']}")
        logger.info(f"💾 Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Extract links from blog posts',
        epilog='''
Examples:
  %(prog)s --posts-dir src/posts
  %(prog)s --citations-only
  %(prog)s --output links.json --quiet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
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
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    try:
        if not args.posts_dir.exists():
            logger.error(f"❌ Posts directory not found: {args.posts_dir}")
            sys.exit(2)

        extractor = LinkExtractor(args.posts_dir)
        all_links = extractor.extract_all()

        # Filter for citations only if requested
        if args.citations_only:
            citation_links = [link for link in all_links if link.type == 'citation']
            extractor.links = citation_links
            extractor.stats['total_links'] = len(citation_links)
            if not args.quiet:
                logger.info(f"🔬 Filtered to {len(citation_links)} citation links (from {len(all_links)} total)")

        extractor.save_results(args.output)
        sys.exit(0)
    except FileNotFoundError as e:
        logger.error(f"Error: File not found: {e}")
        logger.error(f"Expected: {args.posts_dir}")
        logger.error("Tip: Run from repository root")
        sys.exit(2)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    exit(main())
