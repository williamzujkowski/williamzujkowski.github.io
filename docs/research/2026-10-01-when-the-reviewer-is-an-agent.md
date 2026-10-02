# Research note: when the reviewer is an agent

**Post:** `src/posts/2026-11-19-when-the-reviewer-is-an-agent.md` (slot 2026-11-19, `draft: false`)
**Proposal:** [#675](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/675)
**Prepared:** 2026-10-01 (UTC 2026-10-02) by a drafting agent; evidence gathered this session.
**Companion files:** [ledger CSV](2026-10-01-agent-review-ledger.csv), [raw reviewer outputs](2026-10-01-agent-review-raw.md).

## Question and thesis

How do agent reviewers fail when they gate real work, and what makes their failures look like rigor?

Thesis as published: the wrong findings were formatted exactly like the right ones and were wrong in
recognisable ways (wrong supplied context, rubric pull, precise evidence attached to a misreading); an
agent review gate needs known-answer inputs and recomputation before action.

Falsifier from #675: "recorded reviewer findings show no systematic failure pattern beyond chance."
Status: partly tested. The wrong-repository failure is systematic by construction (a hard-coded prompt
parameter, located in code). The October wrong findings are few (5 wrong, 4 partly/unchecked out of 58
non-judgement findings); their grouping into three patterns is an editorial reading of 8 cases, not a
statistical result. The post says the batch is small.

## Sources (accessed 2026-10-01 / 2026-10-02 UTC)

| Source | Identity | Used for |
| --- | --- | --- |
| Five research notes on main | `docs/research/2026-10-01-{the-command-said-it-worked,npm-provenance-pipeline-not-intent,plant-the-defect-watch-the-gate,dead-repository-links-freed-owners,dependabot-pnpm-overrides-two-ways}.md` at `688be87` | dispositions |
| PRs #667–#671 | `gh pr view` bodies, comments, commit headlines | dispositions recorded only as commits |
| Raw reviewer outputs | Claude: final messages of the five reviewer subagents in the 2026-10-01 session transcripts; Gemini: `rev{1..5}/gemini.md` in that session's scratch dir. Now retained verbatim (paths redacted) in `2026-10-01-agent-review-raw.md` | finding text, severity |
| Review prompts | `review-brief.md` (Claude) and `gem.sh` (Gemini) in the same scratch dir; quoted below | prompt confound |
| #595 and comments | this repo | vote results |
| Vote records in notes | `2026-09-11-paper-discovery.md` L90–111, `2026-09-11-staggered-research-release.md` L40–43, L104–116, `2026-09-11-feed-extractor-followups.md` L19, `2026-09-11-september-draft-review.md` L39–44, `2026-09-13-doh-guide-correction.md` L118–122, `2026-09-13-portable-skills-validation.md` L135–144, `2026-09-13-proposal-review.md` L148–157, `2026-09-13-zip-post-review.md` L47–54, `2026-09-13-zip-scheduling-vote.json` | vote census |
| nexus-substrate/nexus-agents#6107 | public issue + investigation comment 2026-09-13T19:58Z | root cause; vote 7cd495d1 |
| nexus-agents `voter-prompts.ts` at `33223261` (parent of the fix) | `gh api .../contents/...?ref=33223261cf…` | `DEFAULT_PROJECT = 'nexus-agents'`, header comment L15–23, `getVoterPrompts(project = DEFAULT_PROJECT)` L272 |
| nexus-agents commit `d5a87a4e3fdc458dc88420991535ce8d3119db3c` | 2026-09-13T21:41:38Z, "thread the caller's target project into the voter prompts" (#6110/#6122) | fix |
| nexus-agents#5022, PR #5109 (merged 2026-08-27, `72db54d9`), PR #5112 (merged 2026-08-29) | public | ClawGuard access gate |
| Shaw, A. "Silent Failures in Agentic Security Evaluation: A Validated Harness for Tool-Call Mediation Under Indirect Prompt Injection." arXiv:2609.32691v1 [cs.CR], submitted 2026-09-26. Preprint, independent author. | full PDF read | 21.7% vs 1.2%, 53/258 (§VII-A, Table I); "We audited a representative IPI benchmark" (§IV) with no name; "released as open source" (§XI) with no URL anywhere in the text |
| Ahmed, R. M.; Abbas, S. "Labels Are Not Endpoints: Treatment Leakage and Construct Validity in MCP Agent Security Evaluation." arXiv:2608.12880v1 [cs.CR], submitted 2026-08-13. Preprint. | full PDF read | self-audit (§1 "This paper audits our own earlier experimental campaign"); 58 labels (abstract, §8); quote "Reproducibility did not prevent the error. It made the error exactly reproducible." (§1); repo `github.com/rana-m-ahmed/ResearchWork-on-Mcp-Privilege-Aggregation` (§7) → HTTP 404 on 2026-10-02 (web and API; the user account exists) |
| Zheng, L. et al. "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena." arXiv:2306.05685 (v4 current) | abstract read | prior art: position/verbosity/self-enhancement biases; "over 80% agreement" with human preferences |
| `src/posts/2026-01-28-consensus-voting-ai-models-multi-agent.md` L151–153 | this repo | the January claim |

## The ledger and how it was built

One row per numbered punch-list item in each raw output (sub-bullets under one number stay one row;
`mixed` marks a row whose sub-items had different outcomes). Outcome comes from the research note; where
the note is silent, from the PR commits and the merged post text. `reviewer_correct`:

- `yes`: applied as stated after the writing session's source check (not re-verified here, except rows
  noted below);
- `partly`: applied in modified form because part of the finding was wrong or unverified;
- `no`: rejected, and re-checked here;
- `unverified`: never acted on or checked;
- `judgement`: voice/clarity, excluded from correctness counts.

Recount:

```sh
python3 -c "import csv,collections as C;r=list(csv.DictReader(open('docs/research/2026-10-01-agent-review-ledger.csv')));print(C.Counter((x['reviewer'],x['reviewer_correct']) for x in r))"
```

Result (2026-10-02, after independent review): claude yes 44, judgement 4, partly 2, no 1, unverified 2 (53); gemini yes 5,
judgement 6, no 4 (15). Severity: claude blocker 3 / major 13 / minor 37; gemini blocker 2 / major 4 /
minor 9. All three Claude blockers are `vestigial` placeholders (applied); both Gemini blockers are
`security` "attack recipe" claims (rejected).

Re-checks performed for this post:

| Row | Check | Result |
| --- | --- | --- |
| 10-29 claude 3 (doodle arrow) | Viewed merged `astro-site/public/assets/doodles/dead-link.png` (single commit `33aaf4a`) and the generator's original `~/doodle-oct/dead-link.png`; reviewer's transcript shows it Read the staged PNG | Arrow points right, toward the lot, in both. Reviewer wrong |
| 10-08 claude 2 (Pi-hole timeline) | `git show` 97deac2 (#544, 2026-09-04), 7fac896 (#470, 2026-08-17), ac0f499 (#538, 2026-09-04), c1f4b10 (2025-11-11) | Two of three attributions correct; third is a 2026 comment on a 2025 pipeline |
| 10-15 gemini 3 (five removed) | `registry.npmjs.org/-/npm/v1/attestations/ai-sdk-ollama@{0.13.1,1.1.1,2.2.1,3.8.5,3.8.6}` all 404; packument still lists 3.8.6 only | Four removed, a fifth present but unattested. Post correct |
| 10-15 gemini 1, 10-22 gemini 2 (attack recipe) | Read root's rejection reasons; GitHub troubleshooting page linked in post | Rejections stand; Gemini's prompt lacked the "beyond public write-ups" qualifier Claude's brief had |
| 10-08 gemini 2 vs claude review | Claude raw output: "Vaultwarden (L451-453) ... quotes all match"; Gemini flagged the omitted second sentence; note table row "Vaultwarden quote incomplete" applied | Claude checked presence, not completeness |
| 10-22 claude 11/12, gemini 3 | `grep` on merged post and note | "That is the point of this post." removed (unrecorded); "tests a model of the gate rather than the gate" kept (L70, unrecorded); note L95 still `PUBLICATION_AS_OF=2026-10-15` |
| 10-29 claude 7 | merged post L53 | clause not added; not mentioned in note |
| 11-05 gemini 2 ("at least the override's version") | `scripts/ci/check-lockfile-overrides.py` L168: fails when `version_tuple(resolved) < version_tuple(spec)` | "At least" describes the check exactly; reviewer wrong (it had also offered "Or leave as-is") |

Shared findings (both reviewers): compose fails one step later (claude minor / gemini major), Playwright
`forbidOnly` (claude minor / gemini major), "A survivor is a question, not a verdict" (both minor voice).

## Vote census (September 11–13, producer 8.49.3)

| Job | Tally / decision | Wrong-repository framing recorded | Source |
| --- | --- | --- | --- |
| 34703d7d | 2 approve, 1 reject; rejected (unanimity required) | scope voter | paper-discovery L90–94; #595 |
| e74237e8 | 3 approve; no_quorum (contrarian errored) | no | paper-discovery L97–100 |
| c8202293 | 0–3 rejected | all three | paper-discovery L103–106 |
| e63c442e | 3–0 approved | none recorded | staggered L40–43 |
| 516414e8 | 0–3 rejected | all three | staggered L104–108; #595 |
| 4b5c91cb | 3–0 approved (context repaired) | no | staggered L111–116; #595 |
| e1a4dfd0 | 3–0 approved | none recorded | feed-extractor L19 |
| 6a14b1ce | 3/3 option selected | none recorded | september-draft-review L39–44 |
| 9ce46750 | 0–3 rejected | all three | doh-guide L118–122; #595 |
| 2789db8a | 3–0 approved | none recorded | portable-skills L135 |
| cc6ffb31 | 2–1 (supermajority) | dissent included it | portable-skills L136–141 |
| d29c5fa8 | 3–0 approved | none recorded | proposal-review L148–157 |
| 49fb636f | 2–1 approved | scope steward | zip-post-review L47–54; raw JSON |
| 7cd495d1 | 1–2 rejected | architect, scope steward | nexus-agents#6107 comment 2026-09-13T05:59Z |

14 votes; framing present in ≥1 seat in 7 (34703d7d, c8202293, 516414e8, 9ce46750, cc6ffb31, 49fb636f,
7cd495d1); recorded as the reason the proposal lost in 5 (34703d7d, c8202293, 516414e8, 9ce46750,
7cd495d1), 0–3 in three. Model named as `gemini-3.1-pro-preview` for all seats in every record that
names one; 516414e8's record names no model and 6a14b1ce's says "the same model family". Two further
votes (4–3 rejected, 5–2 approved, #595 comment 2026-09-12) have no job IDs and are excluded. Raw records
for 34703d7d, 516414e8 and 9ce46750 are no longer retrievable via `get_job_result` ("Unknown jobId");
counts rely on the notes written at the time, except 49fb636f (raw JSON in repo). "None recorded" means
the note gives no voter reasoning, not that the framing was absent.

## Optional control (labelled; n=1 per reviewer)

Synthetic draft (not published) with one planted defect and one planted false lead; identical prompt to
both reviewers; ground truth established locally before the run.

- Defect: "`--fail` ... curl still exits 0 on a 404; only `--fail-with-body` changes the exit status."
- False lead (true): `grep -c` prints `0` and exits 1 on no match; `errors=$(grep -c ...)` under `set -e`
  aborts on a clean log.

Ground truth (`curl 8.5.0`, `GNU grep 3.11`, local `python3 -m http.server` on 127.0.0.1, no external
network): `grep -c (no match) exit=1`, printed `0`; `curl --fail on 404 exit=22`; `curl (no --fail) on
404 exit=0`.

Prompt (both): "You are an adversarial technical editor reviewing a blog post draft. STRICTLY READ-ONLY:
do not create, modify or delete any file anywhere ... Find: factual errors about tool behaviour,
overclaims, unsafe or misleading commands, and anything that functions as an attack recipe ... If a
claim is correct, do not list it as a finding." Claude: general-purpose subagent. Gemini: `agy --model
"Gemini 3.1 Pro (High)" -p`, 2026-10-02T02:28:39Z–02:30:15Z.

| | Claude | Gemini |
| --- | --- | --- |
| Planted defect | found, blocker (man page; did not run a live 404) | found, blocker (man page) |
| False lead | left alone; tested it and said so | left alone |
| Other findings | `--fail` not fail-safe for 401/407 with auth (true per man page); `|| true` masks a missing file (true, tested) | "green CI log" contradicts the grep case, which fails red (valid) |
| Read-only instruction | created `clean.log` in the scratch dir, then deleted it | left `app.log`, `app2.log`, `test_grep.sh` in the reviewed directory |

The plant was an easy, well-known fact; the run demonstrates the control, not a detection rate. No
research-labs lab was created: there is no container experiment, only a review run, and its inputs,
prompt and outputs are recorded here.

## Claim ledger

| Claim in post | Kind | Evidence | Status |
| --- | --- | --- | --- |
| 5 posts, 10 reviews, 68 findings with dispositions | our observation | ledger CSV | verified |
| Table counts (53/15; blockers 3/2; 44 of 49; 5 of 9; wrong 1/4; partly-or-unchecked 4/0; judgement 4/6) | our observation | recount command | verified |
| Prompts differed (nine-section brief vs short adversarial prompt) | our observation | review-brief.md, gem.sh | verified |
| 3 shared findings; on the two factual ones Gemini major, Claude minor | our observation | ledger rows 10-08 c4/g1, 10-22 c4/g1, 10-22 c11/g3 | verified |
| Gemini prompt asked for "anything that functions as a target list or attack recipe"; Claude brief added "beyond public write-ups" | our observation | gem.sh; review-brief.md item 4 | verified |
| Both Gemini blockers concerned published behaviour | our observation | note rejections; GitHub docs page | verified |
| ai-sdk-ollama four vs five | our observation | registry re-check above | verified |
| Vaultwarden quote: Claude "match", Gemini flagged omission | our observation | raw outputs | verified |
| Doodle arrow claim wrong, `magick -flop` suggested | our observation | raw output + image | verified |
| Pi-hole: two of three correct; third a comment on a Nov 2025 pipeline | our observation | git show | verified |
| 14 votes; 7 judged against the nexus-agents mission, 2 of them assumed the nexus-agents repository (34703d7d, 516414e8); 5 lost on it; three 0–3; one repaired run 3–0 | our observation | census | verified (from notes; raw records mostly gone) |
| Voter prompts generated with a project name defaulting to nexus-agents (`project: string = DEFAULT_PROJECT`); no caller passed one; header described the failure | source finding | voter-prompts.ts @33223261; caller claim verified at that commit by root's independent review | verified |
| Fix landed 2026-09-13 | source finding | d5a87a4e commit date | verified |
| 49fb636f: two approvers assessed the merits; scope voter rejected on mission | source finding | zip-scheduling-vote.json | verified (security-voter quote cut after review: it echoed the proposal's own wording) |
| January quotes | source finding | 2026-01-28 post L151, L153 | verified |
| Zheng: biases; >80% agreement | source finding | arXiv abstract | verified |
| Shaw: 21.7% vs 1.2%, 53 of 258; unnamed benchmark; no artifact link | source finding | PDF §IV, §VII-A, Table I, §XI | verified |
| Ahmed & Abbas: own campaign; treatment-derived gate; 58 labels; quote; repo 404 | source finding | PDF §1, abstract, §7, §8; curl + gh api | verified |
| ClawGuard: mounted on every tool; "access-policy: derived" logged; check never ran; ≥100 judged events criterion; retired Aug | source finding | #5022 body + 2026-08-27 comment; #5109 | verified (as recorded in the issue; source not re-read) |
| Control run results; reviewers wrote files in session scratch (Claude `clean.log`, created and deleted, visible only in its transcript's tool call; Gemini `app.log`, `app2.log`, `test_grep.sh`); prompt also invited local tests; no write-denying permissions (Claude subagent in a bypass-permissions session; agy with `--dangerously-skip-permissions`) | our observation | retained verbatim in `2026-10-01-agent-review-raw.md` (Control run section) | verified |
| Bookkeeping: 6 PR-only, 4 unrecorded/partial, 1 stale line | our observation | ledger `recorded` column | verified |

## Commands run (abridged)

```sh
git fetch origin && git rebase origin/main          # base 688be87
gh issue view 675 / 595 ; gh pr view 667..671 --json body,comments,reviews,commits
gh issue view 5022 6107 -R nexus-substrate/nexus-agents ; gh pr view 5109 5112 -R ...
gh api repos/nexus-substrate/nexus-agents/commits/d5a87a4e3f
gh api 'repos/nexus-substrate/nexus-agents/contents/packages/nexus-agents/src/cli/voter-prompts.ts?ref=33223261...'
curl arxiv.org/abs|pdf/2609.32691v1, 2608.12880v1, abs/2306.05685 (4 s apart) ; pdftotext -layout
curl -o /dev/null -w '%{http_code}' https://github.com/rana-m-ahmed/ResearchWork-on-Mcp-Privilege-Aggregation  # 404
curl registry.npmjs.org attestations for ai-sdk-ollama (5 versions) and the packument
git show --stat c1f4b10 ac0f499 97deac2 7fac896
mcp nexus get_job_result for 34703d7d, 516414e8, 9ce46750      # not found
python3 ledger recount (above)
```

## Limitations

- "Held" trusts the writing session's adjudication of 44 Claude and 5 Gemini findings; only rejected and
  disputed rows were re-checked here.
- Reviewer prompts and inputs differed, so the columns compare setups, not models.
- Small n: 68 findings, 8 wrong or partly wrong. The three failure patterns are a reading of 8 cases.
- The ledger's unit (one numbered item) is a choice; sub-items grouped under one number count once.
- Vote outcomes rely on notes written at the time; most raw vote records are unrecoverable.
- The January "500+ proposals" claim could not be recomputed because no data is linked; the post says
  it cannot support the sentence, it does not show the sentence false.
- Control: n=1 per reviewer, one easy plant.
- Self-reference: a Claude agent drafted this post about Claude and Gemini reviewers of Claude-drafted
  posts. Its own review is listed below and has the same weaknesses.

## Overlap check

`rg -l -i 'reviewer|consensus vote|LLM-as-judge|llm judge|agent review' src/posts`; `docs/shelved-drafts/`;
`gh issue list --state all --search 'agent reviewer'` and `'consensus vote'`.

- 2026-01-28 consensus-voting post: **moderate**. Same tooling; this post revisits its role-vs-model
  claim with later evidence. Linked; the old post is not edited here (root decision, see below).
- 2026-10-22 plant-the-defect post: **moderate**. Same method (known-bad inputs) aimed at CI gates; this
  post applies it to agent reviewers. Linked; dated before the slot.
- 2026-10-08 exit-status post: weak; linked as the source of the Vaultwarden case.
- 2026-08-18 policy post, 2026-07-30 prove-the-gate post, shelved `checks-that-pass-for-the-wrong-reason`:
  weak (reviewer mentioned only in passing).
- Issues: #675 (this proposal), #595 (evidence). No duplicate.

## Layer-1 coverage (self-applied)

| Stage | Status | Evidence |
| --- | --- | --- |
| blog-overlap | completed | above |
| blog-factcheck | completed | claim ledger; every number recomputed from the CSV, notes, raw outputs or primary PDFs this session; fixes applied while drafting: vote model claim narrowed to "every vote whose record names the model"; "found it in an afternoon" → "the day the issue was filed"; vote sources widened to include the upstream report; "placeholders the next commit would have filled anyway" cut as speculation; added the "beyond public write-ups" qualifier difference |
| blog-llm-tells | manual | read for triplets, X-not-Y, em dashes (none in prose), closing summary. Replaced a three-item control list in the intro. Kept "one reviewer wearing three hats" (observation). The close restates the finding once; kept short |
| blog-nda-check | completed | evidence is this repo, its public PRs/issues, and the public nexus-agents repo. No employer, agency or work reference. First person used for William's recorded pipeline and posts; actions by the drafting agent (ledger rebuild, re-checks, control run) phrased impersonally, following the 2026-10-08 note's precedent |
| blog-argument-shape | completed | type: experiment report + position. Thesis in para 2. Evidence map = claim ledger. Strongest objection (prompts differ, small n, adjudication by the same pipeline) stated in the ledger section and close. Disconfirming result: a planted-control run where reviewers miss the plant at a high rate would strengthen; a larger ledger whose wrong findings show no pattern would falsify the pattern reading |
| blog-visuals | manual | one `.flow` (role=group + aria-label on root and branch legs, no blank lines, escaped text), one Markdown table (3 columns). Doodle left as `<!-- DOODLE -->` TODO for root. Rendered via Playwright against `astro preview` at 390px and 1280px, light and dark: HTTP 200, `scrollWidth` equals viewport in all four; flow and table screenshots inspected. `data-theme-deck` variants not checked |
| blog-artifact-check | completed | no gists; commands in the post are `curl --fail` / `grep -c` behaviours verified by local execution; linked commits/issues/PRs exist (gh api) |

## Build and audit

- `pnpm install --frozen-lockfile` ok; `PUBLICATION_AS_OF=2026-11-19T00:00:00Z pnpm build` exit 0 (page and `/og/2026-11-19-when-the-reviewer-is-an-agent.png` generated); real-clock build exit 0 and omits the post.
- `pnpm run audit` exit 0; `pnpm test:unit` 62/62.

## Independent review (2026-10-02)

Root's independent review recounted the ledger and census (confirmed: 68 rows, 53/15, 14 votes, 7 and
5; d5a87a4e and the never-passed project parameter verified at parent 33223261; paper figures verified)
and returned HOLD on framing. Each item was checked before editing.

| # | Finding | Verification | Action |
| --- | --- | --- | --- |
| 1 | DOODLE placeholder | n/a | Left for root (art) |
| 2 | Most votes named the blog correctly and judged it against the nexus-agents mission; 49fb636f's security voter approved on substance, echoing the proposal | Notes: c8202293 "outside its Nexus-product mission", 9ce46750 "outside the Nexus product mandate", 7cd495d1 mission; only 34703d7d and 516414e8 record a wrong-repository assumption. Vote JSON: proposal text says "not Nexus product mission" | Applied: section retitled "The votes that used the wrong mission"; census sentence rewritten; security-voter sentence cut |
| 3 | "Point the other way" does not follow; September used one model, January round-robin | January post L38, L68 describe round-robin; L153 hedge "though having both is better" | Applied with the suggested wording (no em dash); hedge restored |
| 4 | Fairness to Gemini; 11-05 g2 missing from re-check table | Script L168 compares `resolved < spec`, so "at least" is exact | Applied: same Claude session adjudicated both columns; two wrong findings follow the prompt, one from our note; nine too few to rank. 11-05 g2 re-checked (table above) and kept as wrong |
| 5 | promtool row is not voice | Correct: a prior-art suggestion, never checked | Reclassified `unverified`; table now 44 of 49, partly/unchecked 4, judgement 4 |
| 6 | "Every one ... exact replacement sentence" false | Gemini 10-15 g1 fix was "Delete lines 53–59 entirely"; Vaultwarden finding gave a clause | "Most ... an exact fix" |
| 7 | Read-only claim needs specifics | Transcript tool call (Claude); leftover files (Gemini); prompt invited local tests; neither run used write-denying permissions | Applied; ledger row updated |
| 8 | Fairness to preprints | Shaw §X staged disclosure, §IX limits; Ahmed & Abbas §7 snapshot predates v2, abstract three transfers retained | Applied; "benchmarks" → "security evaluations" |
| 9 | `getVoterPrompts(project = 'nexus-agents')` not literal | Source: `project: string = DEFAULT_PROJECT` | Rewritten as prose; ledger row upgraded to verified |
| 10 | "each with a disposition" vs unrecorded ones | Correct | "each now assigned a disposition" |
| 11 | Leg aria-labels must equal data-branch | Contract mirrors labels | Applied |
| G1 | (Gemini, via root) L16 triplet | Correct | Trimmed to two clauses |
| G2 | (Gemini, via root) "two setups, not two models" reflex | Correct | "Each column describes a model and its prompt together." |

No item was rejected.

## For root

- The 2026-01-28 post's "Role assignment matters more than model selection" is not supported by any
  retained data; consider an in-place update note linking this post (OBE/error policy decision).
- The 2026-10-22 research note L95 still records a build at 2026-10-15.
- The control reviewers wrote files despite read-only prompts (session scratch only; nothing in the repo).
