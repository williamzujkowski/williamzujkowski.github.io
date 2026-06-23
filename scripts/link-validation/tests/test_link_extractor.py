"""Regression tests for link-extractor.py.

Guards the trailing-punctuation bug that produced hundreds of false-positive
404s and broke the link/citation workflows on every run.
"""
import pytest

from conftest import load_script

le = load_script("link-extractor.py")
clean = le.LinkExtractor._clean_trailing_punct


@pytest.mark.parametrize("raw,expected", [
    # Bare URLs in prose pick up trailing punctuation -> must be stripped.
    ("https://arxiv.org/abs/2408.13687))", "https://arxiv.org/abs/2408.13687"),
    ("https://arxiv.org/html/2405.19699v3**", "https://arxiv.org/html/2405.19699v3"),
    ("https://github.com/williamzujkowski/nexus-agents):**",
     "https://github.com/williamzujkowski/nexus-agents"),
    ("https://doi.org/10.1038/s41586-020-2649-2.", "https://doi.org/10.1038/s41586-020-2649-2"),
    ("https://example.com/path,", "https://example.com/path"),
    ("https://example.com/x;", "https://example.com/x"),
    # Balanced parens are legitimate URL characters -> must be preserved.
    ("https://en.wikipedia.org/wiki/Foo_(bar)", "https://en.wikipedia.org/wiki/Foo_(bar)"),
    ("https://en.wikipedia.org/wiki/Foo_(bar))", "https://en.wikipedia.org/wiki/Foo_(bar)"),
    # Clean URLs are left untouched.
    ("https://example.com/clean", "https://example.com/clean"),
    ("https://example.com/", "https://example.com/"),
])
def test_clean_trailing_punct(raw, expected):
    assert clean(raw) == expected


def test_clean_handles_whitespace():
    assert clean("  https://example.com/x  ") == "https://example.com/x"


def test_extraction_skips_markdown_link_double_count(tmp_path):
    """A markdown-link URL must not also be counted as a bare URL."""
    post = tmp_path / "post.md"
    post.write_text(
        "See [the paper](https://arxiv.org/abs/1234.5678) for details.\n"
        "Bare ref: https://example.com/raw and more text.\n",
        encoding="utf-8",
    )
    extractor = le.LinkExtractor(tmp_path)
    links = extractor.extract_all()
    urls = sorted(link.url for link in links)
    assert urls == ["https://arxiv.org/abs/1234.5678", "https://example.com/raw"]


def test_extraction_cleans_bare_url_punctuation(tmp_path):
    post = tmp_path / "post.md"
    post.write_text("Reference: https://arxiv.org/abs/2408.13687). Done.\n", encoding="utf-8")
    extractor = le.LinkExtractor(tmp_path)
    urls = [link.url for link in extractor.extract_all()]
    assert "https://arxiv.org/abs/2408.13687" in urls
    assert all(not u.endswith(")") for u in urls)
