"""Run the workflows' real selection commands against temporary Git histories."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[3]
WORKFLOWS = ("audits", "a11y", "tests")


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=repo, text=True).strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "ci-test@example.invalid")
    git(tmp_path, "config", "user.name", "CI selection test")
    helper = tmp_path / "scripts/ci/select-inputs.py"
    helper.parent.mkdir(parents=True)
    shutil.copyfile(ROOT / "scripts/ci/select-inputs.py", helper)
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-qm", "Initial tree")
    return tmp_path


def commit_path(repo: Path, path: str) -> None:
    file = repo / path
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("changed input\n")
    git(repo, "add", "--", path)
    git(repo, "commit", "-qm", "Change input")


def selection(repo: Path, base: str, event: str = "pull_request") -> set[str]:
    selected = set()
    for name in WORKFLOWS:
        workflow = (ROOT / f".github/workflows/{name}.yml").read_text()
        # Execute the command checked into each workflow, including its output
        # redirection. A disconnected helper or wrong workflow argument fails.
        commands = [
            line.strip().removeprefix("run: ")
            for line in workflow.splitlines()
            if line.strip().startswith("run: ") and "select-inputs.py" in line
        ]
        assert len(commands) == 1
        output = repo / ".git/selection-output"
        output.write_text("")
        subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", commands[0]],
            cwd=repo,
            env={**os.environ, "BASE": base, "GITHUB_EVENT_NAME": event,
                 "GITHUB_OUTPUT": str(output)},
            check=True,
        )
        key = "python" if name == "tests" else "site"
        assert output.read_text() in (f"{key}=true\n", f"{key}=false\n")
        if output.read_text() == f"{key}=true\n":
            selected.add(name)
    return selected


@pytest.mark.parametrize(("path", "expected"), [
    ("astro-site/src/pages/index.astro", {"audits", "a11y"}),
    ("astro-site/tests/e2e/smoke.spec.ts", {"audits", "a11y"}),
    ("astro-site/pnpm-lock.yaml", {"audits", "a11y"}),
    ("src/posts/example.md", {"audits", "a11y"}),
    ("tests/unit/example.test.mjs", {"audits"}),
    (".github/workflows/audits.yml", {"audits"}),
    (".github/workflows/a11y.yml", {"a11y"}),
    (".github/workflows/tests.yml", {"tests"}),
    ("uv.lock", {"a11y", "tests"}),
    ("pyproject.toml", {"a11y", "tests"}),
    ("scripts/link-validation/internal-link-check.py", {"a11y", "tests"}),
    ("scripts/lib/link_gatekeepers.py", {"a11y", "tests"}),
    ("scripts/ci/tests/example.py", set(WORKFLOWS)),
    ("scripts/compliance/content_check.py", {"tests"}),
    ("docs/example.md", set()),
    ("uv.lock.backup", set()),
    (".github/workflows/audits.yml.backup", set()),
    ("docs/newline\nastro-site/fake.md", set()),
])
def test_changed_inputs(repo: Path, path: str, expected: set[str]) -> None:
    base = git(repo, "rev-parse", "HEAD")
    commit_path(repo, path)
    assert selection(repo, base) == expected


@pytest.mark.parametrize("base", ["", "0" * 40, "missing-ref"])
def test_unavailable_diff_runs_all_jobs(repo: Path, base: str) -> None:
    assert selection(repo, base) == set(WORKFLOWS)


def test_rename_out_of_input_tree_still_runs_owner(repo: Path) -> None:
    commit_path(repo, "tests/unit/old.mjs")
    base = git(repo, "rev-parse", "HEAD")
    git(repo, "mv", "tests/unit/old.mjs", "old.txt")
    git(repo, "commit", "-qm", "Move test out of suite")
    assert selection(repo, base) == {"audits"}


def test_push_compares_previous_tree_after_history_rewrite(repo: Path) -> None:
    ancestor = git(repo, "rev-parse", "HEAD")
    commit_path(repo, "tests/unit/removed.mjs")
    before = git(repo, "rev-parse", "HEAD")
    git(repo, "checkout", "--detach", ancestor)
    commit_path(repo, "docs/new.md")
    # A merge-base diff would miss the removed test in a force push.
    assert selection(repo, before, "push") == {"audits"}
    assert selection(repo, before, "pull_request") == set()
