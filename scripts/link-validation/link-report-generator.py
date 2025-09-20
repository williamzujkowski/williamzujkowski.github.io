#!/usr/bin/env python3
"""
Link Validation Report Generator
Generates comprehensive reports from validation results
"""

import json
import csv
import argparse
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from collections import defaultdict

class ReportGenerator:
    """Generate detailed reports from link validation results"""

    def __init__(self):
        self.stats = defaultdict(int)

    def generate_all_reports(self, links_data: Dict, validation_data: Dict,
                           relevance_data: Dict, repairs_data: Dict,
                           output_dir: Path):
        """Generate all report formats"""
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate different report formats
        self.generate_summary_report(
            links_data, validation_data, relevance_data, repairs_data,
            output_dir / 'summary.md'
        )

        self.generate_detailed_csv(
            links_data, validation_data, relevance_data, repairs_data,
            output_dir / 'detailed_report.csv'
        )

        self.generate_manual_review_queue(
            links_data, validation_data, relevance_data, repairs_data,
            output_dir / 'manual_review.md'
        )

        self.generate_action_plan(
            links_data, validation_data, relevance_data, repairs_data,
            output_dir / 'action_plan.md'
        )

    def generate_summary_report(self, links_data: Dict, validation_data: Dict,
                               relevance_data: Dict, repairs_data: Dict,
                               output_file: Path):
        """Generate markdown summary report"""
        # Calculate statistics
        stats = self._calculate_statistics(
            links_data, validation_data, relevance_data, repairs_data
        )

        report = []
        report.append("# Link Validation Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("\n## Executive Summary\n")
        report.append(f"- **Total Links Checked:** {stats['total_links']}")
        report.append(f"- **Valid Links:** {stats['valid']} ({stats['valid_pct']:.1f}%)")
        report.append(f"- **Broken Links:** {stats['broken']} ({stats['broken_pct']:.1f}%)")
        report.append(f"- **Redirects:** {stats['redirects']}")
        report.append(f"- **Requires Manual Review:** {stats['manual_review']}")
        report.append(f"- **Auto-Fixable:** {stats['auto_fixable']}")

        report.append("\n## Issue Breakdown\n")
        report.append("| Issue Type | Count | Percentage |")
        report.append("|------------|-------|------------|")
        for issue_type, count in stats['by_issue'].items():
            pct = (count / stats['total_links']) * 100 if stats['total_links'] > 0 else 0
            report.append(f"| {issue_type} | {count} | {pct:.1f}% |")

        report.append("\n## Top Affected Domains\n")
        report.append("| Domain | Broken Links | Total Links |")
        report.append("|--------|-------------|-------------|")
        for domain, counts in sorted(stats['by_domain'].items(),
                                    key=lambda x: x[1]['broken'], reverse=True)[:10]:
            report.append(f"| {domain} | {counts['broken']} | {counts['total']} |")

        report.append("\n## Repair Statistics\n")
        report.append(f"- **High Confidence Fixes:** {stats['high_confidence_fixes']}")
        report.append(f"- **Medium Confidence Fixes:** {stats['medium_confidence_fixes']}")
        report.append(f"- **Low Confidence Fixes:** {stats['low_confidence_fixes']}")
        report.append(f"- **No Fix Available:** {stats['no_fix']}")

        report.append("\n## Files with Most Issues\n")
        report.append("| File | Broken Links | Total Links |")
        report.append("|------|-------------|-------------|")
        for file_path, counts in sorted(stats['by_file'].items(),
                                       key=lambda x: x[1]['broken'], reverse=True)[:10]:
            file_name = Path(file_path).name
            report.append(f"| {file_name} | {counts['broken']} | {counts['total']} |")

        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✅ Summary report saved to {output_file}")

    def generate_detailed_csv(self, links_data: Dict, validation_data: Dict,
                             relevance_data: Dict, repairs_data: Dict,
                             output_file: Path):
        """Generate detailed CSV report"""
        # Map results by URL
        validation_map = {r['url']: r for r in validation_data.get('results', [])}
        relevance_map = {r['url']: r for r in relevance_data.get('results', [])}
        repairs_map = {r['original_url']: r for r in repairs_data.get('repairs', [])}

        rows = []
        for link in links_data.get('links', []):
            url = link['url']
            validation = validation_map.get(url, {})
            relevance = relevance_map.get(url, {})
            repair = repairs_map.get(url, {})

            row = {
                'File': Path(link['file_path']).name,
                'Line': link['line_number'],
                'URL': url,
                'Link Text': link.get('text', ''),
                'Type': link.get('type', ''),
                'Status': validation.get('status', 'unknown'),
                'Issue Type': validation.get('issue_type', ''),
                'HTTP Status': validation.get('status_code', ''),
                'Relevance Score': relevance.get('relevance_score', ''),
                'Suggested Action': relevance.get('suggested_action', ''),
                'Repair Available': 'Yes' if repair else 'No',
                'Suggested URL': repair.get('suggested_url', ''),
                'Repair Confidence': repair.get('confidence', ''),
                'Notes': repair.get('notes', '')
            }
            rows.append(row)

        # Write CSV
        if rows:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        print(f"✅ Detailed CSV saved to {output_file}")

    def generate_manual_review_queue(self, links_data: Dict, validation_data: Dict,
                                    relevance_data: Dict, repairs_data: Dict,
                                    output_file: Path):
        """Generate manual review queue"""
        # Map results
        validation_map = {r['url']: r for r in validation_data.get('results', [])}
        relevance_map = {r['url']: r for r in relevance_data.get('results', [])}
        repairs_map = {r['original_url']: r for r in repairs_data.get('repairs', [])}

        # Group links by priority
        priority_groups = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }

        for link in links_data.get('links', []):
            url = link['url']
            validation = validation_map.get(url, {})
            relevance = relevance_map.get(url, {})
            repair = repairs_map.get(url, {})

            # Determine if manual review needed
            needs_review = False
            priority = 'low'

            if validation.get('status') == 'broken' and not repair:
                needs_review = True
                priority = 'critical'
            elif repair and repair.get('confidence', 100) < 70:
                needs_review = True
                priority = 'high'
            elif relevance.get('suggested_action') == 'review':
                needs_review = True
                priority = 'medium'

            if needs_review:
                review_item = {
                    'url': url,
                    'file': Path(link['file_path']).name,
                    'line': link['line_number'],
                    'text': link.get('text', ''),
                    'issue': validation.get('issue_type', 'unknown'),
                    'repair': repair.get('suggested_url', '') if repair else '',
                    'confidence': repair.get('confidence', 0) if repair else 0,
                    'context': link.get('context_before', '')[:100]
                }
                priority_groups[priority].append(review_item)

        # Generate report
        report = []
        report.append("# Manual Review Queue")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        for priority in ['critical', 'high', 'medium', 'low']:
            items = priority_groups[priority]
            if items:
                report.append(f"\n## {priority.capitalize()} Priority ({len(items)} items)\n")

                for item in items[:20]:  # Limit to 20 items per priority
                    report.append(f"### {item['file']}:{item['line']}")
                    report.append(f"- **URL:** {item['url']}")
                    report.append(f"- **Link Text:** {item['text']}")
                    report.append(f"- **Issue:** {item['issue']}")
                    if item['repair']:
                        report.append(f"- **Suggested Fix:** {item['repair']} (confidence: {item['confidence']}%)")
                    report.append(f"- **Context:** ...{item['context']}...")
                    report.append("")

        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✅ Manual review queue saved to {output_file}")

    def generate_action_plan(self, links_data: Dict, validation_data: Dict,
                            relevance_data: Dict, repairs_data: Dict,
                            output_file: Path):
        """Generate action plan for fixes"""
        repairs_map = {r['original_url']: r for r in repairs_data.get('repairs', [])}

        # Group repairs by confidence
        high_confidence = []
        medium_confidence = []
        low_confidence = []

        for repair in repairs_data.get('repairs', []):
            if repair['confidence'] >= 90:
                high_confidence.append(repair)
            elif repair['confidence'] >= 70:
                medium_confidence.append(repair)
            else:
                low_confidence.append(repair)

        # Generate action plan
        report = []
        report.append("# Link Repair Action Plan")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        report.append(f"\n## Phase 1: Automatic Fixes ({len(high_confidence)} links)")
        report.append("\nThese fixes have high confidence and can be applied automatically:\n")
        report.append("```bash")
        report.append("python scripts/link-validation/batch-link-fixer.py \\")
        report.append("    --repairs repairs.json \\")
        report.append("    --confidence-threshold 90 \\")
        report.append("    --apply")
        report.append("```")

        report.append(f"\n## Phase 2: Semi-Automatic Fixes ({len(medium_confidence)} links)")
        report.append("\nThese fixes should be reviewed before applying:\n")
        report.append("```bash")
        report.append("python scripts/link-validation/batch-link-fixer.py \\")
        report.append("    --repairs repairs.json \\")
        report.append("    --confidence-threshold 70 \\")
        report.append("    --dry-run")
        report.append("```")

        report.append(f"\n## Phase 3: Manual Review ({len(low_confidence)} links)")
        report.append("\nThese require manual investigation:")
        report.append("\nReview the `manual_review.md` file for detailed items.")

        report.append("\n## Validation Commands")
        report.append("\nAfter applying fixes, rerun validation:")
        report.append("\n```bash")
        report.append("# Re-extract links")
        report.append("python scripts/link-validation/link-extractor.py")
        report.append("\n# Re-validate")
        report.append("python scripts/link-validation/link-validator.py")
        report.append("\n# Check relevance")
        report.append("python scripts/link-validation/content-relevance-checker.py")
        report.append("```")

        # Write report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))

        print(f"✅ Action plan saved to {output_file}")

    def _calculate_statistics(self, links_data: Dict, validation_data: Dict,
                             relevance_data: Dict, repairs_data: Dict) -> Dict:
        """Calculate comprehensive statistics"""
        stats = {
            'total_links': len(links_data.get('links', [])),
            'valid': 0,
            'broken': 0,
            'redirects': 0,
            'manual_review': 0,
            'auto_fixable': 0,
            'by_issue': defaultdict(int),
            'by_domain': defaultdict(lambda: {'total': 0, 'broken': 0}),
            'by_file': defaultdict(lambda: {'total': 0, 'broken': 0}),
            'high_confidence_fixes': 0,
            'medium_confidence_fixes': 0,
            'low_confidence_fixes': 0,
            'no_fix': 0
        }

        # Map validation results
        validation_map = {r['url']: r for r in validation_data.get('results', [])}
        repairs_map = {r['original_url']: r for r in repairs_data.get('repairs', [])}

        for link in links_data.get('links', []):
            url = link['url']
            validation = validation_map.get(url, {})
            repair = repairs_map.get(url)

            # Count by status
            status = validation.get('status', 'unknown')
            if status == 'valid':
                stats['valid'] += 1
            elif status == 'broken':
                stats['broken'] += 1
            elif status == 'redirect':
                stats['redirects'] += 1

            # Count by issue type
            issue_type = validation.get('issue_type', 'unknown')
            stats['by_issue'][issue_type] += 1

            # Count by domain
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            stats['by_domain'][domain]['total'] += 1
            if status == 'broken':
                stats['by_domain'][domain]['broken'] += 1

            # Count by file
            file_path = link['file_path']
            stats['by_file'][file_path]['total'] += 1
            if status == 'broken':
                stats['by_file'][file_path]['broken'] += 1

            # Count repairs
            if repair:
                confidence = repair.get('confidence', 0)
                if confidence >= 90:
                    stats['high_confidence_fixes'] += 1
                    stats['auto_fixable'] += 1
                elif confidence >= 70:
                    stats['medium_confidence_fixes'] += 1
                else:
                    stats['low_confidence_fixes'] += 1
                    stats['manual_review'] += 1
            elif status == 'broken':
                stats['no_fix'] += 1
                stats['manual_review'] += 1

        # Calculate percentages
        if stats['total_links'] > 0:
            stats['valid_pct'] = (stats['valid'] / stats['total_links']) * 100
            stats['broken_pct'] = (stats['broken'] / stats['total_links']) * 100
        else:
            stats['valid_pct'] = 0
            stats['broken_pct'] = 0

        return stats

def main():
    parser = argparse.ArgumentParser(description='Generate link validation reports')
    parser.add_argument('--links', type=Path, default=Path('links.json'))
    parser.add_argument('--validation', type=Path, default=Path('validation.json'))
    parser.add_argument('--relevance', type=Path, default=Path('relevance.json'))
    parser.add_argument('--repairs', type=Path, default=Path('repairs.json'))
    parser.add_argument('--output-dir', type=Path, default=Path('reports'))

    args = parser.parse_args()

    # Load all data
    with open(args.links, 'r') as f:
        links_data = json.load(f)

    with open(args.validation, 'r') as f:
        validation_data = json.load(f)

    with open(args.relevance, 'r') as f:
        relevance_data = json.load(f)

    with open(args.repairs, 'r') as f:
        repairs_data = json.load(f)

    # Generate reports
    generator = ReportGenerator()
    generator.generate_all_reports(
        links_data, validation_data, relevance_data, repairs_data,
        args.output_dir
    )

    return 0

if __name__ == '__main__':
    exit(main())