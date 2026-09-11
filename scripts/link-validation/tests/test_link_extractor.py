"""Regression tests for link-extractor.py.

Guards the trailing-punctuation bug that produced hundreds of false-positive
404s and broke the link/citation workflows on every run.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

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


@pytest.mark.parametrize("punctuation", ["?", "!", ".", ",", ";", ":", "'", "*"])
def test_explicit_destinations_preserve_trailing_punctuation(tmp_path, punctuation):
    url = f"https://example.com/search?q=why{punctuation}"
    post = tmp_path / "post.md"
    post.write_text(
        f"[inline]({url}) and [reference][query].\n"
        f"[query]: {url}\n"
        f"Bare: {url}\n",
        encoding="utf-8",
    )
    links = le.LinkExtractor(tmp_path).extract_all()
    assert [(link.url, link.text) for link in links] == [
        (url, "inline"), (url, "reference"), ("https://example.com/search?q=why", ""),
    ]


@pytest.mark.parametrize("content,expected", [
    (
        "[arXiv](https://arxiv.org/) and https://arxiv.org/abs/2408.13687\n",
        [("https://arxiv.org/", "arXiv", 1, 0),
         ("https://arxiv.org/abs/2408.13687", "", 1, 32)],
    ),
    (
        "[arXiv](https://arxiv.org/) and https://arxiv.org/\n",
        [("https://arxiv.org/", "arXiv", 1, 0), ("https://arxiv.org/", "", 1, 32)],
    ),
    (
        "https://arxiv.org/ [arXiv](https://arxiv.org/) https://arxiv.org/\n",
        [("https://arxiv.org/", "arXiv", 1, 19),
         ("https://arxiv.org/", "", 1, 0), ("https://arxiv.org/", "", 1, 47)],
    ),
    (
        "https://arxiv.org/ https://arxiv.org/\n",
        [("https://arxiv.org/", "", 1, 0), ("https://arxiv.org/", "", 1, 19)],
    ),
    (
        "See [the paper][study].\n[study]: https://arxiv.org/abs/2408.13687\n",
        [("https://arxiv.org/abs/2408.13687", "the paper", 1, 4)],
    ),
    (
        "[study]: https://arxiv.org/abs/2408.13687\nSee [the paper][study].\n",
        [("https://arxiv.org/abs/2408.13687", "the paper", 2, 4)],
    ),
    (
        "[paper][study] [paper][study]\n[study]: https://arxiv.org/abs/2408.13687\n",
        [("https://arxiv.org/abs/2408.13687", "paper", 1, 0),
         ("https://arxiv.org/abs/2408.13687", "paper", 1, 15)],
    ),
    (
        "[query](https://www.google.com/search?q=why?)\n",
        [("https://www.google.com/search?q=why?", "query", 1, 0)],
    ),
    (
        "[query][search]\n[search]: https://www.google.com/search?q=why?\n",
        [("https://www.google.com/search?q=why?", "query", 1, 0)],
    ),
    (
        "[unused]: https://example.com/\nSee [missing][undefined].\n",
        [],
    ),
    (
        "[one](https://example.com/one) [two](https://example.com/two)\n"
        "Bare: https://en.wikipedia.org/wiki/Foo_(bar)).\n",
        [("https://example.com/one", "one", 1, 0),
         ("https://example.com/two", "two", 1, 31),
         ("https://en.wikipedia.org/wiki/Foo_(bar)", "", 2, 6)],
    ),
])
def test_cli_occurrence_inventory(tmp_path, content, expected):
    """Exercise real file input and JSON output, including occurrence metadata."""
    posts = tmp_path / "posts"
    posts.mkdir()
    post = posts / "post.md"
    post.write_text(content, encoding="utf-8")
    output = tmp_path / "links.json"
    script = Path(le.__file__)
    result = subprocess.run(
        [sys.executable, str(script), "--posts-dir", str(posts),
         "--output", str(output), "--quiet"],
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    data = json.loads(output.read_text(encoding="utf-8"))
    assert set(data) == {"extraction_date", "stats", "links"}
    assert data["stats"]["total_files"] == 1
    assert data["stats"]["total_links"] == len(expected)
    assert sum(data["stats"]["by_type"].values()) == len(expected)
    assert sum(data["stats"]["by_domain"].values()) == len(expected)
    assert [(link["url"], link["text"], link["line_number"], link["position"])
            for link in data["links"]] == expected
    assert len({link["hash"] for link in data["links"]}) == len(expected)
    for link in data["links"]:
        assert set(link) == {
            "url", "text", "type", "context_before", "context_after",
            "file_path", "line_number", "position", "hash",
        }
        assert link["file_path"] == str(post)
        hash_input = f"{post}:{link['line_number']}:{link['position']}:{link['url']}"
        assert link["hash"] == hashlib.md5(hash_input.encode()).hexdigest()[:8]
        assert isinstance(link["context_before"], str)
        assert isinstance(link["context_after"], str)
