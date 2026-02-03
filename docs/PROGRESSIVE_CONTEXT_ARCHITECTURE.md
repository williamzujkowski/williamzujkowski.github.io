# Progressive Context Loading Architecture for CLAUDE.md

**Version:** 1.0.0
**Date:** 2025-11-01
**Status:** DESIGN PHASE
**Author:** Strategic Planning Agent

---

## Executive Summary

This document provides a comprehensive architecture to restructure CLAUDE.md from an ~80K token monolithic document into a progressive context loading system that reduces context length by 80-90% while maintaining complete accessibility.

**Key Metrics:**
- Current size: ~12,900 words (~80K tokens at 6.2 tokens/word)
- Target main file: <2,000 words (<10K tokens)
- Reduction: 84% smaller main file
- Access pattern: On-demand loading via clear indexing

---

## 1. Folder Structure

### Proposed Directory Layout

```
williamzujkowski.github.io/
├── CLAUDE.md                           # Lightweight policy anchor (<10K tokens)
├── .claude-rules.json                  # Enforcement rules (unchanged)
├── MANIFEST.json                       # Repository inventory (unchanged)
│
├── docs/
│   ├── context/                        # NEW: Progressive context modules
│   │   ├── INDEX.yaml                  # Master index of all context modules
│   │   │
│   │   ├── core/                       # HIGH-priority: Core policies & workflows
│   │   │   ├── enforcement-rules.md    # Mandatory rules (from current §59-83)
│   │   │   ├── file-management.md      # File operations & organization
│   │   │   ├── concurrent-execution.md # Parallel ops & batch patterns
│   │   │   ├── compliance-status.md    # Current metrics dashboard
│   │   │   └── quick-reference.md      # Most-used commands & patterns
│   │   │
│   │   ├── workflows/                  # MEDIUM: Operational procedures
│   │   │   ├── blog-post-creation.md   # New post workflow
│   │   │   ├── blog-transformation.md  # Smart Brevity methodology
│   │   │   ├── humanization.md         # 7-phase humanization
│   │   │   ├── research-citations.md   # Citation standards
│   │   │   ├── image-management.md     # Image workflow
│   │   │   ├── gist-management.md      # GitHub gist workflow
│   │   │   └── cleanup-maintenance.md  # Cleanup protocols
│   │   │
│   │   ├── standards/                  # MEDIUM: Content & style guides
│   │   │   ├── writing-style.md        # "Polite Linus" voice
│   │   │   ├── content-boundaries.md   # NDA/work compliance
│   │   │   ├── research-verification.md # Fact-checking protocols
│   │   │   ├── accessibility.md        # WCAG & mobile standards
│   │   │   └── code-style.md           # Code formatting rules
│   │   │
│   │   ├── technical/                  # LOW: Technical implementation
│   │   │   ├── directory-structure.md  # Project layout
│   │   │   ├── build-commands.md       # npm scripts & tooling
│   │   │   ├── sparc-nexus-agents.md    # SPARC methodology
│   │   │   ├── agent-coordination.md   # MCP agents
│   │   │   └── performance-hooks.md    # Optimization patterns
│   │   │
│   │   ├── reference/                  # LOW: Lookup tables
│   │   │   ├── script-catalog.md       # All 37 scripts (links to SCRIPT_CATALOG.md)
│   │   │   ├── lessons-learned.md      # Historical insights
│   │   │   ├── batch-reports.md        # Enhancement history
│   │   │   └── edge-cases.md           # Special scenarios
│   │   │
│   │   └── templates/                  # LOW: Starter templates
│   │       ├── blog-post-template.md   # New post starter
│   │       ├── validation-checklist.md # Pre-publish checklist
│   │       └── module-template.md      # Context module template
│   │
│   ├── guides/                         # Existing guides (unchanged)
│   ├── archive/                        # Existing archive (unchanged)
│   └── ENFORCEMENT.md                  # Existing enforcement doc (reference)
```

### Naming Conventions

**Files:**
- Use kebab-case: `enforcement-rules.md`, `blog-post-creation.md`
- Be descriptive: Name shows content at a glance
- Avoid abbreviations unless universally known (e.g., NDA, WCAG)

**Directories:**
- Single word lowercase preferred: `core/`, `workflows/`, `standards/`
- Plural for collections: `templates/`, `workflows/`

**Versioning:**
- Files include version in frontmatter, not filename
- Use semantic versioning: `version: 1.2.3`

---

## 2. Main CLAUDE.md Structure

### New Lightweight Design (Target: <10K tokens)

```markdown
---
STATUS: AUTHORITATIVE
VERSION: 4.0.0
LAST_AUDIT: 2025-11-01
ARCHITECTURE: PROGRESSIVE_CONTEXT_LOADING
---

# Claude Code Configuration - Progressive Context System

## 🏛️ AUTHORITATIVE DOCUMENTATION NOTICE

This file serves as the **policy anchor** for the williamzujkowski.github.io repository.

**Complete documentation is organized into progressive context modules** at `docs/context/`.

**Last comprehensive audit:** 2025-11-01
**Next scheduled review:** 2026-02-01

---

## 🚨 MANDATORY ENFORCEMENT NOTICE 🚨

**CRITICAL**: Before ANY operation, you MUST:

1. **CHECK** `.claude-rules.json` for current enforcement rules
2. **VALIDATE** MANIFEST.json is current (check last_validated timestamp)
3. **VERIFY** no duplicate files will be created (check file_registry)
4. **CONFIRM** operation follows standards from https://github.com/williamzujkowski/standards
5. **USE** appropriate timestamps (prefer time.gov, fallback to system time)

**Full enforcement details:** `docs/context/core/enforcement-rules.md`

---

## 📊 Current Compliance Status

### Portfolio Health Dashboard

- **Content Compliance**: 100% (56/56 posts NDA-compliant)
- **Citation Coverage**: 90%+ (11.3 avg per post)
- **Humanization Scores**: 94.5% passing (≥75/100)
- **Build Status**: PASSING
- **Lighthouse Mobile**: 95+

**Detailed metrics:** `docs/context/core/compliance-status.md`

---

## 🗺️ Progressive Context Navigation

### How to Use This System

**For Quick Tasks:**
1. Check relevant section below for immediate guidance
2. Most operations need only 1-2 context modules
3. Load modules on-demand using provided paths

**For Complex Tasks:**
1. Start with `docs/context/INDEX.yaml` for full map
2. Load HIGH-priority modules first (core/)
3. Load MEDIUM/LOW modules as needed

**For First-Time LLMs:**
1. Read: `docs/guides/LLM_ONBOARDING.md` (5 min)
2. Load: `docs/context/core/enforcement-rules.md`
3. Load: `docs/context/core/quick-reference.md`
4. Proceed with your task

---

## 📚 Context Module Index

### Core Policies (HIGH Priority - Load First)

**When to load:** Before ANY operation

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [enforcement-rules.md](docs/context/core/enforcement-rules.md) | Mandatory rules & penalties | ~2K tokens | ALWAYS (first load) |
| [file-management.md](docs/context/core/file-management.md) | File operations, directory rules | ~1.5K | Creating/moving files |
| [concurrent-execution.md](docs/context/core/concurrent-execution.md) | Parallel ops, batch patterns | ~1.5K | Multi-step operations |
| [compliance-status.md](docs/context/core/compliance-status.md) | Current metrics dashboard | ~1K | Status checks |
| [quick-reference.md](docs/context/core/quick-reference.md) | Most-used commands | ~2K | Quick lookups |

**Total core context:** ~8K tokens (load all for comprehensive understanding)

---

### Workflows (MEDIUM Priority - Load As Needed)

**When to load:** Performing specific operations

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [blog-post-creation.md](docs/context/workflows/blog-post-creation.md) | New post workflow | ~4K | Creating new blog posts |
| [blog-transformation.md](docs/context/workflows/blog-transformation.md) | Smart Brevity 7-phase | ~3K | Refining existing posts |
| [humanization.md](docs/context/workflows/humanization.md) | v2.0 validation system | ~5K | Humanizing content |
| [research-citations.md](docs/context/workflows/research-citations.md) | Citation standards | ~3K | Adding sources |
| [image-management.md](docs/context/workflows/image-management.md) | Image workflow | ~3K | Working with images |
| [gist-management.md](docs/context/workflows/gist-management.md) | GitHub gist workflow | ~2K | Extracting code |
| [cleanup-maintenance.md](docs/context/workflows/cleanup-maintenance.md) | Cleanup protocols | ~2K | Maintenance tasks |

**Per-workflow context:** 2-5K tokens (load only what you need)

---

### Standards (MEDIUM Priority - Reference As Needed)

**When to load:** Writing or reviewing content

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [writing-style.md](docs/context/standards/writing-style.md) | "Polite Linus" voice | ~3K | Writing content |
| [content-boundaries.md](docs/context/standards/content-boundaries.md) | NDA/work compliance | ~2K | Reviewing sensitive topics |
| [research-verification.md](docs/context/standards/research-verification.md) | Fact-checking protocols | ~3K | Validating claims |
| [accessibility.md](docs/context/standards/accessibility.md) | WCAG & mobile standards | ~2K | UI/UX work |
| [code-style.md](docs/context/standards/code-style.md) | Code formatting rules | ~2K | Writing code |

**Per-standard context:** 2-3K tokens (load relevant standards only)

---

### Technical (LOW Priority - Load Rarely)

**When to load:** Deep system work or architecture questions

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [directory-structure.md](docs/context/technical/directory-structure.md) | Project layout | ~2K | Navigation questions |
| [build-commands.md](docs/context/technical/build-commands.md) | npm scripts & tooling | ~1.5K | Build/deploy issues |
| [sparc-nexus-agents.md](docs/context/technical/sparc-nexus-agents.md) | SPARC methodology | ~3K | Development workflows |
| [agent-coordination.md](docs/context/technical/agent-coordination.md) | MCP agents | ~2K | Multi-agent tasks |
| [performance-hooks.md](docs/context/technical/performance-hooks.md) | Optimization patterns | ~1.5K | Performance tuning |

**Per-technical context:** 1.5-3K tokens (rarely needed)

---

### Reference (LOW Priority - Lookup Only)

**When to load:** Looking up specific details

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [script-catalog.md](docs/context/reference/script-catalog.md) | All 37 scripts | ~6K | Finding scripts |
| [lessons-learned.md](docs/context/reference/lessons-learned.md) | Historical insights | ~3K | Learning from past |
| [batch-reports.md](docs/context/reference/batch-reports.md) | Enhancement history | ~2K | Historical context |
| [edge-cases.md](docs/context/reference/edge-cases.md) | Special scenarios | ~2K | Unusual situations |

**Per-reference context:** 2-6K tokens (load for lookup only)

---

### Templates (LOW Priority - Copy As Needed)

**When to load:** Creating new content or modules

| Module | Purpose | Size | Load When |
|--------|---------|------|-----------|
| [blog-post-template.md](docs/context/templates/blog-post-template.md) | New post starter | ~1K | Creating posts |
| [validation-checklist.md](docs/context/templates/validation-checklist.md) | Pre-publish checklist | ~1K | Before committing |
| [module-template.md](docs/context/templates/module-template.md) | Context module template | ~0.5K | Creating modules |

**Per-template context:** 0.5-1K tokens (minimal)

---

## 🎯 Common Task → Context Loading Patterns

### Task: Create New Blog Post

**Load sequence:**
1. `core/enforcement-rules.md` (mandatory)
2. `core/file-management.md` (file operations)
3. `workflows/blog-post-creation.md` (complete workflow)
4. `standards/writing-style.md` (voice guidelines)
5. `templates/blog-post-template.md` (starter template)

**Total context:** ~12K tokens

---

### Task: Refine Existing Blog Post

**Load sequence:**
1. `core/enforcement-rules.md` (mandatory)
2. `workflows/blog-transformation.md` (Smart Brevity 7-phase)
3. `workflows/humanization.md` (v2.0 validator)
4. `workflows/research-citations.md` (if adding sources)

**Total context:** ~13K tokens

---

### Task: Validate Content Quality

**Load sequence:**
1. `core/enforcement-rules.md` (mandatory)
2. `workflows/humanization.md` (validation system)
3. `templates/validation-checklist.md` (pre-publish)

**Total context:** ~7.5K tokens

---

### Task: Maintenance & Cleanup

**Load sequence:**
1. `core/enforcement-rules.md` (mandatory)
2. `core/file-management.md` (file operations)
3. `workflows/cleanup-maintenance.md` (protocols)

**Total context:** ~5.5K tokens

---

### Task: Script Development/Troubleshooting

**Load sequence:**
1. `core/enforcement-rules.md` (mandatory)
2. `technical/directory-structure.md` (project layout)
3. `reference/script-catalog.md` (find related scripts)
4. `standards/code-style.md` (formatting)

**Total context:** ~11.5K tokens

---

## 📖 Documentation Hierarchy

### Primary (Authoritative - Always Current)
- **CLAUDE.md** (this file): Policy anchor & navigation
- **MANIFEST.json**: System inventory and file registry
- **.claude-rules.json**: Enforcement rules

### Secondary (Supporting - Progressive Loading)
- **docs/context/**: Progressive context modules
- **docs/guides/**: How-to documentation
- **docs/ENFORCEMENT.md**: Extended enforcement details

### Generated (Reference - Derived Data)
- **reports/**: Audit and compliance reports
- **docs/archive/**: Historical documentation

> **Note**: Always load primary docs first, then secondary on-demand.

---

## 🔧 Maintenance Protocols

### Adding New Context Modules

1. Use template: `docs/context/templates/module-template.md`
2. Add entry to `docs/context/INDEX.yaml`
3. Update this CLAUDE.md index if HIGH priority
4. Update MANIFEST.json
5. Commit with descriptive message

### Updating Existing Modules

1. Update version number in module frontmatter
2. Document changes in module's changelog section
3. Update INDEX.yaml if categorization changes
4. Update MANIFEST.json last_validated timestamp
5. Run validation: `npm run validate:km`

### Archiving Obsolete Content

Follow retention policy:
- **Active (0-30 days)**: Keep in `docs/context/`
- **Archive (30-180 days)**: Move to `docs/archive/YYYY-QX/`
- **Purge (180+ days)**: Delete non-reference docs

**Never delete:**
- Enforcement rules
- Core workflows
- Lessons learned
- Final completion reports

---

## 🚀 Quick Start Commands

### For New LLMs
```bash
# Read onboarding (5 min)
cat docs/guides/LLM_ONBOARDING.md

# Load core context (required)
cat docs/context/core/enforcement-rules.md
cat docs/context/core/quick-reference.md

# Check current status
cat docs/context/core/compliance-status.md
```

### For Experienced LLMs
```bash
# Quick reference only
cat docs/context/core/quick-reference.md

# Load specific workflow
cat docs/context/workflows/[workflow-name].md

# Check compliance before starting
cat docs/context/core/compliance-status.md
```

### For Maintenance
```bash
# Cleanup protocol
cat docs/context/workflows/cleanup-maintenance.md

# Validation checklist
cat docs/context/templates/validation-checklist.md
```

---

## 🎓 Learning Path for New Agents

### Phase 1: Onboarding (10 minutes)
1. Read `docs/guides/LLM_ONBOARDING.md`
2. Load `docs/context/core/enforcement-rules.md`
3. Load `docs/context/core/quick-reference.md`

### Phase 2: Task-Specific Training (5-15 minutes per task)
1. Identify your task type (blog, maintenance, development)
2. Load relevant workflow module(s)
3. Load relevant standards module(s)
4. Proceed with task

### Phase 3: Advanced Mastery (optional)
1. Review `docs/context/reference/lessons-learned.md`
2. Study `docs/context/reference/edge-cases.md`
3. Explore technical modules for deep understanding

**Estimated time to productivity:**
- Basic tasks: 15 minutes
- Complex tasks: 30 minutes
- Full mastery: 2-4 hours

---

## 📊 Context Loading Recommendations

### Memory-Constrained Sessions (<100K tokens)
Load only:
- `core/enforcement-rules.md` (mandatory)
- 1-2 workflow modules (task-specific)
- Quick reference for lookups

**Total:** 8-15K tokens

### Standard Sessions (100-200K tokens)
Load:
- All core modules (~8K)
- 2-3 workflow modules (~10K)
- 1-2 standards modules (~5K)
- Quick lookups as needed

**Total:** 20-30K tokens

### Complex Sessions (>200K tokens)
Load:
- All core modules (~8K)
- All relevant workflow modules (~20K)
- All relevant standards modules (~12K)
- Technical modules as needed (~10K)
- Reference modules for lookup (~10K)

**Total:** 40-60K tokens (still 25-40% less than current CLAUDE.md)

---

## 🔗 Cross-References

### External Documentation
- **Standards Submodule**: https://github.com/williamzujkowski/standards
- **Eleventy Docs**: https://www.11ty.dev/docs/
- **Tailwind Docs**: https://tailwindcss.com/docs

### Internal Documentation
- **Architecture**: `docs/ARCHITECTURE.md`
- **Script Catalog**: `docs/guides/SCRIPT_CATALOG.md`
- **Enforcement**: `docs/ENFORCEMENT.md`

### Context System
- **Master Index**: `docs/context/INDEX.yaml`
- **Module Template**: `docs/context/templates/module-template.md`

---

## 📝 Version History

### Version 4.0.0 (2025-11-01)
- **BREAKING**: Restructured to progressive context loading
- Moved 80% of content to `docs/context/` modules
- Created module index and navigation system
- Established loading patterns and recommendations

### Version 3.0.0 (2025-09-23)
- Added humanization v2.0 validator
- Enhanced citation requirements
- Established Smart Brevity methodology

### Version 2.0.0 (2025-08-15)
- Added enforcement rules
- Established compliance standards
- Integrated SPARC methodology

### Version 1.0.0 (2025-06-01)
- Initial monolithic structure
- Basic blog guidelines
- Core workflows

---

## 🆘 Support & Troubleshooting

### Module Not Loading?
- Check path in `docs/context/INDEX.yaml`
- Verify file exists: `ls docs/context/[category]/[module].md`
- Check MANIFEST.json for file registry entry

### Unclear Which Module to Load?
- Start with `docs/context/INDEX.yaml` for full map
- Check "Common Task → Context Loading Patterns" above
- Load `core/quick-reference.md` for guidance

### Module Content Outdated?
- Check version in module frontmatter
- Compare with `docs/context/INDEX.yaml` version
- Report to repository maintainer

### Need Help?
- Review `docs/guides/LLM_ONBOARDING.md`
- Check `docs/context/reference/edge-cases.md`
- Load `docs/context/core/quick-reference.md`

---

**Remember:** This is a **policy anchor**, not a comprehensive guide. Load context modules progressively based on your task requirements.

**Master Index:** `docs/context/INDEX.yaml`

**Questions?** Start with `docs/guides/LLM_ONBOARDING.md`
```

---

## 3. Module Template

### Standard Template for Context Modules

```markdown
---
title: [Module Title]
category: [core|workflows|standards|technical|reference|templates]
priority: [HIGH|MEDIUM|LOW]
version: 1.0.0
last_updated: YYYY-MM-DD
status: [ACTIVE|DRAFT|DEPRECATED|ARCHIVED]
dependencies: [List other modules required]
estimated_tokens: [Approximate size]
tags: [keyword1, keyword2, keyword3]
---

# [Module Title]

## Module Metadata

**Category:** [core|workflows|standards|technical|reference|templates]
**Priority:** [HIGH|MEDIUM|LOW]
**Load When:** [Brief description of when to load this module]
**Dependencies:** [List prerequisite modules]
**Estimated Size:** ~[X]K tokens

---

## Purpose

[1-2 sentences describing what this module covers and why it exists]

---

## When to Load This Module

**Load this module when:**
- [Scenario 1]
- [Scenario 2]
- [Scenario 3]

**Skip this module if:**
- [Scenario where not needed]
- [Alternative module to use instead]

---

## Quick Reference

[2-5 bullet points of most critical information]

---

## Content

[Main content of the module - extracted from current CLAUDE.md]

### Section 1
[Content]

### Section 2
[Content]

---

## Cross-References

### Related Modules
- [Module Name 1](../category/module-name.md) - [Why related]
- [Module Name 2](../category/module-name.md) - [Why related]

### External References
- [Doc Name](https://url) - [What it covers]
- [Resource Name](https://url) - [Why relevant]

---

## Examples

### Example 1: [Use Case]
```bash
# Command or code example
```

**Explanation:** [What this example demonstrates]

### Example 2: [Use Case]
```markdown
<!-- Template or pattern example -->
```

**Explanation:** [What this example demonstrates]

---

## Common Pitfalls

### Pitfall 1: [Description]
**Problem:** [What goes wrong]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

### Pitfall 2: [Description]
**Problem:** [What goes wrong]
**Solution:** [How to fix it]
**Prevention:** [How to avoid it]

---

## Validation

### How to Verify Compliance

**Checklist:**
- [ ] [Validation point 1]
- [ ] [Validation point 2]
- [ ] [Validation point 3]

**Commands:**
```bash
# Validation command 1
# Validation command 2
```

---

## Changelog

### Version 1.0.0 (YYYY-MM-DD)
- Initial creation from CLAUDE.md section [X]
- [Other changes]

---

## Maintenance Notes

**Review Schedule:** [Monthly|Quarterly|Yearly|As-needed]
**Last Review:** YYYY-MM-DD
**Next Review:** YYYY-MM-DD
**Maintainer:** [Role or person]

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
```

---

## 4. Topic Split Strategy

### Mapping Current CLAUDE.md to Modules

#### HIGH Priority → `core/` (Load First)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| §59-83: MANDATORY ENFORCEMENT NOTICE | `core/enforcement-rules.md` | Absolute requirements before any op |
| §337-396: File Management Rules | `core/file-management.md` | Prevents duplicate files, wrong dirs |
| §344-376: Concurrent Execution | `core/concurrent-execution.md` | Critical for efficient operations |
| §26-57: Current Compliance Status | `core/compliance-status.md` | Dashboard of current state |
| Top commands from multiple sections | `core/quick-reference.md` | Most-used patterns |

**Total core:** ~8K tokens (load all or most for comprehensive work)

---

#### MEDIUM Priority → `workflows/` (Load As Needed)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| §700-850: Blog Post Creation Guidelines | `workflows/blog-post-creation.md` | Complete new post workflow |
| §900-1100: Smart Brevity Methodology | `workflows/blog-transformation.md` | 7-phase transformation |
| §1200-1600: Humanization Standards | `workflows/humanization.md` | v2.0 validation system |
| §640-699: Research & Credibility Model | `workflows/research-citations.md` | Citation requirements |
| §2709-2970: Blog Image Standards | `workflows/image-management.md` | Image workflow & automation |
| §2502-2665: GitHub Gist Management | `workflows/gist-management.md` | Code extraction workflow |
| §353-376: Cleanup Phase | `workflows/cleanup-maintenance.md` | Mandatory cleanup protocols |

**Per-workflow:** 2-5K tokens (load only what you need for current task)

---

#### MEDIUM Priority → `standards/` (Reference As Needed)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| §500-638: Content Style Guidelines | `standards/writing-style.md` | "Polite Linus" voice |
| §1650-1850: Personal & Family Info + NDA | `standards/content-boundaries.md` | What NOT to share |
| §640-699: Research Verification | `standards/research-verification.md` | Fact-checking protocols |
| §2829-2861: Accessibility Standards | `standards/accessibility.md` | WCAG & mobile requirements |
| §451-457: Code Style & Best Practices | `standards/code-style.md` | Modular design, DRY, tests |

**Per-standard:** 2-3K tokens (load relevant standards only)

---

#### LOW Priority → `technical/` (Load Rarely)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| §182-336: Project Directory Structure | `technical/directory-structure.md` | Project layout details |
| §308-335: Build Commands | `technical/build-commands.md` | npm scripts reference |
| §423-557: SPARC Commands + Agent Coordination | `technical/sparc-nexus-agents.md` | SPARC methodology |
| §459-556: Available Agents + MCP Tools | `technical/agent-coordination.md` | Multi-agent orchestration |
| §587-630: Performance Benefits + Hooks | `technical/performance-hooks.md` | Optimization patterns |

**Per-technical:** 1.5-3K tokens (rarely needed for most tasks)

---

#### LOW Priority → `reference/` (Lookup Only)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| §234-283: Script Organization Catalog | `reference/script-catalog.md` | All 37 scripts (link to SCRIPT_CATALOG.md) |
| §151-179: Lessons from Enhancement Missions | `reference/lessons-learned.md` | Historical insights |
| §103-130: Documentation Retention Policy | `reference/batch-reports.md` | Archive strategy + reports |
| §2278-2417: Edge Case Quick Reference | `reference/edge-cases.md` | Special scenarios |

**Per-reference:** 2-6K tokens (load for lookup only)

---

#### LOW Priority → `templates/` (Copy As Needed)

| Current Section | Target Module | Rationale |
|----------------|---------------|-----------|
| Extracted from blog creation section | `templates/blog-post-template.md` | Starter template |
| Extracted from validation sections | `templates/validation-checklist.md` | Pre-publish checklist |
| This design document | `templates/module-template.md` | Creating new modules |

**Per-template:** 0.5-1K tokens (minimal)

---

### Content That Stays in Main CLAUDE.md

**Keep in main file (<10K tokens total):**

1. **Authoritative Notice** (§10-24): Policy anchor statement
2. **Enforcement Notice** (§59-83): Critical rules (summarized, link to full)
3. **Compliance Dashboard** (§26-57): Current metrics (summarized)
4. **Context Module Index** (NEW): Tables linking to all modules
5. **Common Task Patterns** (NEW): Quick "load this for X task" guide
6. **Documentation Hierarchy** (§132-149): Shows relationship
7. **Quick Start Commands** (NEW): For new/experienced LLMs
8. **Version History** (NEW): Track major changes
9. **Support** (NEW): Where to go for help

**Total:** ~8K tokens (82% reduction from current ~45K in affected sections)

---

## 5. Index Schema

### `docs/context/INDEX.yaml` Format

```yaml
version: 1.0.0
last_updated: 2025-11-01
schema_version: 1.0.0
description: Master index of progressive context modules

# Metadata about the context system
system:
  total_modules: 30
  total_estimated_tokens: 75000
  average_module_size: 2500
  categories:
    - core
    - workflows
    - standards
    - technical
    - reference
    - templates

# Core modules (HIGH priority - load first)
core:
  - name: enforcement-rules
    title: "Mandatory Enforcement Rules"
    path: docs/context/core/enforcement-rules.md
    version: 1.0.0
    priority: HIGH
    estimated_tokens: 2000
    load_when:
      - "Before ANY operation"
      - "First load in new session"
    dependencies: []
    tags:
      - mandatory
      - enforcement
      - rules
      - penalties
      - file-operations
    summary: "Critical rules that MUST be followed. Violations will be blocked."

  - name: file-management
    title: "File Management & Organization"
    path: docs/context/core/file-management.md
    version: 1.0.0
    priority: HIGH
    estimated_tokens: 1500
    load_when:
      - "Creating new files"
      - "Moving/renaming files"
      - "Organizing content"
    dependencies:
      - enforcement-rules
    tags:
      - files
      - directories
      - organization
      - manifest
      - duplication
    summary: "Rules for file operations, directory structure, and avoiding duplicates."

  - name: concurrent-execution
    title: "Concurrent Execution & Batch Operations"
    path: docs/context/core/concurrent-execution.md
    version: 1.0.0
    priority: HIGH
    estimated_tokens: 1500
    load_when:
      - "Multi-step operations"
      - "Batch processing"
      - "Performance optimization"
    dependencies:
      - enforcement-rules
    tags:
      - concurrent
      - parallel
      - batch
      - performance
      - one-message-rule
    summary: "Patterns for parallel execution and batch operations (2.8-4.4x faster)."

  - name: compliance-status
    title: "Current Compliance Status Dashboard"
    path: docs/context/core/compliance-status.md
    version: 1.0.0
    priority: HIGH
    estimated_tokens: 1000
    load_when:
      - "Status checks"
      - "Before starting work"
      - "Health verification"
    dependencies: []
    tags:
      - compliance
      - metrics
      - dashboard
      - status
      - health
    summary: "Current repository health metrics and compliance dashboard."

  - name: quick-reference
    title: "Quick Reference Guide"
    path: docs/context/core/quick-reference.md
    version: 1.0.0
    priority: HIGH
    estimated_tokens: 2000
    load_when:
      - "Quick lookups"
      - "Common commands"
      - "Frequently used patterns"
    dependencies: []
    tags:
      - reference
      - commands
      - quick-start
      - cheatsheet
    summary: "Most-used commands and patterns for quick reference."

# Workflow modules (MEDIUM priority - load as needed)
workflows:
  - name: blog-post-creation
    title: "Blog Post Creation Workflow"
    path: docs/context/workflows/blog-post-creation.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 4000
    load_when:
      - "Creating new blog posts"
      - "Need complete post workflow"
    dependencies:
      - enforcement-rules
      - file-management
      - writing-style
    tags:
      - blog
      - creation
      - workflow
      - posts
      - frontmatter
    summary: "Complete workflow for creating new blog posts from scratch."

  - name: blog-transformation
    title: "Smart Brevity Blog Transformation"
    path: docs/context/workflows/blog-transformation.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 3000
    load_when:
      - "Refining existing posts"
      - "Smart Brevity transformation"
      - "7-phase methodology"
    dependencies:
      - enforcement-rules
      - humanization
      - research-citations
    tags:
      - blog
      - transformation
      - smart-brevity
      - refinement
      - BLUF
    summary: "7-phase Smart Brevity methodology for transforming existing posts."

  - name: humanization
    title: "Humanization Standards & Validation"
    path: docs/context/workflows/humanization.md
    version: 2.0.0
    priority: MEDIUM
    estimated_tokens: 5000
    load_when:
      - "Validating content tone"
      - "Humanizing AI-generated text"
      - "Pre-commit validation"
    dependencies:
      - enforcement-rules
    tags:
      - humanization
      - validation
      - tone
      - AI-tells
      - scoring
    summary: "v2.0 humanization validator with 155x faster batch processing."

  - name: research-citations
    title: "Research & Citation Standards"
    path: docs/context/workflows/research-citations.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 3000
    load_when:
      - "Adding sources to posts"
      - "Verifying claims"
      - "Research validation"
    dependencies:
      - enforcement-rules
    tags:
      - research
      - citations
      - sources
      - verification
      - academic
    summary: "Citation requirements, research verification, and academic sources."

  - name: image-management
    title: "Blog Image Management Workflow"
    path: docs/context/workflows/image-management.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 3000
    load_when:
      - "Working with blog images"
      - "Hero image generation"
      - "Image optimization"
    dependencies:
      - enforcement-rules
      - file-management
    tags:
      - images
      - hero-images
      - optimization
      - alt-text
      - accessibility
    summary: "Complete image workflow: generation, optimization, metadata."

  - name: gist-management
    title: "GitHub Gist Management Workflow"
    path: docs/context/workflows/gist-management.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 2000
    load_when:
      - "Extracting code to gists"
      - "Managing code examples"
      - "Reducing code ratio"
    dependencies:
      - enforcement-rules
    tags:
      - gist
      - github
      - code-extraction
      - code-ratio
    summary: "Workflow for extracting blog code to GitHub gists."

  - name: cleanup-maintenance
    title: "Cleanup & Maintenance Protocols"
    path: docs/context/workflows/cleanup-maintenance.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 2000
    load_when:
      - "Repository cleanup"
      - "Maintenance tasks"
      - "Removing vestigial content"
    dependencies:
      - enforcement-rules
      - file-management
    tags:
      - cleanup
      - maintenance
      - vestigial
      - archive
      - retention
    summary: "Mandatory cleanup protocols and retention policies."

# Standards modules (MEDIUM priority - reference as needed)
standards:
  - name: writing-style
    title: "Writing Style Guide (Polite Linus)"
    path: docs/context/standards/writing-style.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 3000
    load_when:
      - "Writing blog content"
      - "Reviewing voice/tone"
      - "Content creation"
    dependencies: []
    tags:
      - writing
      - style
      - voice
      - tone
      - smart-brevity
    summary: "Polite Linus voice, Smart Brevity principles, sentence rhythm."

  - name: content-boundaries
    title: "Content Boundaries & NDA Compliance"
    path: docs/context/standards/content-boundaries.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 2000
    load_when:
      - "Reviewing sensitive topics"
      - "Ensuring NDA compliance"
      - "Work/personal boundaries"
    dependencies: []
    tags:
      - NDA
      - compliance
      - boundaries
      - work
      - personal
    summary: "What NOT to share: work references, NDA violations, personal limits."

  - name: research-verification
    title: "Research Verification Protocols"
    path: docs/context/standards/research-verification.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 3000
    load_when:
      - "Validating factual claims"
      - "Finding reputable sources"
      - "Fact-checking"
    dependencies: []
    tags:
      - research
      - verification
      - fact-checking
      - sources
      - credibility
    summary: "NO FABRICATION rule, source validation, Playwright verification."

  - name: accessibility
    title: "Accessibility & Mobile Standards"
    path: docs/context/standards/accessibility.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 2000
    load_when:
      - "UI/UX work"
      - "Image alt text"
      - "Mobile responsiveness"
    dependencies: []
    tags:
      - accessibility
      - WCAG
      - mobile
      - alt-text
      - responsive
    summary: "WCAG AA standards, mobile testing, touch targets, alt text."

  - name: code-style
    title: "Code Style & Best Practices"
    path: docs/context/standards/code-style.md
    version: 1.0.0
    priority: MEDIUM
    estimated_tokens: 2000
    load_when:
      - "Writing code/scripts"
      - "Code review"
      - "Architecture decisions"
    dependencies: []
    tags:
      - code
      - style
      - best-practices
      - DRY
      - SOLID
    summary: "Modular design, test-first, clean architecture, documentation."

# Technical modules (LOW priority - load rarely)
technical:
  - name: directory-structure
    title: "Project Directory Structure"
    path: docs/context/technical/directory-structure.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 2000
    load_when:
      - "Navigation questions"
      - "Project layout queries"
      - "Understanding organization"
    dependencies: []
    tags:
      - directory
      - structure
      - organization
      - layout
    summary: "Complete project directory layout and organization."

  - name: build-commands
    title: "Build Commands & npm Scripts"
    path: docs/context/technical/build-commands.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 1500
    load_when:
      - "Build/deploy issues"
      - "npm script questions"
      - "Tooling setup"
    dependencies: []
    tags:
      - build
      - npm
      - scripts
      - deploy
      - tooling
    summary: "All npm scripts: build, test, validate, debug."

  - name: sparc-nexus-agents
    title: "SPARC Methodology & Claude-Flow"
    path: docs/context/technical/sparc-nexus-agents.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 3000
    load_when:
      - "Development workflows"
      - "SPARC questions"
      - "Claude-Flow setup"
    dependencies: []
    tags:
      - SPARC
      - nexus-agents
      - methodology
      - TDD
      - workflow
    summary: "SPARC phases, Claude-Flow commands, TDD workflow."

  - name: agent-coordination
    title: "Agent Coordination & MCP Tools"
    path: docs/context/technical/agent-coordination.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 2000
    load_when:
      - "Multi-agent tasks"
      - "MCP tool questions"
      - "Swarm orchestration"
    dependencies: []
    tags:
      - agents
      - MCP
      - coordination
      - swarm
      - orchestration
    summary: "54 agents, MCP tools, coordination protocols, swarm patterns."

  - name: performance-hooks
    title: "Performance Optimization & Hooks"
    path: docs/context/technical/performance-hooks.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 1500
    load_when:
      - "Performance tuning"
      - "Hook integration"
      - "Optimization questions"
    dependencies: []
    tags:
      - performance
      - hooks
      - optimization
      - speed
      - efficiency
    summary: "Pre/post hooks, performance benefits, optimization patterns."

# Reference modules (LOW priority - lookup only)
reference:
  - name: script-catalog
    title: "Complete Script Catalog"
    path: docs/context/reference/script-catalog.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 6000
    load_when:
      - "Finding specific scripts"
      - "Script documentation"
      - "Automation questions"
    dependencies: []
    tags:
      - scripts
      - catalog
      - automation
      - reference
    summary: "All 37 scripts organized by category (links to SCRIPT_CATALOG.md)."

  - name: lessons-learned
    title: "Lessons Learned & Historical Insights"
    path: docs/context/reference/lessons-learned.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 3000
    load_when:
      - "Learning from past"
      - "Understanding decisions"
      - "Historical context"
    dependencies: []
    tags:
      - lessons
      - history
      - insights
      - decisions
    summary: "What worked, challenges overcome, key decisions from 6 batches."

  - name: batch-reports
    title: "Enhancement Batch Reports & Archive Strategy"
    path: docs/context/reference/batch-reports.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 2000
    load_when:
      - "Historical reporting"
      - "Archive questions"
      - "Retention policy"
    dependencies: []
    tags:
      - batches
      - reports
      - archive
      - retention
      - history
    summary: "Batch 1-6 summaries, archive locations, retention policy."

  - name: edge-cases
    title: "Edge Cases & Special Scenarios"
    path: docs/context/reference/edge-cases.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 2000
    load_when:
      - "Unusual situations"
      - "Special requirements"
      - "Exception handling"
    dependencies: []
    tags:
      - edge-cases
      - exceptions
      - special
      - scenarios
    summary: "Career/NDA posts, technical deep-dives, tutorials, security posts."

# Template modules (LOW priority - copy as needed)
templates:
  - name: blog-post-template
    title: "Blog Post Starter Template"
    path: docs/context/templates/blog-post-template.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 1000
    load_when:
      - "Creating new posts"
      - "Need starter template"
    dependencies:
      - blog-post-creation
    tags:
      - template
      - blog
      - starter
      - frontmatter
    summary: "Complete blog post template with frontmatter and structure."

  - name: validation-checklist
    title: "Pre-Publish Validation Checklist"
    path: docs/context/templates/validation-checklist.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 1000
    load_when:
      - "Before committing"
      - "Pre-publish checks"
      - "Quality validation"
    dependencies:
      - humanization
      - research-citations
    tags:
      - template
      - checklist
      - validation
      - pre-publish
    summary: "Complete pre-publish checklist for blog posts."

  - name: module-template
    title: "Context Module Template"
    path: docs/context/templates/module-template.md
    version: 1.0.0
    priority: LOW
    estimated_tokens: 500
    load_when:
      - "Creating new modules"
      - "Extending context system"
    dependencies: []
    tags:
      - template
      - module
      - meta
      - system
    summary: "Template for creating new context modules."

# Task-based loading patterns
loading_patterns:
  create_blog_post:
    name: "Create New Blog Post"
    modules:
      - enforcement-rules
      - file-management
      - blog-post-creation
      - writing-style
      - blog-post-template
    estimated_tokens: 12000

  refine_blog_post:
    name: "Refine Existing Blog Post"
    modules:
      - enforcement-rules
      - blog-transformation
      - humanization
      - research-citations
    estimated_tokens: 13000

  validate_content:
    name: "Validate Content Quality"
    modules:
      - enforcement-rules
      - humanization
      - validation-checklist
    estimated_tokens: 7500

  maintenance_cleanup:
    name: "Maintenance & Cleanup"
    modules:
      - enforcement-rules
      - file-management
      - cleanup-maintenance
    estimated_tokens: 5500

  script_development:
    name: "Script Development/Troubleshooting"
    modules:
      - enforcement-rules
      - directory-structure
      - script-catalog
      - code-style
    estimated_tokens: 11500

# Discovery keywords (for searching)
keywords:
  enforcement:
    - mandatory
    - rules
    - violations
    - penalties
    - blocking
    modules:
      - enforcement-rules
      - file-management

  blog:
    - posts
    - writing
    - content
    - creation
    - transformation
    modules:
      - blog-post-creation
      - blog-transformation
      - writing-style

  validation:
    - humanization
    - scoring
    - checks
    - quality
    - compliance
    modules:
      - humanization
      - validation-checklist
      - compliance-status

  research:
    - citations
    - sources
    - verification
    - academic
    - facts
    modules:
      - research-citations
      - research-verification

  images:
    - hero
    - optimization
    - alt-text
    - accessibility
    modules:
      - image-management
      - accessibility

  code:
    - gist
    - extraction
    - scripts
    - development
    modules:
      - gist-management
      - script-catalog
      - code-style

  cleanup:
    - maintenance
    - archive
    - retention
    - vestigial
    modules:
      - cleanup-maintenance
      - batch-reports
```

---

## 6. Migration Plan

### Step-by-Step Migration from Monolithic to Progressive

#### Phase 1: Setup (1 hour)

**Step 1.1: Create Directory Structure**
```bash
cd /home/william/git/williamzujkowski.github.io

# Create context module structure
mkdir -p docs/context/{core,workflows,standards,technical,reference,templates}

# Verify creation
tree docs/context -L 2
```

**Step 1.2: Create INDEX.yaml**
```bash
# Copy provided INDEX.yaml schema
cat > docs/context/INDEX.yaml << 'EOF'
[Paste INDEX.yaml content from section 5]
EOF

# Validate YAML syntax
python -c "import yaml; yaml.safe_load(open('docs/context/INDEX.yaml'))"
```

**Step 1.3: Create Module Template**
```bash
# Copy module template
cat > docs/context/templates/module-template.md << 'EOF'
[Paste module template content from section 3]
EOF
```

---

#### Phase 2: Extract Core Modules (2 hours)

**Priority: These modules are loaded first in every session**

**Step 2.1: Extract enforcement-rules.md**
```bash
# Create core/enforcement-rules.md
# Extract from CLAUDE.md §59-83 + detailed rules from ENFORCEMENT.md
vim docs/context/core/enforcement-rules.md
```

**Content to extract:**
- §59-83: MANDATORY ENFORCEMENT NOTICE
- All rules from `.claude-rules.json`
- File operation rules (CREATE, UPDATE, DELETE)
- Penalties and violations
- Validation gates

**Step 2.2: Extract file-management.md**
```bash
# Create core/file-management.md
# Extract from CLAUDE.md §337-396
vim docs/context/core/file-management.md
```

**Content to extract:**
- §377-396: File Organization Rules
- Directory structure rules
- MANIFEST.json update requirements
- Duplicate file prevention
- Root folder prohibition

**Step 2.3: Extract concurrent-execution.md**
```bash
# Create core/concurrent-execution.md
# Extract from CLAUDE.md §344-376, §557-585
vim docs/context/core/concurrent-execution.md
```

**Content to extract:**
- §344-351: GOLDEN RULE: "1 MESSAGE = ALL RELATED OPERATIONS"
- §557-585: Concurrent Execution Examples
- Batch operation patterns
- Performance benefits (2.8-4.4x faster)

**Step 2.4: Extract compliance-status.md**
```bash
# Create core/compliance-status.md
# Extract from CLAUDE.md §26-57
vim docs/context/core/compliance-status.md
```

**Content to extract:**
- §26-57: Current Compliance Status (all metrics)
- Dashboard format
- Update mechanisms

**Step 2.5: Extract quick-reference.md**
```bash
# Create core/quick-reference.md
# Extract most-used commands from multiple sections
vim docs/context/core/quick-reference.md
```

**Content to extract:**
- Top 10 commands from various sections
- Common patterns
- Quick troubleshooting
- Emergency procedures

**Validation:**
```bash
# Verify all core modules created
ls -lh docs/context/core/

# Should show:
# enforcement-rules.md (~2K words)
# file-management.md (~1.5K words)
# concurrent-execution.md (~1.5K words)
# compliance-status.md (~1K words)
# quick-reference.md (~2K words)
```

---

#### Phase 3: Extract Workflow Modules (3 hours)

**Priority: Load these based on current task**

**Step 3.1: Extract blog-post-creation.md**
```bash
# Create workflows/blog-post-creation.md
# Extract from CLAUDE.md §700-850
vim docs/context/workflows/blog-post-creation.md
```

**Content to extract:**
- Complete blog post creation guidelines
- Minimum standards
- Target audience
- Topic diversity requirements
- Structure (5 parts)
- Content requirements
- Metadata and SEO

**Step 3.2: Extract blog-transformation.md**
```bash
# Create workflows/blog-transformation.md
# Extract from CLAUDE.md §900-1100
vim docs/context/workflows/blog-transformation.md
```

**Content to extract:**
- Smart Brevity methodology overview
- 7 phases (A-G) with examples
- Batch 2 results table
- Swarm orchestration pattern
- Success patterns & pitfalls

**Step 3.3: Extract humanization.md**
```bash
# Create workflows/humanization.md
# Extract from CLAUDE.md §1200-1600
vim docs/context/workflows/humanization.md
```

**Content to extract:**
- Humanization v2.0 overview
- 7-phase framework (condensed)
- Validator commands
- Scoring tiers
- Pre-commit enforcement
- Edge cases

**Step 3.4: Extract research-citations.md**
```bash
# Create workflows/research-citations.md
# Extract from CLAUDE.md §640-699
vim docs/context/workflows/research-citations.md
```

**Content to extract:**
- ABSOLUTE RULE: NO FABRICATION
- Research verification process
- Open-access research platforms
- Research integration workflow
- Citation format (with hyperlinks)
- Pre-publication checklist

**Step 3.5: Extract image-management.md**
```bash
# Create workflows/image-management.md
# Extract from CLAUDE.md §2709-2970
vim docs/context/workflows/image-management.md
```

**Content to extract:**
- Image Management System
- Directory structure
- Image requirements (hero, inline, responsive)
- Automation scripts (3 scripts)
- Workflow for new/existing posts
- Accessibility standards
- Optimization

**Step 3.6: Extract gist-management.md**
```bash
# Create workflows/gist-management.md
# Extract from CLAUDE.md §2502-2665
vim docs/context/workflows/gist-management.md
```

**Content to extract:**
- GitHub Gist Management overview
- When to extract code
- Complete gist workflow (Phase 8.5 + 8.6)
- Gist file format standards
- Gist mapping file
- Maintenance & troubleshooting

**Step 3.7: Extract cleanup-maintenance.md**
```bash
# Create workflows/cleanup-maintenance.md
# Extract from CLAUDE.md §353-376
vim docs/context/workflows/cleanup-maintenance.md
```

**Content to extract:**
- CLEANUP PHASE: MANDATORY FOR ALL WORKFLOWS
- Cleanup targets
- Cleanup rules
- Retention policy (§103-130)
- Archive locations

**Validation:**
```bash
# Verify all workflow modules created
ls -lh docs/context/workflows/

# Should show 7 workflow modules
wc -w docs/context/workflows/*.md
```

---

#### Phase 4: Extract Standards Modules (2 hours)

**Step 4.1: Extract writing-style.md**
```bash
# Create standards/writing-style.md
# Extract from CLAUDE.md §500-638
vim docs/context/standards/writing-style.md
```

**Content to extract:**
- "Polite Linus Torvalds" Standard
- Core principles (lead with point, bullets, cut ruthlessly)
- "Why it matters" sections
- Sentence rhythm and cadence
- Anti-AI-Tells checklist
- Voice guidelines

**Step 4.2: Extract content-boundaries.md**
```bash
# Create standards/content-boundaries.md
# Extract from CLAUDE.md §1650-1850
vim docs/context/standards/content-boundaries.md
```

**Content to extract:**
- Government Work Security Guidelines
- NEVER discuss list
- ALWAYS use patterns
- Safe/unsafe examples
- Personal & family information
- Privacy protection

**Step 4.3: Extract research-verification.md**
```bash
# Create standards/research-verification.md
# Extract from CLAUDE.md §640-699 (detailed verification)
vim docs/context/standards/research-verification.md
```

**Content to extract:**
- NO FABRICATION rule
- Research verification process
- Open-access platforms (detailed)
- Playwright research automation
- Red flags to avoid
- Pre-publication checklist

**Step 4.4: Extract accessibility.md**
```bash
# Create standards/accessibility.md
# Extract from CLAUDE.md §2829-2861
vim docs/context/standards/accessibility.md
```

**Content to extract:**
- Alt text requirements
- WCAG standards
- Mobile responsiveness
- Touch targets
- Keyboard navigation
- Testing procedures

**Step 4.5: Extract code-style.md**
```bash
# Create standards/code-style.md
# Extract from CLAUDE.md §451-457
vim docs/context/standards/code-style.md
```

**Content to extract:**
- Modular Design: Files under 500 lines
- Environment Safety: Never hardcode secrets
- Test-First: Write tests before implementation
- Clean Architecture: Separate concerns
- Documentation: Keep updated
- DRY and SOLID principles

**Validation:**
```bash
# Verify all standards modules created
ls -lh docs/context/standards/

# Should show 5 standards modules
```

---

#### Phase 5: Extract Technical Modules (1.5 hours)

**Step 5.1: Extract directory-structure.md**
```bash
# Create technical/directory-structure.md
# Extract from CLAUDE.md §182-336
vim docs/context/technical/directory-structure.md
```

**Content to extract:**
- Root Directory structure diagram
- Key Directories Explained (src/, scripts/, docs/, _site/)
- Script Organization (Post-Phase 3 Cleanup)
- Configuration Files table

**Step 5.2: Extract build-commands.md**
```bash
# Create technical/build-commands.md
# Extract from CLAUDE.md §308-335
vim docs/context/technical/build-commands.md
```

**Content to extract:**
- Build Commands (Development, Production, Testing, Validation, Debugging)
- All npm scripts with descriptions

**Step 5.3: Extract sparc-nexus-agents.md**
```bash
# Create technical/sparc-nexus-agents.md
# Extract from CLAUDE.md §423-557
vim docs/context/technical/sparc-nexus-agents.md
```

**Content to extract:**
- SPARC Commands (Core, Batchtools, npm)
- SPARC Workflow Phases (5 phases)
- Quick Setup commands

**Step 5.4: Extract agent-coordination.md**
```bash
# Create technical/agent-coordination.md
# Extract from CLAUDE.md §459-556
vim docs/context/technical/agent-coordination.md
```

**Content to extract:**
- Available Agents (54 Total) by category
- Agent Coordination Protocol (Before/During/After work)
- Claude Code vs MCP Tools
- MCP Tool Categories

**Step 5.5: Extract performance-hooks.md**
```bash
# Create technical/performance-hooks.md
# Extract from CLAUDE.md §587-630
vim docs/context/technical/performance-hooks.md
```

**Content to extract:**
- Performance Benefits (84.8% solve rate, 32.3% token reduction)
- Hooks Integration (Pre/Post/Session)
- Advanced Features v2.0.0

**Validation:**
```bash
# Verify all technical modules created
ls -lh docs/context/technical/

# Should show 5 technical modules
```

---

#### Phase 6: Extract Reference Modules (1 hour)

**Step 6.1: Extract script-catalog.md**
```bash
# Create reference/script-catalog.md
# Link to existing docs/guides/SCRIPT_CATALOG.md
vim docs/context/reference/script-catalog.md
```

**Content:**
```markdown
# Complete Script Catalog

**See:** [docs/guides/SCRIPT_CATALOG.md](../../guides/SCRIPT_CATALOG.md)

This module provides a link to the comprehensive script catalog...
[Include summary and links]
```

**Step 6.2: Extract lessons-learned.md**
```bash
# Create reference/lessons-learned.md
# Extract from CLAUDE.md §151-179
vim docs/context/reference/lessons-learned.md
```

**Content to extract:**
- What Worked Well (8 items)
- Challenges Overcome (8 items)
- Key Decisions (5 items)

**Step 6.3: Extract batch-reports.md**
```bash
# Create reference/batch-reports.md
# Extract from CLAUDE.md §103-130
vim docs/context/reference/batch-reports.md
```

**Content to extract:**
- Documentation Retention Policy
- Archive Locations (Q3 2025, Q4 2025)
- Links to batch completion reports

**Step 6.4: Extract edge-cases.md**
```bash
# Create reference/edge-cases.md
# Extract from CLAUDE.md §2278-2417
vim docs/context/reference/edge-cases.md
```

**Content to extract:**
- Career/NDA-Sensitive Posts
- Technical Deep-Dives
- Tutorial/How-To Posts
- Security/Vulnerability Posts
- Meta/Process Posts

**Validation:**
```bash
# Verify all reference modules created
ls -lh docs/context/reference/

# Should show 4 reference modules
```

---

#### Phase 7: Create Templates (30 minutes)

**Step 7.1: Extract blog-post-template.md**
```bash
# Create templates/blog-post-template.md
# Extract from blog creation section
vim docs/context/templates/blog-post-template.md
```

**Content:**
Complete blog post template with frontmatter and structure.

**Step 7.2: Extract validation-checklist.md**
```bash
# Create templates/validation-checklist.md
# Extract from validation sections
vim docs/context/templates/validation-checklist.md
```

**Content:**
Complete pre-publish checklist for blog posts.

**Step 7.3: Module template already created**
```bash
# Verify module-template.md exists from Phase 1
ls -lh docs/context/templates/module-template.md
```

**Validation:**
```bash
# Verify all templates created
ls -lh docs/context/templates/

# Should show 3 templates
```

---

#### Phase 8: Create New CLAUDE.md (2 hours)

**Step 8.1: Backup Current CLAUDE.md**
```bash
cp CLAUDE.md CLAUDE.md.v3.0.0.backup.$(date +%Y%m%d)
```

**Step 8.2: Create New CLAUDE.md**
```bash
# Use provided structure from section 2
vim CLAUDE.md
```

**Paste the new lightweight CLAUDE.md structure from section 2.**

**Step 8.3: Validate New Structure**
```bash
# Check word count (<2,000 target)
wc -w CLAUDE.md

# Should be ~1,800-2,000 words (~10K tokens)

# Compare with old
wc -w CLAUDE.md.v3.0.0.backup.*

# Old: ~12,900 words
# New: ~1,900 words
# Reduction: 85%
```

---

#### Phase 9: Update MANIFEST.json (30 minutes)

**Step 9.1: Add All New Module Files**
```bash
# Update MANIFEST.json to include all new context modules
python scripts/update-manifest.py
```

**Step 9.2: Verify File Registry**
```bash
# Check that all module files are registered
jq '.inventory.files.by_type.md' MANIFEST.json | grep "docs/context"
```

**Step 9.3: Update Last Validated Timestamp**
```bash
# Use time.gov or system time
# Update last_validated field in MANIFEST.json
```

---

#### Phase 10: Validation & Testing (1 hour)

**Step 10.1: Build Test**
```bash
# Ensure site still builds
npm run build

# Should pass without errors
```

**Step 10.2: Link Validation**
```bash
# Validate all internal links in new CLAUDE.md
python scripts/link-validation/link-validator.py --file CLAUDE.md

# Should have 0 broken links
```

**Step 10.3: Context Module Validation**
```bash
# Validate INDEX.yaml syntax
python -c "import yaml; yaml.safe_load(open('docs/context/INDEX.yaml'))"

# Validate all module files exist
python scripts/validate-context-modules.py
```

**Step 10.4: Test Loading Patterns**
```bash
# Test common task patterns manually
# Example: Create new blog post
cat docs/context/core/enforcement-rules.md
cat docs/context/core/file-management.md
cat docs/context/workflows/blog-post-creation.md
cat docs/context/standards/writing-style.md
cat docs/context/templates/blog-post-template.md

# Verify you can load 5 modules for complete workflow
```

**Step 10.5: Knowledge Management Validation**
```bash
# Run KM standards validation
npm run validate:km

# Should pass
```

---

#### Phase 11: Documentation & Commit (30 minutes)

**Step 11.1: Update References**
```bash
# Update LLM_ONBOARDING.md to reference new structure
vim docs/guides/LLM_ONBOARDING.md

# Update ENFORCEMENT.md if needed
vim docs/ENFORCEMENT.md
```

**Step 11.2: Create Migration Documentation**
```bash
# Document migration in this file
cp docs/PROGRESSIVE_CONTEXT_ARCHITECTURE.md docs/MIGRATION_TO_PROGRESSIVE_CONTEXT.md

# Add actual migration results and lessons learned
vim docs/MIGRATION_TO_PROGRESSIVE_CONTEXT.md
```

**Step 11.3: Commit Changes**
```bash
# Stage all changes
git add docs/context/
git add CLAUDE.md
git add MANIFEST.json
git add docs/PROGRESSIVE_CONTEXT_ARCHITECTURE.md

# Commit with descriptive message
git commit -m "feat: Restructure CLAUDE.md to progressive context loading system

- Reduce main CLAUDE.md from ~12,900 to ~1,900 words (85% reduction)
- Create 30 context modules across 6 categories
- Implement master INDEX.yaml for progressive loading
- Maintain complete documentation accessibility
- Enable on-demand context loading patterns

BREAKING CHANGE: CLAUDE.md structure completely redesigned.
All content preserved in docs/context/ modules."

# Push to remote
git push origin main
```

---

#### Phase 12: Post-Migration Monitoring (1 week)

**Step 12.1: Monitor Usage**
```bash
# Track which modules are loaded most frequently
# (If Claude Code provides usage metrics)
```

**Step 12.2: Gather Feedback**
```bash
# Test with real LLM sessions
# Note any:
# - Unclear navigation
# - Missing content
# - Broken links
# - Confusing organization
```

**Step 12.3: Iterate & Improve**
```bash
# Make adjustments based on feedback
# Update INDEX.yaml as needed
# Refine module content for clarity
```

**Step 12.4: Archive Old CLAUDE.md**
```bash
# After 30 days of successful operation
mv CLAUDE.md.v3.0.0.backup.* docs/archive/2025-Q4/
```

---

### Migration Time Estimate

| Phase | Duration | Cumulative |
|-------|----------|------------|
| 1. Setup | 1 hour | 1 hour |
| 2. Extract Core Modules | 2 hours | 3 hours |
| 3. Extract Workflow Modules | 3 hours | 6 hours |
| 4. Extract Standards Modules | 2 hours | 8 hours |
| 5. Extract Technical Modules | 1.5 hours | 9.5 hours |
| 6. Extract Reference Modules | 1 hour | 10.5 hours |
| 7. Create Templates | 30 min | 11 hours |
| 8. Create New CLAUDE.md | 2 hours | 13 hours |
| 9. Update MANIFEST.json | 30 min | 13.5 hours |
| 10. Validation & Testing | 1 hour | 14.5 hours |
| 11. Documentation & Commit | 30 min | 15 hours |
| 12. Post-Migration Monitoring | Ongoing | - |

**Total active migration time:** ~15 hours (2 full work days)

**Post-migration monitoring:** 1 week (passive)

---

## 7. Cleanup Targets

### Vestigial Files & Folders to Review

**After migration completes, review these for archival or deletion:**

#### Documentation Candidates

```
docs/
├── PHASE5_AUTOMATION_STRATEGY.md         # Archive to docs/archive/2025-Q3/
├── BATCH_4_EXEC_SUMMARY.md               # Archive to docs/archive/2025-Q3/
├── lighthouse-audit-summary.md           # Archive if >180 days old
├── FINAL_OPTIMIZATION_REPORT.md          # Keep or archive based on relevance
├── PHASE6_MAINTENANCE_STRATEGY.md        # Potentially superseded by cleanup-maintenance.md
```

**Decision criteria:**
- **Archive (30-180 days):** Completed batch reports, phase reports
- **Keep:** Final completion reports, lessons learned, current methodology
- **Delete (180+ days):** Intermediate reports, superseded plans

#### Old Backups in src/posts/

```
src/posts/
├── *.bak.20250920_*                      # Delete all .bak files
```

**Action:**
```bash
# Find and review all .bak files
find src/posts/ -name "*.bak.*" -ls

# Delete after verifying posts are current
find src/posts/ -name "*.bak.*" -delete
```

#### Temporary/Vestigial Scripts

**Review scripts/ for:**
- Temporary troubleshooting scripts (e.g., `validate-*.py`, `fix-*.py`, `test-*.py`)
- Duplicate or superseded scripts
- One-off analysis scripts no longer needed

**Example candidates:**
```
scripts/
├── validate-claims.py (if temporary)
├── test-citations.py (if temporary)
├── fix-links-temp.py (if temporary)
```

**Decision criteria:**
- **Keep:** Production scripts, actively used utilities
- **Delete:** Temporary troubleshooting, one-off analysis, duplicates

#### Reports/

```
reports/
├── detailed_report.csv                   # Archive or delete if >180 days
├── *.json (old reports)                  # Archive or delete if >180 days
```

**Action:** Review reports/ for outdated analysis and compliance reports.

#### Docs/archive/

**Verify archive organization:**
```bash
# Check archive structure
tree docs/archive/

# Should be organized by quarter:
docs/archive/
├── 2025-Q3/
│   ├── batch-1/
│   ├── batch-2/
│   ├── ...
│   └── batch-6/
└── 2025-Q4/
    ├── phase-8/
    └── ...
```

**Action:** Move any misplaced archived docs to correct quarter.

---

### Cleanup Script Template

```bash
#!/bin/bash
# cleanup-vestigial-content.sh
# Safely remove vestigial content after progressive context migration

set -e

echo "🧹 Cleanup Script for Vestigial Content"
echo "========================================"
echo ""

# Backup first
echo "📦 Creating backup..."
BACKUP_DIR="backups/pre-cleanup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r docs/ "$BACKUP_DIR/docs"
cp -r src/posts/*.bak.* "$BACKUP_DIR/" 2>/dev/null || true
echo "✅ Backup created at $BACKUP_DIR"
echo ""

# Find .bak files in src/posts/
echo "🔍 Finding .bak files in src/posts/..."
BAK_COUNT=$(find src/posts/ -name "*.bak.*" | wc -l)
echo "Found $BAK_COUNT .bak files"

if [ "$BAK_COUNT" -gt 0 ]; then
  echo "Preview of .bak files:"
  find src/posts/ -name "*.bak.*" -ls | head -10
  echo ""
  read -p "Delete all .bak files? (y/N) " -n 1 -r
  echo ""
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    find src/posts/ -name "*.bak.*" -delete
    echo "✅ Deleted $BAK_COUNT .bak files"
  else
    echo "⏭️  Skipped .bak file deletion"
  fi
fi
echo ""

# Archive old documentation
echo "📁 Reviewing documentation for archival..."
echo "Candidates for archive/2025-Q3/:"
ls -lh docs/PHASE*.md docs/BATCH*.md 2>/dev/null || true
echo ""
read -p "Move these to archive/2025-Q3/? (y/N) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
  mkdir -p docs/archive/2025-Q3/
  mv docs/PHASE*.md docs/archive/2025-Q3/ 2>/dev/null || true
  mv docs/BATCH*.md docs/archive/2025-Q3/ 2>/dev/null || true
  echo "✅ Moved to archive"
else
  echo "⏭️  Skipped archival"
fi
echo ""

# Update MANIFEST.json
echo "📝 Updating MANIFEST.json..."
python scripts/update-manifest.py
echo "✅ MANIFEST.json updated"
echo ""

# Validate build
echo "🔨 Validating build..."
npm run build
if [ $? -eq 0 ]; then
  echo "✅ Build passed"
else
  echo "❌ Build failed - review changes before committing"
  exit 1
fi
echo ""

echo "✨ Cleanup complete!"
echo "Review changes and commit if satisfied."
echo "Backup available at: $BACKUP_DIR"
```

**Usage:**
```bash
chmod +x scripts/cleanup-vestigial-content.sh
./scripts/cleanup-vestigial-content.sh
```

---

## 8. Decision Rationale & Trade-offs

### Key Architectural Choices

#### Decision 1: Single INDEX.yaml vs Multiple Indexes

**Choice:** Single master `INDEX.yaml` at `docs/context/`

**Rationale:**
- **Pros:**
  - Single source of truth for all modules
  - Easier to maintain (one file to update)
  - Complete system view at a glance
  - Machine-readable for automation
  - Supports discovery via keywords
- **Cons:**
  - Could become large (but YAML is compact)
  - Single point of failure (but can validate)
  - Harder to split responsibilities (not an issue for 1-2 maintainers)

**Trade-off:** Simplicity and maintainability over distributed indexes. For 30 modules, a single index is manageable and preferable.

---

#### Decision 2: 6 Categories vs More Granular

**Choice:** 6 categories (core, workflows, standards, technical, reference, templates)

**Rationale:**
- **Pros:**
  - Intuitive categorization (priority-based)
  - Aligns with usage patterns (core always, workflows often, reference rarely)
  - Not too many folders (cognitive load)
  - Clear separation of concerns
- **Cons:**
  - Some modules could fit multiple categories (e.g., humanization is both workflow and standard)
  - May need recategorization as system grows

**Trade-off:** Clear priority-based organization over perfect taxonomic categorization. Categories reflect "when to load" not just "what it is."

---

#### Decision 3: Token Estimates in Metadata

**Choice:** Include estimated_tokens in module frontmatter and INDEX.yaml

**Rationale:**
- **Pros:**
  - Helps LLMs budget context window
  - Enables informed loading decisions
  - Supports progressive disclosure strategy
- **Cons:**
  - Estimates can drift as modules evolve
  - Extra maintenance burden
  - Not always accurate (varies by LLM tokenization)

**Trade-off:** Usefulness for context management outweighs maintenance cost. Estimates are guidelines, not guarantees.

---

#### Decision 4: Keep CLAUDE.md as Policy Anchor

**Choice:** CLAUDE.md remains in root as authoritative, lightweight policy anchor

**Rationale:**
- **Pros:**
  - Maintains existing convention (LLMs expect CLAUDE.md)
  - Clear entry point for new agents
  - Policy anchor concept is well-established
  - No breaking change to file location
- **Cons:**
  - Could theoretically move everything to docs/
  - Slight redundancy with INDEX.yaml

**Trade-off:** Convention and clarity over absolute minimalism. CLAUDE.md serves as the "constitution" while modules are the "laws."

---

#### Decision 5: Module Template Standardization

**Choice:** All modules follow strict template format

**Rationale:**
- **Pros:**
  - Consistent navigation experience
  - Predictable structure for LLMs
  - Easier to maintain and update
  - Clear cross-referencing
  - Built-in validation checklist
- **Cons:**
  - Some rigidity (not all modules need all sections)
  - Extra boilerplate for small modules

**Trade-off:** Consistency and navigability over flexibility. Template sections can be omitted if not applicable, but structure is preserved.

---

#### Decision 6: Links vs Content Duplication

**Choice:** Link to existing docs (e.g., SCRIPT_CATALOG.md) rather than duplicate

**Rationale:**
- **Pros:**
  - Single source of truth (no synchronization issues)
  - Reduces redundancy
  - Smaller total repository size
- **Cons:**
  - Two-hop navigation (CLAUDE.md → module → SCRIPT_CATALOG.md)
  - Slightly less convenient

**Trade-off:** Maintainability over convenience. Links prevent divergence between modules and existing docs.

---

#### Decision 7: Progressive Disclosure vs Flatter Structure

**Choice:** Progressive disclosure (HIGH → MEDIUM → LOW priority)

**Rationale:**
- **Pros:**
  - Reduces initial context load
  - Aligns with actual usage patterns
  - Enables efficient sessions (8K vs 80K tokens)
  - Supports memory-constrained environments
- **Cons:**
  - Requires LLMs to understand priority system
  - More navigation decisions

**Trade-off:** Efficiency over simplicity. Modern LLMs can navigate indexed systems effectively.

---

#### Decision 8: YAML for Index vs JSON/Markdown

**Choice:** YAML for INDEX file

**Rationale:**
- **Pros:**
  - More human-readable than JSON
  - Comments supported
  - Compact representation
  - Machine-parseable
  - Supports hierarchical data well
- **Cons:**
  - Whitespace-sensitive (indentation matters)
  - Less universal than JSON
  - Requires YAML parser

**Trade-off:** Human-readability and structure over universal compatibility. Most LLMs can parse YAML.

---

### Anticipated Challenges & Mitigations

#### Challenge 1: LLMs Not Loading Modules

**Risk:** LLMs might continue trying to use old CLAUDE.md patterns without loading modules.

**Mitigation:**
- Clear instructions in new CLAUDE.md header
- "Module Not Found" error handling
- LLM_ONBOARDING.md emphasizes progressive loading
- Examples of common task → module loading patterns

---

#### Challenge 2: Stale Module Content

**Risk:** Modules become outdated as system evolves, creating inconsistencies.

**Mitigation:**
- Version numbers in module frontmatter
- Last_updated timestamps
- Scheduled review cycles (monthly/quarterly)
- Pre-commit hooks validate module links
- INDEX.yaml tracks dependencies

---

#### Challenge 3: Navigation Overhead

**Risk:** Loading 5 modules for a task might feel slower than scanning one big file.

**Mitigation:**
- Core modules are small (1.5-2K tokens each)
- Common task patterns pre-defined in CLAUDE.md
- Quick reference module for lookups
- Benefits (80% less initial context) outweigh navigation cost

---

#### Challenge 4: Module Categorization Disputes

**Risk:** Some content fits multiple categories (e.g., is humanization a workflow or standard?).

**Mitigation:**
- Categorize by primary use case ("when to load")
- Cross-reference related modules in each file
- INDEX.yaml keywords enable discovery across categories
- Categories can evolve with usage patterns

---

#### Challenge 5: Maintenance Burden

**Risk:** 30 files harder to maintain than 1 file.

**Mitigation:**
- Templates reduce boilerplate
- Modules are self-contained (changes localized)
- MANIFEST.json tracks all files
- Scheduled reviews identify outdated content
- Benefits (focused modules, reusability) outweigh cost

---

## 9. Success Metrics

### How to Measure Migration Success

**After 1 week:**
- [ ] All LLM sessions load modules successfully
- [ ] No broken links reported
- [ ] Build passes consistently
- [ ] New blog post created using progressive loading

**After 1 month:**
- [ ] 80% of sessions load <20K tokens context (vs 80K before)
- [ ] Module updates are easier (focused changes, not full CLAUDE.md edits)
- [ ] New context added to modules, not CLAUDE.md directly
- [ ] LLMs report improved navigation clarity

**After 3 months:**
- [ ] System scales to 40-50 modules without confusion
- [ ] Module reuse patterns emerge (e.g., humanization.md loaded in 50% of sessions)
- [ ] Token budget improvements measurable (specific % reduction)
- [ ] Community feedback (if applicable) is positive

---

## 10. Future Enhancements

### Potential Improvements After Initial Migration

#### Enhancement 1: Auto-Generated Module Index

**Idea:** Script to generate INDEX.yaml from module frontmatter

**Benefit:** Reduces manual index maintenance

**Implementation:**
```bash
python scripts/generate-context-index.py --output docs/context/INDEX.yaml
```

---

#### Enhancement 2: Module Dependency Graph

**Idea:** Visualize module dependencies with Mermaid diagram

**Benefit:** Clearer understanding of module relationships

**Implementation:**
```bash
python scripts/visualize-module-dependencies.py --output docs/context/dependency-graph.md
```

---

#### Enhancement 3: Usage Analytics

**Idea:** Track which modules are loaded most frequently

**Benefit:** Identify high-value modules, refine categorization

**Implementation:**
- Hook into LLM context loading (if possible)
- Generate monthly usage reports

---

#### Enhancement 4: Module Versioning & Changelog

**Idea:** Automated changelog generation for module updates

**Benefit:** Transparency on what changed, when, why

**Implementation:**
```bash
python scripts/generate-module-changelog.py --module enforcement-rules
```

---

#### Enhancement 5: Interactive Module Navigator

**Idea:** CLI tool to browse and load modules interactively

**Benefit:** Faster discovery for LLMs and humans

**Implementation:**
```bash
python scripts/navigate-context.py
# Interactive menu:
# 1. Core (5 modules)
# 2. Workflows (7 modules)
# ...
```

---

## 11. Conclusion

### Summary

This architecture redesigns CLAUDE.md from an ~80K token monolithic document into a progressive context loading system with:

- **85% reduction** in main file size (12,900 → 1,900 words)
- **30 focused modules** across 6 priority-based categories
- **On-demand loading** patterns reducing session context by 80-90%
- **Complete accessibility** via master INDEX.yaml and clear navigation
- **15-hour migration** with detailed step-by-step plan

**Key Benefits:**

1. **Reduced context length** - LLMs load only what they need (8-20K vs 80K tokens)
2. **Improved maintainability** - Changes localized to specific modules
3. **Better discoverability** - INDEX.yaml + keywords enable targeted search
4. **Scalability** - System easily grows to 50+ modules without confusion
5. **Backward compatibility** - CLAUDE.md remains authoritative policy anchor

**Next Steps:**

1. **Review this design** with stakeholders
2. **Approve architecture** and migration plan
3. **Execute migration** following 12-phase plan (15 hours)
4. **Monitor usage** for 1 week post-migration
5. **Iterate & improve** based on feedback

---

### Open Questions for Review

1. **Categorization:** Do the 6 categories (core, workflows, standards, technical, reference, templates) align with your mental model?

2. **Priority Levels:** Is HIGH/MEDIUM/LOW granular enough, or should we add CRITICAL/HIGH/MEDIUM/LOW/RARE?

3. **Module Size:** Target 1.5-5K tokens per module. Is this too small (many files) or too large (still chunky)?

4. **INDEX Format:** YAML chosen for human-readability. Prefer JSON for machine-parsing instead?

5. **Migration Timing:** 15-hour estimate for active migration. Does this fit your timeline?

6. **Backward Compatibility:** Should we maintain old CLAUDE.md as `CLAUDE.legacy.md` for 30 days during transition?

7. **Automation:** Which maintenance scripts would be most valuable (index generation, dependency graph, changelog)?

---

**Document Status:** DESIGN PHASE - AWAITING REVIEW

**Next Action:** Review architecture, provide feedback, approve migration

**Estimated Review Time:** 30-45 minutes

**Contact:** Strategic Planning Agent (this session)
