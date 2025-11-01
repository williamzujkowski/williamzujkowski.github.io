---
title: Mandatory Reading & Onboarding
category: core
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 800
load_when:
  - First session with this repository
  - Onboarding new AI agents
  - Understanding repository structure
  - Finding relevant documentation
dependencies: []
tags: [onboarding, documentation, reading-order, architecture]
---

# Mandatory Reading & Onboarding

## Purpose
This module provides **essential reading order** and documentation hierarchy for LLMs working on this repository. Following this reading order ensures proper understanding of enforcement rules, architecture, and available tools before beginning work.

## When to Load This Module
- **First time working with this repository** - Start here
- **Uncertain about repository structure** - Reference hierarchy
- **Looking for specific documentation** - Use reading order guide
- **Onboarding new agents** - Follow complete reading sequence

## Quick Reference

### Reading Order (5-20 minutes total)

1. **LLM_ONBOARDING.md** (5 min) - Quick start guide
2. **ENFORCEMENT.md** (5 min) - Critical rules
3. **ARCHITECTURE.md** (5 min) - System understanding
4. **SCRIPT_CATALOG.md** (as needed) - Available scripts
5. **MANIFEST.json** (reference) - Repository inventory

---

## 📚 Comprehensive Documentation

**MANDATORY READING for all LLMs working on this repository:**

1. **[docs/ENFORCEMENT.md](../../ENFORCEMENT.md)** - ⚠️ CRITICAL: Mandatory enforcement rules
2. **[docs/GUIDES/LLM_ONBOARDING.md](../../GUIDES/LLM_ONBOARDING.md)** - Quick start guide for new AI agents
3. **[docs/ARCHITECTURE.md](../../ARCHITECTURE.md)** - System architecture and design principles
4. **[docs/GUIDES/SCRIPT_CATALOG.md](../../GUIDES/SCRIPT_CATALOG.md)** - Complete catalog of available scripts
5. **[MANIFEST.json](../../../MANIFEST.json)** - Single source of truth for repository inventory

### Reading Order

1. **Start with LLM_ONBOARDING.md** (5 minutes)
   - Understand repository purpose
   - Learn basic commands
   - Get oriented to structure

2. **Read ENFORCEMENT.md** (critical rules)
   - Mandatory compliance requirements
   - Pre-commit hook behaviors
   - Validation processes

3. **Review ARCHITECTURE.md** for system understanding
   - Component relationships
   - Design principles
   - Technology stack

4. **Reference SCRIPT_CATALOG.md** as needed
   - Available automation scripts
   - Script categories and purposes
   - Usage examples

---

## 📂 Documentation Hierarchy

### Primary (Authoritative)

- **CLAUDE.md** (or modular equivalent): Master reference for all standards
- **MANIFEST.json**: System inventory and file registry
- **.claude-rules.json**: Enforcement rules

**Purpose:** Single source of truth for all standards and requirements.

### Secondary (Supporting)

- **docs/ARCHITECTURE.md**: System design
- **docs/GUIDES/**: How-to documentation
- **docs/ENFORCEMENT.md**: Mandatory rules
- **content-review-instructions.md**: Review standards

**Purpose:** Detailed implementation guidance and reference material.

### Generated (Reference)

- **reports/**: Audit and compliance reports
- **docs/STANDARDS/**: Implementation checklists

**Purpose:** Historical records and generated documentation.

> **Note**: All documentation must defer to authoritative sources for canonical requirements.

---

## Repository Quick Facts

### Project Type
Static site built with Eleventy (11ty), using SPARC methodology with Claude-Flow orchestration for Test-Driven Development.

### Key Technologies
- **Static Site Generator:** Eleventy (11ty)
- **Styling:** Tailwind CSS
- **Automation:** Python scripts + Bash utilities
- **Orchestration:** Claude-Flow MCP server
- **Testing:** Jest, Playwright
- **CI/CD:** GitHub Actions

### Important Directories

```
williamzujkowski.github.io/
├── src/                    # Source files for static site
│   ├── posts/             # Blog posts (Markdown)
│   ├── assets/            # Static assets (CSS, images, JS)
│   └── pages/             # Static pages
├── scripts/               # Automation scripts (35 Python, 2 Shell)
├── docs/                  # Documentation
│   ├── context/          # Progressive context loading modules
│   ├── GUIDES/           # How-to guides
│   └── archive/          # Historical documentation
├── tests/                 # Test files
└── _site/                # Build output (git-ignored)
```

### Core Commands

```bash
# Development
npm run serve              # Dev server with hot reload
npm run build              # Build production site

# Testing
npm run test:all           # Run all test suites
npm run validate:km        # Validate knowledge management

# Scripts
python scripts/blog-content/humanization-validator.py  # Validate blog posts
bash scripts/optimize-blog-images.sh                   # Optimize images
```

---

## Cross-References
- Related modules:
  - [enforcement.md](./enforcement.md) - Critical rules to understand first
  - [standards-integration.md](./standards-integration.md) - Standards compliance
- External docs:
  - Complete guides in `docs/GUIDES/`
  - Architecture documentation in `docs/ARCHITECTURE.md`
  - Script catalog in `docs/GUIDES/SCRIPT_CATALOG.md`

## Examples

### Example 1: First-Time Onboarding Workflow

```bash
# Step 1: Read LLM_ONBOARDING.md
cat docs/GUIDES/LLM_ONBOARDING.md

# Step 2: Read ENFORCEMENT.md
cat docs/ENFORCEMENT.md

# Step 3: Explore repository structure
ls -la
cat MANIFEST.json | jq '.repository_structure'

# Step 4: Verify build works
npm run build

# Step 5: Start work with proper context
```

### Example 2: Finding Specific Documentation

```bash
# Need script information?
cat docs/GUIDES/SCRIPT_CATALOG.md

# Need architecture details?
cat docs/ARCHITECTURE.md

# Need enforcement rules?
cat docs/ENFORCEMENT.md

# Need file inventory?
cat MANIFEST.json | jq
```

### Example 3: Understanding Context Loading

```bash
# Progressive context loading modules
ls -la docs/context/*/

# Core modules (HIGH priority - always load)
cat docs/context/core/*.md

# Workflow modules (MEDIUM priority - task-specific)
cat docs/context/workflows/*.md
```

## Common Pitfalls

- **Skipping ENFORCEMENT.md** - Critical rules MUST be understood first
- **Not checking MANIFEST.json** - Source of truth for file inventory
- **Ignoring reading order** - Designed for efficient onboarding
- **Missing architecture context** - System design informs all decisions

## Validation

### How to Verify Correct Application

```bash
# 1. Confirm all mandatory docs exist
test -f docs/ENFORCEMENT.md && \
test -f docs/GUIDES/LLM_ONBOARDING.md && \
test -f docs/ARCHITECTURE.md && \
test -f MANIFEST.json && \
echo "All mandatory docs present"

# 2. Verify you can build the site
npm run build

# 3. Check file structure matches documentation
diff <(cat MANIFEST.json | jq -r '.repository_structure' | sort) \
     <(find . -maxdepth 1 -type d | sort)
```

### Success Criteria
- [ ] Read LLM_ONBOARDING.md (quick start)
- [ ] Read ENFORCEMENT.md (critical rules)
- [ ] Reviewed ARCHITECTURE.md (system understanding)
- [ ] Located SCRIPT_CATALOG.md (available tools)
- [ ] Understand documentation hierarchy
- [ ] Can successfully build the site
- [ ] Know where to find specific documentation

## Changelog
- **2025-11-01**: Initial extraction from CLAUDE.md v3.0.0
