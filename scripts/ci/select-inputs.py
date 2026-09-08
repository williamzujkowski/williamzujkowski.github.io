#!/usr/bin/env python3
"""Select required CI jobs from their inputs; unavailable diffs run the jobs.

Keep selection at job level so unrelated PRs still report required checks.
This helper needs only the Python and Git already installed on hosted runners.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys

INPUTS = {
    "audits": (
        "astro-site/",
        "src/",
        "tests/unit/",
        ".github/workflows/audits.yml",
        "scripts/ci/",
    ),
    "a11y": (
        "astro-site/",
        "src/",
        ".github/workflows/a11y.yml",
        "pyproject.toml",
        "uv.lock",
        "scripts/link-validation/",
        "scripts/lib/",
        "scripts/ci/",
    ),
    "tests": (
        "scripts/",
        "pyproject.toml",
        "uv.lock",
        ".github/workflows/tests.yml",
    ),
}


def changed_paths(base: str, event: str) -> list[str] | None:
    if not base:
        return None
    # PRs compare against the merge base; pushes compare their before/after
    # trees, including force pushes where the old tip need not be an ancestor.
    comparison = f"{base}...HEAD" if event == "pull_request" else f"{base}..HEAD"
    result = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", "-z", comparison, "--"],
        capture_output=True,
        check=False,
    )
    if result.returncode:
        print("Cannot compute changed inputs; running checks.", file=sys.stderr)
        return None
    return result.stdout.decode("utf-8", errors="surrogateescape").split("\0")[:-1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workflow", choices=INPUTS)
    args = parser.parse_args()
    paths = changed_paths(os.environ.get("BASE", ""), os.environ.get("GITHUB_EVENT_NAME", ""))
    selected = paths is None or any(
        path.startswith(pattern) if pattern.endswith("/") else path == pattern
        for path in paths or []
        for pattern in INPUTS[args.workflow]
    )
    output = "python" if args.workflow == "tests" else "site"
    print(f"{output}={str(selected).lower()}")


if __name__ == "__main__":
    main()
