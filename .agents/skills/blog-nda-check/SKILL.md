---
name: blog-nda-check
description: Review blog and biography attribution for current-work disclosure, insufficient time buffering, identifying details, and misleading homelab framing under repository policy.
license: MIT
---

# Blog attribution and NDA review

Read the NDA rules in [repository policy](../../../AGENTS.md) and the
[review contract](../../../docs/skills.md). Inputs are the requested post or page,
its publication/update dates, and any author-provided provenance. Resolve paths
from the repository root, three directories above this skill.

## Contextual review

Read the entire artifact, including frontmatter, captions, quotations, code
examples, linked artifacts when relevant, and biography text. Formatting does not
make sensitive information safe. Identify who each experience describes and when
it occurred. Review explicit employer references, recent work incidents, present
tense that implies a current engagement, scale or architecture details that could
identify an organization, and references to specific government systems or agencies.

Apply the repository's 2–3 year minimum buffer to the actual incident and intended
publication dates. Do not infer that a displayed page-edit date verifies all
activity claims. A vague past-tense reference is not a license to invent when an
event occurred; unresolved timing or context must remain unresolved.

Distinguish public research attribution from the author's work. A link to a public
NIST standard is not evidence of government employment. Technical use of
"production" can describe software behavior without referring to the author's
employer. Report genuine context rather than matching words in isolation.

Homelab framing must describe real homelab work or an explicitly labeled
illustration. It is not cover for employer incidents, measurements, or secrets.
Never repair a violation by changing "at work" to "in my homelab," inventing a
time buffer, or deleting provenance while keeping a claimed observation. Remove
the unsupported detail, recast it as a clearly hypothetical example where valid,
or obtain the factual context needed to resolve it. Personal anecdotes and
measurement provenance remain subject to factcheck.

## Result

For each finding, quote the minimal relevant passage with line number, identify
the rule and contextual evidence, and suggest a truthful bounded remediation.
Clear prohibited disclosures are blocking; identifying detail or unresolved
current-work attribution also prevents a passing verdict until resolved. Explain
why research citations or technical wording were cleared when they resemble a
mechanical warning. Record scope, coverage, verdict, and unresolved assumptions
under the shared contract. A clean result means no policy violation was found in
the reviewed evidence; it is not a legal guarantee.
