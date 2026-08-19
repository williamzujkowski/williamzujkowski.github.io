---

author: William Zujkowski
date: 2026-08-18
description: "A proved gate is only as good as the policy it enforces, and the policy is the part that changes while the agent is running. What OSCAL and the agent-authorization drafts both assume, and what breaks."
title: "The Policy Is the Part That Moves"
tags:
  - security
  - ai
  - compliance
---
The [first post](/posts/2026-07-23-agent-controls-as-oscal) in this series expressed agent guardrails as machine-checkable OSCAL and proved the gate *ran*. The [second](/posts/2026-07-30-prove-the-gate-not-the-agent) proved the gate was *correct for every input*, with a Dafny model, a Rego twin, and differential testing between them.

Both assume something neither states: **the policy is fixed.** A tool call arrives, the gate evaluates it against a static allowlist, and returns allow or deny. That was the right simplification for a proof, and it is the thing that breaks next — because the interesting property of an agent is that its trustworthiness changes while it is running, and a gate proved correct against a frozen policy has nothing to say about that.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/authority-moves.png'); width: min(250px, 66%); aspect-ratio: 400/303; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the same key, a different lock</p>

## Two defects, one shape

I read four active IETF drafts on agent authorization against a working control plane. Fetch them yourself — they are short, and the bodies live at `https://www.ietf.org/archive/id/<draft-name>-<rev>.txt`:

| Draft | Rev |
|---|---|
| `draft-liu-agent-operation-authorization` | 02 |
| `draft-chen-agent-decoupled-authorization-model` | 00 |
| `draft-ni-a2a-ai-agent-security-requirements` | 01 |
| `draft-song-oauth-ai-agent-collaborate-authz` | 02 |

Two things recur, and they are the same mistake at different layers.

### Authority is modelled as issued state, not current state

A token carries an expiry and sometimes a call budget. It stays valid until one of those runs out. Nothing in it refers to the conditions that justified issuing it — the sandbox posture at the time, the reviewer who approved the plan, the agent's behaviour matching what was proposed. Enforcement checks the signature. It does not check the world.

This is fine for the case OAuth was designed around, where the thing holding the token is a piece of software whose behaviour does not drift. It is a poor fit for an actor whose trustworthiness is exactly the variable.

### Demotion does not exist

Every draft models grant and revoke. **None models the middle.** Grep them: across all four, `revoke` and `revocation` occur 13 times — 10 of those in a single draft, 3 in another, and **zero in the remaining two**. `demote`, `downgrade` and `step-down` occur zero times in any of them.

That gap matters because revocation is almost never what you want. An agent that fails a review is usually still useful — it can read, it can propose, it just should not be writing to anything for a while. The available vocabulary offers "keep full authority" or "stop existing," and the honest answer is nearly always in between.

## The referential defect, and where else it lives

`draft-liu-...-02` carries a `policy_id` claim. The definition, verbatim from the draft:

> The policy_id field is a string that serves as an OPA policy reference and MUST match a registered policy in the AS

The token is signed. The signature covers the token. **It does not cover the policy body that identifier resolves to.** Every mention of integrity in that document is a JWS signature over the token or the confirmation record — none of it binds the policy text.

So the audit trail records that an action was authorized under `opa-policy-789`. Later, someone edits the policy registered under that name. The evidence still points at `opa-policy-789`, which now says something different. Nothing was forged and nothing was tampered with; the record simply attests to a name whose meaning moved.

**And OSCAL has the identical defect.** An `implemented-requirement` points at a control by identifier. Nothing content-addresses the control text, or the policy body actually in force at assessment time. The assessment says the control was satisfied. It does not say *which version of the control* was satisfied, so an assessment result and the control it claims to satisfy can drift apart without either one being wrong.

Two communities, two layers, arriving at the same weakness independently. That is usually a sign the mistake is easy rather than careless — a name is the obvious thing to reference, and the cost of referencing it only shows up later.

## What I built

The fix for both is the same, and it is not clever: **bind the digest, not the name.**

```dafny
datatype Authority = Authority(mode: Mode, policyDigest: string)
```

A grant carries a content address of the policy body it was issued against. At decision time the gate compares the digest of the policy actually in force against the one in the grant, and the ordering matters:

```dafny
function DecideBound(
  auth: Authority, policy: Policy, presentedDigest: string,
  modeRules: seq<ModeRule>, call: ToolCall
): Decision
{
  if presentedDigest != auth.policyDigest then
    Deny("policy-body-mismatch")
  else if !ModeAtLeastF(auth.mode, FindModeRule(call.tool, modeRules)) then
    Deny("above-current-authority")
  else
    Decide(call, policy)
}
```

The digest check runs first. A grant issued against a policy body that is no longer in force authorizes nothing, whatever it says about modes or tools.

### Scope is not mode

The second half is the authority mode, and it addresses something the delegation models miss entirely. They are careful about preventing an agent from widening *scope* — which resources it may touch. None of them constrain *mode*.

"Modify one file" and "recommend a patch against one file" target the same resource, in the same operation family, with completely different blast radius. A policy engine checking scope alone cannot tell them apart.

```dafny
datatype Mode = Observe | Suggest | Enforce
```

Each tool declares the minimum mode it requires. An agent holds a current mode. The rule for a tool nobody remembered to list is the one worth stating explicitly:

```dafny
function FindModeRule(tool: string, rules: seq<ModeRule>): Mode
{
  if |rules| == 0 then
    Enforce          // the forgotten case must be the restrictive one
  else if rules[0].tool == tool then
    rules[0].required
  else
    FindModeRule(tool, rules[1..])
}
```

An unlisted tool requires the highest authority, so a mode table with a gap in it fails closed rather than open. That is a one-line decision and it is the difference between an omission that denies and an omission that permits.

### Demotion, without a validity window

```dafny
function Demote(a: Authority, to: Mode): Authority
  requires ModeRank(to) <= ModeRank(a.mode)
{
  Authority(to, a.policyDigest)
}
```

The precondition is the interesting part: `Demote` cannot raise authority. It is not a re-grant with a smaller number in it, and the type system will not let you use it as one.

Note also what is absent. There is no timestamp and no expiry. The demoted authority *is* the authority, so there is no interval during which a stale-but-unexpired grant still answers — which is the failure the issued-state model produces by construction.

## What is proved

Six lemmas, all discharged:

- **`NeverActsAboveAuthority`** — an allow implies the held mode met the required mode.
- **`DemotionTakesEffectImmediately`** — the very next call after a demotion is denied if it needed the old mode. No window.
- **`DemotionCannotWiden`** — anything allowed after a demotion was allowed before it.
- **`GrantBoundToPolicyBody`** — a mismatched digest denies, unconditionally. This is the property a bare `policy_id` cannot express.
- **`ModeGateOnlyRestricts`** — adding modes can turn an allow into a deny and never the reverse, so nothing part 2 proved is weakened.
- **`UnlistedToolRequiresEnforce`** — the gap in the table denies.

Then the same discipline as part 2: a Rego twin written independently, a Python monitor, and a differential test across **324 cases** spanning three modes, both digest states, six calls, and three mode tables. All three implementations agree on every one.

## The lemma that failed first

`DemotionTakesEffectImmediately` did not verify on the first attempt, and the reason is worth more than the five that passed.

I had stated it as: after a demotion, a call requiring more than the new mode is denied with `above-current-authority`. Dafny rejected it. The property is false as written, because the digest check runs *first* — if the policy body has also rotated, the call is denied for a different reason entirely, and my `ensures` clause named the wrong one.

The fix was a precondition, not a code change:

```dafny
requires digest == auth.policyDigest
```

I had written a property that was very nearly true, in a way I would not have caught by testing. Every test I would have thought to write holds the policy constant while varying the mode — which is precisely the case where the claim is correct. The prover checks the cases you did not think of, and the case I did not think of was two things moving at once.

That is the whole argument for this approach in one incident. Not that proofs are rigorous in the abstract, but that they object when your model of your own system is slightly wrong, at the moment you are most confident it isn't.

## What this does not do

Worth being clear about the boundary, since the series keeps insisting on it.

None of this constrains the agent. It constrains the gate in front of the agent, and now the authority the gate evaluates against. An agent can still propose anything it likes; what changed is that "the grant was valid when issued" is no longer sufficient for it to be honoured.

It also does not solve the hard operational question, which is *what should trigger a demotion*. Runtime behaviour diverging from an approved plan, a reviewer blocking, a sandbox posture change — those are all reasonable signals and none of them is formalised here. The lemma says a demotion takes effect immediately. It says nothing about whether you noticed you should demote.

And the digest binding trades one problem for another. A content-addressed policy cannot drift under a grant, but it also cannot be patched without invalidating every outstanding grant. That is the correct default for a security control and a genuine operational cost, and anyone adopting it should price that in rather than discover it.

## Where this leaves the series

Part 1 proved the gate ran. Part 2 proved it was correct for every input. Part 3 removes the assumption that made part 2 tractable, and the removal costs less than expected: six lemmas, one Rego file, and a difftest.

The general shape, which I suspect outlives the specific mechanism: **a proof is only as good as what it quantifies over.** Part 2 quantified over every tool call. It held the policy constant, and I did not notice I had done that until I went looking for what the drafts assumed. Everyone's proof has a variable that got quietly fixed. Finding it is the work.

The code is in [`oscal-agent-controls`](https://github.com/williamzujkowski/oscal-agent-controls) and everything above runs — 26 Dafny obligations, 12 OPA tests, 13 unit tests, and both differential suites, on every commit. Synthetic namespaces and fake tool names throughout, as in the previous two.
