---
name: blog-pre-publish
description: Coordinate all seven repository blog review stages and produce an evidence-backed publication decision that cannot pass missing or incomplete reviews.
license: MIT
---

# Blog pre-publish

Read [repository policy](../../../AGENTS.md), the
[research workflow](../../../docs/blog-research.md), and the
[review contract](../../../docs/skills.md). Resolve the requested draft from the
repository root, three directories above this skill. If the active draft is
ambiguous, establish the target before issuing a publication verdict.

This is an author-time semantic review. It does not replace required build,
accessibility, design, or security CI checks, and a passing report does not itself
authorize publishing, external writes, or merging.

## Seven stages

Read each sibling `SKILL.md` directly if native skill discovery is unavailable:

1. [blog-overlap](../blog-overlap/SKILL.md): archive overlap and distinct contribution.
2. [blog-factcheck](../blog-factcheck/SKILL.md): claim/source support and dates.
3. [blog-llm-tells](../blog-llm-tells/SKILL.md): voice and prose quality.
4. [blog-nda-check](../blog-nda-check/SKILL.md): contextual attribution and disclosure.
5. [blog-argument-shape](../blog-argument-shape/SKILL.md): purpose, evidence, conclusion.
6. [blog-visuals](../blog-visuals/SKILL.md): visual meaning, accessibility, theme behavior.
7. [blog-artifact-check](../blog-artifact-check/SKILL.md): provenance and actual tool behavior.

Independent reviews may run concurrently when delegation is authorized; give them
the same post revision and source evidence, and share fetch results to avoid
duplicate traffic. Reviewers report findings without concurrent edits to the same
file. When edits are authorized, consolidate first, apply fixes, then rerun stages
whose evidence or conclusions changed. Defer costly illustration work until the
argument and evidence are stable. Do not report old-revision reviews as current.

## Coverage and decision

Use the machine-readable report schema in the review contract. Include every
stage, even an unavailable one. Coverage is distinct from findings:

- **completed**: the stage procedure was performed with recorded evidence.
- **manual**: an identified reviewer performed an equivalent review; include
  reviewer identity and evidence. A planned review is not manual completion.
- **not-applicable**: permitted only for artifact-check when its inventory finds
  no artifacts, code, configuration, commands, or API examples; include that scope
  reason. The other six stages must perform their review or inventory even when
  little relevant material exists. Unavailable tools, missing files, inaccessible
  sources, and low confidence are not this state.
- **missing**: the review was not performed or its required procedure was unavailable.
- **failed**: the review attempt could not complete.

For completed/manual stages, record `pass`, `fail`, or `unknown` independently of
coverage. A completed review can find a blocking defect. Missing or failed stages,
unknown verdicts, incomplete evidence, and unresolved blocking findings require
**HOLD**. An absent skill never silently passes. If the specification is missing
but an equivalent documented manual review is possible, retain that distinction
and show its evidence instead of claiming the missing skill executed.

**READY** requires all seven stages accounted for under the contract and no
blocking findings. Optional polish may remain with a passing verdict. Validate a
saved report with `python scripts/skills/validate_report.py REPORT.json` from the
repository root. The validator checks the report contract; it cannot prove an
assertion is true or a review actually happened.

## Output

Give the post path/revision, one coverage/verdict/evidence row per stage, blocking
findings first, then optional polish and the derived READY/HOLD decision. Name
unperformed checks explicitly. Preserve enough supporting detail to audit the
decision without dumping repeated reviewer prose. For a consequential thesis,
dense numerical argument, disputed claim, or archive correction, use
[blog-deep-review](../blog-deep-review/SKILL.md) deliberately; it is separate from
these seven stages. Reviewer agreement never substitutes for source verification.
