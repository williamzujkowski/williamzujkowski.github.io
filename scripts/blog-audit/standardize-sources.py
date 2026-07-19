#!/usr/bin/env python3
"""Normalize trailing source/reference headings in blog posts."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


POST_DIR = Path("src/posts")
STANDARD_HEADING = "## Sources"

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
LINK_LIST_RE = re.compile(r"^\s{0,3}(?:[-*+]|\d+[.)])\s+.*\[[^\]]+\]\([^)]+\)")
SOURCE_RE = re.compile(r"\b(sources|references?|referenced)\b", re.IGNORECASE)
RESOURCE_RE = re.compile(r"\bresources?\b", re.IGNORECASE)
FURTHER_READING_RE = re.compile(r"\bfurther\s+reading\b", re.IGNORECASE)
RESOURCE_CONTEXT_RE = re.compile(
    r"\b(academic|industry|learning|research|security|technical|further\s+reading)\b",
    re.IGNORECASE,
)
RESOURCE_EXCLUDE_RE = re.compile(
    r"\b(getting\s+started|resource\s+(constraints?|usage|requirements?))\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Heading:
    index: int
    level: int
    text: str
    candidate: bool


def markdown_headings(lines: list[str]) -> list[Heading]:
    headings: list[Heading] = []
    in_fence = False

    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith(("```", "~~~")):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        match = HEADING_RE.match(line)
        if not match:
            continue

        text = match.group(2).strip()
        headings.append(
            Heading(
                index=index,
                level=len(match.group(1)),
                text=text,
                candidate=is_source_candidate(lines, index, text),
            )
        )

    return headings


def has_link_list_nearby(lines: list[str], index: int, distance: int = 3) -> bool:
    return any(LINK_LIST_RE.search(line) for line in lines[index + 1 : index + distance + 1])


def is_source_candidate(lines: list[str], index: int, text: str) -> bool:
    if RESOURCE_EXCLUDE_RE.search(text):
        return False

    in_trailing_third = index >= int(len(lines) * 0.70)
    has_nearby_link_list = has_link_list_nearby(lines, index)

    if SOURCE_RE.search(text):
        return in_trailing_third or has_link_list_nearby(lines, index, distance=8)

    if RESOURCE_RE.search(text):
        return (in_trailing_third and RESOURCE_CONTEXT_RE.search(text) is not None) or has_nearby_link_list

    return False


def target_heading(headings: list[Heading]) -> Heading | None:
    candidates = [heading for heading in headings if heading.candidate]
    if not candidates:
        return None

    last = candidates[-1]
    for heading in reversed([h for h in headings if h.index < last.index]):
        if heading.level < last.level and (heading.candidate or FURTHER_READING_RE.search(heading.text)):
            return heading
        if heading.level < last.level:
            break

    return last


def section_end(lines: list[str], headings: list[Heading], target: Heading) -> int:
    for heading in headings:
        if heading.index > target.index and heading.level <= target.level:
            return heading.index
    return len(lines)


def normalize_post(path: Path, dry_run: bool = False) -> tuple[bool, str | None]:
    original = path.read_text()
    lines = original.splitlines(keepends=True)
    bare_lines = [line.rstrip("\n") for line in lines]
    headings = markdown_headings(bare_lines)
    target = target_heading(headings)

    if target is None or bare_lines[target.index] == STANDARD_HEADING:
        return False, None

    end = section_end(bare_lines, headings, target)
    delta = 2 - target.level
    old_heading = bare_lines[target.index].strip()
    lines[target.index] = STANDARD_HEADING + line_ending(lines[target.index])

    if delta:
        for heading in headings:
            if target.index < heading.index < end and heading.level > target.level:
                new_level = min(6, max(3, heading.level + delta))
                text = HEADING_RE.match(bare_lines[heading.index]).group(2).strip()  # type: ignore[union-attr]
                lines[heading.index] = "#" * new_level + " " + text + line_ending(lines[heading.index])

    updated = "".join(lines)
    if not dry_run and updated != original:
        path.write_text(updated)

    return updated != original, old_heading


def line_ending(line: str) -> str:
    return "\n" if line.endswith("\n") else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing files.")
    parser.add_argument("--post-dir", type=Path, default=POST_DIR)
    args = parser.parse_args()

    changed: list[tuple[Path, str]] = []
    for path in sorted(args.post_dir.glob("*.md")):
        did_change, old_heading = normalize_post(path, dry_run=args.dry_run)
        if did_change and old_heading:
            changed.append((path, old_heading))

    for path, old_heading in changed:
        print(f"{path}: {old_heading} -> {STANDARD_HEADING}")
    print(f"changed={len(changed)}")
    print(f"variants={len({old for _, old in changed})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
