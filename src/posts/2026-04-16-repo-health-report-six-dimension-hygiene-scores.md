---
title: "Grading GitHub Repos: Six-Dimension Hygiene Scores from repo-health-report"
date: 2026-04-16
description: "A static-analysis tool that grades any GitHub repo across security, testing, docs, architecture, devops, and maintenance. The methodology is still WIP, but the findings are consistent: most repos are skipping the basics."
tags: [open-source, security, devops, typescript, tooling]
image: https://images.unsplash.com/photo-1588543847037-cb1a75fa9fb6?w=1200&h=630
imageAlt: "Clipboard with a checklist and red pen on a wooden desk"
author: William Zujkowski
---

I wrote a tool called [repo-health-report](https://github.com/williamzujkowski/repo-health-report) that pulls a GitHub repo's metadata through the API and grades it across six dimensions. No cloning, no secrets, no runtime. Just a sustained `gh api` session and ~100 checks that fit in a terminal scroll.

The methodology is still a work in progress. I keep finding edge cases that my heuristics either miss or overscore. But after running it across a few dozen of my own repos and a handful of well-known open source projects, one finding dominates: **we lack basic hygiene everywhere**, and the gap isn't between "good repos" and "bad repos." It's between "repos that have checked two or three boxes" and "repos that haven't."

## The six dimensions

The scorer evaluates these with static heuristics, each weighted to a 0-100 scale:

1. **Security.** Pinned action SHAs, explicit workflow permissions, Dependabot, secret scanning + push protection, SBOM, SAST, CODEOWNERS, `.gitignore`, security policy. 18 checks.
2. **Testing.** CI workflows present, test files exist, coverage config, test runner configured, pre-commit hooks. 5 checks.
3. **Documentation.** README length + quality, CONTRIBUTING, CODE_OF_CONDUCT, LICENSE, CHANGELOG, examples, API docs. 8 checks.
4. **Architecture.** File organization, clear separation of concerns, language/framework conventions, modularity heuristics. 6 checks.
5. **DevOps.** Build workflow, release automation, deploy pipeline, container / package publishing, status badges. 7 checks.
6. **Maintenance.** Issue/PR response times, stale issue ratio, commit recency, dependency freshness. 6 checks.

Each check returns `PASS`, `FAIL`, or `WARN` with a one-line explanation. The report is color-coded terminal output plus a Markdown sidecar file for CI integration.

## A sample report

Here's the output for nexus-agents (the codebase this blog runs on):

```
Overall Grade: A (96/100) — excellent

| Dimension     | Score    | Grade |
|---------------|---------:|-------|
| Security      |  97/100  | A     |
| Testing       | 100/100  | A     |
| Documentation | 100/100  | A     |
| Architecture  | 100/100  | A     |
| DevOps        | 100/100  | A     |
| Maintenance   |  77/100  | C     |
```

The 77/100 on Maintenance is real. I have 12 open Dependabot alerts, 40+ open issues, and a backlog of deferred refactors. The scorer isn't flattering me — it's flagging debt I should address.

Now here's a scored-privately report for an average repo I've run against (name withheld, typical mid-sized open source project):

```
Overall Grade: C (68/100) — fair

| Dimension     | Score   | Grade |
|---------------|--------:|-------|
| Security      | 45/100  | F     |
| Testing       | 72/100  | C     |
| Documentation | 88/100  | B     |
| Architecture  | 80/100  | B     |
| DevOps        | 71/100  | C     |
| Maintenance   | 52/100  | F     |
```

Security at 45/100 is alarmingly common. The specific failures:

- [FAIL] **Pinned dependencies (Actions SHA).** Actions referenced by tag or branch, not SHA. One supply-chain compromise away from malicious workflow code.
- [FAIL] **Token permissions.** No workflow has explicit restrictive permissions. Default is contents:write across all jobs.
- [FAIL] **Push protection.** Secret scanning push protection disabled. Commits with secrets land in history before detection.
- [FAIL] **SBOM.** No software bill of materials published. Downstream consumers can't validate dependency chains.
- [WARN] **SAST.** No CodeQL or Semgrep workflow. Static analysis is a one-file commit away.

None of these are hard to fix. Most take 5-30 minutes. The pattern I keep seeing is that repos accumulate features and never come back to do the hygiene sweep.

## Why it's static analysis

The tool queries the GitHub API — repository metadata, workflow files, security config, commit activity, issue/PR data. It doesn't clone the repo. It doesn't need a GitHub App. It doesn't need a PAT with elevated permissions. Authenticated `gh` CLI is enough.

That design choice keeps it cheap to run (one `npx` invocation), safe for private repos (no code leaves your environment), and fast (a typical run finishes in 30-90 seconds).

The tradeoff: the tool can't assess code-level quality. It sees that a test runner is configured but not whether the tests are meaningful. It sees that a README exists but not whether the README is accurate. That's why "Documentation: 100/100" on nexus-agents means "all the required docs exist," not "the docs are up-to-date with the code." A harder problem for a different tool.

## The AI flag

There's an optional `--ai` flag that hands findings to a [nexus-agents](https://github.com/williamzujkowski/nexus-agents) session for deeper analysis:

```sh
npx repo-health-report owner/repo --ai
```

This takes the static findings and asks a model to synthesize themes, prioritize fixes, and identify patterns across dimensions. It's useful when you're triaging three or four repos and need "what should I fix first" rather than "what did the heuristic flag."

The AI pass doesn't override the static scores. It annotates them. The final grade is always from the deterministic rules so the output is reproducible.

## What WIP methodology actually means

Several dimensions have heuristics I'm not confident about yet:

- **Architecture scoring.** Right now I weight file organization (src/tests separation, no root-level source), presence of language-standard config files, and module count. These are weak proxies. A monorepo with impeccable internal structure can score lower than a flat Python project because the file counts trip my heuristics.
- **Maintenance scoring.** I use a 90-day rolling window for commit recency, but that penalizes projects that are feature-complete and correctly in maintenance mode. A project that hasn't shipped in 6 months because it works isn't unhealthy.
- **DevOps scoring.** Badge detection via README parsing is brittle. A repo can have a working CI pipeline without a badge in the README and score low on a real capability.

These are on the list. I have a [tracking issue](https://github.com/williamzujkowski/repo-health-report/issues) for each and I'm working through them.

## What I keep rediscovering

**Most security failures are zero-effort fixes.** Pinning action SHAs is a find-and-replace. Explicit workflow permissions is a three-line YAML block. Dependabot is a checkbox. The cost of doing them is lower than the cost of reading this paragraph. Yet they're the most consistently failed checks.

**Documentation exists but is stale.** The README says the build command is `npm test`. Running it in `.github/workflows/ci.yml` uses `pnpm test`. This fails a "does the docs match the code" check that I haven't automated yet but definitely need to.

**"We'll do that later" isn't security debt, it's insecurity.** Supply chain compromises via unpinned actions are a pattern, not an edge case. [StepSecurity maintains a ledger](https://www.stepsecurity.io/) of compromised workflows that burned projects using unpinned references. Every tag in `uses:` is a reinvocation of that category of risk.

**Hygiene compounds.** Repos that pass the basics tend to pass the advanced checks too. Repos that fail the basics tend to fail everywhere. The scorer confirms this: the correlation between Security and DevOps scores across the sample I've run is high. Culture travels.

## Numbers

| Metric | Value |
|--------|------:|
| Checks per run | ~100 across 6 dimensions |
| Typical run time | 30-90 seconds |
| API calls per run | ~15-25 (cached where possible) |
| Repos I've scored | 40+ personal, plus spot checks on popular OSS |
| Average score (my own repos) | 82/100 (B) |
| Average Security dimension (random public repo spot checks) | ~55/100 (F-) |
| Most common FAIL | Pinned Actions SHA |
| Least common PASS | SBOM |

## Try it

```bash
npx repo-health-report williamzujkowski/nexus-agents
npx repo-health-report https://github.com/facebook/react
npx repo-health-report <your-own-repo>  # humbling, recommended
```

The [source](https://github.com/williamzujkowski/repo-health-report) is on GitHub. The methodology is explicitly a work in progress — I'll take PRs and issues on the scoring heuristics. The findings it surfaces are not WIP. They're consistent and they're fixable.

I applied these findings to nexus-agents itself. The OSSF Scorecard improvements (7.1 → 9+), CVE patches, CodeQL findings closed, and `validatePath` consolidation that landed in April are covered in the [modularization post](/posts/nexus-agents-april-month-of-modularization/). If you want a worked example of how the dimensions here translate into actual cleanup work, that's the follow-up.

Start with the Security dimension. That's where the biggest reduction in risk for the lowest effort lives. The hygiene is cheap. Skipping it isn't.
