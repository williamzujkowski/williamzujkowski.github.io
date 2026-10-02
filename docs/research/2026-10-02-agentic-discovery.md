# Discovery pass: the agentic development stack — 2026-10-02

Status: discovery and ranking only. No experiments run, no posts drafted.
Workflow: [research-to-blog guide](../blog-research.md). Re-weighted at the author's
request toward **a full agentic development stack and what makes agentic work safe(r)**.

## Lanes

| Lane | Coverage | Record |
| --- | --- | --- |
| Community | HN Algolia (since 2026-08-02, ~40 queries), 8 comment threads, Lobste.rs (hottest, security, ai, vibecoding), GitHub Advisory DB (published ≥ 2026-07-03), primary articles read at source | [community](2026-10-02-agentic-discovery-community.md) |
| arXiv | One rate-limited worker, 22 requests, ≥3.3 s apart; 25 leads, 13 read in full text | [arxiv](2026-10-02-agentic-discovery-arxiv.md) |
| Internal | Every agent-related post, shelved drafts, issues, the author's own agent tooling and session records, mapped onto stack layers | summarized below |
| Nexus | `research_discover` (arXiv; arXiv+GitHub+OpenAlex) seeded 29 unverified leads; all 19 arXiv IDs later confirmed to exist with matching titles | seed only |

Community numbers came through a summarizing fetch tool: recompute every figure from the
primary page before it enters a post. arXiv items are preprints unless stated.

## What the site already covers, and the gaps

| Layer | Covered | Gap |
| --- | --- | --- |
| Instructions / context files | 2025-07-22 | Repo-supplied AGENTS.md, skills and config as **untrusted input** |
| Tools / MCP | 2025-07-29, 2026-06-11, 2026-09-11 | MCP authorization that never executes; scanner reliability |
| Sandbox / egress | 2026-07-02 (survey) | No measurement of the author's own harness |
| Secrets | 2026-07-02 | Misuse explicitly left open; no proxy built |
| Memory | 2026-09-15 | Full recovery drill only proposed |
| Review gates | 2026-07-30, 2026-08-18, 2026-10-22 | **Agent reviewers as a failure mode** |
| Provenance of agent-authored artifacts | indirect (2026-10-08, 2026-10-15) | Unwritten |
| Human approval / authority change | deferred in 2026-07-23 and again in 2026-08-18 | **Unwritten, deferred twice** |

## The convergent theme

All three lanes point the same way: **in an agentic stack the harness, not the model, is
the attack surface, and its controls report success without doing their job.** Examples
from the lanes: repo-local `.git/config` executing outside Codex's sandbox with no model
involved (CVE-2026-19590…19593); aider and Gemini CLI loading repo config into execution;
a goose recipe scanner that does not read the fields that execute; a DB-GPT sandbox that
silently falls back to the host; AGENTS.md silently skipped when telemetry was disabled;
approval records that bind the entry command but not its transitive effects. This is the
site's established "checks that pass for the wrong reason" arc, one layer up.

## Ranking

Weights: reader value to someone building a safe agentic dev stack; extends an existing
post rather than repeating it; a bounded owned lab is feasible (model-free preferred);
evidence quality.

| Rank | Candidate | Lab | Strongest objection |
| --- | --- | --- | --- |
| 1 | **Approving the command approves what it runs**: approval binds `pnpm install`, not its postinstall children; pauses that leak sibling effects. Sources: arXiv 2609.28586v1, 2607.14166v3; human approval miss rates (directional only) | Model-free: synthetic repo + canary lifecycle script; record what a permission rule authorizes vs. the observed process tree, sandbox on and off | Install scripts are long known; the paper is n=17 with no artifact |
| 2 | **The repo is an input**: repo-local config executes before the model is consulted (Codex git-config CVEs, aider, Gemini CLI `.env`, goose), plus silent instruction-file skipping. Source support: arXiv 2609.07360v3 config scanner (Apache-2.0) | Hostile synthetic repo archive, canary, pinned vulnerable vs. fixed versions in a disposable VM; scan the author's own repos | All four CVEs are fixed; risk of a CVE recap. Must show a durable pattern and a check readers can run |
| 3 | **When the reviewer is an agent**: the author's own records (consensus voters reviewing the wrong repository, #595; an access gate whose check never executed, later retired; reviewer findings applied vs. rejected in the October batch) + benchmark-grader validity papers (arXiv 2609.32691v1, 2608.12880v1) | Recompute applied/rejected counts from the October research notes; no new execution | Self-referential; must generalize beyond this repo's tooling |
| 4 | Egress is the boundary: measure what a coding harness sends out (ZCode upload; Docker Sandboxes / Gondolin placeholder secrets) | mitmproxy/DNS logging around a disposable session | Needs a real agent session; risk of capturing real credentials — synthetic workspace only |
| 5 | MCP scanner reliability (arXiv 2607.11086v1) | Synthetic vulnerable/benign MCP servers vs. scanners | LLM scanners need their default backends to be fair |
| 6 | Protected-file read routes in a coding agent (arXiv 2609.35557v1); stdlib shadowing against an auto-approval classifier (Embrace The Red, 2026-08-26) | Canary file / `struct.py` shadow in a container | Only 2 of 15 routes executed in the paper; a working bypass needs a disclosure path before publication |

Ranks 1–3 are proposed as issues [#673](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/673), [#674](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/674) and [#675](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/675). Rank 1 closes the twice-deferred approval gap; rank 2
extends the instruction-file post with a lab; rank 3 uses evidence already on hand.

## Boundaries carried forward

- Author attribution: some of the author's agent tooling is work-adjacent; posts use only
  public, personal projects and this repository's records. Pre-2026 AI-post figures need
  re-verification before reuse (see the 2025 humanization cohort record).
- Running historical vulnerable agent versions: disposable VM, synthetic repo, canary
  payloads only, no network beyond what the canary records.
- Any new bypass found in a current tool is reported to the vendor before a post names it.

Stop reason: all three lanes completed their bounded passes; further queries returned
repeats or product launches without a security mechanism.
