#!/usr/bin/env python3
"""
SCRIPT: scripts/blog-audit/plaintext_gate.py
PURPOSE: Fail if a markup-only edit to a post changed any of its words.
CATEGORY: blog_audit
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2026-10-21

DESCRIPTION:
    Gate for the bold-density pass (issue #698), whose rule is that the plain
    text of every post stays the same. For each post under src/posts/ that
    differs between REF and the working tree:

    - the frontmatter must be byte-identical;
    - outside fenced and inline code, `**x**` / `__x__` emphasis markers and
      ATX heading markers (`#`..`######` plus a space) are removed, then
      whitespace is collapsed;
    - the resulting word sequences must match exactly, with one allowed
      difference: a word that ended in ':' may lose the colon when it is now
      the last word of a heading (a `**Label:**` lead-in that became a
      heading).

    Code is compared verbatim, markers and all. Added, deleted or renamed
    posts fail: a markup pass does neither.

USAGE:
    uv run python scripts/blog-audit/plaintext_gate.py              # vs origin/main
    uv run python scripts/blog-audit/plaintext_gate.py --ref HEAD~1

EXIT:
    0 every changed post passed (the count is printed, so "0 compared" is
    visible), 1 a text change was found, 2 git or usage error.
"""

import argparse
import difflib
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n.*?^---[ \t]*(?:\r?\n|\Z)", re.DOTALL | re.MULTILINE)
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
HEADING = re.compile(r"^(#{1,6})[ \t]+")
# Same span rules as bold_density.py: no whitespace just inside the markers.
BOLD_STAR = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
BOLD_UNDER = re.compile(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])")


def split_frontmatter(text):
    m = FRONTMATTER.match(text)
    return (text[:m.end()], text[m.end():]) if m else ("", text)


def strip_emphasis(line):
    """Drop bold markers outside inline code; code spans pass through untouched.

    Code is swapped for placeholders rather than split around, so a bold span
    that contains code (`**Output for `x` module:**`) is still one span.
    """
    codes = []

    def park(m):
        codes.append(m.group(0))
        return f"\x00{len(codes) - 1}\x00"

    masked = INLINE_CODE.sub(park, line)
    masked = BOLD_UNDER.sub(r"\1", BOLD_STAR.sub(r"\1", masked))
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], masked)


def normalise(body):
    """Return (words, heading_ends): heading_ends indexes each heading's last word."""
    words, heading_ends, fence = [], set(), None
    for line in body.split("\n"):
        if fence is not None:
            if re.match(r"^\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*$", line):
                fence = None
            words.extend(line.split())
            continue
        m = FENCE_OPEN.match(line)
        if m:
            fence = m.group(1)
            words.extend(line.split())
            continue
        heading = HEADING.match(line)
        if heading:
            line = line[heading.end():]
        tokens = strip_emphasis(line).split()
        words.extend(tokens)
        if heading and tokens:
            heading_ends.add(len(words) - 1)
    return words, heading_ends


def compare(old_text, new_text):
    """Return a list of human-readable problems; empty means markup-only."""
    old_fm, old_body = split_frontmatter(old_text)
    new_fm, new_body = split_frontmatter(new_text)
    problems = []
    if old_fm != new_fm:
        problems.append("frontmatter changed")
    old, _ = normalise(old_body)
    new, new_heads = normalise(new_body)
    matcher = difflib.SequenceMatcher(None, old, new, autojunk=False)
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            continue
        if op == "replace" and i2 - i1 == j2 - j1 and all(
            old[i] == new[j] + ":" and j in new_heads
            for i, j in zip(range(i1, i2), range(j1, j2), strict=True)
        ):
            continue  # colon dropped from a lead-in that became a heading
        context = " ".join(old[max(0, i1 - 4):i1])
        problems.append(f"{op} after '…{context}': {' '.join(old[i1:i2])!r} -> "
                        f"{' '.join(new[j1:j2])!r}")
    return problems


def git(*args):
    return subprocess.run(["git", *args], cwd=REPO, check=True,
                          capture_output=True, text=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[1])
    ap.add_argument("--ref", default="origin/main", help="git ref to compare against")
    args = ap.parse_args()
    try:
        status = git("diff", "--name-status", "--no-renames", args.ref, "--", "src/posts/*.md")
    except subprocess.CalledProcessError as error:
        print(f"git diff failed: {error.stderr.strip()}", file=sys.stderr)
        return 2

    failed, compared = 0, 0
    for row in status.splitlines():
        code, path = row.split("\t", 1)
        if code != "M":
            print(f"FAIL {path}: {code} (a markup pass neither adds nor removes posts)")
            failed += 1
            continue
        compared += 1
        old_text = git("show", f"{args.ref}:{path}")
        new_text = (REPO / path).read_text(encoding="utf-8")
        problems = compare(old_text, new_text)
        if problems:
            failed += 1
            print(f"FAIL {path}")
            for problem in problems[:20]:
                print(f"     {problem}")
        else:
            print(f"ok   {path}")
    print(f"\n{compared} changed post(s) compared against {args.ref}; {failed} failed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
