# Scanning-pipeline correction — September 13, 2026

Scope: issue #632, the linked workflow's job dependencies, aggregate gate and
interpretation of the performance table, plus its adjacent universal action-pinning claim. This is a bounded correction to the
October 6, 2025 article, not a complete archive or gist re-audit. The original URL
and publication date remain; `lastUpdate` and a visible correction identify this
review date. No gist or mirror was edited.

## Canonical source inspection

Read the complete canonical workflow through GitHub's gist API at all three
published revisions. Gist creation is November 1, 2025, after the article date;
that establishes artifact availability, not the date its underlying code was
first written or evidence of fabricated experience.

| Revision | Gist commit date | Gate observed |
| --- | --- | --- |
| [bf17f1a](https://gist.github.com/williamzujkowski/8185611a406dd91806f37d51778cdd16/bf17f1a749c35b88bdc1a1f5d77748dd1daaf63c) | 2025-11-01 | Echo plus comments, no result evaluation. |
| [a2ef3b7](https://gist.github.com/williamzujkowski/8185611a406dd91806f37d51778cdd16/a2ef3b7e0e070a7bbc4cf9a669ec0d9937e10c44) | 2026-08-18 | Reads each `needs` result; fails unless every result is `success`. |
| [b8c467b](https://gist.github.com/williamzujkowski/8185611a406dd91806f37d51778cdd16/b8c467be7577d2280bc2f5fea388cb9109555121) | 2026-08-23 | Same aggregate result evaluation. |

Both follower jobs declare `needs: dependency-scan` and do not depend on each
other. The final gate needs all three and uses `if: always()`. The gate checks job
status, not SARIF contents, so it cannot add a failure policy to an advisory
scanner. Checked this reading against GitHub's
[job dependency documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs#defining-prerequisite-jobs)
and [expression documentation](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#always).

The current revision pins all three scanner actions but retains
`actions/checkout@v4` and `github/codeql-action/upload-sarif@v3`. The article now
states those exceptions and recommends pinning them; no gist changes were made.

No workflow was executed as a benchmark or scanner evaluation. The corrected
article labels its echo example as historical, names when the working gate was
present, and describes OSV first followed by potentially overlapping Grype/Trivy.

## Timing interpretation

The three initial values sum to `45 + 150 + 195 = 390` seconds. The listed optimized
values sum to `12 + 35 + 70 = 117` seconds. The reduction in that sum is
`(390 - 117) / 390 = 0.70`. These are recomputed arithmetic, not new measurements.
The old 120-second total did not match its rows.

Searched the repository's research records and gist/script paths for the article,
scanner timings and retained benchmark records. No supporting timing logs were
found. The article now explicitly labels the historical measurements and runner
provenance unverified, including the adjacent claimed optimization savings.
Neither sum nor slowest-scanner duration determines real workflow latency.
No new end-to-end duration is asserted from the dependency graph.

## Review coverage

Read and applied canonical `blog-artifact-check` and `blog-argument-shape`
procedures. Corrected orchestration/gate claims are supported by source inspection;
the timing table is retained as explicitly unverified historical figures with
corrected arithmetic. No claim of full-post publication readiness or verification
of unrelated scanner flags, other gists, historical anecdotes or measurements.

Root performs independent review before merge. Build result is recorded in the
PR. No new tests were authored for this prose correction; the website build is
the relevant mechanical check.
