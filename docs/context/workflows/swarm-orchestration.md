---
title: Swarm Orchestration Workflow
category: workflows
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 2500
load_when:
  - Multi-agent coordination
  - Complex task decomposition
  - Parallel execution needed
dependencies:
  - core/enforcement
  - core/file-management
tags: [swarm, agents, coordination, parallel]
---

# Swarm Orchestration Workflow

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM
**Load When:** Multi-agent coordination, complex task decomposition, parallel execution
**Dependencies:** core/enforcement, core/file-management
**Estimated Size:** ~2,500 tokens

---

## Purpose

This module documents multi-agent swarm orchestration patterns using Claude-Flow for complex task coordination and parallel execution.

---

## When to Load This Module

**Load this module when:**
- Coordinating multiple AI agents
- Complex tasks requiring decomposition
- Parallel execution for speed (2.8-4.4x faster)
- Multi-step workflows with dependencies

**Skip this module if:**
- Single-agent tasks
- Simple sequential operations
- No parallelization needed

---

## Quick Reference

**54 Available Agents:**
- Core: `coder`, `reviewer`, `tester`, `planner`, `researcher`
- Swarm: `hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`
- GitHub: `pr-manager`, `code-review-swarm`, `issue-tracker`

**Agent Coordination Protocol:**
1. **BEFORE Work:** `pre-task`, `session-restore`
2. **DURING Work:** `post-edit`, `notify`
3. **AFTER Work:** `post-task`, `session-end`

**The One-Message Rule:** All related operations in one message for 2.8-4.4x speedup.

---

## 🚀 Available Agents (54 Total)

### Core Development
`coder`, `reviewer`, `tester`, `planner`, `researcher`

### Swarm Coordination
`hierarchical-coordinator`, `mesh-coordinator`, `adaptive-coordinator`, `collective-intelligence-coordinator`, `swarm-memory-manager`

### Consensus & Distributed
`byzantine-coordinator`, `raft-manager`, `gossip-coordinator`, `consensus-builder`, `crdt-synchronizer`, `quorum-manager`, `security-manager`

### Performance & Optimization
`perf-analyzer`, `performance-benchmarker`, `task-orchestrator`, `memory-coordinator`, `smart-agent`

### GitHub & Repository
`github-modes`, `pr-manager`, `code-review-swarm`, `issue-tracker`, `release-manager`, `workflow-automation`, `project-board-sync`, `repo-architect`, `multi-repo-swarm`

### SPARC Methodology
`sparc-coord`, `sparc-coder`, `specification`, `pseudocode`, `architecture`, `refinement`

### Specialized Development
`backend-dev`, `mobile-dev`, `ml-developer`, `cicd-engineer`, `api-docs`, `system-architect`, `code-analyzer`, `base-template-generator`

### Testing & Validation
`tdd-london-swarm`, `production-validator`

### Migration & Planning
`migration-planner`, `swarm-init`

---

## 🎯 Claude Code vs MCP Tools

### Claude Code Handles ALL:
- File operations (Read, Write, Edit, MultiEdit, Glob, Grep)
- Code generation and programming
- Bash commands and system operations
- Implementation work
- Project navigation and analysis
- TodoWrite and task management
- Git operations
- Package management
- Testing and debugging

### MCP Tools ONLY:
- Coordination and planning
- Memory management
- Neural features
- Performance tracking
- Swarm orchestration
- GitHub integration

**KEY**: MCP coordinates, Claude Code executes.

---

## 🚀 Quick Setup

```bash
# Add Claude Flow MCP server
claude mcp add claude-flow npx claude-flow@alpha mcp start
```

---

## MCP Tool Categories

### Coordination
`swarm_init`, `agent_spawn`, `task_orchestrate`

### Monitoring
`swarm_status`, `agent_list`, `agent_metrics`, `task_status`, `task_results`

### Memory & Neural
`memory_usage`, `neural_status`, `neural_train`, `neural_patterns`

### GitHub Integration
`github_swarm`, `repo_analyze`, `pr_enhance`, `issue_triage`, `code_review`

### System
`benchmark_run`, `features_detect`, `swarm_monitor`

---

## 📋 Agent Coordination Protocol

### Every Agent MUST:

**1️⃣ BEFORE Work:**
```bash
npx claude-flow@alpha hooks pre-task --description "[task]"
npx claude-flow@alpha hooks session-restore --session-id "swarm-[id]"
```

**2️⃣ DURING Work:**
```bash
npx claude-flow@alpha hooks post-edit --file "[file]" --memory-key "swarm/[agent]/[step]"
npx claude-flow@alpha hooks notify --message "[what was done]"
```

**3️⃣ AFTER Work:**
```bash
npx claude-flow@alpha hooks post-task --task-id "[task]"
npx claude-flow@alpha hooks session-end --export-metrics true
```

---

## 🎯 Concurrent Execution Examples

### The One-Message Rule

**All related operations in one message for 2.8-4.4x speedup.**

**Swarm-specific applications:**
- Spawn multiple agents in parallel (not sequentially)
- Batch memory operations across agents
- Coordinate hooks (pre-task, post-edit, post-task) in one message

See [file-management.md](../core/file-management.md#concurrent-execution-examples) for complete examples and patterns.

---

## Performance Benefits

- **84.8% SWE-Bench solve rate**
- **32.3% token reduction**
- **2.8-4.4x speed improvement**
- **27+ neural models**

---

## Hooks Integration

### Pre-Operation
- Auto-assign agents by file type
- Validate commands for safety
- Prepare resources automatically
- Optimize topology by complexity
- Cache searches

### Post-Operation
- Auto-format code
- Train neural patterns
- Update memory
- Analyze performance
- Track token usage

### Session Management
- Generate summaries
- Persist state
- Track metrics
- Restore context
- Export workflows

---

## Advanced Features (v2.0.0)

- 🚀 Automatic Topology Selection
- ⚡ Parallel Execution (2.8-4.4x speed)
- 🧠 Neural Training
- 📊 Bottleneck Analysis
- 🤖 Smart Auto-Spawning
- 🛡️ Self-Healing Workflows
- 💾 Cross-Session Memory
- 🔗 GitHub Integration

---

## Cross-References

### Related Modules
- [enforcement.md](../core/enforcement.md) - Mandatory rules
- [file-management.md](../core/file-management.md) - Concurrent execution patterns
- [sparc-development.md](./sparc-development.md) - SPARC methodology integration

### External References
- [Claude-Flow Documentation](https://github.com/ruvnet/claude-flow)
- [Claude-Flow Issues](https://github.com/ruvnet/claude-flow/issues)

---

## Examples

### Example 1: Multi-Agent Blog Post Refinement

```javascript
// Spawn 3 agents in parallel
Task("Planner", "Create pre-analysis for post")
Task("Researcher", "Find 12 academic citations")
Task("Coder", "Execute BLUF and bulletization")

// Wait for completion
// Validate results
// Commit changes

// Result: 3x faster than sequential
```

**Explanation:** Swarm orchestration parallelizes independent tasks.

### Example 2: Agent Coordination Hooks

```bash
# Before starting work
npx claude-flow@alpha hooks pre-task --description "Refine blog post"

# During work
npx claude-flow@alpha hooks post-edit --file "src/posts/example.md" --memory-key "swarm/coder/bluf"

# After completion
npx claude-flow@alpha hooks post-task --task-id "blog-refine-1"
```

**Explanation:** Hooks enable tracking, memory persistence, and coordination.

---

## Common Pitfalls

### Pitfall 1: Sequential Execution
**Problem:** Running operations one-by-one in separate messages
**Solution:** Batch all independent operations in single message
**Prevention:** Follow "One-Message Rule" pattern

### Pitfall 2: Not Using Hooks
**Problem:** Agents don't coordinate, lose context between sessions
**Solution:** Use pre-task, post-edit, post-task hooks consistently
**Prevention:** Add hooks to agent instructions

### Pitfall 3: Wrong Tool for Job
**Problem:** Using MCP for file operations, Claude Code for coordination
**Solution:** Claude Code = execution, MCP = coordination
**Prevention:** Review "Claude Code vs MCP Tools" section

---

## Validation

### How to Verify Correct Application

**Checklist:**
- [ ] All related operations in one message (One-Message Rule)
- [ ] Agent hooks used (pre-task, post-edit, post-task)
- [ ] Claude Code used for file operations (not MCP)
- [ ] MCP used for coordination (not Claude Code)
- [ ] Performance improvement measured (2.8-4.4x faster)

**Commands:**
```bash
# Check swarm status
npx claude-flow@alpha swarm-status

# View agent metrics
npx claude-flow@alpha agent-metrics

# Monitor performance
npx claude-flow@alpha benchmark-run
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md sections:
  - "Available Agents (54 Total)"
  - "Agent Coordination Protocol"
  - "Concurrent Execution Examples"
  - "Performance Benefits"
  - "Hooks Integration"
- Complete agent catalog
- Examples and validation added

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Orchestration Team

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
