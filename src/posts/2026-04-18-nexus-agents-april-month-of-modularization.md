---
title: "A Month of Modularization: nexus-agents in April 2026"
date: 2026-04-18
description: "Extracting benchmarks into a standalone package was the punchline. The setup was a month of governance, skills, security, and pipeline discipline that made the extraction possible in an afternoon."
tags: [ai, software-engineering, open-source, monorepo, typescript]
image: https://images.unsplash.com/photo-1506703719100-a0f3a48c0f86?w=1200&h=630
imageAlt: "Steel girder frame of a building under construction"
author: William Zujkowski
series: "Building AI Systems"
seriesOrder: 4
---

The visible work today was extracting SWE-bench out of nexus-agents into its own standalone package with a shared `BenchmarkAdapter` contract. The whole arc took about six hours across three npm releases. That speed wasn't an accident — it was possible because of three weeks of invisible work that preceded it.

This post covers the whole April 2026 arc on [nexus-agents](https://github.com/williamzujkowski/nexus-agents). The extraction is the capstone. The governance, skills, pipeline discipline, and security hardening that came before are the actual story.

## The shape of the month

246 commits across April 1-18. A partial inventory, grouped by theme:

- **Modularization / extraction** — BenchmarkAdapter contract, nexus-eval-template, nexus-eval-swebench, ecosystem tagging, soft-deprecation of in-tree benchmarks
- **Governance and skills** — subagent coordination rules, debugging discipline skill, drift audit skill, security-advisory-response skill, constraint-divergent design discipline
- **Expert rigor** — anti-pattern prohibitions across 9 experts, Push-Back Cues, Task Scope Management, Reference Implementation sections, mode split for code + architecture experts
- **Pipeline wiring** — learning loop (memory + trust + research + outcomes), security triage stages, codebase intelligence, circuit breakers, vote cascading, input sanitization, contrarian check
- **Security hardening** — OSSF Scorecard 7.1 → 9+, CodeQL findings closed, basic-ftp CVE patched, protobufjs CVE patched via override, 5 `validatePath` sites consolidated onto one safe primitive
- **Structural adapters over casts** — replaced the `RouterLike` cast with a typed structural adapter, runtime type-guards in expert result parsers
- **Human-facing notifications** — step-boundary notifications in pipeline, graph, execute-expert, consensus-plan, triangulated-review
- **Typed structured output** — `generateObject<T>` with parse-retry-with-feedback, replacing scattered JSON-parse-then-Zod-validate patterns

Seven releases landed in that window: v2.30.x through v2.33.2. Most were patch bumps for specific fixes; v2.31.0 shipped the human console notifications, v2.33.0-to-.2 shipped the benchmark extraction.

## Why modularization now

The immediate trigger was packaging hygiene. A `repo-health-report` pass (covered in the [follow-up post](/posts/repo-health-report-six-dimension-hygiene-scores/)) flagged that nexus-agents' npm tarball shipped 1.3MB of benchmark code that external users didn't need. SWE-bench alone was 840KB across 143 files.

The deeper trigger was that the benchmarks had started coupling to nexus-agents' release cadence. Every SWE-bench iteration required a nexus-agents version bump. Every nexus-agents release risked breaking benchmark CI. The two things were connected by history, not by design.

The fix required three preconditions that I hadn't appreciated going in:

1. **A stable public API surface.** If the benchmarks were going to consume `nexus-agents` as a peer dep, everything they needed had to be reliably exported. Not "can be deep-imported from `dist/` if you know the path." Actually in the top-level barrel.

2. **Non-flaky release automation.** Changesets + GitHub Actions had to work consistently enough that I could ship 2-3 patch releases in a day without babysitting them.

3. **A template that forced me to consume my own API.** If I couldn't bootstrap a new benchmark repo from a template and have its tests pass against the published npm package, the API wasn't done.

The first two came from the prior three weeks of work. The third was the extraction itself.

## The BenchmarkAdapter contract

The interface that everything extracts against:

```ts
export interface BenchmarkAdapter<TInstance, TPrediction, TEvalResult> {
  readonly name: string;
  readonly variant?: string;
  loadInstances(config): Promise<readonly TInstance[]>;
  runInstance(instance, ctx): Promise<TPrediction>;
  evaluate(instance, prediction): Promise<TEvalResult>;
  isPass(result: TEvalResult): boolean;
  summarize(results, runTimeMs): BenchmarkRunSummary;
}
```

Four methods, three type parameters, zero references to SWE-bench specifics. Any benchmark you can express as `load → run → evaluate → verdict` fits. HumanEval, MBPP, SWE-bench Pro, a custom internal evaluation — all the same shape.

The generic orchestrator lives in nexus-agents and looks like this:

```ts
const summary = await runBenchmark(new SweBenchAdapter({ variant: 'lite' }), {}, {
  concurrency: 4,
  limit: 10,
  onProgress: (done, total) => console.error(`[${done}/${total}]`),
});
```

`runBenchmark` owns concurrency, timeouts, progress, and partial failure. The adapter owns benchmark-specific logic. Separation of concerns at the seam where it mattered.

## The invisible bug that almost shipped

I built the BenchmarkAdapter contract, shipped nexus-agents v2.33.0, and started writing the template. Tests failed with `TypeError: runBenchmark is not a function`.

The contract existed in source. `packages/nexus-agents/src/benchmarks/adapter.ts` exported it. `packages/nexus-agents/src/benchmarks/index.ts` re-exported it. But nobody re-exported that barrel from `src/index.ts`, so the whole thing was invisible to consumers of the published package.

Three sub-bugs fell out of the investigation:

1. **Missing wire-up.** The benchmarks barrel wasn't in `src/index.ts` or the meta-barrel `exports/index.ts`.
2. **Symbol collision.** The new `OrchestratorOptions` type clashed with the existing workflow `OrchestratorOptions` already exported from `exports/agents.ts`. TypeScript silently dropped the conflicting re-export rather than failing loud.
3. **Function-name collision.** `estimateTokens` existed in both `benchmarks/token-benchmark.ts` (Mem0 4-char heuristic) and `agents/ictm/context-curator.ts` (context-curator variant).

The fix was a 113-line patch — rename, disambiguate, wire up the barrel, ship v2.33.1. The lesson was bigger. `export *` chains through barrels silently drop conflicting identifiers. Running `tsc --noEmit` on the public export chain and grep-ing for `error TS2308` reveals it. Not running that check was the bug.

I've since added export-contract tests that import every symbol from each barrel through the package entry and fail if any resolves to `undefined`. That's the kind of fence-post you only build after a ball has rolled over the edge.

## The template as forcing function

[nexus-eval-template](https://github.com/williamzujkowski/nexus-eval-template) is a GitHub template repository. Click "Use this template" and get:

```
src/adapter.ts       # 4 methods to implement, inline TODOs
src/cli.ts           # parseArgs CLI calling runBenchmark()
src/index.ts         # library export
src/adapter.test.ts  # 3 smoke tests proving the scaffold runs
```

The template's tests pass against the real `nexus-agents` npm package. That's the forcing function. If the scaffold can't run end-to-end, either the contract is incomplete or the public API has gaps. Both need fixing before any extraction happens.

Topic tags `nexus-agents-eval` and `nexus-agents-eval-template` make it discoverable via `gh search repos --owner williamzujkowski --topic nexus-agents-eval`. ECOSYSTEM.md in the main repo points at it. The whole discovery path is static.

## The SWE-bench extraction

With the template working, extracting SWE-bench became mechanical. Clone from the template, rename, implement a thin adapter:

```ts
export class SweBenchAdapter implements BenchmarkAdapter<
  SWEBenchInstance, SWEBenchPrediction, SweBenchAdapterEvalResult
> {
  readonly name = 'swe-bench';
  private readonly runner: SWEBenchRunner;

  async runInstance(instance, ctx) {
    const result = await this.runner.run([instance]);
    if (!result.ok) throw new SWEBenchRunnerError(...);
    return result.value[0].prediction;
  }
  // ... loadInstances, evaluate, summarize, isPass
}
```

[nexus-eval-swebench](https://github.com/williamzujkowski/nexus-eval-swebench) is a prediction-only MVP. It generates patches. It does not execute the Docker-backed test harness that would validate whether each patch resolves the underlying issue. That scoping was deliberate — Docker + ~60GB of prebuilt images + specific registry access don't belong in a default npm install. The README points users to `EvaluationHarness.evaluate()` from nexus-agents for the full pipeline.

`isPass()` reports generation completion, not test resolution. The summary metadata says so explicitly. If the tool over-claimed, it would be worse than a tool that scopes honestly.

## The rest of the month, briefly

The extraction wasn't the only thing that landed. The other threads:

### Human console notifications (v2.31.0)

Pipeline, graph, execute-expert, consensus-plan, and triangulated-review now emit step-boundary notifications to stderr. When a long orchestration is running, the operator sees which step is active in real time rather than staring at a spinner. Not dramatic — just good feedback loops.

### Expert rigor (PRs #1864, #1865, #1866, #1876, #1872)

The nine built-in experts grew:

- **Anti-pattern prohibitions** — each expert has an explicit list of things it refuses to do. "Code expert will not write tests that check for the absence of features." "Architecture expert will not recommend microservices for a project under 10 engineers." This cuts down on sycophantic "here's how you could do that" responses for things the expert shouldn't be doing.
- **Push-Back Cues** — language patterns that indicate the expert should push back rather than comply. "Just make this work" gets a request for the actual constraint. "Add a flag to disable the test" gets a question about what the test was catching.
- **Task Scope Management** — experts that notice when scope is creeping and propose a smaller scope rather than trying to satisfy the larger one.
- **Reference Implementation sections** — each expert ships canonical examples of what its output should look like, so consumers can calibrate expectations.

Combined, these made the experts less likely to produce plausible-looking-but-wrong output when asked to do something outside their scope.

### Skills refactor (PR #1828, #1832)

Migrated to the canonical `skills/<name>/SKILL.md` layout per the Anthropic Agent Skills spec. This lets non-Claude agents discover skills via `skills/index.yaml`. Not a lot of shipped functionality, but a lot of structural cleanup that unblocks follow-on work.

### Security hardening (PRs #1942, #1943, #1928, #1815, #1819, #1934)

- **OSSF Scorecard** went from 7.1 toward 9+ via pinned Actions SHAs, SBOM publishing, push protection, explicit workflow permissions, secret scanning.
- **CVE patches** for basic-ftp and protobufjs via pnpm `overrides`.
- **CodeQL findings** — six real bugs closed that earlier sweeps missed.
- **Path traversal consolidation** — five separate `validatePath` implementations across the codebase replaced by one `safe-path` primitive. Consistent behavior, easier to audit.

### Pipeline wiring (PRs #1763-1801)

The v2 pipeline grew its learning loop, security triage stages, codebase intelligence, circuit breakers, vote cascading, input sanitization, and contrarian check. These aren't end-user-visible changes — they're the mechanism that turns "run a task" into "run a task with memory of prior outcomes, trust scoring of agents, research context, and real-time outcome tracking."

### Typed structured output (PR #1897, #1940)

A new `generateObject<T>()` helper wraps CLI adapter execution:

- Appends Zod schema as JSON Schema instruction to the prompt
- Extracts JSON from the LLM response
- Validates with Zod
- On validation failure, retries once with the validation error fed back to the LLM ("Your previous response failed JSON validation: ...")
- Returns `Result<GenerateObjectResult<T>, GenerateObjectError>`

This replaces a scattered pattern of `extractJsonObject → JSON.parse → Zod.parse` that lived in consensus-plan, triangulated-review, security fix-generator, and finding-triage. Inspired by Vercel AI's `generateObject` and pydantic-ai's parse-retry-with-feedback pattern.

### Subagent coordination (PR #1882)

Adapted the hygiene rules from paperclipai/paperclip — the behavioral subset that translates to nexus-agents' synchronous subagent model. Explicit terminal state on every subagent response (`## Status: complete | blocked — reason | partial — cutoff at X of Y`). No silent trail-offs. Blockers surface in the same response they're hit in.

### Structural adapter over casts (PR #1921, #1927)

Replaced the `RouterLike` cast in the pipeline with a proper structural adapter. Casts paper over incompatibilities; adapters resolve them. The pipeline code got easier to reason about once the cast was gone.

## What I'd tell past-me

**Start with release automation.** If your release process requires babysitting, you won't ship 2-3 times in a day. The first week of April was mostly cleaning up the changesets + plugin.json version sync so that releases became boring. That investment made everything else possible.

**Typecheck the public export chain.** The v2.33.0 ship with an invisible barrel was preventable. Contract tests that import every symbol via the package entry and assert non-`undefined` would have caught it. I added those in v2.33.1. Adding them sooner would have saved a release.

**Template-first extraction.** Don't write the first real extraction (SWE-bench) before the template exists. The template forces the public API to actually be usable. If you find yourself wishing the adapter contract had one more method, the template will tell you before the extraction does.

**Governance and rigor compound.** Each individual rigor PR — anti-pattern prohibitions, Push-Back Cues, Reference Implementations — was small. The cumulative effect is that the experts produce dramatically better output than a month ago. Not because one PR was a breakthrough. Because eight were.

## Numbers

| Metric | Value |
|--------|------:|
| Commits April 1-18, 2026 | 246 |
| Releases shipped | 7 (v2.30.x through v2.33.2) |
| New public API exports (benchmarks) | 8 |
| Closed issues | 20+ |
| Merged PRs | 40+ |
| OSSF Scorecard change | 7.1 → 9+ |
| CVEs patched | 2 (basic-ftp, protobufjs) |
| CodeQL findings closed | 6 |
| `validatePath` sites consolidated | 5 → 1 |
| New standalone repos | 2 (nexus-eval-template, nexus-eval-swebench) |
| Sub-issues closed on the extraction epic (#1960) | 6 of 6 |
| Time from interface-design-done to v2.33.2-published | ~6 hours |

## Try it

- [nexus-agents v2.33.2](https://www.npmjs.com/package/nexus-agents) — `npm install nexus-agents`
- [nexus-eval-template](https://github.com/williamzujkowski/nexus-eval-template) — click "Use this template"
- [nexus-eval-swebench](https://github.com/williamzujkowski/nexus-eval-swebench) — `npx nexus-eval-swebench --variant lite --limit 5`

The extraction epic is [nexus-agents#1960](https://github.com/williamzujkowski/nexus-agents/issues/1960). All six sub-issues are closed. Follow-ups — Docker harness integration for real pass/fail, HumanEval and MBPP extractions — will file new issues against the standalone repos as they're prioritized.

The arc I care about more is the one that made this possible. Three weeks of rigor, governance, and release hygiene turned "extract a benchmark" from a multi-day refactor into an afternoon. If you're looking at your own monorepo wondering where to start, start with the boring preconditions. The extraction itself is easy when the rest of the work has been done.
