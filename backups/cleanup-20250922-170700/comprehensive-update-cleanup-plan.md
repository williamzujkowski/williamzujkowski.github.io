# Comprehensive Update & Cleanup Plan

## OBJECTIVE
Systematically update GitHub Actions workflows, dependencies, and clean up vestigial files following repository-specific instructions from CLAUDE.md, docs/ENFORCEMENT.md, and docs/GUIDES/LLM_ONBOARDING.md, ensuring all operations are based on actual repository state without assumptions.

## PHASE 0: Repository Instructions Discovery

### 0.1 Read Existing Cleanup Instructions
```bash
# First, check what the repository already says about cleanup
npx claude-flow@alpha hive-mind spawn \
  "Read and extract cleanup procedures from: \
   1) CLAUDE.md section on cleanup/vestigial files \
   2) docs/ENFORCEMENT.md for protected files \
   3) docs/GUIDES/LLM_ONBOARDING.md for vestigial audit \
   4) scripts/vestigial_audit.py if it exists \
   5) .claude-rules.json for file organization rules"
```

### 0.2 Document What Repository Says (No Assumptions)
Based on CLAUDE.md and LLM_ONBOARDING.md, the repository already has:
- Vestigial audit scripts
- Protected files list
- Cleanup targets defined
- File organization rules

## PHASE 1: Current State Analysis (Read-Only)

### 1.1 Discover Actual GitHub Actions Versions
```bash
# Don't assume versions - read actual files
echo "=== Checking actual GitHub Actions versions ==="
for workflow in .github/workflows/*.yml; do
  echo "File: $workflow"
  grep -E "uses: actions/|uses: peaceiris/" "$workflow" | grep -v "#"
done

# Check actual warnings from recent runs
gh run list --limit 5 --json conclusion,status,workflowName,createdAt
gh run view --log 2>/dev/null | grep -i "warning\|deprecated\|notice" | head -20
```

### 1.2 Discover Actual Dependencies
```bash
# Read current package.json - don't assume versions
echo "=== Current dependency versions ==="
cat package.json | jq '.dependencies'
cat package.json | jq '.devDependencies'

# Check what npm says about outdated packages
npm outdated --json > outdated-packages.json
cat outdated-packages.json

# Check for security issues
npm audit --json > audit-report.json
cat audit-report.json | jq '.metadata'
```

### 1.3 Discover Vestigial Files (Per Repository Rules)
```bash
# Use repository's own vestigial audit script if it exists
if [ -f "scripts/vestigial_audit.py" ]; then
  python scripts/vestigial_audit.py --full --report
else
  echo "No vestigial audit script found - will create file inventory"
fi

# Check for common vestigial patterns mentioned in CLAUDE.md
find . -type f -name "*.bak" 2>/dev/null
find . -type f -name "*.old" 2>/dev/null
find . -type f -name "*.tmp" 2>/dev/null
find . -type d -name "__pycache__" 2>/dev/null
find . -type d -name ".pytest_cache" 2>/dev/null
find . -type f -name "test-*.py" -path "*/scripts/*" 2>/dev/null
```

## PHASE 2: Update Plan Based on Discoveries

### 2.1 GitHub Actions Updates (Based on Actual Findings)
```yaml
# Template for updates - versions will be determined by discovery
# DO NOT assume v4 exists for all actions - check first

Update Process:
  1. Check current version in use
  2. Check latest available version
  3. Read changelog for breaking changes
  4. Update incrementally (v2→v3→v4)
  5. Test each change
```

### 2.2 Create Action Update Script (Discovers Versions)
```bash
#!/bin/bash
# smart-update-actions.sh

echo "🔍 Discovering GitHub Actions versions..."

# For each action, check what's available
for action in "actions/checkout" "actions/setup-node" "actions/upload-artifact"; do
  echo "Checking $action..."
  
  # Get current version in use
  current=$(grep -h "uses: $action@" .github/workflows/*.yml | \
            sed "s/.*$action@//" | sed 's/[[:space:]].*//' | \
            sort -u | head -1)
  
  echo "  Current: $current"
  
  # Get latest version from GitHub API
  latest=$(curl -s "https://api.github.com/repos/$action/releases/latest" | \
           jq -r '.tag_name')
  
  echo "  Latest: $latest"
  
  if [ "$current" != "$latest" ]; then
    echo "  ⚠️ Update available: $current → $latest"
  else
    echo "  ✅ Already on latest"
  fi
done
```

## PHASE 3: Vestigial File Cleanup (Following Repo Rules)

### 3.1 Read Repository's Cleanup Rules
Per CLAUDE.md and LLM_ONBOARDING.md:
```markdown
CLEANUP TARGETS (from repository documentation):
- Temporary troubleshooting scripts (validate-*.py, fix-*.py, test-*.py)
- Research/analysis files in /docs that are no longer needed
- Duplicate or superseded scripts in /scripts
- Test artifacts and temporary data files
- Old backup files or .bak extensions
- Unnecessary log files or debug outputs

CLEANUP RULES (from repository):
- NEVER delete production scripts without verification
- ALWAYS test site functionality after cleanup
- KEEP essential utilities and actively used tools
- PRESERVE documentation that provides value
- MAINTAIN scripts referenced in CLAUDE.md or README
```

### 3.2 Safe Cleanup Process
```bash
#!/bin/bash
# vestigial-cleanup.sh

echo "🧹 Vestigial File Cleanup (Following Repository Rules)"

# Create backup before any deletion
backup_dir="backups/cleanup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$backup_dir"

# Files to check (from repository rules)
echo "📋 Checking for vestigial files per CLAUDE.md..."

# 1. Find test/fix/validate scripts that might be temporary
find scripts -name "test-*.py" -o -name "fix-*.py" -o -name "validate-*.py" | \
while read -r file; do
  # Check if file is referenced in CLAUDE.md or README
  if grep -q "$(basename $file)" CLAUDE.md README.md 2>/dev/null; then
    echo "  KEEP: $file (referenced in documentation)"
  else
    echo "  REVIEW: $file (not referenced - candidate for removal)"
    cp "$file" "$backup_dir/"
  fi
done

# 2. Find old analysis/report files
find docs -name "*-analysis.json" -o -name "*-report.json" -mtime +30 | \
while read -r file; do
  echo "  OLD REPORT: $file (>30 days old)"
  cp "$file" "$backup_dir/"
done

# 3. Find Python cache directories
find . -type d -name "__pycache__" -o -name ".pytest_cache" | \
while read -r dir; do
  echo "  CACHE: $dir (safe to remove)"
  cp -r "$dir" "$backup_dir/"
done

# 4. Find backup files
find . -name "*.bak" -o -name "*.old" -o -name "*.tmp" | \
while read -r file; do
  echo "  BACKUP: $file"
  cp "$file" "$backup_dir/"
done

echo "✅ Files backed up to $backup_dir"
echo "Review the list above before deletion"
```

### 3.3 Validation Before Cleanup
```bash
# Pre-cleanup validation
echo "🔍 Pre-cleanup validation..."

# 1. Check current build status
npm run build
BUILD_STATUS=$?

# 2. Count current files
BEFORE_COUNT=$(find . -type f | wc -l)

# 3. Check MANIFEST.json is current
if [ -f "scripts/validate_manifest.py" ]; then
  python scripts/validate_manifest.py
fi

echo "Build status: $BUILD_STATUS"
echo "File count: $BEFORE_COUNT"
```

## PHASE 4: Dependency Updates (Conservative Approach)

### 4.1 Smart Dependency Update
```bash
#!/bin/bash
# smart-dependency-update.sh

echo "📦 Smart Dependency Updates"

# 1. Check for security vulnerabilities first
echo "🔒 Security audit..."
npm audit

# 2. Fix only security issues first
npm audit fix

# 3. Check what would be updated
echo "📊 Update analysis..."
npm outdated --long

# 4. Update only patch versions (safest)
echo "🔄 Updating patch versions..."
npm update --save

# 5. For each major update, check breaking changes
for pkg in $(npm outdated --json | jq -r 'keys[]'); do
  current=$(npm outdated --json | jq -r ".[\"$pkg\"].current")
  latest=$(npm outdated --json | jq -r ".[\"$pkg\"].latest")
  
  if [ "$current" != "$latest" ]; then
    echo "Package: $pkg ($current → $latest)"
    echo "Check changelog: https://github.com/search?q=$pkg+changelog"
    read -p "Update this package? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      npm install "$pkg@latest"
      npm run build
      if [ $? -ne 0 ]; then
        echo "❌ Build failed, reverting..."
        npm install "$pkg@$current"
      fi
    fi
  fi
done
```

## PHASE 5: Iterative Testing Strategy

### 5.1 Test After Each Change
```bash
#!/bin/bash
# iterative-test.sh

run_tests() {
  echo "🧪 Running test suite..."
  
  # 1. Build test
  npm run build || return 1
  
  # 2. Link validation
  if [ -f "scripts/link-validator.py" ]; then
    python scripts/link-validator.py || return 1
  fi
  
  # 3. Compliance check
  if [ -f "scripts/check_duplicates.py" ]; then
    python scripts/check_duplicates.py || return 1
  fi
  
  # 4. Manifest validation
  if [ -f "scripts/validate_manifest.py" ]; then
    python scripts/validate_manifest.py || return 1
  fi
  
  return 0
}

# Test after each phase
echo "Phase 1: After GitHub Actions update"
run_tests || exit 1

echo "Phase 2: After dependency updates"
run_tests || exit 1

echo "Phase 3: After vestigial cleanup"
run_tests || exit 1

echo "✅ All tests passed"
```

## PHASE 6: Documentation Updates

### 6.1 Update MANIFEST.json
```bash
# After all changes, update manifest
if [ -f "scripts/update_manifest.py" ]; then
  python scripts/update_manifest.py
else
  echo "Warning: No manifest update script found"
fi
```

### 6.2 Update CLAUDE.md
```markdown
## 📊 Last Maintenance Update

### Update Summary (Date: YYYY-MM-DD)
- GitHub Actions: Updated to latest versions
- Dependencies: Security patches applied
- Vestigial Files: X files removed
- Build Status: PASSING
- Tests: All passing

### Versions After Update:
- Node.js: [actual version]
- Eleventy: [actual version]
- Tailwind CSS: [actual version]
- GitHub Actions: [actual versions]
```

## EXECUTION COMMANDS

```bash
# Complete execution flow
npx claude-flow@alpha hive-mind spawn \
  "Execute comprehensive update and cleanup: \
   1) Read CLAUDE.md, ENFORCEMENT.md, LLM_ONBOARDING.md for procedures \
   2) Discover actual GitHub Actions versions in use \
   3) Check npm outdated and audit reports \
   4) Run vestigial_audit.py if it exists \
   5) Update only what needs updating based on discoveries \
   6) Clean only files matching repository's vestigial patterns \
   7) Test after each change \
   8) Update MANIFEST.json and documentation"
```

## SUCCESS CRITERIA

- [ ] All updates based on actual discovered versions
- [ ] Repository's cleanup rules followed exactly
- [ ] No assumptions about versions or files
- [ ] Tests pass after each phase
- [ ] Documentation updated with actual results
- [ ] Backup created before any deletions
- [ ] MANIFEST.json current
- [ ] Zero hallucinated version numbers

## KEY PRINCIPLES

1. **Discovery First**: Never assume versions - always check actual files
2. **Repository Rules**: Follow CLAUDE.md and existing scripts
3. **Incremental Updates**: One change at a time with testing
4. **Safe Cleanup**: Backup everything, verify references
5. **Document Reality**: Record what actually happened
```

This plan prioritizes discovering the actual state of the repository rather than making assumptions, follows the repository's own documented procedures for cleanup, and ensures everything is validated through testing at each step.