#!/usr/bin/env python3
"""Rendered-text gate for render-time plugins (margin notes, #margin-citations).

scripts/blog-audit/plaintext_gate.py compares post SOURCE text, so it cannot
see a rehype plugin that drops, duplicates or rewords words at render time.
This gate compares what readers get: the text of <main>, outside the margin
notes (.remarque-sidenote), for each post page, between a build of the
base branch and a build of the PR.

Scope. A PR that edits a post legitimately changes that post's page, and a
PR that edits layouts changes every page. So only post pages whose Markdown
BODY is identical in both trees are compared; frontmatter edits (flipping
`marginNotes`) leave the body alone and are exactly what this guards.

Subcommands:
  applicable   print `rendertext=true|false` (for $GITHUB_OUTPUT). True when the
               PR touches the render-plugin files or a post with
               `marginNotes: true`, or when the diff cannot be computed.
  compare      --base-dist D --head-dist D --base-tree T --head-tree T

Python 3 standard library only (runs on a bare hosted runner).
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

# Files whose change can alter what a post renders.
PLUGIN_INPUTS = (
    "astro-site/src/lib/rehype-",
    "astro-site/src/lib/post-schema.mjs",
    "astro-site/astro.config.mjs",
    "astro-site/pnpm-lock.yaml",
    "scripts/ci/rendered-text-gate.py",
)
POSTS_DIR = "src/posts/"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
FLAG = re.compile(r"^marginNotes:\s*true\s*$", re.M)


class MainText(HTMLParser):
    """Text of <main>, skipping every .remarque-sidenote subtree (aside or span)."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.main = 0
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        if tag == "main":
            self.main += 1
        if self.skip:
            self.skip += 1
        elif "remarque-sidenote" in (dict(attrs).get("class") or "").split():
            self.skip = 1

    def handle_startendtag(self, tag, attrs):
        pass  # <x/> never opens a subtree

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if self.skip:
            self.skip -= 1
        elif tag == "main" and self.main:
            self.main -= 1

    def handle_data(self, data):
        if self.main and not self.skip:
            self.parts.append(data)


def main_text(html: str) -> str:
    p = MainText()
    p.feed(html)
    return re.sub(r"\s+", " ", "".join(p.parts)).strip()


def body_of(markdown: str) -> str:
    m = re.match(r"^---\r?\n.*?\r?\n---\r?\n?(.*)$", markdown, re.S)
    return m.group(1) if m else markdown


def first_difference(a: str, b: str) -> str:
    i = next((k for k, (x, y) in enumerate(zip(a, b, strict=False)) if x != y), min(len(a), len(b)))
    lo = max(0, i - 40)
    return f"base ...{a[lo:i + 60]!r}\n    head ...{b[lo:i + 60]!r}"


def compare(base_dist: Path, head_dist: Path, base_tree: Path, head_tree: Path) -> int:
    compared = skipped_edited = skipped_new = 0
    failures: list[str] = []
    for head_page in sorted((head_dist / "posts").glob("*/index.html")):
        slug = head_page.parent.name
        base_page = base_dist / "posts" / slug / "index.html"
        base_md, head_md = base_tree / POSTS_DIR / f"{slug}.md", head_tree / POSTS_DIR / f"{slug}.md"
        if not base_page.exists() or not base_md.exists():
            skipped_new += 1
            continue
        if not head_md.exists() or body_of(base_md.read_text("utf8")) != body_of(head_md.read_text("utf8")):
            skipped_edited += 1
            continue
        compared += 1
        a, b = main_text(base_page.read_text("utf8")), main_text(head_page.read_text("utf8"))
        if a != b:
            failures.append(f"  {slug}\n    {first_difference(a, b)}")
    print(f"rendered-text gate: {compared} post pages compared "
          f"({skipped_edited} skipped: body edited in this PR, {skipped_new} skipped: new)")
    # Non-vacuity: an empty comparison would pass for the wrong reason.
    if compared == 0:
        print("FAIL: no post page was comparable; the gate would be vacuous", file=sys.stderr)
        return 1
    if failures:
        print(f"FAIL: <main> text outside margin notes differs on {len(failures)} page(s):", file=sys.stderr)
        print("\n".join(failures), file=sys.stderr)
        return 1
    print("OK: <main> text outside margin notes is identical to the base build")
    return 0


def changed_paths(base: str, event: str) -> list[str] | None:
    if not base:
        return None
    comparison = f"{base}...HEAD" if event == "pull_request" else f"{base}..HEAD"
    r = subprocess.run(["git", "diff", "--name-only", "--no-renames", "-z", comparison, "--"],
                       capture_output=True, check=False)
    if r.returncode:
        return None
    return r.stdout.decode("utf-8", errors="surrogateescape").split("\0")[:-1]


def applicable(paths: list[str] | None, root: Path = Path(".")) -> bool:
    if paths is None:
        return True
    for p in paths:
        if any(p.startswith(x) if x.endswith("-") or x.endswith("/") else p == x for x in PLUGIN_INPUTS):
            return True
        f = root / p
        if p.startswith(POSTS_DIR) and p.endswith(".md") and f.exists() and FLAG.search(f.read_text("utf8")):
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("applicable")
    c = sub.add_parser("compare")
    for name in ("base-dist", "head-dist", "base-tree", "head-tree"):
        c.add_argument(f"--{name}", type=Path, required=True)
    args = ap.parse_args()
    if args.cmd == "applicable":
        paths = changed_paths(os.environ.get("BASE", ""), os.environ.get("GITHUB_EVENT_NAME", ""))
        print(f"rendertext={str(applicable(paths)).lower()}")
        return 0
    return compare(args.base_dist, args.head_dist, args.base_tree, args.head_tree)


if __name__ == "__main__":
    sys.exit(main())
