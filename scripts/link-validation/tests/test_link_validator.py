"""Regression tests for link-validator.py HTTP status classification.

Locks in that only a genuinely dead resource (404/410) is 'broken'. Everything
else -- bot challenges, rate limits, WAF rejections, paywalls and 5xx -- is
'restricted' (unverifiable, advisory).

This is the validator the citation-validation workflow actually runs, and it had
drifted from simple-validator.py's taxonomy: 400 and 5xx were both classified
broken. Measured false positives from the 2026-08-17 report:

  ai.meta.com/blog/deepfake-detection-challenge-results...  400  page is live
  tinyml.org                                                503  transient
  infonomics-society.org/icitst-2024/...                    500  origin erroring

A 5xx means the origin answered and erred. That is a bad afternoon for the
publisher, not a dead citation, and classifying it as broken feeds live sources
into the auto-repair queue.
"""
import pytest
from conftest import load_script

lv = load_script("link-validator.py")
classify = lv.LinkValidator.classify_http_status


@pytest.mark.parametrize("code,expected", [
    (200, "valid"),
    (404, "broken"),
    (410, "broken"),   # Gone -- the one non-404 that really means dead
    (403, "restricted"),
    (401, "restricted"),
    (202, "restricted"),   # IEEE anti-bot "Accepted" stall
    (418, "restricted"),   # IEEE "I'm a teapot" anti-bot
    (429, "restricted"),   # rate limited
    (999, "restricted"),   # LinkedIn / non-standard anti-bot
    (400, "restricted"),   # ai.meta.com rejects non-browser clients this way
    (405, "restricted"),   # HEAD not allowed
    (451, "restricted"),   # legal block -- the resource exists
    (500, "restricted"),   # origin erroring != citation dead
    (503, "restricted"),   # transient unavailability
])
def test_classify_http_status(code, expected):
    assert classify(code)[0] == expected


def test_antibot_codes_are_never_broken():
    """The #391 false positives: bot challenges must not read as broken."""
    for code in sorted(lv.LinkValidator.ANTIBOT_CODES):
        status, issue_type = classify(code)
        assert status == "restricted"
        assert issue_type == f"http_{code}"


def test_200_variants():
    assert classify(200) == ("valid", None)
    assert classify(200, has_paywall=True) == ("restricted", "paywall")
    assert classify(200, is_redirect=True) == ("redirect", "redirect")


def test_genuinely_dead_stays_broken():
    assert classify(404)[0] == "broken"
    assert classify(410)[0] == "broken"


def test_only_dead_codes_are_broken():
    """The taxonomy in one assertion: 404 and 410, and nothing else."""
    broken = {c for c in range(200, 600) if classify(c)[0] == "broken"}
    assert broken == {404, 410}


def test_matches_simple_validator_taxonomy():
    """The two validators must not disagree about what 'broken' means.

    They drifted once already: the #391 anti-bot fix landed on simple-validator
    while CI ran link-validator.
    """
    sv = load_script("simple-validator.py")
    for code in (200, 202, 301, 400, 403, 404, 410, 429, 451, 500, 503):
        a = classify(code)[0]
        b = sv.SimpleValidator.classify_status(code)[0]
        assert (a == "broken") == (b == "broken"), f"disagree on {code}: {a} vs {b}"


def test_http_binary_and_bounded_html_responses():
    """Real HTTP fixtures retain status/redirects and only inspect a bounded HTML prefix."""
    import asyncio

    import aiohttp
    from aiohttp import web

    async def run():
        binary = b'%PDF-1.7\n\xff\xfe\x80 subscribe to read'

        async def serve(request):
            if request.path == '/redirect':
                raise web.HTTPFound('/pdf')
            if request.path == '/html':
                return web.Response(body=b'<title>Research</title>subscribe to read',
                                    content_type='text/html')
            if request.path == '/large':
                return web.Response(body=b'<title>Public research</title>'
                                    + b' ' * lv.LinkValidator.MAX_HTML_BYTES
                                    + b'subscribe to read', content_type='text/html')
            if request.path == '/invalid-charset':
                return web.Response(body=b'<title>Research\xff</title>',
                                    headers={'Content-Type': 'text/html; charset=unknown-charset'})
            return web.Response(body=binary, content_type='application/pdf',
                                status=int(request.query.get('status', '200')))

        app = web.Application()
        app.router.add_get('/{path}', serve)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '127.0.0.1', 0)
        await site.start()
        base = f'http://127.0.0.1:{site._server.sockets[0].getsockname()[1]}'
        try:
            async with aiohttp.ClientSession() as session:
                validator = lv.LinkValidator(max_retries=1)
                validator.session = session
                for path, status, code in [
                    ('pdf', 'valid', 200), ('redirect', 'redirect', 200),
                    ('pdf?status=404', 'broken', 404), ('pdf?status=503', 'restricted', 503),
                    ('html', 'restricted', 200), ('large', 'valid', 200),
                    ('invalid-charset', 'valid', 200),
                ]:
                    result = await validator._validate_http(f'{base}/{path}', 0)
                    assert (result.status, result.status_code) == (status, code), result
                    assert result.error_message is None
                    if path.startswith('pdf') or path == 'redirect':
                        assert result.content_type == 'application/pdf'
                        assert result.page_title is None
                    if path == 'redirect':
                        assert result.final_url == f'{base}/pdf'
                    if path == 'html':
                        assert result.page_title == 'Research'
                        assert result.issue_type == 'paywall'
                    if path == 'large':
                        assert result.page_title == 'Public research'
        finally:
            await runner.cleanup()

    asyncio.run(run())


def test_occurrence_stats_include_cache_hits_and_skipped_links(monkeypatch, tmp_path):
    import asyncio
    import json

    monkeypatch.setattr(lv, 'PLAYWRIGHT_AVAILABLE', False)
    calls = []

    async def fake_http(url, retry):
        calls.append(url)
        status = url.rsplit('/', 1)[-1]
        return lv.ValidationResult(
            url=url, status=status, status_code=200 if status == 'valid' else None,
            final_url=None, issue_type=None, error_message=None, response_time=0,
            content_type=None, page_title=None, requires_js=False, ssl_valid=True,
            validation_time='2026-09-08', retry_count=1)

    async def run():
        validator = lv.LinkValidator(max_retries=1)
        monkeypatch.setattr(validator, '_validate_http', fake_http)
        urls = ['https://real.test.org/' + status for status in
                ('valid', 'broken', 'restricted', 'redirect', 'timeout', 'error')]
        urls += ['/posts/internal/', 'https://example.com/placeholder']
        results = [await validator.validate_link(url) for url in urls * 2]
        target = tmp_path / 'validation.json'
        await validator.save_results(results, target)
        stats = json.loads(target.read_text())['stats']
        assert stats['total'] == 16
        assert stats['unique_urls'] == 8
        assert stats['cached'] == 8
        categories = ('valid', 'broken', 'restricted', 'redirects', 'timeouts', 'errors',
                      'internal', 'unroutable')
        assert all(stats[key] == 2 for key in categories)
        assert sum(stats[key] for key in categories) == stats['total']
        assert len(calls) == 6

    asyncio.run(run())
