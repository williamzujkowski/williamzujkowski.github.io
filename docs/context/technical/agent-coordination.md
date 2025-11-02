---
title: Agent Coordination & SPARC Integration
category: technical
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1800
load_when:
  - Using SPARC agents
  - Multi-agent coordination
  - Hook integration
dependencies:
  - workflows/sparc-development
  - workflows/swarm-orchestration
tags: [agents, sparc, coordination, hooks]
---

# Agent Coordination & SPARC Integration

This document catalogs available agents, coordination protocols, and Claude-Flow integration patterns.

## Available Agents (54 Total)

### Core Development (5 agents)

`coder`, `reviewer`, `tester`, `planner`, `researcher`

**Use for**: Standard development tasks, code review, testing, planning.

### Swarm Coordination (5 agents)

`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`, `collective-intelligence-coordinator`, `swarm-memory-manager`

**Use for**: Managing multi-agent swarms, coordinating parallel work.

### Consensus & Distributed (7 agents)

`byzantine-coordinator`, `raft-manager`, `gossip-coordinator`, `consensus-builder`, `crdt-synchronizer`, `quorum-manager`, `security-manager`

**Use for**: Distributed decision-making, consensus protocols.

### Performance & Optimization (5 agents)

`perf-analyzer`, `performance-benchmarker`, `task-orchestrator`, `memory-coordinator`, `smart-agent`

**Use for**: Performance analysis, optimization, benchmarking.

### GitHub & Repository (9 agents)

`github-modes`, `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`, `workflow-automation`, `project-board-sync`, `repo-architect`, `multi-repo-swarm`

**Use for**: GitHub operations, PR management, issue tracking.

### SPARC Methodology (6 agents)

`sparc-coord`, `sparc-coder`, `specification`, `pseudocode`, `architecture`, `refinement`

**Use for**: SPARC development workflow, TDD implementation.

### Specialized Development (8 agents)

`backend-dev`, `mobile-dev`, `ml-developer`, `cicd-engineer`, `api-docs`, `system-architect`, `code-analyzer`, `base-template-generator`

**Use for**: Domain-specific development tasks.

### Testing & Validation (2 agents)

`tdd-london-swarm`, `production-validator`

**Use for**: Test-driven development, production validation.

### Migration & Planning (2 agents)

`migration-planner`, `swarm-init`

**Use for**: System migrations, swarm initialization.

## Claude Code vs MCP Tools

### Claude Code Handles ALL Implementation

**Claude Code is responsible for:**
- File operations (Read, Write, Edit, Glob, Grep)
- Code generation and programming
- Bash commands and system operations
- Implementation work
- Project navigation and analysis
- TodoWrite and task management
- Git operations
- Package management
- Testing and debugging

**Why**: Claude Code has direct file system access and can execute operations immediately.

### MCP Tools for Coordination ONLY

**MCP tools are used for:**
- Coordination and planning
- Memory management
- Neural features
- Performance tracking
- Swarm orchestration
- GitHub integration (when using gh CLI is insufficient)

**KEY PRINCIPLE**: MCP coordinates, Claude Code executes.

## Agent Coordination Protocol

### Every Agent MUST Follow

**1️⃣ BEFORE Work:**
```bash
npx claude-flow@alpha hooks pre-task --description "[task description]"
npx claude-flow@alpha hooks session-restore --session-id "swarm-[id]"
```

**Purpose**: Prepare resources, restore context, auto-assign agent.

**2️⃣ DURING Work:**
```bash
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "swarm/[agent]/[step]"
npx claude-flow@alpha hooks notify --message "[what was done]"
```

**Purpose**: Track progress, update memory, coordinate with other agents.

**3️⃣ AFTER Work:**
```bash
npx claude-flow@alpha hooks post-task --task-id "[task]"
npx claude-flow@alpha hooks session-end --export-metrics true
```

**Purpose**: Generate summaries, export metrics, persist state.

## Concurrent Execution

**Agent coordination follows the "One-Message Rule":** All related operations in one message for 2.8-4.4x speedup.

See [file-management.md](../core/file-management.md#concurrent-execution--file-management) for complete concurrent execution patterns and examples.

## MCP Tool Categories

### Coordination
`swarm_init`, `agent_spawn`, `task_orchestrate`

**Use when**: Initializing swarms, spawning specialized agents, orchestrating complex workflows.

### Monitoring
`swarm_status`, `agent_list`, `agent_metrics`, `task_status`, `task_results`

**Use when**: Checking swarm health, monitoring progress, analyzing performance.

### Memory & Neural
`memory_usage`, `neural_status`, `neural_train`, `neural_patterns`

**Use when**: Storing/retrieving persistent memory, training patterns, cognitive analysis.

### GitHub Integration
`github_swarm`, `repo_analyze`, `pr_enhance`, `issue_triage`, `code_review`

**Use when**: Complex GitHub operations beyond `gh` CLI capabilities.

### System
`benchmark_run`, `features_detect`, `swarm_monitor`

**Use when**: Performance benchmarking, feature detection, real-time monitoring.

## Quick Setup

### Add Claude Flow MCP Server

```bash
# Add MCP server to Claude configuration
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

**Verify installation:**
```bash
# Check MCP server is running
npx claude-flow@alpha status
```

## Hooks Integration

### Pre-Operation Hooks

**Auto-executed before operations:**
- Auto-assign agents by file type
- Validate commands for safety
- Prepare resources automatically
- Optimize topology by complexity
- Cache searches

**Example**:
```bash
# Before editing Python file
npx claude-flow@alpha hooks pre-edit --file "script.py"
# → Auto-assigns python-specialist agent
```

### Post-Operation Hooks

**Auto-executed after operations:**
- Auto-format code
- Train neural patterns
- Update memory
- Analyze performance
- Track token usage

**Example**:
```bash
# After editing file
npx claude-flow@alpha hooks post-edit --file "script.py"
# → Formats code, updates memory, analyzes changes
```

### Session Management Hooks

**Session lifecycle:**
- Generate summaries
- Persist state
- Track metrics
- Restore context
- Export workflows

**Example**:
```bash
# End session with metrics
npx claude-flow@alpha hooks session-end --export-metrics true
# → Generates completion report, exports workflow
```

## Advanced Features (v2.0.0)

### 🚀 Automatic Topology Selection

Claude-Flow analyzes task complexity and selects optimal swarm topology:
- **Hierarchical**: Complex tasks with clear delegation
- **Mesh**: High interdependence, peer coordination
- **Ring**: Sequential processing pipelines
- **Star**: Centralized coordination with specialists

### ⚡ Parallel Execution

**Performance gains:**
- 2.8-4.4x speed improvement
- 32.3% token reduction
- 84.8% SWE-Bench solve rate

**How it works**: Agents execute independent tasks concurrently using multiprocessing.

### 🧠 Neural Training

**Capabilities:**
- Pattern recognition from successful workflows
- Adaptive learning from failures
- Predictive task optimization
- Cognitive behavior analysis

**Models**: 27+ pre-trained neural models for common patterns.

### 📊 Bottleneck Analysis

**Automatic detection:**
- Identify slow operations
- Find inefficient patterns
- Suggest optimizations
- Track performance trends

### 🤖 Smart Auto-Spawning

**Intelligent agent creation:**
- Analyze task requirements
- Auto-spawn appropriate agents
- Match capabilities to needs
- Optimize resource allocation

### 🛡️ Self-Healing Workflows

**Automatic recovery:**
- Detect failures
- Retry with backoff
- Reroute tasks
- Preserve state

### 💾 Cross-Session Memory

**Persistent context:**
- Store workflow state
- Resume interrupted tasks
- Share knowledge across sessions
- Build organizational memory

### 🔗 GitHub Integration

**Native GitHub support:**
- PR creation and management
- Issue triage and assignment
- Code review automation
- Release coordination

## Performance Benefits

**Measured improvements:**
- **84.8% SWE-Bench solve rate** (vs 45% baseline)
- **32.3% token reduction** (batching operations)
- **2.8-4.4x speed improvement** (parallel execution)
- **27+ neural models** (pattern recognition)

## Integration Tips

### Starting with Claude-Flow

1. **Start simple**: Begin with basic swarm init
2. **Scale gradually**: Add agents as needed
3. **Use memory**: Store context for efficiency
4. **Monitor progress**: Check swarm status regularly
5. **Train patterns**: Learn from successful workflows
6. **Enable hooks**: Automate coordination
7. **GitHub first**: Use GitHub tools for repo operations

### Common Patterns

**Blog post enhancement:**
```bash
# 1. Init swarm
npx claude-flow@alpha swarm init --topology hierarchical

# 2. Spawn agents
npx claude-flow@alpha agent spawn --type planner
npx claude-flow@alpha agent spawn --type researcher
npx claude-flow@alpha agent spawn --type coder

# 3. Orchestrate task
npx claude-flow@alpha task orchestrate --task "enhance blog posts batch 2" --strategy parallel
```

**Code review:**
```bash
# Use GitHub integration
npx claude-flow@alpha github swarm --task "review PR #123" --agents code-review-swarm
```

## Troubleshooting

### Agent Not Responding

**Check swarm status:**
```bash
npx claude-flow@alpha swarm status --swarm-id [id]
npx claude-flow@alpha agent metrics --agent-id [id]
```

### Memory Issues

**Check memory usage:**
```bash
npx claude-flow@alpha memory usage --namespace "swarm/[id]"
```

### Performance Degradation

**Run bottleneck analysis:**
```bash
npx claude-flow@alpha bottleneck analyze --component swarm
```

## Related Documentation

- **SPARC Methodology**: `docs/context/workflows/sparc-development.md`
- **Swarm Orchestration**: `docs/context/workflows/swarm-orchestration.md`
- **Claude-Flow GitHub**: https://github.com/ruvnet/claude-flow
- **Claude-Flow Issues**: https://github.com/ruvnet/claude-flow/issues
