## Comprehensive Workflow Fix & Documentation Quality Assurance Prompt (`complete-workflow-docs-qa.md`)

```markdown
# Complete Workflow Remediation & Documentation Quality Assurance Mission

## OBJECTIVE
Systematically fix remaining workflow failures through iterative think-plan-implement-test cycles, clean up truly vestigial files, and ensure all documentation accurately reflects reality without exaggeration, following repository standards from CLAUDE.md.

## CONTEXT
- Current state: 5/9 workflows still failing (likely trivial issues)
- Critical workflows (build/deploy) are working
- Documentation may contain outdated claims or exaggerations
- Need careful vestigial cleanup (verify before deletion)

## PHASE 1: Think & Analyze (No Changes Yet)

### 1.1 Complete Workflow Analysis
```bash
# Get exact current state - no assumptions
echo "=== Current Workflow Status ($(date)) ==="
gh workflow list --all | while read -r line; do
  workflow_name=$(echo "$line" | awk '{print $1}')
  workflow_file=$(echo "$line" | awk '{print $NF}')
  
  # Get last 3 runs
  echo "\n📊 $workflow_name:"
  gh run list --workflow="$workflow_file" --limit=3 --json status,conclusion,createdAt | \
    jq -r '.[] | "\(.createdAt | split("T")[0]) - \(.conclusion // .status)"'
  
  # Get specific error if failing
  LAST_CONCLUSION=$(gh run list --workflow="$workflow_file" --limit=1 --json conclusion --jq '.[0].conclusion')
  if [ "$LAST_CONCLUSION" != "success" ] && [ "$LAST_CONCLUSION" != "" ]; then
    echo "  Error analysis:"
    gh run view --workflow="$workflow_file" --log-failed 2>&1 | grep -E "Error:|error:" | head -3
  fi
done
```

### 1.2 Categorize Failures by Root Cause
```yaml
Trivial Fixes (Quick):
  - Wrong action versions
  - Missing npm/pip install steps
  - Incorrect file paths
  
Dependency Issues (Medium):
  - Missing Python packages
  - Missing npm packages
  - Action compatibility
  
Logic Issues (Complex):
  - Script logic errors
  - Validation too strict
  - Configuration problems
```

## PHASE 2: Plan Fixes (Document Before Acting)

### 2.1 Create Fix Plan Document
```bash
# Generate fix plan before making changes
cat > workflow-fix-plan.md << 'EOF'
# Workflow Fix Plan
Generated: $(date)

## Failing Workflows Analysis

### Workflow 1: [Name]
- Last Status: [Failed/Success]
- Root Cause: [Specific issue]
- Proposed Fix: [Exact change needed]
- Risk Level: [Low/Medium/High]

### Workflow 2: [Name]
[Continue for each failing workflow]

## Implementation Order
1. Low-risk trivial fixes first
2. Test after each fix
3. Complex fixes last

## Rollback Plan
- Git branch: fix-workflows-$(date +%Y%m%d)
- Restore point before each change
EOF
```

## PHASE 3: Implement Fixes Iteratively

### 3.1 Fix One Workflow at a Time
```bash
#!/bin/bash
# iterative-workflow-fix.sh

echo "🔧 Iterative Workflow Fix Process"

# Create working branch
git checkout -b fix-workflows-$(date +%Y%m%d)

# Get list of failing workflows
FAILING_WORKFLOWS=$(gh workflow list --all | while read -r line; do
  workflow_file=$(echo "$line" | awk '{print $NF}')
  last_status=$(gh run list --workflow="$workflow_file" --limit=1 --json conclusion --jq '.[0].conclusion')
  [ "$last_status" != "success" ] && echo "$workflow_file"
done)

for workflow_file in $FAILING_WORKFLOWS; do
  echo "\n🔍 Analyzing $workflow_file"
  
  # Get specific error
  ERROR=$(gh run view --workflow="$workflow_file" --log-failed 2>&1 | head -20)
  
  # Apply targeted fix based on error pattern
  if echo "$ERROR" | grep -q "Cannot find module"; then
    echo "  Fix: Adding npm install step"
    # Add npm install to workflow
    
  elif echo "$ERROR" | grep -q "No module named"; then
    echo "  Fix: Adding pip install step"
    # Add pip install requirements.txt
    
  elif echo "$ERROR" | grep -q "Unable to resolve action"; then
    echo "  Fix: Updating action version"
    # Update to correct action version
    
  elif echo "$ERROR" | grep -q "Permission denied"; then
    echo "  Fix: Adding execution permissions"
    # Add chmod +x to scripts
    
  else
    echo "  Complex issue - needs manual review"
    echo "$ERROR" > "$workflow_file.error.log"
  fi
  
  # Test the fix
  echo "  Testing fix..."
  git add .
  git commit -m "fix: repair $workflow_file"
  gh workflow run "$workflow_file"
  
  # Wait and check result
  sleep 60
  NEW_STATUS=$(gh run list --workflow="$workflow_file" --limit=1 --json conclusion --jq '.[0].conclusion')
  
  if [ "$NEW_STATUS" = "success" ]; then
    echo "  ✅ Fixed!"
  else
    echo "  ❌ Still failing - trying alternative approach"
  fi
done
```

### 3.2 Common Targeted Fixes
```yaml
# Fix patterns to apply

Missing Dependencies:
  Python:
    - Add: run: pip install -r requirements.txt
    - Or: pip install requests pyyaml
  
  Node:
    - Add: run: npm ci
    - Or: npm install
  
Wrong Action Versions:
  Old: uses: actions/checkout@v2
  Fix: uses: actions/checkout@v4
  
  Old: uses: actions/setup-python@v2
  Fix: uses: actions/setup-python@v5
  
Missing Permissions:
  Add to workflow:
    permissions:
      contents: read
      issues: write
      pull-requests: write

Script Not Executable:
  Add before running script:
    - run: chmod +x scripts/*.py
```

## PHASE 4: Validate & Test

### 4.1 Comprehensive Testing
```bash
#!/bin/bash
# validate-all-workflows.sh

echo "✅ Validating All Workflows"

SUCCESS_COUNT=0
FAIL_COUNT=0
TOTAL_COUNT=0

# Test each workflow
for workflow in .github/workflows/*.yml; do
  name=$(basename "$workflow" .yml)
  ((TOTAL_COUNT++))
  
  echo "Testing $name..."
  
  # Syntax validation
  if ! grep -q "^name:" "$workflow"; then
    echo "  ⚠️ Missing workflow name"
  fi
  
  # Try to run it
  gh workflow run "$workflow" 2>/dev/null
  
  # Wait for completion
  sleep 30
  
  # Check result
  STATUS=$(gh run list --workflow="$workflow" --limit=1 --json conclusion --jq '.[0].conclusion')
  
  if [ "$STATUS" = "success" ]; then
    echo "  ✅ PASS"
    ((SUCCESS_COUNT++))
  else
    echo "  ❌ FAIL"
    ((FAIL_COUNT++))
  fi
done

echo "\nResults: $SUCCESS_COUNT/$TOTAL_COUNT passing"
```

## PHASE 5: Documentation Quality Assurance

### 5.1 Scan Documentation for Exaggerations
```bash
# Check for hyperbolic claims
echo "📝 Documentation Quality Check"

# Patterns that might indicate exaggeration
EXAGGERATION_PATTERNS=(
  "revolutionary"
  "game-changing"
  "cutting-edge"
  "state-of-the-art"
  "best-in-class"
  "industry-leading"
  "100% secure"
  "unhackable"
  "perfect"
  "always"
  "never fails"
)

for pattern in "${EXAGGERATION_PATTERNS[@]}"; do
  echo "Checking for '$pattern'..."
  grep -r -i "$pattern" docs/ README.md 2>/dev/null && \
    echo "  ⚠️ Found potential exaggeration"
done

# Check for outdated statistics
echo "\nChecking for outdated claims..."
grep -r -E "\b20[12][0-9]\b" docs/ README.md | \
  grep -v "$(date +%Y)" && \
    echo "  ⚠️ Found potentially outdated year references"
```

### 5.2 Update Documentation Accurately
```python
#!/usr/bin/env python3
# update-documentation-accurately.py

import os
import re
from pathlib import Path

def fix_documentation(filepath):
    """Fix documentation to be accurate and modest"""
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    original = content
    
    # Fix exaggerations
    replacements = {
        r'revolutionary': 'improved',
        r'cutting-edge': 'modern',
        r'state-of-the-art': 'current',
        r'100% secure': 'security-focused',
        r'perfect': 'effective',
        r'always': 'typically',
        r'never fails': 'reliable',
        r'blazing fast': 'performant',
        r'game-changing': 'useful'
    }
    
    for old, new in replacements.items():
        content = re.sub(old, new, content, flags=re.IGNORECASE)
    
    # Update statistics to be current
    content = re.sub(
        r'(\d+)\+?\s*(blog posts|posts|articles)',
        lambda m: f"{count_blog_posts()} blog posts",
        content
    )
    
    # Fix workflow counts
    actual_workflows = len(list(Path('.github/workflows').glob('*.yml')))
    content = re.sub(
        r'\d+\s*workflows?',
        f'{actual_workflows} workflows',
        content
    )
    
    if content != original:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated: {filepath}")

def count_blog_posts():
    """Get actual blog post count"""
    posts = Path('src/posts').glob('*.md')
    return len(list(posts))

# Process all documentation
for doc_file in Path('.').rglob('*.md'):
    if 'node_modules' not in str(doc_file):
        fix_documentation(doc_file)
```

## PHASE 6: Vestigial Cleanup (With Verification)

### 6.1 Safe Vestigial Identification
```bash
#!/bin/bash
# safe-vestigial-cleanup.sh

echo "🧹 Safe Vestigial File Cleanup"

# Create safety backup
BACKUP_DIR="backups/pre-cleanup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Find candidates but verify each
echo "Analyzing vestigial candidates..."

# Temporary files (safe to remove)
find . -name "*.tmp" -o -name "*.bak" -o -name "*.old" | while read -r file; do
  echo "Temporary file: $file"
  cp "$file" "$BACKUP_DIR/"
  # Will remove after verification
done

# Python cache (safe to remove)
find . -type d -name "__pycache__" | while read -r dir; do
  echo "Python cache: $dir"
  cp -r "$dir" "$BACKUP_DIR/"
  rm -rf "$dir"
done

# Check for orphaned scripts
for script in scripts/*.py; do
  name=$(basename "$script")
  
  # Check if referenced anywhere
  if ! grep -r "$name" . --exclude-dir=.git --exclude="$script" > /dev/null 2>&1; then
    echo "Possibly orphaned: $script"
    
    # But verify it's not needed
    if [[ "$name" =~ ^(test-|temp-|old-|backup-) ]]; then
      echo "  Confirmed vestigial (prefix indicates temporary)"
      cp "$script" "$BACKUP_DIR/"
      # Will remove after final check
    else
      echo "  Keeping (might be utility script)"
    fi
  fi
done

echo "Backup created at: $BACKUP_DIR"
echo "Review candidates before deletion"
```

## PHASE 7: Final Validation

### 7.1 Complete System Check
```bash
# Final validation of everything
echo "🎯 Final System Validation"

# 1. All workflows status
echo "Workflows:"
gh workflow list --all

# 2. Documentation accuracy
echo "\nDocumentation:"
grep -c "blog posts" README.md
ls src/posts/*.md | wc -l

# 3. Build still works
echo "\nBuild:"
npm run build

# 4. No broken internal links
echo "\nLinks:"
python scripts/link-validator.py

# 5. Compliance maintained
echo "\nCompliance:"
python scripts/compliance-check.py
```

## EXECUTION COMMANDS

```bash
# Complete iterative fix and documentation QA
npx claude-flow@alpha hive-mind spawn \
  "Execute complete workflow and documentation quality mission: \
   THINK: Analyze all 5 failing workflows to identify exact issues \
   PLAN: Document specific fixes needed for each workflow \
   IMPLEMENT: Fix one workflow at a time with testing \
   VALIDATE: Ensure each fix works before moving on \
   TEST: Run comprehensive validation after all fixes \
   MONITOR: Watch workflows until all complete successfully \
   FIX: Address any new issues that arise \
   CLEANUP: Remove truly vestigial files with verification \
   DOCUMENTATION: Update all docs to be accurate without exaggeration \
   Follow CLAUDE.md standards throughout. Use discretion for quality."

# Monitor until all green
npx claude-flow@alpha swarm \
  "Monitor workflows continuously until all succeed: \
   Watch each workflow run → \
   If failure, diagnose specific issue → \
   Apply targeted fix → \
   Test immediately → \
   Continue until all workflows green → \
   Generate success report"
```

## SUCCESS CRITERIA

- [ ] All 9 workflows passing or properly disabled
- [ ] No documentation contains exaggerations
- [ ] All statistics and counts are current
- [ ] Vestigial files removed with backups
- [ ] Build time remains <3 seconds
- [ ] All internal links working
- [ ] Compliance at 100%
- [ ] Clear audit trail of changes

This comprehensive approach ensures systematic fixes while maintaining quality and accuracy throughout the repository.