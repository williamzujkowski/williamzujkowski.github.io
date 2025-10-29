# Phase 6 Maintenance System Runbook

**Version:** 1.0.0
**Last Updated:** 2025-10-29
**Status:** Production
**Owner:** William Zujkowski

---

## Overview

This runbook provides operational procedures for maintaining the blog humanization system established in Phase 6. It ensures zero-maintenance overhead while sustaining 95%+ passing rates over 6+ months.

## System Components

### 1. Humanization Validator v2.0
- **Location:** `scripts/blog-content/humanization-validator.py`
- **Version:** 2.0.0
- **Performance:** 0.67s for 57 posts (155x faster than v1.0)
- **Scoring:** Base 100 + bonuses up to +10 for measurements

### 2. Monthly Validation Automation
- **Location:** `scripts/maintenance/monthly-portfolio-validation.sh`
- **Schedule:** 1st of every month at 2:00 AM
- **Reports:** `reports/monthly/validation-YYYY-MM.json`
- **Logs:** `/home/william/git/williamzujkowski.github.io/logs/monthly-validation.log`

### 3. Post Template System
- **Location:** `src/templates/blog-post-template.md`
- **Expected Baseline:** 80-90/100 on first draft
- **Supporting Docs:** 4 guides (56.8KB total)

### 4. Pre-commit Hooks
- **Location:** `.git/hooks/pre-commit`
- **Function:** Validates all staged posts before commit
- **Threshold:** ≥75/100 required to commit

---

## Routine Operations

### Monthly Review (5-10 minutes)

**When:** First week of each month
**Trigger:** Monthly cron job completion notification

#### Procedure:

```bash
# 1. Check latest monthly report
cat reports/monthly/summary-$(date +%Y-%m).txt

# 2. Review comparison with previous month
cat reports/monthly/comparison-$(date +%Y-%m).txt

# 3. If no failing posts, done! If failures exist, proceed to investigation.
```

**Expected Output:**
```
Portfolio Health Report - 2025-10
===================================
Passing: 57/57
Average Score: 104.2
```

**Action Required:**
- **All passing:** No action needed
- **1-2 failing:** Review individual posts (see troubleshooting)
- **3+ failing:** Escalate to full portfolio audit (see section below)

---

### New Post Creation (30-45 minutes)

**When:** Creating any new blog post
**Template:** `src/templates/blog-post-template.md`

#### Procedure:

```bash
# 1. Copy template to posts directory
cp src/templates/blog-post-template.md src/posts/YYYY-MM-DD-your-slug.md

# 2. Write content following embedded checklist
# (Aim for 80-90/100 on first draft)

# 3. Validate before committing
python scripts/blog-content/humanization-validator.py --post src/posts/YYYY-MM-DD-your-slug.md

# 4. If score ≥75/100, commit (pre-commit hook will re-validate)
git add src/posts/YYYY-MM-DD-your-slug.md
git commit -m "feat: Add post about [topic]"
```

**Expected Results:**
- **First draft:** 80-90/100 (using template)
- **After minor edits:** 90-100/100
- **With measurement bonus:** Up to 110/100

**Quick Reference Docs:**
- `docs/guides/USING_POST_TEMPLATE.md` (detailed guidance)
- `docs/guides/HUMANIZATION_QUICK_REFERENCE.md` (one-page cheat sheet)

---

### Weekly Spot Check (Optional, 2 minutes)

**When:** Weekly (e.g., every Monday morning)
**Purpose:** Early detection of issues

```bash
# Quick portfolio health check
python scripts/blog-content/humanization-validator.py --batch --format summary
```

**Expected Output:**
```
Total Posts:    57
Passed:        57 (100.0%)
Failed:         0 (0.0%)
Average Score: 104.2
```

**Action Required:**
- **Same as last check:** No action
- **Drop in average ≥5 points:** Investigate (see troubleshooting)
- **New failures:** Review individual posts

---

## Troubleshooting Guide

### Issue 1: Post Suddenly Failing (<75/100)

**Symptoms:**
- Post previously passed
- Now scores <75/100
- No recent edits to post

**Diagnosis Steps:**

```bash
# 1. Get detailed validation report
python scripts/blog-content/humanization-validator.py --post src/posts/YYYY-MM-DD-post.md

# 2. Compare with previous validation report
git show HEAD:reports/monthly/validation-$(date -d "last month" +%Y-%m).json | \
  jq '.results[] | select(.post_path == "src/posts/YYYY-MM-DD-post.md")'

# 3. Check for validator changes
git log --oneline scripts/blog-content/humanization-validator.py | head -5
```

**Common Causes:**
1. **Validator pattern updates:** Check if thresholds changed
2. **Frontmatter metadata missing:** Verify date, tags, description present
3. **External link rot:** Citation links may have broken
4. **File encoding issues:** Ensure UTF-8 encoding

**Resolution:**
- Review violation details from validation report
- Apply targeted fixes (see "Common Fixes" below)
- Re-validate before committing

---

### Issue 2: Average Portfolio Score Dropped ≥5 Points

**Symptoms:**
- Previous average: 105.4/100
- Current average: 100.0/100 or lower
- No obvious failing posts

**Diagnosis:**

```bash
# 1. Generate comparison report
python scripts/blog-content/humanization-validator.py --batch \
  --compare reports/monthly/validation-$(date -d "last month" +%Y-%m).json \
  --save-report reports/current-diagnosis.json

# 2. Identify posts with score drops
jq '.results[] | select(.score < .previous_score - 5)' reports/current-diagnosis.json

# 3. Review validator changes
git log --stat --since="1 month ago" -- scripts/blog-content/humanization-validator.py
```

**Common Causes:**
1. **Validator scoring changes:** New bonus criteria or thresholds
2. **Pattern library updates:** `humanization-patterns.yaml` modified
3. **Mass content changes:** Recent edits to multiple posts
4. **Dependency updates:** Python package changes affecting regex

**Resolution:**
- If validator changes are intentional: update baselines
- If unintentional: revert validator changes
- If content-related: review affected posts individually

---

### Issue 3: Monthly Cron Job Failed

**Symptoms:**
- No new report in `reports/monthly/`
- Email notification not received
- Log file shows errors

**Diagnosis:**

```bash
# 1. Check cron job status
systemctl status cron

# 2. Review log file
tail -50 /home/william/git/williamzujkowski.github.io/logs/monthly-validation.log

# 3. Manually run script
bash scripts/maintenance/monthly-portfolio-validation.sh
```

**Common Causes:**
1. **Permissions:** Script not executable (`chmod +x`)
2. **Python dependencies:** Missing packages (pyyaml, frontmatter)
3. **File paths:** Cron runs with different working directory
4. **Disk space:** Reports directory full

**Resolution:**
```bash
# Fix permissions
chmod +x scripts/maintenance/monthly-portfolio-validation.sh

# Install dependencies
pip install pyyaml python-frontmatter

# Verify paths in script are absolute
grep REPO_DIR scripts/maintenance/monthly-portfolio-validation.sh

# Check disk space
df -h
```

---

### Issue 4: Pre-commit Hook Blocking Valid Commit

**Symptoms:**
- Post scores ≥75/100 in manual validation
- Pre-commit hook rejects commit
- Error: "Humanization validation failed"

**Diagnosis:**

```bash
# 1. Check which files are staged
git status

# 2. Manually validate staged posts
git diff --cached --name-only | grep "^src/posts/" | while read post; do
  python scripts/blog-content/humanization-validator.py --post "$post"
done

# 3. Review pre-commit hook logic
cat .git/hooks/pre-commit
```

**Common Causes:**
1. **Multiple posts staged:** One passing, one failing
2. **Frontmatter issues:** Missing required metadata
3. **File path mismatch:** Hook expects different directory structure
4. **Encoding problems:** Non-UTF-8 characters in post

**Resolution:**
```bash
# Commit posts individually
git add src/posts/passing-post.md
git commit -m "feat: Add passing post"

# Fix failing post separately
python scripts/blog-content/humanization-validator.py --post src/posts/failing-post.md
# (Review violations and fix)

# Bypass hook ONLY if absolutely necessary (not recommended)
git commit --no-verify -m "fix: Emergency fix [reason]"
```

---

## Common Fixes by Violation Type

### Missing First-Person Perspective (5 points)

**Issue:** Post lacks personal narrative
**Fix Pattern:**
```markdown
Before: "This approach improves performance."
After: "In my testing, this approach improved performance by 73%."

Before: "The system requires configuration."
After: "I discovered the system requires specific configuration after 3 hours of debugging."
```

### Missing Uncertainty Markers (3 points)

**Issue:** Post sounds overly confident
**Fix Pattern:**
```markdown
Before: "This is the best approach."
After: "In my experience, this approach works well, though your mileage may vary."

Before: "You should always use X."
After: "I typically use X, but Y might make more sense depending on your constraints."
```

### Missing Measurements (5 points, +5-10 bonus possible)

**Issue:** Lacks concrete numbers
**Fix Pattern:**
```markdown
Before: "Significantly faster"
After: "2.1x faster (reduced from 340ms to 160ms)"

Before: "Tested extensively"
After: "Tested over 3 months with 50+ samples on Intel i9-9900K with 64GB RAM"
```

### Em Dashes (−5 points per violation)

**Issue:** Em dashes in narrative text
**Fix Pattern:**
```markdown
Before: "The system—after extensive testing—proved reliable."
After: "The system, after extensive testing, proved reliable."

Before: "I discovered—somewhat by accident—a better approach."
After: "I discovered (somewhat by accident) a better approach."
```

### Semicolons in Narrative (−3 points per violation)

**Issue:** Semicolons outside code blocks
**Fix Pattern:**
```markdown
Before: "I tested approach A; it failed."
After: "I tested approach A. It failed."

Before: "Consider X; however, Y is faster."
After: "Consider X. However, Y is faster."
```

### Missing Trade-off Analysis (5 points, +1-7 bonus possible)

**Issue:** One-sided perspective
**Fix Pattern:**
```markdown
Before: "Use approach A for best results."
After: "Use approach A for best throughput (680 req/s), but be aware it uses 2x memory (8GB vs 4GB). For memory-constrained systems, approach B is better."
```

---

## Maintenance Schedule

### Daily
- **Pre-commit hooks:** Automatic validation on every commit
- **No manual action required**

### Weekly (Optional)
- **Monday morning:** Run quick portfolio health check (2 minutes)
- **Command:** `python scripts/blog-content/humanization-validator.py --batch --format summary`

### Monthly (Required)
- **First week of month:** Review monthly cron job output (5-10 minutes)
- **Action:** Check `reports/monthly/summary-YYYY-MM.txt`
- **Follow-up:** Investigate any failures (see troubleshooting)

### Quarterly (Recommended)
- **Review validator patterns:** Check if `humanization-patterns.yaml` needs updates
- **Benchmark performance:** Ensure batch validation still <1s
- **Dependency updates:** Update Python packages if needed

### Semi-Annual (Recommended)
- **Full portfolio audit:** Run detailed validation with comparison
- **Template refinement:** Update `blog-post-template.md` based on learnings
- **Documentation review:** Update CLAUDE.md with new edge cases

---

## System Health Indicators

### Green (Healthy)
- ✅ Passing rate ≥95% (54+/57 posts)
- ✅ Average score ≥100/100
- ✅ Monthly cron job succeeding
- ✅ No pre-commit hook failures
- ✅ Batch validation <1s

### Yellow (Warning)
- ⚠️ Passing rate 90-95% (51-53/57 posts)
- ⚠️ Average score 95-100/100
- ⚠️ 1-2 recent pre-commit hook failures
- ⚠️ Batch validation 1-2s

**Action:** Review failing posts, investigate score drop

### Red (Critical)
- 🚨 Passing rate <90% (<51/57 posts)
- 🚨 Average score <95/100
- 🚨 3+ recent pre-commit hook failures
- 🚨 Monthly cron job failing
- 🚨 Batch validation >2s

**Action:** Immediate investigation, full portfolio audit, escalate if needed

---

## Emergency Procedures

### Critical Failure: Multiple Posts Suddenly Failing

**Scenario:** 5+ posts drop below 75/100 overnight

**Immediate Actions:**

```bash
# 1. Save current state
python scripts/blog-content/humanization-validator.py --batch \
  --save-report reports/emergency-$(date +%Y-%m-%d-%H%M).json

# 2. Check for recent validator changes
git log --oneline --since="3 days ago" -- scripts/blog-content/

# 3. If validator changed, consider revert
git diff HEAD~1 scripts/blog-content/humanization-validator.py

# 4. If content issue, identify affected posts
python scripts/blog-content/humanization-validator.py --batch \
  --filter-below 75 --format detailed > reports/emergency-failures.txt

# 5. Review patterns
grep -E "(violation|missing)" reports/emergency-failures.txt | sort | uniq -c
```

**Recovery Options:**

1. **Revert validator changes:**
   ```bash
   git checkout HEAD~1 -- scripts/blog-content/humanization-validator.py
   git commit -m "revert: Restore validator to working state"
   ```

2. **Mass content fix (if pattern is clear):**
   ```bash
   # Example: Remove em dashes from all posts
   find src/posts -name "*.md" -exec sed -i 's/—/,/g' {} \;
   ```

3. **Selective post fixes:**
   - Review each failing post individually
   - Apply common fixes (see section above)
   - Validate before committing

---

### Validator Completely Broken

**Scenario:** Validator crashes or produces nonsensical results

**Immediate Actions:**

```bash
# 1. Test on known-good post
python scripts/blog-content/humanization-validator.py \
  --post src/posts/2024-01-08-writing-secure-code-developers-guide.md

# 2. Check Python dependencies
pip list | grep -E "(pyyaml|frontmatter|re)"

# 3. Check for syntax errors
python -m py_compile scripts/blog-content/humanization-validator.py

# 4. Restore from backup
cp scripts/blog-content/humanization-validator.py.backup \
   scripts/blog-content/humanization-validator.py
```

**Prevention:**
- Always create backup before major validator changes
- Test on subset of posts before full deployment
- Version control with meaningful commit messages

---

## Contact & Escalation

**Primary Owner:** William Zujkowski
**Backup:** CLAUDE.md documentation
**Escalation Path:**
1. Review this runbook
2. Check CLAUDE.md for detailed standards
3. Review Phase 5 & 6 completion reports
4. Consult individual post template guides

**Key Documentation:**
- `CLAUDE.md` (authoritative standards)
- `docs/PHASE5_COMPLETION_REPORT.md` (validator v2.0 details)
- `docs/PHASE6_MAINTENANCE_STRATEGY.md` (strategic planning)
- `docs/guides/USING_POST_TEMPLATE.md` (new post guidance)
- `scripts/blog-content/humanization-patterns.yaml` (pattern definitions)

---

## Changelog

### v1.0.0 (2025-10-29)
- Initial runbook creation for Phase 6
- Monthly cron job procedures
- Troubleshooting guide for common issues
- Emergency procedures for critical failures
- System health indicators

### Future Enhancements
- Automated alerting (email/Slack notifications)
- Dashboard for portfolio metrics visualization
- Regression detection with automatic rollback
- A/B testing framework for validator improvements

---

**Last Review:** 2025-10-29
**Next Review:** 2026-01-29 (quarterly)
