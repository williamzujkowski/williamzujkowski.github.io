"""Regression fixtures for advisory audit input extraction."""

import importlib.util
from pathlib import Path

import pytest


def load_helper(name):
    path = Path(__file__).resolve().parents[1] / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


batch = load_helper("batch")
pages = load_helper("pages")


@pytest.mark.parametrize("tags", [
    'tags: [security, "homelab"]',
    'tags:\n- security\n- "homelab"',
    "tags:\n  - security\n  # Author note\n  - 'homelab'",
])
def test_equivalent_tags_contribute_to_overlap(tags):
    text = f"---\ntitle: Quiet machines\n{tags}\ndescription: A page\n---\nBody prose."
    fm, body, end = batch.parse_frontmatter(text)
    assert fm["tags"] == ["security", "homelab"]
    assert fm["description"] == "A page"
    assert batch.overlap_signals(body, fm)["security"] == 3
    assert batch.overlap_signals(body, fm)["homelab"] == 3
    assert text.split("\n")[end:] == ["Body prose."]


@pytest.mark.parametrize("text", ["Body prose.", "---\ntitle: Unclosed\nBody prose."])
def test_missing_or_unclosed_frontmatter_keeps_original_input(text):
    assert batch.parse_frontmatter(text) == ({}, text, 0)


def test_multiline_raw_text_excludes_code_and_preserves_prose_locations():
    text = "\n".join([
        "---", 'const imported = "delve";', "---",
        "<p>Before prose.</p>", '<script type="module">',
        'const label = "leverage";', "</script><p>After script.</p>",
        "<style", '  media="screen">', '.delve { content: "robust"; }',
        "</style>", "<p>After styles.</p>",
    ])
    assert pages.strip_astro_to_prose(text) == [
        (4, "Before prose."), (7, "After script."), (12, "After styles."),
    ]


def test_inline_elements_keep_surrounding_words_and_ignore_tag_case():
    text = '<p>Before<STYLE>.delve {}</STYLE>after.</p>\n<scripture>Visible prose.</scripture>'
    assert pages.strip_astro_to_prose(text) == [(1, "Before after."), (2, "Visible prose.")]


def test_normal_prose_and_fenced_code_behavior_is_preserved():
    text = '<h2>Actual heading</h2>\n```js\ndelve leverage\n```\n<p>Actual prose.</p>'
    assert pages.strip_astro_to_prose(text) == [(1, "Actual heading"), (5, "Actual prose.")]


def test_block_tags_strip_unquoted_inline_comments_but_keep_quoted_hashes():
    text = "---\ntags:\n  - security  # classifier\n  - 'hash # in tag'\n---\nBody prose."
    fm, _, _ = batch.parse_frontmatter(text)
    assert fm["tags"] == ["security", "hash # in tag"]


def test_yaml_quoted_scalars_and_flow_tags_preserve_meaning():
    text = '''---
title: 'A developer''s guide'
tags: ["comma, inside", 'hash # inside', 'it''s quoted']
description: "An escaped \\"quote\\""
---
Body prose.'''
    fm, body, end = batch.parse_frontmatter(text)
    assert fm["title"] == "A developer's guide"
    assert fm["tags"] == ["comma, inside", "hash # inside", "it's quoted"]
    assert fm["description"] == 'An escaped "quote"'
    assert body == "\nBody prose."
    assert text.split("\n")[end:] == ["Body prose."]


@pytest.mark.parametrize("newline", ["\n", "\r\n"])
def test_multiline_scalars_keep_original_body_and_offsets(newline):
    text = newline.join([
        "---", "title: >-", "  Wrapped", "  title", "description: |", "  Exact", "  lines",
        "tags: []", "---", "Body prose.", "Second line.",
    ])
    fm, body, end = batch.parse_frontmatter(text)
    assert fm["title"] == "Wrapped title"
    assert fm["description"] == "Exact\nlines\n"
    assert fm["tags"] == []
    assert body == newline + "Body prose." + newline + "Second line."
    assert end == 9
    assert text.split("\n")[end].rstrip("\r") == "Body prose."


@pytest.mark.parametrize("metadata, error", [
    ("title: first\ntitle: second", "duplicate frontmatter key: title"),
    ("nested: {key: first, key: second}", "duplicate frontmatter key: key"),
    ("title: [unclosed", "invalid frontmatter"),
    ("!!python/object/apply:builtins.sum [[1, 2]]", "invalid frontmatter"),
    ("title: !unknown value", "invalid frontmatter"),
    ("- sequence", "must be a mapping"),
    ("scalar", "must be a mapping"),
    ("null", "must be a mapping"),
    ("title: 42", "title must be a string"),
    ("title: null", "title must be a string"),
    ("tags: security", "tags must be a list of strings"),
    ("tags: [security, 3]", "tags must be a list of strings"),
    ("tags: [true]", "tags must be a list of strings"),
    ("title: &loop [*loop]", "title must be a string"),
    ("tags: &loop [*loop]", "tags must be a list of strings"),
    ("value: &value 42\ntitle: *value", "title must be a string"),
    ("42: value", "mapping keys must be strings"),
    ("defaults: &defaults {title: first}\n<<: *defaults", "invalid frontmatter"),
])
def test_invalid_metadata_fails_with_source_context(metadata, error):
    with pytest.raises(ValueError, match=error) as failure:
        batch.parse_frontmatter(f"---\n{metadata}\n---\nBody", source="draft.md")
    assert str(failure.value).startswith("draft.md:")


def test_delimiter_prefix_is_not_a_closing_delimiter():
    text = "---\ntitle: Draft\n---not-a-delimiter\nBody prose."
    assert batch.parse_frontmatter(text) == ({}, text, 0)


@pytest.mark.parametrize("metadata", ["", "# Only a comment\n"])
def test_empty_frontmatter_preserves_body_and_line_offsets(metadata):
    text = f"---\n{metadata}---\nBody"
    fm, body, end = batch.parse_frontmatter(text)
    assert fm == {}
    assert body == "\nBody"
    assert text.split("\n")[end:] == ["Body"]


def test_string_aliases_are_valid_metadata():
    fm, _, _ = batch.parse_frontmatter("---\ntitle: &title Useful title\ntags: [*title]\n---\nBody")
    assert fm["title"] == "Useful title"
    assert fm["tags"] == ["Useful title"]


def test_audit_fails_instead_of_reporting_clean_on_invalid_frontmatter(tmp_path):
    post = tmp_path / "bad-post.md"
    post.write_text("---\ntitle: One\ntitle: Two\n---\nQuiet prose.")
    with pytest.raises(ValueError, match="bad-post.md: invalid frontmatter"):
        batch.audit_post(post, [])
