# Progressive Context Loading Research Report

**Date:** 2025-11-01
**Prepared for:** CLAUDE.md restructure (80K → progressive loading)
**Status:** Research Complete

---

## Executive Summary

Research into Anthropic's Skills architecture, MCP resource organization, and large-scale documentation patterns reveals a clear path forward for restructuring CLAUDE.md. The optimal approach combines:

1. **Lightweight Policy Anchor** (~2,000 words) - Keep critical rules, navigation index, and enforcement in root CLAUDE.md
2. **Hierarchical Memory System** - Organize detailed context into high/medium/low detail levels following Anthropic's 4-tier memory hierarchy
3. **Progressive Disclosure** - Load context on-demand using Skills-style "name + brief description" navigation
4. **Import Syntax** - Leverage `@path/to/import` for modular composition

**Key Finding:** Anthropic's Skills system proves LLMs can autonomously navigate hierarchical documentation when given clear indexes and brief descriptions. Our 80K CLAUDE.md should become a 2K navigation hub pointing to 15-20 topic-specific modules.

---

## 1. Anthropic Skills Architecture

### Core Design Principles

Anthropic's Skills system (released October 2025) implements **progressive disclosure** - Claude initially sees only skill names and brief descriptions, then autonomously decides which skills to load based on the task at hand.

**Architecture:**
- **Discovery Phase:** LLM sees table of contents (skill names + 1-2 sentence descriptions)
- **Selection Phase:** LLM autonomously chooses relevant skills
- **Loading Phase:** Full markdown files (SKILL.md) loaded as new user messages
- **Execution Phase:** Skills modify context, tools, and model parameters

**Key Innovation:** "Prompts are hierarchical and retrieved as needed—like a decision tree of prompt 'files.' Think of it like Wikipedia: you start with a table of contents that references deeper and deeper fragments only when necessary."

### Skills vs Traditional Prompts

| Traditional Prompts | Anthropic Skills |
|---------------------|------------------|
| All context loaded upfront | Progressive disclosure |
| Static, single-file | Modular, composable |
| Fixed context window | Unbounded context potential |
| Manual selection | Autonomous navigation |

**Application to CLAUDE.md:**
Our root CLAUDE.md should act as the "skills index" - listing available topics with brief descriptions, allowing LLMs to autonomously load detailed context only when needed.

---

## 2. CLAUDE.md Memory Hierarchy (Official)

Anthropic's official documentation outlines a **4-tier cascading memory system**:

### Tier 1: Enterprise Memory (Organization-wide)
- Security policies, compliance rules
- Shared across all users and projects
- Highest precedence

### Tier 2: User Memory (`~/.claude/CLAUDE.md`)
- Personal preferences, coding styles
- Loaded for all projects
- Second-highest precedence

### Tier 3: Project Memory (`./CLAUDE.md`)
- Project-specific instructions, commands
- Most common location
- Should be checked into Git

### Tier 4: Subdirectory Memory (on-demand)
- Discovered when interacting with subdirectory files
- Loaded progressively as needed
- Lowest precedence

**Loading Order:** Files higher in hierarchy take precedence. System recursively merges all discovered CLAUDE.md files.

**Import Syntax:** `@path/to/import` enables modular composition within files.

**Best Practice:** "Keep CLAUDE.md files minimal, including only information that is essential for every session."

---

## 3. Progressive Context Loading Best Practices

### Quality Over Quantity

**Key Research Finding:** "Simply filling the context window with as much information as possible is actually a bad practice, as this creates context bloat which can lead to worse performance and higher costs."

**The "Lost in the Middle" Problem:**
- Performance degrades significantly as context length increases
- Relevant information at **beginning or end** = highest performance
- Information in **middle of long contexts** = significantly degraded performance

**Implication for CLAUDE.md:**
- Keep root file brief (<2,000 words)
- Place critical enforcement rules at beginning
- Place navigation index at end
- Move detailed explanations to separate modules

### Directory-Level Context

"Some tools support directory-level rules or memory files, where context is only loaded when the model is working on tasks in that specific directory."

**Application:**
```
docs/
├── CLAUDE.md              # Docs-specific context
├── guides/
│   └── CLAUDE.md          # Guide authoring standards
├── standards/
│   └── CLAUDE.md          # Standards development rules
scripts/
└── CLAUDE.md              # Script development context
```

### Selective Loading Strategies

Research shows "dynamic example selection" and "heuristic-based example selection" achieve better results than loading all available examples.

**For CLAUDE.md:**
- Root file = high-level index + critical rules
- Topic modules = loaded on-demand when relevant
- Edge case documentation = nested deeper, loaded only when needed

---

## 4. MCP Resource Organization Patterns

### Three-Primitive Model

MCP servers organize context through:

1. **Resources** - Data sources (like GET endpoints, no side effects)
2. **Tools** - Actionable operations (can perform computations, side effects)
3. **Prompts** - Reusable templates and workflows

**Key Architecture:**
- Resources have URIs and names for discovery
- Capability negotiation ensures clear understanding of what's available
- Clients have 1:1 relationship with servers (stateful sessions)

**Application to CLAUDE.md:**

```markdown
## Available Context Modules (Resources)

### Blog Writing (`@docs/guides/blog-writing.md`)
Standards for blog post creation, style, citations, humanization.

### Security & NDA Compliance (`@docs/guides/security-compliance.md`)
Government work boundaries, responsible disclosure, homelab attribution.

### SPARC Development (`@docs/guides/sparc-development.md`)
SPARC methodology, swarm orchestration, agent coordination.
```

LLM can "discover" resources via URI + description, then load on-demand.

---

## 5. Architecture Decision Records (ADR) Patterns

### Hierarchical Relationship Model

"The consequences of one ADR are very likely to become the context for subsequent ADRs, similar to Alexander's idea of a pattern language: the large-scale responses create spaces for the smaller scale to fit into."

**Key Principles:**
- Each ADR addresses one core technical direction
- Multi-phase decisions logged as separate records
- ADRs serve as append-only log (design evolution over time)
- Best location: dedicated ADR folder in documentation, near source code

**Integration with C4 Model:**
- C4 diagrams show the "what" (architecture structure)
- ADRs document the "why" (decision rationale)
- Together they provide complete context

**Application to CLAUDE.md:**
- Root CLAUDE.md = architectural overview (the "what")
- Topic modules = decision rationale (the "why")
- Lessons learned docs = evolution log (the "how we got here")

---

## 6. Large Repository Documentation Patterns

### Kubernetes Codebase Organization

- Monorepo structure with multiple components
- Main repository contains core components
- Separate repos for specialized tools (kubectl, cli-runtime)
- Clear directory hierarchy: `/cmd`, `/pkg`, `/docs`

### React Application Structure

"Structure projects by features instead of by type, grouping all related features together and nesting them as needed."

**Principles:**
- Feature-based organization > type-based
- One entity per file (improved navigation)
- Less rules > more rules (strict simple rules scale better)
- Large apps cannot be structured like small apps

**Application to CLAUDE.md:**

Organize by **workflow/task** rather than by **content type**:

```
docs/
├── workflows/
│   ├── blog-writing.md          # Complete blog workflow
│   ├── code-reduction.md        # Code-to-content optimization
│   └── humanization.md          # Humanization refinement
├── policies/
│   ├── security-compliance.md   # NDA, responsible disclosure
│   └── content-boundaries.md    # What to never discuss
├── tools/
│   ├── script-catalog.md        # Available scripts
│   └── validation-tools.md      # Testing and validation
```

### Document Indexing Best Practices

**Key Findings:**
- Systematic organization using searchable tags, metadata, taxonomies
- Set up indexes at share level for large repositories (divide into segments)
- Analytics-driven optimization based on user search patterns
- Cross-platform integration for consistent indexing

**Application:**
- Root CLAUDE.md = master index with tags/metadata
- Topic modules tagged by workflow, priority, frequency
- Search-optimized structure (H1/H2/H3 hierarchy)

---

## Recommended Architecture for CLAUDE.md

### 1. Root CLAUDE.md Structure (Target: 2,000 words)

```markdown
# Claude Code Configuration - SPARC Development Environment

**VERSION:** 4.0.0
**LAST UPDATED:** 2025-11-01
**CONTEXT LOADING:** Progressive (see Context Index below)

---

## 🚨 CRITICAL ENFORCEMENT RULES (Always Loaded)

### File Management
- NEVER save files to root directory
- ALWAYS update MANIFEST.json after changes
- MUST check .claude-rules.json before operations

### Content Compliance
- Zero tolerance for work references (NDA)
- All claims require citations with working hyperlinks
- Humanization score ≥75/100 before commit

### Development Standards
- Concurrent execution in single message (2.8-4.4x faster)
- TodoWrite batch operations (5-10+ todos minimum)
- Pre-commit hooks enforce all standards

---

## 📚 Context Index (Load on Demand)

### High Priority (Load First)
Load these for most development tasks:

- **[@docs/workflows/blog-writing.md](workflows/blog-writing.md)** (3,500 words)
  Blog post creation, Smart Brevity transformation, humanization standards.

- **[@docs/policies/security-compliance.md](policies/security-compliance.md)** (1,200 words)
  Government work boundaries, NDA compliance, responsible disclosure.

- **[@docs/workflows/code-development.md](workflows/code-development.md)** (2,800 words)
  SPARC methodology, swarm orchestration, agent coordination.

### Medium Priority (Load When Relevant)
Load these for specialized tasks:

- **[@docs/workflows/image-management.md](workflows/image-management.md)** (2,100 words)
  Blog image generation, optimization, gist management.

- **[@docs/workflows/citation-research.md](workflows/citation-research.md)** (1,800 words)
  Academic source discovery, citation formatting, link validation.

- **[@docs/tools/script-catalog.md](tools/script-catalog.md)** (3,200 words)
  Complete inventory of 37 scripts organized by category.

### Low Priority (Load Only When Needed)
Load these for edge cases and deep reference:

- **[@docs/reference/batch-completion-reports.md](reference/batch-completion-reports.md)**
  Historical batch transformation results (Batch 1-6).

- **[@docs/reference/lessons-learned.md](reference/lessons-learned.md)**
  Cumulative lessons from enhancement missions.

- **[@docs/policies/edge-cases.md](policies/edge-cases.md)**
  Career posts, technical deep-dives, security disclosure, meta posts.

---

## 🔍 Quick Discovery Guide

**New to this repository?** Load in this order:
1. [@docs/guides/LLM_ONBOARDING.md](guides/LLM_ONBOARDING.md) (5 min read)
2. [@docs/ENFORCEMENT.md](ENFORCEMENT.md) (critical rules)
3. This file (you're reading it)

**Working on blog posts?** Load:
1. [@docs/workflows/blog-writing.md](workflows/blog-writing.md)
2. [@docs/policies/security-compliance.md](policies/security-compliance.md)
3. [@docs/workflows/citation-research.md](workflows/citation-research.md)

**Debugging validation errors?** Load:
1. [@docs/tools/validation-tools.md](tools/validation-tools.md)
2. [@docs/reference/common-errors.md](reference/common-errors.md)

---

## 📊 Current Compliance Status (Always Visible)

| Metric | Status | Last Audit |
|--------|--------|------------|
| NDA Compliance | 100% | 2025-10-28 |
| Citation Coverage | 90%+ | 2025-10-28 |
| Humanization Rate | 94.5% (52/55 posts) | 2025-10-29 |
| Build Status | PASSING | 2025-11-01 |

---

## 🎯 Mission Statement

This blog shares real homelab and research work with authentic personal voice. We prioritize:
- Technical accuracy with reputable citations
- Personal storytelling over credentials
- Accessibility and mobile-first design
- Transparency about failures and trade-offs

---

**For detailed context on any topic, load the appropriate module from Context Index above.**
```

### 2. Hierarchical Module Structure

#### High Detail Level (3,000-5,000 words)
**Purpose:** Complete workflow documentation for frequent tasks
**Examples:** Blog writing, code development, SPARC methodology
**Load frequency:** Most sessions

**Structure:**
```markdown
# Blog Writing Workflow

## Quick Reference
- Target length: 1,400-2,100 words
- Citations: 10+ with working hyperlinks
- Humanization: ≥75/100 score
- Images: Hero + 1 per major section

## Phase-by-Phase Guide
[Detailed 7-phase methodology]

## Validation Checklist
[Complete pre-commit checklist]

## Common Pitfalls
[Edge cases and troubleshooting]

## Examples
[3-5 concrete examples]
```

#### Medium Detail Level (1,500-2,500 words)
**Purpose:** Specialized context for specific task types
**Examples:** Image management, citation research, script usage
**Load frequency:** 30-40% of sessions

**Structure:**
```markdown
# Citation Research Workflow

## Overview
[2-3 paragraph summary]

## Tools and Scripts
[Relevant scripts with usage examples]

## Best Practices
[Key principles in bullet form]

## Validation
[How to verify citations]
```

#### Low Detail Level (500-1,000 words)
**Purpose:** Edge cases, historical context, deep reference
**Examples:** Batch completion reports, lessons learned, specific edge cases
**Load frequency:** <10% of sessions

**Structure:**
```markdown
# Security Post Edge Cases

## When This Applies
[Specific scenarios]

## Adjustments
[How standards differ]

## Examples
[2-3 concrete examples]
```

### 3. Navigation Metadata

Each module should include frontmatter for discovery:

```markdown
---
title: "Blog Writing Workflow"
category: "workflow"
priority: "high"
frequency: "most-sessions"
dependencies: ["security-compliance.md", "citation-research.md"]
tags: ["blog", "writing", "humanization", "smart-brevity"]
last_updated: "2025-11-01"
word_count: 3500
estimated_read: "15 minutes"
---
```

### 4. Import Strategy

Use `@path/to/import` for composition:

```markdown
# Blog Writing Workflow

## Security Compliance
@docs/policies/security-compliance.md#nda-boundaries

## Humanization Standards
@docs/workflows/humanization.md#7-phase-methodology

## Citation Requirements
@docs/workflows/citation-research.md#minimum-standards
```

---

## Examples of Topic Splitting

### Example 1: Blog Writing (Currently ~8,000 words in CLAUDE.md)

**Root CLAUDE.md (200 words):**
```markdown
## 📝 Blog Post Creation

**Quick start:** Load [@docs/workflows/blog-writing.md](workflows/blog-writing.md)

**Minimum standards:**
- 1,400-2,100 words (6-9 min read)
- 10+ citations with working hyperlinks
- Humanization score ≥75/100
- Hero image + section images
- <25% code-to-content ratio

**Pre-commit validation:**
```bash
python scripts/blog-content/humanization-validator.py --post [file].md
python scripts/blog-research/check-citation-hyperlinks.py
```

**For complete workflow, load blog-writing.md.**
```

**docs/workflows/blog-writing.md (3,500 words):**
```markdown
# Blog Writing Workflow

## Quick Reference
[Essential checklist]

## Content Requirements
[Detailed standards]

## Smart Brevity Transformation
[7-phase methodology]

## Humanization Standards
[Validation and refinement]

## Pre-Publication Checklist
[Complete validation steps]

## Examples
[3-5 complete examples]
```

**docs/workflows/humanization.md (2,000 words):**
```markdown
# Humanization Refinement

## 7-Phase Methodology
[Detailed phase-by-phase]

## Validation with v2.0
[Humanization validator usage]

## Edge Cases
[Career posts, technical deep-dives]
```

---

### Example 2: Security & NDA Compliance (Currently ~1,500 words)

**Root CLAUDE.md (100 words):**
```markdown
## 🔒 Security & NDA Compliance

**CRITICAL:** Zero tolerance for work references.

**Never discuss:**
- Current or recent work incidents
- Specific government systems
- Active vulnerabilities at work

**Always use:**
- "Years ago, I learned..." (vague timeframes)
- "In my homelab..." (personal projects)
- "Research suggests..." (academic framing)

**For complete guidelines, load [@docs/policies/security-compliance.md](policies/security-compliance.md)**
```

**docs/policies/security-compliance.md (1,200 words):**
```markdown
# Security & NDA Compliance

## Overview
[Why this matters]

## Never Discuss (Complete List)
[Comprehensive boundaries]

## Safe Patterns
[Approved phrasings with examples]

## Time Buffering
[How to reference past work]

## Homelab Attribution
[Security testing framing]

## Responsible Disclosure
[90-day rule, CVSS scoring]
```

---

### Example 3: SPARC Development (Currently ~3,000 words)

**Root CLAUDE.md (150 words):**
```markdown
## 🚀 SPARC Development

**Quick commands:**
```bash
npx claude-flow sparc tdd "<feature>"     # Full TDD workflow
npx claude-flow sparc batch <modes> "<task>"  # Parallel execution
```

**Core methodology:**
1. Specification → Requirements analysis
2. Pseudocode → Algorithm design
3. Architecture → System design
4. Refinement → TDD implementation
5. Completion → Integration

**Available agents:** 54 total (coder, reviewer, tester, planner, researcher...)

**For complete SPARC guide, load [@docs/workflows/code-development.md](workflows/code-development.md)**
```

**docs/workflows/code-development.md (2,800 words):**
```markdown
# SPARC Development Workflow

## Overview
[SPARC methodology explained]

## Available Commands
[Complete command reference]

## Agent Catalog
[54 agents organized by category]

## Swarm Orchestration
[Multi-agent coordination patterns]

## Integration with MCP
[How SPARC uses MCP tools]

## Examples
[Complete workflow examples]
```

---

## Implementation Checklist

### Phase 1: Restructure Root CLAUDE.md (2-3 hours)
- [ ] Create new root CLAUDE.md with 2,000 word limit
- [ ] Keep critical enforcement rules at top
- [ ] Build Context Index with 3-tier priority
- [ ] Add Quick Discovery Guide
- [ ] Preserve compliance status dashboard
- [ ] Test that minimal context loads correctly

### Phase 2: Extract High-Priority Topics (4-6 hours)
- [ ] Create `docs/workflows/blog-writing.md` (3,500 words)
- [ ] Create `docs/workflows/code-development.md` (2,800 words)
- [ ] Create `docs/policies/security-compliance.md` (1,200 words)
- [ ] Add navigation metadata to each file
- [ ] Test import syntax works correctly
- [ ] Validate LLM can discover and load modules

### Phase 3: Extract Medium-Priority Topics (3-4 hours)
- [ ] Create `docs/workflows/image-management.md` (2,100 words)
- [ ] Create `docs/workflows/citation-research.md` (1,800 words)
- [ ] Create `docs/workflows/humanization.md` (2,000 words)
- [ ] Create `docs/tools/script-catalog.md` (3,200 words)
- [ ] Add cross-references between related modules

### Phase 4: Organize Low-Priority Reference (2-3 hours)
- [ ] Consolidate batch completion reports
- [ ] Organize lessons learned by category
- [ ] Document edge cases separately
- [ ] Create index of archived documentation
- [ ] Ensure nothing is lost in transition

### Phase 5: Update Cross-References (2-3 hours)
- [ ] Update all `@import` paths
- [ ] Fix links in existing documentation
- [ ] Update LLM_ONBOARDING.md with new structure
- [ ] Update ENFORCEMENT.md references
- [ ] Test all navigation paths work

### Phase 6: Validation & Testing (2-3 hours)
- [ ] Load root CLAUDE.md in fresh session (verify <2K words)
- [ ] Test that LLM can autonomously navigate to topics
- [ ] Verify import syntax loads correctly
- [ ] Test Quick Discovery Guide pathways
- [ ] Confirm all critical rules still enforced
- [ ] Run full build and deployment test

### Phase 7: Documentation & Communication (1-2 hours)
- [ ] Update MANIFEST.json with new structure
- [ ] Document migration in ARCHITECTURE.md
- [ ] Create migration guide for future LLMs
- [ ] Update pre-commit hooks if needed
- [ ] Add note about new structure to README

---

## Key Principles to Follow

### 1. Progressive Disclosure
"Start with a table of contents that references deeper and deeper fragments only when necessary."

**Implementation:**
- Root CLAUDE.md = index with brief descriptions
- LLM loads detailed context only when relevant
- Avoid loading all context upfront

### 2. Quality Over Quantity
"Simply filling the context window with as much information as possible is actually a bad practice."

**Implementation:**
- Keep root file <2,000 words
- Place critical rules at beginning (loaded first)
- Place navigation at end (reference after understanding context)

### 3. Autonomous Navigation
"Claude initially sees only skill names and brief descriptions, then autonomously decides which skills to load."

**Implementation:**
- Clear, descriptive module names
- 1-2 sentence descriptions per module
- Trust LLM to choose relevant context

### 4. Hierarchical Precedence
"Files higher in the hierarchy take precedence and are loaded first."

**Implementation:**
- Root CLAUDE.md = highest authority
- Workflow modules = second level
- Edge cases and reference = lowest level

### 5. Keep Memory Lean
"Include only information that is essential for every session."

**Implementation:**
- Root file = universally relevant rules
- Topic modules = task-specific context
- Archive = historical reference only

### 6. Structure for Discovery
"Systematic organization using searchable tags, metadata, taxonomies."

**Implementation:**
- Consistent frontmatter in all modules
- Tag-based organization
- Clear H1/H2/H3 hierarchy
- Searchable naming conventions

### 7. Feature-Based Organization
"Structure projects by features instead of by type, grouping all related features together."

**Implementation:**
- Organize by workflow/task (not by content type)
- Group related context together
- Nest edge cases under primary topics

### 8. Minimize Rules, Maximize Clarity
"Less rules is better than more rules, with strict following of simple general rules."

**Implementation:**
- Each module focuses on one core workflow
- Clear, simple guidelines over exhaustive edge cases
- Link to examples rather than explaining every scenario

### 9. Versioning and Evolution
"ADRs serve as append-only log, extending beyond initial design."

**Implementation:**
- Version root CLAUDE.md (currently 4.0.0)
- Track when modules last updated
- Preserve lessons learned as evolution log

### 10. Test-Driven Refactoring
"Validate improvements with automated testing."

**Implementation:**
- Verify build passes after restructure
- Test LLM can navigate new structure
- Confirm pre-commit hooks still work
- Validate no loss of critical information

---

## Success Metrics

**After implementation, measure:**
- Root CLAUDE.md word count: Target <2,000 (currently ~12,900)
- Context loading time: <1 second for root + one module
- Navigation success rate: LLM finds correct module >95% of time
- No degradation in build success rate (currently 100%)
- No new compliance violations introduced
- Developer satisfaction with new structure

---

## References

### Primary Sources
1. **Anthropic Skills Architecture**
   - [Official Skills Announcement](https://www.anthropic.com/news/skills) (October 2025)
   - [Skills Deep Dive](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
   - [Memory Management Docs](https://docs.claude.com/en/docs/claude-code/memory)

2. **Progressive Context Loading Research**
   - "Lost in the Middle: How Language Models Use Long Contexts" ([arXiv:2307.03172](https://arxiv.org/abs/2307.03172))
   - [LLM Context Management Guide](https://eval.16x.engineer/blog/llm-context-management-guide)

3. **MCP Architecture**
   - [Model Context Protocol Core Architecture](https://modelcontextprotocol.io/docs/concepts/architecture)
   - [MCP Introduction](https://www.philschmid.de/mcp-introduction)

4. **ADR Patterns**
   - [Architecture Decision Records GitHub](https://adr.github.io/)
   - [Microsoft Azure ADR Guide](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record)

5. **Large Repository Documentation**
   - [Kubernetes Codebase Guide](https://dev.to/chuck_ha/learning-the-kubernetes-codebase-1324)
   - [React Application Structure](https://reactresources.com/topics/code-organization)

### Internal Documentation
- Current CLAUDE.md (12,900 words)
- MANIFEST.json (repository inventory)
- docs/ARCHITECTURE.md (system design)
- docs/guides/LLM_ONBOARDING.md (quick start)
- docs/ENFORCEMENT.md (mandatory rules)

---

## Conclusion

The path forward is clear: transform our 80K token CLAUDE.md into a **lightweight navigation hub** (~2,000 words) with **progressive context loading** through hierarchical modules. Anthropic's Skills architecture proves LLMs can autonomously discover and load relevant context when given clear indexes and brief descriptions.

**Next Steps:**
1. Review this research with stakeholders
2. Begin Phase 1: Restructure root CLAUDE.md
3. Incrementally extract topics into modules
4. Validate navigation and loading work correctly
5. Measure success against defined metrics

**Expected Outcome:**
- 85% reduction in root file size (12,900 → 2,000 words)
- Faster context loading (<1 second for relevant modules)
- Improved LLM navigation (autonomous topic discovery)
- Maintained 100% compliance and enforcement
- Preserved all critical information (zero loss)

---

**Research completed:** 2025-11-01
**Prepared by:** Research Agent
**Next review:** After Phase 1 implementation
