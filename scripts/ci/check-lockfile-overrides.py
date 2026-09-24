#!/usr/bin/env -S uv run python3
"""Assert that pnpm's `overrides` survive into the committed lockfile.

WHY THIS EXISTS (issue #540, upstream dependabot/dependabot-core#16232)

Dependabot rewrites `astro-site/pnpm-lock.yaml` itself rather than shelling
out to pnpm, and its serialiser loses overrides in TWO distinct ways. Only
the first one is self-announcing:

1. It drops the top-level `overrides:` header. `pnpm install
   --frozen-lockfile` then refuses with ERR_PNPM_LOCKFILE_CONFIG_MISMATCH.
   Loud, but the message names neither the cause nor the fix, so the repo
   has re-diagnosed it from scratch more than once -- and got it wrong the
   first time (#533, disproved 3m43s later by #537).

2. It re-resolves a parent-scoped override back to the version the parent
   asked for. This one is SILENT. On PR #638 the header was gone AND
   `satori@0.33.4` had reverted to `fflate: 0.7.3`, reopening
   GHSA-px8p-9vwx-vf98.

Mode 2 is why this check reads the resolved graph instead of just grepping
for the header. Two cheaper checks were considered and both miss it:

  * `grep -q '^overrides:' pnpm-lock.yaml` -- passes on a lockfile whose
    header was restored by hand while the resolution stayed regressed,
    which is exactly what the #540 workaround warns against ("Do not
    repair only the header: regenerate and inspect the resolved graph").
  * "is fflate@0.7.5 anywhere in the lockfile?" -- passes on PR #638,
    because `@shuding/opentype.js` depends on 0.7.5 independently. The
    patched version being PRESENT says nothing about whether SATORI uses
    it.

The fix in every case is the same, and this script prints it:

    cd astro-site && pnpm install --lockfile-only

This check can only ADD a failure. If it is buggy and passes, the frozen
install behind it still refuses, so the gate is never weakened.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

FIX_COMMAND = "cd astro-site && pnpm install --lockfile-only"
ISSUE_URL = "https://github.com/williamzujkowski/williamzujkowski.github.io/issues/540"
UPSTREAM_URL = "https://github.com/dependabot/dependabot-core/issues/16232"


def parse_package_overrides(package_json: str) -> dict[str, str]:
    """The `pnpm.overrides` map from package.json, or {} if absent."""
    data = json.loads(package_json)
    overrides = data.get("pnpm", {}).get("overrides", {})
    if not isinstance(overrides, dict):
        return {}
    return {str(k): str(v) for k, v in overrides.items()}


def parse_lockfile_overrides(lockfile: str) -> dict[str, str]:
    """The top-level `overrides:` block from pnpm-lock.yaml, or {}.

    Hand-parsed rather than via PyYAML: this must run before `pnpm install`
    in a Node-only job, and the block is a flat scalar map at a known
    indent. A dependency here would be a dependency on the very install
    this check guards.
    """
    out: dict[str, str] = {}
    in_block = False
    for line in lockfile.splitlines():
        if not in_block:
            if line.rstrip() == "overrides:":
                in_block = True
            continue
        # The block ends at the next top-level key (column 0, non-blank).
        if line.strip() and not line.startswith((" ", "\t")):
            break
        if not line.strip():
            continue
        match = re.match(r"\s+(.+?):\s*(.+?)\s*$", line)
        if match:
            key, value = match.group(1), match.group(2)
            out[key.strip("'\"")] = value.strip("'\"")
    return out


def resolved_dependency(lockfile: str, parent: str, child: str) -> str | None:
    """The version `child` resolves to under `parent` in the snapshots.

    `parent` is matched as a package key prefix (`satori@`), so it covers
    whatever version of the parent is in the tree without this check
    needing to be updated on every parent bump.
    """
    lines = lockfile.splitlines()
    current: str | None = None
    for line in lines:
        stripped = line.strip()
        # A package/snapshot key sits at exactly two spaces and ends in ':'.
        if line.startswith("  ") and not line.startswith("   ") and stripped.endswith(":"):
            current = stripped[:-1].strip("'\"")
            continue
        if current is None or not current.startswith(f"{parent}@"):
            continue
        match = re.match(rf"\s+{re.escape(child)}:\s*(\S+)\s*$", line)
        if match:
            return match.group(1).strip("'\"")
    return None


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(part) for part in re.findall(r"\d+", version)[:3])


def check(package_json: str, lockfile: str) -> list[str]:
    """Return a list of problems; empty means the lockfile is faithful."""
    problems: list[str] = []
    declared = parse_package_overrides(package_json)
    if not declared:
        return problems

    recorded = parse_lockfile_overrides(lockfile)
    if not recorded:
        problems.append(
            "pnpm-lock.yaml has no `overrides:` block, but package.json declares "
            f"{len(declared)}: {', '.join(sorted(declared))}."
        )
    else:
        for name, spec in sorted(declared.items()):
            if name not in recorded:
                problems.append(
                    f"override `{name}: {spec}` is in package.json but missing "
                    "from the lockfile's `overrides:` block."
                )
            elif recorded[name] != spec:
                problems.append(
                    f"override `{name}` is `{spec}` in package.json but "
                    f"`{recorded[name]}` in the lockfile."
                )

    # The silent mode: a parent-scoped override (`satori>fflate`) whose
    # header is fine but whose resolved edge went back to the parent's own
    # pin. Only parent-scoped entries can be checked this way; a bare
    # override has no single parent to inspect.
    for name, spec in sorted(declared.items()):
        if ">" not in name:
            continue
        parent, child = (part.strip() for part in name.split(">", 1))
        if not parent or not child:
            continue
        resolved = resolved_dependency(lockfile, parent, child)
        if resolved is None:
            problems.append(
                f"override `{name}: {spec}` declares that {parent} should use "
                f"{child} {spec}, but the lockfile records no {child} "
                f"dependency for {parent} at all."
            )
        elif version_tuple(resolved) < version_tuple(spec):
            problems.append(
                f"RESOLUTION REGRESSED: {parent} resolves {child} to "
                f"{resolved}, below the overridden {spec}. The `overrides:` "
                "header alone does not catch this."
            )
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package-json", default="astro-site/package.json", type=Path)
    parser.add_argument("--lockfile", default="astro-site/pnpm-lock.yaml", type=Path)
    args = parser.parse_args()

    for path in (args.package_json, args.lockfile):
        if not path.is_file():
            print(f"::error::{path} not found", file=sys.stderr)
            return 1

    problems = check(args.package_json.read_text(), args.lockfile.read_text())
    if not problems:
        print(f"Lockfile overrides are faithful to {args.package_json}.")
        return 0

    print(f"::error::{args.lockfile} does not match {args.package_json}.")
    for problem in problems:
        print(f"  - {problem}")
    print()
    print(f"  Fix:      {FIX_COMMAND}")
    print(f"  Context:  {ISSUE_URL}")
    print(f"  Upstream: {UPSTREAM_URL}")
    print()
    print(
        "  If this is a Dependabot branch, regenerate the lockfile and inspect\n"
        "  the resolved graph before pushing -- restoring the header alone can\n"
        "  leave a downgraded, vulnerable dependency in place."
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
