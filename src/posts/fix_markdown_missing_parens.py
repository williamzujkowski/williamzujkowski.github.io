#!/usr/bin/env python3
"""
Fix Markdown links missing the closing ')'.

Handles two conservative cases:
  A) [text](https://example.com            # missing ')' at end of line
  B) [text](https://example.com (2021      # missing ')' before trailing content

Safety:
- Skips fenced code blocks (``` and ~~~).
- Dry-run by default (prints unified diffs).
- Creates timestamped .bak backups on write (unless --no-backup).
- Recurses from CWD, skipping common junk dirs.
"""

from __future__ import annotations
import argparse
import difflib
import pathlib
import re
import sys
from datetime import datetime

DEFAULT_EXCLUDE_DIRS = {
    ".git", ".hg", ".svn", "node_modules", ".yarn", ".venv", "venv",
    ".tox", "dist", "build", ".cache"
}
DEFAULT_EXTS = {".md", ".mdx", ".markdown"}

# Fenced code blocks (start/stop on the same kind of fence)
FENCE_RE = re.compile(r"^\s*(```|~~~)")

# Case A: ends with a missing ')'
BROKEN_EOF_RE = re.compile(
    r"""
    (?P<prefix>\[[^\]\n]+\]\()      # [text](
    (?P<target>[^\s\)]+)            # URL/path (no spaces or ')')
    (?P<trail_spaces>\s*)           # spaces up to EOL
    $                               # end of line
    """,
    re.VERBOSE,
)

# Case B: missing ')' *before* trailing content starting with a space,
# with no closing ')' anywhere on the line.
BROKEN_WITH_TRAIL_RE = re.compile(
    r"""
    (?P<prefix>\[[^\]\n]+\]\()      # [text](
    (?P<target>[^\s\)]+)            # URL/path (no spaces or ')')
    (?P<sep>\s+)                    # at least one space (separator)
    (?P<after>[^)]*)                # anything that is *not* ')', up to EOL
    $                               # end of line
    """,
    re.VERBOSE,
)

def is_code_fence(line: str) -> bool:
    return bool(FENCE_RE.match(line))

def _fix_once(line: str) -> tuple[str, bool]:
    """
    Attempt a single conservative fix on the line.
    Returns (possibly_modified_line, changed?)
    """
    # If there is already a ')' closing a link on this line after an opening '(' from a link,
    # we won't touch it (avoids interfering with valid [text](url "title") links).
    # We only act when *no* closing ')' exists after the matched URL segment.
    if BROKEN_EOF_RE.search(line):
        m = BROKEN_EOF_RE.search(line)
        assert m is not None
        # Sanity: ensure there isn't a ')' later (shouldn't be due to regex), keep cautious.
        return f"{m.group('prefix')}{m.group('target')}){m.group('trail_spaces')}\n", True

    if BROKEN_WITH_TRAIL_RE.search(line):
        m = BROKEN_WITH_TRAIL_RE.search(line)
        assert m is not None
        # Only fix if there is no ')' anywhere after the '(' that starts the link
        # (our pattern already enforces no ')' to EOL).
        return f"{m.group('prefix')}{m.group('target')}){m.group('sep')}{m.group('after')}\n", True

    return line, False

def fix_line_conservatively(line: str, max_passes: int = 3) -> str:
    """
    Repeatedly apply a single safe fix per pass to handle multiple broken links on one line.
    Caps passes to avoid runaway loops.
    """
    out = line
    for _ in range(max_passes):
        out2, changed = _fix_once(out)
        if not changed:
            break
        out = out2
    return out

def process_text(text: str) -> str:
    out_lines = []
    in_fence = False
    fence_token = None  # track ``` vs ~~~

    for raw in text.splitlines(keepends=True):
        if is_code_fence(raw):
            tok = raw.strip().split()[0]
            if not in_fence:
                in_fence, fence_token = True, tok
            else:
                # Only close if matching the same fence token
                if tok == fence_token:
                    in_fence, fence_token = False, None
            out_lines.append(raw)
            continue

        if in_fence:
            out_lines.append(raw)
            continue

        out_lines.append(fix_line_conservatively(raw))
    return "".join(out_lines)

def iter_files(root: pathlib.Path, include_exts: set[str], exclude_dirs: set[str]) -> list[pathlib.Path]:
    files = []
    for p in root.rglob("*"):
        if p.is_dir():
            continue
        if p.suffix.lower() in include_exts:
            # ensure no excluded parent
            if any(part in exclude_dirs for part in p.parts):
                continue
            files.append(p)
    return files

def main():
    ap = argparse.ArgumentParser(description="Fix Markdown links missing a closing ')'.")
    ap.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan (default: current directory).")
    ap.add_argument("--exts", default=",".join(sorted(DEFAULT_EXTS)),
                    help=f"Comma-separated file extensions (default: {','.join(sorted(DEFAULT_EXTS))})")
    ap.add_argument("--exclude-dirs", default=",".join(sorted(DEFAULT_EXCLUDE_DIRS)),
                    help=f"Comma-separated directory names to skip (default: {','.join(sorted(DEFAULT_EXCLUDE_DIRS))})")
    ap.add_argument("--write", action="store_true", help="Apply changes in-place (with .bak backups).")
    ap.add_argument("--no-backup", action="store_true", help="Do not create .bak backups when writing.")
    args = ap.parse_args()

    include_exts = {
        (e.strip().lower() if e.strip().startswith(".") else f".{e.strip().lower()}")
        for e in args.exts.split(",") if e.strip()
    }
    exclude_dirs = {d.strip() for d in args.exclude_dirs.split(",") if d.strip()}

    targets: list[pathlib.Path] = []
    for raw in args.paths:
        p = pathlib.Path(raw)
        if p.is_file():
            if p.suffix.lower() in include_exts:
                targets.append(p)
        elif p.is_dir():
            targets.extend(iter_files(p, include_exts, exclude_dirs))
        else:
            print(f"! Skipping missing path: {raw}", file=sys.stderr)

    if not targets:
        print("No target files found.")
        sys.exit(0)

    changed_any = False
    for fpath in sorted(set(targets)):
        try:
            original = fpath.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"! Skipping non-UTF8 file: {fpath}", file=sys.stderr)
            continue

        fixed = process_text(original)

        if fixed == original:
            continue

        changed_any = True
        if args.write:
            if not args.no_backup:
                ts = datetime.now().strftime("%Y%m%d%H%M%S")
                backup = fpath.with_suffix(fpath.suffix + f".bak.{ts}")
                backup.write_text(original, encoding="utf-8")
            fpath.write_text(fixed, encoding="utf-8")
            print(f"[fixed] {fpath}")
        else:
            print(f"\n--- {fpath}")
            print(f"+++ {fpath}  (proposed)")
            for line in difflib.unified_diff(
                original.splitlines(keepends=True),
                fixed.splitlines(keepends=True),
                fromfile=str(fpath),
                tofile=str(fpath),
            ):
                sys.stdout.write(line)

    if not changed_any:
        print("No fixes needed. ✅")
    elif not args.write:
        print("\nDry-run only. Re-run with --write to apply changes. (Backups will be created unless --no-backup.)")

if __name__ == "__main__":
    main()
