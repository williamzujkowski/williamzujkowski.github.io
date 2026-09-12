---
author: William Zujkowski
date: 2026-08-18
description: "Pilot Execution treats recovery as a state-changing program and previews its cross-component effects before committing the action."
title: "The Recovery Button Deserves a Dry Run"
tags:
  - systems
  - reliability
  - security
  - distributed-systems
---

Recovery commands are often reviewed as if they were harmless instructions: restart the member, rebuild the index, move the leader, try again. The system is already unhealthy when someone runs them, which is precisely when a side effect is hardest to see. A recovery action can be locally sensible and still make another component's state worse.

The NSDI '26 paper [“Pilot Execution: Simulating Failure Recovery In Situ for Production Distributed Systems”](https://www.usenix.org/conference/nsdi26/presentation/li-zhenyu) treats recovery as a program that deserves a preview. The paper was presented May 4–6, 2026, before this post's date. Its PILOT framework runs a dry version of a recovery action in the live system's context, observes the effects, and commits only after the operator has a view of what would change.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/formal-gate.png'); width: min(300px, 76%); aspect-ratio: 420/198; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">let the gate see the blast radius</p>

The authors first study 75 real-world recovery failures. They report that cross-component interactions are a recurring source of trouble: a recovery path touches state that the initiating component does not own. PILOT is evaluated on five distributed systems and finds 17 of 20 recovery failures in that evaluation, including an unknown HBase bug. Those numbers belong to the paper's systems and workloads. They are not a universal failure rate.

## “Dry run” has to mean something

A command that prints what it intends to do is not automatically a dry run. A useful preview has to preserve the context that makes the action dangerous: leases, queues, membership, locks, and the state of the other components that will observe the change.

That is the paper's central distinction. PILOT does not merely validate the syntax of a recovery command. It follows the action through the execution path, records the effects that would be visible to the system, and isolates the final commit. The result is closer to a transaction preview than to a shell script with `--check` appended.

There are limits. A preview can miss consequences that depend on the action actually being committed. It can also inherit the blind spots of its instrumentation. A successful pilot is evidence that this execution did not expose a known bad interaction, not a proof that recovery is safe in every future state.

## A small lab version

A disposable local worker can expose four events: the caller's timeout, the cancellation request, the worker's actual termination, and cleanup of its temporary state. The harness can run a harmless counter and write a marker to a temporary directory. The preview records which events would happen; the commit performs them. A test then checks that a timed-out caller is not mistaken for a stopped worker.

That distinction is basic and routinely blurred. A timeout is an observation by the caller. Cancellation is a request. Termination is a fact about the worker. Cleanup is a separate operation with its own failure modes. Treating those as one boolean is how a recovery controller declares victory while the old work continues in the background.

The experiment should report its actual execution date and runtime version. It should not claim to reproduce PILOT's distributed evaluation. The point is to make the paper's boundary concrete: preview the state transition, name what the preview cannot see, and keep the final write behind an explicit commit.

## Recovery as a privileged write path

Recovery has the same security shape as an administrative API. It can mutate durable state while normal safeguards are already under pressure. That makes least privilege and auditability relevant even when the incident is accidental. A recovery role should be able to propose an action, inspect its predicted effects, and obtain an explicit commit authority. The preview itself should not silently perform the write it claims to simulate.

PILOT does not replace backups, fencing, or a human decision. It changes the question from “does this command look reasonable?” to “what does this action touch in the state that is actually present?” That is a much more useful question when the system has stopped behaving politely.
