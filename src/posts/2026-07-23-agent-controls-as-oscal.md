---
title: "The Firewall Stays Put. The Agent Improvises."
date: 2026-07-23
description: "Rewriting security controls for probabilistic agents. Static control catalogs assume systems that do what they're told; AI agents don't — so here's how to express agent guardrails (tool allowlists, secret-egress denial, audit) as machine-checkable OSCAL component definitions."
tags:
- security
- ai
- oscal
- compliance
- ai-agents
---

Most writing about AI-agent risk is qualitative: prompt injection, excessive agency, tool misuse, the usual gallery. Separately, the compliance world has [OSCAL](https://pages.nist.gov/OSCAL/), a machine-readable format for expressing security controls. I haven't found the two connected in public writing. This is a post about what happens when you try — and about why the sharper question is which control *expressions* survive contact with a non-deterministic actor.

I have reasons to care about this intersection. I'm an OSCAL Foundation member, and I authored a NIST SP 800-53 overlay for AI-agent behaviors. Control catalogs are already machine-readable; the part I keep circling is how to *use* that while building with LLMs — pulling the applicable controls as a checklist so the well-worn security angles get covered deliberately, alongside the new ones AI opens up, and documenting what a system actually enforces as CLI agents help build it. I've poked at this in the open — an early [standards repo](https://github.com/williamzujkowski/standards) and [an MCP server on top of it](/posts/2025-07-22-supercharging-claude-cli-with-standards), both experiments I've let go quiet rather than products. This post is the idea underneath them. I work most of this out in my own test environments first, where I have room to fail loudly and cheaply. The thinking generalizes to higher-stakes settings; the freedom to fail cheaply does not.

## The problem with borrowing a control catalog

A control catalog was written for systems that do what they're told. You configure a firewall; it stays configured. You set a permission; it holds. The system is boring, and boring is exactly what you want from a control.

An agent is not boring. It holds delegated credentials, it improvises across trust boundaries, and it keeps its plan in the one place you can't trust — the model's output. So "the agent has a tool policy" isn't a control. It's a wish with YAML nearby. The control is the thing that says *no* before the tool runs, outside the model's path, and can prove it did with a failing test and an audit line.

That gap changes four things about how a control has to be written.

**Bind the capability.** A system control often asserts that a function or boundary *exists*. An agent control has to assert which action the agent may take — under which task, with which identity, against which destination, with which approval. "The agent has a tool policy" is weak. "The runtime denies every tool call that does not match the policy tuple `{tool, action, resource, destination, principal, task}`, before execution" survives contact with the agent.

**Treat outputs as untrusted until mediated.** The model's plan is not the enforcement boundary. OWASP's [Excessive Agency](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) guidance is blunt about this: damaging actions follow unexpected, ambiguous, or manipulated model output, and the mitigation is complete mediation with a deterministic decision *outside* the model path.

**Make delegated authority explicit.** Agents act *as* users, service accounts, workflows, or other agents. That's a confused-deputy problem waiting to happen. A durable control names whose authority is in use, how it's scoped, when it expires, and whether the downstream system enforces the same scope — not just the agent's runtime.

**Make it testable.** For a non-deterministic actor, the evidence is executable: allowed tool set, blocked tool set, destination allowlist, a secret-egress detector, review gates, audit fields. It comes from negative tests and runtime traces, not from a policy document. "Trust me, the prompt says behave" is not a control.

## The worked example, said plainly

Here is one behavior. I built it as a small reference implementation in my test environment — the code is in [`oscal-agent-controls`](https://github.com/williamzujkowski/oscal-agent-controls) — so everything below actually runs. The agent may call only the tools listed in a committed `agent-policy.yaml`. A separate, tighter allowlist governs where a secret may go. Every decision is logged.

I'll describe the OSCAL in Simplified Technical English on purpose — short sentences, one action each. It reads like a checklist because a control *is* a checklist.

Model the agent as an OSCAL software component. Give the component one `control-implementation`. Set its `source` to the NIST SP 800-53 Rev 5 catalog. Add one `implemented-requirement` for **AC-6** (least privilege). Set the default tool decision to `deny`. Add a property that names the policy file. Add a property that names the check a pipeline must run.

```json
{
  "control-id": "ac-6",
  "description": "The runtime exposes only task-approved tools and denies all other tool calls before execution.",
  "props": [
    { "name": "agent-control", "ns": "https://example.local/ns/agent-controls", "value": "tool-allowlist" },
    { "name": "default-decision", "ns": "https://example.local/ns/agent-controls", "value": "deny" },
    { "name": "policy-file", "ns": "https://example.local/ns/agent-controls", "value": "agent-policy.yaml" },
    { "name": "pipeline-assertion", "ns": "https://example.local/ns/agent-controls", "value": "all_tool_calls_subset_of_allowed_tools" }
  ]
}
```

Add a second requirement for **AC-4** (information flow enforcement): block any tool call that would transmit a detected secret to an unapproved destination. Add a third for **AU-12** (audit record generation): every requested, allowed, denied, and reviewed call writes a structured record. `CM-7` (least functionality) and `SI-4` (system monitoring) map onto the same behaviors, though this example doesn't verify them independently. *(The full component definition — synthetic namespaces, fake tool names throughout — lives in the repo; the `ac-6` slice above is the shape.)*

The gate itself is a fixed decision cascade. The first check that fails denies, and nothing downstream re-opens the question:

<div class="flow" role="group" aria-label="Reference-monitor decision cascade for one tool call">
  <div class="flow-node">Agent tool call</div>
  <div class="flow-node is-gate"><b>On the tool allowlist?</b><i>else deny: tool-not-allowlisted</i></div>
  <div class="flow-node is-gate"><b>Action permitted for the tool?</b><i>else deny: action-not-permitted</i></div>
  <div class="flow-node is-gate"><b>Destination permitted?</b><i>else deny: destination-not-permitted</i></div>
  <div class="flow-node is-gate"><b>Secret bound off the egress allowlist?</b><i>if yes, deny: secret-egress-blocked</i></div>
  <div class="flow-branch" role="group" aria-label="Final decision">
    <div class="flow-leg" data-branch="all gates pass" role="group" aria-label="all gates pass"><div class="flow-node is-good"><b>ALLOW</b><i>matched-allow-rule</i></div></div>
    <div class="flow-leg" data-branch="any gate fails" role="group" aria-label="any gate fails"><div class="flow-node is-bad"><b>DENY</b><i>deny by default</i></div></div>
  </div>
</div>

Now the pipeline does the work the prose can't. It reads the component definition. It loads the policy file. It confirms `ac-6`, `ac-4`, and `au-12` are present. Then it runs the tests against the gate. An unlisted tool call is denied. An allowed tool used for an unpermitted action is denied. An allowed tool aimed at an unapproved destination is denied. And the interesting one: an allowed tool calling an *approved* destination is still denied when its payload carries a secret — because secret-egress is a separate, tighter allowlist than tool use, and it wins. Two legitimate calls are allowed. Every decision, allow or deny, writes an audit record with the required fields. The pipeline emits an OSCAL `assessment-results` file: nine findings, all pass.

That last step is the whole point. The control is no longer a sentence someone hopes is true. It's an assertion something ran, against a real runtime, and recorded the answer — a machine-readable finding you can diff on the next commit:

```json
{
  "title": "deny secret egress",
  "description": "expected deny/secret-egress-blocked, got deny/secret-egress-blocked",
  "target": {
    "target-id": "ac-4",
    "type": "objective-id",
    "status": { "state": "pass", "reason": "satisfied" }
  }
}
```

## What actually changed

Nothing in OSCAL needed inventing. The component-definition model already carries `props` for application-specific semantics and `links` for pointing at a policy schema. The 800-53 controls already exist. What changed is the *expression*: instead of documenting that a policy exists, the requirement names the deterministic decision, the enforcement default, the policy artifact, and the pipeline assertion that proves it. The control describes behavior a machine can check.

This isn't a solved space. NIST's [COSAiS](https://csrc.nist.gov/projects/cosais) project is actively developing 800-53 overlays for single- and multi-agent AI systems — the standards bodies already see agents as different enough to need tailored treatment. There's adjacent [AI risk-management guidance](https://www.nist.gov/itl/ai-risk-management-framework) too, though it's prose, not machine-checkable — which is rather the point. What I haven't found is a clean, public component-definition idiom for agent *runtime* behavior: tool allowlists, secret-egress denial, and the harder cases past them — delegated-credential scope, human-approval gates. This post takes the first two; the rest are the same shape.

To be clear about what this is and isn't: it's an idiom, not an authorization package. The example uses a fake policy namespace and synthetic tool names, and the control mapping is illustrative. But the shape holds. Agents make the difference between a control and a wish very concrete, because the agent will absolutely take the wish literally and then improvise. So write the control as something that can say no on its own — and keep the YAML for the part that proves it did.
