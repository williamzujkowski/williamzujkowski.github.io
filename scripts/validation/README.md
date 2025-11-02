# Validation Scripts Documentation

## Overview

This directory contains validation scripts for build monitoring and metadata quality checks.

## Scripts

### 1. metadata-validator.py

Validates frontmatter metadata across all blog posts.

**Usage:**
```bash
# Text output (default)
uv run python scripts/validation/metadata-validator.py

# JSON output
uv run python scripts/validation/metadata-validator.py --format json

# Custom posts directory
uv run python scripts/validation/metadata-validator.py --posts-dir src/posts
```

**Checks:**
- ✅ **Title:** Required field
- ✅ **Description:** Length validation (optimal: 120-160 chars)
- ✅ **Date:** Format validation (YYYY-MM-DD or ISO 8601)
- ✅ **Author:** Required field
- ✅ **Tags:** Count validation (recommend 3-8 tags)
- ⚠️ **Hero Image:** Path validation (warning if missing)

**Exit Codes:**
- `0` - All validation passed (warnings OK)
- `1` - Validation failed (critical errors found)

### 2. build-monitor.py

Monitors build process, detects regressions, and provides detailed diagnostics.

**Usage:**
```bash
# Establish baseline (run once)
uv run python scripts/validation/build-monitor.py --baseline

# Run build and compare with baseline
uv run python scripts/validation/build-monitor.py --compare

# Just run build (no comparison)
uv run python scripts/validation/build-monitor.py
```

**Metrics Tracked:**
- Build time (total and Eleventy-specific)
- Files written/copied
- Posts parsed
- JavaScript bundle sizes
- Warnings and errors
- Build success/failure status

**Regression Detection:**
- Build failures
- Time increases >20%
- New errors introduced
- Statistics changes

**Exit Codes:**
- `0` - Build passed
- `1` - Build failed or regression detected

### 3. continuous-monitor.sh

Real-time file monitoring with automatic validation on save.

**Usage:**
```bash
# Start monitoring (foreground)
./scripts/validation/continuous-monitor.sh

# Run in background
./scripts/validation/continuous-monitor.sh &

# View log
tail -f .validation-monitor.log
```

**Features:**
- Uses `inotifywait` if available (faster)
- Falls back to polling if not installed
- Logs all changes to `.validation-monitor.log`
- Validates modified markdown files automatically

**Install inotify-tools (recommended):**
```bash
# Ubuntu/Debian
sudo apt-get install inotify-tools

# Fedora/RHEL
sudo dnf install inotify-tools

# macOS
brew install fswatch  # Alternative for macOS
```

## Integration with Pre-commit

These scripts integrate with pre-commit hooks:

```bash
# In .git/hooks/pre-commit
uv run python scripts/validation/metadata-validator.py --format json > /tmp/validation.json

if [ $? -ne 0 ]; then
    echo "❌ Metadata validation failed - fix errors before committing"
    exit 1
fi
```

## CI/CD Integration

### GitHub Actions Example:

```yaml
name: Validate Build
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3

      # Establish baseline
      - name: Create baseline
        run: uv run python scripts/validation/build-monitor.py --baseline

      # Make changes (your workflow here)

      # Compare with baseline
      - name: Validate build
        run: uv run python scripts/validation/build-monitor.py --compare

      # Validate metadata
      - name: Check metadata quality
        run: uv run python scripts/validation/metadata-validator.py
```

## Current Status

### Baseline (2025-11-02)

**Build Status:** ✅ PASSING
- Build time: 8.54s
- Posts parsed: 63
- Files written: 209
- Eleventy time: 4.59s

**Metadata Quality:**
- Valid posts: 0/63 (0.0%)
- Posts with warnings: 29
- Posts with errors: 34

**Top Issues:**
1. Missing author: 34 posts
2. Missing hero_image: 63 posts (non-critical)
3. Invalid date format: 11 posts

### Recommended Actions

1. **Critical:** Add author field to 34 posts
2. **Important:** Fix date formats in 11 posts
3. **Optional:** Add hero images (currently warnings only)

## Advanced Usage

### Batch Validation

Validate specific posts:
```bash
# Validate single post
uv run python scripts/validation/metadata-validator.py --posts-dir src/posts | grep "2024-01-08"
```

### JSON Output Processing

Process JSON output with jq:
```bash
# Count posts by issue type
uv run python scripts/validation/metadata-validator.py --format json | \
  jq '.issues_summary | to_entries[] | select(.value > 0) | {issue: .key, count: .value}'

# List posts with errors
uv run python scripts/validation/metadata-validator.py --format json | \
  jq '.posts_with_issues[] | select(.valid == false) | .file'
```

### Build Performance Tracking

Track build time over multiple runs:
```bash
# Create baseline
uv run python scripts/validation/build-monitor.py --baseline

# After changes
uv run python scripts/validation/build-monitor.py --compare | \
  grep "Time delta" > build-performance.log
```

## Troubleshooting

### Metadata Validator Issues

**Problem:** "YAML parsing error"
- **Solution:** Check frontmatter syntax, ensure `---` delimiters are correct

**Problem:** "Path not found" for hero images
- **Solution:** Verify image paths are relative to project root or absolute

### Build Monitor Issues

**Problem:** Build timeout (>120s)
- **Solution:** Increase timeout in script or investigate slow build steps

**Problem:** Baseline not found
- **Solution:** Run with `--baseline` flag first before using `--compare`

### Continuous Monitor Issues

**Problem:** "inotifywait: command not found"
- **Solution:** Install inotify-tools (see Installation section above)

**Problem:** High CPU usage with polling
- **Solution:** Install inotifywait for efficient file watching

## Files Generated

- `.build-baseline.json` - Build baseline for comparison
- `.validation-monitor.log` - Continuous monitoring log
- `/tmp/validation.json` - Temporary validation results (pre-commit)

## Contributing

When adding new validation checks:

1. Update `metadata-validator.py` with new validation method
2. Add test cases for edge cases
3. Update this README with new checks
4. Update exit codes if needed
5. Add to issues_summary dict

## References

- **CLAUDE.md:** Enforcement rules and standards
- **MANIFEST.json:** File registry and project metadata
- **.claude-rules.json:** Automated enforcement rules
