---
title: Documentation Template
category: templates
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 500
load_when:
  - Creating new documentation
  - Standardizing docs format
dependencies: []
tags: [template, documentation, guide, reference]
---

# Documentation Template

## Module Metadata
- **Category:** templates
- **Priority:** LOW
- **Load frequency:** When creating new documentation files
- **Dependencies:** None

## Purpose

This module provides standardized templates for different types of documentation (guides, references, API docs) ensuring consistency across the repository.

## When to Load This Module

- Creating new documentation files
- Standardizing existing documentation
- Understanding documentation structure

---

## Guide/How-To Template

Use this template for instructional documentation (e.g., "How to Add Citations", "Getting Started Guide").

```markdown
# [Guide Title]

**Purpose:** [What this guide covers in one sentence]

**Audience:** [Who this guide is for]

**Prerequisites:**
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

**Estimated Time:** [X minutes/hours]

---

## Quick Start

[3-5 step minimal example for immediate results]

1. **[Step 1]:** [Minimal action]
```bash
# Command example
command --option
```

2. **[Step 2]:** [Next action]

3. **[Step 3]:** [Final action]

**Expected Result:** [What should happen]

---

## Detailed Guide

### Step 1: [Descriptive Title]

**What:** [What this step accomplishes]

**Why:** [Why this step is necessary]

**How:**

1. [Detailed instruction]
```[language]
# Code example with comments
command --detailed-options
```

2. [Next instruction]

**Verification:**
```bash
# Command to verify step completed
verify-command
```

**Expected output:**
```
Expected result text
```

### Step 2: [Descriptive Title]

[Repeat pattern for each step]

---

## Troubleshooting

### Issue: [Problem Description]

**Symptoms:**
- [Symptom 1]
- [Symptom 2]

**Cause:** [Root cause explanation]

**Solution:**

1. [Step to resolve]
```bash
# Fix command
fix-command
```

2. [Verification step]

**Prevention:** [How to avoid in the future]

### Issue: [Another Problem]

[Repeat pattern for common issues]

---

## Examples

### Example 1: [Real-World Scenario]

**Context:** [When you'd use this approach]

**Implementation:**
```[language]
# Complete working example
# With explanatory comments
# Showing realistic usage
```

**Explanation:** [What this example demonstrates]

**Expected Output:**
```
Output text here
```

### Example 2: [Another Scenario]

[Repeat pattern for multiple examples]

---

## Best Practices

**Do:**
- [Recommended practice 1]
- [Recommended practice 2]
- [Recommended practice 3]

**Don't:**
- [Anti-pattern 1]
- [Anti-pattern 2]
- [Anti-pattern 3]

---

## Further Reading

- [Related Guide](link) - [What it covers]
- [External Resource](link) - [Why it's useful]
- [Official Documentation](link) - [Relevant section]

---

## Changelog

- YYYY-MM-DD: [Change description]
```

---

## Reference Documentation Template

Use this template for reference material (e.g., "Command Reference", "API Reference").

```markdown
# [Reference Title]

**Purpose:** [What this reference covers]

**Last Updated:** YYYY-MM-DD

---

## Overview

[Brief description of what's documented]

**Key Concepts:**
- [Concept 1]: [Brief explanation]
- [Concept 2]: [Brief explanation]
- [Concept 3]: [Brief explanation]

---

## Commands

### Command: [command-name]

**Purpose:** [What this command does]

**Syntax:**
```bash
command [required-arg] [--optional-arg]
```

**Arguments:**

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `arg1` | string | Yes | - | [Description] |
| `--option` | flag | No | false | [Description] |

**Examples:**

```bash
# Example 1: [Use case]
command basic-usage

# Example 2: [Advanced use case]
command --with-options value
```

**Output:**
```
Expected output format
```

**Exit Codes:**
- `0` - Success
- `1` - General error
- `2` - Invalid argument

**Related Commands:**
- `related-command` - [What it does]

---

## Configuration

### Option: [option-name]

**Purpose:** [What this option controls]

**Type:** [string|integer|boolean|array]

**Default:** `[default-value]`

**Values:**
- `value1` - [Description]
- `value2` - [Description]

**Example:**
```[format]
option_name: value
```

**Notes:**
- [Important note 1]
- [Important note 2]

---

## API Reference

### Function: [function-name]

**Purpose:** [What this function does]

**Signature:**
```python
def function_name(
    arg1: Type,
    arg2: Optional[Type] = None
) -> ReturnType:
    """
    [Brief description]

    Args:
        arg1: [Description]
        arg2: [Description]

    Returns:
        [Return value description]

    Raises:
        ErrorType: [When this error occurs]
    """
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `arg1` | Type | Yes | - | [Description] |
| `arg2` | Type | No | None | [Description] |

**Returns:**

- **Type:** ReturnType
- **Description:** [What is returned]

**Raises:**

- `ErrorType`: [Condition that causes error]

**Example:**
```python
# Example usage
result = function_name("value")
print(result)  # Expected output
```

---

## Data Structures

### Structure: [StructureName]

**Purpose:** [What this structure represents]

**Format:**
```json
{
  "field1": "type",
  "field2": 123,
  "nested": {
    "subfield": "value"
  }
}
```

**Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `field1` | string | Yes | [Description] |
| `field2` | integer | No | [Description] |

**Example:**
```json
{
  "field1": "example",
  "field2": 42
}
```

---

## Quick Reference Tables

### [Category] Commands

| Command | Description | Example |
|---------|-------------|---------|
| `cmd1` | [What it does] | `cmd1 --opt` |
| `cmd2` | [What it does] | `cmd2 arg` |

### [Category] Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `opt1` | true/false | false | [What it controls] |
| `opt2` | 1-100 | 10 | [What it controls] |

---

## Cross-References

**Related Documentation:**
- [Doc Title](link) - [What it covers]

**External Resources:**
- [Resource Title](link) - [Why it's useful]

---

## Changelog

- YYYY-MM-DD: [Change description]
```

---

## Architecture/Design Document Template

Use this template for architectural documentation.

```markdown
# [System/Feature Name] Architecture

**Version:** X.Y.Z
**Last Updated:** YYYY-MM-DD
**Status:** [Draft|Review|Approved]

---

## Executive Summary

[2-3 paragraph overview of the system/feature]

**Key Points:**
- [Main point 1]
- [Main point 2]
- [Main point 3]

---

## Goals & Requirements

### Functional Requirements
- [Requirement 1]
- [Requirement 2]

### Non-Functional Requirements
- **Performance:** [Criteria]
- **Scalability:** [Criteria]
- **Security:** [Criteria]

### Constraints
- [Constraint 1]
- [Constraint 2]

---

## Architecture Overview

[High-level description]

**Diagram:**
```mermaid
[Mermaid diagram code]
```

**Components:**
- [Component 1]: [Purpose]
- [Component 2]: [Purpose]

---

## Detailed Design

### Component: [Component Name]

**Responsibility:** [What this component does]

**Interfaces:**
- [Interface 1]: [Description]

**Dependencies:**
- [Dependency 1]: [Why needed]

**Implementation Notes:**
- [Note 1]

---

## Data Flow

[Describe how data moves through the system]

**Diagram:**
```mermaid
sequenceDiagram
    [Sequence diagram code]
```

**Steps:**
1. [Step 1 description]
2. [Step 2 description]

---

## Trade-offs & Decisions

### Decision: [Decision Title]

**Options Considered:**
- **Option A:** [Pros/cons]
- **Option B:** [Pros/cons]

**Decision:** [Chosen option]

**Rationale:** [Why this option was chosen]

**Consequences:** [Implications]

---

## Security Considerations

- [Security aspect 1]
- [Security aspect 2]

---

## Performance Considerations

- [Performance aspect 1]
- [Performance aspect 2]

---

## Future Enhancements

- [Enhancement 1]
- [Enhancement 2]

---

## References

- [Reference 1](link)
- [Reference 2](link)

---

## Changelog

- YYYY-MM-DD: [Change]
```

---

## Documentation Best Practices

### Writing Style

**Be clear:**
- Use simple language
- Define jargon on first use
- One concept per paragraph

**Be concise:**
- Lead with the point
- Use bullets for lists
- Cut unnecessary words

**Be helpful:**
- Include examples
- Show expected outputs
- Provide troubleshooting

### Structure

**Logical flow:**
1. Start with overview
2. Prerequisites/requirements
3. Step-by-step instructions
4. Examples
5. Troubleshooting
6. References

**Use headings:**
- Clear hierarchy (H1 → H2 → H3)
- Descriptive titles
- Consistent formatting

### Code Examples

**Always include:**
- Comments explaining key concepts
- Expected output
- Working, tested code
- Error handling

**Format:**
```language
# Example with explanation
command --option value

# Expected output:
# Output text here
```

---

## Cross-References

**Related modules:**
- `templates/module-template` - Context module template
- `templates/blog-post-template` - Blog post template
- `reference/directory-structure` - Where to save documentation

---

## Changelog
- 2025-11-01: Initial documentation template creation
