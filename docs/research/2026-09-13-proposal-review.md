# Research proposal review — September 13, 2026

Scope: the six open blog proposals, reviewed against main `a1edb21`, existing
articles, scheduled posts, research/shelved records, issue comments, and relevant
closed work. This is an editorial allocation decision, not publication approval.
No experiments, cloud calls, article drafts, or new publication dates were made.
The September 14, 15 and 21 schedule remains intact.

## Decision

Prioritize three bounded feasibility passes in this order. A pass earns further work
only when it produces useful evidence; it does not reserve a publication slot.
The estimates below are editorial planning estimates, excluding publication QA.

| Order | Proposal | Decision | Why / next gate |
| --- | --- | --- | --- |
| 1 | [#591: ZIP parser disagreement](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/591) | Pursue a small pilot | Strong security relevance and inspectable outputs. Three pinned parsers, a valid control and at most six harmless fixtures; demonstrate a reader-relevant agreement/rejection/disagreement outcome. |
| 2 | [#589: Concurrent music edits](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/589) | Pursue a trace-based explainer | Distinctive fit with the live-coding work. One historical trace plus one useful inert music-edit example; keep replica equality, insertion contiguity and syntax separate. |
| 3 | [#588: Retry recovery](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/588) | Pursue the original retry question | A concrete recovery decision goes beyond the existing resilience overview. Select this thesis; park the separate Svalinn overload-control angle. |
| 4 | [#592: DNS cache isolation](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/592) | Defer; retain the topology experiment | A distinct DNS mechanism, but another shared-state article needs a useful deployment distinction: separated forwarders with shared versus separated upstream caches. |
| 5 | [#602: Retention and restore manifest](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/602) | Artifact first; defer a standalone post | The scheduled retention article already explains the proposed lesson. A reusable, executed recovery drill could justify an extension or a new post. |
| 6 | [#598: Encrypted DNS metadata](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/598) | Reframe to constrained IoT; defer | Its dataset is unsuitable for a standalone DoH study. Require a named IoT reader decision before further work; remove automatic publication of an aggregate recap. |

## What would make the first three worth reading?

### ZIP: inspect the content boundary, not another scanner dashboard

The existing scanning-pipeline article covers integration. The useful new result
is whether the scanner and consumer receive equivalent content, including entry
order, warnings, rejection and output hashes. PR #610 selected another subject for
its slot; it did not complete or invalidate this proposal.

Capture per-entry data before extraction overwrites can conceal a disagreement.
If the title promises a scanner/consumer comparison, include a named harmless
marker checker; three extraction tools alone establish only parser behavior.

Start with one day of feasibility work under the issue's original offline limits.
Do not run the large upstream fuzzing campaign or execute extracted content.
If current parsers agree or safely reject every selected case, preserve that
negative result. It earns a post only if it supports a useful compatibility or
validation decision; historical findings alone cannot establish a current bypass.
[USENIX Security 2025 paper and artifact links](https://www.usenix.org/conference/usenixsecurity25/presentation/you).

### Music: the example has to explain more than broken syntax

The June music article covers browser automation and isolated sessions. This
proposal concerns edits to the same replicated document, so overlap is weak.
The example must expose a concrete editing property; replacing “shopping list”
with “drum pattern” does not create a contribution.

Budget half to one day for the first trace and artifact. The published Yjs example
uses three replica IDs and historical Yjs 13.6.8, not a universal two-replica failure.
The issue's title should remain provisional. Respect causal-delivery requirements
and distinguish Fugue from FugueMax. Do not equate convergence with musical intent
or run the resulting text as code. Stop after the historical trace and one useful
new example; drop the music framing if it adds nothing.
[Successor paper, v3 and Appendix A](https://arxiv.org/html/2305.00583v3),
[earlier errata](https://martin.kleppmann.com/2019/03/25/papoc-interleaving-anomalies.html).

The [author artifact](https://github.com/mweidner037/fugue/tree/31e74fea67f23add13a5d10f781c0d78edcd14da)
was inspected at its November 2023 revision; current-library behavior and execution
compatibility remain untested. Check its directory-specific license exceptions
before redistributing code. This is older research, not a 2026 discovery.

### Retries: recovery must happen after the fault goes away

The useful outcome is goodput of original requests after a temporary fault,
including new arrivals, abandonment and terminal failure. Compare identical
arrival schedules and the specified controls. Do not manufacture metastability
by retuning until a queue stays full. If the sustaining condition does not appear,
report non-reproduction and decide whether the operational lesson remains useful.
The existing general resilience post lacks this measured recovery comparison.
[Metastable Failures in the Wild, OSDI 2022](https://www.usenix.org/conference/osdi22/presentation/huang-lexiang).

Keep the issue's 30-minute execution ceiling; allow one to two working days for
implementation/analysis before deciding on publication. Specify whether timed-out
work continues on the server and that the shared retry budget is process-wide,
not a distributed coordination claim. Existing token-bucket guidance is prior art;
the new contribution must be the measured recovery/fairness boundary.
The 2026 Svalinn angle is
another thesis and a substantially different artifact. Its
[Go reproduction instructions](https://github.com/GT-ANSR-Lab/svalinn-go) require
a multi-node environment and runtime/kernel instrumentation. A small limiter
simulation cannot substantiate the paper's multi-resource results. Newer research
is useful when it improves the reader's question, not merely its date.

## Why the other proposals wait

### DNS cache isolation: worthwhile only beyond the familiar warning

The September 21 article concerns the Linux page cache; it does not complete
this DNS experiment. Both concern shared state, so leave editorial space between
them. The DoH privacy repairs are already complete in #593/#620.

The experiment must verify cache state and isolate the common upstream as well
as local forwarders. Use the proposed one-day cap and held-out/permuted-label
comparison; stop if controls fail and preserve non-discrimination without tuning
until positive. The paper's browser exploit and current browser viability are
outside this direct-client lab. Broadly shared resolvers can dilute attribution,
so the two-client model cannot imply identifiable browsing on every public cache.
[DNS FLaRE, particularly §§8.8–8.9](https://www.usenix.org/system/files/usenixsecurity25-moav.pdf).

### Retention: prove a useful restore, or extend the existing article

The scheduled September 14 article already covers delete markers, protected
versions, an evidence manifest and expiry controls. Repeating AWS documentation
would add little. A reusable drill could still be valuable even if every result
matches documented behavior.

Before execution, settle an authorized real provider, permission matrix, storage
and request budget, retention duration and cleanup. Count setup, retries and
verification in the proposed request cap. A denied delete needs a successful
eligible control to distinguish retention enforcement from simply lacking delete
permission. Recover the intended version and verify its original-byte hash.
An emulator establishes only emulator behavior. If the output is merely expected
response screenshots plus the existing schema, extend the September article
instead of publishing another post. [AWS Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html).

### IoT metadata: change the research question before changing the classifier

The 2026 paper focuses on constrained-IoT frame classification and header elision.
It does not recover domain names. Section VIII explicitly discourages isolated
DoH studies using its aligned TLS 1.2 dataset. The current broad framing risks
repeating the corrected DoH article's existing traffic-analysis limitation.
[Paper, §§VI–VIII](https://arxiv.org/html/2606.10097v1).

Rescue it only around one named scenario and IoT protocol-design decision.
Small plot CSVs exist in the pinned artifact, so checking a figure does not require
downloading everything. The [versioned release](https://zenodo.org/records/21136943)
separates 171.2 MB of code/plot material from 175.4 GB of full data. New classifier
claims still require an appropriate raw subset and evaluation split within the
original budget. The upstream full workflow can take weeks and exposes a Docker
socket; none of it was executed in this review. Inspect selected data directly.
If the reader decision or usable evidence is absent, keep notes and shelve the
standalone article. Replotting alone is not an editorial reason to publish.

## Review coverage and limitations

Three independent agents reviewed paired proposals: `proposal_systems` (#588/#591),
`proposal_music_cache` (#589/#592), and `proposal_challenge` (#598/#602). Root
independently checked the last pair, compared the portfolio, and verified the
scheduled archive context. Sources were read as evidence, not executed. No claim
is made that every cited artifact currently runs or that publication QA is done.

Nexus registry search for the exact combined query “DNS privacy Timelock
metastability Fugue ZIP” returned no matches. That result is not evidence of
novelty or absent prior art. A real consensus review of the concrete portfolio
was requested in job `job-vote-d29c5fa8-3ca9-4e5c-8390-c57cf63ed879`.

The job completed at 05:40:21 UTC, producer 8.49.3: **approved 3–0**, real
quick-mode supermajority with fail-closed error handling. All three roles used
`gemini-3.1-pro-preview`, so this is role diversity, not model-family diversity.
The tool emitted an alternatives warning; the actual question was approval of
one fixed ordered plan, not selection of a winning option. No option-election
claim is made and no rerun was used.

The security voter also mentioned Zip Slip and cache poisoning, which are not
the proposed experiments. Those associations do not expand scope or establish
findings: ZIP traversal/symlink fixtures remain excluded, and DNS cache timing is
not a cache-poisoning test. Source review and the narrower gates above control.

Stop reason: all six existing proposals received a decision, nearest-archive
comparison, source/method check and explicit next gate. This was not a fresh
paper-discovery sweep. No new proposal issue was created.
