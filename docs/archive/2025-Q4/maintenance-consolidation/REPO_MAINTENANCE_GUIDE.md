# Repository Maintenance Guide

**Last Updated:** 2025-10-29
**Script:** `scripts/utilities/repo-maintenance.py`
**Version:** 1.0.0

## Overview

The repository maintenance script is a comprehensive tool for automated cleanup, archival, and health monitoring of the repository. It's designed to run monthly (or on-demand) to keep the repository clean and healthy.

## Features

### 1. Temporary File Cleanup
- Scans for temporary files in root directory
- Removes files not modified in 7+ days
- Preserves protected files (requirements.txt, test-citation-workflow.sh)
- Patterns detected:
  - `test-*.py`
  - `validate-*.py`
  - `fix-*.py`
  - `*.bak`, `*.tmp`, `*.swp`, `*~`

### 2. Report Archive Management
- Archives reports older than 60 days
- Organizes by year-month: `docs/archive/reports/YYYY-MM/`
- Preserves essential files:
  - `script-metadata.json` (latest only)
  - `maintenance-*.json` reports
- Optional backup before archiving

### 3. Image Variant Detection
- Detects recursive image variants (`*-###-###.*`)
- Reports but doesn't delete (pre-commit hooks handle this)
- Helps identify optimization issues

### 4. Duplicate File Detection
- Scans for duplicate content in docs/
- Uses SHA-256 hashing for accuracy
- Reports file size and locations
- Useful for cleanup decisions

### 5. Health Metrics
- **MANIFEST.json Validation**: Checks validity and freshness
- **Script Inventory**: Counts total, new, and modified scripts
- **Pre-commit Hooks**: Verifies installation status
- **npm Audit**: Reports security vulnerabilities
- **Git Status**: Shows uncommitted/unpushed changes

### 6. SEO Drift Detection
- Checks meta descriptions (120-160 character range)
- Alerts if >10% of posts drift outside range
- Generates detailed findings per post
- Helps maintain SEO quality

## Usage

### Quick Start

```bash
# Preview all operations
python scripts/utilities/repo-maintenance.py --dry-run --full

# Run health check only (safest)
python scripts/utilities/repo-maintenance.py --health-check

# Full maintenance with verbose output
python scripts/utilities/repo-maintenance.py --full --verbose

# Cleanup with backup
python scripts/utilities/repo-maintenance.py --cleanup --archive --backup
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview changes without applying (recommended first) |
| `--cleanup` | Run cleanup operations only |
| `--archive` | Archive old reports only |
| `--health-check` | Run health metrics only |
| `--full` | Run all operations (cleanup + archive + health) |
| `--verbose` | Detailed output with findings |
| `--force` | Skip confirmation prompts (for automation) |
| `--backup` | Create backups before archiving |

### Exit Codes

- **0**: Clean (no issues)
- **1**: Warnings (non-critical issues)
- **2**: Errors (critical issues)

## Common Scenarios

### Monthly Maintenance Routine

```bash
# 1. Preview what will happen
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose

# 2. Review the output, then run for real
python scripts/utilities/repo-maintenance.py --full --backup

# 3. Check the generated report
cat docs/reports/maintenance-$(date +%Y-%m-%d).json
```

### Before a Release

```bash
# Quick health check
python scripts/utilities/repo-maintenance.py --health-check --verbose

# If warnings found, run cleanup
python scripts/utilities/repo-maintenance.py --cleanup --force

# Verify everything is good
python scripts/utilities/repo-maintenance.py --health-check
```

### Troubleshooting Build Issues

```bash
# Check for issues
python scripts/utilities/repo-maintenance.py --health-check --verbose

# Look for duplicate files that might conflict
python scripts/utilities/repo-maintenance.py --health-check | grep -A 5 "duplicates"

# Clean up temp files that might interfere
python scripts/utilities/repo-maintenance.py --cleanup
```

### Investigating SEO Issues

```bash
# Run health check with verbose output
python scripts/utilities/repo-maintenance.py --health-check --verbose 2>&1 | grep -A 20 "seo_drift"

# Or save detailed report
python scripts/utilities/repo-maintenance.py --health-check --verbose > seo-report.txt
```

## Automation

### Cron Setup (Monthly)

Add to crontab (`crontab -e`):

```bash
# Run maintenance on the 1st of each month at 2 AM
0 2 1 * * cd /home/william/git/williamzujkowski.github.io && python scripts/utilities/repo-maintenance.py --full --force >> logs/maintenance.log 2>&1
```

### GitHub Actions

Create `.github/workflows/maintenance.yml`:

```yaml
name: Monthly Maintenance

on:
  schedule:
    # Run on 1st of each month at 00:00 UTC
    - cron: '0 0 1 * *'
  workflow_dispatch: # Allow manual trigger

jobs:
  maintenance:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml requests

      - name: Run maintenance
        run: |
          python scripts/utilities/repo-maintenance.py --full --force --verbose

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: maintenance-report
          path: docs/reports/maintenance-*.json

      - name: Check exit code
        run: |
          if [ $? -eq 2 ]; then
            echo "::error::Maintenance found critical errors"
            exit 1
          fi
```

### Pre-release Check

Add to release workflow:

```yaml
- name: Pre-release maintenance check
  run: |
    python scripts/utilities/repo-maintenance.py --health-check --verbose
    if [ $? -eq 2 ]; then
      echo "::error::Repository health check failed"
      exit 1
    fi
```

## Output Examples

### Clean Repository

```
=== Repository Maintenance Report ===

Statistics:
  duplicate_files: 0
  duplicate_sets: 0
  image_variants_found: 0
  posts_with_seo_drift: 2
  temp_files_found: 0
  total_posts_checked: 59
  total_scripts: 47

✓ Status: CLEAN
```

### With Warnings

```
=== Repository Maintenance Report ===

Statistics:
  duplicate_files: 3
  temp_files_found: 5
  posts_with_seo_drift: 13

Warnings (13):
  ⚠ Found temp file: test-validation.py (modified 2025-10-15)
  ⚠ Found temp file: fix-links.py (modified 2025-10-20)
  ⚠ 22.0% of posts have out-of-range descriptions

⚠ Status: WARNINGS
```

### With Errors

```
=== Repository Maintenance Report ===

Errors (2):
  ✗ MANIFEST.json validation failed: Invalid JSON
  ✗ npm audit found 5 critical vulnerabilities

✗ Status: ERRORS FOUND
```

## Report Format

JSON reports are saved to `docs/reports/maintenance-YYYY-MM-DD.json`:

```json
{
  "timestamp": "2025-10-29T00:00:00-04:00",
  "statistics": {
    "temp_files_found": 5,
    "temp_files_removed": 5,
    "old_reports_found": 12,
    "reports_archived": 12,
    "duplicate_files": 0,
    "image_variants_found": 0,
    "total_scripts": 47,
    "posts_with_seo_drift": 13
  },
  "actions": [
    {
      "action": "Deleted temp file: test-validation.py",
      "status": "completed",
      "timestamp": "2025-10-29T00:00:05-04:00"
    }
  ],
  "findings": {
    "health": [
      {
        "message": "MANIFEST.json is valid",
        "severity": "info",
        "timestamp": "2025-10-29T00:00:10-04:00"
      }
    ],
    "seo_drift": [
      {
        "message": "post-name.md: description length 43 (target: 120-160)",
        "severity": "warning",
        "timestamp": "2025-10-29T00:00:15-04:00"
      }
    ]
  },
  "errors": [],
  "warnings": ["22.0% of posts have out-of-range descriptions"],
  "exit_code": 1
}
```

## Safety Features

### Protected Files (Never Deleted)
- `MANIFEST.json`
- `CLAUDE.md`
- `.claude-rules.json`
- `.eleventy.js`
- `package.json`
- `tailwind.config.js`
- `README.md`
- `scripts/lib/common.py`
- `requirements.txt`
- `test-citation-workflow.sh`

### Protected Directories (Never Scanned for Cleanup)
- `.git/`
- `node_modules/`
- `_site/`

### Safeguards
1. **7-day grace period**: Temp files must be >7 days old
2. **Dry-run mode**: Preview before applying changes
3. **Backup option**: Create backups before archiving
4. **Protected patterns**: Essential files never touched
5. **Hash-based detection**: Accurate duplicate detection

## Troubleshooting

### "MANIFEST.json not found"

```bash
# Regenerate MANIFEST.json if missing
python scripts/utilities/generate-manifest.py
```

### "Pre-commit hooks not installed"

```bash
# Install hooks
pre-commit install
```

### "npm audit found vulnerabilities"

```bash
# Fix automatically
npm audit fix

# Or review manually
npm audit
```

### "Too many SEO warnings"

```bash
# Get detailed list
python scripts/utilities/repo-maintenance.py --health-check --verbose 2>&1 | grep "description length"

# Fix descriptions manually or with script
python scripts/blog-content/optimize-blog-content.py --fix-descriptions
```

## Integration with Other Tools

### Works Well With
- **Pre-commit hooks**: Maintenance runs after hooks validation
- **Link validators**: Combine with link checking scripts
- **Blog optimization**: Run before blog content enhancements
- **Citation tools**: Health check includes research validation

### Recommended Workflow
1. Run maintenance script
2. Review findings
3. Run specific cleanup tools as needed
4. Commit changes
5. Pre-commit hooks validate
6. Push to remote

## Best Practices

1. **Run monthly**: Keep repository clean with regular maintenance
2. **Use dry-run first**: Always preview before applying changes
3. **Enable backups**: Use `--backup` for archives
4. **Monitor reports**: Review JSON reports for trends
5. **Fix warnings**: Address SEO drift and duplicates promptly
6. **Automate carefully**: Use `--force` only in trusted automation
7. **Version control**: Commit maintenance reports for historical tracking

## Future Enhancements

Potential additions (not yet implemented):
- Automatic SEO description fixing
- Link validation integration
- Code quality metrics
- Performance benchmarking
- Dependency update checking
- Security scanning integration
- Automated PR creation for fixes

## Support

For issues or questions:
1. Check this guide first
2. Review generated reports in `docs/reports/`
3. Run with `--verbose` for detailed output
4. Check script comments for implementation details
5. Review `.claude-rules.json` for standards

## Version History

- **1.0.0** (2025-10-29): Initial release
  - Temp file cleanup
  - Report archiving
  - Health checks
  - SEO drift detection
  - Image variant detection
  - Duplicate detection
