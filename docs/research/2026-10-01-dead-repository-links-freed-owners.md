# Research note: dead declared repository links and freed GitHub owners

**Post:** `src/posts/2026-11-05-dead-repository-links-freed-owners.md` (slot 2026-11-05, `draft: false`)
**Written:** 2026-10-01. **Kind:** reading/analysis post over an existing, already-merged
measurement in William's public `dependency-risk-profiler` repo. No new experiment was
run, and no third party was probed for this post (see "Lab" below).

## Evidence base (primary, William's own repo)

All pinned to merge commit `b3fe6e5fe1fba59d2c6d8f5ef92456f252d23fd2` (PR #429, merged
2026-08-13T01:32:50Z) of https://github.com/williamzujkowski/dependency-risk-profiler (public).

| Artifact | What it supplies |
|---|---|
| `docs/dangling-links-protocol.md` | Pre-registration: claim, ≥10% threshold, three falsification lines, the ethics line ("A count of freed namespaces is a defensive measurement; a list of claimable ones is a target list.") |
| `docs/dangling-links-result.md` | Result prose, compounded 3.2%, first-run guard narrative |
| `research/results/dangling-links.json` | **Raw aggregates**: auth-failing links npm 40 / packagist 10 / pypi 31 / rubygems 39; distinct_owners 118; checked 118; errors 0; owner_missing 25; owner_exists 93 |
| `research/cross_ecosystem/dangling.py` | Method: one `GET https://api.github.com/users/<owner>` per de-duplicated owner; 404 → missing, 200 → exists, else error; owners `sorted()` then mapped over a 6-worker pool; token from `GH_TOKEN`; output aggregates only |
| `research/results/cross-ecosystem-clone-yield.json` | Stage-two per-ecosystem reasons, independently showing the same auth counts (40/10/31/39 of 200); on-GitHub counts 190/190/193/196 |
| `research/results/cross-ecosystem-computability.json` | Stage-one sampling (1,000/ecosystem, seed 20260813) |
| `docs/cross-ecosystem-protocol.md`, `docs/cross-ecosystem-result.md` | Sampling frame (uniform from full name lists), 200-per-ecosystem clone subsample |
| PR #429 commits | `3abf017651` "docs: pre-register…" at 2026-08-13T01:12:18Z precedes `bda6b1ad89` result at 01:28:14Z |
| `docs/what-this-tool-is.md` / README | 41.51% of declared weight computed from the self-declared repository URL |

The 59/118 first-run error count and the 20.3% partial figure exist **only** in the
result doc and PR #429 body; no raw artifact of the failed run is retained. 12/59 = 0.2034
is consistent with the stated 20.3%, but this is consistency, not verification.

## Recomputation (this session)

```
25/118                      = 0.2119   (Wilson 95%: 0.148–0.294)
40+10+31+39                 = 120 ; 120/800 = 0.150
npm 40/200=0.200 rubygems 39/200=0.195 pypi 31/200=0.155 packagist 10/200=0.050
npm+pypi+rubygems 110/600   = 0.183
0.150 * 25/118              = 0.0318  (the result doc's "≈3.2%")
link-level bound: 120 links, 118 owners ⇒ missing-owner links ∈ [25, 27] ⇒ 3.1%–3.4% of 800
12/59                       = 0.2034  (first-run partial figure; consistency only)
```

Note: the result doc's 3.2% multiplies a link-level rate by an owner-level rate. The post
states the link-level bound 25–27 of 800 (3.1–3.4%) instead, which needs no assumption.

Also checked: `GET /users/github` returns `"type": "Organization"`, so the users endpoint
covers organisations and an org owner is not misread as missing.

## External sources (fetched 2026-10-01)

| Source | Locator | Used for |
|---|---|---|
| GitHub Docs, "Username changes" | https://docs.github.com/en/account-and-profile/concepts/username-changes ; source `github/docs` `content/account-and-profile/concepts/username-changes.md` @ `10844e10c034b5e5d9b62793c3af9feb4b91de07`, lines 30, 40, 42 | old username "becomes available for anyone else to claim"; redirect overridden when new owner creates same-name repo |
| GitHub Docs, "Personal account reference" | https://docs.github.com/en/account-and-profile/reference/personal-account-reference ; source line 16 + reusable `data/reusables/accounts/delete-account-repo-namespace-retirement.md` @ same SHA | "available for anyone to use after 90 days"; deletion retirement rule |
| GitHub Docs reusable, rename retirement | `data/reusables/accounts/rename-account-repo-namespace-retirement.md` @ same SHA | current rule: Marketplace action, or >100 clones or >100 Actions uses in the week prior; retires `OLD-OWNER/REPOSITORY-NAME` |
| Ben Balter, "New tools for open source maintainers", GitHub Blog, 2018-04-18 (updated 2021-10-28) | https://github.blog/open-source/maintainers/new-tools-for-open-source-maintainers/ | original 100-clone rule; "To prevent developers from pulling down potentially unsafe packages…" |
| Ladisa, Plate, Martinez, Barais, "SoK: Taxonomy of Attacks on Open-Source Software Supply Chains", IEEE S&P 2023, arXiv:2204.04008 (v2, 2022-04-19) | PDF text: "(AV-501) Dangling Reference"; "Dangling references (re)uses resource identifiers of orphaned projects" | prior art naming |
| Goldman & Kadkoda, "GitHub Dataset Research Reveals Millions Potentially Vulnerable to RepoJacking", Aqua Nautilus, 2023-06-21 | https://www.aquasec.com/blog/github-dataset-research-reveals-millions-potentially-vulnerable-to-repojacking/ | GHTorrent June 2019; 1.25M sampled; 36,983 = 2.95% |
| Elad Rapoport, "Persistent Threat: New Exploit Puts Thousands of GitHub Repositories and Millions of Users at Risk", Checkmarx, 2023-09-12 | https://checkmarx.com/blog/persistent-threat-new-exploit-puts-thousands-of-github-repositories-and-millions-of-users-at-risk/ | two Checkmarx bypasses in 2022 + one disclosed 2023-03-01, fixed 2023-09-01; "over 4,000 packages … using renamed usernames and are at risk … in case a new bypass is found"; Packagist/Go/Swift |
| Denis Makrushin, "More than 1,000 GitHub repositories at risk: how to detect RepoJacking vulnerabilities", 2025-01-29 | https://makrushin.com/repojacking-github/ | signup-form availability check; "1,363 repositories associated with vulnerable accounts"; "986 unique accounts were eligible for re-registration" |
| OpenSSF Scorecard README + `cmd/package_managers.go` @ `c0c8dea5b436a74d730d35e679a6efa8b6303cf7` | README §"Using a Package manager"; go file L127–147 | `--npm` takes `repository.url`, trims `.git`/`git+`; "The package ecosystem flags are to find a GitHub repo only." |
| deps.dev API v3 docs | https://docs.deps.dev/api/v3/ | relationProvenance: SLSA_ATTESTATION, GO_ORIGIN, PYPI_PUBLISH_ATTESTATION, RUBYGEMS_PUBLISH_ATTESTATION, UNVERIFIED_METADATA |
| PyPI docs, Project metadata → Verified details | https://docs.pypi.org/project_metadata/ | Trusted Publisher URL verification; "URL verification occurs when release files are uploaded and is not repeated afterwards." |
| npm Docs, "Generating provenance statements" | https://docs.npmjs.com/generating-provenance-statements | "Ensure your package.json is configured with a public repository that matches (case-sensitive) where you are publishing with provenance from." |
| Packagist "About" | https://packagist.org/about | submission is by public repository URL; versions fetched from VCS tags |

Dropped: SecurityWeek/HackerNews/BleepingComputer secondary coverage (used only as leads).

## Claim ledger

| Proposed claim | Kind | Evidence and locator | Scope/caveat | Status |
|---|---|---|---|---|
| 25 of 118 distinct owners returned 404 | our observation (DRP) | dangling-links.json | snapshot mid-Aug 2026; owners de-duplicated | verified |
| ≈ a fifth; 95% CI ~15–29% | inference | Wilson recomputed | n=118 | verified |
| 120/800 declared links failed with auth; per-ecosystem 20.0/19.5/15.5/5.0% | our observation | dangling-links.json; clone-yield.json reasons | "declared" incl. a few non-GitHub links in the 200 | verified |
| 25–27 of 800 links (3.1–3.4%) point at a missing owner | inference | bound from 120 links / 118 owners | this draw only | verified |
| Protocol written before the run, ≥10% threshold | source finding (DRP) | protocol doc; PR #429 commit order | commit order shows ordering of commits, not of execution | partial (as documented by the repo) |
| First run 59/118 errors → inconclusive; surviving half would have said 20.3% | source finding (DRP) | result doc; PR #429 body | no raw artifact retained | partial |
| Lookups in roughly alphabetical order | our observation | dangling.py `sorted(...)` + pool map | concurrent workers ⇒ "roughly" | verified |
| 41.51% of DRP declared weight from repo URL | source finding (DRP) | what-this-tool-is.md table; README | DRP's scorer only | verified |
| GitHub rename/deletion/retirement rules | source finding | github/docs @ 10844e1 | current docs, not the rules on each owner's rename date | verified |
| Scorecard `--npm` uses `repository.url` verbatim (trimmed) | source finding | package_managers.go L127–147 | npm path shown; PyPI/RubyGems paths exist too | verified |
| deps.dev labels provenance incl. UNVERIFIED_METADATA | source finding | deps.dev API v3 doc | | verified |
| PyPI verification is upload-time only | source finding | docs.pypi.org | | verified |
| Packagist low rate because the link is load-bearing | hypothesis (DRP's explanation) | packagist.org/about supports mechanism | untested; labelled as such in post | partial |
| Prior-art figures (Aqua, Checkmarx, Makrushin, Ladisa) | source finding | as above | Checkmarx "4,000" is conditional on a future bypass; stated | verified |
| "Abstain when repo created after first release / manifest doesn't name package" | opinion | none | labelled "my suggestion, untested" | n/a |

## Commands run

- `cat`/Read of the DRP docs, script and JSON results listed above; `git log` on DRP; `gh pr view 429/428 -R williamzujkowski/dependency-risk-profiler`.
- `python3 -c` recomputation above.
- `gh api repos/github/docs/contents/...@10844e1`, `gh api repos/ossf/scorecard/contents/...@c0c8dea`.
- `curl` + text extraction for Aqua, Checkmarx, Makrushin, GitHub Blog, deps.dev, PyPI, npm, Packagist pages; arXiv API + PDF (`pdftotext`) for 2204.04008.
- One `curl https://api.github.com/users/github` (well-known org; checks endpoint semantics). No lookups of any sampled owner.

## Lab

Not applicable. The post reports an existing, merged measurement. Re-running it would mean
re-probing third-party accounts, which the brief excludes and adds nothing the retained
aggregates do not already show. No research-labs worktree was created.

## Limitations (carried into the post)

- Snapshot (mid-August 2026); namespaces churn continuously.
- 800 declared links, 118 owners; ±7 points on the conditional share.
- GitHub only; auth conflates private / renamed / deleted.
- 404 ≠ registerable; retirement rules and unpublished reservations unmeasured.
- Nothing about exploitation was measured.
- Minor upstream inconsistency: computability.json says npm declared 546, clone-yield.json says 543 "declared_in_stage_one" (re-probed in a later run). Does not affect any figure in the post.

## Overlap check

- `rg -il 'repojack|repo-jack|namespace retire|freed namespace|dangling' src/posts docs/shelved-drafts` → no hits.
- `rg -il 'repository field|declared repository|dependency-risk-profiler|deps\.dev|scorecard'` → `2026-04-16-repo-health-report-six-dimension-hygiene-scores.md` (repo hygiene scoring via GitHub API: weak, different question), `2026-04-18-nexus-agents-april…` (Scorecard score of own project: weak), `2026-04-14-signed-usb-rescue-boot…` (weak), shelved `2026-08-01-dependency-risk-leading-indicators.md` (refuted leading-indicator thesis).
- `2026-05-07-patch-fast-pull-slow…` (npm supply chain, Shai-Hulud): weak/moderate, different mechanism.
- `gh issue list --state all --search repojacking|"dangling repository"|dependency-risk-profiler` → only #304 (closed: DRP leading-indicator post refused because the claim was withdrawn).
- Shelved-drafts lesson applied: the denominator draft was shelved for claims broader than its frame. This post scopes every number to the sample, four ecosystems and snapshot; it makes **no** predictive claim for DRP and says nothing was exploited. It does not repeat any withdrawn claim from DRP `docs/withdrawn-claims.md`.
- Verdict: no strong overlap; no cross-link required. Optional: none of the archive posts is a natural link target.

## Layer-1 coverage (self-applied)

| Stage | Status | Evidence |
|---|---|---|
| blog-overlap | completed | above |
| blog-factcheck | completed | ledger; all external quotes re-fetched and matched verbatim; numbers recomputed from JSON. Two items rest on repo prose only (first-run 59/118; Packagist mechanism) and are labelled |
| blog-llm-tells | manual | read-through: no em dashes, no banned hedges outside quoted source text, no exclamations; one three-item scope list kept because it is a genuine scope statement; softened an absolute "nobody checks" to match PyPI/npm verification |
| blog-nda-check | completed | no employer/work reference; all first person refers to William's public repo and its recorded runs; no sampled package/owner names published |
| blog-argument-shape | completed | thesis: "For those packages, the field a scorer reads names an account that, on the day it was checked, nobody held." Type: experiment report + prior-art positioning. Strongest objection (404 ≠ claimable; retirement protects popular repos) answered in its own section. Close follows from the body. Disconfirming result named in the post (protocol's <10% line) |
| blog-visuals | manual | one `.flow` (role/aria-label on root, branch legs mirrored), one Markdown table; doodle left as TODO for root; render not inspected in a browser |
| blog-artifact-check | completed | linked artifacts are DRP files at an immutable commit (verified to exist); Scorecard code pinned to commit with line range verified; no gists, no config, no commands for readers to run |
