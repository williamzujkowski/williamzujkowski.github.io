---
title: Task Routing Patterns & Loading Sequences
category: workflows
priority: HIGH
version: 1.0.0
last_updated: 2025-11-16
estimated_tokens: 1800
load_when:
  - Determining which modules to load for a task
  - Unclear which pattern matches current work
  - Need explicit loading sequence
  - Validating routing compliance
dependencies:
  - core/enforcement
  - core/nda-compliance
tags: [routing, loading, patterns, tasks, sequences, mandatory]
---

# Task Routing Patterns & Loading Sequences

## Purpose

This module provides **explicit loading sequences** for common tasks, mapping task types to required modules. Use this when determining which modules to load, following the 3-tier routing system (MANDATORY/RECOMMENDED/OPTIONAL).

---

## When to Load This Module

- **Determining modules to load** - Start here before any task
- **Unclear which pattern applies** - Find similar task pattern
- **Need step-by-step loading sequence** - Use explicit file paths
- **Validating routing compliance** - Check against checklist

---

## Quick Reference

**Common Task Patterns:**

| Task Type | Tier | Required Modules | Token Cost |
|-----------|------|-----------------|------------|
| Create blog post | 🚨 MANDATORY | enforcement + nda-compliance + blog-topic-summary + blog-writing + writing-style | ~16K |
| Transform post | ✅ RECOMMENDED | enforcement + blog-transformation + writing-style | ~10K |
| Refactor quality | ✅ RECOMMENDED | enforcement + code-block-quality + blog-transformation | ~6K |
| Validate content | ✅ RECOMMENDED | enforcement + humanization-standards + citation-research | ~5K |
| Manage images | 💡 OPTIONAL | image-standards + image-automation | ~3K |
| Git operations | 🚨 MANDATORY | enforcement + git-workflow | ~4K |
| SPARC development | ✅ RECOMMENDED | enforcement + sparc-development + agent-coordination | ~6K |
| Swarm orchestration | 🚨 MANDATORY | enforcement + swarm-orchestration + agent-coordination | ~6K |
| Emergency debug | ✅ RECOMMENDED | enforcement + mandatory-reading | ~4K |

**Pattern:** 🚨 MANDATORY tasks block without required skills. ✅ RECOMMENDED tasks warn but allow override. 💡 OPTIONAL tasks use LLM judgment.

---

## Explicit Loading Sequences

### Task 1: Create Blog Post

**Tier:** 🚨 MANDATORY
**Token cost:** ~16K
**Required modules (load in exact order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: MANDATORY - NDA compliance
Read docs/context/core/nda-compliance.md

# Step 3: MANDATORY - Topic selection & gap analysis
Read docs/context/workflows/blog-topic-summary.md

# Step 3b: OPTIONAL - Load full topic selection module only when:
# - Planning content calendar or quarterly themes
# - Need comprehensive topic idea bank (90+ ideas)
# Read docs/context/workflows/blog-topic-selection.md

# Step 4: MANDATORY - Writing workflow
Read docs/context/workflows/blog-writing.md

# Step 5: MANDATORY - Writing style
Read docs/context/standards/writing-style.md
```

**Why MANDATORY:** Public content with NDA risks, must fill content gaps

---

### Task 2: Transform Existing Post

**Tier:** ✅ RECOMMENDED
**Token cost:** ~10K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: RECOMMENDED - Transformation workflow
Read docs/context/workflows/blog-transformation.md

# Step 3: RECOMMENDED - Writing style
Read docs/context/standards/writing-style.md
```

**Override scenario:** Emergency link fix (don't need full transformation workflow)

---

### Task 3: Git Commit

**Tier:** 🚨 MANDATORY
**Token cost:** ~4K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: MANDATORY - Git workflow
Read docs/context/technical/git-workflow.md
```

**Why MANDATORY:** Commits permanent, must validate before pushing

---

### Task 4: Swarm Orchestration

**Tier:** 🚨 MANDATORY
**Token cost:** ~6K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: MANDATORY - Swarm workflow
Read docs/context/workflows/swarm-orchestration.md

# Step 3: MANDATORY - Agent coordination
Read docs/context/technical/agent-coordination.md
```

**Why MANDATORY:** Prevents hallucinated agents, ensures coordination

---

### Task 5: Refactor Code Block Quality

**Tier:** ✅ RECOMMENDED
**Token cost:** ~6K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: RECOMMENDED - Code block standards
Read docs/context/standards/code-block-quality.md

# Step 3: RECOMMENDED - Transformation workflow (if blog post)
Read docs/context/workflows/blog-transformation.md
```

**Override scenario:** Typo fix (don't need full quality framework)

---

### Task 6: Validate Content

**Tier:** ✅ RECOMMENDED
**Token cost:** ~5K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: RECOMMENDED - Humanization standards
Read docs/context/standards/humanization-standards.md

# Step 3: RECOMMENDED - Citation research
Read docs/context/standards/citation-research.md
```

**Override scenario:** Quick link check (don't need humanization validation)

---

### Task 7: Manage Images

**Tier:** 💡 OPTIONAL
**Token cost:** ~3K
**Required modules (load in order):**

```bash
# Step 1: RECOMMENDED - Image standards
Read docs/context/standards/image-standards.md

# Step 2: RECOMMENDED - Image automation
Read docs/context/technical/image-automation.md
```

**LLM judgment:** One-off update may not need automation module

---

### Task 8: SPARC Development

**Tier:** ✅ RECOMMENDED
**Token cost:** ~6K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: RECOMMENDED - SPARC workflow
Read docs/context/workflows/sparc-development.md

# Step 3: RECOMMENDED - Agent coordination
Read docs/context/technical/agent-coordination.md
```

**Override scenario:** Simple script (don't need full TDD methodology)

---

### Task 9: Emergency Debug

**Tier:** ✅ RECOMMENDED
**Token cost:** ~4K
**Required modules (load in order):**

```bash
# Step 1: MANDATORY - Core enforcement
Read docs/context/core/enforcement.md

# Step 2: RECOMMENDED - Mandatory reading
Read docs/context/core/mandatory-reading.md

# Step 3: OPTIONAL - Troubleshooting (if available)
# Read docs/context/reference/troubleshooting.md
```

**Override scenario:** Known issue with obvious fix

---

## Tier 2: RECOMMENDED Patterns (15 total)

**Pattern:** These combinations proven effective but allow override with documented reasoning.

| Pattern | Recommended Skills | Override Scenario |
|---------|-------------------|-------------------|
| Blog transformation | enforcement + blog-transformation + writing-style + citation-research | Emergency link fix |
| Content validation | enforcement + humanization-standards + citation-research | Quick link check |
| Image management | image-standards + image-automation | One-off update |
| Code refactoring | enforcement + code-block-quality + blog-transformation | Typo fix |
| SPARC development | enforcement + sparc-development + agent-coordination | Simple script |
| Gist extraction | gist-management + code-block-quality | Single code block move |
| Research automation | research-automation + citation-research | Manual citation |
| Security writing | writing-style + technical-authority + nda-compliance | Non-security topic |
| Module creation | module-template + file-management + standards-integration | Quick reference doc |
| Script development | script-template + sparc-development | Throwaway test script |
| Mermaid diagrams | accessibility + writing-style | Simple flowchart |
| Accessibility review | accessibility + image-standards + humanization-standards | Text-only content |
| Performance optimization | build-automation + image-automation | CSS-only change |
| Documentation update | mandatory-reading + file-management + documentation-hierarchy | Typo fix |
| Archive cleanup | file-management + compliance-history | Single file delete |

**Complete list:** See `docs/context/INDEX.yaml` routing_patterns section

---

## Tier 3: OPTIONAL (LLM Autonomy)

**Discovery mechanisms for novel tasks:**

### By Tags

INDEX.yaml maps tags → skills:
- "citations" → citation-research + research-automation
- "blog" → blog-writing + blog-transformation + humanization-standards + writing-style
- "enforcement" → enforcement + standards-integration
- "images" → image-standards + image-automation
- "git" → git-workflow + enforcement

### By Priority

- **HIGH:** Always consider loading (enforcement, nda-compliance, file-management, mandatory-reading, standards-integration)
- **MEDIUM:** Load for specific workflows (blog-writing, sparc-development, swarm-orchestration, writing-style)
- **LOW:** Load only when explicitly needed (gist-management, build-automation, templates)

### By Similarity

"This is like [known pattern] but different because..."

**Example:**
- Task: "Create CLI automation tool"
- Similar to: SPARC development (script creation)
- Different: Not test-driven, simpler scope
- Load: enforcement + script-template (skip sparc-development)

---

## Routing Validation Checklist

### Before Starting ANY Task

- [ ] Checked this module (routing-patterns.md) for routing requirements
- [ ] Identified task tier (MANDATORY/RECOMMENDED/OPTIONAL)
- [ ] Loaded required skills in correct order
- [ ] Verified dependencies (checked INDEX.yaml)
- [ ] Documented any overrides with reasoning

### After Completing Task

- [ ] All required skills were applied correctly
- [ ] No MANDATORY skills were skipped
- [ ] Override reasons documented (if any)
- [ ] Novel patterns noted for future routing improvements

---

## Loading Sequence Template

**Use this template for documenting custom loading sequences:**

```markdown
### Task: [Task Name]

**Tier:** [MANDATORY/RECOMMENDED/OPTIONAL]
**Token cost:** ~[estimate]K
**Required modules (load in order):**

```bash
# Step 1: [MANDATORY/RECOMMENDED/OPTIONAL] - [reason]
Read docs/context/[category]/[module].md

# Step 2: [MANDATORY/RECOMMENDED/OPTIONAL] - [reason]
Read docs/context/[category]/[module].md
```

**Why [tier]:** [Justification for tier assignment]
**Override scenario:** [When it's acceptable to skip modules]
```

---

## Examples

### Example 1: Blog Post Creation (MANDATORY)

**Task:** Create new blog post about security topic

**Routing decision:**
1. Check this module → Found "Task 1: Create Blog Post"
2. Identified tier: 🚨 MANDATORY
3. Loaded 5 modules in order (enforcement, nda-compliance, blog-topic-summary, blog-writing, writing-style)
4. No overrides (MANDATORY can't be overridden)

**Outcome:** All required skills loaded, ready to create post

---

### Example 2: Emergency Bug Fix (RECOMMENDED with override)

**Task:** Fix broken link in blog post (emergency)

**Routing decision:**
1. Check this module → Similar to "Task 2: Transform Existing Post"
2. Identified tier: ✅ RECOMMENDED (but override justified)
3. Loaded only enforcement.md (skip blog-transformation, writing-style)
4. Documented override: "Emergency link fix, don't need full transformation workflow"

**Outcome:** Faster execution (4K vs 10K tokens), override documented

---

### Example 3: Novel Task (OPTIONAL)

**Task:** Create dashboard for blog statistics

**Routing decision:**
1. Check this module → No exact match
2. Similar to: Script development + Data visualization
3. Discovery via tags: "automation" → script-catalog + research-automation
4. Loaded: enforcement + script-template + sparc-development (TDD for data accuracy)
5. Documented: "Novel task: Dashboard creation. Loaded script-template + sparc-development. Consider promoting to Tier 2 if repeated."

**Outcome:** Found relevant modules via discovery, documented for future

---

## Common Pitfalls

### Pitfall 1: Loading Too Many Modules

**Problem:** Loading all modules "just in case"
**Solution:** Use this routing catalog to load only what's needed
**Prevention:** Check tier system, respect OPTIONAL judgment

### Pitfall 2: Skipping MANDATORY Skills

**Problem:** Ignoring MANDATORY requirements to save tokens
**Solution:** Pre-commit will block, wasting more time
**Prevention:** Always check tier before starting task

### Pitfall 3: Not Documenting Overrides

**Problem:** Overriding RECOMMENDED without explaining why
**Solution:** Document reason in task notes or commit message
**Prevention:** Use "Override scenario" as template

---

## Cross-References

**Related modules:**
- [autonomy-framework.md](../core/autonomy-framework.md) - When to follow routing vs use judgment
- [enforcement.md](../core/enforcement.md) - Mandatory enforcement rules
- [mandatory-reading.md](../core/mandatory-reading.md) - Documentation hierarchy

**External references:**
- `docs/context/INDEX.yaml` - Complete module catalog
- `CLAUDE.md` - Root anchor with Tier 1 table
- `.claude-rules.json` - Enforcement rules

---

## Changelog

- **2025-11-16**: Initial extraction from CLAUDE.md v4.1.0 Section 3.2 (Task-Based Loading Patterns)
