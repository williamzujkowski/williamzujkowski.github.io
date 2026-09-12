# Shelved drafts

Drafts retained outside the published content collection. Each entry records why
it was shelved: an editorial hold, an obsolete standalone proposal, or a thesis
refuted by evidence. Shelving does not by itself mean the research was invalid.
Preserve the evidence and the specific decision when reconsidering a draft.

## `2026-08-01-dependency-risk-leading-indicators.md` — "Zero CVEs Is Not a Safety Rating"

**Shelved 2026-08-14. Not stale — refuted, by our own measurements.**

Its thesis: maintenance cadence, maintainer concentration and provenance posture
are leading indicators of dependency risk, visible before the advisory.

All three were then measured in `dependency-risk-profiler`:

| claim in the draft | what the measurement found |
|---|---|
| provenance posture predicts compromise | control base rate **12.72%** vs **12.5%** in victims, **p=0.97** |
| release cadence is a leading signal | circular — it scores 0.734 on abandonment because it *is* abandonment |
| the composite predicts trouble | **0.4955** against the one activity-independent outcome. A coin flip |
| the tool beats a naive baseline | download count's bottom bucket beat its LOW bucket **3 of 3 runs** |

The README claim it rests on was withdrawn 7-0. `docs/withdrawn-claims.md` in
that repo is the standing record.

The part of the draft that survives — that a low CVE count means "unknown", not
"clean" — is real and unoriginal, and cannot carry a post on its own.

**What replaces it:** the census methods post on the denominator problem, and
(possibly) a post on the validation programme itself. Failing to validate your
own tool across ten studies is a better story than the tool working would have
been.


## `2026-09-08-search-is-part-of-the-static-build.md` — "Search Is Part of the Static Build"

**Shelved 2026-09-11. Obsolete as a standalone proposal; the fixes already shipped.**

The September 8 observations were real, and the draft scopes its original index
counts to the reviewed revision. Its proposed indexing, request-lifecycle and
keyboard-focus changes were subsequently implemented and tested. Publishing the
draft unchanged would present completed work as the next version's plan.

The useful material remains in the [site-improvement record](../research/2026-09-08-site-improvement-plan.md).
A future article would need a narrower reader question and completed evidence,
such as the tradeoff between search results and navigation listings. This draft
is historical working material, not a retraction or an active publishing plan.

## `2026-09-08-agent-memory-recovery-plan.md` — "Your Agent’s Memory Needs a Recovery Plan"

**Shelved 2026-09-11. Editorial hold for a narrower rewrite; the experiment is real.**

The [executed experiment](../research/2026-09-08-memory-recovery-lab.md) retained 27
model calls across nine prepared scenarios. Those scenarios supplied only four
unique model inputs; repeated or equivalent states do not demonstrate nine
independent recovery mechanisms. The deterministic fixture prepared the states:
the model did not discover poisoning, authenticate a reference, repair persistent
memory or send a real message.

The defensible observation is narrower: repairing canonical data can leave a
stale derived summary, and action success alone does not verify clean state.
Keep the raw evidence, failed controls and preservation results. Reconsider this
draft around that specific distinction after checking overlap with the published
agent-gate and policy-change posts. The results have not been refuted; the broader
recovery-plan framing has not earned publication.
# 2026-09-12 replacements

- `2026-08-14-nobody-publishes-the-denominator.md` — replaced by a source-led SYSSPEC post; the census draft made broader claims than its frame audit supported.
- `2026-08-18-checks-that-pass-for-the-wrong-reason.md` — replaced by a source-led Pilot Execution post; the corpus audit overstated what rounded percentages and review comments could prove.
