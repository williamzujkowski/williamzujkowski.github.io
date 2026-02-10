---
title: "Building Nexus-Agents: What I Learned Creating a Multi-Model AI Orchestration System"
date: "2026-02-09"
lastUpdate: "2026-02-09"
description: "The engineering story behind nexus-agents, a multi-model orchestration system that coordinates Claude, Gemini, and Codex through consensus voting, adaptive routing, and graph workflows. Lessons from 900+ GitHub issues and 22,000 tests."
author: "William Zujkowski"
tags: [ai, software-engineering, open-source, orchestration, typescript]
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=630"
imageAlt: "Abstract visualization of interconnected neural network nodes"
readingTime: "12-14 min read"
---

I started nexus-agents because I kept running into the same problem: different AI models are good at different things, and switching between them manually is tedious. Claude writes better architecture docs. Gemini handles broad research faster. Codex is solid for focused code generation. I wanted one system that could route tasks to the right model automatically.

What began as a weekend routing script turned into a multi-model orchestration platform with consensus voting, graph workflows, a plugin pipeline, and a full TUI. I tested dozens of approaches before landing on the architecture that stuck. Here's what I found along the way.

## The Problem With Single-Model Workflows

Most AI-assisted development workflows look like this: you pick one model, send it everything, and hope for the best. The model might be great at code generation but mediocre at security analysis. Or excellent at research but slow at producing clean TypeScript.

I was spending time not writing software but context-switching between AI tools. Open Claude for architecture planning. Switch to Gemini for broad research. Use Codex for rapid code generation. Copy context between them. Lose track of which model said what.

**The core insight:** Model selection is a routing problem, not a loyalty problem. Different tasks have measurably different performance across models. A system that routes intelligently should outperform any single model used for everything.

## Architecture Decisions That Shaped Everything

### The MCP Foundation

I built nexus-agents as an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server. MCP is Anthropic's open protocol for connecting AI models to external tools and data sources. This was the single most important architecture decision.

MCP gave me a standard interface that any compatible client could use. Claude Code, Cursor, Windsurf. Any MCP client gets access to the full orchestration system without custom integration work.

The server exposes 20 tools through MCP: task orchestration, expert agent creation, consensus voting, workflow execution, research tracking, and more. Each tool is a self-contained capability that clients can compose.

### CLI Adapter Pattern

Each AI model has quirks. Claude uses XML-style tool calls. Gemini has different token limits. Codex has its own API patterns. I needed an abstraction layer.

The CLI adapter pattern wraps each model behind a common interface:

```typescript
interface CliAdapter {
  readonly cliName: string;
  executeTask(task: TaskConstraint): Promise<TaskOutcome>;
  isAvailable(): Promise<boolean>;
}
```

Every model interaction flows through this interface. The adapter handles model-specific serialization, token counting, error recovery, and timeout management. When a new model comes out, I write one adapter file. Everything else stays untouched.

The `ResilientAdapter` wrapper adds circuit breaker patterns. If a model fails three times in a row, the system stops trying it for a cooldown period and routes to alternatives. This prevents cascading failures when an API goes down.

### Composite Router: Five-Stage Model Selection

Picking the right model for a task isn't simple. I built a five-stage routing pipeline:

**Stage 1, Budget Router:** If the billing mode is `plan` (monthly subscription), cost drops out of the equation entirely. Strongest models win. If billing is `api` (pay-per-token), cost factors into scoring.

**Stage 2, Zero Router:** Eliminates models that can't handle the task at all. If a task needs 100K context and a model maxes at 32K, it's out.

**Stage 3, Preference Router:** User preferences and task hints influence scoring. If you ask for a "security review," models with higher security quality scores get a boost.

**Stage 4, TOPSIS Router:** Multi-criteria decision analysis. Balances quality scores, context window fit, speed, and cost using the TOPSIS algorithm. This produces a ranked list of candidates.

**Stage 5, LinUCB Bandit:** The adaptive layer. LinUCB is a contextual bandit algorithm that learns from outcomes. When a model succeeds at a task type, it gets a higher score next time. When it fails, the score drops. Over time, the system converges on optimal routing without manual tuning.

The entire pipeline runs in under 10ms. The routing decision is nearly free compared to the actual model inference.

## Consensus Voting: When One Opinion Isn't Enough

Some decisions are too important for a single model. Architecture changes, security modifications, breaking API changes. These deserve multiple perspectives.

Nexus-agents implements multi-model consensus voting. For a given proposal, the system creates specialized agent roles (architect, security engineer, DevEx advocate, PM, and a deliberately contrarian "catfish" agent), assigns them across available models round-robin, and collects votes with reasoning.

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

The catfish role is intentionally adversarial. Its job is to find problems the others missed. It doesn't always change the outcome, but it consistently surfaces edge cases.

Three voting thresholds exist: majority (>50%), supermajority (>66%), and unanimous. Architecture changes require supermajority. Breaking API changes require unanimous. Sprint planning uses simple majority.

The key learning: **multi-model consensus catches blind spots that any single model misses.** Each model has different training data biases and reasoning patterns. The disagreements are often more valuable than the agreements.

## The V2 Pipeline

Six months in, the original orchestration code was getting brittle. Task analysis, model routing, execution, and outcome tracking were all tangled together. I rebuilt the core as a plugin pipeline.

The V2 architecture has clear separation:

**TaskContract** validates that every task has the required fields before it enters the pipeline. No more half-formed tasks causing mysterious failures downstream.

**PipelineRunner** executes a chain of plugins in order. Each plugin can transform the task, add metadata, or halt execution with a policy violation.

**PluginRegistry** handles plugin registration at startup. Core plugins handle task analysis, model routing, and CLI execution. Custom plugins can add logging, metrics, or domain-specific logic.

**PolicyEngine** enforces rules. "Tasks requesting more than 100K tokens must use a model with sufficient context." "Security-tagged tasks must route to models with security quality score above 7." Policies run in three modes: `off`, `warn`, or `block`.

**EventBus** lets plugins communicate through events, not direct calls. This eliminated the coupling that made V1 fragile. When the model router selects a model, it emits an event. The outcome tracker listens for completion events. Nothing calls anything directly.

**ArtifactStore** captures every pipeline execution produces artifacts: the original task, routing decisions, model output, quality signals. Artifacts enable debugging, auditing, and the feedback loop that trains LinUCB.

This was the most expensive refactor I've done. It took 193 pipeline tests, 10 implementation phases, weeks of work. But the system went from "scary to modify" to "boring to extend," which is exactly where infrastructure should be.

## Graph Workflows

Not every task is a single model call. Complex tasks require multiple steps with dependencies: analyze the codebase, identify security issues, draft fixes, validate the fixes compile, then create a report.

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

The `analyze` and `security` nodes run in parallel. The `report` node waits for both to complete. Checkpointing saves progress after each node, so if the pipeline crashes mid-execution, it resumes from the last checkpoint instead of starting over.

Seven built-in workflow templates cover common patterns: code review, security scanning, architecture analysis, and more. Custom workflows can be defined in YAML or built programmatically.

## What 22,000 Tests Taught Me

The test suite grew organically to 22,000+ tests across 811 files. Running the full suite takes about two minutes. Here's what maintaining a test suite at that scale teaches you:

**Test isolation matters more than test count.** Early on, tests shared state through singletons and module-level caches. One test would set a config value, and 30 other tests would pass or fail depending on execution order. I spent more time debugging test interactions than actual bugs.

The fix was aggressive: every test sets up its own state, every test tears it down. No shared mutable state between tests. This added boilerplate but eliminated an entire class of debugging nightmares.

**Vitest's parallel execution is essential.** The suite runs across multiple workers. Tests that accidentally depend on execution order fail immediately in CI even if they pass locally. This catches isolation bugs before they reach main.

**Export contract tests prevent API drift.** I have 51 tests that do nothing but verify that public exports exist and have the right types. When someone renames or removes an export, these tests catch it before consumers break. Boring tests, high value.

**Mock boundaries matter.** I mock at the adapter boundary,the CLI adapters return fake responses, but everything above them runs real code. This catches integration issues that pure unit tests miss. The tradeoff is slower tests, but the bugs caught are worth it.

## Security as Architecture

Nexus-agents processes untrusted input: GitHub issues, PR comments, user-provided tasks. The security model treats all external content as potentially hostile.

**Trust tiers:** Every input gets classified into one of four tiers. Repo files and CI results are authoritative (Tier 1). Collaborator issue bodies are semi-trusted (Tier 2). Unknown user comments are untrusted (Tier 3). Content with injection patterns is hostile (Tier 4).

**Typed actions:** When processing untrusted input, agents can only emit predefined action types: `SummarizeIssue`, `ProposeLabels`, `DraftReply`, `ClassifyIssue`, `RequestHumanApproval`, `RefuseAction`. No free-form tool calls. This prevents prompt injection from escalating into arbitrary actions.

**Input sanitization:** Before any LLM processes external content, a sanitizer strips HTML tags that could carry injection payloads (`<picture>`, `<source>`, `<img>`), XML-like tags that mimic system prompts, and Base64-encoded blocks.

**Rule of Two:** No agent may simultaneously process untrusted input, have write access to the repository, and access secrets. If all three are needed, the system requires human approval. This limits the blast radius of any compromise.

The hostile input firewall has 62 tests covering injection patterns I've encountered in the wild. It's one of the most valuable pieces of the system. Not because it's clever, but because it's paranoid in exactly the right ways.

## The TUI Nobody Asked For (But I Needed)

Watching orchestration happen through log files is miserable. I built a terminal UI using Ink (React for the terminal) with four panels: active agents, weather report (model performance metrics), current task, and outcome history.

The TUI shows which models are being used, their success rates, routing decisions, and vote outcomes in real-time. It turned orchestration from an opaque process into something observable.

Building a TUI taught me that React's component model works surprisingly well for terminal interfaces. State management with a reducer pattern, keyboard shortcuts for navigation, and an event bus for live updates. It's basically a React app that renders to ANSI escape codes.

The TUI is optional. The system works fine through MCP or CLI without it. But when debugging routing decisions or watching a consensus vote happen in real-time, the visual feedback is invaluable.

## Lessons From 900+ Issues

The GitHub issue tracker hit 900+ issues. Some patterns emerged:

**Dogfooding reveals real problems.** The most valuable bugs came from using nexus-agents to develop nexus-agents. The MCP tool timeout issues, the routing edge cases, the adapter failures. All found by eating my own cooking.

**Epics keep scope manageable.** Major features get an epic issue with sub-issues for each phase. The V2 pipeline was 10 phases. The security hardening was 8 modules. Breaking work into phases with clear acceptance criteria prevents scope creep and makes progress visible.

**Research issues prevent premature decisions.** Before implementing a feature, I create a research issue. What are the options? What do other systems do? What are the tradeoffs? This adds a week of lead time but prevents months of rework.

**Fitness audits enforce quality.** A custom `fitness-audit` command scores the codebase on 8 dimensions: canonical paths, explicit behavior, determinism, observability, config simplicity, layer separation, operator ergonomics, and governance integration. The target is 90/100. Current score: 98/100. Every push runs this check.

## What I'd Do Differently

**Start with the plugin pipeline.** The V1 monolithic orchestration code worked, but refactoring it into V2 was painful. If I'd started with a pipeline architecture, six months of coupling headaches would have been avoided.

**Fewer adapter abstractions, more direct integration.** The adapter pattern is clean but adds overhead. For the three CLIs I actually support, direct integration might have been simpler. The abstraction layer paid off when adding the third adapter, but the first two didn't need it.

**Type the config from day one.** Nexus-agents uses Zod for config validation now, but the first three months used untyped YAML parsing. Every config-related bug in that period was a type error that Zod would have caught instantly.

**Invest in observability earlier.** The EventBus and ArtifactStore were late additions. They should have been foundational. Every orchestration system needs a way to answer "why did it make that decision?" from day one.

## Where It's Going

Nexus-agents is at a point where the infrastructure is solid and the interesting work is in the intelligence layer. The AgentPlanner (code-named AOrchestra) dynamically selects which expert roles to create based on task analysis. Instead of always spawning 5 agents, it picks the 2-3 that matter for a given task.

The adaptive routing via LinUCB is still learning. With more outcome data, routing accuracy should improve without manual tuning. The goal is a system where you describe what you want, and the orchestration layer handles model selection, expert composition, and quality validation automatically.

The codebase is open source. If you're interested in multi-model orchestration, want to see how consensus voting works in practice, or need a reference implementation for MCP server development, take a look at the [repository](https://github.com/williamzujkowski/nexus-agents).

Building this taught me that the future of AI-assisted development isn't about picking the best model. It's about building systems that use the right model for each piece of the problem. The orchestration layer is where the real advantage is.
