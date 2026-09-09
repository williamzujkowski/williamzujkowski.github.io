"""Daily reports preserve coverage, review evidence and usable artifact contracts."""
import csv
import json
import subprocess
import sys
from pathlib import Path

from conftest import load_script

reporter = load_script('link-report-generator.py')
SCRIPT = Path(reporter.__file__)


def render(tmp_path, links, results, repairs=None, relevance=None):
    reporter.ReportGenerator().generate_all_reports(
        {'links': links}, {'results': results}, {'results': relevance or []},
        {'repairs': repairs or []}, tmp_path)
    return ((tmp_path / 'summary.md').read_text(),
            (tmp_path / 'manual_review.md').read_text())


def source(url, line=7, path='src/posts/paper.md'):
    return {'url': url, 'file_path': path, 'line_number': line, 'text': 'Research'}


def test_repeated_rate_limited_url_exposes_every_occurrence(tmp_path):
    url = 'https://journal.test/paper'
    links = [source(url, i, f'src/posts/folder-{i}/same-name.md') for i in range(1, 26)]
    summary, queue = render(tmp_path, links, [
        {'url': url, 'status': 'needs_manual', 'issue_type': 'http_429',
         'status_code': 429, 'notes': 'Retry later'}])
    assert '**Validation results (unique URLs):** 1' in summary
    assert '**Extracted link occurrences:** 25' in summary
    assert '**Review entries:** 25 ' in summary
    assert '| Needs manual verification | 1 | 25 |' in summary
    assert '| Confirmed broken | 0 | 0 |' in summary
    assert '**Verification incomplete.**' in summary
    assert 'Unresolved / advisory (25 entries)' in queue
    assert queue.count('**URL:**') == 25
    for link in links:
        assert f"{link['file_path']}:{link['line_number']}" in queue
    with (tmp_path / 'detailed_report.csv').open() as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 25
    assert rows[-1]['File'] == links[-1]['file_path']
    assert rows[-1]['Notes'] == 'Retry later'


def test_mixed_status_counts_reconcile_and_unknowns_remain_advisory(tmp_path):
    statuses = ['valid', 'broken', 'redirect', 'needs_manual', 'restricted',
                'timeout', 'error', 'internal', 'unroutable', 'new_status']
    results = [{'url': f'https://test.invalid/{i}', 'status': status}
               for i, status in enumerate(statuses)]
    results[6]['error_message'] = 'Connection reset'
    summary, queue = render(tmp_path, [source(r['url']) for r in results], results)
    assert '| **Total** | **10** | **10** |' in summary
    count_rows = [row.split('|')[2:4] for row in summary.splitlines()
                  if row.startswith('| ') and row.split('|')[2].strip().isdigit()]
    assert sum(int(row[0]) for row in count_rows) == 10
    assert sum(int(row[1]) for row in count_rows) == 10
    assert '**Review entries:** 6 ' in summary
    assert 'Confirmed broken (1 entries)' in queue
    assert 'Unresolved / advisory (5 entries)' in queue
    assert '**Status:** new_status' in queue
    assert 'Connection reset' in queue
    assert '**Status:** internal' not in queue
    assert '**Status:** unroutable' not in queue


def test_partial_results_and_missing_source_metadata_are_visible(tmp_path):
    present = 'https://test.invalid/present'
    missing = 'https://test.invalid/missing'
    orphan = 'https://test.invalid/orphan'
    summary, queue = render(tmp_path, [source(present), source(missing, 9)], [
        {'url': present, 'status': 'valid'},
        {'url': orphan, 'status': 'error', 'error_message': 'DNS failure'}])
    assert '**Extracted occurrences with a verdict:** 1' in summary
    assert '**Unchecked extracted occurrences:** 1' in summary
    assert '**Checked URLs without extracted source metadata:** 1' in summary
    assert '| Errors | 1 | 0 |' in summary
    assert '| Unchecked | 0 | 1 |' in summary
    assert '**Review entries:** 2 ' in summary
    assert 'src/posts/paper.md:9' in queue
    assert 'Source unavailable:unknown' in queue
    assert 'No validation result' in queue
    assert 'DNS failure' in queue
    with (tmp_path / 'detailed_report.csv').open() as f:
        rows = list(csv.DictReader(f))
    assert {r['URL'] for r in rows} == {present, missing, orphan}
    assert len(rows) == 3


def test_repairs_never_remove_broken_findings_or_authorize_automatic_edits(tmp_path):
    url = 'https://test.invalid/broken'
    summary, queue = render(tmp_path, [source(url)], [{'url': url, 'status': 'broken'}],
                            [{'original_url': url, 'suggested_url': 'https://test.invalid/new',
                              'confidence': 99}])
    assert '**Review entries:** 1 ' in summary
    assert 'Confirmed broken (1 entries)' in queue
    assert 'confidence: 99%' in queue
    plan = (tmp_path / 'action_plan.md').read_text()
    assert 'human review' in plan
    assert '--apply' not in plan
    assert 'content-relevance-checker.py' not in plan
    assert 'simple-validator.py' in plan
    for filename in ('link-extractor.py', 'simple-validator.py'):
        result = subprocess.run([sys.executable, str(SCRIPT.parent / filename), '--help'],
                                capture_output=True, text=True)
        assert result.returncode == 0, result.stderr
    for flag in ('--posts-dir', '--output', '--links'):
        assert flag in plan


def test_valid_results_with_review_suggestions_share_summary_queue_policy(tmp_path):
    urls = ['https://test.invalid/repaired', 'https://test.invalid/relevance']
    summary, queue = render(
        tmp_path, [source(url) for url in urls],
        [{'url': url, 'status': 'valid'} for url in urls],
        [{'original_url': urls[0], 'suggested_url': urls[0] + '/new', 'confidence': 55}],
        [{'url': urls[1], 'suggested_action': 'review'}])
    assert '**Review entries:** 2 ' in summary
    assert 'Suggested repair (review before applying) (1 entries)' in queue
    assert 'Content relevance review (1 entries)' in queue


def test_cli_retains_all_artifact_names_and_writes_empty_csv_header(tmp_path):
    args = []
    for kind, payload in (('links', {'links': []}), ('validation', {'results': []}),
                          ('relevance', {'results': []}), ('repairs', {'repairs': []})):
        path = tmp_path / f'{kind}.json'
        path.write_text(json.dumps(payload))
        args += [f'--{kind}', str(path)]
    output = tmp_path / 'reports'
    result = subprocess.run([sys.executable, str(SCRIPT), *args, '--output-dir', str(output),
                             '--quiet'], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert {path.name for path in output.iterdir()} == {
        'summary.md', 'manual_review.md', 'action_plan.md', 'detailed_report.csv'}
    with (output / 'detailed_report.csv').open() as f:
        reader = csv.DictReader(f)
        assert 'Status' in reader.fieldnames
        assert list(reader) == []
    assert '| **Total** | **0** | **0** |' in (output / 'summary.md').read_text()
