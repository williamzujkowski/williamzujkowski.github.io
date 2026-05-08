---
title: "Patch Fast, Pull Slow: Defending in the Year of Copy Fail"
date: 2026-05-07
description: "AI is finding bugs faster, researchers pile on the moment one drops, and registries ship malware by the hundred-thousand. Defenders are caught between two contradictory imperatives. The fix is architectural, not temporal."
tags: [security, supply-chain, vulnerability-management, kernel, npm, homelab]
image: https://images.unsplash.com/photo-1614064641938-3bbee52942c7?w=1200&h=630
imageAlt: "Digital padlock surrounded by converging code — the defender in the middle"
author: William Zujkowski
---

A week ago I had two browser tabs open on my second monitor. The left one was [copy.fail](https://copy.fail/) — a fresh Linux kernel privilege escalation, nine-year exposure window, 732-byte exploit. The right one was [Sonatype's Q4 2025 malware index](https://www.sonatype.com/blog/open-source-malware-index-q4-2025-automation-overwhelms-ecosystems): 394,877 new malicious npm packages in a single quarter, a 476% jump.

The left tab said: **patch immediately or get popped by a script kiddie running yesterday's PoC.**
The right tab said: **hold your dependencies, audit before you pull, or get popped by a developer compromise of an upstream you depend on.**

Both are correct. They are also, literally, the opposite advice.

This is the squeeze defenders are living in now, and "balance speed and safety" is not a strategy. Below is what's actually going on, and what I'm doing about it in the homelab.

## The Left Jaw: AI Bugs and the Pile-On

Copy Fail ([CVE-2026-31431](https://copy.fail/)) is a straight-line logic flaw in the kernel's `algif_aead` module reachable through `AF_ALG` and `splice()`. No race, no offsets, no spray. Local unprivileged user → root, on basically every mainstream Linux distro built since 2017. The PoC is a 732-byte Python script that works unmodified across distributions. The bug was found by automated code scanning, not by a human chasing a hunch.

That last part matters. Watch the next two weeks.

On April 30 — one day after disclosure — [Copy_Fail2: Electric Boogaloo](https://github.com/0xdeadbeefnetwork/Copy_Fail2-Electric_Boogaloo) appears with the same primitive (page-cache write into any readable file) sourced from a different subsystem (XFRM/IPsec via `MSG_SPLICE_PAGES`). Brad Spengler's commentary tags it "copyfail-class." A few days later, [dirtyfrag](https://github.com/V4bel/dirtyfrag) drops from Hyunwoo Kim, chaining `xfrm-ESP` with `RxRPC` for a deterministic 4-byte STORE primitive that survives the first round of mitigations (algif_aead blacklisting). The dirtyfrag README is honest about the sequencing: Copy Fail "motivated this research." The embargo broke before patches existed.

This is the pile-on dynamic. One high-signal disclosure attracts a wave of researchers who go looking for the same shape of bug in adjacent subsystems, and they find them, because the shape was always there. The same week, [VulnCheck's 2026 exploitation report](https://www.vulncheck.com/blog/state-of-exploitation-2026) noted that **28.96% of known-exploited vulnerabilities in 2025 were exploited on or before the day their CVE was published**, up from 23.6% the year before. The Cloud Security Alliance has a name for what's happening: ["The Collapsing Exploit Window."](https://labs.cloudsecurityalliance.org/research/csa-whitepaper-collapsing-exploit-window-ai-speed-vulnerabil/) Mean time-to-exploit was 32 days in 2022, ~5 days in 2023, and is now under 5. AI systems generate working exploit code in 10-15 minutes for about a dollar a try.

If you read those numbers and your conclusion is "patch faster," you have only read the top half of the page.

## The Right Jaw: The Registry as a Weapon

While you're patching faster, the package registries you depend on are getting weaponized at industrial scale.

In 2025 attackers published **454,648 malicious npm packages** ([Sonatype 2026 SOSS Report](https://www.sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware)). 99% of new open-source malware now targets npm specifically. Q4 2025 alone accounted for 89% of the year's total — partly thanks to the [IndonesianFoods campaign](https://www.sonatype.com/blog/open-source-malware-index-q4-2025-automation-overwhelms-ecosystems), which generated a new malicious package every seven seconds. In September 2025 the [Shai-Hulud worm](https://socket.dev/blog/ongoing-supply-chain-attack-targets-crowdstrike-npm-packages) became the first known self-replicating npm malware, compromising 500+ packages in days by stealing maintainer credentials and republishing infected versions. The April 2026 SAP/npm wave that [The Register tracked](https://www.theregister.com/2026/04/30/supply_chain_attacks_sap_npm_packages/) is just the latest entry in a list that no longer fits in a tweet.

Read those numbers and the conclusion looks like "audit your dependencies before you pull."

Picture both jaws of a vise closing on you at once. The left jaw tightens whether you patch fast or slow: five-day mean time-to-exploit means the script kiddies are already running yesterday's PoC against any host you missed, and Copy Fail's nine-year window puts essentially every multi-tenant Linux box on the target list. The right jaw tightens whether you pin or pull: every `npm install --update` is a draw from a bag that grew by 394,877 poisoned cards in Q4 2025 alone, published by attackers who specifically optimize for the moments after a version goes live, before anyone has looked at it. A vise doesn't care how fast you wiggle. The squeeze is positional, not directional. The only way out is to change shape.

That is the squeeze.

## The Wrong Answers

Two answers to this paradox are popular, and both are wrong:

**"Just patch faster."** This works for kernel CVEs and vendor-signed binaries because the trust path runs through a known maintainer's release pipeline. It is actively dangerous when applied uniformly to npm/PyPI/RubyGems, where "patch faster" means "be the first organization to install the malicious 1.4.7 that landed forty minutes ago." The TeamPCP campaign weaponized this directly: scheduled scanners pulled mutable `aquasecurity/trivy-action` tags during the March attack window and ran the attacker's `entrypoint.sh`, then four days later the same playbook ran against `checkmarx/kics-github-action`. Patch velocity attacked patch velocity, twice, in the same month.

**"Wait, audit, marinate."** This works for dependencies whose maintainers and signing keys you actually verify. It is malpractice for actively-exploited kernel CVEs. The 9-year window on Copy Fail is not a comfort: it is the population of attackers who have had a working PoC for one week and a target list of every multi-tenant Linux host on the internet. There is no version of "let's see how this shakes out" that ends well at five days mean time-to-exploit.

Both answers fail because they treat **patching** and **pulling** as the same operation. They are not.

## The Twist: When the Scanner Is the Target

**The security tools themselves are now the preferred target. The guard dogs are carrying the payload.**

A single threat actor, [TeamPCP](https://www.wiz.io/blog/teampcp-attack-kics-github-action), has been running a sustained, chained campaign across the security-tooling supply chain:

- **Late February 2026:** initial breach of Trivy CI/CD; credentials exfiltrated. Aqua's first round of remediation is incomplete and some refreshed tokens leak too.
- **March 19, 2026:** [Trivy publicly compromised](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) — 76 of 77 version tags force-pushed, malicious `v0.69.4` published. ([Microsoft's defender guidance](https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/) and [my own homelab triage](/posts/2026-03-21-trivy-supply-chain-compromise-ai-assisted-investigation) followed.)
- **March 23, 2026:** [Checkmarx KICS GitHub Actions](https://socket.dev/blog/checkmarx-supply-chain-compromise) hit, reusing CI/CD secrets stolen from the Trivy intrusion. The same credential-stealing payload is grafted onto a different scanner.
- **April 22, 2026:** [second KICS compromise](https://www.bleepingcomputer.com/news/security/new-checkmarx-supply-chain-breach-affects-kics-analysis-tool/) — a threat actor authenticates to Docker Hub with valid Checkmarx publisher credentials and pushes malicious `checkmarx/kics` images. Two VS Code marketplace versions ship the same payload.
- **Same window:** LiteLLM caught as a downstream. [Vect ransomware](https://www.halcyon.ai/ransomware-alerts/trivy-supply-chain-compromise-enters-extortion-phase-as-vect-ransomware-publishes-first-victim) begins extorting the first round of Trivy victims, which is what monetization looks like once the credential harvest is complete.

[Palo Alto Unit 42 named the pattern directly](https://www.paloaltonetworks.com/blog/cloud-security/trivy-supply-chain-attack/): "When security scanners become the weapon." [Docker's own retrospective](https://www.docker.com/blog/trivy-kics-and-the-shape-of-supply-chain-attacks-so-far-in-2026/) calls Trivy and KICS "the shape of supply chain attacks so far in 2026."

Scanners and CI/CD security tools sit in privileged positions by definition. They read your filesystem, your container registries, your cloud APIs, and the secrets you handed them so they could check those things. They are wired into your CI with elevated permissions. They are the things you trust to *tell you when you're compromised*. Compromising one isn't equivalent to compromising any other npm dependency — it is closer to compromising a domain admin.

The patch lane I'm about to recommend assumes your scanner is on your side. When the scanner is the implant, the patch lane has been turned against you, and the workload that was supposed to *find* the malware has been generating it. The 44 Aqua repos defaced during the March incident were the visible damage; the credential harvest from CI runners across thousands of organizations was the real one.

Plan for it.

## The Resolution: Two Operations, Two Cadences

Patching applies a vendor-signed fix to known code. Pulling introduces new code from a registry.

Those operations have different trust paths, different blast radii, and they should run on different cadences. One cadence for both is exactly what the squeeze exploits.

| | Patch lane | Pull lane |
|---|---|---|
| **Trust anchor** | Vendor signing key, distro security team | Registry account, often a single maintainer |
| **Failure mode** | Slow patch → public exploit hits unpatched host | Fast pull → install fresh malware |
| **Optimal cadence** | Aggressive (hours-to-days for KEV) | Deliberate (cool-off period, version pinning) |
| **Right metric** | Mean time to remediate | Mean age of newly-pulled versions |
| **Wrong instinct** | "Wait and see" | "Always latest" |

Stop optimizing for "patch velocity" as a single number. Optimize for blast radius per lane.

## What I Do in the Homelab

These aren't hypothetical. This is what's deployed today on my home infrastructure:

**Patch lane — kernel and OS:**

- Unattended-upgrades runs nightly on every Debian/Ubuntu host. Security pocket only.
- KEV/EPSS-driven prioritization (the system [I described last September](/posts/2025-09-20-vulnerability-prioritization-epss-kev)) re-runs daily and pages me on KEV additions. For Copy Fail, the alert fired before I'd seen the announcement on Mastodon.
- Multi-tenant boxes (Proxmox guests that run user code, build runners, anything with `unprivileged_userns_clone=1`) get a different policy: I take them down and patch within hours, not days. The Copy Fail PoC works against them. Wait-and-see is not on the menu.

**Pull lane — application dependencies:**

- Lockfiles committed for everything. `npm ci` / `pip install --require-hashes`, never `npm install` in CI.
- A 7-day cool-off on new package versions, enforced via [Renovate](https://docs.renovatebot.com/configuration-options/#minimumreleaseage)'s `minimumReleaseAge: "7 days"` setting. Yes, this means I'm 7 days behind on ecosystem updates. That is the point. Most malicious-package campaigns burn out or get unpublished inside 72 hours; a one-week cool-off catches the long tail and costs me almost nothing in genuine velocity. Aggressive auto-pullers are footsteps in sand. The 7-day cool-off is closer to sandwalking: by the time I reach for the package, someone faster has already surfaced the worm and triggered the unpublish.
- Critically: the cool-off does *not* apply to security updates. Renovate's `vulnerabilityAlerts` block runs without `minimumReleaseAge` so that a fresh advisory for `express` or `requests` gets pulled immediately even though regular minor bumps wait the week. If you only set the cool-off and forget the security-alert override, you've handed yourself the worst of both lanes: slow on real CVEs *and* fast on attacker-published versions. Don't do that.
- GitHub Actions and Docker images pinned to commit SHAs / image digests, not tags. Tags are mutable; SHAs are not. (See the Trivy post for what happens when you don't.)
- Socket.dev wired into PR review on the repos I care about, mostly to flag install-script abuse and post-publish drift.
- A periodic `npm-why` / `pipdeptree` audit of how many packages I'm actually pulling, and an ongoing project to remove the ones I don't actually need. Every dependency is a trust surface; the cheapest one is the one I deleted.

**Scanner lane — treat security tools as privileged, not trusted:**

After the Trivy/KICS year, scanners get their own policy:

- Scoped, short-lived `GITHUB_TOKEN` for every scan job. Read-only by default, with `permissions:` declared explicitly per workflow. The Trivy-March intrusion was contained in my homelab because the affected token had `contents:read` and `security-events:write` and nothing else.
- Scanner action versions pinned to commit SHAs, never tags. Especially for the security tool itself — if I am going to trust a third party to read every file in my CI, I want bit-identical bytes between runs.
- Outbound network egress from CI runners restricted where the runtime supports it. The TeamPCP payload exfiltrated to attacker-controlled infrastructure. A CI runner that cannot reach arbitrary internet has a much smaller failure surface.
- A "second-opinion" cadence for findings: when a scanner says "you're clean," I do not treat that as evidence of cleanliness. I treat it as evidence the scanner ran. Different question.

**The cross-cutting practice — runtime containment:**

The patch lane and pull lane both eventually fail. When they do, the question is what the malicious code can reach. seccomp, user namespaces, eBPF egress filtering, capability dropping in Docker, and the SBOM-runtime enforcement experiment [I ran with NodeShield](/posts/2025-11-23-nodeshield-runtime-sbom-enforcement) all push toward the same answer: assume the install will eventually contain hostile code, and reduce what hostile code can do.

This is the part the "patch faster vs wait longer" debate keeps missing. **Neither lane needs to be perfect if the runtime can survive the misses.**

## What I'm Worried About

Three things keep me up.

**The pile-on is going to get worse, not better.** Copy Fail was found by an automated scanner. So is most of [Google's OSS-Fuzz output](https://google.github.io/oss-fuzz/), and Meta and Microsoft have published research on LLM-augmented fuzzing that materially raises the bug-discovery rate per researcher-hour. The economics of bug discovery are changing in a direction that produces more high-signal disclosures with shorter intervals between them, and each disclosure is an invitation to the next ten researchers. Defenders cannot patch their way out of a workload that grows superlinearly.

**Registry attackers are running their own AI loops.** Shai-Hulud was self-replicating. IndonesianFoods automated package generation. The next iteration is going to use an LLM to write convincing READMEs and `package.json` descriptions for each typosquat, in the maintainer's own English-as-second-language register, with realistic test files. The cool-off period buys time, but only if humans are looking during the cool-off.

**The scanner-as-target pattern is going to spread.** TeamPCP picked Trivy and KICS because those tools have privileged CI/CD positions and enterprise trust, and that math works for every other security vendor too. Snyk, Wiz, Falco, Grype, semgrep, the SBOM tools, the eBPF agents, the secret-scanning bots — every one of them has the same trust shape. I expect at least one more scanner-class compromise before the end of the year, and I'd love to be wrong.

## Lessons

1. **Patching and pulling are different operations.** Run them on different cadences against different threat models. Stop conflating them.
2. **Pin to immutable references — SHAs, hashes, digests.** Tags and `latest` are mutable; treat anything mutable as untrusted by default.
3. **Use a cool-off window for new package versions.** A week is plenty. The cost is small; the benefit is most malicious-package campaigns die before you'd have pulled them.
4. **KEV/EPSS triage for the patch lane, lockfile + audit for the pull lane.** Two systems, two dashboards, two on-call playbooks.
5. **Invest in runtime containment.** The lanes will fail. seccomp, user namespaces, egress filtering, and capability minimization decide what failure looks like.
6. **Watch what you're measuring.** "Mean time to patch" alone will quietly push you into the registry attacker's optimal scenario.
7. **Treat security tools as privileged, not trusted.** Pin them to SHAs, scope their tokens narrowly, restrict their egress, and assume any one of them can be the next Trivy.

Defenders are not getting more time or attention. Attackers know that, and they have organized three attack surfaces around it: the kernel, the registry, and the scanner that was supposed to watch the other two. The honest answer to the squeeze isn't to pick a side. It's to stop pretending the sides are the same problem.

---

*Sources used in this post:*

- [copy.fail (CVE-2026-31431)](https://copy.fail/)
- [Copy_Fail2: Electric Boogaloo PoC](https://github.com/0xdeadbeefnetwork/Copy_Fail2-Electric_Boogaloo)
- [dirtyfrag PoC (Hyunwoo Kim)](https://github.com/V4bel/dirtyfrag)
- [VulnCheck: State of Exploitation 2026](https://www.vulncheck.com/blog/state-of-exploitation-2026)
- [CSA: The Collapsing Exploit Window](https://labs.cloudsecurityalliance.org/research/csa-whitepaper-collapsing-exploit-window-ai-speed-vulnerabil/)
- [Sonatype 2026 State of the Software Supply Chain](https://www.sonatype.com/state-of-the-software-supply-chain/2026/open-source-malware)
- [Sonatype: Open Source Malware Index Q4 2025](https://www.sonatype.com/blog/open-source-malware-index-q4-2025-automation-overwhelms-ecosystems)
- [Socket.dev: Shai-Hulud npm worm coverage](https://socket.dev/blog/ongoing-supply-chain-attack-targets-crowdstrike-npm-packages)
- [The Register: April 2026 SAP npm wave](https://www.theregister.com/2026/04/30/supply_chain_attacks_sap_npm_packages/)
- [Renovate: minimumReleaseAge configuration](https://docs.renovatebot.com/configuration-options/#minimumreleaseage)
- [Wiz: TeamPCP attack on KICS GitHub Action](https://www.wiz.io/blog/teampcp-attack-kics-github-action)
- [Socket.dev: Checkmarx supply chain compromise](https://socket.dev/blog/checkmarx-supply-chain-compromise)
- [BleepingComputer: New Checkmarx supply-chain breach affects KICS](https://www.bleepingcomputer.com/news/security/new-checkmarx-supply-chain-breach-affects-kics-analysis-tool/)
- [Palo Alto Unit 42: When Security Scanners Become the Weapon](https://www.paloaltonetworks.com/blog/cloud-security/trivy-supply-chain-attack/)
- [Docker: Trivy, KICS, and the shape of supply chain attacks so far in 2026](https://www.docker.com/blog/trivy-kics-and-the-shape-of-supply-chain-attacks-so-far-in-2026/)
- [Microsoft Security: Detecting and defending against the Trivy supply chain compromise](https://www.microsoft.com/en-us/security/blog/2026/03/24/detecting-investigating-defending-against-trivy-supply-chain-compromise/)
- [Halcyon: Vect ransomware extortion phase](https://www.halcyon.ai/ransomware-alerts/trivy-supply-chain-compromise-enters-extortion-phase-as-vect-ransomware-publishes-first-victim)
