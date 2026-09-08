#!/usr/bin/env -S uv run python3
"""
SCRIPT: citation-report.py
PURPOSE: Generate citation-specific validation report for GitHub Actions
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.1.0
UPDATED: 2025-11-02T18:00:00-04:00

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
    - Markdown report with broken, restricted and unresolved citation links
    - Grouped by blog post
    - Includes suggested actions

DEPENDENCIES:
    - Python 3.8+
    - json, pathlib (standard library)
    - logging_config for centralized logging

MANIFEST_REGISTRY: scripts/link-validation/citation-report.py
"""

import argparse
import json
import sys
from collections import Counter, defaultdict, deque
from pathlib import Path

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


def generate_citation_report(validation_data: dict, links_data: dict) -> str:
    """Report every checked occurrence, with unresolved findings kept advisory."""
    results = validation_data.get('results', [])
    counts = Counter(result.get('status', 'unknown') for result in results)
    sources = defaultdict(deque)
    for link in links_data.get('links', []):
        sources[link['url']].append(link)

    groups = {name: defaultdict(list) for name in ('broken', 'restricted', 'unresolved')}
    verified = {'valid', 'redirect', 'internal', 'unroutable'}
    for result in results:
        url = result['url']
        source = sources[url].popleft() if sources[url] else {}
        status = result.get('status', 'unknown')
        if status in verified:
            continue
        group = status if status in ('broken', 'restricted') else 'unresolved'
        groups[group][source.get('file_path', 'Source unavailable')].append((source, result))

    # A partial run must expose extracted occurrences that have no verdict too.
    unchecked = 0
    for remaining in sources.values():
        for source in remaining:
            unchecked += 1
            groups['unresolved'][source.get('file_path', 'Source unavailable')].append((
                source, {'url': source['url'], 'status': 'unchecked',
                         'issue_type': 'not_checked', 'error_message': 'No validation result'}))

    report = [
        '# Citation Validation Report', '',
        f"**Checked citation occurrences:** {len(results)}",
        f"**Unique URLs in checked results:** {len({r['url'] for r in results})}",
        f"**Cache hits (occurrences):** {validation_data.get('stats', {}).get('cached', 'not recorded')}",
        f"**Unchecked extracted occurrences:** {unchecked}", '',
        '| Result | Citation occurrences |', '| --- | ---: |',
    ]
    labels = {
        'valid': 'Valid', 'broken': 'Broken', 'restricted': 'Access-restricted',
        'redirect': 'Redirects', 'timeout': 'Timeouts (unresolved)', 'error': 'Errors (unresolved)',
        'internal': 'Internal (checked separately)', 'unroutable': 'Placeholder (not checked online)',
    }
    for status in dict.fromkeys([*labels, *counts]):
        report.append(f"| {labels.get(status, status + ' (unresolved)')} | {counts[status]} |")
    report.extend([f'| **Total** | **{len(results)}** |', ''])

    if groups['unresolved'] or groups['restricted']:
        report.extend(['**Verification incomplete.** Restricted responses and unresolved checks '
                       'are advisory; they do not establish that a citation is broken.', ''])
    if not groups['broken']:
        report.extend(['No confirmed broken citation links found.', ''])

    sections = {
        'broken': ('Broken citations', 'Verify the failure, then find an authoritative replacement '
                   'for dead resources or a valid HTTPS endpoint for TLS failures.'),
        'restricted': ('Access-restricted / unverifiable', 'The checker could not verify these '
                       'responses (including login walls, rate limits and server errors). '
                       'Check in a browser or retry later; these findings are advisory.'),
        'unresolved': ('Unresolved / errors / timeouts', 'Retry these checks and inspect DNS or '
                       'connection errors before changing a citation. Missing results also appear '
                       'here. These findings are advisory, not confirmed broken links.'),
    }
    for group, (heading, advice) in sections.items():
        report.extend([f'## {heading}', '', advice, ''])
        if not groups[group]:
            report.extend(['None.', ''])
            continue
        for post, entries in sorted(groups[group].items(), key=lambda item: (-len(item[1]), item[0])):
            report.extend([f'### {post} ({len(entries)} occurrences)', ''])
            for source, result in entries:
                issue = result.get('issue_type') or result.get('status', 'unknown')
                report.append(f"- Line {source.get('line_number', 'unknown')}: `{result['url']}` ({issue})")
                if source.get('text'):
                    report.append(f"  Link text: {source['text']}")
                if source.get('context_before'):
                    report.append(f"  Context: {source['context_before'][:100]}")
                if result.get('status_code'):
                    report.append(f"  HTTP status: {result['status_code']}")
                if result.get('error_message'):
                    report.append(f"  Error: {result['error_message']}")
            report.append('')
    return '\n'.join(report)


def main() -> int:
    """
    Main entry point for citation report generation.

    Returns:
        Exit code: 0 for success, 1 for broken links or errors
    """
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

    try:
        # Validate input files
        if not args.input.exists():
            logger.error(f"Validation results not found: {args.input}")
            return 1

        if not args.links.exists():
            logger.error(f"Links data not found: {args.links}")
            return 1

        # Load data
        logger.debug(f"Loading validation results from {args.input}")
        with open(args.input, encoding='utf-8') as f:
            validation_data = json.load(f)

        logger.debug(f"Loading link data from {args.links}")
        with open(args.links, encoding='utf-8') as f:
            links_data = json.load(f)

        if args.verbose:
            logger.info(f"Loaded validation results: {len(validation_data.get('results', []))} links")
            logger.info(f"Loaded link data: {len(links_data.get('links', []))} links")

        # Generate report
        logger.debug("Generating citation report")
        report = generate_citation_report(validation_data, links_data)

        # Save report
        logger.debug(f"Writing report to {args.output}")
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)

        logger.info(f"Citation report saved to: {args.output}")

        # Print summary
        broken_count = len([
            r for r in validation_data.get('results', [])
            if r.get('status') == 'broken'
        ])
        restricted_count = len([
            r for r in validation_data.get('results', [])
            if r.get('status') == 'restricted'
        ])

        # Report generation succeeded. The broken-link count is surfaced to the
        # workflow via the `validate` step's output, so a successful report must
        # exit 0 -- returning non-zero here fails the step under `bash -eo
        # pipefail` and (via implicit success()) skips the issue-creation step.
        if broken_count > 0:
            logger.warning(f"Found {broken_count} broken citation links")
        else:
            logger.info("No confirmed broken citation links found; see report for verification gaps")
        if restricted_count > 0:
            logger.info(
                f"{restricted_count} citation links are access-restricted "
                "(403/401/paywall) -- unverifiable by CI, not counted as broken"
            )
        return 0

    except Exception as e:
        logger.error(f"Fatal error generating citation report: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    exit(main())
