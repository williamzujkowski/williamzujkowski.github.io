#!/usr/bin/env python3
"""
SCRIPT: check-citation-hyperlinks.py
PURPOSE: Check all blog posts for citations that lack hyperlinks
CATEGORY: academic_research
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Check all blog posts for citations that lack hyperlinks. This script is part of the academic research
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/check-citation-hyperlinks.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/check-citation-hyperlinks.py

    # With verbose output
    python scripts/check-citation-hyperlinks.py --verbose

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

MANIFEST_REGISTRY: scripts/check-citation-hyperlinks.py
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class CitationChecker:
    def __init__(self):
        self.posts_dir = Path(".")
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
        all_issues = {}
        
        for post_file in sorted(self.posts_dir.glob("*.md")):
            issues = self.check_file(post_file)
            if issues:
                all_issues[str(post_file)] = issues
        
        return all_issues
    
    def print_report(self, issues: Dict[str, List[Dict]]):
        """Print a formatted report of citation issues."""
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
    checker = CitationChecker()
    issues = checker.scan_all_posts()
    checker.print_report(issues)
    
    # Return exit code based on whether issues were found
    return 0 if not issues else 1

if __name__ == "__main__":
    exit(main())