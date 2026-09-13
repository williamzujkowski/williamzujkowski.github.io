# Portable skills validation — 2026-09-13

Scope: repository-owned blog skills for issues #587 and #619. These are bounded
author-time checks, not a claim that every review stage has been behaviorally
validated in every harness.

## Sources and discovery

The [Agent Skills specification](https://agentskills.io/specification) defines
the package and metadata. Discovery paths are a client concern. Official
[Codex documentation](https://learn.chatgpt.com/docs/build-skills),
[Gemini CLI documentation](https://geminicli.com/docs/cli/skills/),
[Claude Code documentation](https://code.claude.com/docs/en/skills), and
[VS Code documentation](https://code.visualstudio.com/docs/agent-customization/agent-skills)
were fetched during this review. See [the maintained discovery matrix](../skills.md)
for the resulting instructions.

Before creating `.agents/skills`, `gemini skills list` returned no skills. After
creation, it listed all nine blog skills as enabled, with locations under this
checkout's `.agents/skills/`. This proves local discovery in Gemini CLI 0.51.0;
it does not prove that a model can execute the skills with this account.

Claude Code documents `.claude/skills` project discovery and personal-before-
project precedence for duplicate names. This migration uses an explicit path
adapter instead of making another procedural copy. No personal skills were
deleted or replaced by the validation runs.

## Behavioral task

The review prompt proposed another guide to implementing DNS-over-HTTPS with
Pi-hole and dnscrypt-proxy to prevent ISP monitoring. It asked each harness to
use `blog-overlap`, inspect archive metadata, read the closest existing post
fully, and report the canonical skill path, corpus scope, overlap verdict, and
publication recommendation. It explicitly prohibited edits, web browsing, MCP,
delegation, and any claim that other review stages had run.

Exact Codex prompt (the shell preserved the literal `$`):

```text
Use $blog-overlap to evaluate this proposed blog topic against this repository: Implement DNS-over-HTTPS on a home network with Pi-hole and dnscrypt-proxy to prevent ISP monitoring. Read the closest existing post fully and inspect corpus metadata for other overlaps. Do not edit files, browse the web, delegate, or invoke MCP. Report the resolved skill file, exact corpus scope, closest existing post, decision about publishing another deployment guide, and coverage/verdict for overlap only. Do not claim other reviews ran.
```

Exact initial agy prompt:

```text
Read-only portability evaluation. Read .agents/skills/blog-overlap/SKILL.md and docs/skills.md explicitly from /home/william/git/williamzujkowski.github.io and apply that canonical procedure. Evaluate this proposed blog topic against the repository: Implement DNS-over-HTTPS on a home network with Pi-hole and dnscrypt-proxy to prevent ISP monitoring. Read the closest existing post fully and inspect corpus metadata for other overlaps. Do not edit files, browse the web, delegate, or invoke MCP. Report resolved skill file, corpus scope, closest existing post, decision about publishing another deployment guide, and coverage/verdict for overlap only. State this is an explicit-file-read invocation, not a native discovery test. Do not claim other reviews ran.
```

This is a proposal-level overlap test. There is no new full draft or proposed
publication date; a reviewer must preserve that limitation. The existing
2025-07-08 guide is the obvious substantive duplicate. Successful behavior means
identifying that duplicate with file evidence, keeping related filtering or
segmentation posts distinct, and avoiding an aggregate `READY` result.

## Execution controls and account failures

- Codex CLI 0.154.0: `codex exec --sandbox read-only --ephemeral --json`, with
  native `$blog-overlap` name invocation and a 180-second process timeout.
- Claude Code 2.1.266: explicit canonical-path invocation, `--permission-mode
  dontAsk`, only `Read,Grep,Glob` tools, no MCP servers, no session persistence,
  and a 180-second process timeout. The run returned HTTP 429 before inference:
  usage credits exhausted; reported input and output tokens were both zero.
  This run does not count as skill activation or completion.
- Gemini CLI 0.51.0: read-only `--approval-mode plan` invocation, with a
  180-second process timeout. Account setup returned `IneligibleTierError`,
  stating the client is no longer supported for the account's individual tier
  and directing migration to Antigravity. Native discovery succeeded separately;
  execution did not.
- agy: explicit canonical-path invocation using an available
  `gemini-3.1-pro-high` model, `--mode plan --sandbox`, a three-minute print
  timeout, and a 210-second outer process timeout. This tests explicit reading,
  not agy native skill discovery. The changelog command identified 1.2.2 as its
  latest entry; that alone is not an installed-binary version assertion.

No permission-bypass flags or direct paid API calls were used. CLI authentication
was inherited from the installed local harnesses. The failing clients were not
retried with purchased credits, another identity, or weaker permissions.

## Observed outcomes

Codex completed with exit status 0. Name invocation resolved the canonical
`.agents/skills/blog-overlap/SKILL.md`; the log records reading it and the shared
contract. It inventoried 96 Markdown posts, distinguished 93 eligible posts from
three scheduled posts (no explicit drafts), and read the three strongest
candidates fully. Its ranked result separated the duplicate DoH deployment guide
from a related Raspberry Pi project guide and a monitoring/automation post. It
reported `coverage: completed`, `verdict: fail` for proposal overlap, named the
missing draft/date, and made no aggregate readiness claim.

The first agy run completed with exit status 0 in 54 seconds. Its report identified
the canonical file, the duplicate DoH guide, and the same overlap-only
`completed`/`fail` result. It explicitly labeled invocation as a file read.
However, its result omitted the required candidate ranking and publication-date
scope. The plan-mode harness wrote local report artifacts and added a needless
confirmation request. No repository files were changed. This first result
demonstrates application of the core duplicate check, with incomplete procedural
reporting; a bounded follow-up requested the omitted evidence.

Exact agy follow-up prompt:

```text
Your overlap report omits required evidence. Complete the existing review: inspect metadata across src/posts to report exact corpus size/date scope and draft/scheduled status; read strongest related candidate posts fully and report ranked candidate paths/dates, shared argument vs distinct contribution, and existing link status. Give inspected passages or line evidence from post bodies, not just the description. Report exact tool-read ranges if available so full reads are verifiable. Use local read-only tools only, no web/MCP/delegation. Return the findings directly in your response, with scoped coverage/verdict and limitations. Do not create/edit plan artifacts or request approval: the authorized task is review only.
```

The agy follow-up completed with exit status 0 in 162 seconds and returned its
findings directly. It supplied two ranked candidates, full-file read ranges,
body quotations, link status, and the distinction between `dnscrypt-proxy` in
the description and `cloudflared` in the implementation. The quoted passages
match the repository. Its 97-file inventory includes 96 Markdown files and
`posts.json`, consistent with the Codex count.

One metadata conclusion was wrong: agy treated the presence of a `draft:` key
as evidence of a draft and also named a file without that key. Independent
inspection found only two `draft:` entries, both `false`, and zero explicit
drafts. The correct scheduled set relative to 2026-09-13 comprises the September
14 retention, September 15 memory, and September 21 cache-isolation posts.
This error does not change the duplicate finding, but it prevents treating the
report as fully accurate. The overlap procedure was tightened to require
inspection of boolean values and an explicit publication cutoff. No claim is
made that another model run has validated that clarification.

Thus two harnesses applied the canonical overlap procedure and completed a
bounded review. Codex used name invocation; agy used the explicit-file adapter
and needed one correction request. This demonstrates portability with observable
limits, rather than identical behavior or nine fully validated review skills.

The duplicate comparison also exposed implementation and artifact discrepancies
in the old DoH guide. These were independently checked and filed as
[issue #620](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/620);
the skills migration does not claim to repair them.

## Nexus and independent review

Nexus producer 8.49.3 approved the plan 3–0 in job
`job-vote-2789db8a-c5d4-4d98-879c-bb17b4f0001a`. The final conditional vote was
2 approvals and 1 rejection under supermajority, job
`job-vote-cc6ffb31-7eb6-4a6b-9ee4-72e1a2720de7`. All three roles used
`gemini-3.1-pro-preview`; role diversity is not model diversity.

The dissent included a wrong-repository scope objection and a valid observation
that two actual harness executions were still pending when the vote ran. The
vote therefore did not replace behavioral validation. A separate independent
security review inspected all nine canonical files and exercised a synthetic
missing-review report, which correctly produced `HOLD`.

## Packaging and deterministic checks

The upstream `skills-ref` reference validator was checked out at immutable
revision `69ef37e9424c0a7ea9dd2293b559e43ec8176379` for format validation. It is
a demonstration implementation; format success does not establish security or
editorial correctness. All nine canonical skills passed the pinned validator.

The combined Python checks reported 262 tests plus 11 subtests passing before
the final skill review, and Ruff reported no script violations. The local report
validator has fixtures for partial and missing review coverage. It derives the
decision instead of trusting a supplied `READY`, and its explicit limits are
documented in [the review contract](../skills.md).
After tightening the exemption rule, the final focused checks passed 30 report
validation tests and 39 tests across the skills and blog-audit families.

Raw local CLI output is retained under `/tmp/portable-skills-*` during this
session. Those files are temporary, may contain harness metadata, and are not
durable public artifacts. The commands, task, versions, and outcome summary in
this document are the reviewable record; rerun the task after harness changes.

SHA-256 digests of raw output (basenames under `/tmp/`):

| Artifact | SHA-256 |
| --- | --- |
| `portable-skills-codex-overlap.jsonl` | `282f427b91cf6cdf9a1829137b2f9e4ef10b7f38ed6307c73c4c06e6cefe534e` |
| `portable-skills-claude-overlap.json` | `13e89e922face093e0ba6a3d6cae5396ee6e3d03739aba005fef51922ffb2a44` |
| `portable-skills-gemini-list-after.txt` | `a0fe75e1c7720bab48ec3e14217e71d091af6c6fc9d9bbe5a746ec5067c8ae50` |
| `portable-skills-gemini-overlap.json` | `7893012d8c7fbd9b8a1b25fb972c430063a6e54021f9eb1fd41c9842f6b5a3fc` |
| `portable-skills-agy-overlap.json` | `eb9087ea1a225be2d4af8438f339e12ccddd274ab716b14792b25a1aec02d4fc` |
| `portable-skills-agy-overlap-followup.json` | `5cd0a1c4c98757209ff80d38d39e9adb82907638f2a6ebd2bd850bf8ed1f6770` |
