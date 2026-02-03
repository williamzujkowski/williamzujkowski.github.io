---
title: SPARC Development Workflow
category: workflows
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 2800
load_when:
  - Using SPARC methodology
  - TDD development
  - System architecture work
dependencies:
  - core/enforcement
tags: [sparc, tdd, development, methodology]
---

# SPARC Development Workflow

## Module Metadata

**Category:** workflows
**Priority:** MEDIUM
**Load When:** Using SPARC methodology, TDD development, system architecture work
**Dependencies:** core/enforcement
**Estimated Size:** ~2,800 tokens

---

## Purpose

This module documents the SPARC (Specification, Pseudocode, Architecture, Refinement, Completion) methodology with Claude-Flow orchestration for systematic Test-Driven Development.

---

## When to Load This Module

**Load this module when:**
- Using SPARC methodology for development
- Implementing TDD workflows
- Coordinating multi-agent development
- System architecture planning

**Skip this module if:**
- Simple script development (use script-catalog.md)
- Blog content work (use blog-writing.md)

---

## Quick Reference

**Core Commands:**
- `nexus-agents sparc modes` - List available modes
- `nexus-agents sparc tdd "<feature>"` - Run complete TDD workflow
- `npm run build` - Build production site
- `npm run test:all` - Run all test suites

**5 SPARC Phases:**
1. **Specification** - Requirements analysis
2. **Pseudocode** - Algorithm design
3. **Architecture** - System design
4. **Refinement** - TDD implementation
5. **Completion** - Integration

---

## SPARC Commands

### Core Commands

```bash
# List available modes
nexus-agents sparc modes

# Execute specific mode
nexus-agents sparc run <mode> "<task>"

# Run complete TDD workflow
nexus-agents sparc tdd "<feature>"

# Get mode details
nexus-agents sparc info <mode>
```

### Batchtools Commands

```bash
# Parallel execution
nexus-agents sparc batch <modes> "<task>"

# Full pipeline processing
nexus-agents sparc pipeline "<task>"

# Multi-task processing
nexus-agents sparc concurrent <mode> "<tasks-file>"
```

### Available npm Commands

```bash
# Build production site
npm run build

# Development server with hot reload
npm run serve

# Run unit tests
npm run test

# Run all test suites
npm run test:all

# Validate knowledge management standards
npm run validate:km
```

---

## SPARC Workflow Phases

### 1. Specification - Requirements Analysis

**Command:**
```bash
nexus-agents sparc run spec-pseudocode
```

**Purpose:** Analyze requirements and define acceptance criteria

**Deliverables:**
- Functional requirements document
- Edge case identification
- Acceptance criteria
- Initial test scenarios

### 2. Pseudocode - Algorithm Design

**Command:**
```bash
nexus-agents sparc run spec-pseudocode
```

**Purpose:** Design algorithms and logic flow before implementation

**Deliverables:**
- High-level algorithm design
- Data structure definitions
- Control flow diagrams
- Complexity analysis

### 3. Architecture - System Design

**Command:**
```bash
nexus-agents sparc run architect
```

**Purpose:** Design scalable, maintainable system architecture

**Deliverables:**
- Architecture diagrams
- Component interfaces
- Integration points
- Technology stack decisions

### 4. Refinement - TDD Implementation

**Command:**
```bash
nexus-agents sparc tdd
```

**Purpose:** Implement features using Test-Driven Development

**Deliverables:**
- Passing test suites
- Production code
- Refactored implementation
- Code coverage reports

**TDD Cycle:**
1. **Red**: Write failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality

### 5. Completion - Integration

**Command:**
```bash
nexus-agents sparc run integration
```

**Purpose:** Integrate components and validate system behavior

**Deliverables:**
- Integration tests passing
- System documentation
- Deployment scripts
- Performance validation

---

## Code Style & Best Practices

### Core Principles

- **Modular Design**: Files under 500 lines
- **Environment Safety**: Never hardcode secrets
- **Test-First**: Write tests before implementation
- **Clean Architecture**: Separate concerns
- **Documentation**: Keep updated

### DRY and SOLID

**DRY (Don't Repeat Yourself):**
- Extract reusable functions
- Create shared utilities
- Use configuration files

**SOLID Principles:**
- **S**ingle Responsibility: One class, one purpose
- **O**pen/Closed: Open for extension, closed for modification
- **L**iskov Substitution: Subclasses interchangeable with base
- **I**nterface Segregation: Many specific interfaces over one general
- **D**ependency Inversion: Depend on abstractions, not concretions

---

## Blog Visual Enhancement System

**Quick Commands for Blog Optimization:**

```bash
# Analyze posts for high code ratios
python scripts/blog-content/optimize-blog-content.py

# Generate Mermaid diagram templates
python scripts/utilities/diagram-manager.py

# Search and download stock images (no API keys)
python scripts/blog-images/playwright-image-search.py
```

**Code Reduction Guidelines:**
- Target <25% code-to-content ratio
- Replace verbose code with Mermaid diagrams
- Keep snippets to 5-10 essential lines
- Link to GitHub gists for full examples

See docs/BLOG_VISUAL_ENHANCEMENT_GUIDE.md for complete documentation.

---

## Cross-References

### Related Modules
- [enforcement.md](../core/enforcement.md) - Mandatory rules before operations
- [swarm-orchestration.md](./swarm-orchestration.md) - Multi-agent coordination

### External References
- [Claude-Flow Documentation](https://github.com/ruvnet/nexus-agents)
- [docs/ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
- [docs/BLOG_VISUAL_ENHANCEMENT_GUIDE.md](../../BLOG_VISUAL_ENHANCEMENT_GUIDE.md) - Visual optimization

---

## Examples

### Example 1: Complete TDD Workflow

```bash
# Run full TDD workflow for new feature
nexus-agents sparc tdd "implement user authentication"

# SPARC will automatically:
# 1. Generate specification
# 2. Create pseudocode
# 3. Design architecture
# 4. Write tests first
# 5. Implement passing code
# 6. Refactor and integrate
```

**Explanation:** One command orchestrates entire TDD lifecycle.

### Example 2: Parallel Mode Execution

```bash
# Execute multiple modes in parallel
nexus-agents sparc batch spec-pseudocode,architect "<task>"

# Benefits: 2.8-4.4x faster than sequential
```

**Explanation:** Batch commands leverage parallel execution for speed.

---

## Common Pitfalls

### Pitfall 1: Skipping Specification Phase
**Problem:** Jump straight to coding without clear requirements
**Solution:** ALWAYS run spec-pseudocode first
**Prevention:** Follow SPARC phases in order

### Pitfall 2: Not Writing Tests First
**Problem:** Implementation-driven development, not test-driven
**Solution:** Use `sparc tdd` command to enforce red-green-refactor
**Prevention:** Commit to TDD discipline

### Pitfall 3: Hardcoding Secrets
**Problem:** API keys, passwords in source code
**Solution:** Use environment variables, .env files (git-ignored)
**Prevention:** Review code style & best practices

---

## Validation

### How to Verify Correct Application

**Checklist:**
- [ ] All 5 SPARC phases completed
- [ ] Tests written before implementation
- [ ] All tests passing (`npm run test:all`)
- [ ] Code follows style guidelines
- [ ] No secrets hardcoded
- [ ] Documentation updated

**Commands:**
```bash
# Validate all tests pass
npm run test:all

# Check build succeeds
npm run build

# Validate knowledge management
npm run validate:km

# Verify no secrets in code
grep -r "API_KEY\|PASSWORD\|SECRET" src/ --exclude-dir=node_modules
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md sections:
  - "SPARC Commands"
  - "SPARC Workflow Phases"
  - "Code Style & Best Practices"
  - "Blog Visual Enhancement System"
- Complete command reference
- Examples and validation added

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Development Team

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
