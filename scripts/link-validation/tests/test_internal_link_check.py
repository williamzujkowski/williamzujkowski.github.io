"""Exercise the actual offline CLI against small built sites, without a server."""
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "internal-link-check.py"
SITE = "https://example.test"


def run_site(tmp_path, files, *args):
    dist = tmp_path / "dist"
    dist.mkdir(exist_ok=True)
    for name, content in files.items():
        path = dist / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    return subprocess.run([sys.executable, str(SCRIPT), "--dist", str(dist),
                           "--site-url", SITE, *args], capture_output=True, text=True)


@pytest.mark.parametrize("href", ["'/missing/'", '"/missing/"', "/missing/",
                                  "'../missing/'", "'https://example.test/missing/'",
                                  "'//EXAMPLE.test:443/missing/'"])
def test_missing_paths_in_all_internal_url_forms_fail(tmp_path, href):
    result = run_site(tmp_path, {"nested/index.html": f"<a href={href}>missing</a>"})
    assert result.returncode == 1
    assert "dead path" in result.stdout


def test_valid_relative_same_origin_assets_and_encoded_anchors(tmp_path):
    result = run_site(tmp_path, {
        "index.html": '<a href="nested/">Nested</a>',
        "nested/index.html": """<a href='../target.html?q=a&amp;b=2#caf%C3%A9'>Target</a>
          <a href='https://EXAMPLE.test:443/target.html#old&amp;name'>Alias</a>
          <img src=../image.svg><link href=../style.css rel=stylesheet>
          <a href='#local'>Local</a><h2 id=local>Heading</h2>""",
        "target.html": '<h1 id="café">Target</h1><a name="old&amp;name"></a>',
        "image.svg": '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
        "style.css": 'body { margin: 0; }',
    })
    assert result.returncode == 0, result.stdout + result.stderr


def test_base_url_changes_relative_and_fragment_resolution(tmp_path):
    result = run_site(tmp_path, {
        "index.html": """<base href='/docs/'><base href='/ignored/'>
          <a href='target.html#there'>Target</a><a href='#base-anchor'>Base</a>""",
        "docs/index.html": '<h1 id="base-anchor">Docs</h1>',
        "docs/target.html": '<h1 id=there>Target</h1>',
    })
    assert result.returncode == 0, result.stdout + result.stderr


def test_external_origins_schemes_and_markup_inside_text_are_ignored(tmp_path):
    result = run_site(tmp_path, {"index.html": """
      <a href='https://elsewhere.test/missing'>External</a>
      <a href='//elsewhere.test/missing'>External</a><a href='http://example.test/missing'>Other scheme</a>
      <a href='mailto:a@example.test'>Mail</a><img src='data:image/png;base64,none'>
      <script>const example = '<a href="/not-an-element">';</script>
      <!-- <a href='/not-real'> -->&lt;a href='/text-only'&gt;
      """})
    assert result.returncode == 0, result.stdout + result.stderr


def test_external_base_makes_root_relative_references_external(tmp_path):
    result = run_site(tmp_path, {"index.html": "<base href='https://elsewhere.test/'><a href='/missing'>External</a>"})
    assert result.returncode == 0, result.stdout + result.stderr


def test_missing_anchor_and_search_assets_are_not_exempt(tmp_path):
    result = run_site(tmp_path, {"index.html": "<a href='#missing'>Anchor</a><script src='/pagefind/missing.js'></script>"})
    assert result.returncode == 1
    assert "dead anchor #missing" in result.stdout
    assert "dead path  /pagefind/missing.js" in result.stdout


def test_parent_file_and_symlinks_cannot_satisfy_internal_references(tmp_path):
    (tmp_path / "outside.html").write_text('<h1 id="secret">Outside</h1>')
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "escape.html").symlink_to(tmp_path / "outside.html")
    result = run_site(tmp_path, {"index.html": """<a href='../outside.html'>Parent</a>
      <a href='/%2e%2e/outside.html'>Encoded parent</a><a href='/escape.html#secret'>Symlink</a>"""})
    assert result.returncode == 1
    assert "dead path  ../outside.html" in result.stdout
    assert "dead path  /%2e%2e/outside.html" in result.stdout
    assert "dead path  /escape.html#secret" in result.stdout
    assert "HTML file resolves outside dist" in result.stdout


def test_empty_build_and_invalid_site_fail_closed(tmp_path):
    assert run_site(tmp_path, {}).returncode == 1
    result = run_site(tmp_path, {"index.html": "<h1>Home</h1>"}, "--site-url", "file:///tmp")
    assert result.returncode == 2


def test_broken_fragment_cannot_be_satisfied_by_script_or_comment(tmp_path):
    result = run_site(tmp_path, {"index.html": """<a href='#fake'>Missing</a>
      <script>const fake = 'id="fake"';</script><!-- id="fake" -->"""})
    assert result.returncode == 1
    assert "dead anchor #fake" in result.stdout


@pytest.mark.parametrize("parent", ["%2e%2e", ".%2E", "%2E."])
def test_encoded_dot_segments_cannot_escape_project_ownership_check(tmp_path, parent):
    result = run_site(tmp_path, {
        "index.html": f"<a href='/remarque/{parent}/missing/'>Missing</a>",
    })
    assert result.returncode == 1
    assert "dead path" in result.stdout
    assert "Other deployments (excluded from offline check): 0 references" in result.stdout


def test_encoded_dot_segments_resolve_existing_local_target(tmp_path):
    result = run_site(tmp_path, {
        "index.html": "<a href='/remarque/%2e%2e/about/%2E/#here'>About</a>",
        "about/index.html": "<h1 id=here>About</h1>",
    })
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2 pages, 1 links, 1 anchors" in result.stdout
    assert "Other deployments (excluded from offline check): 0 references" in result.stdout


def test_encoded_slash_does_not_create_project_ownership_boundary(tmp_path):
    result = run_site(tmp_path, {
        "index.html": "<a href='/remarque%2Fmissing/'>Missing</a>",
    })
    assert result.returncode == 1
    assert "Other deployments (excluded from offline check): 0 references" in result.stdout


@pytest.mark.parametrize("element", ["textarea", "title"])
def test_script_literals_in_text_elements_do_not_hide_subsequent_links(tmp_path, element):
    result = run_site(tmp_path, {
        "index.html": f"<{element}><script>literal example</{element}>"
                      "<a href='/missing/'>Real missing link</a>",
    })
    assert result.returncode == 1
    assert "dead path  /missing/" in result.stdout


def test_astro_error_canonical_maps_to_emitted_error_page(tmp_path):
    result = run_site(tmp_path, {"404.html": "<link rel=canonical href='https://example.test/404/'>"})
    assert result.returncode == 0, result.stdout + result.stderr


def test_sibling_deployment_exclusion_has_a_path_segment_boundary(tmp_path):
    result = run_site(tmp_path, {"index.html": """<a href='/remarque/'>Other project</a>
      <a href='/remarque/specimen/'>Other project</a><a href='/remarque-other/'>Missing here</a>"""})
    assert result.returncode == 1
    assert 'Other deployments (excluded from offline check): 2 references' in result.stdout
    assert 'dead path  /remarque-other/' in result.stdout
    assert 'dead path  /remarque/' not in result.stdout


def test_filename_suffix_is_not_mistaken_for_directory_index(tmp_path):
    result = run_site(tmp_path, {"myindex.html": "<h1 id=here>Here</h1><a href='#here'>Here</a>"})
    assert result.returncode == 0, result.stdout + result.stderr


def test_rcdata_and_inert_template_children_do_not_create_document_elements(tmp_path):
    result = run_site(tmp_path, {"index.html": """<title><a href='/not-real'>Title text</a></title>
      <textarea><a href='/not-real' id='fake'>Text</a></textarea>
      <template id='real-template'><h2 id='inert'>Inert</h2><a href='/inert'>Not active</a></template>
      <a href='#real-template'>Template element</a><a href='#fake'>Missing</a><a href='#inert'>Missing</a>"""})
    assert result.returncode == 1
    assert "dead anchor #fake" in result.stdout
    assert "dead anchor #inert" in result.stdout
    assert "dead anchor #real-template" not in result.stdout
    assert "dead path" not in result.stdout


def test_browser_top_fragment_needs_no_explicit_id(tmp_path):
    result = run_site(tmp_path, {"index.html": "<a href='#top'>Top</a><a href='#TOP'>Top</a>"})
    assert result.returncode == 0, result.stdout + result.stderr
