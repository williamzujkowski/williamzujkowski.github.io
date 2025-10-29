# Repository Maintenance Quick Reference

**Script:** `scripts/utilities/repo-maintenance.py`

## Quick Commands

```bash
# 🔍 Preview what will happen (ALWAYS RUN THIS FIRST)
python scripts/utilities/repo-maintenance.py --dry-run --full

# 🏥 Health check only (safe)
python scripts/utilities/repo-maintenance.py --health-check

# 🧹 Cleanup temporary files
python scripts/utilities/repo-maintenance.py --cleanup

# 📦 Archive old reports
python scripts/utilities/repo-maintenance.py --archive --backup

# 🚀 Full maintenance
python scripts/utilities/repo-maintenance.py --full --backup

# 📊 Verbose output
python scripts/utilities/repo-maintenance.py --full --verbose
```

## What Gets Cleaned

### ✅ Safe to Remove
- `test-*.py` in root (>7 days old)
- `validate-*.py` in root (>7 days old)
- `fix-*.py` in root (>7 days old)
- `*.bak`, `*.tmp`, `*.swp` (>7 days old)
- Reports in `docs/reports/` (>60 days old)

### ❌ Never Removed
- `MANIFEST.json`, `CLAUDE.md`, `.claude-rules.json`
- `requirements.txt`, `test-citation-workflow.sh`
- Protected files in `.claude-rules.json`
- Anything in `.git/`
- Files modified within 7 days

## What Gets Checked

### Health Metrics
- ✓ MANIFEST.json validity
- ✓ Pre-commit hooks installed
- ✓ npm security audit
- ✓ Git uncommitted/unpushed changes
- ✓ Script inventory (total, new, modified)

### Quality Checks
- ⚠️ SEO meta descriptions (120-160 chars)
- ⚠️ Image variants (recursive `-###-###`)
- ⚠️ Duplicate files (by hash)

## Exit Codes

- **0** = ✅ Clean
- **1** = ⚠️ Warnings
- **2** = ❌ Errors

## Common Issues

### "SEO drift detected"
```bash
# View affected posts
python scripts/utilities/repo-maintenance.py --health-check --verbose 2>&1 | grep "description length"

# Fix manually or with optimization script
python scripts/blog-content/optimize-blog-content.py
```

### "Image variants found"
```bash
# Pre-commit hooks will prevent them
# Run to clean existing:
git add -A && git commit -m "test"  # hooks will clean
```

### "Duplicates detected"
```bash
# Review duplicates
python scripts/utilities/repo-maintenance.py --health-check --verbose

# Remove manually after verification
```

### "npm vulnerabilities"
```bash
npm audit fix
```

## Monthly Workflow

1. **Preview**: `python scripts/utilities/repo-maintenance.py --dry-run --full`
2. **Review**: Check what will be cleaned
3. **Execute**: `python scripts/utilities/repo-maintenance.py --full --backup`
4. **Verify**: Check exit code and report
5. **Commit**: `git add . && git commit -m "chore: monthly maintenance"`

## Report Location

`docs/reports/maintenance-YYYY-MM-DD.json`

## Need Help?

See full guide: `docs/GUIDES/REPO_MAINTENANCE_GUIDE.md`
