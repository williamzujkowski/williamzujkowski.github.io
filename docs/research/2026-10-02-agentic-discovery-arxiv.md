# arXiv discovery lane — agentic dev-stack safety (2026-10-02 UTC)

Worker: sole arXiv fetcher. Access window 2026-10-02T02:04:13Z – 02:06:56Z (UTC).
Rules followed (docs/blog-research.md §1-2): one connection, sequential, >=3.0 s
between requests (measured min gap 3.33 s), cache-before-fetch, stop on 403 (none seen).
Raw cache: `disc2/arx/` (`requests.log`, `*.xml`, `ft/*.html|pdf|txt`, `fetch.py`).

## Request count: 22 arXiv requests
- 2 × API `id_list` metadata batches (19 Nexus leads; 25 own-query candidates)
- 7 × API `search_query` (sorted submittedDate desc, max_results=30, filtered to >= 2026-07-04)
- 13 × full text (10 HTML 200, 1 PDF 200, **3 × 404 on /html/2607.14166v3**: my fetcher
  retried a 404 twice with backoff before falling back to PDF. Within the rate limit but
  wasteful; a 404 should not be retried. Recorded, not hidden.)
- Non-arXiv checks: 7 `gh api repos/...` + 1 PyPI JSON (artifact existence/licence only).

## Queries (API syntax)
| # | query | in-window hits |
|---|---|---|
| L | id_list of the 19 Nexus leads | 19/19 resolve; titles match the lead list |
| Q1 | `(cat:cs.CR OR cat:cs.SE OR cat:cs.AI) AND abs:"coding agent" AND (abs:sandbox OR abs:permission OR abs:permissions)` | 18 |
| Q2 | `(cat:cs.CR OR cat:cs.SE) AND abs:"prompt injection" AND (abs:repository OR abs:"pull request" OR abs:issue OR abs:AGENTS.md OR abs:"instruction file")` | 20 |
| Q3 | `(cat:cs.CR OR cat:cs.SE) AND (abs:"Model Context Protocol" OR ti:MCP) AND (abs:scanner OR abs:vulnerab OR abs:security)` | 24 |
| Q4 | `(cat:cs.CR OR cat:cs.AI) AND abs:agent AND abs:memory AND (abs:poisoning OR abs:injection)` | 30 (cap hit, truncated) |
| Q5 | `(cat:cs.CR OR cat:cs.SE OR cat:cs.AI) AND abs:agent AND (abs:exfiltration OR abs:egress) AND (abs:secret OR abs:credential OR abs:network)` | 15 |
| Q6 | `(cat:cs.CR OR cat:cs.SE OR cat:cs.AI) AND abs:benchmark AND abs:agent AND (abs:"construct validity" OR abs:"evaluation validity" OR abs:"harness bug" OR abs:"false negatives" OR abs:"silent")` | 30 (cap hit; mostly off-topic) |
| Q7 | `(cat:cs.SE OR cat:cs.CR) AND (abs:"agent-authored" OR abs:"AI-generated pull requests" OR abs:"agentic pull requests" OR abs:"code review") AND abs:agent AND (abs:security OR abs:provenance)` | 7 |

Coverage gaps: Q4/Q6 hit the 30 cap (older in-window items not seen); Q7 found little on
provenance/review of agent-authored code; no unbounded prior-art search was run (time budget).

## Leads table (identity from arXiv API; all v1 unless noted; status = arXiv comment field only)
| # | ID (ver) | Title (short) | Authors (first; n) | Submitted | Status/venue | Tier |
|---|---|---|---|---|---|---|
| 1 | 2609.07360v3 | Scanning the Harness: Configuration Exposures in AI Coding-Agent Supply Chains | Kapner; 4 | 2026-09-07 (v3 09-25) | preprint; v3 "corrected counts" | DEEP |
| 2 | 2607.11086v1 | Rethinking MCP Security: Runtime MCP Servers and Security Scanner Reliability | P. Chen; 9 | 2026-07-13 | preprint (extends arXiv:2512.15144) | DEEP |
| 3 | 2609.32691v1 | Silent Failures in Agentic Security Evaluation: A Validated Harness for Tool-Call Mediation | A. Shaw; 1 (independent) | 2026-09-26 | preprint, 7 pp | DEEP |
| 4 | 2608.12880v1 | Labels Are Not Endpoints: Treatment Leakage and Construct Validity in MCP Agent Security Evaluation | R.M. Ahmed; 2 | 2026-08-13 | preprint | DEEP (skim) |
| 5 | 2609.28586v1 | Agent Approval Laundering: Transitive Effects Beyond the Approved Invocation | J. Zhang; 7 | 2026-09-23 | preprint | DEEP |
| 6 | 2607.14166v3 | Stop Means Stop: Enforcement Gap in Agent-Framework Control Primitives | S. Khan; 1 (independent) | 2026-07-15 (v3 08-08) | preprint | DEEP |
| 7 | 2609.35557v1 | The Compiler May Read It, the Agent May Not | S. Roy; 1 | 2026-09-28 | preprint, 6 pp | DEEP |
| 8 | 2609.08371v1 | Authority Is Not a String: CapScope | Bouras, Dai, Mechtaev | 2026-09-08 | LMPL '26 workshop (per paper header) | DEEP |
| 9 | 2607.14611v1 | Bad Memory: Prompt Injection Risks from Memory in Agentic Systems | Gadgil; 4 (incl. Roesner) | 2026-07-16 | preprint (ACM template placeholders left in) | DEEP |
| 10 | 2608.27092v1 | The Framing Gap: IPI Exfiltration Defeats Surface-Level Defenses | Rahman, Kim | 2026-08-27 | preprint | DEEP (skim) |
| 11 | 2609.22510v1 | Defusing Explosive Prompts: Trigger-Based Prompt Injections | Szczepaniak; 4 (incl. Nassi) | 2026-09-18 | preprint | abstract |
| 12 | 2607.05120v1 | Agent Data Injection Attacks are Realistic Threats | Choi; 6 | 2026-07-06 | preprint | abstract |
| 13 | 2608.27299v1 | When Context Gets Root: Privilege Escalation in LLM Harnesses | X. He; 9 | 2026-08-27 | preprint | abstract |
| 14 | 2607.23624v3 | Third-Party API Routers for Agentic Software Development | D. Fu; 4 | 2026-07-26 (v3 09-05) | preprint | abstract |
| 15 | 2609.13889v1 | Persistent Memory Poisoning Attack on Harness-Based Agents (PMPA) | S. Huang; 3 | 2026-09-12 | preprint; code MIT | abstract |
| 16 | 2609.14119v1 | Same Name, Different Server: Silent Drift in MCP | O. Kraishan; 1 | 2026-09-12 | preprint | abstract |
| 17 | 2608.00997v2 | Registry Descriptions Go Stale Unevenly (MCP drift, 89 days) | G. Bharti; 1 | 2026-08-02 (v2 08-04) | preprint; v2 self-corrects 5 claims; data CC-BY-4.0 Zenodo | abstract |
| 18 | 2609.18217v1 | Implicit Trust in LLM Tool-Calling Pipelines (cross-channel fragmentation) | Ediga, Chattopadhyay | 2026-09-16 | preprint | abstract |
| 19 | 2608.02670v1 | Permission Denied: Coding Agents in Hardened Environments | Davidovich; 4 | 2026-08-02 | preprint | abstract |
| 20 | 2608.30686v1 | Beyond the Payload: User Invocation and Repository Poisoning (CIPR) | F. Zhu; 6 | 2026-08-31 | EMNLP 2026 main (per comment) | abstract |
| 21 | 2609.39678v1 | Aletheia: Permission-Minimality Testing for Coding-Agent Rules | J. Shi; 5 (incl. D. Lo) | 2026-09-30 | preprint, 6 pp | abstract |
| 22 | 2607.19267v1 | They'll Verify. They Just Won't Act. (agentic CI/CD laundering) | Y. Sidot; 1 | 2026-07-21 | preprint; code MIT | abstract |
| 23 | 2609.33371v1 | API Secrets Should Never Become Tokens (vault-mediated boundary) | Kenney; 5 | 2026-09-27 | preprint; evaluates authors' own product (Corvic) | abstract |
| 24 | 2607.05743v1 | Balkanization of Execution-Security Research for AI Coding Agents (SoK, 39 papers) | M. Rashidi; 1 | 2026-07-07 | preprint | abstract — useful prior-art map |
| 25 | 2608.14876v1 | Workspace Topology as an Attack Vector in Agentic Coding Assistants | A. Day; 12 | 2026-08-14 | CAMLIS 2026 (per comment) | abstract |

Also seen, not ranked: 2610.01349 PACE; 2609.22818 Price of Safety (memory-defence false
quarantines 33.6%); 2608.20658 Claws in Plain Sight; 2607.25619 SkillGate; 2608.00150 Exposed by
Design; 2609.27263 gh-aw empirical study; remaining Nexus leads (ActGuard, ECLIPSE, SecOPD,
SkillShield, A2M, ChainWatch, FlowGuard, WeClawArena, Web3 survey, UCM, How Agents Ask for
Permission) — legitimate-looking but either attack/defence-of-the-week or not checkable
against tools the author runs. ChainWatch (2607.19432) is a "demonstrate on 5 scenarios"
framework paper with no measured evaluation in the abstract: weakest of the set.

## Deep notes (top 8)

### 1. 2609.07360v3 — Scanning the Harness
- Unit: repository declaration at pinned commit; 3,171 repos (2,660 "setups", 511 skill
  collections) from a 9,295-candidate funnel built from topics/curated lists (not a probability sample — they omit CIs for that reason).
- Headline (Table 1): unpinned MCP package declaration 260/2,660 = 9.8% (24.5% of 1,063 setups
  with MCP config); broad execution grant 67 (2.5%; 12.6% of 533 with hooks/settings); broad
  skill `allowed-tools` 101 (3.8%); any S-exposure 409 (15.4%); any finding 475 (17.9%).
- Validity work: separate re-derivation script (8,549 records, 112 refuted); model adjudication
  (claude-fable-5-1) on 158 disputed pairs; one-author manual review 93.3% agreement overall,
  70.7% on the 157 model-adjudicated pairs. **v3 correction: scanner and audit both counted
  `Bash(find:*)` as arbitrary exec; Claude Code docs say wildcard grants exclude `-exec`/`-delete`
  — 62 findings removed.** Shared-error case: two implementations by the same team agreed and were both wrong.
- Artifacts: tool `redhat-community-ai-tools/harness-eval` (Apache-2.0, created 2026-06-01,
  pushed 2026-09-30); data `Benkapner/harness-eval-experiments` (licence NOASSERTION; **last push
  2026-09-07, before v3 on 09-25** — check whether the v3 reanalysis script is actually there).
- Threat model: a changed dependency or untrusted instruction exercises capability the agent
  holds; runtime consequence explicitly unmeasured; recall unmeasured.
- Owned-lab feasibility: HIGH, no LLM. Run harness-eval against the author's own repos
  (`.mcp.json`, `.claude/settings*.json`, skills, `nexus-agents.yaml` setups) plus a planted
  positive/negative control (an `npx -y pkg` unpinned decl + a pinned one; `Bash(find:*)` to test the v3 fix).
- Strongest objection: a declaration is not an exposure (npx cache, Docker pull policy, client
  semantics); "unpinned npx" overlaps long-known lockfile advice; scanner authors audit their
  own scanner.

### 2. 2607.11086v1 — MCP scanner reliability (MCPZoo)
- 64,611 unique servers, 37,288 interactable; 8 scanners with >200 stars (Snyk Agent-Scan,
  Tencent A.I.G static/dynamic, Cisco MCP-Scanner, Ant MCPScan, MCPSafetyScanner, Lasso
  mcp-gateway, nova-proximity, mcp-armor).
- 96.89% of interactable servers flagged by >=1 scanner; **none flagged by all eight**;
  per-scanner flag rate 0.54%–80.04%; prompt-injection flag rate 0.02%–76.58%.
- Precision (Table 7): 100 sampled flagged servers, stratified; two reviewers + tiebreak; avg
  precision 45.53%, range 10.40%–96.88%; e.g. Agent-Scan 22/78 = 28.21%, A.I.G static 49/86 = 56.98%.
  Low-volume scanners most precise. Recall from a CVE ground-truth set (Appendix D), e.g. 16/32.
- Caveat that matters: **LLM-based scanners were re-pointed at a local Qwen3-235B-A22B**, timeout
  1500 s, ≤5 iterations — not their default backends; Agent-Scan hit vendor 429s. Precision is
  for that configuration.
- Licence CC BY-NC-ND 4.0 (no derived figures). Public query interface claimed (URL footnote not extracted).
- Owned-lab feasibility: MEDIUM-HIGH. Build 4–6 synthetic MCP servers (known command
  injection, path traversal, a harmless server with scary wording, a placeholder "API_KEY=xxx"),
  run 2–3 open scanners locally. Positive AND negative control as per the site's rules. LLM-backed
  scanners need a local model or paid key — note it.
- Strongest objection: scanner configs non-default; "true positive" required demonstrable
  reachable flaw, which penalises scanners designed to flag capability risk by intent.
  Prior art: FlowGuard (2607.14754, same group) proposes the evidence-grounded fix — same authors.

### 3. 2609.32691v1 — Silent Failures in Agentic Security Evaluation (+ 4. 2608.12880v1)
- Four defect classes in an audited IPI harness: D1 payload placed only if a free-text field
  matched one of 4 hardcoded literals → 39/43 payloads never delivered, still counted as
  trials; D2 attack success by tool name, not args → **21.7% vs 1.2% on identical traces
  (258 attack runs)**; D3 env errors charged as false rejection (10.3% vs 6.7%, 282 benign
  runs; undefended baseline had nonzero FRR, impossible by construction); D4 no traces.
  llama3.1:8b "62.8% ASR" → 0/43 under corrected harness (reached the payload in 41/43).
- Fix: loader rejects unresolvable locators/unfireable predicates; per-scenario environments;
  argument-level predicates; mandatory traces. Power analysis stated up front; frontier ASR
  2.3% [0.4, 12.1] — defences not distinguishable at n=43.
- **Red flags**: the audited benchmark is never named or cited, nor is the "prior report" of
  62.8% or the gemma "tool-binding barrier"; no artifact URL in the paper despite "released as
  open source"; attack suites withheld; single independent author; model "gpt-5.6-terra"
  unverifiable from outside. It reads like a self-audit of the author's own earlier harness
  without saying so. Cannot be checked as written.
- 2608.12880 (Labels Are Not Endpoints) is the honest version of the same story: the authors
  audit **their own** MCP campaign; the grader used `adversarial_payload_present` (derived
  from treatment) to gate ATTACK_SUCCESS, so CLEAN runs could not score positive. Re-grading
  moved 58 labels to benign; locked v2 has **zero** ATTACK_SUCCESS; 3 verified protected-data
  transfers + 1 forwarding case remain. "Reproducibility did not prevent the error. It made the
  error exactly reproducible." Linked repo `rana-m-ahmed/ResearchWork-on-Mcp-Privilege-Aggregation` **returns 404**.
- Owned-lab feasibility: HIGH with a local model (Ollama) and mock tools: build the toy harness,
  plant D1/D2/treatment-leak defects, show the same traces producing different headline numbers.
  This is "plant the defect, watch the gate" (scheduled 2026-10-22) applied to a security benchmark.
- Strongest objection: AgentDojo already defines the utility/ASR triple and argument-level
  checks; "benchmarks have bugs" is generic unless the audited benchmark is named.

### 5. 2609.28586v1 — Approval laundering
- Claim: coding-agent approval records bind the entry command, not its transitive effects.
  Vite@64dfee12 `pnpm install --frozen-lockfile` (pnpm 10.34.3) → postinstall runs
  simple-git-hooks, writes `node_modules/.modules.yaml`; MCP docs-tool call in
  modelcontextprotocol/servers@7b1170d1 also exercised network.
- Numbers: 111 approval/trace pairs, residual records 40 → 17 (command semantics) → 13 (+metadata);
  11 fixed-SHA runs 10 → 2 → 0; holdout 17 workflows macro recall 0.926 / precision 0.941;
  frontends Claude Code (2.1.205 PreToolUse hook integration), Copilot CLI, Qwen Code.
  Disclosed to Anthropic/GitHub/Alibaba.
- **No artifact**: "paper-only ... does not include a public artifact URL, the experiment
  ledger, or raw execution captures."
- Owned-lab feasibility: HIGH, no LLM required for the core claim: a synthetic repo with a
  root `postinstall` + a dependency build script, approve `pnpm install` in Claude Code (or
  replay the command), diff filesystem/strace effects; contrast pnpm 10 `onlyBuiltDependencies`/
  `allowBuilds` default. A Claude Code PreToolUse hook that annotates predicted effects is a nice build.
- Strongest objection: install scripts running on install is documented npm behaviour and old
  prior art (Latch, npm ecosystem studies, `--ignore-scripts`); the contribution is a formal
  vocabulary and 17-case holdout, heavy jargon for a known mechanism. n is small.

### 6. 2607.14166v3 — Stop Means Stop
- Model-free differential probes on LangGraph 1.2.7, LlamaIndex Workflows, Microsoft Agent
  Framework, OpenAI Agents SDK 0.17.7, CrewAI 1.15.11, LangGraph.js 1.4.7: approval gate pauses
  its own branch while a sibling effect commits ("sibling leak") in 5/6 (all with a pre-execution
  gate); replay double-execution, cancellation orphans, timeout zombies. Live: 215/1,200
  unmediated leaks, P(leak|emitted)=1.00; plan-shape emission up to 14%.
- Repair SOUNDGATE (Rust; Verus/TLA+/TLAPS/Loom claims). Artifact now public:
  `sajjadanwar0/soundgate-paper` (MIT, pushed 2026-10-02); PyPI `soundgate` 0.1.3 MIT.
- Owned-lab feasibility: VERY HIGH, no LLM: a 30-line LangGraph graph with two parallel nodes,
  one `interrupt()`, one side effect that writes a sentinel; reject, check the sentinel.
- Strongest objection: "barrier semantics" is an implied contract; maintainers may call
  superstep semantics by design. Not Claude Code/Codex — less direct to the author's stack.
  The verification stack is ambitious for a single independent author; verify claims in the
  artifact before citing them.

### 7. 2609.35557v1 — The Compiler May Read It, the Agent May Not
- Claude Code specifically: the vendor doc says sandbox "applies only to Bash, PowerShell, and
  Monitor commands and their child processes", built-in file tools use the permission system
  instead. 15 read routes × 4 mechanisms (container, permission rules, sandbox, instruction
  file) = 60 cells; **only 2 routes executed** (direct read, encoder; both denied July 2026
  against a decoy tree); 21 cells are reasoning, 30 uniform by construction; 5 routes covered
  by neither (allowed build target recipe, compiler print mode e.g. `-E`, git history, ...).
  Deny list grew 118, 13, 4, 0 command names over 5 weeks. Proposed fix: a second-user
  trusted broker (approximation, with costs). Ancillary scripts on arXiv.
- Owned-lab feasibility: HIGH (needs Claude Code, which the author runs): decoy-file tree,
  copy the deny rules, try each route; measured where the paper only reasoned.
- Strongest objection: single rater, 13/15 untested, vendor docs move; overlaps
  2026-07-02 sandbox/secret-proxy post.

### 8. 2609.08371v1 — CapScope
- Pi coding agent (earendil-works/pi, MIT); per-sub-agent typed capabilities outside context;
  5 tasks × 5 surfaces (README, agent-instruction file, skill, docstring, pytest output) × 4
  conditions × 3 trials = 300 runs. Injected effect 33–47/75 (baselines) vs 3/75 CapScope;
  repairs 68/75 vs 68–72/75. Single model qwen3.5-flash **via a third-party OpenAI-compatible
  router ("CloseAI")** — the trusted path 2607.23624 says can rewrite responses. Artifact on figshare (licence not checked).
- Feasibility: MEDIUM (needs an LLM; local model plausible with Pi). Objection: one model, 3
  trials/cell, tiny tasks, preflight ceiling is itself LLM-generated; CaMeL is prior art.

### (9–10, skimmed) Bad Memory 2607.14611; Framing Gap 2608.27092
- Bad Memory: threat model assumes the payload is already in CLAUDE.md/AGENTS.md (getting it
  written there "did not trivially succeed"); 10 trials/cell; Claude Haiku 4.5, Opus 4.7,
  GPT-5.2/5.5; nice qualitative finding: GPT-5.2 moved a vulnerable-pin rule *into* AGENTS.md.
  Artifact anonymous.4open.science. Objection: following CLAUDE.md is the documented design;
  overlaps 2026-09-15 memory post. Needs paid models.
- Framing Gap: canary secret, record-only mock tools, gpt-4o/mini + 4 Ollama models; overt
  injections refused, "integrity signature/config field" reframing → gpt-4o 0%→100%;
  destination allow-list and planner/reader split → 0% (by construction). No artifact URL.
  Feasible locally with Ollama. Objection: allow-list closing exfil is tautological; overlaps
  2026-07-02 secret-proxying post.

## Prior-art / overlap check (repo, read-only)
`rg` over src/posts and `gh issue list --state all`: related published posts are
2026-07-02 (sandbox vs secret), 2026-07-23 (agent controls as OSCAL), 2026-07-30 (prove the
gate), 2026-09-11 (read-only MCP DB role), 2026-09-15 (agent memory recovery), 2025-07-29
(MCP standards server); scheduled 2026-10-22 "Plant the defect, watch the gate". Issue #443
(authority that changes during operation, closed) touches CapScope's subject. No post or issue
covers MCP scanner reliability, harness-config exposure scanning, approval laundering, or
agent-security benchmark validity.

## Stop reason
Bounded pass complete: 25 leads tabled, 8 read in full text (2 skimmed further), artifacts
checked for the top set. Stopped at the ~25-lead budget, not because results ran out (Q4 and
Q6 hit the 30-result cap). No throttling or denial encountered.
