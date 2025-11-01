#!/usr/bin/env -S uv run python3
"""
SCRIPT: check-citation-hyperlinks.py
PURPOSE: Check all blog posts for citations that lack hyperlinks
CATEGORY: academic_research
LLM_READY: True
VERSION: 1.1.0
UPDATED: 2025-11-01

DESCRIPTION:
    Check all blog posts for citations that lack hyperlinks. Detects academic citations,
    research claims, and statistics that should be backed by reputable sources.
    This ensures blog content meets the 90%+ citation coverage standard.

LLM_USAGE:
    python scripts/blog-research/check-citation-hyperlinks.py [options]

ARGUMENTS:
    --dir (str): Directory to scan (default: src/posts)
    --format (str): Output format [text|json] (default: text)
    --quiet, -q: Suppress non-essential output
    --version: Show script version
    --help, -h: Show help message with examples

EXAMPLES:
    # Basic usage (scan all posts)
    python scripts/blog-research/check-citation-hyperlinks.py

    # Scan custom directory
    python scripts/blog-research/check-citation-hyperlinks.py --dir src/posts

    # JSON output for automation
    python scripts/blog-research/check-citation-hyperlinks.py --format json

    # Quiet mode
    python scripts/blog-research/check-citation-hyperlinks.py --quiet

OUTPUT:
    - List of posts with missing citation hyperlinks
    - Grouped by citation type (academic, research claim, percentage, etc.)
    - Summary statistics
    - Exit code: 0 (no issues), 1 (issues found), 2 (usage error)

DEPENDENCIES:
    - Python 3.8+
    - No external dependencies (uses stdlib only)

RELATED_SCRIPTS:
    - scripts/blog-research/add-academic-citations.py: Add citations to posts
    - scripts/blog-research/research-validator.py: Comprehensive validation
    - scripts/blog-content/humanization-validator.py: Full post validation

MANIFEST_REGISTRY: scripts/blog-research/check-citation-hyperlinks.py
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Tuple

class CitationChecker:
    def __init__(self, posts_dir: str = "src/posts", quiet: bool = False):
        self.posts_dir = Path(posts_dir)
        self.quiet = quiet
        self.citation_patterns = [
            # Academic style citations without links
            (r'\(([A-Z][a-z]+(?:\s+(?:et\s+al\.|&|and)\s+[A-Z][a-z]+)*),?\s+(\d{4})\)', 'author_year'),
            # IEEE style without links
            (r'\[(\d+)\](?!\()', 'ieee_style'),
            # Research claims without sources
            (r'(?:studies show|research (?:shows|indicates|suggests|proves|demonstrates))\s+[^.]*?(?:\d+(?:\.\d+)?%|that)', 'research_claim'),
            # Specific percentages without citations
            (r'(?<![/\[])\b\d+(?:\.\d+)?%\s+(?:of|improvement|increase|decrease|reduction)', 'percentage'),
            # "According to" without links
            (r'According to\s+(?!.*?https?://)[^,.\n]+', 'according_to'),
        ]
        self.results = []

    def log(self, message: str):
        """Log message unless in quiet mode."""
        if not self.quiet:
            print(message)

    def check_file(self, filepath: Path) -> List[Dict]:
        """Check a single markdown file for citations without hyperlinks."""
        issues = []

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # Skip frontmatter
        in_frontmatter = False
        start_line = 0
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    start_line = i + 1
                    break

        # Check for citations without links
        for i, line in enumerate(lines[start_line:], start=start_line+1):
            # Skip code blocks
            if line.strip().startswith('```'):
                continue

            # Skip lines that already have markdown links
            if '[' in line and '](' in line:
                # Check if the citation is linked
                continue

            for pattern, pattern_type in self.citation_patterns:
                matches = re.finditer(pattern, line, re.IGNORECASE)
                for match in matches:
                    # Check if this is inside a link
                    full_match = match.group(0)
                    start_pos = match.start()

                    # Look for surrounding link syntax
                    before = line[:start_pos]
                    after = line[start_pos + len(full_match):]

                    if not (before.endswith('[') or after.startswith('](http')):
                        issues.append({
                            'line': i,
                            'text': line.strip(),
                            'match': full_match,
                            'type': pattern_type
                        })

        return issues

    def scan_all_posts(self) -> Dict[str, List[Dict]]:
        """Scan all blog posts for citation issues."""
        if not self.posts_dir.exists():
            raise FileNotFoundError(
                f"Posts directory not found: {self.posts_dir}\n"
                f"Expected: {self.posts_dir.absolute()}\n"
                f"Current directory: {Path.cwd()}\n"
                f"Tip: Run from repository root or specify --dir"
            )

        post_files = list(self.posts_dir.glob("*.md"))
        if not post_files:
            self.log(f"No markdown files found in {self.posts_dir}")
            return {}

        all_issues = {}
        self.log(f"Scanning {len(post_files)} posts in {self.posts_dir}...")

        for post_file in sorted(post_files):
            issues = self.check_file(post_file)
            if issues:
                all_issues[str(post_file)] = issues

        return all_issues

    def print_report(self, issues: Dict[str, List[Dict]], format_type: str = 'text'):
        """Print a formatted report of citation issues."""
        if format_type == 'json':
            output = {
                'total_posts': len(list(self.posts_dir.glob('*.md'))),
                'posts_with_issues': len(issues),
                'total_issues': sum(len(v) for v in issues.values()),
                'issues': issues
            }
            print(json.dumps(output, indent=2))
            return

        # Text format
        if not issues:
            print("✅ All citations have hyperlinks!")
            return

        print("=" * 60)
        print("CITATIONS WITHOUT HYPERLINKS")
        print("=" * 60)
        print()

        total_issues = sum(len(v) for v in issues.values())
        print(f"Found {total_issues} citations without hyperlinks in {len(issues)} files\n")

        for filepath, file_issues in issues.items():
            filename = Path(filepath).name
            print(f"\n📄 {filename}")
            print("-" * 40)

            # Group by type
            by_type = {}
            for issue in file_issues:
                issue_type = issue['type']
                if issue_type not in by_type:
                    by_type[issue_type] = []
                by_type[issue_type].append(issue)

            for issue_type, typed_issues in by_type.items():
                print(f"\n  {issue_type.replace('_', ' ').title()} ({len(typed_issues)} issues):")
                for issue in typed_issues[:3]:  # Show first 3
                    print(f"    Line {issue['line']}: {issue['match']}")
                if len(typed_issues) > 3:
                    print(f"    ... and {len(typed_issues) - 3} more")

        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"Total posts checked: {len(list(self.posts_dir.glob('*.md')))}")
        print(f"Posts with issues: {len(issues)}")
        print(f"Total citations without hyperlinks: {total_issues}")

def main():
    parser = argparse.ArgumentParser(
        description='Check blog posts for citations lacking hyperlinks',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scan all posts in default directory
  %(prog)s

  # Scan custom directory
  %(prog)s --dir src/posts

  # JSON output for automation
  %(prog)s --format json

  # Quiet mode (only errors)
  %(prog)s --quiet
        """
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.1.0')
    parser.add_argument('--dir', default='src/posts',
                       help='Directory to scan for markdown files (default: src/posts)')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress non-essential output')

    args = parser.parse_args()

    try:
        checker = CitationChecker(posts_dir=args.dir, quiet=args.quiet)
        issues = checker.scan_all_posts()
        checker.print_report(issues, format_type=args.format)

        # Return exit code based on whether issues were found
        return 0 if not issues else 1

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        if not args.quiet:
            import traceback
            traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
