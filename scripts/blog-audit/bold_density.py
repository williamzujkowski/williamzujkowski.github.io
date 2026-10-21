#!/usr/bin/env python3
"""
SCRIPT: scripts/blog-audit/bold_density.py
PURPOSE: Count bold spans and bold lead-ins per published post, worst first.
CATEGORY: blog_audit
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2026-10-21

DESCRIPTION:
    The documented recount behind the bold-density pass (issue #698). The
    "78 of 98 posts exceed 2 bold per 400 words" figure in that issue came
    from a one-off measurement; this is the method written down so the next
    count can be compared with it.

    Per post, over the body only:
    - frontmatter, fenced code (``` and ~~~, any indent), HTML comments and
      inline code are removed before anything is counted;
    - a bold span is `**text**` or `__text__` with no whitespace just inside
      either marker, and `__` not inside a word (so `a ** b` is not bold);
    - words are runs of letters/digits (apostrophes and hyphens join), after
      also dropping HTML tags, link/image targets and bare URLs;
    - a lead-in is a paragraph or list item whose first content is a bold
      span that ends in ':' (`**Note:**`) or is followed by ':' (`**Note**:`).
      Paragraph lead-ins are the heading candidates; list-item lead-ins are
      usually definition lists and are reported separately.

    Only published posts count: `draft: true` and posts dated after today
    are skipped unless --all is given. Stdlib only.

    The 2-per-400 threshold selects posts to inspect. It is not a quota.

USAGE:
    uv run python scripts/blog-audit/bold_density.py            # worst-first table
    uv run python scripts/blog-audit/bold_density.py --top 30
    uv run python scripts/blog-audit/bold_density.py --json
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
POSTS = REPO / "src" / "posts"
THRESHOLD = 2.0  # bold spans per 400 words; selects posts for inspection

FRONTMATTER = re.compile(r"\A---[ \t]*\r?\n(.*?)^---[ \t]*(?:\r?\n|\Z)", re.DOTALL | re.MULTILINE)
FENCE_OPEN = re.compile(r"^\s*(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?!`)(.+?)(?<!`)\1(?!`)")
CODE_MARK = "\x00"  # stands in for inline code so a bold span around it survives

# No whitespace just inside the markers; `__` must not touch a word character
# on the outside, which keeps snake__case__name out (CommonMark agrees).
BOLD_STAR = re.compile(r"\*\*(?=\S)(.+?)(?<=\S)\*\*")
BOLD_UNDER = re.compile(r"(?<![\w])__(?=\S)(.+?)(?<=\S)__(?![\w])")

LIST_ITEM = re.compile(r"^\s*(?:>\s*)*(?:[-*+]|\d+[.)])\s+")
BLOCKQUOTE = re.compile(r"^\s*(?:>\s*)+")
LEAD_IN = re.compile(r"^(?:\*\*(?=\S)(.+?)(?<=\S)\*\*|__(?=\S)(.+?)(?<=\S)__)(:?)")
WORD = re.compile(r"[^\W_]+(?:['’-][^\W_]+)*")


def split_frontmatter(text):
    """Return (frontmatter, body). Missing or unclosed frontmatter -> ('', text)."""
    m = FRONTMATTER.match(text)
    if not m:
        return "", text
    return m.group(1), text[m.end():]


def is_published(frontmatter, today=None):
    if re.search(r"^draft:\s*true\s*$", frontmatter, re.MULTILINE | re.IGNORECASE):
        return False
    m = re.search(r"^date:\s*['\"]?(\d{4}-\d{2}-\d{2})", frontmatter, re.MULTILINE)
    if m:
        today = today or datetime.date.today()
        return datetime.date.fromisoformat(m.group(1)) <= today
    return True


def prose_lines(body):
    """Body lines with fenced code, HTML comments and inline code masked.

    Fenced lines become empty strings so line positions (and the blank-line
    paragraph boundaries around them) are preserved.
    """
    out, fence = [], None
    for line in body.split("\n"):
        m = FENCE_OPEN.match(line)
        if fence is None and m:
            fence = m.group(1)
            out.append("")
            continue
        if fence is not None:
            close = re.match(r"^\s*(" + re.escape(fence[0]) + r"{" + str(len(fence)) + r",})\s*$", line)
            if close:
                fence = None
            out.append("")
            continue
        out.append(line)
    text = "\n".join(out)
    # Comments can span lines; keep their newlines so line numbers hold.
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.DOTALL)
    return [INLINE_CODE.sub(CODE_MARK, line) for line in text.split("\n")]


def bold_spans(line):
    return BOLD_STAR.findall(line) + BOLD_UNDER.findall(line)


def count_words(lines):
    text = "\n".join(lines).replace(CODE_MARK, " ")
    # Markers out first: "container-to-**host**" is one word, not two.
    text = BOLD_UNDER.sub(r"\1", BOLD_STAR.sub(r"\1", text))
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # keep link text, drop target
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    return len(WORD.findall(text))


def lead_ins(lines):
    """Yield (line_no, kind, label) for bold lead-ins; kind is 'para' or 'item'."""
    prev_blank = True
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        # A heading closes its block like a blank line does, and is never a lead-in.
        if not stripped or stripped.startswith("#"):
            prev_blank = True
            continue
        item = LIST_ITEM.match(line)
        if item:
            rest, kind = line[item.end():], "item"
        elif prev_blank:
            rest, kind = BLOCKQUOTE.sub("", line).lstrip(), "para"
        else:
            rest = None
        if rest is not None:
            m = LEAD_IN.match(rest)
            if m:
                label = m.group(1) or m.group(2)
                if label.endswith(":") or m.group(3):
                    yield i, kind, label.rstrip(":")
        prev_blank = False


def measure(text):
    _, body = split_frontmatter(text)
    lines = prose_lines(body)
    bold = sum(len(bold_spans(line)) for line in lines)
    words = count_words(lines)
    leads = list(lead_ins(lines))
    return {
        "words": words,
        "bold": bold,
        "bold_per_400": round(bold * 400 / words, 2) if words else 0.0,
        "lead_ins_para": sum(1 for _, k, _ in leads if k == "para"),
        "lead_ins_item": sum(1 for _, k, _ in leads if k == "item"),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n")[1])
    ap.add_argument("--glob", default="*.md", help="glob under src/posts (default: *.md)")
    ap.add_argument("--top", type=int, default=0, help="show only the N worst posts")
    ap.add_argument("--all", action="store_true", help="include drafts and scheduled posts")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a table")
    args = ap.parse_args()

    rows = []
    for path in sorted(POSTS.glob(args.glob)):
        text = path.read_text(encoding="utf-8")
        frontmatter, _ = split_frontmatter(text)
        if not frontmatter or (not args.all and not is_published(frontmatter)):
            continue
        rows.append({"post": path.name, **measure(text)})
    if not rows:
        print(f"No published posts matched {args.glob}", file=sys.stderr)
        sys.exit(1)
    rows.sort(key=lambda r: (-r["bold_per_400"], r["post"]))
    over = sum(1 for r in rows if r["bold_per_400"] > THRESHOLD)
    shown = rows[: args.top] if args.top else rows

    if args.json:
        print(json.dumps({"threshold": THRESHOLD, "posts": len(rows), "over": over,
                          "rows": shown}, indent=2))
        return

    print(f"{'#':>3} {'POST':<64} {'WORDS':>6} {'BOLD':>5} {'/400':>6} {'LI-P':>5} {'LI-I':>5}")
    print("=" * 99)
    for n, r in enumerate(shown, 1):
        print(f"{n:>3} {r['post'][:-3][:63]:<64} {r['words']:>6} {r['bold']:>5} "
              f"{r['bold_per_400']:>6.2f} {r['lead_ins_para']:>5} {r['lead_ins_item']:>5}")
    print(f"\n{over} of {len(rows)} published posts exceed {THRESHOLD:g} bold per 400 words. "
          "LI-P/LI-I = bold lead-ins on paragraphs / list items.")


if __name__ == "__main__":
    main()
