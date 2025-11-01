---
title: Standards Integration
category: core
priority: HIGH
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1000
load_when:
  - Before any file operation
  - When validating changes
  - Before commits
  - During MANIFEST.json updates
dependencies: [enforcement.md]
tags: [standards, manifest, timestamps, validation, submodule]
---

# Standards Integration

## Purpose
This module defines **integration requirements** with the external standards repository (github.com/williamzujkowski/standards) and explains MANIFEST.json management, timestamp handling, and operation validation.

## When to Load This Module
- **Before any operation** - Confirm compliance with standards
- **When updating MANIFEST.json** - Follow update procedures
- **When handling timestamps** - Use correct time sources
- **During validation** - Verify standards compliance

## Quick Reference

| Component | Requirement | How to Verify |
|-----------|------------|---------------|
| Standards Submodule | Must follow github.com/williamzujkowski/standards | Check submodule status |
| MANIFEST.json | Must be current (`last_validated` within 24h) | `jq '.last_validated' MANIFEST.json` |
| Timestamps | Prefer time.gov, fallback to system time | Use appropriate source |
| File Registry | No duplicates allowed | `grep -r "[filename]" MANIFEST.json` |

---

## Standards Repository Integration

### External Standards Reference

All operations MUST follow standards from:
**https://github.com/williamzujkowski/standards**

This repository is integrated as a Git submodule and defines:
- File naming conventions
- Directory structure requirements
- Coding standards
- Documentation patterns
- Validation rules

### Verifying Standards Compliance

```bash
# Check submodule status
git submodule status

# Update standards submodule if needed
git submodule update --init --recursive

# View current standards
ls -la standards/
cat standards/README.md
```

---

## MANIFEST.json Management

### What is MANIFEST.json?

**Single source of truth** for repository inventory, containing:
- Complete file registry
- Repository structure metadata
- Last validation timestamp
- File categorization
- Dependency tracking

### Critical MANIFEST.json Rules

1. **CHECK** `last_validated` timestamp before operations
2. **UPDATE** after ANY file create/delete/move operations
3. **VERIFY** no duplicate entries in `file_registry`
4. **VALIDATE** structure matches actual repository

### Validation Workflow

```bash
# 1. Check currency (must be within 24 hours)
jq '.last_validated' MANIFEST.json

# 2. Verify file_registry accuracy
jq '.file_registry | length' MANIFEST.json
find . -type f | wc -l

# 3. Check for duplicates
jq '.file_registry[] | .path' MANIFEST.json | sort | uniq -d

# 4. Update if needed
# (Update script would go here)
```

### When to Update MANIFEST.json

**ALWAYS update after:**
- Creating new files
- Deleting files
- Moving/renaming files
- Changing file purposes
- Modifying directory structure

**Enforcement:**
Pre-commit hooks automatically validate MANIFEST.json currency and update if needed.

---

## Timestamp Handling

### Timestamp Sources (Priority Order)

1. **Primary: time.gov** - Official US government time source
   ```bash
   curl -s https://time.gov/ | grep -oP '\d{2}:\d{2}:\d{2}'
   ```

2. **Fallback: System time** - Use if time.gov unavailable
   ```bash
   date -u +"%Y-%m-%dT%H:%M:%SZ"
   ```

### Timestamp Formats

**ISO 8601 format required:**
- Full datetime: `2025-11-01T12:34:56Z`
- Date only: `2025-11-01`

**Examples:**
```json
{
  "last_validated": "2025-11-01T14:23:45Z",
  "created_date": "2025-11-01",
  "modified_date": "2025-11-01T14:23:45Z"
}
```

### Why Timestamps Matter

- **Consistency:** All timestamps from same source
- **Accuracy:** Official time source prevents drift
- **Validation:** Pre-commit hooks check timestamp validity
- **Compliance:** Required for MANIFEST.json updates

---

## Operation Validation

### Pre-Operation Checklist

Before ANY operation that modifies files:

1. **Confirm standards compliance**
   ```bash
   # Check if operation follows standards
   cat standards/file-naming.md
   ```

2. **Validate MANIFEST.json is current**
   ```bash
   jq '.last_validated' MANIFEST.json
   # Must be within 24 hours
   ```

3. **Verify no duplicate files**
   ```bash
   grep -r "[new-filename]" MANIFEST.json
   # Must return no results
   ```

4. **Check directory structure**
   ```bash
   # Ensure target directory exists and is correct
   ls -la [target-directory]/
   ```

5. **Use correct timestamp source**
   ```bash
   # Try time.gov first, fallback to system time
   curl -s https://time.gov/ || date -u +"%Y-%m-%dT%H:%M:%SZ"
   ```

### Post-Operation Requirements

After file operations:

1. **Update MANIFEST.json** with new file entries
2. **Validate** MANIFEST.json structure
3. **Test** that build still passes
4. **Commit** changes with updated MANIFEST.json

---

## Cross-References
- Related modules:
  - [enforcement.md](./enforcement.md) - Enforcement relies on standards compliance
  - [file-management.md](./file-management.md) - File organization follows standards
- External docs:
  - `MANIFEST.json` - Repository inventory
  - `standards/` submodule - Complete standards documentation
  - `.claude-rules.json` - Enforcement rules

## Examples

### Example 1: Creating New File with Standards Compliance

```bash
# 1. Check standards for file naming
cat standards/file-naming.md

# 2. Verify MANIFEST.json is current
jq '.last_validated' MANIFEST.json

# 3. Check for duplicates
grep -r "new-module.md" MANIFEST.json

# 4. Create file in correct location
cat > docs/context/core/new-module.md <<EOF
---
title: New Module
category: core
priority: HIGH
version: 1.0.0
last_updated: $(date -u +"%Y-%m-%d")
---
EOF

# 5. Update MANIFEST.json
# (Update operation here)

# 6. Validate and commit
npm run build
git add docs/context/core/new-module.md MANIFEST.json
git commit -m "feat: add new core module"
```

### Example 2: Validating MANIFEST.json Currency

```bash
# Get last_validated timestamp
LAST_VALIDATED=$(jq -r '.last_validated' MANIFEST.json)

# Get current time
CURRENT_TIME=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Compare (should be within 24 hours)
echo "Last validated: $LAST_VALIDATED"
echo "Current time: $CURRENT_TIME"

# If > 24 hours, update MANIFEST.json
```

### Example 3: Checking Standards Compliance

```bash
# Verify submodule is current
cd standards/
git pull origin main
cd ..

# Check specific standard
cat standards/documentation-structure.md

# Verify compliance
# (Validation logic here)
```

## Common Pitfalls

- **Outdated MANIFEST.json** - Always check `last_validated` timestamp
- **Duplicate file entries** - Search before creating new files
- **Wrong timestamp source** - Use time.gov first, system time as fallback
- **Standards drift** - Update submodule regularly
- **Missing MANIFEST.json updates** - Update after ALL file operations

## Validation

### How to Verify Correct Application

```bash
# 1. Standards submodule is current
git submodule status | grep standards

# 2. MANIFEST.json is current (within 24 hours)
jq '.last_validated' MANIFEST.json

# 3. No duplicate files in registry
jq '.file_registry[] | .path' MANIFEST.json | sort | uniq -d

# 4. Timestamps use correct format
jq '.last_validated' MANIFEST.json | grep -E '^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'

# 5. Build passes
npm run build
```

### Success Criteria
- [ ] Standards submodule present and current
- [ ] MANIFEST.json `last_validated` within 24 hours
- [ ] No duplicate entries in file_registry
- [ ] All timestamps use ISO 8601 format
- [ ] File operations follow standards
- [ ] Build passes after validation

## Changelog
- **2025-11-01**: Initial extraction from CLAUDE.md v3.0.0
