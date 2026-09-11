---
title: "Two Processes, One Page Cache: Testing Shared State Before Blaming the VM"
date: 2026-09-21
draft: false
description: "A small Linux experiment separates shared file identity from identical bytes, with a failed tmpfs control and a careful look at a July 2026 VM-isolation preprint."
tags: [linux, security, virtualization, storage, homelab]
---

Two programs can have separate address spaces and still benefit from the same cached file. For this post, the accompanying lab tested that ordinary Linux behavior with synthetic data: one child process read a page, and another read it afterward. Sharing the file made a clear difference. Giving the processes separate files containing identical bytes did not produce the same cache-residency change.

The experiment began with an unhelpfully perfect result. Every supposedly cold page was already resident. The temporary directory was in RAM. The benchmark had brought its own answer.

This is a local process experiment, motivated by a [July 2026 preprint about page-cache leakage across containers and VMs](https://arxiv.org/abs/2607.17518). It does not reproduce that paper's VM results. Its useful contribution is smaller: make the shared state visible, check the control, then ask what a virtualization boundary actually separates.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Shared file state beneath separate processes">
  <section class="arch-tier" data-label="Processes" role="group" aria-label="Processes"><span class="arch-chip">Reader A</span><span class="arch-chip">Reader B</span></section>
  <section class="arch-tier" data-label="File identity" role="group" aria-label="File identity"><span class="arch-chip is-primary">Same backing file</span></section>
  <section class="arch-tier" data-label="Kernel" role="group" aria-label="Kernel"><span class="arch-chip">Shared page-cache state</span></section>
</div>
<figcaption>Separate processes can read the same cached file pages. The control uses separately created files containing the same bytes.</figcaption>
</figure>

## The new paper asks about the storage path

Alon Abudraham, Xingyu Chen, Itamar Levi, and Ari Trachtenberg published *Isolation Failure From Shared Storage* on arXiv on July 20, 2026; this discussion uses [version 2, dated July 21](https://arxiv.org/html/2607.17518v2). The inspected record identifies a preprint, without a peer-reviewed venue.

Their threat model requires a local attacker colocated with the victim and storage objects sharing cache state beneath the isolation boundary. Their evaluation varies container runtimes and VM storage configurations. Shared, host-cacheable backing objects retain timing signals in their experiments; direct I/O and dedicated block-device configurations attenuate or remove the measured signal. Those conditions matter more than the headline's word “failure.” [Sections 3–4](https://arxiv.org/html/2607.17518v2#S3).

Page-cache attacks themselves are older. Gruss and colleagues demonstrated them in [*Page Cache Attacks*, CCS 2019](https://gruss.cc/files/pagecacheattacks.pdf). The 2026 work extends the environments under examination. It does not discover that a cache remembers things.

My [earlier gVisor post](/posts/2024-09-25-gvisor-container-sandboxing-security/) discusses reducing exposure to the host kernel. This question sits underneath that discussion: which file-backed state remains shared after requests pass through the runtime?

## A small experiment with a visible control

The [lab script and recorded evidence](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-09-11-page-cache-lab.md) use Python's standard library and Linux interfaces. Two generated 8 MiB files contain identical deterministic bytes but have different inodes. Each trial chooses a page offset and one of three conditions:

- **Shared file:** a primer child reads the target page before the probe child reads it.
- **Independent file:** the primer reads the corresponding page of the other file.
- **No primer:** only the probe child reads the target.

There are 60 trials per condition, shuffled with a recorded seed. Each read covers one 4 KiB page. The timed interval surrounds `pread` inside the probe child; launching Python and hashing the returned bytes happen outside it. This is elapsed read time, including any scheduling delay during that interval, rather than an isolated hardware latency.

Before every trial, the controller requests eviction of both generated files with `POSIX_FADV_DONTNEED`. That operation is advice, not a guarantee. The files are synchronized after creation because dirty pages need different handling. The [Linux manual](https://man7.org/linux/man-pages/man2/posix_fadvise.2.html) explicitly describes these limitations.

The controller also takes [mincore residency snapshots](https://man7.org/linux/man-pages/man2/mincore.2.html) before priming, after priming, and after probing. These snapshots check whether the intended state was established. They are not a timing classifier, and they say nothing about another user's private files.

## The first control failed

The initial run placed its fixtures in `/tmp`, which this machine mounts as `tmpfs`. Every target page was reported resident before priming: **180 out of 180 trials**. The three median read times clustered between **12.75 and 13.03 microseconds**. Calling that “no leakage” would have been a conclusion about an experiment that never established its cold condition. [First-run data](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-09-11-page-cache-results.json).

One change followed: place the same generated fixtures in a temporary directory on the repository's ext4 filesystem. The original run remains in the evidence record. No host-wide cache flush, memory-pressure workload, or additional privilege was introduced.

Review turned up a warning worth crediting: [*Eviction Notice*'s artifact appendix](https://snee.la/pdf/pubs/eviction-notice.pdf#page=16) already cautions that its implementation cannot run with `/tmp` mounted as `tmpfs`. This lab encountered that pitfall before finding the warning.

## On disk, file identity mattered

The second run established nonresident target pages before all 180 trials. Reading the shared target made its selected page resident in **60/60** trials. Reading the independent file did so in **0/60**; the no-primer condition also had **0/60** resident. After probing, every target page was resident. [Second-run data](https://github.com/williamzujkowski/williamzujkowski.github.io/blob/main/docs/research/2026-09-11-page-cache-ext4-results.json).

| Primer condition | Target resident before probe | Median probe read |
| --- | --- | --- |
| Shared target file | 60/60 | 13.15 µs |
| Independent file, identical bytes | 0/60 | 129.68 µs |
| No primer | 0/60 | 199.42 µs |

All trials remain in those medians, including reads exceeding four milliseconds. The difference between the two cold-condition medians deserves restraint: these are different shuffled trials on one running machine, not matched hardware measurements. No confidence interval or held-out classifier was calculated. The cleanest observation is the residency change; the timing difference accompanies it.

Both child processes intentionally received access to the test data. They ran under the same user. That makes the mechanism easy to inspect and keeps the experiment harmless. It also makes this a poor demonstration of a security boundary being crossed. A stranger did not recover a secret here.

## What carries over to a VM decision

A VM experiment still needs guest images, verified storage configuration, and controls for both guest and host caching. None of those is supplied by two Python children. The paper supplies evidence for its evaluated stacks; this lab supplies evidence for these files on this machine.

Between the 2019 paper and the July preprint, [*Eviction Notice*, presented at NDSS in February 2026](https://snee.la/pdf/pubs/eviction-notice.pdf), studied additional page-cache attack primitives and explained restrictions on residency interfaces. Being able to inspect a file this lab owns is not a bypass of those restrictions.

The practical next step is an inventory, not a cache-mode change: identify shared image layers, backing files, and host filesystem exports in the deployment under review. Then test the relevant path against the required threat model. Changing storage policy deserves its own performance and correctness review.

Before any of that, check whether the cold page is cold. `/tmp` is a convenient directory name. It is not a storage specification.
