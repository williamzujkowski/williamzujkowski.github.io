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
