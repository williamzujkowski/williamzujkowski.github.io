---
title: "Zero CVEs Is Not a Safety Rating"
date: 2026-08-01
description: "CVE count is a lagging indicator of dependency risk. By the time one is filed, you've already shipped the code. The signals that actually predict trouble — maintenance cadence, maintainer concentration, provenance posture — are visible before the advisory, if you look."
tags:
- security
- supply-chain
- homelab
- dependencies
---

When [the trivy-action tags got force-pushed with malicious code](/posts/2026-03-21-trivy-supply-chain-compromise-ai-assisted-investigation), I found out on a Saturday morning, twelve hours in, the way most people did: scrolling a security feed. That post was about the scramble after — triage the blast radius, rotate the secrets, notify the neighbors. This one is about the part before, the part I keep wishing I'd been better at: noticing that a dependency was a risk while it was still just a risk, not yet an incident.

The tool most people reach for to answer "is this dependency safe" is a vulnerability scanner, and the number it hands back is a CVE count. That number is a rear-view mirror. A CVE is filed *after* someone finds the flaw, *after* it shipped, usually *after* you've already run it in CI. It's a real signal. It is not a leading one.

<div class="zine-doodle" aria-hidden="true" style="--doodle: url('/assets/doodles/cve-rearview.png'); width: min(300px, 70%); aspect-ratio: 400/303; margin: 2rem auto 0.5rem;"></div>
<p class="hand-note" style="text-align: center; display: block;">the danger you can see is already behind you</p>

## Zero is the most dangerous number

The counterintuitive part: a low CVE count is not evidence of safety, and it's sometimes evidence of the opposite. A popular, heavily-audited library accrues CVEs because people are *looking* — attention finds bugs, and finding bugs generates advisories. A dead single-maintainer package that three thousand projects depend on has zero CVEs because nobody has audited it since 2019. One of those is safer than the other, and it isn't the one with the clean scorecard.

So the number to distrust most is zero. Zero CVEs on a widely-used dependency means "unknown," not "clean." The interesting question isn't how many vulnerabilities have been *found* — it's how likely this dependency is to be the source of the next one, and whether you'd even hear about it if it were.

That question has leading indicators. None of them are oracles. All of them are cheaper to check than an incident is to clean up.

<figure class="arch-fig">
<div class="arch is-stack" role="group" aria-label="Leading dependency-risk signals versus the lagging CVE count">
  <section class="arch-tier" data-label="Leading — checkable before anything happens" role="group" aria-label="Leading — checkable before anything happens"><span class="arch-chip is-primary"><b>maintainer concentration</b><i>bus factor of one</i></span><span class="arch-chip is-guard"><b>release cadence</b><i>last commit / release gap</i></span><span class="arch-chip is-guard"><b>provenance posture</b><i>2FA, signed, attested</i></span><span class="arch-chip is-guard"><b>version drift</b><i>how far behind latest</i></span><span class="arch-chip is-guard"><b>license</b><i>missing / mismatched</i></span></section>
  <section class="arch-tier" data-label="Lagging — only after it shipped and someone looked" role="group" aria-label="Lagging — only after it shipped and someone looked"><span class="arch-chip is-bad"><b>CVE / advisory count</b><i>the rear-view mirror</i></span></section>
</div>
<figcaption>The leading signals are visible while you still have a choice; the CVE arrives after you've already run the code. A low count on the bottom row means "nobody has looked," not "nothing is there."</figcaption>
</figure>

## What actually predicts trouble

**Maintenance cadence.** OWASP's [Open Source Software Top 10](https://owasp.org/www-project-open-source-software-top-10/) lists "Unmaintained Software" as its own risk category (OSS-RISK-4), and the checks it suggests are the boring, observable ones: recent commits, release frequency, whether the repo is archived, whether issues get answered or just accumulate. An unmaintained dependency isn't dangerous because it's old — plenty of finished software is old. It's dangerous because when a vulnerability *is* found, there's nobody home to fix it, and you inherit the patch. I'll be honest about the strength of this signal: I couldn't find a clean study proving "abandoned today" forecasts "CVE next year." Treat cadence as triage, not prophecy. It tells you where to look first, not what will break.

**Maintainer concentration.** This is the [xz-utils](https://www.openwall.com/lists/oss-security/2024/03/29/4) lesson, and it's the one that changed how I read a dependency. `xz` was effectively solo-maintained; a helpful contributor spent *years* building trust before shipping the backdoor in 5.6.0 and 5.6.1 — releases they were, by then, trusted to sign ([CVE-2024-3094](https://nvd.nist.gov/vuln/detail/CVE-2024-3094)). The leading signal there wasn't a code smell a scanner could catch. It was social: a critical, single-maintainer project under exactly the kind of burnout pressure that makes a too-good-to-be-true co-maintainer look like relief. A bus factor of one is a security property, not just a project-management one.

**Provenance posture.** Can the package tell you who built the artifact you're installing, and how? The ecosystems have quietly made this checkable. [PyPI has required two-factor auth for every maintainer since January 2024](https://blog.pypi.org/posts/2024-01-01-2fa-enforced/) and supports build attestations under [PEP 740](https://peps.python.org/pep-0740/); [npm's trusted publishing](https://docs.npmjs.com/trusted-publishers/) swaps long-lived tokens for short-lived OIDC from CI and emits provenance automatically; [SLSA](https://slsa.dev/spec/v1.2/build-requirements) puts numbers on how unforgeable that provenance is. A dependency published from a laptop with a token from 2021 is a different risk than one published with provenance from a hosted build — even if both have zero CVEs.

**License.** Not a vulnerability signal at all, but a triage gate worth one glance: a missing or non-[SPDX](https://spdx.org/licenses/) license, or a copyleft obligation that doesn't match how you ship, is a reason to slow down before adopting — separate from whether the code is safe.

The good news is you don't have to compute these by hand. [OpenSSF Scorecard](https://github.com/ossf/scorecard) already scores most of them — Maintained, Code-Review, Signed-Releases, Token-Permissions, Dangerous-Workflow, Pinned-Dependencies — on a 0-to-10 scale, and [deps.dev](https://docs.deps.dev/) exposes the whole picture (dependency graph, licenses, advisories, Scorecard) over a public API. The raw material for a leading-indicator triage pass is sitting there, free.

## How I actually use this

In my test environments I've stopped opening the vulnerability count first. Before I adopt a dependency I do a two-minute pass that's mostly the questions above: when was the last release, how many people can push to it, does it publish provenance, does deps.dev show anything already smoldering in its own dependency graph. It's not a gate that blocks a build. It's a bias — toward dependencies that would *tell me* if something went wrong, and away from the quiet ones that wouldn't.

The tool I kept wishing for was one I'd half-built and parked, so I went back and finished it: [`dependency-risk-profiler`](https://github.com/williamzujkowski/dependency-risk-profiler). Point it at a manifest — Python, npm, Go, Rust, Ruby, PHP, .NET, or Java, whether the Java project builds with Maven or Gradle — and it scores every dependency on the leading indicators: version drift, release cadence, maintainer concentration, provenance. It leans on the public sources (deps.dev, OpenSSF Scorecard, OSV, the registries) so the data-gathering is already done.

Two decisions do the real work, and both are about refusing to round up. A signal it couldn't measure is recorded as *unmeasured*, with the reason, and it leaves both halves of the average rather than quietly scoring a confident medium that looks earned. And an advisory only counts against you if it actually applies to the version you have installed — the rest get counted, listed, and kept out of the score rather than hidden or amplified.

Run it on a manifest with a couple of skeletons in it and the pre-incident signals lead:

```text
$ dependency-risk-profiler analyze requirements.txt

Dependency Risk · requirements.txt (python)
4 dependencies · overall 2.1 / 5.0 · 20 signals could not be measured

RISK     DEPENDENCY  VERSION            LEADING SIGNALS                                       ADVISORIES
HIGH     pycrypto    2.6.1 → 2.6.1      unmaintained ~12 years · Public domain license flag    2 scored · 6 filtered
MEDIUM   flask       3.0.0 → 3.1.3      stable, low release cadence · 1 minor version behind   1 scored · 9 filtered
MEDIUM   nose        1.3.7 → 1.3.7      unmaintained ~11 years                                 none
LOW      requests    2.31.0 → 2.34.2    stable, low release cadence · 3 minor versions behind  3 scored · 13 filtered

Worst first. "filtered" = advisories excluded from the score: ones that do not affect
the installed version, plus informational / withdrawn / low-confidence ones.
```

Read the `nose` row twice. Eleven years without a release, **zero advisories**, and it still lands above the actively-maintained library sitting three versions behind. That's the whole argument in one line: a CVE-first view sorts this list exactly backwards, because the package with nothing to report is the one nobody has looked at since 2015.

`pycrypto` is the other half. An abandoned cryptography library is a bad thing to have, and here it reads HIGH on *cadence*, with the advisories as corroboration rather than the verdict. And the filtered counts are the noise a CVE-first view would have amplified into panic — nine of flask's ten advisories don't apply to the version that's actually installed, so counting them would have been counting nothing. Hand it a GitHub token and the maintainer-concentration signal fills in from the API too, the bus-factor read that would have flagged xz.

That's one manifest. The version I actually run now points at a whole GitHub org or account — the same aim as [grading my own repos on hygiene](/posts/2026-04-16-repo-health-report-six-dimension-hygiene-scores), pointed outward at what those repos depend on instead of inward at how they're kept. It walks every repo, dedupes the dependencies across all of them, and ranks by blast radius — because the same sole-maintainer package sitting in thirty of your repos is thirty exposures, and the one worth fixing first is the one that reaches the most. Same leading-indicator triage, aimed at the whole codebase instead of one corner of it. It flags a dependency as *known-vulnerable* on a separate axis from its risk score, too, so a well-maintained library pinned to a version with a live advisory reads as exactly what it is — fine project, bad pin, update it — instead of getting averaged into a number that hides the fix.

## The honest limits

None of this would have reliably stopped xz. The attacker had a high-trust account, signed their releases, and played a multi-year game; a provenance check would have cheerfully confirmed that the backdoored tarball was signed by exactly the maintainer everyone trusted. Provenance tells you *who* built the artifact, not that they're honest. Scorecard itself says it's heuristic — false positives and false negatives included. Leading indicators raise the cost and the visibility of an attack; they don't buy certainty, and anyone selling certainty in this space is selling something.

That's not a knock on the method — it's the reason to run it as one layer, not a gate pretending to be the last word. Defense in depth works precisely because no single control has to be perfect: the scanner catches the known CVEs and patching closes them; the incident runbook is there for whatever still gets through. Leading-indicator triage sits in front of all of it — the layer that lets you, or an organization across every repo it owns, spend a dependency's risk down while spending it is still cheap. Swap the abandoned package, pin to the release that ships provenance, open the upgrade PR before the drift turns into a deadline. Small, boring moves, taken because a signal showed up early — which is the only reason they cost less than the incident they head off.

But that's the wrong bar. The trivy post was about how fast you can react after the tags get poisoned. This is the cheaper half of the same problem: you can respond well after the CVE, or you can weight the odds before it — notice the sole maintainer, prefer the package with provenance, distrust the zero.

And the window for reacting is closing. In June 2026 CISA issued [BOD 26-04](https://www.cisa.gov/news-events/directives/bod-26-04-prioritizing-security-updates-based-risk): three days to patch the vulnerabilities that clear all four of its high-risk bars — publicly reachable, in the [Known Exploited Vulnerabilities catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog), automatable end to end, and good for full system control — the most aggressive standing clock the directive series has carried. The reason it gives is blunt: AI is compressing the gap between a disclosure and a working exploit from months toward hours, and a proof-of-concept that used to cost a researcher a week now costs a model an afternoon. It binds federal agencies; the clock doesn't check whose network it's on.

When the reaction window is that short, reacting well stops being a strategy and becomes a bet you lose on a long enough timeline. So do both, but front-load the cheap half. The reaction is expensive and the triage is nearly free, and the whole point of a leading indicator is that it shows up while you still have a choice — across every repo you own, before the next proof-of-concept writes itself.

Here's the turn, though, and it's why this isn't a doom post: the same acceleration cuts both ways, and the defensive side of it is further along than the offense gets credit for. It has never been cheaper to spend a dependency's risk down than it is right now. The identifying is what this whole post is about; the boring middle of the fixing is increasingly work you can hand off. Point an agent at the structured report the tool already emits — every risky package with its blast radius, its advisories, the version that closes them, and the file to change — and it can open the issues, hunt down replacements, and draft the upgrade PRs while you keep the judgment call and the merge. That's how I run it across my own repos now. The attackers got a machine-speed offense; a machine-speed defense is sitting right there, mostly automatable — which is the first time in this fight I can say that and mean it.
