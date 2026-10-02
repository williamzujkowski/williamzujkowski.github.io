# Research note: approving the command approves what it runs

**Post:** `src/posts/2026-11-12-approving-the-command-approves-what-it-runs.md` (slot 2026-11-12, `draft: false`)
**Proposal:** issue #673. **Researched:** 2026-10-01 (UTC 2026-10-02).
**Lab:** research-labs branch `lab/approval-scope`, commits `548b232` (lab) and `ce11f7d`
(evidence). Not pushed. The post links `RESEARCH_LABS_COMMIT`, which root replaces with the
merged commit.

## Question and thesis

What does an approval or permission rule for an agent's shell command actually authorize: the
command line, or everything it transitively runs and writes? Thesis: a rule such as
`Bash(npm install *)` matches command text (by documented design), while the install starts
lifecycle scripts from the project and its dependencies, writes inside and outside the project,
and can plant a hook that a later, separately approved `git commit` runs. The sandbox is the layer
that sees those child processes, and it constrains where effects land, not whether code runs.

Falsifier (from #673): the harness's permission or sandbox layer demonstrably constrains or
surfaces the transitive effects in every tested case. Result: not met. The permission layer does
neither by design. sandbox-runtime denied the outside-project write and the `.git/hooks` write but
allowed in-project writes and every script's execution. npm's default output did not name the
dependency's script.

## Sources (all accessed 2026-10-01/02 UTC)

| Source | Version / locator |
| --- | --- |
| Zhang, Xia, Wu, Yue, Zhang, Cheng, Tu, *Agent Approval Laundering: Transitive Effects Beyond the Approved Invocation* | arXiv 2609.28586v1, submitted 2026-09-23, preprint (cs.CR). Read in full: https://arxiv.org/html/2609.28586v1 (abstract, §I, §II-A/B, §III-A/B, §VI-E, §VII, §VIII, ethics). No public artifact (stated in "Attribution and release"). |
| Khan, *Stop Means Stop: Measuring and Repairing the Enforcement Gap in Agent-Framework Control Primitives* | arXiv 2607.14166v3 (v1 2026-07-15, v2 2026-07-17, v3 2026-08-08), preprint, independent author. PDF read: abstract, §1, Table 3, framework identities (FW-A = LangGraph 1.2.7). Artifact `sajjadanwar0/soundgate-paper`: public, MIT, created 2026-07-08, pushed 2026-10-02 (`gh api`). |
| Claude Code docs, Permissions | https://code.claude.com/docs/en/permissions (fetched as `.md`): "What a Bash rule doesn't match" (#bash-rule-limits), wildcard patterns, Read/Edit deny scope, "How permissions interact with sandboxing" |
| Claude Code docs, Sandboxing | https://code.claude.com/docs/en/sandboxing: "What the sandbox restricts" table, "What runs outside the sandbox", fail-open warning + `failIfUnavailable`, Protected paths |
| `@anthropic-ai/sandbox-runtime` | npm 0.0.78 (lockfile-pinned); repo `anthropics/sandbox-runtime` (Apache-2.0); `src/sandbox/sandbox-utils.ts` (DANGEROUS_FILES/DIRECTORIES, hooks/config in .git), `src/sandbox/linux-sandbox-utils.ts` (`enableWeakerNestedSandbox` binds `/proc`), README security notes |
| npm docs | npm/cli tag v10.9.8: `docs/lib/content/using-npm/scripts.md` (lifecycle for `npm install`/`npm ci`; `binding.gyp` default), `workspaces/config/lib/definitions/definitions.js` (`foreground-scripts`, `ignore-scripts`), `docs/lib/content/commands/npm-query.md` (`:attr`). Rendered at docs.npmjs.com/cli/v10/... (quotes re-verified there). |
| pnpm v10.0.0 release notes | https://github.com/pnpm/pnpm/releases/tag/v10.0.0 ("Lifecycle scripts of dependencies are not executed during installation by default") |
| git githooks | https://git-scm.com/docs/githooks (`--no-verify` for pre-commit and commit-msg; prepare-commit-msg "is not suppressed by the --no-verify option") |

Considered and excluded: the scalex.dev approval-game miss rates listed in #673 (directional,
methodology disputed); not needed for the thesis, not re-fetched, not cited.

## Claim ledger

| Proposed claim | Kind | Evidence and locator | Scope/caveat | Status |
| --- | --- | --- | --- | --- |
| `npm install` started 3 lifecycle scripts; markers inside and outside the project; hook written; `git commit` ran it | our observation | `plain.json` arm `npm-install` (lifecycleScripts, markersInside/Outside, preCommitHookPresent, commit.hookRan) | one fixture, npm 10.9.8 | verified |
| npm's output named 2 of 3 scripts; dependency's script unnamed | our observation | `npm-install`/`npm-ci` `output.scriptsShown` (2 entries); tail shows `added 1 package in Ns` | default npm settings | verified |
| `--foreground-scripts` names all 3 | our observation | arm `npm-install-foreground-scripts` scriptsShown = 3 | | verified |
| pnpm 10 skipped dependency script, warned; root postinstall/prepare ran | our observation + source | arm `pnpm-install` (2 scripts, `pnpmIgnoredBuildsWarning: true`); pnpm v10.0.0 notes | pnpm 10.33.0 | verified |
| Allowlisting the dependency runs 3, names 3 | our observation | arm `pnpm-install-dep-allowed` (`onlyBuiltDependencies` in pnpm-workspace.yaml) | | verified |
| Controls: `--ignore-scripts` for npm install/ci and pnpm: 0 scripts, 0 markers, no hook | our observation | three control arms; harness guard requires exit 0, traced, >0 processes | | verified |
| Under srt: all scripts ran, inside markers written, outside marker and hook EROFS, commit ran nothing | our observation | `sandbox.json` arms `npm-install`, `pnpm-install` notableMutations | srt run directly, weaker nested mode, relaxed container seccomp/AppArmor | verified |
| srt without user namespaces exits non-zero and runs nothing | our observation | `plain.json` `sandboxUnavailable` (exit 1, 0 processes) + test 8 | hardened container | verified |
| Rule "matches the command text Claude writes"; "isn't a security boundary around the program" | source finding | Permissions #bash-rule-limits | | verified (quote re-fetched) |
| Read/Edit deny rules don't cover "arbitrary subprocesses … like a Python or Node script that opens files itself" | source finding | Permissions, Read/Edit section | | verified |
| Trailing ` *` matches bare command; `*` stands in for any text | source finding | Permissions, Wildcard patterns | `npm install <pkg>` coverage is inference from the documented grammar | verified |
| Sandbox applies to commands "and the processes they start"; default writes = working dir + temp; `.git` hooks/config protected; off by default; falls back unsandboxed unless `failIfUnavailable` | source finding | Sandboxing doc | | verified |
| `autoAllowBashIfSandboxed` default true; "the sandbox boundary substitutes for that whole-tool prompt"; content-scoped ask rules still prompt | source finding | Permissions, "How permissions interact with sandboxing" | | verified |
| Claude Code builds the sandbox on sandbox-runtime | source finding | Sandboxing doc | | verified |
| `foreground-scripts` quote; `npm install`/`npm ci` lifecycle lists; `binding.gyp` → `node-gyp rebuild` default | source finding | npm v10.9.8 docs/definitions | | verified |
| Approval laundering definition quote | source finding | 2609.28586v1 full-text abstract. NOTE: the arXiv *abs page* abstract words it differently ("names the entry invocation but omits effects exercised by its workflow"); the post quotes the full text and links the HTML. | | verified |
| Vite case: `pnpm --dir <fixed-sha-workspace> install --frozen-lockfile`, postinstall (simple-git-hooks per transcript), wrote `node_modules/.modules.yaml` | source finding | 2609.28586v1 §II-A | pnpm 10.34.3 at vite@64dfee12 | verified |
| 111 pairs; residual records 40 → 17 → 13 (13 "when post hoc analysis adds metadata available at decision time") | source finding | 2609.28586v1 abstract and §I | #673 says "n=17 residual workflows"; the paper's 17 is residual *records* under command semantics (of 111) and separately the 17-workflow holdout | verified |
| Disclosed to Anthropic, GitHub, Alibaba; no artifact | source finding | 2609.28586v1 Ethics: Responsible disclosure; Attribution and release | | verified |
| Proposed fix binds predicted effects pre-decision; Claude Code PreToolUse integration | source finding | 2609.28586v1 §VI-E, §VII | Claude Code 2.1.205 in the paper | verified |
| Sibling leak in every framework with a pre-execution gate, 5 of 6 | source finding | 2607.14166v3 abstract | not reproduced here | verified |
| LangGraph sweep: same superstep 577/577, later 0/331 | source finding | 2607.14166v3 Table 3 (1,000 seeded workflows on FW-A) | | verified |
| "Whether any individual gap is a bug or a deliberate design is for maintainers to say" | source finding | 2607.14166v3 §1 | | verified |
| `--no-verify` bypasses pre-commit | source finding | githooks | | verified |
| Inventory snippet returns project + `node_modules/canary-dep`; trace snippet prints exactly 3 scripts | our observation | scratch `snippet.sh` run in the lab image (see Commands) | used `--offline` flags in the container | verified |
| The project is what you run next (node_modules, build scripts) | inference | from documented in-workspace write allowance | labelled as consequence, not measured | inference |
| Sandbox-as-boundary is "the right trade" for this problem | opinion | | | opinion |

## Commands run

Lab (from the research-labs worktree, clean tree at `548b232`, `dirty=false` in both records):

```sh
./scripts/approval-lab.sh test      > results/test.txt     # 8/8 pass
./scripts/approval-lab.sh run       > results/plain.json
./scripts/approval-lab.sh sandbox   > results/sandbox.json
```

Retained at `docs/evidence/approval-scope-2026-10-01/` (commit `ce11f7d`). Image id
`sha256:76d7355d8e1c…` (rebuilt locally; base image and packages pinned). Environment recorded in
each JSON: node v22.23.2, npm 10.9.8, pnpm 10.33.0, git 2.39.5, strace 6.1, bubblewrap 0.8.0,
sandbox-runtime 0.0.78.

Control-first: the first full matrix exposed that the sandbox-mode control "passed" while srt was
refusing to start (srt parsed strace's `-s 4096` as its own `--settings`). Fixed with `--` and a
guard that a control must exit 0, be traced and start >0 processes. A second false start: an
earlier `pnpm ignored-builds` inventory printed "Cannot identify as no node_modules found" after an
`--ignore-scripts` install; dropped rather than interpreted.

Mutation checks (host copy, parser tests only): changing the `sh -c` detector to `-x`, removing the
`EEXIST` filter, and deleting the `.git/hooks` classification each turned a test red. A first
attempted mutation (guarding only the exact `.git/hooks` path) was ineffective because the prefix
branch still matched; recorded, replaced.

Snippet verification: scratch `snippet.sh` run in the lab image (`--network none`, nonroot, caps
dropped) with `--offline --no-audit --no-fund` added to the npm calls. The first trace grep printed
each script 8–10 times (failed `PATH` lookups); the `= 0$` filter in the post fixes that.

Site: `pnpm install --frozen-lockfile`; `PUBLICATION_AS_OF=2026-11-12T00:00:00Z pnpm build` (exit
0); `pnpm run audit` (exit 0); `pnpm test:unit` (62 pass); `internal-link-check.py` (all resolve).
Playwright render at 390px light/dark and 1280px: a first build overflowed by 5px on mobile from
an unbreakable `.git/hooks/pre-commit` label in the `.flow` and a five-column table; both fixed,
no overflow after.

## Limitations

- One fixture, one dependency, one hook pattern; npm 10.9.8 / pnpm 10.33.0 / Node 22 / git 2.39.5;
  linux/amd64; no network, so network effects are untested.
- sandbox-runtime run directly, not Claude Code. Inside Docker it needs relaxed seccomp/AppArmor
  and `enableWeakerNestedSandbox` (binds `/proc`). Filesystem write rules are the measured
  property; process isolation is not assessed.
- No agent, model or Claude Code binary ran. Prompt contents and what Claude Code records are
  documented semantics, not observations.
- Payloads catch their own errors; a real hook manager would fail the install under the sandbox.
- Stop Means Stop's sibling leak is cited, not reproduced.

## Overlap check

`rg -i "ignore-scripts|postinstall|onlyBuiltDependencies|install script|lifecycle|preinstall"` over
`src/posts` and `docs/shelved-drafts`: no post covers install scripts or approval scope (the
2026-10-15 provenance post mentions installing with scripts disabled, in passing).
`gh issue list --state all --search "approval OR postinstall OR ignore-scripts OR lifecycle"`:
only #673 itself and unrelated issues. Related, cross-linked: 2026-07-23 (deferred human-approval
gates), 2026-07-02 (sandbox survey), 2026-10-15 (provenance). All publish before 2026-11-12.

## Layer-1 coverage

| Stage | Status | Evidence |
| --- | --- | --- |
| blog-overlap | completed | Above; no strong overlap; three moderate cross-links added, all earlier than the slot. |
| blog-factcheck | completed | Every quote re-fetched by script (`factcheck.py` in scratch): 22/24 matched as-is; one normalisation miss confirmed present by direct grep; the 2609.28586 quote is in the full text, not the abs page, so the link now points at the HTML. Fixes: removed "years ahead of most of us" (unsupported), "has been there for years" → "an ordinary documented setting", "post hoc" restored to the 40→17→13 sentence, `.modules.yaml` no longer attributed to the postinstall, "tests plant defects" corrected to hand-planted mutations, "five of six" scoped to frameworks with a pre-execution gate. |
| blog-llm-tells | manual | Read for filler, hedging, stock contrasts, triads, em dashes (none in prose), closing summaries. One "where, not whether" contrast kept as the thesis line; one triad in the "what you run next" list kept as a literal list. |
| blog-nda-check | completed | No employer or work context; first person limited to running the public lab; no reference to the excluded repositories or any agency. |
| blog-argument-shape | completed | Experiment report with a position. Thesis: L18 + "constrains where effects land, not whether code runs". Strongest objection (install scripts are old news) answered in "Old news, new button". Falsifier stated and answered in Limits. Close follows from the body. |
| blog-visuals | completed | One `.flow` (role/aria-label, tokens via classes) and one 4-column table; rendered 390px light/dark and 1280px light, no overflow after fixes. Doodle left as `<!-- DOODLE: ... -->` for root. |
| blog-artifact-check | completed | Every flag and key in the post was run in the lab or checked against versioned docs/source: `--ignore-scripts`, `--foreground-scripts`, `npm query :attr`, `strace` snippet, `onlyBuiltDependencies` (run); `failIfUnavailable`, `autoAllowBashIfSandboxed`, `enableWeakerNestedSandbox`, exact-match `Bash(...)` rule grammar, `--no-verify` (docs/source). Lab link is a placeholder for root. |

No independent (second-agent) review was run; root review pending.

## Independent review (root, 2026-10-02): HOLD, then revised

Root re-ran the lab (8/8; plain and sandbox arms matched the retained JSON; a planted
script-running control made the harness exit 3; a detector mutation went red; both snippets
found the 3 scripts) and verified sources. Items, each checked before applying:

| # | Finding | Verification | Outcome |
| --- | --- | --- | --- |
| 1 | Blocker: a privately held topic leaked via a hook-directory config mention | `rg -i` over post, note and lab | Removed from post (now "look in `.git/hooks`"), note (two places) and lab comment; re-grep zero hits in all three trees |
| 3 | Fail-open sentence unfair: docs scope the fallback to a missing dependency/unsupported platform; troubleshooting says an unprivileged container fails with a `bwrap` error | Sandboxing doc, Troubleshooting ("sandboxed commands fail with a `bwrap` error such as `Can't mount proc…`") | Applied suggested wording |
| 4 | Weakened-mode caveat buried in Limits | sandbox-runtime README: "This option considerably weakens security" (the README, not the Claude Code docs) | Added to the sandbox paragraph, attributed to the runtime's README |
| 5 | Falsifier paragraph overstated | — | Now "sandbox-runtime, run standalone"; permission layer stated as judged from documentation, not tested, though #673 proposed a real harness |
| 6 | `--no-verify` advice incomplete | githooks: pre-commit and commit-msg "can be bypassed with the --no-verify option"; prepare-commit-msg "is not suppressed"; post-commit has no bypass | Applied |
| 7 | strace default string limit | strace default `-s` is 32 | Added `-s 4096` |
| 8 | "Real hook managers fail loudly" untested | — | Now "may fail or warn" |
| 9 | pnpm quote ends in "!" | release notes | Quote now stops before the punctuation |
| 10 | Docs say "a per-user temp directory"; lab allowed all of `/tmp` | Sandboxing doc; `run.mjs` settings | Quoted the docs and stated the lab's wider setting |
| A | `[^"]*` truncates at strace's escaped `\"` | Demonstrated: a benign `preinstall` with escaped quotes; naive grep printed `"node -e \"`, escape-aware `grep -oE '"-c", "([^"\\]|\\.)*"'` printed it whole (`snippet-check.txt`, lab `ce11f7d`) | Applied |
| B | `npm query` covered 4 of 7 install-time scripts | npm v10.9.8 scripts page: preinstall, install, postinstall, prepublish, preprepare, prepare, postprepare | Query widened in post and lab (`548b232`); re-run in the lab image, same result on the fixture |
| C | Reused the Oct 15 post's thesis phrase | — | Now cited as that post's title |

Lab history rewritten (unpushed) so no commit contains the removed topic: one lab commit `548b232` on origin/main `d34cb74`, evidence `ce11f7d`; `git log -p origin/main..HEAD | grep -ci -E` for the two terms returns 0. Re-run at `548b232` from a clean tree: 8/8 tests; every observation identical to the
first (pre-review) run (diffed summaries). Site rebuilt at `PUBLICATION_AS_OF=2026-11-12T00:00:00Z`;
`pnpm run audit` passed. `RESEARCH_LABS_COMMIT` and the DOODLE comment left for root.
