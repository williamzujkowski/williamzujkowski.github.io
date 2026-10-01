# Research note: Dependabot loses a pnpm override two ways

**Post:** `src/posts/2026-11-05-dependabot-pnpm-overrides-two-ways.md` (slot 2026-11-05, `draft: false`)
**Researched:** 2026-10-01. **Lab:** research-labs branch `lab/pnpm-override-drift`
(commits `c807b5d` lab, `2185517` evidence); the post links `RESEARCH_LABS_COMMIT`, which root replaces.

## Question and thesis

Does a pnpm override survive the lockfiles Dependabot writes, and which cheap checks notice
when it doesn't? Thesis: an override is a security control stored in a file a bot
regenerates; check the resolved edge it governs, not the presence of the override line.
Falsifier: a bot lockfile that drops the header but keeps the overridden edge (the silent half
would then be absent), or a header-only repair that pnpm's frozen install rejects (the
"loud half protects you" claim would be wrong).

## Sources (all accessed 2026-10-01)

| Source | Version / locator |
| --- | --- |
| GitHub Advisory GHSA-px8p-9vwx-vf98 / CVE-2026-45820, "fflate unzipSync can enter an infinite loop when parsing malformed ZIP64 archives" | `gh api /advisories/GHSA-px8p-9vwx-vf98`; published 2026-07-22, updated 2026-09-03, not withdrawn. npm ranges include `>= 0.7.0, < 0.7.5` (patched 0.7.5). GitHub severity "medium"; CVSS 3.1 7.5 (`AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H`); CVSS 4.0 6.6. |
| dependabot/dependabot-core#16232, "pnpm update drops existing overrides metadata and reverts parent-scoped dependency resolution" (author williamzujkowski) | Opened 2026-09-09; state OPEN, 0 comments, labels `L: github:actions`, `L: javascript` at access. |
| pnpm docs, settings → overrides (10.x) | https://pnpm.io/10.x/settings#overrides ; raw `pnpm/pnpm.io` `versioned_docs/version-10.x/settings.md` at commit `0abfe79` (2026-09-26). Selector examples `bar@^2.1.0`, `qar@1>zoo`. |
| pnpm docs, `pnpm install --frozen-lockfile` (10.x) | https://pnpm.io/10.x/cli/install#--frozen-lockfile : "fails to install if the lockfile is out of sync with the manifest / an update is needed or no lockfile is present". |
| pnpm docs, `pnpm dedupe --check` (10.x) | https://pnpm.io/10.x/cli/dedupe : "Exits with a non-zero status code if changes are possible." |
| pnpm source v10.33.0 | `hooks/read-package-hook/src/createVersionsOverrider.ts` (parent selector: `semver.satisfies(manifest.version, parentPkg.bareSpecifier)`; target selector via `isIntersectingRange(targetPkg.bareSpecifier, bareSpecifier)`), `isIntersectingRange.ts` (`semver.intersects`). |
| npm registry `fast-uri` time | https://registry.npmjs.org/fast-uri : 3.1.6 2026-08-23, 3.1.7 2026-09-02T11:06Z, 3.1.8 2026-09-15. |
| npm registry manifests | `satori@0.33.4` and `@0.33.5` depend on `fflate: 0.7.3` (exact); `@shuding/opentype.js@1.4.0-beta.0` depends on `fflate: ^0.7.3`; `ajv@8.x` on `fast-uri: ^3.0.1`. |
| Repo issue #540 (body + 3 comments), #563; PRs #533, #537, #564, #635, #638, #639/commit `38e324bf`, #662 and its check-lint job 109539204570 log | `gh issue view`, `gh pr view`, `gh api .../actions/jobs/109539204570/logs`. |
| `docs/research/2026-09-08-refactor-review.md` row #564/#540 | In-repo. |

## Claim ledger

| Claim in post | Kind | Evidence | Scope / caveat | Status |
| --- | --- | --- | --- | --- |
| Satori pins fflate exactly 0.7.3; 0.7.3 is affected | source | npm manifests; advisory range `>=0.7.0,<0.7.5` | 0.33.4 and 0.33.5 | verified |
| Satori imports `inflateSync`, not `unzipSync`; build-time only on repo fonts | source + observation | #563 body; scratch install of satori 0.33.4 `dist/index.js` imports `{inflateSync}` from "fflate"; opentype.js also only `inflateSync` | static import inspection, not a reachability proof | verified |
| Advisory CVSS 3.1 score 7.5 | source | advisory API `cvss_severities.cvss_v3.score` | GitHub label "medium"; v4 6.6 | verified |
| Five site checks fail in under thirty seconds with ERR_PNPM_LOCKFILE_CONFIG_MISMATCH | repo record | #540 body: 8–17s (#532, #537); #540 comment: 13–21s (#638); #662 run: five failed jobs 7–28s incl. compliance-check 28s | range across PRs 7–28s | verified |
| First diagnosis (#533 duplicate block) wrong; #537 opened 3m43s after merge | repo record | #533 merged 2026-09-04T05:19:11Z; #537 created 05:22:54Z = 3m43s; #540 "That was wrong" | — | verified |
| Override added Sept 8 | repo record | `git log -S'satori>fflate'` → `2ba4e8a` 2026-09-08 (#562); #563 | — | verified |
| Four bot lockfiles since; all lack header and have satori→0.7.3, opentype→0.7.5 | our observation | `git show` of d0160c5, origin/pr635 (47e1fd7), pr638 (477fd50), pr662 (74d64b1) lockfiles; `inspect.sh` | Only npm-ecosystem bot PRs touching astro-site after 2026-09-08; #565/#636/#663 are actions-only | verified |
| #540 cited fast-uri 3.1.7 as proof of override application; 3.1.7 was newest 3.x two days earlier | repo record + source | #540 body quote; registry time | "fresh resolution" hedge: an incremental update from main (also 3.1.7) gives the same answer | verified |
| Header-only lockfile: frozen install exit 0, satori linked to 0.7.3 | lab observation | `docs/evidence/pnpm-override-drift-2026-10-01.json` (revision c807b5d, image sha256:6e64e73e…) | pnpm 10.33.0, Node 22.23.2, toy manifest | verified |
| `--lockfile-only` leaves header-only unchanged; restores no-header | lab observation | same evidence, `lockfileOnlyRegeneration` | with metadata cached at build | verified |
| `dedupe --check` fails both bad files in lab, and fails on site `main` | lab + scratch | lab evidence; scratch `repo-check.sh` on main lockfile listed vite 8.1.5→8.2.2 among others | scratch run used network, pnpm 10.33.0 | verified |
| `fflate@0.7.5 present` check passes all three | lab | static checks in evidence | — | verified |
| check script asserts header + parent edge; stdlib-only; caught #662 with both messages | repo record | script source; job log lines 185–187 | — | verified |
| `pnpm install --lockfile-only` is the printed fix and works when header missing | repo + lab | script `FIX_COMMAND`; lab | — | verified |
| 9 of 10 overrides inert: uuid/dompurify absent; 7 already satisfied | repo record | commit 38e324bf message, #540 comment table; pre-#639 lockfile has 0 uuid/dompurify entries | measured by the repo on 2026-09-24; not re-measured here | verified (attributed) |
| Version-selector overrides match declared ranges by intersection; parent selector by `satisfies` | source | pnpm v10.33.0 source files | docs text itself only gives examples | verified |
| Commit quote "the surface the bot can silently re-resolve from 10 pins to 1" | repo record | 38e324bf message | — | verified |
| Upstream #16232 open, no replies on Oct 1; updater version unknown | source | `gh issue view` | — | verified |

## Commands run (abridged; scripts retained in session scratch `post6/`)

- `gh issue view 540|563`, `gh pr view 533|537`, `gh pr list --author app/dependabot --state all --limit 200`, `gh pr checks 662`, job log fetch, `gh issue view 16232 -R dependabot/dependabot-core`, `gh search issues --repo dependabot/dependabot-core "pnpm override"`.
- `git fetch origin pull/{537,564,635,638,662}/head`, `git show <ref>:astro-site/pnpm-lock.yaml`, awk extraction of `satori@` and `@shuding/opentype.js@` snapshot edges.
- Scratch prototype (network, `npx pnpm@10.33.0`): `install --lockfile-only`, `--frozen-lockfile`, `why fflate`, `audit --prod`, `dedupe --check`, `install --fix-lockfile`, `dedupe`.
- Lab: `./scripts/pnpm-lab.sh test` (4/4 pass) and `./scripts/pnpm-lab.sh run` at clean revision c807b5d.
- Site: `pnpm install --frozen-lockfile`; `PUBLICATION_AS_OF=2026-11-05T00:00:00Z pnpm build` (exit 0); `pnpm run audit` (exit 0; 2 baselined zine.css false positives); Playwright screenshots of the `.flow` and table at 390px light/dark and 1280px light, no horizontal overflow.

## Observations not used in the post (retained for honesty)

- Scratch: `pnpm audit --prod` flagged GHSA-px8p-9vwx-vf98 at path `.>satori>fflate` on both bad lockfiles. Useful but advisory-dependent and network-bound; omitted to keep the post on checks that work for any override.
- Scratch: on the header-only lockfile, `pnpm install --fix-lockfile` and `pnpm dedupe` restored satori→0.7.5; plain `pnpm install` and `install --lockfile-only --force` did not. Not in the lab, so not claimed.
- A fresh no-override resolution (not incremental) dedupes opentype.js to 0.7.3 too, so the presence check would fail there. The incremental simulation matches the real bot files; the fresh one does not.
- Issue #540 was closed 2026-09-24 although commit 38e324bf says it does not close it. The post does not characterise #540's state.

## Limitations

The lab simulates the bot's lockfile shape; it does not run Dependabot. One manifest, one
parent-scoped override, pnpm 10.33.0 (site CI uses `version: 10`, currently 10.34.x locally).
Registry metadata for re-resolution is captured at image build, so `dedupe --check` and
regeneration results can change as the registry changes. Bare (global) overrides were not
tested against the bot. Reachability of `unzipSync` is not demonstrated either way beyond
static import inspection.

## Overlap check

`rg -i "dependabot|pnpm|lockfile|overrides" src/posts docs/shelved-drafts`; `gh issue list --state all --search "override" / "dependabot pnpm" / "blog lockfile"`.
Candidates: `2026-05-07-patch-fast-pull-slow-defending-copy-fail-shai-hulud` (moderate:
lockfiles + frozen installs + Renovate cooldowns; different question; cross-linked in the
close), `2025-10-06-automated-security-scanning-pipeline` (weak: scanner gates),
`2026-04-16-repo-health-report…` (weak: mentions Dependabot as a checkbox). No shelved draft
or issue proposes this post. Issues #540/#563/#639 are the source record, not prior posts.

## Layer-1 coverage

| Stage | Status | Evidence |
| --- | --- | --- |
| blog-overlap | completed | Above; one moderate candidate, cross-linked (published 2026-05-07, before slot). |
| blog-factcheck | completed | 17 ledger claims verified; fixes applied: "under twenty seconds" → "in under thirty seconds" (#662 compliance-check took 28s); "any resolution" → "a fresh resolution"; selector paragraph rewritten after the pnpm source contradicted my first draft ("matches only a resolution below 2.8.3" was wrong: matching is on the declared range by intersection); removed an invented claim that the commit "named the trade"; "lab's copy" → scratch install. |
| blog-llm-tells | manual | Read for filler, hedging, stock contrasts, three-item lists, em dashes (none in prose). Removed a repeated "It just…" construction and a redundant closing sentence. |
| blog-nda-check | completed | All first-person claims trace to this repo's issues/PRs/commits; no employer or work context; homelab/site attribution only. |
| blog-argument-shape | completed | Experiment report + position. Thesis in close (L~105). Strongest objection — the vuln was unreachable — is stated up front; the scope paragraph limits to one repo, one override shape, lab-not-bot. Disconfirmer: a header-only repair that frozen install rejects. |
| blog-visuals | completed (doodle pending) | One `.flow` (role/aria present, tokens via classes), one Markdown table; rendered at 390px light/dark and 1280px, no overflow. Doodle left as `<!-- DOODLE: … -->` for root. |
| blog-artifact-check | completed | Commands/flags checked against pnpm 10.x docs and run in the lab (`--frozen-lockfile`, `--lockfile-only`, `dedupe --check`); check-script behaviour checked against its source and the #662 job log; lab link is a placeholder for root. |

## Independent review (root, 2026-10-01): HOLD, then revised

The reviewer re-ran the lab (4/4) and reproduced the header-only result. They also confirmed the
advisory, the satori imports, the pnpm source lines, the fast-uri timing and #16232. I
verified each finding before editing:

| # | Finding | Verification | Action |
| --- | --- | --- | --- |
| 3 | "Every Dependabot PR" false before late August | Bot commits 34666fb (#446), cf6d5bf (#482), 40b6f70 (#523), cca617d (#524, 2026-08-23) all contain `overrides:`; 994335d (#530, 2026-08-25) does not. `git diff cca617d~1 8d50a67` on package.json/dependabot.yml shows only dependency-version changes. #530 failed the same five checks (9–25s). | Reworded to "From August 25 on", plus an onset paragraph. |
| 4 | Six bot commits, not four | #638 commits 477fd50, ddb4c95, c1c4545 (force-pushes 2026-09-24T04:19/04:24Z, after #639 merged at 04:08Z); all three lack the header and have satori→0.7.3. | Fixed: six lockfiles across four PRs. |
| 5 | "The fix it prints is the one that works" overclaims | Lab row: `--lockfile-only` leaves header-only unchanged. The script docstring said "the fix in every case is the same". It also said "the frozen install behind it still refuses", which is false for header-only, and asserted an unsourced code path ("rewrites … rather than shelling out to pnpm"). | Added a caveat and the remedy to the post. Edited the script docstring and failure hint; `pytest scripts/ci/tests/test_lockfile_overrides.py`: 18 passed; ruff clean. Restarting from the untouched bot lockfile is lab-tested. Restarting from `main`'s lockfile is ordinary pnpm re-resolution but untested here. |
| 6 | Timing wording | #662 failed jobs ran 7–28s and #530's 9–25s; Trivy, Socket and security-scan passed. I did not re-derive the reviewer's 39–69s commit-to-red figure and did not use it. | "each within thirty seconds of starting"; "fails every check that installs dependencies". |
| 7 | Prior art #13036 | Opened 2025-09-08, still open; `injectWorkspacePackages` removed from lockfile settings; quotes ERR_PNPM_LOCKFILE_CONFIG_MISMATCH. | Cited in the loud-half section. |
| 8 | GitHub severity medium, CVSS 4.0 6.6 | Advisory API. | Added. |
| 9 | fast-uri `^3.1.6` is a range | Pre-#639 lockfile header. | "floors or ranges". |
| 10 | Truncated check-output quote | Job log line 187. | Completed. |
| 12 | Why not `pnpm audit --prod` | Scratch run flagged `.>satori>fflate`. | Added a one-paragraph answer. |
| 13 | Voice flat | n/a | Added two observations ("the best kind of vulnerability to lose control of"; the wet-paint sign) and the onset line. |

External review (agy, Gemini 3.1 Pro): "lost it in two ways" clarified as two losses in the same bot lockfile (header and resolved edge). Kept "at least the override's version": the script compares against the override's floor, which is what this repository's one override is.
