# ZIP article review — 2026-09-13

Target: `src/posts/2026-09-28-zip-index-stream-reader-disagreement.md`.
Schedule: September 28, one week after the existing September 21 page-cache post;
all research and lab evidence was public by September 13. No earlier post is displaced.

The contribution is an inspectable regression case for content identity at a
parser/API handoff. The existing October 2025 scanning article addresses scanner
orchestration and enforcement. Full archive search for ZIP/parser/ZipDiff and
inspection of that article found related security context, not the same test.
The earlier ZIP proposal's scanner/consumer title was narrowed to match actual
API observations: no filesystem extraction, malware or scanner bypass is measured.

## Claim ledger

| Claim | Evidence checked | Verdict and limit |
| --- | --- | --- |
| Identical fixture, indexed/streaming lists differ | Raw report at research-labs68874f0, fixture `local-entry-absent-from-index`, all three runs | Verified; this archive deliberately violates correspondence requirements |
| Each local record needs a central record | PKWARE APPNOTE6.3.10 §4.3.2 | Verified; successful iteration is not validity certification |
| Java streaming reads local metadata | Java21 ZipInputStream API note | Verified; two Java paths are one implementation |
| Python supports duplicate-entry objects | Python3.12 ZipFile.open documentation; adapter opens each ZipInfo | Verified; no name-only lookup or extraction result claimed |
| Six inputs,18 outcomes,17successes/1rejection | Recomputed raw per-fixture results, matching stdout/parsed objects | Verified; three sequence differences, only one marker-decision difference |
| 23tests passed and CI matched | CI34741618089, artifact10312418126 and local retained reference | Verified independently by root and music_pilot; entire adapter result objects match |
| Lab follows established research | USENIX Security2025 You/Chen/Wang/Duan paper §§2,4 and attribution | Verified; original tiny corpus, no fuzzing-campaign replication/novelty claim |
| Docker command and bounds | Immutable Dockerfile, wrapper, generators, Python/Java adapters | Verified source and executed commands; linux/amd64 runtime, no external input interface |

Primary links are in the article and immutable lab README. All quantities describe
these fixed inputs, not prevalence, benchmark performance or production behavior.
The original recommendation is integration testing of entry identity, with
rejection preserved separately from successful absence of a marker.

## Independent review and adjudication

`music_pilot` performed separate factcheck, voice, attribution, argument and
artifact reviews on the whole post using canonical repository skills. It
independently downloaded the CI artifact, recomputed counts and compared source
hashes. It found no blockers. Root separately completed overlap, source checks,
visual/render/accessibility review and the final coverage record.

Nexus `documentation-expert` completed its prose/argument review successfully
using gemini-3.1-pro-preview (90,286ms). It did not browse and relied on the supplied
evidence; no independent network verification is attributed to it. Its requested
Mermaid replacement conflicts with authoritative `docs/content-visuals.md`, which
requires native HTML for this flow. That recommendation was rejected with the
actual policy as evidence. The native flow passed rendered checks.

The separate real scheduling vote `job-vote-49fb636f-5bf3-4efb-87a8-db8e1afa77c5`
completed at06:16:54UTC, producer8.49.3, approved2–1, quick-mode supermajority with
fail_closed and no simulated votes. All three roles used gemini-3.1-pro-preview.
The scope dissent again evaluated the personal blog against the Nexus product's
mission. It remains recorded, not relabeled as assent; independent review and
required checks establish actual scope/correctness. Full tool record:
[2026-09-13-zip-scheduling-vote.json](2026-09-13-zip-scheduling-vote.json).
No retry for a preferred vote was made.

## Verification

Future preview at `PUBLICATION_AS_OF=2026-09-28T00:00:00Z` built successfully.
Root inspected full-page screenshots at1440px Latte and390px Dracula: readable
native flow/table, no horizontal page overflow and no missing assets. Targeted
axe WCAG2/2.1/2.2AA found zero violations in both views, with the repository's
existing syntax-highlighted-code contrast exclusion. The visual is a specific
mechanism diagram after the introduction; no decorative doodle is necessary.

Design audits, Astro check and lint passed. The seven-stage coverage JSON binds
the final file hash. Production build and required PR checks must pass before
merge; today’s build must exclude the future post. No general archive-ready
verdict is implied for the older scanning article merely because it is linked.
