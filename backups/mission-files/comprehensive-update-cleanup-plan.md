
# Vulnerability Remediation & CI/CD Monitoring Mission

## OBJECTIVE
Fix all security vulnerabilities (including Dependabot alerts), monitor GitHub Actions until fully green, and resolve any issues following repository rules from CLAUDE.md, ENFORCEMENT.md, and established procedures.

## CONTEXT
Previous update completed successfully but GitHub has detected 1 moderate vulnerability via Dependabot. Need to address this and ensure all GitHub Actions complete successfully with zero issues.

## PHASE 1: Vulnerability Assessment

### 1.1 Check Dependabot Alerts
```bash
# Get current Dependabot alerts
gh api /repos/williamzujkowski/williamzujkowski.github.io/dependabot/alerts \
  --jq '.[] | {package: .security_advisory.summary, severity: .security_advisory.severity, vulnerable_version: .security_vulnerability.vulnerable_version_range}'

# Check security advisories
gh api /repos/williamzujkowski/williamzujkowski.github.io/dependabot/alerts \
  --jq '.[] | .security_advisory.references[].url'

# View specific alert details
gh api /repos/williamzujkowski/williamzujkowski.github.io/dependabot/alerts/1
```

### 1.2 Analyze NPM Audit
```bash
# Detailed vulnerability report
npm audit --json > vulnerability-report.json
cat vulnerability-report.json | jq '.vulnerabilities'

# Check if fix is available
npm audit fix --dry-run

# Check specific package versions
npm ls --depth=0 | grep -E "(high|critical|moderate)"
```

## PHASE 2: Strategic Fix Approach

### 2.1 Follow Repository Rules
Per CLAUDE.md enforcement:
```yaml
Fix Priority:
  1. Critical vulnerabilities - Immediate
  2. High vulnerabilities - Same day
  3. Moderate vulnerabilities - Within sprint
  4. Low vulnerabilities - Next maintenance window

Fix Process:
  1. Backup current state
  2. Test fix in isolation
  3. Apply fix incrementally
  4. Validate build and tests
  5. Monitor production
```

### 2.2 Safe Vulnerability Fix Script
```bash
#!/bin/bash
# fix-vulnerabilities.sh

echo "🔒 Security Vulnerability Remediation"
echo "Following CLAUDE.md procedures..."

# Create restore point
git checkout -b security-fix-$(date +%Y%m%d)
cp package.json package.json.security-backup
cp package-lock.json package-lock.json.security-backup

# Get vulnerability details
echo "📊 Current vulnerabilities:"
npm audit

# Try automatic fix first
echo "🔧 Attempting automatic fix..."
npm audit fix

# Check if vulnerabilities remain
REMAINING=$(npm audit --json | jq '.metadata.vulnerabilities.total')

if [ "$REMAINING" -gt 0 ]; then
  echo "⚠️ Manual intervention required for $REMAINING vulnerabilities"
  
  # Force fixes if safe
  read -p "Force fix remaining vulnerabilities? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    npm audit fix --force
  else
    # Manual resolution
    echo "📝 Manual resolution needed:"
    npm audit --json | jq '.vulnerabilities | to_entries[] | {
      package: .key,
      severity: .value.severity,
      fix: .value.fixAvailable
    }'
  fi
fi

# Validate fix didn't break anything
echo "✅ Validating fixes..."
npm run build || {
  echo "❌ Build failed, reverting..."
  mv package.json.security-backup package.json
  mv package-lock.json.security-backup package-lock.json
  npm install
  exit 1
}

echo "✅ Vulnerabilities fixed successfully"
```

## PHASE 3: GitHub Actions Monitoring

### 3.1 Continuous Monitoring Script
```bash
#!/bin/bash
# monitor-github-actions.sh

echo "👁️ GitHub Actions Continuous Monitor"

# Trigger a fresh run
echo "🚀 Triggering fresh workflow run..."
gh workflow run build.yml

# Get the run ID
sleep 5
RUN_ID=$(gh run list --limit 1 --json databaseId --jq '.[0].databaseId')

echo "📊 Monitoring run $RUN_ID..."

# Monitor until completion
while true; do
  STATUS=$(gh run view $RUN_ID --json status --jq '.status')
  CONCLUSION=$(gh run view $RUN_ID --json conclusion --jq '.conclusion')
  
  echo "Status: $STATUS"
  
  if [ "$STATUS" = "completed" ]; then
    if [ "$CONCLUSION" = "success" ]; then
      echo "✅ Workflow completed successfully!"
      break
    else
      echo "❌ Workflow failed with conclusion: $CONCLUSION"
      echo "Fetching logs..."
      gh run view $RUN_ID --log-failed
      
      # Auto-fix common issues
      ./auto-fix-ci-issues.sh $RUN_ID
    fi
  fi
  
  sleep 30
done
```

### 3.2 Auto-Fix Common CI Issues
```bash
#!/bin/bash
# auto-fix-ci-issues.sh

RUN_ID=$1

echo "🔧 Attempting auto-fix for run $RUN_ID"

# Get failure reason
LOGS=$(gh run view $RUN_ID --log 2>&1)

# Common fixes
if echo "$LOGS" | grep -q "npm ERR! code ENOENT"; then
  echo "Fix: Missing dependencies"
  rm -rf node_modules package-lock.json
  npm install
  git add package-lock.json
  git commit -m "fix: regenerate package-lock.json"
  git push
  
elif echo "$LOGS" | grep -q "Error: Process completed with exit code 1"; then
  echo "Fix: Build error"
  npm run build:debug
  
elif echo "$LOGS" | grep -q "Node.js 16 actions are deprecated"; then
  echo "Fix: Update action versions"
  for workflow in .github/workflows/*.yml; do
    sed -i 's/@v3/@v4/g' "$workflow"
  done
  git add .github/workflows/
  git commit -m "fix: update action versions to v4"
  git push
  
elif echo "$LOGS" | grep -q "rate limit"; then
  echo "Fix: Rate limit hit, waiting..."
  sleep 3600
  
else
  echo "Unknown issue, manual intervention required"
  echo "$LOGS" > ci-failure-log.txt
  echo "Logs saved to ci-failure-log.txt"
fi
```

## PHASE 4: Dependabot Configuration

### 4.1 Configure Dependabot Properly
```yaml
# .github/dependabot.yml
version: 2
updates:
  # NPM dependencies
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
      day: "monday"
      time: "04:00"
    open-pull-requests-limit: 5
    reviewers:
      - "williamzujkowski"
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "chore"
      prefix-development: "chore"
      include: "scope"
    ignore:
      # Ignore major versions that might break
      - dependency-name: "@11ty/eleventy"
        update-types: ["version-update:semver-major"]
      - dependency-name: "tailwindcss"
        update-types: ["version-update:semver-major"]

  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    labels:
      - "ci/cd"
      - "dependencies"
```

### 4.2 Auto-Merge Safe Updates
```yaml
# .github/workflows/auto-merge-dependabot.yml
name: Auto-merge Dependabot PRs

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: github.actor == 'dependabot[bot]'
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Check if safe to merge
        id: check
        run: |
          # Only auto-merge patch and minor updates
          if [[ "${{ github.event.pull_request.title }}" =~ "patch" ]] || 
             [[ "${{ github.event.pull_request.title }}" =~ "minor" ]]; then
            echo "safe=true" >> $GITHUB_OUTPUT
          fi
      
      - name: Auto-merge
        if: steps.check.outputs.safe == 'true'
        run: |
          gh pr review --approve "${{ github.event.pull_request.number }}"
          gh pr merge --auto --squash "${{ github.event.pull_request.number }}"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## PHASE 5: Complete Monitoring Loop

### 5.1 Full Resolution Workflow
```bash
#!/bin/bash
# complete-security-resolution.sh

echo "🛡️ Complete Security Resolution Workflow"

# Step 1: Fix vulnerabilities
echo "Step 1: Fixing vulnerabilities..."
./fix-vulnerabilities.sh || exit 1

# Step 2: Commit fixes
echo "Step 2: Committing fixes..."
git add package*.json
git commit -m "fix: resolve security vulnerabilities

- Fixed Dependabot alert #1
- Updated vulnerable dependencies
- Passed all security audits"

# Step 3: Push and monitor
echo "Step 3: Pushing fixes..."
git push origin security-fix-$(date +%Y%m%d)

# Step 4: Create PR
echo "Step 4: Creating pull request..."
gh pr create \
  --title "fix: resolve security vulnerabilities" \
  --body "Fixes Dependabot alerts and npm audit issues" \
  --label "security"

# Step 5: Monitor CI
echo "Step 5: Monitoring CI/CD..."
PR_NUMBER=$(gh pr view --json number --jq '.number')

# Wait for checks
while true; do
  CHECK_STATUS=$(gh pr checks $PR_NUMBER --json status --jq '.[].status' | sort -u)
  
  echo "Check status: $CHECK_STATUS"
  
  if [[ "$CHECK_STATUS" == "COMPLETED" ]]; then
    CHECK_CONCLUSION=$(gh pr checks $PR_NUMBER --json conclusion --jq '.[].conclusion' | sort -u)
    
    if [[ "$CHECK_CONCLUSION" == "SUCCESS" ]]; then
      echo "✅ All checks passed!"
      
      # Auto-merge if safe
      echo "Merging PR..."
      gh pr merge $PR_NUMBER --squash --delete-branch
      break
    else
      echo "❌ Checks failed"
      gh pr checks $PR_NUMBER
      
      # Try to fix
      ./auto-fix-ci-issues.sh
    fi
  fi
  
  sleep 60
done

echo "✅ Security resolution complete!"
```

## PHASE 6: Validation & Reporting

### 6.1 Final Validation
```bash
# Confirm all issues resolved
echo "🔍 Final validation..."

# No vulnerabilities
npm audit --audit-level=low
VULNS=$(npm audit --json | jq '.metadata.vulnerabilities.total')

# All Actions green
FAILED_RUNS=$(gh run list --limit 10 --json conclusion | jq '[.[] | select(.conclusion != "success")] | length')

# Dependabot happy
OPEN_ALERTS=$(gh api /repos/williamzujkowski/williamzujkowski.github.io/dependabot/alerts | jq '. | length')

if [[ "$VULNS" -eq 0 ]] && [[ "$FAILED_RUNS" -eq 0 ]] && [[ "$OPEN_ALERTS" -eq 0 ]]; then
  echo "✅ All security issues resolved!"
else
  echo "⚠️ Issues remain:"
  echo "  Vulnerabilities: $VULNS"
  echo "  Failed runs: $FAILED_RUNS"  
  echo "  Open alerts: $OPEN_ALERTS"
fi
```

### 6.2 Generate Report
```markdown
## Security Resolution Report
Date: $(date)

### Vulnerabilities Fixed
- Total fixed: X
- Critical: 0
- High: 0
- Moderate: X
- Low: X

### GitHub Actions Status
- All workflows: ✅ Green
- Last successful run: [link]
- Build time: X seconds

### Dependabot Status
- Open alerts: 0
- Auto-merge enabled: Yes
- Next scan: [date]

### Repository Health
- Build: ✅ Passing
- Tests: ✅ All passing
- Security: ✅ No vulnerabilities
- Compliance: ✅ 100% with CLAUDE.md
```

## EXECUTION COMMANDS

```bash
# Complete vulnerability fix and monitoring
npx claude-flow@alpha hive-mind spawn \
  "Execute vulnerability fix and monitoring mission: \
   1) Read and fix Dependabot alert #1 \
   2) Run npm audit and fix all issues \
   3) Monitor GitHub Actions until green \
   4) Auto-fix any CI/CD issues \
   5) Validate zero vulnerabilities remain \
   6) Generate security report \
   Follow CLAUDE.md and ENFORCEMENT.md procedures throughout"

# Continuous monitoring loop
npx claude-flow@alpha swarm \
  "Monitor GitHub Actions continuously: \
   Watch all workflow runs, \
   Identify failures immediately, \
   Apply automatic fixes for known issues, \
   Re-run until all green, \
   Report final status"
```

## SUCCESS CRITERIA

- [ ] Zero npm vulnerabilities (audit clean)
- [ ] All Dependabot alerts resolved
- [ ] All GitHub Actions passing
- [ ] No deprecation warnings
- [ ] Build time < 3 seconds
- [ ] All tests passing
- [ ] Compliance maintained at 100%
- [ ] Security report generated
