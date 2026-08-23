#!/usr/bin/env python3
"""NDA-compliance and citation-coverage checks over the post corpus.

Advisory by design: neither metric fails the build. AGENTS.md assigns the
*contextual* NDA judgment to the Layer-1 `blog-nda-check` skill; this is the
cheap mechanical pass that runs on every commit.

Advisory does not mean unfalsifiable, though. Two things DO exit non-zero:

  * scanning zero posts -- an empty walk must never read as a clean pass
    (the same defect as issue #492)
  * a corpus path that does not exist

Previously this lived as ~70 lines of Python inside a `python3 -c "..."`
string in compliance-monitor.yml, with shell-escaped quotes. Extracted so it
can be read, tested, and linted (ruff now covers scripts/).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# NDA signal patterns.
#
# These are word-boundaried. The previous list was not, and `at work` matched
# `th{at work}s`, `wh{at work}ed`, `th{at work}flow` -- 35 of its 36 hits in
# the corpus were noise.
#
# A pattern here that matches NOTHING is doing its job. An earlier review
# called six of these "dead" for producing zero hits; for a compliance check,
# zero hits means the corpus is clean, not that the pattern is useless.
# --------------------------------------------------------------------------
SIGNAL_PATTERNS: list[tuple[str, str]] = [
    (r"\bat work\b", "present-tense work reference"),
    (r"\bmy (?:current |present )?employer\b", "employer reference"),
    (r"\bthe (?:company|org(?:anisation|anization)) I work for\b", "employer reference"),
    (r"\bmy team\b", "current-team reference"),
    (r"\bour (?:security )?team\b", "current-team reference"),
    (r"\bour production\b", "current-environment reference"),
    (r"\bwe (?:recently|just) (?:discovered|found|had|saw)\b", "recent-incident reference"),
    (r"\ba (?:recent|current) incident\b", "recent-incident reference"),
    (r"\blast (?:week|month|quarter) at\b", "recent-timeline work reference"),
    # Scale revelations only count in FIRST PERSON. A bare "1,000+ servers" in
    # a generic scaling table, "150 users" on a cited satellite link, or an
    # "RTX 3090 hosts the hypervisor" are not disclosures — an earlier version
    # of this pattern flagged all three.
    (
        r"\b(?:we|i)\s+(?:run|manage|operate|monitor|support|administer)\s+"
        r"(?:about\s+|roughly\s+|around\s+|~)?[\d,]{3,}\+?\s+"
        r"(?:endpoints|servers|users|hosts|seats|devices|systems)\b",
        "scale revelation",
    ),
    (
        r"\b(?:our|my)\s+(?:fleet|estate|environment|network|infrastructure)\s+"
        r"of\s+(?:about\s+|roughly\s+|around\s+|~)?[\d,]{3,}\b",
        "scale revelation",
    ),
]

# Broad technical vocabulary. These are legitimate in this blog's register --
# "in production", "sensitive data", "government guidance" all appear in
# ordinary prose. Reported as an aggregate so they cannot drown the signal
# list; previously they flagged 62 of 92 posts individually.
CONTEXT_WORDS: list[str] = [
    r"\bin production\b",
    r"\bsensitive\b",
    r"\bconfidential\b",
    r"\bclassified\b",
    r"\bgovernment\b",
    r"\bagency\b",
]


def iter_posts(posts_dir: Path):
    yield from sorted(posts_dir.glob("**/*.md"))


def strip_code(text: str) -> str:
    """Drop fenced blocks and inline code before matching prose patterns."""
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return re.sub(r"`[^`\n]*`", "", text)


def check_nda(posts: list[Path]) -> int:
    signal_hits: list[str] = []
    context_counts: dict[str, int] = {}

    for post in posts:
        prose = strip_code(post.read_text())
        for pattern, label in SIGNAL_PATTERNS:
            for m in re.finditer(pattern, prose, re.IGNORECASE):
                line = prose[: m.start()].count("\n") + 1
                snippet = " ".join(prose[max(0, m.start() - 40) : m.end() + 40].split())
                signal_hits.append(f"{post.name}:{line}  [{label}]  …{snippet}…")
        for word in CONTEXT_WORDS:
            n = len(re.findall(word, prose, re.IGNORECASE))
            if n:
                context_counts[word] = context_counts.get(word, 0) + n

    print(f"\nNDA signal patterns: {len(signal_hits)} hit(s) across {len(posts)} posts")
    for hit in signal_hits:
        print(f"  - {hit}")
    if not signal_hits:
        print("  (none)")

    if context_counts:
        print("\nContext vocabulary (advisory aggregate, not per-post):")
        for word, n in sorted(context_counts.items(), key=lambda kv: -kv[1]):
            print(f"  {n:5}  {word}")

    print(
        "\nAdvisory only — this does not fail the build. The contextual gate is "
        "the Layer-1 blog-nda-check skill (see AGENTS.md)."
    )
    return len(signal_hits)


CITATION_LINK = re.compile(r"(?<!\!)\[[^\]]*\]\((https?://[^)]+)\)")
SELF_HOST = "williamzujkowski.github.io"
BADGE_HOSTS = ("shields.io", "img.shields.io", "badgen.net", "badge.fury.io")


def has_real_citation(content: str) -> bool:
    """A citation is an external, non-badge link — not a self-link or an image.

    The previous check counted a link to another post on this same blog, a
    shields.io badge, and a bare `## Sources` heading with nothing under it.
    """
    for m in CITATION_LINK.finditer(content):
        url = m.group(1)
        if SELF_HOST in url:
            continue
        if any(h in url for h in BADGE_HOSTS):
            continue
        return True
    return False


def check_citations(posts: list[Path], target: float) -> float:
    with_citations = [p for p in posts if has_real_citation(p.read_text())]
    coverage = len(with_citations) / len(posts) * 100

    print(f"\nCitation coverage: {coverage:.1f}% ({len(with_citations)}/{len(posts)} posts)")
    missing = [p.name for p in posts if p not in with_citations]
    if missing:
        print(f"  posts with no external citation ({len(missing)}):")
        for name in missing[:20]:
            print(f"    - {name}")
        if len(missing) > 20:
            print(f"    … and {len(missing) - 20} more")

    if coverage < target:
        print(f"  WARNING: below the {target:.0f}% target stated in AGENTS.md")
    print("\nAdvisory only — this does not fail the build.")
    return coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--posts-dir", type=Path, default=Path("src/posts"))
    parser.add_argument(
        "--citation-target",
        type=float,
        default=90.0,
        help="AGENTS.md states 90%%; the old inline check said 70%%.",
    )
    args = parser.parse_args()

    if not args.posts_dir.exists():
        print(f"ERROR: posts directory not found: {args.posts_dir}", file=sys.stderr)
        return 1

    posts = list(iter_posts(args.posts_dir))
    if not posts:
        print(
            f"ERROR: scanned 0 posts under {args.posts_dir}. An empty walk is not a "
            "clean pass — check the path.",
            file=sys.stderr,
        )
        return 1

    check_nda(posts)
    check_citations(posts, args.citation_target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
