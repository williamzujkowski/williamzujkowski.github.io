#!/usr/bin/env -S uv run python3
"""Generate daily link reports with explicit URL and occurrence coverage.

The daily validator checks each unique URL once. Reports join that verdict to
all extracted occurrences without pretending each occurrence was a new request.
Unresolved results remain advisory, and repair suggestions require human review.
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

VERIFIED = {'valid', 'redirect', 'internal', 'unroutable'}
STATUS_LABELS = {
    'valid': 'Valid', 'broken': 'Confirmed broken', 'redirect': 'Redirects',
    'needs_manual': 'Needs manual verification', 'restricted': 'Access-restricted',
    'timeout': 'Timeouts', 'error': 'Errors', 'unchecked': 'Unchecked',
    'internal': 'Internal (checked separately)',
    'unroutable': 'Placeholder (not checked online)',
}
CSV_FIELDS = ['File', 'Line', 'URL', 'Link Text', 'Type', 'Status', 'Issue Type',
              'HTTP Status', 'Relevance Score', 'Suggested Action', 'Repair Available',
              'Suggested URL', 'Repair Confidence', 'Notes']


def review_reason(row: dict) -> str | None:
    """One review policy shared by the summary and complete review queue."""
    status = row['validation'].get('status', 'unknown')
    if status == 'broken':
        return 'Confirmed broken'
    if status not in VERIFIED:
        return 'Unresolved / advisory'
    if row['repair']:
        return 'Suggested repair (review before applying)'
    if row['relevance'].get('suggested_action') == 'review':
        return 'Content relevance review'
    return None


class ReportGenerator:
    """Join validation evidence once, then render the four existing artifacts."""

    def generate_all_reports(self, links_data: dict, validation_data: dict,
                             relevance_data: dict, repairs_data: dict, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)
        links = links_data.get('links', [])
        validation = {r['url']: r for r in validation_data.get('results', [])}
        relevance = {r['url']: r for r in relevance_data.get('results', [])}
        repairs = {r['original_url']: r for r in repairs_data.get('repairs', [])}
        rows = []
        for link in links:
            url = link['url']
            rows.append({'source': link, 'validation': validation.get(url, {
                'url': url, 'status': 'unchecked', 'issue_type': 'not_checked',
                'notes': 'No validation result'}),
                'relevance': relevance.get(url, {}), 'repair': repairs.get(url, {})})
        # A mismatched/partial extraction artifact must not hide checked URLs.
        extracted_urls = {link['url'] for link in links}
        for url, result in validation.items():
            if url not in extracted_urls:
                rows.append({'source': {'url': url}, 'validation': result,
                             'relevance': relevance.get(url, {}), 'repair': repairs.get(url, {})})

        reports = {
            'summary.md': self.summary(links, validation, rows),
            'manual_review.md': self.review_queue(rows),
            'action_plan.md': self.action_plan(repairs),
        }
        for name, content in reports.items():
            (output_dir / name).write_text(content, encoding='utf-8')
        with (output_dir / 'detailed_report.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()
            writer.writerows(self.csv_row(row) for row in rows)
        logger.info(f'Link reports saved to {output_dir}')

    @staticmethod
    def summary(links: list, validation: dict, rows: list) -> str:
        url_counts = Counter(r.get('status', 'unknown') for r in validation.values())
        occurrence_counts = Counter(row['validation'].get('status', 'unknown')
                                    for row in rows[:len(links)])
        review_rows = [row for row in rows if review_reason(row)]
        unchecked = occurrence_counts['unchecked']
        missing_sources = len(rows) - len(links)
        report = [
            '# Link Validation Report', '',
            f"**Generated:** {datetime.now().isoformat(timespec='seconds')}", '',
            f'**Validation results (unique URLs):** {len(validation)}',
            f'**Extracted link occurrences:** {len(links)}',
            f'**Extracted occurrences with a verdict:** {len(links) - unchecked}',
            f'**Unchecked extracted occurrences:** {unchecked}',
            f'**Checked URLs without extracted source metadata:** {missing_sources}',
            f'**Review entries:** {len(review_rows)} '
            '(extracted occurrences plus checked URLs without source metadata)', '',
            '| Result | Checked unique URLs | Extracted occurrences |',
            '| --- | ---: | ---: |',
        ]
        for status in dict.fromkeys([*STATUS_LABELS, *url_counts, *occurrence_counts]):
            label = STATUS_LABELS.get(status, status + ' (unresolved)')
            report.append(f'| {label} | {url_counts[status]} | {occurrence_counts[status]} |')
        report.extend([f'| **Total** | **{len(validation)}** | **{len(links)}** |', ''])
        if any(row['validation'].get('status', 'unknown') not in VERIFIED | {'broken'}
               for row in rows):
            report.extend(['**Verification incomplete.** Unresolved and unchecked results are '
                           'advisory; they do not establish that a link is broken.', ''])
        report.extend(['See `manual_review.md` for every review entry and source location, '
                       '`detailed_report.csv` for all results, and `action_plan.md` for '
                       'supervised follow-up. No repairs are applied by this workflow.', ''])
        return '\n'.join(report)

    @staticmethod
    def review_queue(rows: list) -> str:
        groups = defaultdict(list)
        for row in rows:
            reason = review_reason(row)
            if reason:
                groups[reason].append(row)
        report = ['# Manual Review Queue', '',
                  'Unresolved checks are advisory. Verify repair suggestions before changing a citation.', '']
        for reason in ('Confirmed broken', 'Unresolved / advisory',
                       'Suggested repair (review before applying)', 'Content relevance review'):
            entries = groups[reason]
            report.extend([f'## {reason} ({len(entries)} entries)', ''])
            if not entries:
                report.extend(['None.', ''])
            for row in entries:
                source, verdict, repair = row['source'], row['validation'], row['repair']
                report.extend([
                    f"### {source.get('file_path', 'Source unavailable')}:{source.get('line_number', 'unknown')}",
                    f"- **URL:** `{source['url']}`",
                    f"- **Status:** {verdict.get('status', 'unknown')}",
                    f"- **Issue:** {verdict.get('issue_type') or 'not specified'}",
                ])
                if source.get('text'):
                    report.append(f"- **Link text:** {source['text']}")
                if verdict.get('status_code'):
                    report.append(f"- **HTTP status:** {verdict['status_code']}")
                for key in ('notes', 'error_message'):
                    if verdict.get(key):
                        report.append(f"- **Details:** {verdict[key]}")
                if repair:
                    report.append(f"- **Suggested URL:** `{repair.get('suggested_url', '')}` "
                                  f"(confidence: {repair.get('confidence', 'unknown')}%)")
                if source.get('context_before'):
                    report.append(f"- **Context:** {source['context_before'][:100]}")
                report.append('')
        return '\n'.join(report)

    @staticmethod
    def csv_row(row: dict) -> dict:
        source, validation, relevance, repair = (
            row['source'], row['validation'], row['relevance'], row['repair'])
        return {
            'File': source.get('file_path', 'Source unavailable'),
            'Line': source.get('line_number', 'unknown'), 'URL': source['url'],
            'Link Text': source.get('text', ''), 'Type': source.get('type', ''),
            'Status': validation.get('status', 'unknown'),
            'Issue Type': validation.get('issue_type', ''),
            'HTTP Status': validation.get('status_code', ''),
            'Relevance Score': relevance.get('relevance_score', ''),
            'Suggested Action': relevance.get('suggested_action', ''),
            'Repair Available': 'Yes' if repair else 'No',
            'Suggested URL': repair.get('suggested_url', ''),
            'Repair Confidence': repair.get('confidence', ''),
            'Notes': ' '.join(str(value) for value in (
                validation.get('notes'), validation.get('error_message'), repair.get('notes')) if value),
        }

    @staticmethod
    def action_plan(repairs: dict) -> str:
        return '\n'.join([
            '# Link Review Action Plan', '',
            f'**Suggested repairs (unique URLs):** {len(repairs)}', '',
            'Read `manual_review.md` and `detailed_report.csv` first. Retry unresolved '
            'checks or verify them in a browser before treating them as broken. Confirm '
            'that each suggested replacement supports the original claim; a confidence '
            'score does not establish citation identity.', '',
            'The workflow only reports findings. `repairs.json` contains suggestions '
            'for human review, and `links.json` preserves their source locations. '
            'Make reviewed content edits in a branch.', '',
            'Re-extract and validate after edits, from the repository root:', '',
            '```bash',
            'uv run python scripts/link-validation/link-extractor.py \\',
            '  --posts-dir src/posts --output /tmp/reviewed-links.json',
            'uv run python scripts/link-validation/simple-validator.py \\',
            '  --links /tmp/reviewed-links.json --output /tmp/reviewed-validation.json',
            '```', '',
        ])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--version', action='version', version='%(prog)s 2.0.0')
    parser.add_argument('--links', type=Path, default=Path('links.json'))
    parser.add_argument('--validation', type=Path, default=Path('validation.json'))
    parser.add_argument('--relevance', type=Path, default=Path('relevance.json'))
    parser.add_argument('--repairs', type=Path, default=Path('repairs.json'))
    parser.add_argument('--output-dir', type=Path, default=Path('reports'))
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress progress messages')
    args = parser.parse_args()
    if args.quiet:
        logger.setLevel('ERROR')
    try:
        data = [json.loads(path.read_text(encoding='utf-8'))
                for path in (args.links, args.validation, args.relevance, args.repairs)]
        ReportGenerator().generate_all_reports(*data, args.output_dir)
        return 0
    except FileNotFoundError as error:
        logger.error(f'Input file not found: {error}')
        return 2
    except (ValueError, KeyError, TypeError, OSError) as error:
        logger.error(f'Cannot generate link reports: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
