# Research note: plant the defect, watch the gate

**Post:** `src/posts/2026-10-15-plant-the-defect-watch-the-gate.md` (slot 2026-10-15, `draft: false`; root has said the final date will be 2026-10-22 and will rename at integration)
**Prepared:** 2026-10-01. **Repo revision experimented on:** `fc0c1eb3cdb251e295fb5c908122e07892358839` (main).
**Type:** experiment report on this repository's own CI gates + reading of prior art.
**Lab:** none. The experiments are one-off mutations of this repository's checks, not
reusable lab code, so nothing was added to `research-labs`; the scripts and raw output
are retained below in full. No gate was modified on this branch; every mutation was
reverted and the tree verified clean (`git status --porcelain` empty) after each run.

## Thesis

A gate that cannot fail produces exactly the output of a gate that passed. The only way
to tell them apart is to plant a known defect and require the gate to go red, through the
same entry point CI runs, and to put a floor on how much the gate examined.

Falsifier: if the repository's required checks went red on every planted defect that
matches a rule they claim to enforce, and asserted a non-trivial floor, the post's
examples would not exist. Experiments 1-4 below are the attempt; five of seven rows survived.

## Sources (accessed 2026-10-01)

| # | Source | Identity | Used for |
| --- | --- | --- | --- |
| S1 | Yue Jia, Mark Harman, "An Analysis and Survey of the Development of Mutation Testing" | IEEE TSE 37(5):649-678, Sept 2011, doi:10.1109/TSE.2010.62 (Crossref). Full text read from the accepted-manuscript PDF (archived copy of `crest.cs.ucl.ac.uk/fileadmin/crest/sebasepaper/JiaH10.pdf` via web.archive.org; the live UCL host refused connections). Note: accepted version, "may change prior to final publication". | Definition (faults "deliberately seeded into the original program, by simple syntactic changes"), history (Lipton 1971 student paper; DeMillo et al. and Hamlet late 1970s), equivalent mutants (§II-B: "syntactically different but functionally equivalent"; detection undecidable). |
| S2 | R.A. DeMillo, R.J. Lipton, F.G. Sayward, "Hints on Test Data Selection: Help for the Practicing Programmer" | *Computer* 11(4):34-41, April 1978, doi:10.1109/C-M.1978.218136 (Crossref metadata) | Cited only as a founding paper, per S1. Full text NOT read; the post makes no claim about its content. |
| S3 | Goran Petrović, Marko Ivanković, "State of Mutation Testing at Google" | ICSE-SEIP '18, pp. 163-171, doi:10.1145/3183519.3183521 (Crossref); PDF `storage.googleapis.com/gweb-research2023-media/pubtools/4203.pdf` (linked from research.google) | Abstract: "assesses test suite efficacy by inserting small faults"; §3 "For each line, at most one mutant is generated"; arid lines (logging etc.) suppressed; contributions list: "the reported usefulness of the surfaced results improved from 20% to 80%". Note: the research.google landing page summary said 14,000 code authors, the PDF says 13,000; the post uses neither. |
| S4 | Stryker Mutator docs | https://stryker-mutator.io/docs/ | Exact HTML: "If your tests <em>fail</em> then the mutant is <em>killed</em>." / "If your tests passed, the mutant <em>survived</em>."; platforms StrykerJS, Stryker.NET, Stryker4s. |
| S5 | mutmut docs | https://mutmut.readthedocs.io/en/latest/ | "Mutmut is a mutation testing system for Python, with a strong focus on ease of use." |
| S6 | EICAR, "Anti Malware Testfile" | https://www.eicar.org/download-anti-malware-testfile/ | "Instead of using real malware, which could cause real damage, this test file allows people to test anti-virus software without having to use a real computer virus." and the smoke-detector sentence quoted in the post. |
| S7 | Bo Chen, "From Runnable to Verifiable: An Independent Reproducibility Study of LLM/Agent-Driven Vulnerability Validation Artifacts" | arXiv:2608.09567v1 [cs.CR], submitted 2026-08-10; preprint, not peer reviewed; self-described exploratory results from a pre-registered protocol. PDF read this session (§5.4, abstract). Suggested by root's discovery pass. | Abstract + §5.4: patched-counterfactual verdicts on 30 cases, 10 clean / 20 dirty; "A trigger signal on the vulnerable build is not evidence of CVE-specific reproduction unless the patched counterfactual is clean." |
| R1 | Issues #492, #511, #642, #643, #644, #645, #647, #655, #660; PRs #516, #652, #656 | `gh issue view N --json ...`, retrieved 2026-10-01 | History and claims attributed to them in the post. |
| R2 | Branch protection + check runs | `gh api .../branches/main/protection`; `gh api .../commits/<sha>/check-runs` | Required contexts `["remarque","axe","check-lint","pytest"]`, `strict: true`; three skipped merges (Experiment 5). |

## Claim ledger

| Proposed claim (post) | Kind | Evidence and locator | Scope/caveat | Status |
| --- | --- | --- | --- | --- |
| Four required checks: remarque, axe, check-lint, pytest | observation | R2 protection API output (Exp 5) | as of 2026-10-01 | verified |
| Typography audit prints "Floor: 13px (Remarque --text-micro)" and passes with `--text-micro: 0.5rem` appended; remarque wrapper also passes | our observation | Exp 1 section C | `fc0c1eb`; mutation appended to `global.css` after the `remarque-tokens/core` import, so it wins the cascade at equal specificity (not rendered/verified in a browser) | verified |
| Twelve declarations under `astro-site/src/` use `font-size: var(--text-micro)` | observation | `rg -o 'font-size\s*:\s*var\(--text-micro' src \| wc -l` → 12 (53 for all `--text-*`, matching #642) | | verified |
| `remarque` job runs the typography audit | observation | `.github/workflows/audits.yml` remarque job steps | | verified |
| Control: literal 8px → exit 1 (audit and wrapper) | our observation | Exp 1 section B | | verified |
| `exit(1)`→`exit(0)` mutation: unit tests 56/56; audit prints FAIL then exits 0 | our observation | Exp 2 section B | | verified |
| `scan()` stub: unit tests 56/56; audit "No violations found. (37 files scanned)" with 8px planted | our observation | Exp 2 section C | | verified |
| Reverting #652's `(?![\w-])` to `\b` → 1 of 56 unit tests fail | our observation | Exp 2 section D | | verified |
| Deleting `scripts/ci/tests/test_*.py`: 345 → 304 passed, exit 0, using tests.yml:60's command | our observation | Exp 3 | 41 tests lost; `-p no:cacheprovider` added to avoid writing cache | verified |
| Nested posts: extractor 0 links from 0 files, validator + summary exit 0; flat control 1,544 links from 97 files | our observation | Exp 4, 4b | run against a COPY of the posts in scratch; #645 reports the same with an empty dir | verified |
| #492: then-only required check passed when tool never ran | source (repo) | issue #492 body | contexts were `["remarque"]` then | verified |
| #511: 60+ violations across 18 checkers; axe 18 passed on empty dist | source (repo) | issue #511 body | | verified |
| #516 fixed with negative-control matrices | source (repo) | PR #516 body | | verified |
| #652 tests read scripts as text and assert on regex literals | source (repo) + observation | `tests/unit/audit-scanner-reach.test.mjs` header ("pattern-reach tests, not end-to-end runs") | | verified |
| #660: 79 mutations, 51 killed, 28 survived, 4 equivalent; quoted sentence | source (repo) | issue #660 body | performed in an earlier session at `92335f9`; not re-run here | verified (as recorded) |
| #660: `is_link_local` drop equivalent because `ipaddress` covers 169.254/16 under `is_private` | source (repo) | issue #660 "Narrower" | | verified (as recorded) |
| #660: compliance docstring promises zero-post scan exits non-zero; untested | source (repo) | issue #660 | | verified (as recorded) |
| MIN_TESTS was 42 vs 48; 7 of 10 files deletable; now 56 = exact count | source (repo) + observation | PR #652 body; `run-unit-tests.mjs` `MIN_TESTS = 56`; Exp 2 baseline `# tests 56` | | verified |
| Playwright has no `forbidOnly` | observation | `grep forbidOnly astro-site/playwright.config.ts` → no match | | verified |
| pytest exits 5 only if zero tests collected across all paths | source (repo) | #644 item 2; consistent with Exp 3 | pytest semantics not separately fetched from docs | partial (consistent with observation) |
| Link extractor uses non-recursive glob | observation | `link-extractor.py:128` `glob('*.md')` | | verified |
| Three September commits merged with all four required checks `skipped` | observation | Exp 5 (3cfaf5f/#627, 336f1a4/#626, 9588210/#617) | legitimate docs-only skips; the crash path is hypothetical | verified |
| "changes" job had not failed in last 30 runs of each workflow | source (repo) | #644 item 4 | not re-measured | verified (as recorded) |
| Jia & Harman definition/history quotes | source finding | S1 §I | accepted-manuscript text | verified |
| Stryker killed/survived quote; platforms | source finding | S4 | | verified |
| EICAR purpose + smoke-detector quote | source finding | S6 | | verified |
| Chen preprint: 20 of 30 verdict-reaching cases still produced the claimed signal on the patched build; trigger-without-clean-counterfactual conclusion | source finding | S7 abstract and §5.4 ("30 verdicts (10 clean / 20 dirty) plus 3 unbuildable") | preprint; LLM/agent vulnerability artifacts, not CI; post labels it a preprint | verified |
| Google: at most one mutant per line, arid lines incl. logging, usefulness 20%→80% | source finding | S3 abstract, §3, §4.1, contributions list | | verified |
| "For a handful of CI gates the mutants can be hand-written" | inference | labelled as inference in post | | inference |
| Scanning-pipeline post's original gate echoed a string | source (repo) | `src/posts/2025-10-06-automated-security-scanning-pipeline.md` "What blocks, precisely" + original-gist paragraph | | verified |
| #642/#644/#645/#660 open; token mutation still passes on main | observation | `gh issue view` states 2026-10-01; Exp 1 | "as of this writing" = 2026-10-01; re-check before 10-15 | verified (date-bound) |

## Overlap check

- `rg -il "mutation test|mutant|mutmut|stryker" src/posts docs/shelved-drafts docs/research` → no hits.
- `rg -il "fail open|exit 0|exit code" src/posts` → 2025-07-22 (Claude CLI standards) and 2025-08-25 (Suricata); both incidental, weak.
- `gh issue list --state all --search "mutation testing"` → #660, #647, #642, #645 (the evidence itself), #492, #501, #509 (history). No blog proposal on this topic. `gh pr list --state all --search mutation` → #652 and older CI PRs; #664 (open, editorial calendar guard) unrelated.
- **Moderate:** `2026-07-30-prove-the-gate-not-the-agent.md` proves an AI-agent policy gate in Dafny + differential testing. Different question (is the decision function correct for all inputs) vs this post (can the CI check fail at all, and did it look). Cross-linked from the post.
- **Moderate:** `2025-10-06-automated-security-scanning-pipeline.md` documents an aggregate gate that echoed a string. Cross-linked as the degenerate case.
- **Weak:** `2026-08-18-recovery-needs-a-dry-run.md` (preview a recovery action); shared "rehearse the safety mechanism" theme only. No link.
- Both linked posts are dated before 2026-10-15 and `draft: false`.

## Layer-1 coverage (self-applied, 2026-10-01)

| Stage | Status | Notes |
| --- | --- | --- |
| blog-overlap | completed | See above. |
| blog-factcheck | completed | All 30 ledger rows checked; every number recomputed from raw output or read from the primary text this session. S2 content not read (cited for identity only). One fix applied: "almost nobody points the technique back at it" removed as unsupported. |
| blog-llm-tells | manual | Read for voice. Removed a three-item list ("its banner, its docstring, its name"). 0 em dashes, 0 exclamation marks. Remaining risk: "That is the point of this post." is mildly meta; kept. |
| blog-nda-check | completed | All evidence is this public repository and public papers. No employer, agency or incident references. First person used only for actions recorded in this repo's issues/PRs and in this note. |
| blog-argument-shape | completed | Type: experiment report + position argument. Thesis para 3. Evidence map = ledger. Close quotes #642's acceptance criterion; follows from the body. Strongest objections (equivalent mutants; fixture only catches its own shape) answered in "What it costs". |
| blog-visuals | completed | One `.flow` (role=group, aria-label, legs mirrored), one Markdown table, one doodle TODO for root. Rendered via Playwright against `astro preview` at 375px and 1280px, light and dark: HTTP 200, `scrollWidth` equals viewport at both widths (no horizontal scroll). Doodle not drawn (root handles art). |
| blog-artifact-check | completed | No gists. Commands and file paths named in the post checked against the repo at `fc0c1eb` (audit banner text, `MIN_TESTS`, `tests.yml:60` command, `link-extractor.py:128`, audits.yml steps). |

## Build and audit

- `pnpm install --frozen-lockfile` ok; `PUBLICATION_AS_OF=2026-10-15T00:00:00Z pnpm build` exit 0; page and `/og/2026-10-15-plant-the-defect-watch-the-gate.png` generated.
- `pnpm run audit` exit 0 (the inner "audit FAILED — 2 problem(s)" line is the two baselined `zine.css` false positives; the wrapper reports 0 real failures).
- `pnpm test:unit` 56/56.

## Limitations

- Seven hand-chosen mutations, chosen because issues predicted they would survive. This is a demonstration that specific holes exist on `fc0c1eb`, not a mutation score for the repo. #660's 79-mutant run is cited, not reproduced.
- The token mutation's rendered effect (8px text) follows from the cascade; it was not verified in a browser.
- Experiment 4 used a copy of the posts; the real workflow was not run against a reorganised tree.
- The Playwright `test.only` hole (#644 item 1) is cited from the issue and the config grep; it was not executed.
- The status of open issues is as of 2026-10-01. If any lands before publication, the "as of this writing" paragraph needs updating.

## Commands run and raw output

Experiment scripts were run from scratch (`<scratch>` below) against the worktree at
`fc0c1eb`. Paths under the session scratch directory are abbreviated to `<scratch>`.

### Experiment 1 — typography floor vs its own token (#642 item 1)

```bash
#!/usr/bin/env bash
# Experiment 1: typography floor vs the token it is named after (#642 item 1).
# Plants each mutation in the worktree, runs the gate, records exit codes, reverts.
set -u
WT=/tmp/claude-worktrees/da2f7ebc-4212eac9bf09
cd "$WT/astro-site" || exit 2
CSS=src/styles/global.css
echo "HEAD $(git -C "$WT" rev-parse HEAD)  node $(node --version)  date $(date -u +%FT%TZ)"

run() {
  echo "--- typography-audit"
  node scripts/typography-audit.mjs; echo "typography-audit exit=$?"
  echo "--- run-remarque-audit (tail)"
  node scripts/run-remarque-audit.mjs > /tmp/ra.$$ 2>&1; rc=$?
  tail -3 /tmp/ra.$$; rm -f /tmp/ra.$$
  echo "run-remarque-audit exit=$rc"
}

echo "=== A. baseline (clean main)"
run

echo "=== B. positive control: a literal 8px declaration"
printf '\n.planted-control { font-size: 8px; }\n' >> "$CSS"
run
git -C "$WT" checkout -- "astro-site/$CSS"

echo "=== C. mutation: redefine the token every micro declaration uses"
printf '\n:root { --text-micro: 0.5rem; }\n' >> "$CSS"
echo "declarations using var(--text-micro) under src/: $(grep -rho 'font-size: *var(--text-micro)' src | wc -l)"
run
git -C "$WT" checkout -- "astro-site/$CSS"

echo "=== D. tree restored?"
git -C "$WT" status --porcelain astro-site/src
```

Output:

```text
HEAD fc0c1eb3cdb251e295fb5c908122e07892358839  node v22.22.3  date 2026-10-01T04:45:19Z
=== A. baseline (clean main)
--- typography-audit
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  No violations found. (37 files scanned)
typography-audit exit=0
--- run-remarque-audit (tail)

remarque-audit passed (contrast + gamut clean; all source-scan findings are reviewed, baselined false positives) ✓

run-remarque-audit exit=0
=== B. positive control: a literal 8px declaration
--- typography-audit
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  [FAIL] styles/global.css:1645 → 8px (8.0px)
         .planted-control { font-size: 8px; }

1 typography violation(s).
typography-audit exit=1
--- run-remarque-audit (tail)

remarque-audit FAILED (after baseline suppression).

run-remarque-audit exit=1
=== C. mutation: redefine the token every micro declaration uses
declarations using var(--text-micro) under src/: 12
--- typography-audit
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  No violations found. (37 files scanned)
typography-audit exit=0
--- run-remarque-audit (tail)

remarque-audit passed (contrast + gamut clean; all source-scan findings are reviewed, baselined false positives) ✓

run-remarque-audit exit=0
=== D. tree restored?
```

### Experiment 2 — mutate the audit, run the unit suite (#660)

```bash
#!/usr/bin/env bash
# Experiment 2: mutate the audit scripts themselves; does `pnpm test:unit` notice? (#660)
set -u
WT=/tmp/claude-worktrees/da2f7ebc-4212eac9bf09
cd "$WT/astro-site" || exit 2
TYPO=scripts/typography-audit.mjs
ACCENT=scripts/accent-font-audit.mjs
CSS=src/styles/global.css
echo "HEAD $(git -C "$WT" rev-parse HEAD)  node $(node --version)  date $(date -u +%FT%TZ)"

unit() {
  node scripts/run-unit-tests.mjs > /tmp/ut.$$ 2>&1; rc=$?
  grep -E '^# (tests|pass|fail) ' /tmp/ut.$$; grep -E '^not ok' /tmp/ut.$$ | head -3; rm -f /tmp/ut.$$
  echo "test:unit exit=$rc"
}
restore() { git -C "$WT" checkout -- astro-site/scripts astro-site/src; }

echo "=== A. baseline"
unit

echo "=== B. M1: typography audit exits 0 on violations (last process.exit(1) -> 0)"
python3 - "$TYPO" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
i=s.rindex("process.exit(1);"); s=s[:i]+"process.exit(0);"+s[i+len("process.exit(1);"):]
open(p,"w").write(s)
PY
git -C "$WT" diff --stat -- astro-site/scripts
unit
echo "--- and the gate itself, with a literal 8px planted:"
printf '\n.planted-control { font-size: 8px; }\n' >> "$CSS"
node scripts/typography-audit.mjs; echo "typography-audit exit=$?"
restore

echo "=== C. M2: typography scan() counts the file, then returns without reading it"
python3 - "$TYPO" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace("function scan(file) {\n  filesScanned += 1;", "function scan(file) {\n  filesScanned += 1; return;",1)
open(p,"w").write(s)
PY
git -C "$WT" diff --stat -- astro-site/scripts
unit
printf '\n.planted-control { font-size: 8px; }\n' >> "$CSS"
node scripts/typography-audit.mjs; echo "typography-audit exit=$?"
restore

echo "=== D. M3 (control the tests SHOULD catch): revert #652's accent-font fix to \\b"
python3 - "$ACCENT" <<'PY'
import sys; p=sys.argv[1]; s=open(p).read()
s=s.replace(r"/\.hand-note(?![\w-])/.test(line)", r"/\.hand-note\b/.test(line)",1)
open(p,"w").write(s)
PY
git -C "$WT" diff --stat -- astro-site/scripts
unit
restore

echo "=== E. tree restored?"
git -C "$WT" status --porcelain astro-site
```

Output:

```text
HEAD fc0c1eb3cdb251e295fb5c908122e07892358839  node v22.22.3  date 2026-10-01T04:45:55Z
=== A. baseline
# tests 56
# pass 56
# fail 0
test:unit exit=0
=== B. M1: typography audit exits 0 on violations (last process.exit(1) -> 0)
 astro-site/scripts/typography-audit.mjs | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
# tests 56
# pass 56
# fail 0
test:unit exit=0
--- and the gate itself, with a literal 8px planted:
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  [FAIL] styles/global.css:1645 → 8px (8.0px)
         .planted-control { font-size: 8px; }

1 typography violation(s).
typography-audit exit=0
=== C. M2: typography scan() counts the file, then returns without reading it
 astro-site/scripts/typography-audit.mjs | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
# tests 56
# pass 56
# fail 0
test:unit exit=0
USWDS Typography Floor Audit

  Floor: 13px (Remarque --text-micro)

  No violations found. (37 files scanned)
typography-audit exit=0
=== D. M3 (control the tests SHOULD catch): revert #652's accent-font fix to \b
 astro-site/scripts/accent-font-audit.mjs | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
# tests 56
# pass 55
# fail 1
not ok 4 - accent-font-audit: .hand-note-wrapper does not open the allowlist
test:unit exit=1
=== E. tree restored?
```

### Experiment 3 — required pytest command with a suite deleted (#644 item 2)

```bash
#!/usr/bin/env bash
# Experiment 3: the required `pytest` check has no floor (#644 item 2).
# Runs the exact command from .github/workflows/tests.yml:60, then deletes a
# whole suite's test files and runs it again.
set -u
WT=/tmp/claude-worktrees/da2f7ebc-4212eac9bf09
cd "$WT" || exit 2
echo "HEAD $(git rev-parse HEAD)  date $(date -u +%FT%TZ)"
CMD=(uv run --with pytest python -m pytest scripts/link-validation/tests/ scripts/ci/tests/ scripts/security-labs/ scripts/blog-audit/tests/ scripts/skills/tests/ -q -p no:cacheprovider)

echo "=== A. baseline"
"${CMD[@]}" 2>&1 | tail -1; echo "pytest exit=${PIPESTATUS[0]}"

echo "=== B. mutation: delete every test file in scripts/ci/tests/"
rm scripts/ci/tests/test_*.py
ls -A scripts/ci/tests/
"${CMD[@]}" 2>&1 | tail -1; echo "pytest exit=${PIPESTATUS[0]}"
git checkout -- scripts/ci/tests

echo "=== C. tree restored?"
git status --porcelain scripts
```

Output:

```text
HEAD fc0c1eb3cdb251e295fb5c908122e07892358839  date 2026-10-01T04:46:21Z
=== A. baseline
345 passed, 11 subtests passed in 42.49s
pytest exit=0
=== B. mutation: delete every test file in scripts/ci/tests/
__pycache__
304 passed, 11 subtests passed in 5.54s
pytest exit=0
=== C. tree restored?
```

### Experiment 4 — link pipeline over a nested corpus (#645 item 1)

```bash
#!/usr/bin/env bash
# Experiment 4: the link pipeline over a corpus it cannot see (#645 item 1).
# Mutation: the posts move one directory down (src/posts/2026/*.md), the kind of
# reorganisation a repo does on purpose. Runs the same three steps link-monitor.yml
# runs, against a COPY of the posts in scratch; the repo is not modified.
# No network is touched because zero URLs reach the validator.
set -u
WT=/tmp/claude-worktrees/da2f7ebc-4212eac9bf09
S=<scratch>/exp4
rm -rf "$S"; mkdir -p "$S/posts/2026"
cd "$WT" || exit 2
echo "HEAD $(git rev-parse HEAD)  date $(date -u +%FT%TZ)"
cp src/posts/*.md "$S/posts/2026/"
echo "posts copied into nested dir: $(ls "$S/posts/2026" | wc -l)"
LV=scripts/link-validation

uv run python $LV/link-extractor.py --posts-dir "$S/posts" --output "$S/links.json" 2>&1 | tail -4
echo "link-extractor exit=${PIPESTATUS[0]}"
python3 -c "import json;d=json.load(open('$S/links.json'));print('links.json stats:',d.get('stats'))"

uv run python $LV/simple-validator.py --links "$S/links.json" --output "$S/validation.json" 2>&1 | tail -4
echo "simple-validator exit=${PIPESTATUS[0]}"

uv run python $LV/link-health-summary.py --input "$S/validation.json" 2>&1 | tail -8
echo "link-health-summary exit=${PIPESTATUS[0]}"
```

Positive control:

```bash
#!/usr/bin/env bash
# Positive control for experiment 4: same extractor, flat src/posts.
WT=/tmp/claude-worktrees/da2f7ebc-4212eac9bf09
S=<scratch>
cd "$WT" || exit 2
echo "=== control: same extractor, flat src/posts"
uv run python scripts/link-validation/link-extractor.py --posts-dir src/posts --output "$S/exp4/links-flat.json" 2>&1 | grep -E "Extracted"
echo "link-extractor exit=${PIPESTATUS[0]}"
```

Output:

```text
HEAD fc0c1eb3cdb251e295fb5c908122e07892358839  date 2026-10-01T04:47:31Z
posts copied into nested dir: 97
INFO: ✅ Extracted 0 links from 0 files
INFO: 📊 By type: {}
INFO: 💾 Results saved to <scratch>/exp4/links.json
link-extractor exit=0
links.json stats: {'total_files': 0, 'total_links': 0, 'by_type': {}, 'by_domain': {}}
INFO:   Needs manual review: 0
INFO:   Redirects: 0
INFO:   Timeouts: 0
INFO:   Errors: 0
simple-validator exit=0
Total links: 0
Internal broken: 0
External broken: 0 (advisory)
Overall: 0/0 (0.0%)
External failures: 0 (0.0% of all links)
link-health-summary exit=0
=== control: same extractor, flat src/posts
INFO: ✅ Extracted 1544 links from 97 files
link-extractor exit=0
```

### Experiment 5 — skipped required checks on merged commits (#644 item 4)

```bash
#!/usr/bin/env bash
# Verify #644 item 4: commits that merged with the four required checks reporting skipped.
cd /tmp/claude-worktrees/da2f7ebc-4212eac9bf09 || exit 2
for c in 3cfaf5f 336f1a4 9588210; do
  full=$(git rev-parse "$c")
  echo "== $c $(git log -1 --format=%s "$c")"
  gh api "repos/williamzujkowski/williamzujkowski.github.io/commits/$full/check-runs?per_page=100" \
    --jq '.check_runs[] | select(.name|test("^(remarque|axe|check-lint|pytest|changes)$")) | "\(.name) \(.conclusion)"' | sort -u
done
echo "== branch protection required contexts"
gh api repos/williamzujkowski/williamzujkowski.github.io/branches/main/protection --jq '{c:.required_status_checks.contexts, strict:.required_status_checks.strict}'
```

Output:

```text
== 3cfaf5f docs: keep new research labs in dedicated reproducible repository (#627)
axe skipped
changes success
check-lint skipped
pytest skipped
remarque skipped
== 336f1a4 Prioritize research proposals with evidence and publication gates (#626)
axe skipped
changes success
check-lint skipped
pytest skipped
remarque skipped
== 9588210 Scope link monitor write permissions to its job (#617)
axe skipped
changes success
check-lint skipped
pytest skipped
remarque skipped
== branch protection required contexts
{"c":["remarque","axe","check-lint","pytest"],"strict":true}
```

### Other commands

```bash
rg -o 'font-size\s*:\s*var\(--text-[\w-]+' astro-site/src | wc -l      # 53
rg -o 'font-size\s*:\s*var\(--text-micro' astro-site/src | wc -l       # 12
grep -n forbidOnly astro-site/playwright.config.ts                       # no match
curl -s https://api.crossref.org/works/<doi>                              # S1, S2, S3 identity
curl -s 'https://export.arxiv.org/api/query?id_list=2608.09567'          # S7 identity
pdftotext google.pdf / jia.pdf / arxiv.pdf; grep for quoted sentences     # S1, S3, S7 text
# Render check: astro preview on :4399 + Playwright screenshots of .flow and table at
# 375x900 and 1280x1000, colorScheme light/dark; scrollWidth == viewport width in all four.
```
