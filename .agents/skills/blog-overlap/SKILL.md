---
name: blog-overlap
description: Review a blog draft against this repository's archive for repeated arguments, useful cross-links, and a distinct contribution. Use for overlap checks and finding related posts.
license: MIT
---

# Blog overlap

Read [repository policy](../../../AGENTS.md) and the
[review contract](../../../docs/skills.md). Resolve the requested post against
the repository root, three directories above this skill. Use the current task's
explicit draft; do not silently choose whichever file has the newest timestamp.

## Procedure

1. Read the entire target, including title, date, tags, headings, code identifiers,
   and existing cross-links. State its central claim and intended reader outcome.
2. Search `src/posts/` using distinctive entities, mechanisms, title terms, and
   tags. Common tags such as `security` are discovery hints, not evidence of
   redundancy. Inspect draft and scheduled posts as well as published posts;
   distinguish their status and date in the report. Read the `draft` boolean
   value: a present `draft: false` key does not make a post a draft. Determine
   eligibility using the repository's publication rules and an explicit date
   cutoff; eligibility alone does not prove a deployment happened. If the
   proposed publication date is missing, report link availability as unresolved.
3. Read the strongest candidates in full. Compare the question, thesis, evidence,
   and reader decision with the target. Similar vocabulary can support different
   arguments; different titles can conceal the same argument.
4. Classify overlap as **strong** (substantially the same claim and evidence),
   **moderate** (related problem with a distinct contribution), or **weak**
   (shared subject only). Explain the classification using passages from both
   posts. A cross-link does not reduce substantive overlap.
5. Recommend the smallest useful change: position the new contribution, add a
   relevant link, consolidate a redundant argument, or leave it alone. Check
   whether suggested internal links will be available by the publication date.

Local search is sufficient for this stage. External prior art belongs to
research or deep review. Do not produce precise similarity scores unless an
actual implementation computed them; record its method if used.

## Result

Report the target path, archive/search scope, central claim, and a ranked list
of candidate paths with their dates, shared argument, distinct contribution,
existing link status, and recommended action. Record coverage and verdict using
the shared contract. Evidence includes inspected paths and relevant passages or
line numbers. An unresolved duplicate argument is a blocking finding; an optional
cross-link is polish. If no candidate survives inspection, describe the search
performed instead of claiming the archive contains no overlap with certainty.
