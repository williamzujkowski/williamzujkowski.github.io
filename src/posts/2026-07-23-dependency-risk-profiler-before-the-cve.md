---
title: "Dependency Risk Profiler: Scoring a Dependency Before Anyone Files a CVE"
date: "2026-07-23"
lastUpdate: "2026-07-23"
description: "A small Python CLI that scores each dependency on the conditions that produce a future vulnerability — staleness, bus factor, governance — rather than waiting for a CVE to exist. What it measures, where it stops, and the joke it plays on itself."
author: "William Zujkowski"
tags: [security, supply-chain, python, open-source, dependencies]
readingTime: "9 min read"
---

`dependency-risk-profiler` is a small Python CLI that reads your `requirements.txt` — or `package-lock.json`, or `go.mod` — and gives every dependency a risk score from 0 to 5. The twist is what the score is *about*. It isn't "does this version have a known vulnerability." It's "does this package look like the kind of thing that's going to grow one."

That distinction is the whole reason it exists, so let me start there.

## The gap between "vulnerable" and "risky"

Most of the tooling you already run is reactive by design. Trivy and Grype answer a precise, useful question: does this exact version match a disclosed CVE? [EPSS](https://www.first.org/epss/) takes the pile of already-disclosed CVEs and re-ranks them by how likely each is to be exploited in the next month. [CISA's KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) is more reactive still — it lists the CVEs that are *confirmed* to be under active exploitation. Every one of these is genuinely worth having. I've [written before](/posts/2025-09-20-vulnerability-prioritization-epss-kev/) about wiring EPSS and KEV together to triage a backlog, and I stand by all of it.

But notice what they share: each needs a CVE to exist first. By the time a vulnerability has an identifier, you're already downstream of the interesting moment. The interesting moment is upstream — the year before, when a package quietly acquired the *conditions* for a future incident. One maintainer who stopped answering issues eighteen months ago. No security policy, no branch protection, a single point of human failure. That package isn't vulnerable today. It's just clearly on the way there, and nothing that keys off a CVE identifier will tell you so.

That's the space `dependency-risk-profiler` pokes at: leading indicators instead of trailing ones.

## What it actually measures

You point it at a manifest and it walks each dependency, pulling from the npm and PyPI JSON APIs, `pkg.go.dev`, and a shallow `git clone --depth 1` of the source repo for the signals that only live in git history. Each dependency gets scored on a handful of components, every one normalized to 0.0–1.0, weighted, and mapped onto LOW / MEDIUM / HIGH / CRITICAL bands:

- **Staleness** — time since the last commit. The quiet killer.
- **Maintainer count** — the bus factor, read off `git shortlog`. One maintainer is a governance risk, not a personality judgment.
- **Deprecation** — the registry sometimes just tells you the package is dead, if you ask.
- **Known-exploit flag** — this one *is* CVE-aware, and honestly so: it fans out to [OSV](https://osv.dev/), NVD, and the GitHub Advisory Database in parallel, caches the results, and normalizes the CVSS scores. Pre-CVE profiling doesn't mean ignoring the CVEs that already exist.
- **Version drift** — how far behind latest you're pinned.
- **Health signals** — the presence of tests, CI config, a `CONTRIBUTING.md`. Crude proxies, but they correlate.
- **License risk** — permissive vs. copyleft vs. the genuinely alarming "no license field at all."
- **Community health** — stars, forks, PR activity, bucketed rather than fetishized.
- **Governance checks** — and this is the part I'm fondest of. It mirrors a subset of [OpenSSF Scorecard](https://github.com/ossf/scorecard): `Maintained`, `Security-Policy`, `Branch-Protection`, `Dependency-Update-Tool`. If you're going to guess whether a project will handle its *next* vulnerability well, the way it's governed *now* is the best tell you've got.

Output is a rich terminal table or `--output json`, and there's a `--generate-graph` mode that renders the dependency tree (d3, graphviz, or cytoscape) so you can see where the risk clusters. Every weight is a flag — `--staleness-weight`, `--maintainer-weight`, and so on — because "risky" means different things for a hobby script and a payment system, and the tool shouldn't pretend otherwise.

## Where it stops — and this matters

The honest version of this post has to include the boundary, because "supply-chain risk" is a phrase people use to mean five different things.

`dependency-risk-profiler` does **not** detect typosquatting or dependency-confusion. It does **not** scan install scripts for malicious `postinstall` hooks. It does **not** verify [SLSA](https://slsa.dev/) provenance. If you want the malicious-package angle — the deliberate attacks catalogued in work like the [Backstabber's Knife Collection](https://arxiv.org/abs/2005.09535) — this is the wrong tool, and I'd rather say that plainly than let the word "supply-chain" imply a coverage it doesn't have. Its lane is maintenance decay and governance health: the slow, boring, accidental way most dependencies become liabilities. Not the adversarial way a few of them do.

It also isn't the runtime side of the problem. If you want to block a compromised dependency *as it executes*, that's a different design entirely — closer to the [runtime SBOM enforcement](/posts/2025-11-23-nodeshield-runtime-sbom-enforcement/) approach. Profiling is a pre-adoption, pre-renewal question. Enforcement is a runtime one. Both are worth having; neither is the other.

## The joke it plays on itself

Here's the part I can't leave out, because it's true and it's the most honest thing about the project.

I built `dependency-risk-profiler` in a three-day sprint: 134 commits between April 15th and April 18th, 2025. And then nothing. Not one commit since.

By its own staleness heuristic — where more than a year without an update maxes out the risk score — the tool would now flag *itself* as high-risk. A thing built to measure whether your dependencies have been quietly abandoned has, itself, been quietly abandoned. You can read that as irony or as unusually rigorous dogfooding, depending on how charitable you're feeling on a given day.

I'm inclined to be charitable, because it's the normal shape of a useful side project: built in a burst to answer a question I actually had, used, learned from, set down. The score isn't wrong about it. That's rather the point — the metric is honest even when it's inconvenient, which is the only kind of security metric worth shipping. If anything, running the profiler on its own repo is the cleanest demo it has.

## What I'd keep and what I'd change

The core bet still looks right to me: governance and maintenance signals are a real leading indicator, and Scorecard-style checks are a better predictor of "will this project handle its next CVE competently" than any point-in-time vulnerability scan. That part I'd build again.

What I'd change is the humility of the output. A 0–5 score with four crisp bands *feels* more precise than the underlying signals justify — a single-maintainer package that ships tests and a security policy is a genuinely different animal from a single-maintainer package that ships neither, and a scalar risk band flattens that. Next time I'd surface the *reasons* as first-class output, not just the number. The number tells you where to look. The reasons tell you whether to actually worry.

Which, come to think of it, is the same lesson EPSS learned the expensive way: a score is only useful if you can see what drove it.

## Sources

- Jacobs, Romanosky, Suciu, Edwards, Sarabi — *Enhancing Vulnerability Prioritization: Data-Driven Exploit Predictions with Community-Driven Insights* (EPSS v3), 2023. [arxiv.org/abs/2302.14172](https://arxiv.org/abs/2302.14172)
- Ohm, Plate, Sykosch, Meier — *Backstabber's Knife Collection: A Review of Open Source Software Supply Chain Attacks*, 2020. [arxiv.org/abs/2005.09535](https://arxiv.org/abs/2005.09535)
- FIRST.org — *Exploit Prediction Scoring System (EPSS)*. [first.org/epss](https://www.first.org/epss/)
- CISA — *Known Exploited Vulnerabilities Catalog*. [cisa.gov/known-exploited-vulnerabilities-catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- OpenSSF — *Scorecard* (checks reference). [github.com/ossf/scorecard](https://github.com/ossf/scorecard)
- OpenSSF — *SLSA: Supply-chain Levels for Software Artifacts*. [slsa.dev](https://slsa.dev/)
- `dependency-risk-profiler` — [github.com/williamzujkowski/dependency-risk-profiler](https://github.com/williamzujkowski/dependency-risk-profiler)
