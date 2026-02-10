---
title: "Building Nexus-Agents: What I Learned Creating a Multi-Model AI Orchestration System"
date: "2026-02-09"
lastUpdate: "2026-02-09"
description: "The engineering story behind nexus-agents, a research-backed multi-model orchestration system that coordinates Claude, Gemini, and Codex through consensus voting, adaptive routing, and graph workflows."
author: "William Zujkowski"
tags: [ai, software-engineering, open-source, orchestration, typescript]
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630"
imageAlt: "Abstract visualization of interconnected neural network nodes"
readingTime: "12 min read"
---

About a year ago, I started building a routing script in my homelab because I was tired of switching between AI models manually. Claude produced better architecture docs. Gemini handled broad research faster. Codex was solid for focused code generation. I wanted one system that could pick the right model for each task automatically.

That routing script grew into [nexus-agents](https://github.com/williamzujkowski/nexus-agents), a multi-model orchestration platform built on published research from roughly 68 arXiv papers. Consensus voting, graph workflows, a plugin pipeline, adaptive bandit routing, a full TUI. I tried probably 30 different approaches before landing on the architecture that stuck. Here's what I found.

## The Problem With Single-Model Workflows

Most AI-assisted development workflows look like this: you pick one model, send it everything, and hope for the best. The model might be great at code generation but mediocre at [security analysis](/posts/ai-new-frontier-cybersecurity/). Or excellent at research but slow at producing clean TypeScript.

I was spending time not writing software but context-switching between tools. Open Claude for architecture planning. Switch to Gemini for broad research. Use Codex for rapid code generation. Copy context between them. Lose track of which model said what. Frustrating.

**The core insight:** Model selection is a routing problem, not a loyalty problem. Research on [LLM routing](https://arxiv.org/abs/2406.18510) confirms that different tasks have measurably different performance across models. A system that routes intelligently should outperform any single model used for everything. The [RouteLLM paper](https://arxiv.org/abs/2406.18510) showed this could cut costs 85% while maintaining quality, which convinced me the approach was worth pursuing.

## Architecture: Research-Backed, Not Ad Hoc

### The MCP Foundation

I built nexus-agents as an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server. This was the single most important architecture decision, though I didn't realize it at the time.

MCP gave me a standard interface that any compatible client could use. Claude Code, Cursor, Windsurf. Any MCP client gets access to the full orchestration system without custom integration. I wrote about [building MCP servers](/posts/building-mcp-standards-server/) separately, but the key takeaway is that MCP turned a custom tool into a platform. The server exposes 20 tools through MCP: task orchestration, expert agent creation, consensus voting, workflow execution, and research tracking.

An [STPA safety analysis of MCP](https://arxiv.org/abs/2601.08012) later validated some of my security concerns about the protocol. More on that below.

### CLI Adapter Pattern

Each AI model has quirks. Claude uses XML-style tool calls. Gemini has different token limits. Codex has its own API patterns. I needed an abstraction layer.

```typescript
interface CliAdapter {
  readonly cliName: string;
  executeTask(task: TaskConstraint): Promise<TaskOutcome>;
  isAvailable(): Promise<boolean>;
}
```

Every model interaction flows through this interface. The adapter handles serialization, token counting, error recovery, and timeout management. When a new model comes out, I write one adapter file. Everything else stays untouched.

The `ResilientAdapter` wrapper adds circuit breaker patterns. If a model fails three times in a row, the system stops trying it for a cooldown period and routes to alternatives. I learned this the hard way when an API outage cascaded through the whole system at 2am. That was a rough debugging session.

### Five-Stage Model Selection

Picking the right model for a task isn't simple. I built a five-stage routing pipeline, each stage backed by research:

**Stage 1, Budget Router:** If the billing mode is `plan` (monthly subscription), cost drops out entirely. Strongest models win. If billing is `api` (pay-per-token), cost factors into scoring.

**Stage 2, Zero Router:** Eliminates models that can't handle the task at all. If a task needs 100K context and a model maxes at 32K, it's out.

**Stage 3, Preference Router:** User preferences and task hints influence scoring. If you ask for a "security review," models with higher security quality scores get a boost.

**Stage 4, TOPSIS Router:** Multi-criteria decision analysis based on the [MoMA framework](https://arxiv.org/abs/2509.07571). Balances quality scores, context window fit, speed, and cost using the TOPSIS algorithm. This produces a ranked list of candidates.

**Stage 5, LinUCB Bandit:** The adaptive layer. Based on [PILOT](https://arxiv.org/abs/2508.21141), LinUCB is a contextual bandit algorithm that learns from outcomes. When a model succeeds at a task type, it gets a higher score next time. When it fails, the score drops. Over time, the system converges on optimal routing without manual tuning.

The entire pipeline runs in under 10ms. I was surprised how fast TOPSIS is when you're only ranking 6-8 models. The routing decision is nearly free compared to actual model inference. I wrote a [deeper dive on the routing research](/posts/routellm-contextual-bandits-model-router-research/) separately, including the approaches that didn't work.

## Consensus Voting: Multiple Perspectives on Hard Decisions

Some decisions are too important for a single model. Architecture changes, security modifications, breaking API changes. Research on [multi-agent collaboration](https://arxiv.org/abs/2501.06322) and [voting vs. consensus protocols](https://arxiv.org/abs/2502.19130) showed that structured multi-agent deliberation catches problems that individual models miss.

Nexus-agents creates specialized agent roles (architect, security engineer, DevEx advocate, PM, and a deliberately contrarian "catfish" agent), assigns them across available models round-robin, and collects votes with reasoning.

```
$ nexus-agents vote --proposal "Migrate from REST to gRPC for internal services" \
    --threshold supermajority

Architect (Claude):    APPROVE  (92% confidence)
Security (Gemini):     APPROVE  (88% confidence)
DevEx (Codex):         REJECT   (71% confidence)
PM (Claude):           APPROVE  (85% confidence)
Catfish (Gemini):      REJECT   (67% confidence)

Result: APPROVED (3-2, supermajority met)
```

The catfish role draws from [Free-MAD anti-conformity research](https://arxiv.org/abs/2509.11035). Its job is to find problems the others missed. It doesn't always change the outcome, but it consistently surfaces edge cases. I was skeptical at first, but after it caught a backwards-incompatible change that three other agents approved, I stopped questioning it.

Three voting strategies exist: majority (>50%), supermajority (>66%), and unanimous. A fourth, [higher-order voting](https://arxiv.org/abs/2510.01499), uses Bayesian-optimal aggregation with correlation awareness. Architecture changes require supermajority. Breaking API changes require unanimous.

The key learning: **multi-model consensus catches blind spots that any single model misses.** The disagreements are often more valuable than the agreements. I covered [the research and practical patterns behind consensus voting](/posts/consensus-voting-ai-models-multi-agent/) in a separate post.

## The Adaptive Feedback Loop

The routing system doesn't just pick models. It learns. Every task execution produces an outcome with quality signals. The `ArtifactStore` captures routing decisions, model output, and success metrics. A `computeQualityReward()` function feeds these outcomes back to the LinUCB bandit, adjusting future routing weights.

This is inspired by [Self-Refine](https://arxiv.org/abs/2303.17651) and [Reflexion](https://arxiv.org/abs/2303.11366), both of which showed that iterative feedback loops improve LLM output quality over time. I'm not sure yet how much the adaptive routing improves over static weights. Probably 10-15% based on early measurements, but I need more data before I'd commit to a number.

## The V2 Pipeline

Six months in, the original orchestration code was brittle. Task analysis, model routing, execution, and outcome tracking were all tangled together. I rebuilt the core as a plugin pipeline.

The V2 architecture has clear separation. **TaskContract** validates inputs. **PipelineRunner** executes plugin chains. **PluginRegistry** handles registration at startup. **PolicyEngine** enforces rules in three modes: `off`, `warn`, or `block`. **EventBus** decouples communication. **ArtifactStore** captures everything for debugging and the feedback loop.

This was the most expensive refactor I've done. 193 pipeline tests. 10 implementation phases. Weeks of work. I probably should have started with this architecture from day one, but I didn't know enough about the problem space yet. The system went from "scary to modify" to "boring to extend," which is exactly where infrastructure should be.

## Research Registry: 68 Papers and Counting

I track every paper that influences the architecture in a research registry. As of this writing, 68 arXiv papers across routing, consensus, memory, orchestration, code generation, and security. Before implementing any major feature, I create a research issue, survey the literature, and prototype against published baselines.

This seems like overhead. It probably is for most projects. But it caught me three times where my initial approach was worse than a published technique. The [SATER confidence-aware routing paper](https://arxiv.org/abs/2510.05164) replaced my hand-tuned confidence thresholds. The [TRINITY thinker/worker/verifier pattern](https://arxiv.org/abs/2512.04695) improved my agent orchestration structure. The [A-MEM agentic memory paper](https://arxiv.org/abs/2502.12110) solved a context persistence problem I'd been fighting for weeks.

## Graph Workflows

Not every task is a single model call. Complex tasks require multiple steps with dependencies: analyze the codebase, identify [security issues](/posts/vulnerability-management-scale-open-source/), draft fixes, validate they compile, then create a report.

Graph workflows model these as directed acyclic graphs. Each node is a task. Edges represent dependencies. The execution engine runs independent nodes in parallel and respects dependency ordering.

```typescript
const workflow = new GraphBuilder()
  .addNode('analyze', analyzeTask)
  .addNode('security', securityTask)
  .addNode('report', reportTask)
  .addEdge('analyze', 'report')
  .addEdge('security', 'report')
  .build();
```

Checkpointing saves progress after each node, so if the pipeline crashes mid-execution, it resumes from the last checkpoint instead of starting over. Seven built-in templates cover common patterns: code review, [security scanning](/posts/automated-security-scanning-pipeline/), architecture analysis, and more.

## What 22,000 Tests Taught Me

The test suite grew to 22,000+ tests across 811 files. Full suite runs in about two minutes. Here's what maintaining tests at that scale teaches you:

**Test isolation matters more than test count.** Early on, tests shared state through singletons and module-level caches. One test would set a config value, and 30 other tests would pass or fail depending on execution order. I spent more time debugging test interactions than actual bugs. The fix was aggressive: every test sets up its own state, every test tears it down.

**Export contract tests prevent API drift.** I have 51 tests that do nothing but verify public exports exist and have the right types. Boring tests. High value.

**Mock boundaries matter.** I mock at the adapter boundary. CLI adapters return fake responses, but everything above them runs real code. The tradeoff is slower tests, but the integration bugs caught are worth it.

## Security as Architecture

Nexus-agents processes untrusted input: GitHub issues, PR comments, user-provided tasks. I learned from [MCP safety research](https://arxiv.org/abs/2601.08012) and the [Agent-SafetyBench evaluation](https://arxiv.org/abs/2412.14470) that treating all external content as potentially hostile isn't paranoia. It's engineering.

**Trust tiers:** Every input gets classified into four tiers. Repo files are authoritative (Tier 1). Collaborator issue bodies are semi-trusted (Tier 2). Unknown user comments are untrusted (Tier 3). Content with injection patterns is hostile (Tier 4).

**Typed actions:** When processing untrusted input, agents can only emit predefined action types: `SummarizeIssue`, `ProposeLabels`, `DraftReply`, `RequestHumanApproval`, `RefuseAction`. No free-form tool calls. This prevents [prompt injection](/posts/securing-personal-ai-experiments/) from escalating into arbitrary actions.

**Rule of Two:** No agent may simultaneously process untrusted input, have write access to the repository, and access secrets. If all three are needed, the system requires human approval.

The hostile input firewall has 62 tests covering injection patterns I've encountered in the wild. It's one of the most valuable pieces of the system. Not because it's clever, but because it's paranoid in exactly the right ways.

## Lessons From 900+ Issues

**Dogfooding reveals real problems.** The most valuable bugs came from using nexus-agents to develop nexus-agents. MCP tool timeouts, routing edge cases, adapter failures. All found by eating my own cooking.

**Research issues prevent premature decisions.** Before implementing a feature, I create a research issue. What are the options? What do other systems do? What are the tradeoffs? This adds a week of lead time but prevents months of rework.

**Fitness audits enforce quality.** A custom `fitness-audit` command scores the codebase on 8 dimensions. Target: 90/100. Current: 98/100. Every push runs this check.

## What I'd Do Differently

**Start with the plugin pipeline.** The V1 monolithic code sort of worked, but refactoring it into V2 was painful. If I'd started with a pipeline architecture, six months of coupling headaches would have been avoided.

**Type the config from day one.** Nexus-agents uses [Zod](https://zod.dev) for config validation now, but the first three months used untyped YAML parsing. Every config-related bug in that period was a type error that Zod would have caught instantly.

**Invest in observability earlier.** The EventBus and ArtifactStore were late additions. They should have been foundational. Every orchestration system needs a way to answer "why did it make that decision?" from day one.

## Where It's Going

The AgentPlanner (code-named AOrchestra) is the newest component, drawing from [Pick and Spin efficient orchestration](https://arxiv.org/abs/2512.22402) and [TRINITY's thinker/worker/verifier pattern](https://arxiv.org/abs/2512.04695). It dynamically selects which expert roles to create based on task analysis. Instead of always spawning 5 agents, it picks the 2-3 that matter for a given task.

To be clear about what's production-tested versus experimental: the five-stage router, consensus voting, graph workflows, and security pipeline are all running daily. I use them to develop nexus-agents itself. AOrchestra and higher-order voting are newer, behind feature flags, and haven't seen enough traffic to measure their impact yet. The adaptive LinUCB routing is somewhere in between. It runs in production but I'm honestly not sure how much it improves over static weights. Maybe it plateaus quickly, maybe it keeps improving. Time will tell.

The [codebase is open source](https://github.com/williamzujkowski/nexus-agents). If you're interested in multi-model orchestration, want to see how consensus voting works in practice, or need a reference implementation for [MCP server development](/posts/building-mcp-standards-server/), take a look.

Building this taught me that the future of AI-assisted development isn't about picking the best model. It's about building systems that use the right model for each piece of the problem. And backing those systems with real research, not vibes.
