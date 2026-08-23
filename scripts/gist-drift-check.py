#!/usr/bin/env python3
"""Compare each published gist against this repo's local mirror under gists/.

The gists are canonical; gists/ is a browsable copy. Nothing enforced that the
two agree, and five files silently diverged after the published versions were
corrected (see gists/README.md). This is that missing mechanism.

All the gists are public, so no credentials are needed beyond an authenticated
`gh` for the API rate limit.

Usage:
    uv run python scripts/gist-drift-check.py            # report and exit 1 on drift
    uv run python scripts/gist-drift-check.py --quiet    # only print problems
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
GISTS_DIR = REPO_ROOT / "gists"
MAPPING = GISTS_DIR / "gist-mapping.json"


def fetch_gist(gist_id: str) -> dict | None:
    """Return the parsed gist payload, or None if it cannot be read."""
    proc = subprocess.run(
        ["gh", "api", f"gists/{gist_id}"],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--quiet", action="store_true", help="only print files that need attention"
    )
    args = parser.parse_args()

    mapping = json.loads(MAPPING.read_text())
    entries = [
        (rel, meta["url"].rsplit("/", 1)[-1])
        for rel, meta in sorted(mapping.items())
        if isinstance(meta, dict) and "url" in meta
    ]

    problems: list[tuple[str, str, str]] = []
    in_sync = 0

    for rel, gist_id in entries:
        local = GISTS_DIR / rel
        gist = fetch_gist(gist_id)

        if gist is None:
            problems.append((rel, "GIST-UNREADABLE", f"gists/{gist_id}"))
            continue

        published = gist.get("files", {}).get(local.name)
        if published is None:
            names = ", ".join(gist.get("files", {})) or "(none)"
            problems.append((rel, "FILENAME-MISMATCH", f"gist contains: {names}"))
            continue

        if not local.exists():
            problems.append((rel, "LOCAL-MISSING", f"published {gist_id}"))
            continue

        pub_text = published.get("content", "")
        if pub_text == local.read_text():
            in_sync += 1
            if not args.quiet:
                print(f"  in-sync   {rel}")
        else:
            detail = (
                f"published {len(pub_text.splitlines())}L "
                f"vs local {len(local.read_text().splitlines())}L "
                f"(updated {gist.get('updated_at', '')[:10]})"
            )
            problems.append((rel, "DRIFTED", detail))

    print(f"\nchecked {len(entries)} mapped gists: {in_sync} in sync, {len(problems)} need attention")

    if not problems:
        print("No drift. The mirror matches what is published.\n")
        return 0

    print()
    for rel, status, detail in problems:
        print(f"  {status:18} {rel}")
        print(f"  {'':18} -> {detail}")
    print(
        "\nThe published gist is canonical. To resync a drifted file:\n"
        "  gh api gists/<id> --jq '.files[\"<name>\"].content' > gists/<path>\n"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
