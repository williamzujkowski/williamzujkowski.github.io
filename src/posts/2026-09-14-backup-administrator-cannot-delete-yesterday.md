---
title: "Your Backup Administrator Should Not Be Able to Delete Yesterday"
date: 2026-09-14
description: "Timelock Drive puts retention below a compromised host. An offline model shows why unfreezing a backup must start a countdown, not erase its protection."
tags: [security, backup, storage, research, homelab]
draft: false
---

Timelock Drive is a storage design that makes yesterday's data harder to destroy even after an attacker takes over the machine managing it. Its useful question is blunt: who can overrule retention? The [OSDI 2026 paper](https://www.usenix.org/conference/osdi26/presentation/rosenblum) places that decision in an isolated checker beneath the host. The administrator can request a change. The checker can decline.

That is a more interesting backup property than a reassuring padlock icon. An administrator account is occasionally an attacker account wearing its usual name.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Timelock Drive separates the compromised host from retention enforcement">
  <section class="arch-tier" data-label="Untrusted host" role="group" aria-label="Untrusted host"><span class="arch-chip is-warn">Administrator and operating system</span><span class="arch-chip">Versioning software</span></section>
  <section class="arch-tier" data-label="Trusted boundary" role="group" aria-label="Trusted boundary"><span class="arch-chip is-guard">Timelock checker</span><span class="arch-chip is-guard">Checker clock and protected state</span></section>
  <section class="arch-tier" data-label="Storage" role="group" aria-label="Storage"><span class="arch-chip is-primary">Protected data and metadata</span></section>
</div>
<figcaption>The host requests storage changes; the isolated checker enforces retention. This is a conceptual view, not a wiring diagram.</figcaption>
</figure>

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/timelock-retention.png'); width: min(240px, 62%); aspect-ratio: 380/417; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">Yesterday is still under guard.</p>

## Unfreeze does not mean writable

The paper's particularly useful distinction is between *frozen* and *counting down*. A frozen block stays protected indefinitely. Unfreezing starts its original retention duration; it does not grant immediate permission to overwrite. The checker also protects metadata, because corrupting the record of a lock would defeat the lock. These mechanisms assume an isolated, non-decreasing checker clock. See [§§2–3 and Figure 2b](https://www.usenix.org/system/files/osdi26-rosenblum.pdf).

Here is the practical reading: removing a version from active use should not consume the time needed to discover that removing it was a mistake. An old but still-live block should not quietly run out of protection merely because it was created a long time ago.

This is a research design with an interposed prototype, not firmware to install on an ordinary backup disk. Its threat model excludes physical destruction and treats exfiltration separately. Recovery also depends on retaining a pre-intrusion state until detection; the retention window is not a promise of indefinite recovery. Those boundaries matter more than a headline performance number. [Paper, §§2 and 5](https://www.usenix.org/system/files/osdi26-rosenblum.pdf).

## A small model with a deliberately bad clock

The accompanying [offline experiment](https://github.com/williamzujkowski/williamzujkowski.github.io/tree/main/scripts/security-labs/timelock) reduces the transition to one synthetic value, integer time, and mutation requests. It ran on September 11, 2026: eight deterministic cases, 34 operations, no disk devices, backup files, network connections, or malware. The [raw JSON](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/timelock/results-2026-09-11.json) records every request and resulting state.

The retention interval is seven invented ticks. They are not seconds, days, or a recommended backup policy. The model begins with an already-written, frozen value called `yesterday`. It permits writes and deletion only strictly after expiry, following Figure 2b's boundary.

<div class="flow" role="group" aria-label="The model's seven-tick retention starts at unfreeze">
  <div class="flow-node"><b>Frozen</b><i>Still protected at tick 100</i></div>
  <div class="flow-node is-gate"><b>Unfreeze at 100</b><i>Expiry becomes 107</i></div>
  <div class="flow-node"><b>Tick 107</b><i>Mutation still denied</i></div>
  <div class="flow-node is-good"><b>Tick 108</b><i>Mutation permitted</i></div>
</div>

The most informative observations were the controls, not the rejected requests:

| Case | Observed result |
| --- | --- |
| Frozen value reaches tick 100 | Overwrite and deletion rejected |
| Wrong design starts expiry at creation | Deletion succeeds at tick 100 without unfreezing |
| Unfreeze at 100, then delete at 106, 107, 108 | Denied, denied, allowed |
| Host jumps its clock to 1,000 | Correct model denies early deletion |
| Wrong design trusts that host clock | Identical deletion request succeeds |
| Checker time moves backward from 6 to 0 | Clock update rejected; value remains protected |
| Host moves its clock backward | Does not postpone deletion once checker time permits it |

These are [model results](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/timelock/results-2026-09-11.json), not observations of Timelock Drive. The early-overwrite case also rejects shortening the original interval and a repeated unfreeze request. The deliberately broken controls show that the exercise can distinguish two faulty policies from the intended one. A program that rejects everything would fail the expiry control. Creation-based expiry is legitimate for a fixed-retention policy; it is wrong here because the requirement is to protect a live, frozen value until release starts its countdown.

The [five unit tests](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/timelock/test_timelock.py) passed, including checks across different frozen lifetimes and both mutation operations. They establish bounded behavior of this Python program. They do not establish a storage guarantee: another Python caller can directly change its fields. The real isolation boundary is the part the model assumes away.

## Retention is already a product feature. Read the escape hatch.

The paper should sharpen questions about existing systems, not make timed retention sound newly invented. [Amazon S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html#object-lock-retention-modes) documents a concrete distinction: governance retention allows a specially authorized bypass; compliance retention prevents object-version deletion or shortening by users, including the account's root user. AWS separately names account deletion as an exception. Those are different administrative boundaries.

AWS also documents [variable retention with event holds](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html#object-lock-retention-periods): release sets the retention deadline from that event plus a duration. That is a close existing analogue to the countdown; the paper's isolated block-level checker is the distinction examined here.

The same documentation says protection applies to an object **version**. A simple delete can add a delete marker while the protected version remains. That means a successful delete response and an unrecoverable backup are different observations. A retention test needs to check the retained version, not merely the latest-object listing. [Object Lock deletion behavior](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html#object-lock-delete).

For a disposable homelab test, the interesting evidence would therefore be a small manifest: protected version identifier, retention mode, expiry, identity making each request, and the result of recovering the original bytes. Include a successful deletion after expiry as a control. This post did not perform that cloud test; it is a proposed extension, with real account permissions and storage costs to inspect first.

## The recovery question still comes afterward

An undeleted block is only one part of a useful restore. The next test should ask whether the recovery procedure can locate the right version and make its contents usable. That question is deliberately absent from the tiny state model: it has no catalog, encryption keys, filesystem, or application to restore. Its [limitations](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/scripts/security-labs/timelock/README.md) also exclude persistent clocks, crash recovery, and authenticated metadata.

This gives the backup review a better order. First identify the authority that can destroy a retained version. Then check which operations cross that boundary, including policy changes and time handling. Finally exercise recovery with the surviving data. Keep those observations separate; a green retention test cannot answer an unrun restore test.

Put an attempted early deletion in the next disposable restore drill, alongside the successful restore. Record which identity tried it and where the refusal came from. A retention setting becomes much more informative when someone has actually tried to overrule it.
