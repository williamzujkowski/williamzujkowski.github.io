"""The scheduled alarm uses parsed deployment ownership and confirmed verdicts."""
import json
import os
import re
import shlex
import subprocess
from pathlib import Path

import pytest
from conftest import load_script

summary = load_script('link-health-summary.py')
ROOT = Path(__file__).resolve().parents[3]
SITE = 'https://williamzujkowski.github.io'


def workflow_command():
    workflow = (ROOT / '.github/workflows/link-monitor.yml').read_text()
    step = workflow.split('    - name: Check for Critical Issues\n', 1)[1].split(
        '    - name:', 1)[0]
    return shlex.split(re.search(r'^      run: (.+)$', step, re.MULTILINE).group(1))


def run_summary(tmp_path, results):
    input_file = tmp_path / 'validation.json'
    input_file.write_text(json.dumps({'results': results}))
    output = tmp_path / 'outputs'
    output.write_text('previous_step=retained\n')
    command = workflow_command()
    command[command.index('--input') + 1] = str(input_file)
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                            env={**os.environ, 'GITHUB_OUTPUT': str(output)})
    return result, output.read_text()


def test_six_external_author_urls_reach_existing_notification_threshold(tmp_path):
    urls = [
        'https://github.com/williamzujkowski/missing',
        'https://gist.github.com/williamzujkowski/missing',
        'https://gist.githubusercontent.com/williamzujkowski/missing/raw',
        'https://raw.githubusercontent.com/williamzujkowski/missing/main/file',
        'https://research.test/authors/williamzujkowski',
        'https://research.test/paper?author=williamzujkowski',
    ]
    result, output = run_summary(tmp_path, [{'url': url, 'status': 'broken'} for url in urls])
    assert result.returncode == 0, result.stderr  # advisory even above the threshold
    assert 'internal_broken=0\n' in output
    assert 'external_broken=6\n' in output
    workflow = (ROOT / '.github/workflows/link-monitor.yml').read_text()
    assert "fromJSON(steps.check_critical.outputs.external_broken || '0') > 5" in workflow


@pytest.mark.parametrize(('url', 'owner'), [
    (SITE + '/posts/', 'local'),
    ('https://WILLIAMZUJKOWSKI.github.io:443/posts/', 'local'),
    ('https://williamzujkowski.github.io:444/posts/', 'external'),
    ('https://williamzujkowski.github.io:0/posts/', 'external'),
    ('http://williamzujkowski.github.io/posts/', 'external'),
    ('https://williamzujkowski.github.io.attacker.test/', 'external'),
    ('https://williamzujkowski.github.io@attacker.test/', 'external'),
    ('https://attacker.test@williamzujkowski.github.io/posts/', 'local'),
    ('https://attacker.test/?next=' + SITE, 'external'),
    ('//gist.github.com/williamzujkowski/missing', 'external'),
    ('/posts/?next=https://attacker.test', 'local'),
    ('posts/page/', 'local'),
    ('#anchor', 'local'),
])
def test_origin_uses_host_scheme_and_effective_port(url, owner):
    assert summary.classify_site_url(url)[0] == owner
    counts = summary.summarize([{'url': url, 'status': 'broken'}])
    assert counts['internal_broken'] == (owner == 'local')
    assert counts['external_broken'] == (owner != 'local')


@pytest.mark.parametrize(('path', 'owner', 'normalized'), [
    ('/remarque', 'project', '/remarque'),
    ('/remarque/specimen/', 'project', '/remarque/specimen/'),
    ('/remarque-other/', 'local', '/remarque-other/'),
    ('/remarque%2Fspecimen/', 'local', '/remarque%2Fspecimen/'),
    ('/remarque/%2e%2e/posts/', 'local', '/posts/'),
    ('/remarque/.%2E/posts/', 'local', '/posts/'),
    ('/posts/%2E%2e/remarque/specimen/', 'project', '/remarque/specimen/'),
    ('/remarque/%2F../specimen/', 'project', '/remarque/%2F../specimen/'),
])
def test_shared_project_policy_obeys_normalized_segment_boundaries(path, owner, normalized):
    actual, parts = summary.classify_site_url(path)
    assert (actual, parts.path) == (owner, normalized)
    counts = summary.summarize([{'url': SITE + path, 'status': 'broken'}])
    assert counts['external_broken'] == (owner != 'local')


def test_unresolved_unknown_and_unchecked_results_do_not_raise_alarm():
    statuses = ['valid', 'redirect', 'restricted', 'needs_manual', 'timeout', 'error',
                'internal', 'unroutable', 'unchecked', 'new_status', None]
    results = [{'url': 'https://external.test/source', 'status': status} for status in statuses]
    assert summary.summarize(results) == {
        'broken_count': 0, 'total_count': 11, 'broken_percent': '0.0',
        'internal_broken': 0, 'external_broken': 0,
    }
    assert summary.summarize([]) == {
        'broken_count': 0, 'total_count': 0, 'broken_percent': '0.0',
        'internal_broken': 0, 'external_broken': 0,
    }


def test_cli_preserves_exact_outputs_and_distinguishes_external_percentage(tmp_path):
    result, output = run_summary(tmp_path, [
        {'url': SITE + '/missing/', 'status': 'broken'},
        {'url': '/missing-too/', 'status': 'broken'},
        {'url': SITE + '/remarque/missing/', 'status': 'broken'},
        {'url': 'https://external.test/restricted', 'status': 'needs_manual'},
    ])
    assert result.returncode == 0, result.stderr
    assert output == ('previous_step=retained\nbroken_count=3\ntotal_count=4\n'
                      'broken_percent=75.0\ninternal_broken=2\nexternal_broken=1\n')
    assert 'Overall: 3/4 (75.0%)' in result.stdout
    assert 'External failures: 1 (25.0% of all links)' in result.stdout


@pytest.mark.parametrize('url', ['https://[invalid', '', '   ', None, 42])
def test_malformed_confirmed_failure_is_not_silently_exempted(url):
    counts = summary.summarize([{'url': url, 'status': 'broken'}])
    assert counts['external_broken'] == 1
    assert counts['internal_broken'] == 0
    assert summary.summarize([{'status': 'broken'}])['external_broken'] == 1
