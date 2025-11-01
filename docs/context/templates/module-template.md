---
title: Context Module Template
category: templates
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 500
load_when:
  - Creating new context modules
  - Extending progressive loading system
dependencies: []
tags: [template, module, context, documentation]
---

# Context Module Template

## Module Metadata
- **Category:** templates
- **Priority:** LOW
- **Load frequency:** When creating new context modules or extending the progressive loading system
- **Dependencies:** None

## Purpose

This module provides a standardized template for creating new context modules in the progressive loading system, ensuring consistency in structure, frontmatter, and documentation patterns.

## When to Load This Module

- Creating new context modules
- Extending progressive loading system
- Standardizing documentation format

---

## Frontmatter Format

```yaml
---
title: [Module Title - Clear, descriptive name]
category: [core|workflows|standards|technical|reference|templates]
priority: [HIGH|MEDIUM|LOW]
version: 1.0.0
last_updated: YYYY-MM-DD
estimated_tokens: [number]
load_when:
  - "[Scenario 1 - Specific use case]"
  - "[Scenario 2 - Another use case]"
  - "[Scenario 3 - Additional context]"
dependencies:
  - [category/module-name]
  - [category/other-module]
tags: [tag1, tag2, tag3, tag4, tag5]
---
```

---

## Module Structure

### 1. Module Metadata Section

```markdown
# [Module Title]

## Module Metadata
- **Category:** [category name]
- **Priority:** [HIGH/MEDIUM/LOW]
- **Load frequency:** [Description of when/how often to load]
- **Dependencies:** [List of dependent modules or "None"]

## Purpose

[One concise paragraph describing what this module covers and why it exists.
Focus on the value it provides and the problems it solves.]

## When to Load This Module

- [Bullet 1: Specific scenario]
- [Bullet 2: Another scenario]
- [Bullet 3: Additional context]
- [Bullet 4: Related use cases]

---
```

### 2. Quick Reference Section (Optional)

```markdown
## Quick Reference

[Table, commands, or key patterns for rapid access]

| Pattern | Command | Example |
|---------|---------|---------|
| [Name] | `command` | `command --option` |

---
```

### 3. Content Sections

```markdown
## [Primary Section Title]

[Content organized logically with clear headings]

### [Subsection Title]

[Details with examples, code blocks, explanations]

**Key Points:**
- [Bullet 1]
- [Bullet 2]
- [Bullet 3]

**Example:**
```[language]
# Code example with comments
command --option value
```

**Why it matters:** [Explanation of significance]

---

## [Secondary Section Title]

[Continue pattern for additional sections]

---
```

### 4. Examples Section

```markdown
## Examples

### Example 1: [Scenario Title]

**Context:** [When/why to use this approach]

**Implementation:**
```[language]
# Complete working example
# With explanatory comments
```

**Expected Outcome:** [What should happen]

### Example 2: [Another Scenario]

[Repeat pattern for multiple examples]

---
```

### 5. Common Pitfalls Section

```markdown
## Common Pitfalls

### Pitfall 1: [Issue Description]

**Problem:** [What goes wrong]

**Why it happens:** [Root cause]

**Solution:** [How to avoid/fix]

**Example:**
```[language]
# Correct approach
```

---
```

### 6. Validation Section

```markdown
## Validation

[How to verify correct application of this module's guidance]

**Validation Commands:**
```bash
# Command to check correctness
command --validate

# Command to verify outcome
command --check
```

**Expected Results:**
- [Criterion 1]
- [Criterion 2]
- [Criterion 3]

---
```

### 7. Cross-References Section

```markdown
## Cross-References

**Related modules:**
- `category/module-name` - [Brief description of relationship]
- `category/other-module` - [How they connect]

**External documentation:**
- [Document Title](path/to/doc.md) - [What it covers]
- [Another Doc](path/to/other.md) - [Relevance]

**Tools/scripts:**
- `path/to/script.py` - [What it does]

---
```

### 8. Changelog Section

```markdown
## Changelog

- YYYY-MM-DD: [Change description]
- YYYY-MM-DD: [Earlier change]
```

---

## Category Guidelines

### core
- **Priority:** HIGH
- **Token budget:** ~1,200 per module
- **Purpose:** Critical rules, mandatory reading, enforcement
- **Examples:** enforcement, nda-compliance, file-management

### workflows
- **Priority:** MEDIUM
- **Token budget:** ~2,000 per module
- **Purpose:** Task-specific processes and methodologies
- **Examples:** blog-writing, sparc-development, swarm-orchestration

### standards
- **Priority:** MEDIUM/HIGH
- **Token budget:** ~1,800 per module
- **Purpose:** Quality gates, validation standards
- **Examples:** humanization-standards, citation-research, writing-style

### technical
- **Priority:** MEDIUM/LOW
- **Token budget:** ~1,500 per module
- **Purpose:** Implementation details, automation references
- **Examples:** script-catalog, git-workflow, build-automation

### reference
- **Priority:** LOW
- **Token budget:** ~1,000 per module
- **Purpose:** Historical context, lessons learned
- **Examples:** directory-structure, batch-history, compliance-history

### templates
- **Priority:** LOW
- **Token budget:** ~500 per module
- **Purpose:** Reusable patterns and templates
- **Examples:** blog-post-template, module-template, script-template

---

## Token Estimation Guidelines

**Rough estimates:**
- Quick reference table: ~50 tokens
- Section with bullets/examples: ~150 tokens
- Code block with explanation: ~100 tokens
- Detailed example: ~200 tokens
- Cross-references section: ~80 tokens

**Target ranges by category:**
- core: 800-1,500 tokens
- workflows: 1,500-3,500 tokens
- standards: 1,200-2,500 tokens
- technical: 1,000-2,000 tokens
- reference: 800-1,200 tokens
- templates: 400-600 tokens

---

## Dependency Management

**Specify dependencies when:**
- Module references another module's content
- Workflow requires prior knowledge from another module
- Standards build on core rules

**Format:**
```yaml
dependencies:
  - core/enforcement
  - standards/humanization-standards
```

**If no dependencies:**
```yaml
dependencies: []
```

---

## Tags Best Practices

**Use 3-7 tags per module:**
- Primary category indicator (e.g., "blog", "git", "validation")
- Functional tags (e.g., "automation", "enforcement", "workflow")
- Content tags (e.g., "humanization", "citations", "images")
- Cross-cutting concerns (e.g., "mandatory", "nda", "security")

**Example tag combinations:**
- Blog writing: `[blog, writing, content, workflow]`
- Enforcement: `[mandatory, rules, validation, pre-commit, enforcement]`
- Humanization: `[humanization, validation, tone, voice, authenticity]`

---

## Writing Style Guidelines

**Be concise:**
- One idea per paragraph
- Bullets for lists (not prose)
- Lead with the point

**Be specific:**
- Use concrete examples
- Include actual commands
- Show expected outputs

**Be helpful:**
- Explain "why" not just "what"
- Include common pitfalls
- Provide validation steps

---

## Cross-References

**Related modules:**
- `core/file-management` - File organization rules (where to save modules)
- `reference/directory-structure` - Repository layout understanding

**External documentation:**
- [docs/context/INDEX.yaml](../INDEX.yaml) - Module registry and metadata

---

## Changelog
- 2025-11-01: Initial template creation for progressive loading system
