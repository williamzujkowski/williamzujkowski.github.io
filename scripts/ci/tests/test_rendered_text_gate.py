"""Tests for scripts/ci/rendered-text-gate.py (loaded by path: the name has a hyphen)."""

from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("rtg", ROOT / "scripts/ci/rendered-text-gate.py")
rtg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rtg)

PAGE = '<html><body><nav>skip me</nav><main><p>See <a href="#n">the paper</a>.</p>{extra}</main></body></html>'
NOTE = '<aside class="remarque-sidenote" id="n" role="note">Title (2020)<br>more <em>words</em></aside>'


def test_text_ignores_notes_including_void_elements_inside_them():
    assert rtg.main_text(PAGE.format(extra=NOTE + "<p>after</p>")) == "See the paper.after"


def test_layout_chrome_is_ignored_but_the_post_header_and_body_are_not():
    chrome = (
        '<nav class="post-breadcrumb"><a>Front</a> / <a>Dispatches</a></nav>'
        '<nav class="remarque-breadcrumb"><ol><li><a>Front</a></li><li><span aria-current="page">Title</span></li></ol></nav>'
        '<nav class="remarque-pager post-pager"><a rel="next"><span>Next</span><span>Another post</span></a></nav>'
        '<div class="remarque-endmark"></div>'
        '<footer class="post-footer"><span>Tags:</span><details><summary>Share</summary><a>Reddit</a></details></footer>'
    )
    assert rtg.main_text(PAGE.format(extra=chrome + "<p>after</p>")) == "See the paper.after"
    assert rtg.main_text(PAGE.format(extra="<h1>Title</h1>")) == "See the paper.Title"


def test_text_outside_main_is_ignored_and_whitespace_normalised():
    assert rtg.main_text(PAGE.format(extra="<p>a\n\n  b</p>")) == "See the paper.a b"


def test_inline_span_notes_are_ignored_too():
    inline = '<main><p>See <a>x</a><a class="remarque-sidenote-ref"></a><span class="remarque-sidenote" role="note">N <em>e</em></span>.</p></main>'
    plain = "<main><p>See <a>x</a>.</p></main>"
    assert rtg.main_text(inline) == rtg.main_text(plain)


def test_body_ignores_frontmatter():
    assert rtg.body_of("---\ntitle: a\nmarginNotes: true\n---\nBody\n") == "Body\n"


def make_tree(root: Path, dist: str, slug: str, html: str, md: str) -> None:
    (root / dist / "posts" / slug).mkdir(parents=True)
    (root / dist / "posts" / slug / "index.html").write_text(html)
    (root / "tree" / "src/posts").mkdir(parents=True, exist_ok=True)
    (root / "tree" / "src/posts" / f"{slug}.md").write_text(md)


def run(tmp_path, base_html, head_html, base_md="---\nt: 1\n---\nbody", head_md="---\nt: 1\nmarginNotes: true\n---\nbody"):
    for side, html, md in (("base", base_html, base_md), ("head", head_html, head_md)):
        d = tmp_path / side
        (d / "dist/posts/p").mkdir(parents=True)
        (d / "dist/posts/p/index.html").write_text(html)
        (d / "src/posts").mkdir(parents=True)
        (d / "src/posts/p.md").write_text(md)
    return rtg.compare(tmp_path / "base/dist", tmp_path / "head/dist", tmp_path / "base", tmp_path / "head")


def test_same_text_with_a_note_added_passes(tmp_path):
    assert run(tmp_path, PAGE.format(extra=""), PAGE.format(extra=NOTE)) == 0


def test_changed_word_fails(tmp_path, capsys):
    assert run(tmp_path, PAGE.format(extra="<p>one</p>"), PAGE.format(extra="<p>two</p>")) == 1
    assert "differs on 1 page" in capsys.readouterr().err


def test_edited_body_is_not_compared_and_empty_comparison_fails(tmp_path, capsys):
    assert run(tmp_path, PAGE.format(extra="<p>one</p>"), PAGE.format(extra="<p>two</p>"), head_md="---\n---\nnew body") == 1
    assert "vacuous" in capsys.readouterr().err


def test_applicable_selection(tmp_path):
    (tmp_path / "src/posts").mkdir(parents=True)
    (tmp_path / "src/posts/on.md").write_text("---\nmarginNotes: true\n---\nx")
    (tmp_path / "src/posts/off.md").write_text("---\ntitle: x\n---\nx")
    assert rtg.applicable(["astro-site/src/lib/rehype-source-marginalia.mjs"], tmp_path)
    assert rtg.applicable(["src/posts/on.md"], tmp_path)
    assert not rtg.applicable(["src/posts/off.md", "astro-site/src/pages/index.astro"], tmp_path)
    assert rtg.applicable(None, tmp_path)
