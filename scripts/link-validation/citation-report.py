#!/usr/bin/env -S uv run python3
"""
SCRIPT: citation-report.py
PURPOSE: Generate citation-specific validation report for GitHub Actions
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-10-28T00:00:00-04:00

DESCRIPTION:
    Generates a markdown report specifically for citation link validation,
    designed to be used in GitHub Actions workflows.

LLM_USAGE:
    python scripts/link-validation/citation-report.py --input validation.json --links links.json --output report.md

ARGUMENTS:
    --input: Path to validation results JSON
    --links: Path to extracted links JSON
    --output: Path to output markdown report
    --verbose: Enable verbose output

EXAMPLES:
    # Generate citation report
    python scripts/link-validation/citation-report.py \
        --input citation-validation.json \
        --links citation-links.json \
        --output citation-report.md

OUTPUT:
    - Markdown formatted report with broken citation links
    - Grouped by blog post
    - Includes suggested actions

DEPENDENCIES:
    - Python 3.8+
    - json, pathlib (standard library)

MANIFEST_REGISTRY: scripts/link-validation/citation-report.py
"""

import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List
from datetime import datetime


def generate_citation_report(validation_data: Dict, links_data: Dict) -> str:
    """Generate markdown report for broken citation links"""

    # Map validation results by URL
    validation_map = {r['url']: r for r in validation_data.get('results', [])}

    # Group broken links by blog post
    broken_by_post = defaultdict(list)

    for link in links_data.get('links', []):
        url = link['url']
        validation = validation_map.get(url, {})

        if validation.get('status') == 'broken':
            post_path = Path(link['file_path'])
            broken_by_post[post_path.name].append({
                'url': url,
                'line': link['line_number'],
                'text': link.get('text', 'No link text'),
                'issue_type': validation.get('issue_type', 'unknown'),
                'status_code': validation.get('status_code'),
                'error_message': validation.get('error_message'),
                'context': link.get('context_before', '')[:100]
            })

    # Generate report
    report = []
    report.append("# Broken Citation Links by Blog Post")
    report.append("")

    if not broken_by_post:
        report.append("✅ No broken citation links found!")
        return '\n'.join(report)

    # Sort posts by number of broken links (most broken first)
    sorted_posts = sorted(
        broken_by_post.items(),
        key=lambda x: len(x[1]),
        reverse=True
    )

    for post_name, broken_links in sorted_posts:
        report.append(f"## 📄 {post_name} ({len(broken_links)} broken links)")
        report.append("")

        for i, link_info in enumerate(broken_links, 1):
            report.append(f"### {i}. Line {link_info['line']}")
            report.append("")
            report.append(f"**URL:** `{link_info['url']}`")
            report.append("")
            report.append(f"**Link Text:** {link_info['text']}")
            report.append("")
            report.append(f"**Issue:** {link_info['issue_type']}")

            if link_info['status_code']:
                report.append(f"**HTTP Status:** {link_info['status_code']}")

            if link_info['error_message']:
                report.append(f"**Error:** {link_info['error_message']}")

            report.append("")
            report.append(f"**Context:** `...{link_info['context']}...`")
            report.append("")

            # Suggest actions based on issue type
            issue_type = link_info['issue_type']
            if issue_type == '404':
                report.append("**Suggested Action:** 🔍 Search for updated URL or find alternative source")
            elif issue_type == 'paywall':
                report.append("**Suggested Action:** 🔓 Find open-access alternative or use Wayback Machine")
            elif issue_type == 'timeout':
                report.append("**Suggested Action:** ⏱️ Retry later or find more reliable source")
            elif issue_type == 'ssl_error':
                report.append("**Suggested Action:** 🔒 Check if site has valid HTTPS or find alternative")
            elif issue_type == 'redirect':
                report.append("**Suggested Action:** ↪️ Update to final URL")
            else:
                report.append("**Suggested Action:** 🔧 Investigate and find replacement")

            report.append("")
            report.append("---")
            report.append("")

    # Add summary statistics
    report.append("## 📊 Summary Statistics")
    report.append("")

    total_broken = sum(len(links) for links in broken_by_post.values())
    total_posts = len(broken_by_post)

    report.append(f"- **Total Posts with Broken Links:** {total_posts}")
    report.append(f"- **Total Broken Citation Links:** {total_broken}")
    report.append(f"- **Average Broken Links per Post:** {total_broken / total_posts:.1f}")
    report.append("")

    # Issue type breakdown
    issue_counts = defaultdict(int)
    for links in broken_by_post.values():
        for link in links:
            issue_counts[link['issue_type']] += 1

    report.append("### Issue Types")
    report.append("")
    report.append("| Issue Type | Count | Percentage |")
    report.append("|------------|-------|------------|")

    for issue_type, count in sorted(issue_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_broken) * 100
        report.append(f"| {issue_type} | {count} | {percentage:.1f}% |")

    report.append("")

    # Add repair recommendations
    report.append("## 🔧 Repair Recommendations")
    report.append("")
    report.append("1. **For 404 errors:** Use academic search tools to find updated URLs:")
    report.append("   - [Google Scholar](https://scholar.google.com/)")
    report.append("   - [arXiv.org](https://arxiv.org/)")
    report.append("   - [Zenodo](https://zenodo.org/)")
    report.append("   - [CORE](https://core.ac.uk/)")
    report.append("")
    report.append("2. **For paywalls:** Find open-access alternatives:")
    report.append("   - Use [Unpaywall](https://unpaywall.org/) browser extension")
    report.append("   - Search [PubMed Central](https://www.ncbi.nlm.nih.gov/pmc/)")
    report.append("   - Check author's personal website or ResearchGate")
    report.append("")
    report.append("3. **For timeouts/errors:** Archive the page:")
    report.append("   - Use [Wayback Machine](https://web.archive.org/)")
    report.append("   - Archive current version if site is unstable")
    report.append("")
    report.append("4. **After fixing:** Re-run validation:")
    report.append("   ```bash")
    report.append("   python scripts/link-validation/link-extractor.py --posts-dir src/posts --output links.json --citations-only")
    report.append("   python scripts/link-validation/link-validator.py --input links.json --output validation.json")
    report.append("   ```")
    report.append("")

    return '\n'.join(report)


def main():
    parser = argparse.ArgumentParser(
        description='Generate citation validation report for GitHub Actions'
    )
    parser.add_argument(
        '--input',
        type=Path,
        required=True,
        help='Path to validation results JSON'
    )
    parser.add_argument(
        '--links',
        type=Path,
        required=True,
        help='Path to extracted links JSON'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('citation-report.md'),
        help='Output markdown report path'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )

    args = parser.parse_args()

    # Validate input files
    if not args.input.exists():
        print(f"❌ Validation results not found: {args.input}")
        return 1

    if not args.links.exists():
        print(f"❌ Links data not found: {args.links}")
        return 1

    # Load data
    with open(args.input, 'r', encoding='utf-8') as f:
        validation_data = json.load(f)

    with open(args.links, 'r', encoding='utf-8') as f:
        links_data = json.load(f)

    if args.verbose:
        print(f"📊 Loaded validation results: {len(validation_data.get('results', []))} links")
        print(f"📋 Loaded link data: {len(links_data.get('links', []))} links")

    # Generate report
    report = generate_citation_report(validation_data, links_data)

    # Save report
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✅ Citation report saved to: {args.output}")

    # Print summary
    broken_count = len([
        r for r in validation_data.get('results', [])
        if r.get('status') == 'broken'
    ])

    if broken_count > 0:
        print(f"⚠️  Found {broken_count} broken citation links")
        return 1
    else:
        print("✅ All citation links are valid")
        return 0


if __name__ == '__main__':
    exit(main())
