---
title: "Investigating the Trivy Supply Chain Compromise with AI Agents"
date: 2026-03-21
description: "How I used AI-assisted investigation to triage the trivy-action supply chain attack across my homelab and work repos — and some thoughts on weekend incident response and community notification gaps."
tags: [security, supply-chain, homelab, ai, incident-response]
author: William Zujkowski
---

On Friday March 19, someone force-pushed malicious code to 75 of 76 version tags in `aquasecurity/trivy-action`. If your CI pipeline pinned to any tag from `0.0.1` through `0.34.2`, you may have run code that exfiltrated your CI secrets, SSH keys, and environment variables to attacker-controlled infrastructure.

I found out about it the way most people do — scrolling through security Twitter on a Saturday morning. By that point, the attack had been active for over 12 hours.

## What Happened

The [advisory from Aqua Security](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23) describes it as a continuation of a supply chain attack that began in late February. Compromised credentials were used to publish a malicious Trivy v0.69.4 release, force-push 76 of 77 version tags in `trivy-action`, and replace all 7 tags in `setup-trivy`.

The malicious `entrypoint.sh` harvested CI environment variables, runner memory, SSH keys, and cloud credentials. It encrypted the bundle and exfiltrated it to a typosquat domain (`scan.aquasecurtiy.org` — note the misspelling) with fallback to Cloudflare tunnels. On some victims it created a `tpcp-docs` repository to stash exfiltrated data.

[Socket.dev](https://socket.dev/blog/trivy-under-attack-again-github-actions-compromise) and [Wiz](https://www.wiz.io/blog/trivy-compromised-teampcp-supply-chain-attack) published detailed analyses with IOCs.

## My Exposure

I maintain about a dozen repos across work and personal projects. Several use `trivy-action` in CI. When I saw the advisory, the question was simple: which repos were affected, and did any CI runs execute the compromised code during the attack window?

Rather than manually checking each repo's workflow files and CI history, I used [nexus-agents](https://github.com/williamzujkowski/nexus-agents) — a multi-model AI orchestration tool I've been building — to help with the investigation. The AI agents:

1. **Searched all local repos** for `trivy-action` references (`grep -rl` across `~git/*/`)
2. **Classified risk** by comparing each repo's pinned version against the known-compromised tag list
3. **Checked CI run history** for each affected repo during the compromise window via `gh run list`
4. **Verified IOCs** — checked for the `tpcp-docs` repository, suspicious local files (`sysmon.py`, `/tmp/pglog`), DNS indicators, and the malicious trivy v0.69.4 binary
5. **Created GitHub issues** on each affected repo with findings and remediation steps

The whole triage took about 20 minutes, including fixes. Without the AI assist, it would have been an hour of tab-switching between repos, workflows, and run logs.

## What I Found

Five repos had `trivy-action` references:

| Repo | Version | CI Runs During Window | Impact |
|---|---|---|---|
| **williamzujkowski.github.io** | `@master` (branch) | 28 runs | **Safe** — master branch wasn't affected |
| **homelab** | `@0.33.1` (tag) | 0 runs | **Safe** — no runs since Feb 18 |
| **mcp-standards-server** | `@0.32.0` (tag) | **1 run (Mar 20 03:50 UTC)** | **Potentially impacted** |
| **machine-rites** | `@master` (branch) | N/A | **Safe** — master unaffected |
| **standards** | SHA-pinned | N/A | **Safe** — pre-compromise commit |

The mcp-standards-server nightly scan executed the compromised `@0.32.0` tag on March 20 at 03:50 UTC — solidly within the attack window. The trivy job completed successfully in 53 seconds, meaning the malicious entrypoint ran.

However: no IOCs were found. No `tpcp-docs` repo appeared. No suspicious files on disk. The `GITHUB_TOKEN` available to that workflow had limited scope (`contents:read`, `security-events:write`) and expired after the run. Based on the IOC absence and limited token scope, I assessed this as low-impact and did not rotate secrets.

## The Fix

Every repo got the same remediation: pin `trivy-action` to the known-safe commit SHA (`57a97c7e7821a5776cebc9bb87c984fa69cba8f1`) instead of a mutable version tag. Tags can be force-pushed. Commit SHAs cannot.

```yaml
# Before (vulnerable — tags are mutable)
uses: aquasecurity/trivy-action@0.32.0

# After (safe — commit SHAs are immutable)
uses: aquasecurity/trivy-action@57a97c7e7821a5776cebc9bb87c984fa69cba8f1
```

This is the single most important lesson: **pin GitHub Actions to full commit SHAs, not version tags**. Tags are a convenience alias that repository maintainers (or attackers with compromised credentials) can change at any time.

## What Frustrated Me

**The notification gap.** The attack started Friday evening UTC. I learned about it Saturday morning from Twitter, not from GitHub, not from Aqua Security, and not from any automated alert. If I hadn't been casually reading security feeds on a weekend, I wouldn't have known until Monday.

GitHub Dependabot eventually created PRs on some repos, but only for the tag bump — not with any urgency indicator that this was a supply chain compromise, not a normal version update. The distinction matters enormously for triage priority.

**Weekend timing is not a coincidence.** Attackers consistently choose Friday evenings and weekends because response teams are slower, fewer eyes are on dashboards, and the blast radius window is wider. Every security team knows this. We should plan for it better.

**Mutable tags are a design flaw.** Git tags being force-pushable by anyone with write access means the entire version-pinning model for GitHub Actions is built on mutable references. GitHub could fix this by making action tags immutable once published, or by defaulting `uses:` resolution to the commit SHA behind a tag at set-pipeline time. Neither exists today.

## Empathy for the Responders

I want to acknowledge the Aqua Security team and everyone who worked through the weekend to contain this. Supply chain compromises are exhausting — you're racing against an attacker who chose the timing deliberately, coordinating with GitHub's trust and safety team, trying to notify an unknown number of affected users, and doing it all while your regular team is off for the weekend.

The post-incident advisory ([GHSA-69fq-xp46-6x23](https://github.com/aquasecurity/trivy/security/advisories/GHSA-69fq-xp46-6x23)) is thorough and honest about the root cause (incomplete credential rotation from a prior incident). That transparency matters.

## Lessons

1. **Pin actions to commit SHAs.** Not tags, not branches. SHAs are immutable.
2. **AI agents are genuinely useful for security triage.** Cross-repo grep, CI history analysis, IOC checking, and issue creation — all parallelizable tasks that benefit from automation.
3. **Have a weekend playbook.** If your security scanning runs on a schedule, know how to quickly check what ran and when.
4. **Monitor your dependencies' security advisories.** Don't rely on Twitter for incident notification.
5. **Scope your CI tokens narrowly.** The mcp-standards-server's limited `GITHUB_TOKEN` scope meant that even if secrets were exfiltrated, the blast radius was contained.

The repos involved: [nexus-agents](https://github.com/williamzujkowski/nexus-agents), [homelab](https://github.com/williamzujkowski/homelab-iac), [mcp-standards-server](https://github.com/williamzujkowski/mcp-standards-server).
