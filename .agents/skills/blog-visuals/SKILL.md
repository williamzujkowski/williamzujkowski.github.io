---
name: blog-visuals
description: Review or create blog diagrams and zine doodles using this site's native visual patterns, accessible markup, theme tokens, and mobile layout conventions.
license: MIT
---

# Blog visuals

Read [repository policy](../../../AGENTS.md),
[the visual contracts](../../../docs/content-visuals.md), and the
[review contract](../../../docs/skills.md). Inputs are the requested post or
visual brief and existing assets. Resolve repository paths from the root, three
directories above this skill. Review alone does not require generating an asset;
create or edit when the task authorizes it.

## Choose and inspect

Inventory `.flow`, `.arch`, `.seq`, tables, code blocks, graphs, and doodles. Ask
what the reader must understand: processes use `.flow`, layers or zones use
`.arch`, actor exchanges use `.seq`, and comparisons use Markdown tables. Split
dense graphs into focused views; Mermaid is legacy for genuine node graphs.
Copy the maintained class contracts from the visual documentation.

Inspect visual claims against the prose and source evidence: diagram arrows,
trust boundaries, chart scales, and labels can overstate a result. Confirm token
colors, the 0.8125rem text floor, mobile reflow, and accessible names/structure.
`.flow` and `.arch` roots need `role="group"` and `aria-label`; mirror tier/branch
labels into accessible markup. Do not introduce one-off classes or hardcoded
theme colors. Check rendered output when layout or assets change.

## Zine asset procedure

For a post otherwise opening as pure text, choose one specific visual metaphor
whose interacting objects carry the idea without a stamped label. Use an
available authorized image tool; avoid embedding provider names, model choices,
permission-bypass flags, or credentials in the portable workflow. A useful brief:
medium-weight confident ink, visible hand-drawn wobble, simple composition on
cream paper, no text or letters. Preserve the user's chosen image tool when given.

Verify that a real file exists and inspect it. Reject generic topic icons, hidden
lettering, or a metaphor that needs its caption to make sense. Use a bounded
iteration budget, normally two revisions; report any remaining gap honestly.
Use `scripts/zine-art/ink-mask.py` from the repository root with its documented
inputs after inspecting its help. Output must be an alpha-masked pure-black PNG
under 60 KB. Confirm actual dimensions, alpha, and size rather than trusting a
tool's success message.

Place the doodle after the introduction and before the next heading, following
the documented markup. Set aspect ratio from the actual asset; keep
`aria-hidden="true"` only because the adjacent prose carries its meaning. A short
caption may add voice. Social cards are generated at build time: do not add
hero-image frontmatter.

## Result and verification

Report visual inventory, metaphor suitability, content accuracy, and accessibility
findings with locations. After changes, build and run the design audit from
`astro-site/`, then inspect the rendered page on mobile and in light/dark decks
using `data-theme-deck`. A broken mask can be invisible or a solid block even when
the build passes. Record performed checks and any unavailable browser/image
capability using the shared contract; do not claim a render review from source
inspection alone. A required visual or accessibility defect blocks readiness.
