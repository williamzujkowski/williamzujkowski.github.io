# Feed and link-extractor follow-ups

Date: 2026-09-11. Starting commit: `a5b9bd2`.

## Scope and decisions

- [#581](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/581): RSS and JSON Feed exposed authored diagram markup as text. Enable HTML in the shared Markdown renderer, sanitize it, preserve diagram labels and readable block boundaries without site CSS, and sanitize the final fallback again. Root-relative URL rewriting now operates on parsed attributes so literal code examples remain unchanged.
- [#582](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/582): replace URL-prefix deduplication with overlapping source spans, collect reference definitions before uses, and trim trailing prose punctuation only from bare URLs. Keep the existing report shape and occurrence metadata.
- [#540](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/540): [upstream dependabot-core#16232](https://github.com/dependabot/dependabot-core/issues/16232) remains open, with no comments and last update 2026-09-09T15:38:25Z when checked. No evidence warrants changing the current lockfile workaround.

No dependency, publication-policy, site-style, or automated link-repair changes.

## Research and review

Inspected the installed sanitizer implementation and its [upstream documentation](https://github.com/apostrophecms/apostrophe/tree/main/packages/sanitize-html#transformations). Its parser normalizes and escapes attribute values; `transformTags.text` replaces an element's direct text, so it is unsuitable for prepending diagram labels. The implementation carries labels through temporary escaped attributes, expands only the sanitizer's canonical output, then applies the final allowlist. The final pass removes temporary attributes. Active elements, styles and event handlers are excluded. Authored CSS doodles are omitted while their separate captions remain.

Nexus 8.49.3 orchestration job `orch-mtwiqrrq-41xfai` completed with zero steps and zero experts. A subsequent `code-expert` execution failed with `No model adapter available`; neither is counted as a substantive review. Local source research and an independent delegated review supplied that analysis.

Nexus consensus job `job-vote-e1a4dfd0-174c-4f33-a98c-00f094ded3c6` approved the bounded plan **3–0**, with no errors or simulated votes. Architect, security and scope-steward roles all used `gemini-3.1-pro-preview`; this is a three-role review, not three independent model families.

Independent adversarial review found that an initial separator replacement changed ordinary inline prose (`micro` + `services`). The revision limits added spacing to children of diagram nodes and sequence steps. A regression test preserves the original prose. Encoded labels, forged markers, direct text, nested children, malformed active HTML and literal URL examples were also probed. A second review found that transforming a doodle to a discarded tag left stale sanitizer bookkeeping and mis-nested the following heading. Doodles now use `exclusiveFilter` to remove the original subtree; a regression checks sibling closing tags and forged removal markers.

## Validation

The initial eight feed tests produced six failures against the original renderer; literal-code and footnote tests already passed. The suite now includes twelve feed tests, with the global unit floor raised from 30 to 42.

The extractor's full 197-test suite passes, including 11 real CLI cases and eight explicit-punctuation cases. Ruff passes. Before/after CLI inventory: **95 posts, 1,545 occurrences** in each run. Every ordered link record and all statistics are identical; only the extraction timestamp is excluded from comparison. Temporary evidence: `/tmp/issue582-baseline.json` and `/tmp/issue582-after.json`.

Production build passes: 210 pages. Offline link validation resolves 8,389 links and 2,526 anchors; four links into other deployments are intentionally excluded. Astro checking reports zero errors/warnings and seven existing hints. ESLint reports zero errors and two existing warnings. All five design audits pass.

The initial local browser command passed all 91 functional tests but failed 24 optional visual-authoring comparisons against existing machine-local snapshots (image differences and screenshot timeouts). These snapshots are not tracked and the suite intentionally skips them in CI. No snapshots were updated. The final CI-mode run passed **91 tests**, with **24 intentional visual-authoring skips**, no failures and no retries. Both feeds contain **92 published articles** with identical content fields. The composited-grain contrast audit also passed. The feed-specific checks compare all RSS/JSON content, exclude drafts, inspect markup and footnote targets, and render representative architecture/branch diagrams at 360px and 1024px without site CSS.
