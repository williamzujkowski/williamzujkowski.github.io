"""Oversized advisory findings must not prevent the broken-citation issue update."""
import pytest
from conftest import load_script

issue = load_script('citation-issue-body.py')
RUN_URL = 'https://github.com/owner/repo/actions/runs/123'


def test_small_report_is_preserved_and_links_to_complete_artifact():
    report = '# Citation report\n\n| Broken | 1 |\n'
    body = issue.build_issue_body(report, RUN_URL, '2026-09-08')
    assert report in body
    assert RUN_URL in body
    assert 'citation-validation-report' in body
    assert 'truncated' not in body


@pytest.mark.parametrize('line', ['DNS failure: ' + 'a' * 350 + '\n', '🔒 Échec DNS: ' + '界' * 200 + '\n'])
def test_full_body_is_bounded_in_utf8_with_notice_and_artifact_link(line):
    report = '# Citation report\n\n| Broken | 1 |\n\n' + line * 550
    body = issue.build_issue_body(report, RUN_URL, '2026-09-08')
    assert len(report.encode('utf-8')) > issue.MAX_BODY_BYTES
    assert len(body.encode('utf-8')) <= issue.MAX_BODY_BYTES
    assert '| Broken | 1 |' in body
    assert '**Report excerpt truncated.**' in body
    assert RUN_URL in body
    assert '\ufffd' not in body


def test_single_oversized_line_is_also_bounded():
    body = issue.build_issue_body('界' * 100_000, RUN_URL, '2026-09-08')
    assert len(body.encode('utf-8')) <= issue.MAX_BODY_BYTES
    assert 'Report excerpt truncated' in body
    assert RUN_URL in body
