"""Regression fixtures for the bold-density recount and its plain-text gate (#698)."""

import importlib.util
from pathlib import Path


def load_helper(name):
    path = Path(__file__).resolve().parents[1] / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bold_density = load_helper("bold_density")
gate = load_helper("plaintext_gate")

POST = """---
title: "**Not** counted"
date: 2024-01-01
---

**Attack surface:**

- **Password in transit:** logged by the app
- plain item with **emphasis** mid-line

**Why this works**: one sentence.
**Not a lead-in:** this line continues the paragraph above.

**Bold opener** with no colon is emphasis, not a lead-in.

```python
x = "**inside a fence**"
```

~~~
**also fenced:**
~~~

Inline `**code**` and <!-- **a comment** --> and snake__case__name stay out.
"""


def test_fences_inline_code_comments_and_frontmatter_are_excluded():
    m = bold_density.measure(POST)
    # Attack surface, Password in transit, emphasis, Why this works, Not a lead-in,
    # Bold opener.
    assert m["bold"] == 6


def test_lead_ins_need_a_colon_and_a_block_start():
    lines = bold_density.prose_lines(bold_density.split_frontmatter(POST)[1])
    found = [(kind, label) for _, kind, label in bold_density.lead_ins(lines)]
    assert found == [
        ("para", "Attack surface"),
        ("item", "Password in transit"),
        ("para", "Why this works"),
    ]


def test_words_skip_code_urls_and_tags():
    text = "---\ntitle: t\n---\nOne [two](https://x.example/a b) `three` <b>four</b> https://y.example\n"
    assert bold_density.measure(text)["words"] == 3  # One, two, four


def test_unbolding_does_not_change_the_word_count():
    before = "---\ntitle: t\n---\nthe container-to-**host** direction\n"
    assert bold_density.measure(before)["words"] == 3
    assert bold_density.measure(before.replace("**", ""))["words"] == 3


def test_drafts_and_scheduled_posts_are_not_published():
    import datetime
    today = datetime.date(2026, 10, 21)
    assert bold_density.is_published("date: 2026-10-21", today)
    assert not bold_density.is_published("date: 2026-10-22", today)
    assert not bold_density.is_published("date: 2024-01-01\ndraft: true", today)


OLD = """---
title: t
---

**Attack surface:**

- **Term:** a definition with **emphasis**
- Run `make **all**` first

**Output for `axios` module:**

**Why**: it matters.

```sh
echo "**kept**"
```
"""


def test_gate_accepts_markup_only_changes():
    new = OLD.replace("**Attack surface:**", "#### Attack surface")
    new = new.replace("with **emphasis**", "with emphasis").replace("**Why**:", "Why:")
    new = new.replace("**Output for `axios` module:**", "#### Output for `axios` module")
    assert gate.compare(OLD, new) == []


def test_gate_rejects_a_changed_word():
    new = OLD.replace("**Attack surface:**", "#### Attack surface").replace("matters", "counts")
    problems = gate.compare(OLD, new)
    assert len(problems) == 1 and "'matters.' -> 'counts.'" in problems[0]


def test_gate_only_forgives_a_dropped_colon_on_a_heading():
    assert gate.compare(OLD, OLD.replace("**Why**: it", "**Why** it"))
    assert gate.compare(OLD, OLD.replace("**Attack surface:**", "**Attack surface**"))


def test_gate_compares_code_and_frontmatter_verbatim():
    assert gate.compare(OLD, OLD.replace("make **all**", "make all"))
    assert gate.compare(OLD, OLD.replace('"**kept**"', '"kept"'))
    assert gate.compare(OLD, OLD.replace("title: t", "title: u")) == ["frontmatter changed"]


# --- HTML markup is not text (gate v1.1.0) ---

HTML_OLD = """---
title: t
---

## Routing

<div class="flow" role="group" aria-label="Routing path">
  <div class="flow-node">Query</div>
  <div class="flow-branch">
    <div class="flow-leg" data-branch="Yes"><div class="flow-node">Cache</div></div>
    <div class="flow-leg" data-branch="No"><div class="flow-node">Model</div></div>
  </div>
</div>

<span>open("/etc/shadow", O_RDONLY)</span> then a &amp; b.
"""


def test_gate_ignores_wrapping_text_in_inline_tags():
    new = HTML_OLD.replace("<span>open", "<span><code>open").replace(
        "O_RDONLY)</span>", "O_RDONLY)</code></span>"
    )
    assert gate.compare(HTML_OLD, new) == []


def test_gate_allows_splitting_a_flow_with_only_new_tags():
    new = HTML_OLD.replace(
        '  <div class="flow-branch">',
        '</div>\n<div class="flow" role="group" aria-label="Second view">\n  <div class="flow-branch">',
    )
    assert new != HTML_OLD and gate.compare(HTML_OLD, new) == []


def test_gate_rejects_a_changed_word_inside_a_tag():
    assert gate.compare(HTML_OLD, HTML_OLD.replace(">Cache<", ">Memo<"))


def test_gate_rejects_an_added_visible_word():
    assert gate.compare(HTML_OLD, HTML_OLD.replace(">Model<", ">Pick a Model<"))


def test_gate_decodes_entities_and_strips_comments():
    assert gate.compare(HTML_OLD, HTML_OLD.replace("&amp;", "&")) == []
    assert gate.compare(HTML_OLD, HTML_OLD.replace("a &amp; b", "a &#38; b")) == []
    assert gate.compare(HTML_OLD, HTML_OLD + "\n<!-- note\nspanning lines -->\n") == []


def test_gate_handles_multiline_tags_and_quoted_gt():
    new = HTML_OLD.replace(
        '<div class="flow-node">Query</div>',
        '<div\n    class="flow-node"\n    title="a > b">Query</div>',
    )
    assert gate.compare(HTML_OLD, new) == []


def test_gate_still_compares_code_verbatim_and_forgives_heading_colon():
    assert gate.compare("text `<b>x</b>` more\n", "text `x` more\n")
    assert gate.compare("**Lead:** body\n", "#### Lead\n\nbody\n") == []
