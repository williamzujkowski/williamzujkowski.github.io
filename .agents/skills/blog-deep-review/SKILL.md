---
name: blog-deep-review
description: Conduct a deliberate adversarial review of consequential blog posts or archive content across purpose, source accuracy, prose, and prior-art/fairness lenses.
license: MIT
---

# Blog deep review

Read [repository policy](../../../AGENTS.md), the
[research workflow](../../../docs/blog-research.md), and the
[review contract](../../../docs/skills.md). Inputs are the requested post or
explicit archive scope plus available sources and experiment artifacts. Resolve
paths from the repository root, three directories above this skill. This review
complements the seven-stage pre-publish workflow; it is not an automatic eighth
stage for every small edit.

## Independent lenses

When delegation is authorized and available, run four independent reviewers on
the same revision. Give them the source material and their lens, without other
reviewers' conclusions. If independent reviewers are unavailable, perform separate
passes where useful and disclose the lack of independence; never invent votes or
claim that one reviewer constituted four independent agents.

1. **Reason to exist.** Identify the specific reader, what they can do or decide
   afterwards, the strongest expert dismissal, and whether the post answers it.
   Locate the best contribution and the material that dilutes it. Return publish,
   named revisions, or substantially rework with reasons.
2. **Source accuracy.** Verify load-bearing facts and each numerical claim against
   primary sources. Re-derive arithmetic, scope, denominators, uncertainty, and
   comparisons. Record exact matches, honest rounding, mismatches, and unavailable
   evidence. Check whether the cited version existed before publication.
3. **Prose and structure.** Apply the actual voice policy and use a few related
   posts for context without treating their defects as precedent. Trace section
   progression, identify where reader attention is lost, and propose concrete cuts
   or line edits. Preserve necessary qualifications and earned humor.
4. **Prior art and fairness.** Search primary literature and project histories for
   the same result and the strongest counterexample. Test absolutes, novelty,
   attribution, and fair representation of named people or projects. Distinguish
   observed evidence from inferred motive. Assess security examples in the actual
   task context; flag exposed secrets, identifying private details, or unsafe
   operational assumptions with specific evidence.

## Adjudicate and verify

Reviewers can agree and still be wrong. Recompute every challenged number from
raw inputs before accepting a correction. Where reasonable treatments differ,
calculate each and explain the range. Resolve conflicting edits by examining
what the paragraph contributes and what the sources support, not majority alone.
Follow the repository's Nexus review/fallback rules when using its tools.

Apply changes only within the authorized task. Rerun affected semantic reviews
and appropriate build/design checks after substantial edits. Search for stale
copies of corrected figures in tables, captions, artifacts, and related posts.
For published work, document material factual corrections visibly and preserve
the slug. Correct upstream artifacts when authorized; otherwise record a concrete
follow-up rather than silently pretending the source was fixed.

For archive work, triage first: claims contradicted by later retained evidence,
dense numerical arguments, dated security recommendations, unresolved citations,
and reader impact. Missing/dead sources require recovery or qualification, not an
automatic declaration that the underlying claim is false. Keep the requested
scope bounded and report batches as they complete.

## Result

Lead with a supported verdict: stands, correct in place, substantially rework, or
recommend withdrawal. Report factual errors, unanswered objections, uncited prior
art, unfair claims, and proposed cuts. Include reviewer coverage, disagreements,
adjudication evidence, and every recomputation. Distinguish unsupported from
fabricated, unavailable from contradicted, and recommended changes from completed
work. Incomplete lenses or critical unverified claims must remain visible.
