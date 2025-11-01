---
title: File Management & Organization
category: core
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1800
load_when:
  - Creating new files
  - Moving or renaming files
  - Cleanup operations
  - Documentation management
dependencies: [enforcement.md]
tags: [files, organization, cleanup, concurrent-execution, directories]
---

# File Management & Organization

## Purpose
This module defines **absolute rules** for file operations to prevent root directory clutter, ensure concurrent execution patterns, and maintain clean repository organization through proper cleanup workflows.

## When to Load This Module
- **Before creating any files** - Verify correct directory
- **During cleanup operations** - Follow mandatory cleanup phase
- **When organizing content** - Apply retention policies
- **During concurrent operations** - Execute all related ops in one message

## Quick Reference

### File Organization Rules

| File Type | Correct Location | NEVER Here |
|-----------|-----------------|------------|
| Source code | `/src` | Root |
| Tests | `/tests` | Root |
| Documentation | `/docs` | Root |
| Scripts | `/scripts` | Root |
| Config files | `/config` or root (if needed) | Random subdirs |

### Concurrent Execution Pattern

**GOLDEN RULE:** "1 MESSAGE = ALL RELATED OPERATIONS"

- **TodoWrite**: Batch ALL todos in ONE call (5-10+ minimum)
- **File operations**: Batch ALL reads/writes/edits in ONE message
- **Bash commands**: Batch ALL terminal operations in ONE message

---

## 🚨 CRITICAL: CONCURRENT EXECUTION & FILE MANAGEMENT

### ABSOLUTE RULES

1. ALL operations MUST be concurrent/parallel in a single message
2. **NEVER save working files, text/mds and tests to the root folder**
3. ALWAYS organize files in appropriate subdirectories

### ⚡ GOLDEN RULE: "1 MESSAGE = ALL RELATED OPERATIONS"

**MANDATORY PATTERNS:**
- **TodoWrite**: ALWAYS batch ALL todos in ONE call (5-10+ todos minimum)
- **Task tool**: ALWAYS spawn ALL agents in ONE message with full instructions
- **File operations**: ALWAYS batch ALL reads/writes/edits in ONE message
- **Bash commands**: ALWAYS batch ALL terminal operations in ONE message
- **Memory operations**: ALWAYS batch ALL memory store/retrieve in ONE message

**Why it matters:** Parallel execution = 2.8-4.4x faster. Sequential = slow, wasted tokens.

### Concurrent Execution Examples

✅ **Correct:**
```javascript
// Single message with all operations
Read("file1.js")
Read("file2.js")
Edit("file1.js", old, new)
Edit("file2.js", old, new)
Bash("npm test")
```

❌ **Wrong:**
```javascript
// Message 1
Read("file1.js")

// Message 2
Edit("file1.js", old, new)

// Message 3
Bash("npm test")
```

---

## 🧹 CLEANUP PHASE: MANDATORY FOR ALL WORKFLOWS

### EVERY TODO LIST MUST INCLUDE

1. **Cleanup tasks** as final items (remove temp files, vestigial scripts, test artifacts)
2. **Validation after cleanup** to ensure nothing breaks
3. **Commit and push** cleaned state
4. **Monitor deployment** to verify site functionality
5. **Revert if needed** and fix issues iteratively

### Cleanup Targets

- Temporary troubleshooting scripts (e.g., `validate-*.py`, `fix-*.py`, `test-*.py`)
- Research/analysis files in `/docs` that are no longer needed
- Duplicate or superseded scripts in `/scripts`
- Test artifacts and temporary data files
- Old backup files or `.bak` extensions
- Unnecessary log files or debug outputs

### Cleanup Rules

- NEVER delete production scripts without verification
- ALWAYS test site functionality after cleanup
- KEEP essential utilities and actively used tools
- PRESERVE documentation that provides value
- MAINTAIN scripts referenced in CLAUDE.md or README

---

## 📁 File Organization Rules

### Never Save to Root

**Use these directories:**

```
/src         → Source code
/tests       → Test files
/docs        → Documentation (including this file)
/scripts     → Automation utilities
/config      → Configuration files
```

### Common Mistakes

❌ `validate-claims.py` in root
❌ `test-citations.md` in root
❌ `working-notes.txt` anywhere

✅ `scripts/blog-research/validate-claims.py`
✅ `tests/test-citations.py`
✅ `docs/working-notes.md`

---

## 📋 Documentation Retention Policy

### Active Documentation (0-30 days)
- Keep in root `/reports` or `/docs`
- Current phase work, recent completion reports
- Actively referenced methodology documents

### Archive (30-180 days)
- Move to `/docs/archive/YYYY-QX/`
- Completed batch reports (Batch 1-6)
- Phase completion reports (Phase 8.4, 8.5, etc.)
- Historical test reports

### Purge (180+ days)
- Delete non-reference documentation
- Superseded plans and intermediate reports
- Redundant status updates

### Never Delete
- `LESSONS_LEARNED.md` files (all batches)
- Final completion reports (latest per phase)
- Methodology documentation (`CLAUDE_MD_UPDATES.md`, `UNIFIED_HUMANIZATION_METHODOLOGY.md`)
- Validation tools and pattern definitions
- Architecture and enforcement guides

### Archive Locations
- **Q3 2025**: `docs/archive/2025-Q3/` (Batches 1-6, Smart Brevity transformation)
- **Q4 2025**: `docs/archive/2025-Q4/` (Phase 8 code reduction, security refinements)

---

## 📂 Documentation Hierarchy

### Primary (Authoritative)
- **CLAUDE.md**: Master reference for all standards (or modular equivalent)
- **MANIFEST.json**: System inventory and file registry
- **.claude-rules.json**: Enforcement rules

### Secondary (Supporting)
- **docs/ARCHITECTURE.md**: System design
- **docs/GUIDES/**: How-to documentation
- **docs/ENFORCEMENT.md**: Mandatory rules
- **content-review-instructions.md**: Review standards

### Generated (Reference)
- **reports/**: Audit and compliance reports
- **docs/STANDARDS/**: Implementation checklists

> **Note**: All documentation must defer to authoritative sources for canonical requirements.

---

## Cross-References
- Related modules:
  - [enforcement.md](./enforcement.md) - Enforcement rules require proper file organization
  - [standards-integration.md](./standards-integration.md) - Standards define file structure
- External docs:
  - `MANIFEST.json` - Complete file registry
  - `docs/ARCHITECTURE.md` - System architecture

## Examples

### Example 1: Creating a New Validation Script (CORRECT)

```bash
# CORRECT: Create in appropriate subdirectory
cat > scripts/blog-research/validate-new-pattern.py <<EOF
#!/usr/bin/env python3
# Validation script
EOF

# Update MANIFEST.json
# Test script
# Commit changes
```

### Example 2: Creating a Test File (INCORRECT)

```bash
# INCORRECT: Creating in root
❌ cat > test-validation.py <<EOF

# CORRECT: Creating in tests directory
✅ cat > tests/test-validation.py <<EOF
```

### Example 3: Concurrent File Operations

```bash
# Create multiple related files in ONE message
cat > docs/context/core/module1.md <<EOF
# Module 1
EOF

cat > docs/context/core/module2.md <<EOF
# Module 2
EOF

cat > docs/context/core/module3.md <<EOF
# Module 3
EOF

# All in parallel, not sequential messages
```

### Example 4: Cleanup Workflow

```bash
# Phase 1: Identify cleanup targets
find . -name "*-test-*.py" -type f

# Phase 2: Remove temporary files
rm scripts/blog-research/test-validation.py
rm docs/working-notes-temp.md

# Phase 3: Validate site still works
npm run build

# Phase 4: Commit cleaned state
git add .
git commit -m "chore: cleanup temporary files"
```

## Common Pitfalls

- **Root directory clutter** - Always check destination before creating files
- **Sequential operations** - Batch all related operations in one message
- **Skipping cleanup phase** - Every workflow must include cleanup tasks
- **Deleting valuable docs** - Follow retention policy, preserve key documents
- **Incomplete validation** - Test after cleanup to ensure nothing breaks

## Validation

### How to Verify Correct Application

```bash
# 1. Check for files in root that shouldn't be there
ls -la *.py *.md *.txt 2>/dev/null | grep -v "README\|LICENSE\|CLAUDE"

# 2. Verify proper directory usage
find src tests docs scripts -type f | wc -l

# 3. Check for temporary files
find . -name "*-temp-*" -o -name "*-test-*" -o -name "*.bak"

# 4. Validate archive organization
ls -la docs/archive/*/

# 5. Ensure MANIFEST.json is current
jq '.last_validated' MANIFEST.json
```

### Success Criteria
- [ ] No working files in root directory
- [ ] All files in appropriate subdirectories
- [ ] Cleanup phase completed (temp files removed)
- [ ] Build passes after cleanup
- [ ] Documentation organized per retention policy
- [ ] MANIFEST.json updated with changes

## Changelog
- **2025-11-01**: Initial extraction from CLAUDE.md v3.0.0
