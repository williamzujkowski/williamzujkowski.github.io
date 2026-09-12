---
author: William Zujkowski
date: 2026-08-14
description: "SYSSPEC treats a filesystem specification as the thing an agent edits, then asks generated code to live up to the contract."
title: "The Filesystem Should Start as a Specification"
tags:
  - systems
  - ai
  - filesystems
  - security
---

There is a familiar way to ask an AI system to build a filesystem: describe the feature, paste the error, and hope the next patch does not quietly remove the lock you needed in the first place. Filesystems are a poor place to rely on hope. A missed ordering rule becomes a race, and a race becomes a corrupted directory at the least convenient possible moment.

The FAST '26 paper [“Sharpen the Spec, Cut the Code”](https://www.usenix.org/conference/fast26/presentation/liu-qingyuan) starts from a better boundary. SYSSPEC asks for a structured specification of functionality, modules, and concurrency obligations. An agent generates the implementation from that specification, and later changes are patches to the specification itself. The paper was available at the February 24–26, 2026 conference; its earlier [arXiv version](https://arxiv.org/abs/2512.13047v4) was posted before this article's date.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/specification-blueprint.png'); width: min(260px, 68%); aspect-ratio: 319/420; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the contract gets the pencil first</p>

That change sounds cosmetic until you follow where the invariant lives. In a prompt-only workflow, “lookup a directory entry” is a sentence. In SYSSPEC, it is a named operation with dependencies and rules that another operation must continue to respect. The generated code is still ordinary code. The contract is what makes a later change reviewable.

## A prompt is not a concurrency contract

The paper's generated filesystem, SPECFS, is concurrent and is evaluated against a manually written baseline. The authors report hundreds of regression tests and ten filesystem features evolved from the specification. Those are results for their artifact, not a guarantee that an arbitrary model can safely write a filesystem. The useful claim is narrower: a structured, machine-readable description gives the generator something more precise than prose to preserve.

That distinction matters for security. A filesystem has at least three different questions hiding inside a sentence such as “rename this entry”: which names and directory objects may be observed; which locks or ordering constraints protect the transition; and what state must remain true if the operation fails halfway through. A code review can miss any one of them. A specification cannot make the implementation correct by itself, but it can make the missing question visible.

SYSSPEC also uses a directed acyclic graph of specification patches. A feature branch that changes the implementation directly can accidentally fork an invariant. A patch that names the changed contract can be checked against the edges that depend on it. The graph does not remove merge conflicts; it gives the conflict something better to talk about than two piles of generated code.

## What the paper does not show

The evaluation does not turn SPECFS into a production filesystem. The paper explicitly leaves crash consistency and a direct storage stack outside its scope. Passing regression tests is evidence about those tests. It is not formal verification, and it is not evidence about every workload or failure mode.

If I were evaluating the artifact, I would start with one operation and one contract: a directory lookup, its allowed dependencies, and its locking obligation. I would read the generated implementation, run the supplied test for that operation in a disposable environment, and then write an independent test for the failure case the contract claims to cover. I would record the command, revision, and test result. I would not enable host-wide FUSE permissions or run an unknown launcher merely to make a persuasive screenshot.

The test is deliberately small. A generated filesystem that cannot explain one operation is not improved by generating ten more. A green result is useful only when the contract, implementation, and test are all visible at once.

## The practical lesson

Specification-first generation moves the review boundary. Instead of asking whether a large patch “looks right,” ask whether the requested change is represented in the contract, whether its dependencies are explicit, and whether the generated code still satisfies the old obligations.

That is a modest promise. It is also one an engineering team can check. The model remains probabilistic. The specification, parser, tests, and review diff can be deterministic. Put the uncertainty where it can be measured, and leave the filesystem with fewer opportunities to improvise.
