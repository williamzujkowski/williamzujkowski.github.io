# Staggered 2026 research release

Status: articles reviewed and scheduled; local release checks complete; PR CI and merge follow. Neither post is published yet.

The author approved Timelock Drive first and page-cache isolation second, with
staggered dates after research became public, and authorized consensus decisions,
implementation, issues, review and merge without repeated feedback requests.

| Post | Source chronology | Planned website date |
| --- | --- | --- |
| Backup administrator and retained history | [Timelock Drive, OSDI 2026](https://www.usenix.org/conference/osdi26/presentation/rosenblum); proceedings available July 13, 2026 | September 14, 2026 |
| Two processes, one page cache | [arXiv 2607.17518](https://arxiv.org/abs/2607.17518), first submitted July 20, 2026; v2 July 21; preprint | September 21, 2026 |

Both dates follow the September 11 preparation and evidence collection. Dates
denote UTC eligibility. Actual site appearance follows a successful deployment;
the daily build is configured for 10:17 UTC. GitHub scheduling is best effort, and
failed/delayed builds can postpone release. The public repository is not an
embargo: website publication filtering does not conceal committed source.

## Evidence and review requirements

- Timelock: an original synthetic retention model must not be described as a
  reproduction of the paper's isolated hardware enforcement or security proof.
- Page cache: record available virtualization capabilities before choosing the
  local experiment. If only a shared-file/process demonstration is feasible,
  explicitly distinguish it from the paper's VM and container experiments.
- Keep all controls, raw results and negative results. Numerical claims must be
  independently recomputed. First-person prose must not invent author history.
- Verify primary source versions, release dates, limitations and errata; review
  overlap, attribution, voice, artifacts, visuals, security and prior art.
- Current builds must omit the scheduled posts from all generated public
  surfaces; a local future-date build must render both for pre-release QA.

## Nexus record

`execute_spec(dryRun: true)` parsed the requirements and acceptance criteria. It
performed no implementation. Work was explicitly ordered as source/experiment
validation, drafting, independent review, build checks and merge.

Plan vote `job-vote-e63c442e-dc1c-4c4e-8510-9f799a6c26fc` completed with an
**approved, 3–0** result using simple majority and fail-closed error handling.
The architecture, security and scope roles all used `gemini-3.1-pro-preview`;
these are distinct roles, not independent model families. No simulated votes.
The vote supports the plan, not the factual accuracy of the papers or lab results.

## Tracking

- [#597: Timelock post](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/597).
- [#599: Page-cache post](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/599).
- [#600: Publication scheduling](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/600).
- DNS metadata and Svalinn remain queued in #598 and #588; this release develops
  the two explicitly prioritized posts.

## Independent review and iteration

Three collaborating agents and root covered argument/reason-to-exist, primary-source
accuracy and arithmetic, prose/structure, prior art/fairness, contextual NDA,
security, artifact provenance, and scheduling code. Authors cross-reviewed the
other article; scheduling's author explicitly identified its own code reread as
self-review. Root independently reviewed the publication path and lab method.
This adapts the local blog-deep-review lenses to the available concurrency; votes
do not substitute for source verification.

- Timelock: eight cases and 34 operations, independently recomputed and exactly
  replayed. The model assumes isolation and does not reproduce hardware. Added
  AWS variable retention/event holds as a close existing countdown analogue.
- Page cache: retained both 180-trial runs, including the failed tmpfs control.
  Root and reviewers recomputed each condition's counts and medians and verified
  preserved source hashes. Corrected a residency sentence that reversed 0/60
  and wording that misplaced February's NDSS paper after July. Credited that
  paper's existing tmpfs warning, discovered during review.
- Browser QA caught and fixed the helper's source-directory depth. A separate
  pre-existing feed-layout assertion compared viewport coordinates after a
  preceding screenshot had scrolled; it now compares document coordinates.
- The local visual-authoring suite was accidentally included in the first full
  run. Its machine-specific baselines are not this release's acceptance gate;
  the CI-mode suite and direct new-post screenshots provide the relevant checks.

Follow-ups: [#601](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/601)
tracks a test-only mismatch when a real-clock build and browser assertions span
UTC midnight; [#602](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/602)
proposes a disposable version-aware retention/restore manifest experiment. No
live cloud experiment was performed.

## Release QA

- 230 Python tests and 11 subtests; 48 Node tests; Ruff, Astro check, ESLint and
  five design audits passed. Astro retained seven existing hints; ESLint retained
  two existing warnings. No dependency changes.
- CI-mode browser suite: 91 passed, 24 local visual-authoring cases skipped.
  Future September 21 publication suite: four passed.
- Actual builds: September 11 has 92 posts and hides both articles; September 14
  has 93 and exposes only Timelock; September 21 has 94 and exposes both. Checked
  routes, social cards, JSON/XML feeds, archives and sitemap. Browser checks
  exercise taxonomy and the real Pagefind index. Restored the actual-clock build.
- Both new articles returned 200 and passed axe at 1280px and 390px in light and
  dark modes: eight scans, no page errors or horizontal overflow. Inspected the
  mobile heading and rendered diagrams; native visuals remain readable.
- Internal links: current 210 pages/8,389 links and future 213 pages/8,498 links
  passed. Configured Gitleaks scans were clean. An unconfigured whole-post scan
  rediscovered the exact TLS-group false positive already resolved by #493 and
  the repository allowlist; no new secret or blanket suppression.

Release vote `job-vote-516414e8-317e-4c53-8874-6c8f0ed74973` returned rejected
0–3 with no voter errors. All three roles rejected solely because they assumed
the target was the Nexus implementation repository, despite the explicit website
scope. This is a tool-context failure, not an approval and not a release defect
finding; evidence was added to existing #595. A single context-corrected attempt
was dispatched as `job-vote-4b5c91cb-69d8-4fae-8e08-8fe57018a4c3`.

The context-corrected release vote completed at 2026-09-11 15:10:46 UTC:
**approved 3–0**, no errors, no simulations, simple majority with fail-closed
handling, producer 8.49.3. Architecture, security and scope all used
`gemini-3.1-pro-preview`. This approval is conditional on required PR CI passing;
it does not erase the earlier rejected record or make correlated roles
independent model families.
