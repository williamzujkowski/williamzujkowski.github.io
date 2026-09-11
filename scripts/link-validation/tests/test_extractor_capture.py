"""Regression tests for URL capture boundaries in link-extractor.py.

Both bugs here produced the same useless outcome: a "broken link" report naming
a URL that appears NOWHERE in the corpus, so there was nothing for a human to
go and fix, and the entry never cleared.

  over-capture  `[culori](https://culorijs.org/)'s OKLCH converter`
                -> https://culorijs.org/)'s        (site returns 200)

  under-capture `[DoD ZT RA](https://.../Library/(U)ZT_RA_v2.0(U)_Sep22.pdf)`
                -> https://.../Library/(U          (link renders fine)
"""

import pytest
from conftest import load_script

ex = load_script("link-extractor.py")
LinkExtractor = ex.LinkExtractor


def _hrefs(line):
    import re
    return [m.group(2) for m in re.finditer(LinkExtractor.PATTERNS['markdown_link'], line)]


# --- under-capture: balanced parens in the destination ----------------------
def test_markdown_href_keeps_balanced_parens():
    line = ("5. **[DoD Zero Trust Reference Architecture]"
            "(https://dowcio.war.gov/Portals/0/Documents/Library/(U)ZT_RA_v2.0(U)_Sep22.pdf)**"
            " - DISA and NSA, version 2.0.")
    assert _hrefs(line) == [
        "https://dowcio.war.gov/Portals/0/Documents/Library/(U)ZT_RA_v2.0(U)_Sep22.pdf"]


def test_wikipedia_style_parenthetical_slug_survives():
    line = "see [Foo](https://en.wikipedia.org/wiki/Foo_(bar)) for context"
    assert _hrefs(line) == ["https://en.wikipedia.org/wiki/Foo_(bar)"]


def test_two_links_on_one_line_are_not_merged():
    """The balanced-paren pattern must stay non-greedy across separate links."""
    line = "[a](https://x.test/a) and then [b](https://y.test/b)"
    assert _hrefs(line) == ["https://x.test/a", "https://y.test/b"]


# --- over-capture: bare-URL scan running past the closing paren -------------
@pytest.mark.parametrize("line,overcaptured", [
    ("runs it through [`culori`](https://culorijs.org/)'s OKLCH converter",
     "https://culorijs.org/)'s"),
    ("respects [minimumReleaseAge](https://docs.renovatebot.com/configuration-options/#minimumreleaseage)'s window",
     "https://docs.renovatebot.com/configuration-options/#minimumreleaseage)'s"),
])
def test_overcaptured_bare_url_is_recognised_as_its_markdown_link(tmp_path, line, overcaptured):
    post = tmp_path / "post.md"
    post.write_text(line, encoding="utf-8")
    links = LinkExtractor(tmp_path).extract_all()
    assert [link.url for link in links] == _hrefs(line)
    assert overcaptured not in [link.url for link in links]


def test_a_genuinely_separate_bare_url_is_still_extracted(tmp_path):
    """The guard must not swallow an unrelated bare URL on the same line."""
    post = tmp_path / "post.md"
    post.write_text(
        "see [culori](https://culorijs.org/) and also https://other.test/page",
        encoding="utf-8",
    )
    links = LinkExtractor(tmp_path).extract_all()
    assert [link.url for link in links] == ["https://culorijs.org/", "https://other.test/page"]
