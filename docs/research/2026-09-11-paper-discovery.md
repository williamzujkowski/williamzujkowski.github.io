# Paper discovery and editorial follow-ups — 2026-09-11

Status: researched proposals; no experiments run and no new posts published.
Workflow: [research-to-blog guide](../blog-research.md).

## Discovery and selection

The corpus at discovery contained 95 Markdown posts: 92 published and three
drafts. Review included drafts, [shelved work](../shelved-drafts/README.md), and
open and closed issues. Historical reports already marked SUPERSEDED remain
historical; their recommendations were not reused as current evidence.

Nexus `research_discover` searched arXiv for “systems security reproducibility
benchmarks” from 2025-01-01, with five requested results. It reported no failed
sources, five found, one filtered and four new metadata leads. Those leads were
not promoted: their broad reproducibility/agent focus offered a weaker fit than
the concrete systems questions below. A separate systems search for “systems
tail latency coordinated omission” returned three weakly related leads and no
failed sources. No novelty or factual claim rests on these search results.
Nexus `research_query` returned no matches for “blog paper systems”; that registry
result does not replace the local editorial overlap review.

Three parallel reviewers examined security research, systems/creative-computing
research, and the existing editorial workflow. Primary proceedings, papers,
author errata and artifact documentation supplied the shortlisted evidence.
Publication year was not a ranking score: an older paper with a useful experiment
beat a recent abstract with no distinct reader question.

## Shortlist

| Suggested order | Reader question | Primary research | Why develop it |
| --- | --- | --- | --- |
| First | Did the scanner and installer read the same ZIP? | [My ZIP isn't your ZIP, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/you) | A small parser comparison can show a concrete security assumption failing without executing a payload. |
| Second | The outage ended; why did the retries continue? | [Metastable Failures in the Wild, OSDI 2022](https://www.usenix.org/conference/osdi22/presentation/huang-lexiang) | Measure useful completions and recovery, extending the existing general resilience post. |
| Third | Can two editors agree on a broken drum pattern? | [The Art of the Fugue, arXiv v3](https://arxiv.org/abs/2305.00583v3), [TPDS 2025 DOI](https://doi.org/10.1109/TPDS.2025.3611880) | Connect distributed text semantics to live coding, distinct from browser automation. |
| Fourth | Who shares your DNS cache? | [DNS FLaRE, USENIX Security 2025](https://www.usenix.org/conference/usenixsecurity25/presentation/moav) | Separate transport privacy from cache state, with a more involved local network experiment. |

This pass expanded the guide's adjustable three-issue default to four because
these independently reviewed questions cover distinct mechanisms and reader uses.
This order is editorial judgment, not a measured quality score. Each proposal
issue records the nearest existing post, sources, planned controls, falsifier,
resource limits and acceptance criteria. All resource figures are estimates or
proposed caps. Source discovery does not establish available lab hardware.

### Evidence boundaries that change the plans

- ZIP: the [full artifact appendix](https://www.usenix.org/system/files/usenixsecurity25-appendix-you.pdf)
  recommends 128 GB RAM and 300 GB disk. The proposal is a tiny three-parser
  adaptation, not a reproduction of the full 50-parser study. Distinguish parser
  rejection from successful extraction with different outputs.
- Retries: a temporary slowdown alone is not metastability. Degradation must
  persist after removal of the trigger. Count original requests, retries and
  abandoned work separately, including negative results.
- CRDTs: the [authors' 2019 errata](https://martin.kleppmann.com/2019/03/25/papoc-interleaving-anomalies.html)
  invalidate the older definition and construction. Use the successor paper;
  distinguish Fugue from FugueMax and convergence from preservation of musical
  intent. Keep all pattern text inert.
- DNS: current browser mitigations can affect reproduction of the published
  attack. The proposal tests synthetic cache isolation, not a current browser
  exploit or real users' browsing histories.

## Verified maintenance findings

- Author-time overlap parsing drops block-style tags: a minimal fixture returns
  an empty tag string; 64 current posts use block lists. Page prose extraction
  also retains JavaScript from a multiline script fixture. Both need focused
  regression fixes, not another content gate.
- Active documentation incorrectly exempted About/Now from attribution rules
  and described mechanical NDA checking as blocking. The workflow change fixes
  these contradictions while preserving advisory mechanical checks.
- Author-local pre-publish/factcheck skills have stage-count, missing-review,
  image-frontmatter and evidence-guidance drift. These remain author-local
  maintenance; repository edits alone cannot repair the installed copies.
- The DoH post overstates privacy. [RFC 8484 §8](https://www.rfc-editor.org/rfc/rfc8484.html#section-8)
  distinguishes the encrypted path from server-side correlation.
- The private-cloud post contradicts itself about ZFS-over-iSCSI backups; the
  inspected [upstream backend](https://github.com/proxmox/pve-storage/blob/master/src/PVE/Storage/ZFSPlugin.pm)
  supports VM images. Backup storage needs a separately supported target.
- The resilience post has incident and measurement claims without identified
  public or homelab provenance. That is an evidence gap, not proof of fabrication.

## Planning and review record

Nexus `execute_spec(dryRun: true)` parsed six requirements and five acceptance
criteria into a task graph. It performed no implementation or validation. Its
generic graph classified research as code and omitted real research dependencies;
the working order was source verification → proposal review → issue filing,
alongside documentation → independent review → relevant checks → PR.

The first real three-role unanimous vote
`job-vote-34703d7d-4e51-494a-be08-45bd4d096d11` rejected the plan **2–1**.
The scope voter incorrectly assumed this was the Nexus product repository and
that existing templates covered the request. The useful concern was process
sprawl; the implementation stays within one guide, one template, an AGENTS link
and two policy wording corrections. A second vote supplied the actual blog repo,
the user's explicit request, and the absence of an existing template.
`job-vote-e74237e8-7c84-4f61-8f3c-2efeb286fe71` returned three approving role
votes but an overall **no_quorum** verdict: its absolute-quorum quick-mode
contrarian check errored. This is not an approval; no-quorum remains recorded
despite the role tally. Votes do not establish paper accuracy or authorize
publication.

The final summary review `job-vote-c8202293-edad-49ce-a50d-82d273128baf`
returned **rejected, 0–3**. Each voter treated reviewing this external blog repo as
outside its Nexus-product mission, rather than evaluating the supplied change.
No successful consensus approval is claimed. Repeated attempts stopped; the
completed independent source/diff reviews and required checks inform the merge
judgment under existing user authorization. Integration investigation is tracked
in [#595](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/595).

All three rounds' voters used `gemini-3.1-pro-preview`; these are distinct
roles, not independent model families. No simulated votes were used.

## Tracking

- Workflow and policy corrections: [#585](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/585).
- Author-time parsing defects: [#586](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/586).
- Author-local skill maintenance: [#587](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/587).
- Retry recovery proposal: [#588](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/588).
- CRDT music proposal: [#589](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/589).
- Resilience provenance review: [#590](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/590).
- ZIP parser proposal: [#591](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/591).
- DNS cache proposal: [#592](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/592).
- DoH privacy correction: [#593](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/593).
- ZFS storage correction: [#594](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/594).

## Independent validation

A reviewer checked the ten editorial/workflow issue bodies and this report, then walked the guide
through the 2019 interleaving-paper scenario. The guide led to the errata and
successor version, corpus checks, a bounded inert-text experiment and separate
convergence/non-interleaving claims. This was a read-through scenario, not an
executed experiment or proof of future agent compliance.

Review removed an unsupported available-hardware assumption from the ZIP issue,
made the template workflow URL absolute for issue rendering, and corrected the
page-audit docstring's remaining suggestion that omitted reviews do not apply.
Ruff and whitespace checks passed; all six local guide links resolve. Comparing
Python ASTs with the module docstring removed confirms no runtime change. Existing
required PR checks remain the merge condition; no new content gate was added.

The first PR security scan misclassified editorial wording in the issue template
as a generic API key. The prompt was rewritten in plain sentences without adding
a scanner exception. Python tests passed on that revision; the amended revision
requires fresh CI before merge.
