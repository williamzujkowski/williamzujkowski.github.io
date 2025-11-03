# Swarm Agent Validation Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-03
**Purpose:** Prevent agent type hallucinations in swarm orchestration

---

## 🚨 Problem Statement

Swarm initialization prompts often reference agent types that **don't exist** in the available agent catalog, leading to:

- Failed agent spawning
- Wasted tokens on invalid operations
- Confusion about available capabilities
- Inconsistent swarm deployments

**Example from Session 9 Analysis:**
```yaml
# ❌ WRONG: These agents DON'T exist
worker_types:
  - analyst        # Not in catalog
  - optimizer      # Not in catalog
  - documenter     # Not in catalog
```

---

## ✅ Available Agents (54 Total)

**Always verify against:** `docs/context/technical/agent-coordination.md`

### Core Development (5 agents)
- `coder` ✅
- `reviewer` ✅
- `tester` ✅
- `planner` ✅
- `researcher` ✅

### Swarm Coordination (5 agents)
- `hierarchical-coordinator` ✅
- `mesh-coordinator` ✅
- `adaptive-coordinator` ✅
- `collective-intelligence-coordinator` ✅
- `swarm-memory-manager` ✅

### Consensus & Distributed (7 agents)
- `byzantine-coordinator` ✅
- `raft-manager` ✅
- `gossip-coordinator` ✅
- `consensus-builder` ✅
- `crdt-synchronizer` ✅
- `quorum-manager` ✅
- `security-manager` ✅

### Performance & Optimization (5 agents)
- `perf-analyzer` ✅
- `performance-benchmarker` ✅
- `task-orchestrator` ✅
- `memory-coordinator` ✅
- `smart-agent` ✅

### GitHub & Repository (9 agents)
- `github-modes` ✅
- `pr-manager` ✅
- `code-review-swarm` ✅
- `issue-tracker` ✅
- `release-manager` ✅
- `workflow-automation` ✅
- `project-board-sync` ✅
- `repo-architect` ✅
- `multi-repo-swarm` ✅

### SPARC Methodology (6 agents)
- `sparc-coord` ✅
- `sparc-coder` ✅
- `specification` ✅
- `pseudocode` ✅
- `architecture` ✅
- `refinement` ✅

### Specialized Development (8 agents)
- `backend-dev` ✅
- `mobile-dev` ✅
- `ml-developer` ✅
- `cicd-engineer` ✅
- `api-docs` ✅
- `system-architect` ✅
- `code-analyzer` ✅
- `base-template-generator` ✅

### Testing & Validation (2 agents)
- `tdd-london-swarm` ✅
- `production-validator` ✅

### Migration & Planning (2 agents)
- `migration-planner` ✅
- `swarm-init` ✅

---

## 🔄 Agent Type Substitutions

Use this table when swarm prompts reference non-existent agents:

| ❌ Hallucinated | ✅ Use Instead | Reason |
|-----------------|----------------|--------|
| `analyst` | `perf-analyzer` | Performance analysis |
| `optimizer` | `refinement` | Code optimization |
| `documenter` | `coder` (with doc focus) | No dedicated doc agent |
| `writer` | `coder` | Content generation |
| `qa` | `tester` | Quality assurance |
| `architect` | `system-architect` | System design (exists, but be specific) |

---

## 🛠️ Pre-Swarm Validation Checklist

Before initializing any swarm:

1. ✅ **Load agent catalog:**
   ```bash
   # Read agent coordination module
   Read("docs/context/technical/agent-coordination.md")
   ```

2. ✅ **Validate agent types:**
   ```bash
   # Verify each agent type exists in 54 available agents
   # Match exact naming (case-sensitive)
   ```

3. ✅ **Check for common hallucinations:**
   - `analyst` → Use `perf-analyzer`
   - `optimizer` → Use `refinement` or `code-analyzer`
   - `documenter` → Use `coder` with documentation focus

4. ✅ **Document swarm composition:**
   ```yaml
   # Example valid swarm
   agents:
     - type: researcher
       count: 1
     - type: coder
       count: 2
     - type: tester
       count: 1
     - type: reviewer
       count: 1
   ```

---

## 📊 Validation Pattern

**Always use this pattern in swarm initialization:**

```bash
# 1. Load agent catalog first
Read("docs/context/technical/agent-coordination.md")

# 2. Validate proposed agents against catalog
proposed_agents = [researcher, coder, tester, analyst]  # ❌ analyst invalid
valid_agents = [researcher, coder, tester, perf-analyzer]  # ✅ corrected

# 3. Initialize swarm with ONLY valid agents
Task("Researcher", "...", "researcher")  # ✅
Task("Coder", "...", "coder")            # ✅
Task("Tester", "...", "tester")          # ✅
Task("Analyzer", "...", "perf-analyzer") # ✅ (not analyst)
```

---

## 🎯 Best Practices

### DO ✅
- **Always load** `docs/context/technical/agent-coordination.md` before swarm init
- **Verify** each agent type against the 54 available agents
- **Use exact names** (case-sensitive: `perf-analyzer` not `perfAnalyzer`)
- **Document** agent composition in swarm planning

### DON'T ❌
- **Don't assume** agent types exist without verification
- **Don't use** generic names like "analyst", "optimizer", "documenter"
- **Don't hallucinate** agents based on task descriptions
- **Don't skip** agent validation step

---

## 🔍 Common Mistakes

### Mistake 1: Generic Agent Names
```yaml
# ❌ WRONG
agents:
  - analyst        # Doesn't exist
  - optimizer      # Doesn't exist
  - documenter     # Doesn't exist

# ✅ CORRECT
agents:
  - perf-analyzer  # Performance analysis
  - refinement     # Code optimization
  - coder          # Documentation (with focus)
```

### Mistake 2: Skipping Validation
```bash
# ❌ WRONG: No validation
Task("Analyst", "Analyze data", "analyst")  # Will fail

# ✅ CORRECT: Validate first
Read("docs/context/technical/agent-coordination.md")  # Load catalog
Task("Analyzer", "Analyze data", "perf-analyzer")     # Use valid agent
```

### Mistake 3: Assuming Agents Exist
```bash
# ❌ WRONG: Assumes "qa-specialist" exists
Task("QA Specialist", "Test code", "qa-specialist")

# ✅ CORRECT: Use validated agent
Task("Tester", "Test code", "tester")  # From catalog
```

---

## 📝 Related Documentation

- **Agent Catalog:** `docs/context/technical/agent-coordination.md`
- **Swarm Orchestration:** `docs/context/workflows/swarm-orchestration.md`
- **SPARC Methodology:** `docs/context/workflows/sparc-development.md`

---

## 🎉 Success Criteria

A valid swarm initialization:
- ✅ All agent types verified against catalog
- ✅ No hallucinated agents
- ✅ Clear agent-to-task mapping
- ✅ Documentation of swarm composition

**Validation Pass Rate:** Aim for 100% agent type accuracy in swarm prompts.

---

**Last Verified:** 2025-11-03
**Agent Catalog Version:** 1.1.0 (54 agents)
**Next Review:** 2025-12-01
