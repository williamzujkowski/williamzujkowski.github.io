"""Reports retain unresolved occurrences and do not conflate them with broken links."""
from conftest import load_script

reporter = load_script('citation-report.py')


def test_error_only_run_exposes_dns_and_timeout_at_every_source():
    results = [
        {'url': 'https://a.test/paper', 'status': 'error', 'issue_type': 'dns_error',
         'error_message': 'Name or service not known'},
        {'url': 'https://a.test/paper', 'status': 'error', 'issue_type': 'dns_error'},
        {'url': 'https://b.test/paper', 'status': 'timeout', 'issue_type': 'timeout'},
    ]
    links = [{'url': result['url'], 'file_path': f'src/posts/post-{i}.md', 'line_number': i + 10}
             for i, result in enumerate(results)]
    report = reporter.generate_citation_report({'results': results, 'stats': {'cached': 1}},
                                               {'links': links})
    assert '**Verification incomplete.**' in report
    assert '**Checked citation occurrences:** 3' in report
    assert '**Unique URLs in checked results:** 2' in report
    assert '| Broken | 0 |' in report
    assert '| Errors (unresolved) | 2 |' in report
    assert '| Timeouts (unresolved) | 1 |' in report
    assert 'Name or service not known' in report
    for i in range(3):
        assert f'src/posts/post-{i}.md' in report
        assert f'Line {i + 10}:' in report


def test_mixed_categories_reconcile_occurrences_and_keep_source_less_errors():
    statuses = ['valid', 'broken', 'restricted', 'redirect', 'timeout', 'error',
                'internal', 'unroutable', 'future_status']
    results = [{'url': f'https://a.test/{status}', 'status': status} for status in statuses]
    report = reporter.generate_citation_report({'results': results}, {'links': []})
    assert '| **Total** | **9** |' in report
    rows = [line for line in report.splitlines() if line.startswith('| ') and line.endswith(' |')]
    assert sum(int(row.split('|')[2]) for row in rows if row.split('|')[2].strip().isdigit()) == 9
    assert 'Source unavailable' in report
    assert 'Line unknown: `https://a.test/error`' in report
    assert 'future_status (unresolved)' in report
    assert 'Internal (checked separately)' in report


def test_missing_results_report_unchecked_occurrences_without_inventing_verdicts():
    report = reporter.generate_citation_report({'results': []}, {'links': [
        {'url': 'https://a.test/paper', 'file_path': 'src/posts/paper.md', 'line_number': 7}]})
    assert '**Checked citation occurrences:** 0' in report
    assert '**Unchecked extracted occurrences:** 1' in report
    assert '**Verification incomplete.**' in report
    assert 'Line 7: `https://a.test/paper` (not_checked)' in report
    assert '| Broken | 0 |' in report
