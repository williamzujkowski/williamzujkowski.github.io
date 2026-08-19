---
title: "You Can't Prove the Agent. Prove the Gate."
date: 2026-07-30
description: "Formal verification for AI-agent security. You can't prove a probabilistic model does the right thing — but the deterministic gate in front of it is small enough to prove outright. Dafny proofs, a Rego twin, and differential testing, following the method AWS used for Cedar."
tags:
- security
- ai
- formal-verification
- ai-agents
- oscal
---

The [last post](/posts/2026-07-23-agent-controls-as-oscal) built a gate for an AI agent and proved it *ran* — negative tests, an audit trail, a machine-readable finding you could diff on the next commit. That's a real improvement over a policy document nobody executes. It is also the weakest useful thing you can say about a security control: it passed the cases I thought to write.

The cases you didn't think to write are where the incident lives. So here is the stronger claim, and this post is about earning it: not "the gate passed my tests" but "the gate cannot allow a call the policy doesn't permit" — checked for every possible input at once, by a machine that doesn't get bored or optimistic. You cannot make that claim about an LLM. You can make it about the thing standing in front of the LLM.

## Why the gate is the part you can prove

A formal proof needs something total, deterministic, and small. Feed it a function that terminates on every input, always returns an answer, and fits in your head, and an automated prover will chew through every case for you. Feed it something that samples from a distribution and you get a shrug.

An agent is the second thing. Its behavior lives in a model's weights and a temperature setting; "prove the agent won't exfiltrate a secret" is not a request a prover can honor. The gate is the first thing. The reference monitor from the last post is a pure function: a tool call goes in, an `allow`/`deny` with a reason comes out, and nothing about the model's mood changes the answer. That is exactly the shape a prover likes.

So point the proof at the gate. The agent is the interesting part, sure. But the gate is the part where "cannot" is an available word.

## What a proof buys over a test

A test picks an input and checks the output. Write four negative tests and you've checked four points in a space with billions of them. A proof quantifies over the whole space. "For *every* tool call and *every* policy, if nothing on the allowlist matches, the decision is deny" is one statement that stands in for every test you'd never finish writing.

I modeled the gate in [Dafny](https://dafny.org/), which discharges proofs with an SMT solver. The decision function mirrors the Python monitor's logic for the synthetic policy — same order, same deny reasons — written in Simplified Technical English, because a decision procedure reads like one anyway. Check the tool, check the action, check the destination, check for a secret, then decide (one defensive branch trimmed for space):

```dafny
function Decide(call: ToolCall, policy: Policy): Decision
{
  match FindToolRule(call.tool, policy.allowedTools)
  case NoRule => Deny("tool-not-allowlisted")
  case Found(rule) =>
    if !InString(call.action, rule.actions) then
      Deny("action-not-permitted")
    else if !ResourceOrDestinationPermitted(call, rule) then
      Deny("destination-not-permitted")
    else if HasSecret(call, policy) && !EgressAllowed(call, policy) then
      Deny("secret-egress-blocked")
    else
      Allow("matched-allow-rule")
}
```

Then the properties. These are not tests. Each one is a statement Dafny proves holds for all inputs, or the build fails:

```dafny
lemma DenyByDefault(call: ToolCall, policy: Policy)
  ensures !MatchesSomeAllowRule(call, policy) ==> Decide(call, policy).Deny?

lemma EgressDominance(call: ToolCall, policy: Policy)
  ensures HasSecret(call, policy) && !EgressAllowed(call, policy)
          ==> Decide(call, policy).Deny?

lemma AllowRequiresRule(call: ToolCall, policy: Policy)
  ensures Decide(call, policy).Allow? ==> MatchesSomeAllowRule(call, policy)
```

`DenyByDefault` says the gate fails closed: no matching rule, no allow. `EgressDominance` says a secret headed somewhere unapproved is denied even when the tool call is otherwise fine — the sharp point from the last post, now a theorem instead of a test. `AllowRequiresRule` says the gate never says yes by accident: every allow traces back to a rule someone wrote down. A fourth lemma proves the function is total, which Dafny mostly insists on anyway.

The proof bodies are empty. That is the good outcome — it means the properties fall straight out of the definitions, and the solver needs no hand-holding to see it. When the body has to fill up with hints, that's usually the model telling you the property is more fragile than you thought.

## The gap a proof leaves open

Here is the part most "we formally verified it" claims skip. A proof of the model is a proof of the *model*. It says nothing about whether the model matches the code you actually ship. You can prove a beautiful theorem about a Dafny function and still deploy a Python one that disagrees with it in a corner you never lined up.

This is a known problem with a known discipline, and the people who worked it out are worth copying. AWS built [Cedar](https://www.amazon.science/blog/how-we-built-cedar-with-automated-reasoning-and-differential-testing), their authorization language, with exactly this worry in mind. They modeled the engine in Dafny with mechanized proofs — the models have [since moved to Lean](https://github.com/cedar-policy/cedar-spec), same method, different prover — then used *differential testing* to hammer the model and the production Rust engine with generated inputs — on the order of a hundred million tests a night — checking that the two always agree. That second step turned up real bugs the proofs alone couldn't, because the proofs were about the model and the bugs were in the gap between it and the shipping code.

So the gate carries a miniature of the same idea. Three implementations of the same decision — the Python reference monitor, the Dafny model compiled to Python, and a [Rego](https://www.openpolicyagent.org/docs/latest/policy-language/) policy you could actually drop into [OPA](https://www.openpolicyagent.org/) as a deployable decision point — get fed the same enumerated corpus of synthetic tool calls. A harness asserts all three return the same decision *and* the same reason for every one.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Differential testing across three implementations of the gate">
  <section class="arch-tier" data-label="One input" role="group" aria-label="One input"><span class="arch-chip"><b>432 synthetic tool calls</b><i>enumerated, not sampled</i></span></section>
  <section class="arch-tier" data-label="Three implementations" role="group" aria-label="Three implementations"><span class="arch-chip is-primary"><b>Python monitor</b><i>the shipped gate</i></span><span class="arch-chip is-guard"><b>Dafny model</b><i>proved, compiled to Python</i></span><span class="arch-chip is-guard"><b>Rego policy</b><i>deployable in OPA</i></span></section>
  <section class="arch-tier" data-label="Compared on" role="group" aria-label="Compared on"><span class="arch-chip">decision + reason, for every call</span></section>
  <section class="arch-tier" data-label="Result" role="group" aria-label="Result"><span class="arch-chip is-guard"><b>All three agree</b><i>a disagreement is a bug</i></span></section>
</div>
<figcaption>Prove the model, then check the proof against the code you ship. The Dafny-proved decision, the deployable Rego policy, and the production Python monitor must return the same decision and the same reason for every call in the corpus.</figcaption>
</figure>

Run it, and the three columns line up:

```text
$ python verify/difftest/run.py
decision,reason,count
allow,matched-allow-rule,20
deny,action-not-permitted,192
deny,destination-not-permitted,56
deny,secret-egress-blocked,20
deny,tool-not-allowlisted,144
checked 432 synthetic calls
all engines agree
```

432 is not millions. This is a toy, and I want to be precise about what it demonstrates: the *method*, not an industrial guarantee. The proved model, the deployable policy, and the production code agree across every case the corpus covers, and the corpus is enumerated rather than sampled, so "every case" means something bounded and honest. Scaling from hundreds of enumerated cases to millions of generated ones — with generators that actually hit the corners, which is the part that earns its keep — is engineering, not a new idea. The [whole thing](https://github.com/williamzujkowski/oscal-agent-controls) verifies in CI on every push: `dafny verify`, `opa test`, and the differential run.

## What this does and doesn't earn you

A proven gate is not a safe agent. The agent will still improvise, still get prompt-injected, still try things you didn't anticipate — verification doesn't touch any of that. What it changes is the trust you place in the one component standing between the agent's improvisation and the blast radius. When the gate says deny, you now know it says deny for *every* call the allowlist doesn't cover, not just the ones your test suite remembered.

Two honest limits. First, the proof is only as good as the model's fidelity to the real runtime; differential testing narrows that gap but three implementations can still share one wrong assumption, which is why the corpus and the model both deserve suspicion. Second, the gate proves enforcement, not detection — "if the payload matches a secret pattern, deny" is a theorem, but whether the pattern actually catches real secrets is a separate, unproven, and much messier problem.

None of that diminishes the move. You take the messy, probabilistic, genuinely-hard part and you refuse to stake safety on proving it. You isolate a small deterministic gate, prove *that* outright, and check the proof against the code you ship. The agent improvises. The gate does not — and now you can prove it.

---

*Part 3, [The Policy Is the Part That Moves](/posts/2026-08-18-the-policy-is-the-part-that-moves), removes the assumption this post depends on: that the policy holds still.*
