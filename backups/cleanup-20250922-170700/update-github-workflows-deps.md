# GitHub Workflows & Dependencies Modernization Plan

## OBJECTIVE
Systematically review, update, and test all GitHub Actions workflows and project dependencies to ensure they use current supported versions, following the repository's documented processes in CLAUDE.md and docs/guides/LLM_ONBOARDING.md.

## PHASE 1: Documentation Review & Current State Audit

### 1.1 Read Repository Standards
```bash
# First, understand the repository's update processes
npx claude-flow@alpha hive-mind spawn \
  "Read and analyze: \
   1) CLAUDE.md - Check for dependency update procedures \
   2) docs/guides/LLM_ONBOARDING.md - Review maintenance workflows \
   3) docs/ENFORCEMENT.md - Understand validation requirements \
   4) package.json - Note current Node/npm dependencies \
   5) .github/workflows/*.yml - List all workflow files"
```

### 1.2 Audit Current GitHub Workflows
```bash
# Check workflow runs for deprecation warnings
gh run list --limit 10 --json conclusion,status,name,createdAt | jq '.'

# View recent workflow logs for warnings
gh run view --log | grep -i "deprecated\|warning\|notice"

# List all workflows
ls -la .github/workflows/

# Check each workflow for outdated actions
grep -h "uses:" .github/workflows/*.yml | sort -u
```

### 1.3 Identify Deprecated Actions
Common deprecated actions to look for:
```yaml
# OLD (deprecated)
- uses: actions/checkout@v2  # Should be v4
- uses: actions/setup-node@v2  # Should be v4
- uses: actions/upload-artifact@v2  # Should be v4
- uses: actions/download-artifact@v2  # Should be v4
- uses: actions/cache@v2  # Should be v4
- uses: peaceiris/actions-gh-pages@v3  # Check for v4

# Node 12/16 deprecation warnings
- uses: actions/setup-node@v3
  with:
    node-version: 12  # Node 12 is EOL
    node-version: 16  # Node 16 is EOL, use 18 or 20
```

## PHASE 2: Dependency Analysis

### 2.1 Check npm Dependencies
```bash
# Check for outdated npm packages
npm outdated

# Audit for vulnerabilities
npm audit

# Check which dependencies need major updates
npm outdated --long

# Review package.json
cat package.json | jq '.dependencies, .devDependencies'
```

### 2.2 Analyze Eleventy & Tailwind Versions
```bash
# Current versions in use
npm list @11ty/eleventy tailwindcss postcss

# Check latest available versions
npm view @11ty/eleventy version
npm view tailwindcss version
npm view postcss version

# Check for breaking changes
npm info @11ty/eleventy versions --json | tail -20
```

## PHASE 3: Iterative Update Strategy

### 3.1 GitHub Actions Updates (Priority 1)
```yaml
# Update workflow template
name: Update GitHub Actions Workflow

# Step 1: Update checkout action
- name: Checkout repository
  uses: actions/checkout@v4  # Updated from v2/v3
  with:
    fetch-depth: 0  # Full history for better compatibility

# Step 2: Update Node setup
- name: Setup Node.js
  uses: actions/setup-node@v4  # Updated from v2/v3
  with:
    node-version: '20'  # Use Node 20 LTS
    cache: 'npm'  # Built-in caching

# Step 3: Update artifact handling
- name: Upload artifact
  uses: actions/upload-artifact@v4
  with:
    name: build-output
    path: _site/
    retention-days: 30  # Specify retention

# Step 4: Update GitHub Pages deployment
- name: Deploy to GitHub Pages
  uses: peaceiris/actions-gh-pages@v4  # Check latest version
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./_site
```

### 3.2 Progressive Update Process
```bash
# Create update branch
git checkout -b chore/update-github-actions

# Update one workflow at a time
# 1. Update build.yml first (least risky)
# 2. Test locally with act
act -l  # List workflows
act -j build  # Test build job

# 3. Commit and create PR
git add .github/workflows/build.yml
git commit -m "chore: update build workflow to use actions v4"

# 4. Monitor PR checks
gh pr create --title "chore: update GitHub Actions to v4" \
  --body "Updates deprecated GitHub Actions to latest versions"

# 5. After merge, monitor for issues
gh run watch
```

## PHASE 4: Dependency Updates

### 4.1 Safe Update Order
```bash
# 1. Update patch versions first (safest)
npm update

# 2. Update Tailwind and PostCSS (check for breaking changes)
npm install tailwindcss@latest postcss@latest autoprefixer@latest

# 3. Test build
npm run build

# 4. Update Eleventy (may have breaking changes)
npm install @11ty/eleventy@latest

# 5. Test thoroughly
npm run serve
npm run build
```

### 4.2 Testing Matrix
```yaml
Test Checklist:
  Local Development:
    - [ ] npm install succeeds
    - [ ] npm run serve works
    - [ ] npm run build completes
    - [ ] No console errors
    - [ ] Dark mode toggles
    - [ ] Navigation works
    
  CI/CD Pipeline:
    - [ ] GitHub Actions run successfully
    - [ ] No deprecation warnings
    - [ ] Build artifacts generated
    - [ ] Deployment succeeds
    
  Production:
    - [ ] Site loads correctly
    - [ ] All pages accessible
    - [ ] Images load
    - [ ] Links work
    - [ ] Performance unchanged
```

## PHASE 5: Implementation Commands

### 5.1 Automated Update Script
```bash
#!/bin/bash
# update-workflows.sh

echo "🔄 Updating GitHub Workflows and Dependencies"

# Check current state
echo "📊 Current workflow runs:"
gh run list --limit 5

# Check for warnings
echo "⚠️ Checking for deprecation warnings:"
gh run view --log | grep -E "(deprecated|warning)" | head -20

# Update workflows
echo "📝 Updating workflow files:"
for workflow in .github/workflows/*.yml; do
  echo "Processing $workflow"
  
  # Update actions versions
  sed -i 's/actions\/checkout@v[23]/actions\/checkout@v4/g' "$workflow"
  sed -i 's/actions\/setup-node@v[23]/actions\/setup-node@v4/g' "$workflow"
  sed -i 's/actions\/upload-artifact@v[23]/actions\/upload-artifact@v4/g' "$workflow"
  sed -i 's/actions\/download-artifact@v[23]/actions\/download-artifact@v4/g' "$workflow"
  sed -i 's/actions\/cache@v[23]/actions\/cache@v4/g' "$workflow"
  
  # Update Node version
  sed -i 's/node-version: 1[246]/node-version: 20/g' "$workflow"
done

echo "✅ Workflow files updated"
```

### 5.2 Dependency Update Script
```bash
#!/bin/bash
# update-dependencies.sh

echo "📦 Updating npm dependencies"

# Backup current state
cp package.json package.json.backup
cp package-lock.json package-lock.json.backup

# Update npm itself
npm install -g npm@latest

# Clear cache
npm cache clean --force

# Update dependencies
echo "1️⃣ Updating patch versions..."
npm update

echo "2️⃣ Checking for major updates..."
npm outdated

echo "3️⃣ Updating build tools..."
npm install --save-dev \
  tailwindcss@latest \
  postcss@latest \
  autoprefixer@latest \
  @11ty/eleventy@latest

echo "4️⃣ Running audit fix..."
npm audit fix

echo "5️⃣ Testing build..."
npm run build

if [ $? -eq 0 ]; then
  echo "✅ Build successful"
  rm package.json.backup package-lock.json.backup
else
  echo "❌ Build failed, restoring backup"
  mv package.json.backup package.json
  mv package-lock.json.backup package-lock.json
  npm install
fi
```

## PHASE 6: Validation & Monitoring

### 6.1 Post-Update Validation
```bash
# Local validation
npm test
npm run build
npm run serve

# Check for remaining warnings
npm ls  # Check for peer dependency issues
npm audit  # Security check

# GitHub Actions validation
gh workflow run build.yml
gh run watch

# Production validation
curl -I https://williamzujkowski.github.io
lighthouse https://williamzujkowski.github.io --output=json
```

### 6.2 Monitoring Plan
```yaml
Daily Checks:
  - GitHub Actions status dashboard
  - Dependabot alerts
  - Build time metrics
  - Error logs

Weekly Reviews:
  - npm audit report
  - Deprecation warnings in logs
  - Performance metrics
  - New releases of key dependencies

Monthly Updates:
  - Dependency updates (patch/minor)
  - Security patches
  - GitHub Actions version bumps

Quarterly Reviews:
  - Major version updates
  - Framework migrations
  - Tool evaluations
```

## ROLLBACK PLAN

If updates cause issues:
```bash
# Quick rollback
git revert HEAD
git push

# Or restore from backup branch
git checkout main
git reset --hard backup/pre-update

# Restore npm packages
rm -rf node_modules package-lock.json
npm install

# Re-deploy previous version
gh workflow run deploy.yml --ref stable
```

## SUCCESS CRITERIA

- [ ] All GitHub Actions using v4 or latest
- [ ] Zero deprecation warnings in workflow logs
- [ ] Node.js 20 LTS in use
- [ ] All npm dependencies up to date
- [ ] npm audit shows 0 vulnerabilities
- [ ] Build time ≤ previous baseline
- [ ] All tests passing
- [ ] Site functionality unchanged
- [ ] Lighthouse scores maintained or improved

## EXECUTION SEQUENCE

1. **Hour 1**: Audit and document current state
2. **Hour 2**: Update GitHub Actions workflows
3. **Hour 3**: Test and deploy workflow updates
4. **Hour 4**: Update npm dependencies (minor/patch)
5. **Hour 5**: Test dependency updates locally
6. **Hour 6**: Deploy and monitor production
7. **Hour 7**: Update documentation
8. **Hour 8**: Final validation and cleanup
```

## Claude-Flow Commands for Execution

```bash
# Phase 1: Initial Audit
npx claude-flow@alpha hive-mind spawn \
  "Following CLAUDE.md and LLM_ONBOARDING.md procedures: \
   1) Review .github/workflows for deprecated actions \
   2) Check recent workflow runs for warnings \
   3) Audit npm dependencies for updates \
   4) Generate comprehensive update plan"

# Phase 2: Update GitHub Actions
npx claude-flow@alpha swarm \
  "Update all GitHub Actions workflows: \
   1) Update to actions/checkout@v4 \
   2) Update to actions/setup-node@v4 \
   3) Set Node version to 20 LTS \
   4) Fix any deprecation warnings \
   5) Test with local act tool"

# Phase 3: Update Dependencies
npx claude-flow@alpha hive-mind spawn \
  "Update npm dependencies safely: \
   1) Run npm audit and fix issues \
   2) Update Tailwind/PostCSS to latest \
   3) Update Eleventy if compatible \
   4) Test build thoroughly \
   5) Validate no regressions"

# Phase 4: Complete Testing
npx claude-flow@alpha verify content \
  "Validate all updates: \
   Run full test suite, check build times, \
   verify GitHub Actions, test production deploy"
