# Website and publishing improvement plan

Reviewed September 8, 2026, against `875cc84036070b64b7b8ebca820d6e7b04552083` and the live site. The initial review below records the baseline findings. Implementation began later the same day; see the execution record at the end for current status. New posts remain unpublished drafts.

## Direction

Keep the current Astro/Svelte architecture, Remarque typography and static deployment. The largest demonstrated opportunities are reliable search and accurate maintenance feedback. A redesign would leave those problems intact.

Keep the editorial center on agentic security, security tools and practical systems work. The author clarified that preference during the review. Website engineering is secondary material, not the next main article.

The review used three independent agents, local production checks, live Chromium interactions, and original research sources. Work progressed through bounded review, reproduction, and synthesis cycles, extending the research cycle after the author's topic clarification. No recurring background loop was installed.

## Ordered implementation backlog

Effort ranges are planning estimates, not measured implementation times. Each issue contains reproduction details and acceptance criteria.

| Order | Work | Why now | Completion evidence | Estimated effort |
|---|---|---|---|---|
| 1 | [#549: repeated search opening leaves the page inert](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/549) | P1: a normal keyboard sequence disables reader interaction until reload | Open/open/close regression restores interaction and original focus; preserves pre-existing inert state | Half day |
| 2 | [#553: CI input coverage](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/553) | P1: test-only and some workflow-only changes skip relevant required jobs | Test, workflow, lockfile and checker-only diffs select their consuming jobs; required checks still report on unrelated changes | Half–one day |
| 3 | [#554: binary citation responses](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/554), [#555: report completeness and counting](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/555) | P2: successful PDF responses become errors; unresolved checks disappear from reports | Controlled HTTP fixtures, error-only report, duplicate-URL counting reconciliation | One day |
| 4 | [#550: asynchronous search lifecycle](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/550) | P2: old results can replace current state; failures resemble empty results | Reversed completion, clear/close, loader/query/data failure and retry fixtures; accessible status messages | Half–one day |
| 5 | [#551: index scope and additional results](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/551), [#552: unsupported search URL](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/552) | P2: tag/archive listings consume the result window; structured data promises an inert URL | Real built-index queries return substantive destinations; drafts/404 excluded; continuation available; query URL works or unsupported schema removed | One day |
| 6 | [#557: biography policy and factual freshness](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/557) | P2: About/Now and canonical attribution guidance disagree | Author resolves biography scope, verifies current facts and comparative claims, records reviewed date | One editorial session |
| 7 | [#556: curated archive entry points](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/556) | P3: small editorial discovery experiment | Two short reading paths, clear prerequisites, mobile/no-JavaScript checks, manual newcomer navigation exercise | Half day |

Implement each workstream in a small PR. Search indexing should select useful standalone pages as well as posts; a raw reduction in indexed-page count is not a relevance metric. A compact query set should include `ebpf`, `proxmox`, an exact title, a project name and a no-match string. Assert useful destinations and exclusions without freezing every ranking position.

For citations, use status/header handling for binary downloads; no PDF parser is needed. Bound any HTML inspection and preserve existing URL/TLS protections. Keep unresolved and access-restricted outcomes advisory and visible. Report occurrences and unique URLs separately instead of summing unlike quantities.

## Evidence behind the priorities

- Local Chromium reproduced Search → Ctrl+K → Escape leaving no dialog but `main.inert=true` and 15 `data-search-inert` elements. The site reviewer independently reproduced it live.
- Both the local and live Pagefind index returned 17 matches for `ebpf`. The first eight were the article, six tag pages and `/posts/`. The UI exposes only those eight. The production build indexed 210 HTML pages, including 404, for 92 published posts.
- A browser-only delayed Pagefind fixture reproduced stale `security` results after shortening the current query to `e`. Loader/query/data error handling findings come from source inspection; those failures were not all exercised in the browser during this review.
- CI regex evaluation excludes root `tests/unit/**`, `audits.yml`, `a11y.yml`, and `uv.lock` from their relevant jobs. Python's workflow already includes its own definition; preserve that behavior.
- The [September 7 citation run](https://github.com/williamzujkowski/williamzujkowski.github.io/actions/runs/34133539640) contains 22 decoding-error occurrences across 16 unique URLs. The tooling reviewer also reproduced a binary PDF failure with a local HTTP fixture.
- Recounting that artifact yields 551 occurrences: 391 valid, 36 redirects, 24 errors, 36 internal, 60 restricted, 3 timeouts and 1 broken. These sum to 551. Its `stats.valid=270` counts a different population. The report excludes error/timeout rows from its per-post sections.

Existing [#540](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/540) covers Dependabot's lockfile serialization problem; [#548](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/548) covers the current broken-citation alert. Neither was duplicated.

The documented deployment-order decision in #501 and the accepted CSP choices remain settled. This review found no reason to introduce a CMS, hosted search, new scanner service, or additional recurring audit workflow.

## Editorial selection

The recent archive already covers credential proxying and sandboxes (July 2), machine-readable agent controls (July 23), deterministic gate proofs (July 30), mutable authorization policy (August 18), and claim/artifact verification (August 18). The next article should add operational depth rather than reintroduce those arguments.

| Candidate | Evidence and timeliness | Distinct contribution | Decision |
|---|---|---|---|
| **Your Agent's Memory Needs a Recovery Plan** | [MemSecBench, July 29 preprint](https://arxiv.org/html/2607.27080v1), [GhostWriter, July 6 preprint](https://arxiv.org/html/2607.06595v1), [Cisco's April 1 disclosure](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code) | Incident recovery for durable agent state: remove hostile semantics while retaining necessary benign context | Selected; new draft |
| Read-only MCP needs a read-only database role | [AWS September 4 advisory, CVE-2026-85787](https://aws.amazon.com/security/security-bulletins/2026-101-aws/) | Concrete database-enforced least privilege and a controlled integration test, following the SQL validation bypass | Strong next practical post; avoid merely restating the gate article |
| Memory filtering can discard useful evidence | [Utility Under Attack, August 21 preprint](https://arxiv.org/html/2608.21230v1) | Test factual poisoning as well as imperative injection; include utility when evaluating trust-based retrieval | Research candidate; needs independent reproduction before a tool recommendation |
| Search Is Part of the Static Build | This review's build and browser evidence | Pagefind index boundaries and interface correctness | Secondary local draft retained after topic clarification |

Concrete follow-on work is tracked in [#558: memory recovery experiment](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/558) and [#559: database-enforced MCP permissions](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/559). Both experiments were subsequently run; the execution record links their methods and retained results.

Hacker News, Reddit and security reporting supplied discovery leads. Community posts and vendor promotion were not treated as independent confirmation of vulnerability prevalence. For example, the [Reddit MCP-vetting discussion](https://www.reddit.com/r/mcp/comments/1ubx5ec/how_are_you_actually_vetting_mcp_servers_before/) is useful for reader questions; its headline statistics need their original studies before publication. The [HN shared-memory tool discussion](https://news.ycombinator.com/item?id=48283108) provides product context, not a security evaluation.

## New-post acceptance criteria

- A specific recovery thesis, with links to relevant earlier posts rather than repeating their introductions.
- Research summaries distinguish injection, persistence, activation and repair; experimental denominators and conditional rates remain explicit.
- Cite versioned primary papers. Do not treat preprint benchmarks as field incident rates or rank products across unlike experiments.
- Historical disclosures include the attack prerequisite and reported fix. Do not imply a fixed version remains vulnerable.
- Proposed homelab exercises use synthetic data and mock actions, and are explicitly unexecuted unless an actual artifact and run record exist.
- Use existing `.flow`/table patterns, accessible labels and theme tokens. No invented measurements, current-work stories or published claims that planned controls already work.
- Keep `draft: true` until author review. Run the production renderer against a temporary copy with drafts enabled for visual/content checks, then confirm the normal build excludes drafts.

## Review of the plan

Nexus quick consensus returned 2 approvals and 1 rejection on the initial website plan. It is advisory input, not evidence that findings are correct. The rejection misread narrowing an existing index as expanding it, and fixing skipped CI inputs as introducing skips; those objections do not match the proposal. Its useful caution about bounded response handling is included above. The architect also misidentified the exact unit-test job: the tests run in `check-lint`, not `remarque`.

The author subsequently redirected the main blog topic to security; the vote preceded that change and does not represent a review of the security draft.

## Validation record

Baseline production build, Astro checking, ESLint, Node unit tests, five design audits, Python tests and Ruff passed. Astro emitted existing deprecation/unused-symbol hints. The built internal-link check passed for 210 pages, 5,648 links and 2,525 anchors.

The full local Playwright command produced **63 passes and 24 failures**, all failures in `visual-baselines.spec.ts`. That file is explicitly a machine-specific visual authoring tool, skipped in CI; this run encountered screenshot differences and screenshot/browser errors. No baselines were regenerated. Functional, accessibility, theme, forced-colors and sidenote cases passed. The initial automatic preview startup also exited early; a subsequent run reused the running preview successfully.

Node unit tests report 15 passing tests; Python reports 108. These green results do not cover the newly reproduced search sequences.

Both new drafts passed a production build in a temporary preview copy, with `draft: false` set only in that copy. Chromium checks at 1280px and 375px found HTTP 200, one H1, one flow diagram, no page overflow, and zero axe WCAG A/AA violations on both pages. The security post also received an independent primary-source review, which found no blocking factual issues and prompted addition of a clean baseline to the proposed drill.

The preview copy initially shared the dependency directory's Astro content cache with the repository, so concurrent builds contaminated the first draft-exclusion check. Rebuilding the normal repository after the preview build completed corrected the generated output. Final checks confirm both drafts are absent from production post routes, OG images, feeds, sitemap and homepage/archive listings. Do not use concurrent draft previews with a shared Astro cache in future validation.

The mechanical content advisory found zero NDA pattern hits across the two drafts and 100% post-level citation presence. That percentage measures posts containing citations, not semantic claim coverage; primary-source review supplied the latter judgment. The author-local skill pipeline was not invoked; no claim is made that those separate skills passed.

Deliverables are [the security draft](../shelved-drafts/2026-09-08-agent-memory-recovery-plan.md), [the secondary search draft](../shelved-drafts/2026-09-08-search-is-part-of-the-static-build.md), this plan, and issues #549–#559. That initial review did not deploy changes. Subsequent implementation and validation are recorded below.


## Backlog execution, September 8

The author authorized implementation, issue creation, parallel agents and Nexus
consensus in place of repeated feedback requests. The initial implementation vote
approved the bounded plan 2–1. The dissent requested human approval despite that
explicit authorization; its useful cautions about bounded HTTP handling and a
bounded live crawl were retained.

Implemented search lifecycle and keyboard-focus repairs, visible errors and retry,
pagination, substantive-page indexing, and removal of unsupported SearchAction
metadata. Added two short reading paths. About/Now now follow the repository's
attribution policy; Now labels an explicit **page edit date**, without implying that
all personal activity claims were independently reverified.

CI input selection now has real-git-history regression tests. Citation handling
bounds HTML inspection and accepts successful binary responses without decoding
them; reports retain unresolved and unchecked occurrences with consistent counting
units. The expired eBPF paper link now points to the coauthor's PDF, and its adjacent
description matches the paper's performance-monitoring scope.

Both follow-on labs have actual retained evidence:

- [Memory recovery](2026-09-08-memory-recovery-lab.md): 27 CLI trials across nine
  deterministic prepared states. Independent recomputation found 15 correct contact
  tasks, 24 correct unrelated recall tasks and nine false destinations. All state
  hashes and the runner hash match. The fixture measures downstream adoption, not
  real ingestion or autonomous repair.
- [PostgreSQL privileges](2026-09-08-postgres-readonly-lab.md): 24 checks against a
  disposable PostgreSQL 18.6 instance, including 15 expected permission denials and
  a deliberately granted privileged-function positive control. This did not install
  or test the MCP server or its patch.

All three drafts passed 12 isolated preview scans: desktop/mobile in light/dark,
with no axe exclusions, overflow, JavaScript errors or broken images. The temporary
build used separate caches; 556 root build/cache file hashes remained unchanged.
Normal production drafts remain excluded. The [manual full-site suite](../live-site-validation.md)
provides a repeatable route-by-route deployment check without adding a cron job.

Issue #540 remains an upstream Dependabot reproduction problem. There was no open
bot PR to test. The existing frozen-lockfile failure remains the correct visible
boundary; no speculative lockfile-repair automation was introduced.


The first complete local sweep ran 426 checks (210 routes in two configurations
plus six interaction/feed checks): 414 passed. Ten failures exposed 48 unlabeled
GFM task checkboxes across five older posts (#561); a shared renderer transform
now adds names and the existing page-specific exclusion has been removed. The
other two failures were the validator expecting `/404.html` as the canonical path;
Astro correctly uses `/404/`, and that assertion was corrected. A report-size
review also produced #560: issue excerpts are capped at 50,000 UTF-8 bytes while
the full citation report remains available as an artifact.


Final implementation validation before the dependency follow-up: 80 E2E cases
passed (including 17 search regressions), with the 24 machine-specific visual
baseline authoring cases intentionally skipped under CI. All 20 targeted
route/feed/interaction rechecks passed. Python: 143 tests plus three subtests;
Node: 18 tests. Astro checking, ESLint, design and composited-grain audits,
Ruff, actionlint and the 210-page internal-link check passed. The normal build
excludes all three drafts from post routes, OG images, feeds, sitemap and lists.

The final Nexus panel approved the gated merge process 6–1. The dissent mistook
the PostgreSQL writing experiment for a proposed website database backend and
treated the requested live confirmation as replacing preview testing; neither
matches the implementation. The useful concern about review breadth is retained:
PR #562 combines independent backlog workstreams, with separately observable
required checks. No vote establishes that a lab proves broader security claims.

GitHub subsequently surfaced Dependabot alert 141 (#563): Satori pins an affected
fflate ZIP-extraction release. Inspection found no ZIP-extraction path in the
site's build-time font rendering. The scoped compatible patch override passed frozen installation and production
build; all 92 OG PNGs are byte-identical, and the production dependency audit
reports zero vulnerabilities. The advisory was not dismissed on the basis of
that reachability review.
Deployment and final live-validation evidence are recorded in
[PR #562](https://github.com/williamzujkowski/williamzujkowski.github.io/pull/562).
