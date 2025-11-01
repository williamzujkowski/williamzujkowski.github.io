---
title: Mandatory Enforcement Rules
category: core
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1500
load_when:
  - Any operation that modifies files
  - Creating new content
  - Before commits
  - File operations (create, edit, delete)
dependencies: []
tags: [mandatory, rules, validation, pre-commit, enforcement]
---

# Mandatory Enforcement Rules

## Purpose
This module defines **critical enforcement rules** that MUST be followed before ANY operation. These rules are automatically validated by pre-commit hooks and GitHub Actions to prevent repository corruption, duplicate files, and standards violations.

## When to Load This Module
- **Before creating any files** - Check for duplicates
- **Before editing existing files** - Validate MANIFEST.json currency
- **Before committing changes** - Ensure all validation passes
- **When unsure about file operations** - Reference these rules first

## Quick Reference

| Rule | Action Required | Consequence if Violated |
|------|----------------|-------------------------|
| Check `.claude-rules.json` | Verify current enforcement rules | Operation blocked |
| Validate MANIFEST.json | Check `last_validated` timestamp | Pre-commit fails |
| No duplicate files | Check `file_registry` | Operation fails |
| Follow standards | Confirm compliance with github.com/williamzujkowski/standards | GitHub Actions fail |
| Correct timestamps | Use time.gov, fallback to system time | Inconsistent metadata |

---

## 🚨 MANDATORY ENFORCEMENT NOTICE

**CRITICAL**: Before ANY operation, you MUST:

1. **CHECK** `.claude-rules.json` for current enforcement rules
2. **VALIDATE** MANIFEST.json is current (check last_validated timestamp)
3. **VERIFY** no duplicate files will be created (check file_registry)
4. **CONFIRM** operation follows standards from https://github.com/williamzujkowski/standards
5. **USE** appropriate timestamps (prefer time.gov, fallback to system time)

## Violations Will Be Automatically Blocked

Your operation will **FAIL** if you:
- Create duplicate files instead of updating existing ones
- Don't update MANIFEST.json after changes
- Violate standards from the submodule
- Use incorrect timestamps
- Save files to incorrect directories

## Enforcement Is Active

- **Pre-commit hooks** validate all changes
- **GitHub Actions** enforce standards on all pushes
- **`.claude-rules.json`** defines mandatory rules

See `.claude-rules.json` for complete enforcement rules.

---

## Pre-Commit Hook Enforcement

Pre-commit hooks automatically enforce these standards:

### Hook Actions
1. **MANIFEST.json validation** - Ensures repository inventory is current
2. **Duplicate detection** - Prevents creating duplicate files
3. **Standards compliance** - Verifies adherence to coding standards
4. **Humanization validation** (blog posts) - Checks posts score ≥75/100
5. **MANIFEST.json update** - Auto-updates file registry after validation

### If Validation Fails

```bash
# Example failure output:
❌ FAIL: Operation blocked - duplicate file detected

Violation: File already exists in file_registry
Location: scripts/blog-research/validate-claims.py

Action required:
- Update existing file instead of creating new one
- OR remove existing file first (with justification)
```

### To Refine and Retry
1. Address violations using appropriate corrections
2. Re-run validation manually if needed
3. Verify all checks pass
4. Re-attempt commit

### Bypass (NOT Recommended)

```bash
# Only use for emergencies (e.g., fixing broken build)
git commit --no-verify -m "emergency: fix critical issue"
```

**Why it matters:** Automated enforcement prevents repository corruption and maintains quality standards.

---

## Cross-References
- Related modules:
  - [file-management.md](./file-management.md) - File organization rules
  - [standards-integration.md](./standards-integration.md) - Standards compliance
- External docs:
  - `.claude-rules.json` - Complete enforcement rules
  - `MANIFEST.json` - Repository inventory
  - `docs/ENFORCEMENT.md` - Detailed enforcement documentation

## Examples

### Example 1: Before Creating a New File

```bash
# ALWAYS check MANIFEST.json first
grep -r "scripts/blog-research/validate-claims.py" MANIFEST.json

# If found, UPDATE existing file instead
# If not found, proceed with creation AND update MANIFEST.json
```

### Example 2: Before Committing Changes

```bash
# Validation runs automatically on commit
git add .
git commit -m "feat: add new feature"

# If validation fails:
# 1. Read error message
# 2. Fix violations
# 3. Re-attempt commit
```

### Example 3: Checking Current Enforcement Rules

```bash
# Read current rules
cat .claude-rules.json

# Verify MANIFEST.json is current
jq '.last_validated' MANIFEST.json
```

## Common Pitfalls

- **Forgetting to check MANIFEST.json** - Always verify before creating files
- **Skipping pre-commit hooks** - Never use `--no-verify` unless emergency
- **Ignoring validation errors** - Read and address ALL violations
- **Creating duplicates** - Search file_registry first
- **Outdated timestamps** - Use time.gov for accuracy

## Validation

### How to Verify Correct Application

```bash
# 1. Ensure pre-commit hooks are installed
ls -la .git/hooks/pre-commit

# 2. Test validation on staged changes
git add [file]
git commit --dry-run

# 3. Check MANIFEST.json is current
jq '.last_validated' MANIFEST.json

# 4. Verify no duplicates will be created
grep -r "[filename]" MANIFEST.json
```

### Success Criteria
- [ ] Pre-commit hooks installed and active
- [ ] MANIFEST.json `last_validated` within 24 hours
- [ ] No duplicate files in `file_registry`
- [ ] All standards checks pass
- [ ] Validation runs successfully on commit

## Changelog
- **2025-11-01**: Initial extraction from CLAUDE.md v3.0.0
