# DoH guide correction evidence

Date: 2026-09-13. Scope: issue #620 and
`src/posts/2025-07-08-implementing-dns-over-https-home-networks.md`.
This is a source and artifact review, not a deployment or benchmark experiment.

## Decision and chronology

Preserve the original July 8, 2025 date and slug; add a visible September 13, 2026
correction. Narrow the article to browser and Pi-hole upstream topology and
proposed acceptance checks. Remove incomplete deployment examples, invalid Python
requirements, unsupported performance figures and first-person experiences for
which this review found no retained author evidence. Missing evidence does not
establish fabrication. No replacement homelab experiment is claimed.

The current Cloudflare removal notice belongs to the dated correction. Historical
protocol and topology sources below predate the original post. The current
Pi-hole guide is explicitly labeled a September 2026 installation reference;
its present distribution assumptions are not attributed to July 2025.

## Claim ledger

| Retained claim | Evidence | Scope/status |
| --- | --- | --- |
| DoH transports DNS messages over HTTPS; resolver identity, privacy limits, and resolver trust remain relevant. | [RFC 8484](https://www.rfc-editor.org/rfc/rfc8484.html), October 2018, sections 3, 8, 9. | Verified protocol claims; no universal privacy guarantee. |
| Firefox mode 2 permits ordinary-DNS fallback; mode 3 and exclusions need distinct treatment. | [Mozilla source documentation](https://github.com/mozilla-firefox/firefox/blob/ce8560edadf1e29fd9646be1fb3cfaa9b4e0d7b1/netwerk/docs/dns/dns-over-https-trr.md), commit dated 2024-06-27. | Verified historical behavior; no new browser experiment. |
| Pi-hole can forward ordinary DNS to a local dnscrypt-proxy listener that uses an encrypted upstream. | [Pi-hole source guide](https://github.com/pi-hole/docs/blob/7ca1c7b7aae00f0cb175c9b6ef02fe53ab2092e9/docs/guides/dns/dnscrypt-proxy.md), commit dated 2025-03-04. | Verified topology and port separation. Historical install commands are not reproduced as current instructions. |
| A browser querying an external resolver directly bypasses Pi-hole filtering for that query. | Inference from the documented browser and Pi-hole paths above. | Explicit topology inference, not a measured result. |
| New cloudflared releases remove proxy-dns beginning 2026-02-02. | [Cloudflare notice](https://developers.cloudflare.com/changelog/post/2025-11-11-cloudflared-proxy-dns/), 2025-11-11. | Verified announced removal schedule, reported in a dated correction; no old binary recommended. |
| Current Pi-hole instructions advise against new cloudflared proxy installations. | [Pi-hole cloudflared guide](https://docs.pi-hole.net/guides/dns/cloudflared/), accessed 2026-09-13. | Verified current warning. |

Read-only GitHub API queries used the commits endpoint with the relevant path,
`until=2025-07-08T00:00:00Z` and `per_page=1` to identify historical documentation,
then retrieved each file with its immutable revision via the contents endpoint.
Source content was inspected, not executed. HTTP sources were read with web tools.

## Removed artifact findings

All five public gists were retrieved using `gh api gists/ID`, including filenames,
full content, creation/update timestamps and the API truncation flag (false for
every file). They were created on November 3, 2025, between 22:49:46 and 22:49:50
UTC. Later gist creation can reflect extraction of older code; the timestamp span
alone does not establish the origin of the underlying work.

| Gist | Observed content defect |
| --- | --- |
| [Router setup](https://gist.github.com/williamzujkowski/9ca841f8bdea7bced7c797ee2cfa5597) | Explicit omitted implementation; mixed platform setup; cloudflared installation does not configure the claimed complete DNS path. |
| [Monitoring](https://gist.github.com/williamzujkowski/82e4d29a006b6fc5b20b881760d6deb9) | `benchmark_dns`, query functions and test inputs are undefined; log analysis is omitted. No measurements are retained. |
| [Security hardening](https://gist.github.com/williamzujkowski/48bd7c6e1d18e0d12cfcad67ff4a644c) | Pinning file has `return context` outside a function; IPv4 host OUTPUT rules do not establish that all network devices use DoH. |
| [Troubleshooting](https://gist.github.com/williamzujkowski/365d9b3a0dc812e93ec8177e5bf84922) | Writes configuration files; hostname ping selects a plaintext downgrade; version-specific setting validity was not established. Removed rather than substituted with guessed keys. |
| [Advanced routing](https://gist.github.com/williamzujkowski/8749d27f31c0c222e79033fc978069bd) | Geographic helper is undefined; nginx upstream block has no complete request or TLS configuration. |

The article no longer presents these as usable tools. The public gists remain
unchanged; archival annotations are tracked in
[issue #624](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/624).
A search under `gists/` found no corresponding DoH mirrors.
No gist drift check was needed because no mirrored or remote artifact was edited.

The removed dependency instructions mixed standard-library modules with external
distributions. [Python's standard library](https://docs.python.org/3/library/index.html)
contains `base64`, `hashlib`, `ssl` and `statistics`; the `dns.resolver` import is
provided by [dnspython](https://dnspython.readthedocs.io/en/stable/installation.html).
Since the replacement article runs no Python examples, it needs no replacement
requirements block.

## Final review coverage

Used the portable pre-publish, factcheck, artifact-check, NDA and visuals
procedures. The retained prose contains no employer incident or asserted personal
deployment/benchmark; the homelab checks are clearly proposed actions. The source
and artifact findings above support the bounded correction.

Visual source inventory: existing zine doodle retained; one native `.flow` added
with `role="group"` and a purpose-specific accessible name; one Markdown table.
No new raster asset, custom visual class or hardcoded color was introduced.

The [seven-stage report](2026-09-13-doh-review.json) records manual review with
evidence and derives READY for the correction. This means the article's review
is complete; it is not a claim that a deployment or benchmark was performed.

Four independent reviewers covered the deep-review lenses on source SHA-256
`169d8af15c7382ae458de15a97ec93de952c0ce1437d31e1bb02ea033fe101b1`:

- `harness_validation`: reason to exist, overlap and argument; searched 96 posts
  and fully compared the March Raspberry Pi and February automation articles.
- `root`: source accuracy and chronology; retrieved primary documents and commit
  dates, verified retained configuration details, and reviewed attribution.
- `doh_prose_review`: prose and structure; no blockers, optional title/wording
  suggestions remain editorial choices.
- `doh_fairness_review`: prior art, fairness and security; independently checked
  the protocol, browser, Pi-hole and Cloudflare claims; no blockers.

The content drafter's source/artifact inventory informed the review but was not
counted as an independent reviewer. No numerical results remain to recompute.
The adjacent February dependency defect is tracked separately in #622.

Targeted axe testing found a real shared-style defect: flow captions using
`fg-muted` on Latte's surface had 4.25:1 contrast at 13px. The caption rule now
uses `fg`. Two regressions verify the actual DoH page at 1440px Latte and 390px
Dracula, including the selected deck, live page, flow visibility, axe and overflow.
The corrected rendered diagram was also inspected visually.

Validation passed: production build, five design audits, Astro check (zero errors
or warnings, seven hints), ESLint (zero errors, two existing warnings), 48 unit
tests, 216-page internal-link validation, and 93 browser tests in CI mode.
The 24 local screenshot-authoring cases are deliberately skipped in CI. An initial
local-mode run reached those cases and failed because this isolated checkout had
no machine-specific baselines; it was stopped and not reported as passing.
The CI-mode run used its normal skip guard and a fresh preview server, without
disabling assertions. Required hosted checks remain a merge condition.

Nexus producer 8.49.3 plan job
`job-vote-9ce46750-66ab-435e-a942-5ca97f82501b` rejected 0–3. All three roles used
`gemini-3.1-pro-preview` and rejected the external blog scope as outside the Nexus
product mandate. The result remains rejected under #595; no favorable-result
retry was used. Completed independent review and required checks provide the
repository's documented fallback under the owner's existing authorization.
