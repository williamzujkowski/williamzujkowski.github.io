"""Tests for check-lockfile-overrides.py (issue #540).

Every test that asserts the check PASSES is paired with a planted failure
proving the check can still fail on that same input shape. A guard nobody
has watched go red is a guard nobody knows works.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

MODULE_PATH = Path(__file__).resolve().parents[1] / "check-lockfile-overrides.py"
spec = importlib.util.spec_from_file_location("check_lockfile_overrides", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def make_package(overrides: dict[str, str] | None) -> str:
    data: dict = {"name": "site", "version": "1.0.0"}
    if overrides is not None:
        data["pnpm"] = {"overrides": overrides}
    return json.dumps(data)


FAITHFUL_LOCK = """\
lockfileVersion: '9.0'

settings:
  autoInstallPeers: true

overrides:
  satori>fflate: 0.7.5
  vite: '>=8.0.13'

importers:

  .:
    dependencies:
      satori:
        specifier: ^0.33.4
        version: 0.33.4

snapshots:

  '@shuding/opentype.js@1.4.0-beta.0':
    dependencies:
      fflate: 0.7.5

  satori@0.33.4:
    dependencies:
      fflate: 0.7.5
"""

# The exact shape Dependabot produced on PR #638: no `overrides:` header AND
# satori re-resolved to the vulnerable pin, while an unrelated package keeps
# 0.7.5 in the tree.
DEPENDABOT_LOCK = FAITHFUL_LOCK.replace(
    "overrides:\n  satori>fflate: 0.7.5\n  vite: '>=8.0.13'\n\n", ""
).replace("  satori@0.33.4:\n    dependencies:\n      fflate: 0.7.5",
          "  satori@0.33.4:\n    dependencies:\n      fflate: 0.7.3")


class TestParsing:
    def test_reads_declared_overrides(self):
        got = mod.parse_package_overrides(make_package({"a": "1", "b>c": "2"}))
        assert got == {"a": "1", "b>c": "2"}

    def test_no_pnpm_block_is_empty(self):
        assert mod.parse_package_overrides(make_package(None)) == {}

    def test_reads_lockfile_overrides_block(self):
        got = mod.parse_lockfile_overrides(FAITHFUL_LOCK)
        assert got == {"satori>fflate": "0.7.5", "vite": ">=8.0.13"}

    def test_block_stops_at_next_top_level_key(self):
        """`importers:` must not be swallowed into the overrides map."""
        got = mod.parse_lockfile_overrides(FAITHFUL_LOCK)
        assert "importers" not in got
        assert "snapshots" not in got

    def test_missing_block_is_empty(self):
        assert mod.parse_lockfile_overrides(DEPENDABOT_LOCK) == {}

    def test_resolves_dependency_under_the_named_parent(self):
        assert mod.resolved_dependency(FAITHFUL_LOCK, "satori", "fflate") == "0.7.5"

    def test_does_not_confuse_a_different_parent(self):
        """The 0.7.5 under @shuding/opentype.js must not be read as satori's."""
        assert mod.resolved_dependency(DEPENDABOT_LOCK, "satori", "fflate") == "0.7.3"
        assert mod.resolved_dependency(
            DEPENDABOT_LOCK, "@shuding/opentype.js", "fflate") == "0.7.5"

    def test_absent_parent_resolves_to_none(self):
        assert mod.resolved_dependency(FAITHFUL_LOCK, "nosuchpkg", "fflate") is None


class TestCheck:
    def test_faithful_lockfile_has_no_problems(self):
        pkg = make_package({"satori>fflate": "0.7.5", "vite": ">=8.0.13"})
        assert mod.check(pkg, FAITHFUL_LOCK) == []

    def test_no_declared_overrides_is_vacuously_fine(self):
        assert mod.check(make_package(None), DEPENDABOT_LOCK) == []

    def test_dependabot_lockfile_is_rejected(self):
        """The real PR #638 shape: dropped header AND regressed resolution."""
        pkg = make_package({"satori>fflate": "0.7.5", "vite": ">=8.0.13"})
        problems = mod.check(pkg, DEPENDABOT_LOCK)
        assert problems, "the #638 lockfile shape must not pass"
        assert any("no `overrides:` block" in p for p in problems)
        assert any("RESOLUTION REGRESSED" in p for p in problems)

    def test_restoring_only_the_header_still_fails(self):
        """This is the whole reason the check reads the resolved graph.

        A hand-fix that re-adds the header but leaves satori on the
        vulnerable pin would satisfy `pnpm install --frozen-lockfile` and a
        `grep -q '^overrides:'` check. It must not satisfy this one.
        """
        header_only = DEPENDABOT_LOCK.replace(
            "settings:\n  autoInstallPeers: true\n",
            "settings:\n  autoInstallPeers: true\n\noverrides:\n"
            "  satori>fflate: 0.7.5\n  vite: '>=8.0.13'\n",
        )
        pkg = make_package({"satori>fflate": "0.7.5", "vite": ">=8.0.13"})
        problems = mod.check(pkg, header_only)
        assert not any("no `overrides:` block" in p for p in problems)
        assert any("RESOLUTION REGRESSED" in p for p in problems)

    def test_missing_single_override_is_reported(self):
        pkg = make_package({"satori>fflate": "0.7.5", "vite": ">=8.0.13",
                            "esbuild": ">=0.28.1"})
        problems = mod.check(pkg, FAITHFUL_LOCK)
        assert any("esbuild" in p and "missing" in p for p in problems)

    def test_drifted_value_is_reported(self):
        pkg = make_package({"satori>fflate": "0.7.5", "vite": ">=9.0.0"})
        problems = mod.check(pkg, FAITHFUL_LOCK)
        assert any("`vite`" in p and ">=9.0.0" in p for p in problems)

    def test_parent_with_no_such_dependency_is_reported(self):
        pkg = make_package({"satori>nothere": "1.0.0"})
        problems = mod.check(pkg, FAITHFUL_LOCK)
        assert any("records no nothere dependency" in p for p in problems)

    def test_resolution_above_the_override_is_accepted(self):
        """An override is a floor. Resolving higher is not a regression."""
        higher = FAITHFUL_LOCK.replace(
            "  satori@0.33.4:\n    dependencies:\n      fflate: 0.7.5",
            "  satori@0.33.4:\n    dependencies:\n      fflate: 0.8.1")
        pkg = make_package({"satori>fflate": "0.7.5"})
        assert not any("REGRESSED" in p for p in mod.check(pkg, higher))


class TestAgainstTheRealTree:
    """Run the check against the repository's own committed files."""

    repo = Path(__file__).resolve().parents[3]

    def test_committed_lockfile_is_faithful(self):
        pkg = (self.repo / "astro-site" / "package.json").read_text()
        lock = (self.repo / "astro-site" / "pnpm-lock.yaml").read_text()
        assert mod.check(pkg, lock) == []

    def test_the_real_tree_would_fail_if_the_header_were_dropped(self):
        """Negative control: the passing test above must not be vacuous.

        If `parse_lockfile_overrides` silently returned {} for our real
        lockfile, the test above would pass for the wrong reason. Strip the
        header from the genuine file and the check must go red.
        """
        pkg = (self.repo / "astro-site" / "package.json").read_text()
        lock = (self.repo / "astro-site" / "pnpm-lock.yaml").read_text()
        if not mod.parse_package_overrides(pkg):
            pytest.skip("no overrides declared; nothing to drop")
        stripped = "\n".join(
            line for line in lock.splitlines()
            if not line.startswith("overrides:")
        )
        assert mod.check(pkg, stripped), "stripping the header must fail the check"
