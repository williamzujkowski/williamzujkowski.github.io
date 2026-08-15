# Shelved drafts

Posts that were written, then contradicted by later evidence. Kept because the
record of being wrong is worth more than a deleted file, and because the
retraction is itself publishable material.

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
