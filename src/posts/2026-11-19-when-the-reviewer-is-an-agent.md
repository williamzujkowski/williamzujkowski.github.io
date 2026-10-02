---
title: "When the Reviewer Is an Agent"
date: 2026-11-19
draft: false
author: William Zujkowski
description: "Sixty-eight agent review findings on five posts, each checked against its source: what the wrong ones had in common, and the controls an agent review gate needs."
tags:
  - ai
  - security
  - software-engineering
  - testing
---

Every post in my October batch went past two agent reviewers before it was scheduled. One was a Claude reviewer running in a separate context; the other was Gemini 3.1 Pro, run through the agy CLI. Their punch lists went back to the session that wrote the posts, which checked each finding against its source and recorded in the post's research note what it applied and what it rejected. Five posts, ten reviews, 68 findings, each now assigned a disposition. That is the nearest thing I have to ground truth about agent review when it gates real work.

Most findings were right. The wrong ones were formatted exactly like the right ones, and they were wrong in recognisable ways: mostly the reviewer had been given the wrong frame, or had attached precise evidence to a misreading. A review gate staffed by agents needs what [any other gate needs](/posts/2026-10-22-plant-the-defect-watch-the-gate): inputs whose right answer is known in advance, and recomputation of every claim before anyone acts on it.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/empty-pitch-card.png'); width: min(240px, 62%); aspect-ratio: 400/284; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">A firm decision, confidently delivered.</p>

## The ledger

The ledger behind this post rebuilds the batch's review record from the research notes, the five pull requests (#667 to #671) and the reviewers' raw outputs, which had survived only in a session scratch directory and are now [retained in the repository](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-10-01-agent-review-raw.md). One row per numbered finding, in a [CSV](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-10-01-agent-review-ledger.csv) anyone can recount.

| | Claude reviewer | Gemini reviewer |
| --- | --- | --- |
| Findings | 53 | 15 |
| Labelled blocker | 3, all unfilled placeholders; applied | 2, both "attack recipe"; both rejected |
| Non-judgement findings that held as stated | 44 of 49 | 5 of 9 |
| Wrong | 1 | 4 |
| Partly right, or never checked | 4 | 0 |
| Voice and clarity (judgement calls) | 4 | 6 |

"Held" means the writing session, itself a Claude session, verified the finding against the source and applied it; the same session adjudicated both columns. The rejected and disputed findings were re-checked for this post; the 49 accepted ones were not. The reviewers also had different prompts: Claude got a nine-section brief with the repository's review procedures, Gemini a short adversarial-editor prompt. Each column describes a model and its prompt together. Of Gemini's four wrong findings, two follow directly from its prompt and one came from an error in our own research note. Nine checkable findings are too few to rank anything.

Only three findings appeared in both lists. On the two of those where the stakes were factual, Gemini called the problem major and Claude called it minor. Of the five findings labelled blocker, three were unfilled placeholders and two were wrong. Severity told me what each reviewer thought, and nothing else.

## What the wrong ones had in common

**The rubric found what it was told to find.** Gemini's prompt asked for "anything that functions as a target list or attack recipe". Both of its blockers were exactly that, and both concerned published behaviour. One was the [provenance post's](/posts/2026-10-15-npm-provenance-attests-the-pipeline) diagram of a trusted-publishing hijack, drawn at the level of detail of the public vendor write-ups it cites. The other was the mutation post's sentence that a crashed deciding job leaves required checks `skipped`, which GitHub [documents](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/collaborating-on-repositories-with-code-quality-features/troubleshooting-required-status-checks). The Claude reviewer's brief asked the same question with three more words, "beyond public write-ups", and it found nothing to block. Model and prompt both differed, so this cannot say which one mattered; the qualifier is the likelier suspect.

**The summary stood in for the source.** Gemini said the provenance post's "four removed ai-sdk-ollama versions" should be five. It had counted from a line in the research note that grouped a fifth, still-published version with the four. The post was right and the note was sloppy. Going the other way, the Claude reviewer listed the Vaultwarden template quote in the [exit-status post](/posts/2026-10-08-the-command-said-it-worked) among the quotes that "match". It did match, as far as it went. The draft had dropped the next sentence, which says the option is meant for use behind a separate authentication layer. Gemini caught that. Checking that a quote appears in the source is a different check from whether it represents the source.

**Precise evidence, wrong conclusion.** The Claude reviewer reported that the dead-link doodle's arrow "points left, away from the empty lot", and supplied the ImageMagick command to mirror it. The arrow points right, at the lot, in both the generated original and the merged file. On the exit-status post it said three of four defects had arrived in 2026 correction passes, and cited the commits. Two had. The third commit added a comment vouching for a pipeline that dated from November 2025. The hashes were real; the inference attached to one of them was not.

Most of these arrived with a line number, a severity, evidence and an exact fix, the same shape as the 49 that held. The format of a review finding carries no information about whether it is true.

## The votes that used the wrong mission

In September this site also used consensus votes from my nexus-agents project as a review step. This site's research notes, [#595](https://github.com/williamzujkowski/williamzujkowski.github.io/issues/595) and the upstream report record 14 votes with job IDs between September 11 and 13. In seven, at least one voter judged the blog proposal against the nexus-agents product's mission; in two of those, a voter assumed the target was the nexus-agents repository itself. In five, that mission framing was the recorded reason the proposal lost, three of them 0–3. Every vote whose record names the model ran `gemini-3.1-pro-preview` in all three seats. One run with the context spelled out in the prompt approved 3–0.

The cause was in the harness. Every voter role prompt was generated with a project name that defaulted to nexus-agents, and no caller ever passed another one. The module's own header comment described this exact failure, outside proposals rejected as misaligned, and the parameter added to prevent it was never set. The [investigation](https://github.com/nexus-substrate/nexus-agents/issues/6107) found it the day the issue was filed, and the fix that threads the target project into every prompt [landed](https://github.com/nexus-substrate/nexus-agents/commit/d5a87a4e3fdc458dc88420991535ce8d3119db3c) on September 13.

Three roles on one model with one system prompt are one reviewer wearing three hats; a unanimous vote measured their shared premise. In the [retained record](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-09-13-zip-scheduling-vote.json) of one 2–1 approval, the two approving voters assessed the post on its merits and the scope voter rejected it as outside a mission it was never meant to apply. A tally cannot tell those apart; only the reasoning can.

## What this does to the January claim

My [January post on consensus voting](/posts/2026-01-28-consensus-voting-ai-models-multi-agent) said "Role assignment matters more than model selection", from "roughly six months of multi-model consensus voting across 500+ proposals". It links no data I can recompute. The September votes cannot test it: all three seats ran one model, unlike January's round-robin design, and they failed because the shared role prompt carried the wrong mission. If anything that says role framing matters, in the bad direction. In October, two model families with different prompts overlapped on three findings in 68, and each caught something the other had passed as fine. Because the prompts differed, that does not settle it either.

The January post hedged its own claim, "though having both is better", and that hedge is the part the records still support. What they add is narrower: the frame a reviewer is given decides what it can see, for every seat that shares it. Without January's data, I would not repeat the headline sentence as a design rule.

## Graders have the same problem

None of this is new to the [LLM-as-judge literature](https://arxiv.org/abs/2306.05685), which documents position, verbosity and self-enhancement biases while finding strong judges agree with human preferences over 80% of the time on open-ended chat. A gate is a narrower job. There is usually a right answer, and you can recompute it.

Two recent preprints make that point about security evaluations. Shaw's [*Silent Failures in Agentic Security Evaluation*](https://arxiv.org/abs/2609.32691v1) re-scores identical traces and finds that crediting an attack whenever the target tool is called, ignoring its arguments, reports 21.7% attack success where the argument-level rate is 1.2%, misclassifying 53 of 258 attack runs. It never names the benchmark it audited and gives no artifact link, though it says the harness is released and the full attack suites are withheld until the archival version; it also lists its own limits, including a single tool domain and a 43-scenario attack stratum too small to compare defenses. As written, the audit cannot be checked. Ahmed and Abbas's [*Labels Are Not Endpoints*](https://arxiv.org/abs/2608.12880v1) audits their own MCP campaign, whose grader used a variable derived from the treatment to decide attack success. Re-grading moved 58 historical attack or hijack labels to authorized benign completions, while three verified protected-data transfers survived it. Their summary is the best sentence in either paper: "Reproducibility did not prevent the error. It made the error exactly reproducible." The repository they link, a snapshot that predates the corrected reconstruction, returns 404 as of October 2026.

My own tooling has the gate version. An access-policy middleware in nexus-agents was mounted on every tool and logged "access-policy: derived" on each orchestration, but the policy lived in an async scope that inbound tool calls never entered, so the access check [never ran once](https://github.com/nexus-substrate/nexus-agents/issues/5022). Its promotion criterion required at least 100 judged events from a mode that could produce none. It was [retired as an enforcement mechanism](https://github.com/nexus-substrate/nexus-agents/pull/5109) in August. The log line was real, and it was the most convincing part.

## Controls for a review gate

<div class="flow" role="group" aria-label="An agent review gate with planted controls">
  <div class="flow-node"><b>Review batch</b><i>Real drafts plus one planted defect and one planted correct-but-odd claim</i></div>
  <div class="flow-node"><b>Reviewers</b><i>Target named as structured input; no write access</i></div>
  <div class="flow-node is-gate"><b>Controls</b><i>Defect caught? Correct claim left alone?</i></div>
  <div class="flow-branch" role="group" aria-label="Control outcomes">
    <div class="flow-leg" data-branch="Both" role="group" aria-label="Both"><div class="flow-node is-good"><b>Recompute each finding</b><i>Against the primary source; record every disposition</i></div></div>
    <div class="flow-leg" data-branch="Either missed" role="group" aria-label="Either missed"><div class="flow-node is-bad"><b>Void the batch verdict</b><i>Fix the setup before rerunning</i></div></div>
  </div>
</div>

1. **Plant a defect and a false lead in every batch.** One trial run gave both reviewers the same prompt and a short synthetic draft. The planted error was a claim that `curl --fail` exits 0 on a 404 (locally it exits 22). The false lead was the true but surprising fact that `grep -c` prints `0` and exits 1 when nothing matches, which ends a `set -e` script on a clean log. Both reviewers caught the defect and left the false lead alone. One run each, with an easy plant, shows the control working; it measures nothing about rates.
2. **Make the target structured input, and check the reviewer echoes it.** A rejection or approval whose reasoning names the wrong project is void, whichever way it went.
3. **Recompute before you edit.** A reviewer's evidence field is another claim. The doodle took one look to settle; the commit history took a pickaxe search.
4. **Record every disposition, including the ones nobody acted on.** Six findings in this batch are recorded only as PR commits, four have dispositions that were not recorded or only partly, and one stale line a reviewer flagged is still in a research note. The ledger exists because the raw outputs happened to survive.
5. **Enforce read-only with permissions.** Both control reviewers were told "STRICTLY READ-ONLY", and both wrote files in a session scratch directory, the prompt having also invited local tests. The Claude reviewer created a log file and deleted it; Gemini left two logs and a test script behind. Neither ran under write-denying permissions, and a sentence was all that stood in for them.

The [records behind every number](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-10-01-when-the-reviewer-is-an-agent.md) are in the research note, including the control run's prompt and outputs. The batch is small, the reviewers had different prompts, and the "held" column trusts one session's adjudication of 49 findings. Even so, agent reviewers caught real errors in every post here. The wrong findings looked identical to the real ones, and only a check against the source told them apart.
