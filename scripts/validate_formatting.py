#!/usr/bin/env python3
"""
SCRIPT: validate_formatting.py
PURPOSE: Validate markdown formatting and link syntax in blog posts
CATEGORY: validation
CREATED: 2025-09-21
"""

import re
import glob
import json
from pathlib import Path

def check_links(content):
    """Find various link formatting issues"""
    # Find broken links (missing closing paren)
    broken = re.findall(r'\[([^\]]+)\]\([^)]*$', content, re.MULTILINE)

    # Find bare URLs (not in markdown format)
    bare_urls = re.findall(r'(?<![\[\(])(https?://[^\s\[\]\(\)]+)(?![\]\)])', content)

    # Find spaced links
    spaced = re.findall(r'\[([^\]]+)\]\s+\(([^)]+)\)', content)

    # Find links with missing brackets
    missing_bracket = re.findall(r'^\s*\]\(https?://[^\)]+\)', content, re.MULTILINE)

    return {
        'broken': broken,
        'bare_urls': bare_urls,
        'spaced': spaced,
        'missing_bracket': missing_bracket
    }

def check_markdown_issues(content):
    """Check for other markdown formatting issues"""
    issues = []

    # Check for unclosed code blocks
    if content.count('```') % 2 != 0:
        issues.append("Unclosed code block")

    # Check for headers without space after #
    bad_headers = re.findall(r'^#+[^\s#]', content, re.MULTILINE)
    if bad_headers:
        issues.append(f"Headers without space: {len(bad_headers)}")

    # Check for unclosed bold/italic
    if content.count('**') % 2 != 0:
        issues.append("Unclosed bold markers")

    single_asterisks = re.findall(r'(?<!\*)\*(?!\*)', content)
    if len(single_asterisks) % 2 != 0:
        issues.append("Unclosed italic markers")

    return issues

def find_missing_citations(content):
    """Find claims that likely need citations"""
    patterns = [
        r'\d+%\s+of\s+\w+',  # Percentage claims
        r'research\s+shows',  # Research mentions
        r'studies\s+indicate',  # Study mentions
        r'according\s+to\s+(?!my|our|the\s+homelab)',  # According to (but not personal)
        r'proven\s+to',  # Proven claims
        r'statistics\s+show',  # Statistics mentions
    ]

    missing_citations = []
    for pattern in patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        missing_citations.extend(matches)

    return missing_citations

def validate_post(filepath):
    """Validate a single post file"""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]
        else:
            frontmatter = ""
            body = content
    else:
        frontmatter = ""
        body = content

    # Check link issues
    link_issues = check_links(body)

    # Check markdown issues
    markdown_issues = check_markdown_issues(body)

    # Find missing citations
    missing_citations = find_missing_citations(body)

    return {
        'link_issues': link_issues,
        'markdown_issues': markdown_issues,
        'missing_citations': missing_citations
    }

def main():
    """Main validation function"""
    posts_dir = Path('src/posts')
    all_issues = {}
    stats = {
        'total_posts': 0,
        'posts_with_issues': 0,
        'total_broken_links': 0,
        'total_bare_urls': 0,
        'total_missing_citations': 0,
        'posts_needing_citations': 0
    }

    print("# Markdown Formatting and Citation Validation Report")
    print("=" * 60)

    for post_path in sorted(posts_dir.glob('*.md')):
        stats['total_posts'] += 1
        issues = validate_post(post_path)

        has_issues = False

        # Check if post has any issues
        if any(issues['link_issues'].values()) or issues['markdown_issues'] or issues['missing_citations']:
            has_issues = True
            stats['posts_with_issues'] += 1
            all_issues[str(post_path)] = issues

            print(f"\n## {post_path.name}")

            # Report link issues
            if issues['link_issues']['broken']:
                print(f"  ❌ Broken links (missing closing paren): {len(issues['link_issues']['broken'])}")
                stats['total_broken_links'] += len(issues['link_issues']['broken'])

            if issues['link_issues']['bare_urls']:
                print(f"  ⚠️  Bare URLs: {len(issues['link_issues']['bare_urls'])}")
                stats['total_bare_urls'] += len(issues['link_issues']['bare_urls'])

            if issues['link_issues']['spaced']:
                print(f"  ⚠️  Spaced links: {len(issues['link_issues']['spaced'])}")

            if issues['link_issues']['missing_bracket']:
                print(f"  ❌ Missing opening bracket: {len(issues['link_issues']['missing_bracket'])}")

            # Report markdown issues
            for issue in issues['markdown_issues']:
                print(f"  ⚠️  {issue}")

            # Report missing citations
            if issues['missing_citations']:
                print(f"  📚 Potential missing citations: {len(issues['missing_citations'])}")
                stats['total_missing_citations'] += len(issues['missing_citations'])
                stats['posts_needing_citations'] += 1

    # Print summary
    print("\n" + "=" * 60)
    print("## Summary Statistics")
    print(f"Total posts scanned: {stats['total_posts']}")
    print(f"Posts with issues: {stats['posts_with_issues']} ({stats['posts_with_issues']/stats['total_posts']*100:.1f}%)")
    print(f"Total broken links: {stats['total_broken_links']}")
    print(f"Total bare URLs: {stats['total_bare_urls']}")
    print(f"Posts needing citations: {stats['posts_needing_citations']}")
    print(f"Total missing citations: {stats['total_missing_citations']}")

    # Calculate citation coverage
    current_coverage = (stats['total_posts'] - stats['posts_needing_citations']) / stats['total_posts'] * 100
    print(f"\nCurrent citation coverage: {current_coverage:.1f}%")
    print(f"Target citation coverage: 90%+")

    # Save detailed report
    with open('reports/formatting_audit.json', 'w') as f:
        json.dump({
            'stats': stats,
            'issues': all_issues
        }, f, indent=2)

    print("\nDetailed report saved to reports/formatting_audit.json")

if __name__ == "__main__":
    main()