"""Regression tests for batch-link-fixer.py URL substitution."""

import pytest

from conftest import load_script

blf = load_script("batch-link-fixer.py")
replace_url = blf.BatchLinkFixer._replace_url


def test_markdown_link_url_replaced_cleanly():
    content = "See [paper](https://old.example/paper) for details."

    fixed, count = replace_url(content, "https://old.example/paper", "https://new.example/paper")

    assert count == 1
    assert fixed == "See [paper](https://new.example/paper) for details."
    assert "paper))" not in fixed


@pytest.mark.parametrize("suffix", [")", "]", "."])
def test_bare_url_followed_by_prose_punctuation(suffix):
    content = f"Reference https://old.example/resource{suffix} next"

    fixed, count = replace_url(content, "https://old.example/resource", "https://new.example/resource")

    assert count == 1
    assert fixed == f"Reference https://new.example/resource{suffix} next"


def test_markdown_url_that_itself_ends_with_paren():
    old_url = "https://en.wikipedia.org/wiki/Mercury_(disambiguation)"
    new_url = "https://example.com/wiki/mercury"
    content = f"See [Mercury]({old_url}) for examples."

    fixed, count = replace_url(content, old_url, new_url)

    assert count == 1
    assert fixed == f"See [Mercury]({new_url}) for examples."
