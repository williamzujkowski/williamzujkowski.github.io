# Batch Validation Guide

## Overview

The humanization validator now supports efficient batch processing with parallel execution, enabling portfolio-wide validation in under 1 second.

## Quick Start

### Basic Batch Validation
```bash
python scripts/blog-content/humanization-validator.py --batch
```

### Common Use Cases

#### 1. Find Posts Below Threshold
```bash
# Show only posts scoring below 90
python scripts/blog-content/humanization-validator.py --batch --filter-below 90
```

#### 2. Generate JSON Report
```bash
# Output as JSON for automation
python scripts/blog-content/humanization-validator.py --batch --format json > validation.json
```

#### 3. Save Historical Report
```bash
# Save report with timestamp
python scripts/blog-content/humanization-validator.py --batch \
  --save-report reports/validation-$(date +%Y-%m-%d).json
```

#### 4. Detailed Violations
```bash
# Show all violations for each post
python scripts/blog-content/humanization-validator.py --batch --format detailed
```

#### 5. Custom Worker Count
```bash
# Use 8 workers for faster processing on high-core systems
python scripts/blog-content/humanization-validator.py --batch --workers 8
```

## Performance

### Benchmarks (57 posts)
- **Total Time**: 0.74 seconds
- **Per Post**: ~0.013 seconds
- **Workers**: 4 parallel processes
- **Speedup**: ~60x faster than single-threaded sequential

### Comparison
- **Single-post mode**: ~0.8s per post → 45.6s for 57 posts
- **Batch mode**: 0.74s total → **60x faster**

## Output Formats

### 1. Summary (Default)
Clean table with scores, status, and issue counts:
```
Post                                                Score     Status   Issues
--------------------------------------------------------------------------------
2025-03-24-from-it-support-to-senior-infosec...      55       FAIL       5
2024-11-19-llms-smart-contract-vulnerability.md      97       PASS       1
2024-01-08-writing-secure-code-developers-guide.md  110       PASS       0
```

**Statistics shown**:
- Total posts
- Pass/fail counts and rates
- Average, median, min, max scores

### 2. JSON
Machine-readable format for automation:
```json
{
  "timestamp": "2025-10-29T10:30:00",
  "total_posts": 57,
  "statistics": {
    "passed": 56,
    "failed": 1,
    "pass_rate": 98.2,
    "avg_score": 105.4
  },
  "results": [...]
}
```

### 3. Detailed
Full violations and warnings for each post:
```
================================================================================
2025-03-24-from-it-support-to-senior-infosec-engineer.md
Score: 55/100

Violations:
  • missing_required_pattern: Missing first-person perspective
  • missing_required_pattern: Missing trade-offs discussion

Warnings:
  • jargon: Corporate buzzword "leverage" found 3 times
```

## Filtering Options

### By Score
```bash
# Only show posts below 90
--filter-below 90

# Only show posts below 70 (failing posts)
--filter-below 70
```

### By Status
```bash
# Fail on any score below 80
--min-score 80
```

## Report Comparison (Coming Soon)

```bash
# Compare current state with previous report
python scripts/blog-content/humanization-validator.py --batch \
  --compare reports/validation-2025-10-28.json
```

Output will show:
- **Improvements**: Posts with higher scores
- **Regressions**: Posts with lower scores
- **Unchanged**: Posts with same scores
- **New posts**: Posts not in previous report

## CI/CD Integration

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Validate humanization standards
python scripts/blog-content/humanization-validator.py --batch --min-score 70
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "❌ Humanization validation failed"
    echo "Run with --format detailed to see violations"
    exit 1
fi

echo "✅ All posts pass humanization standards"
```

### GitHub Actions
```yaml
name: Validate Blog Posts

on:
  pull_request:
    paths:
      - 'src/posts/**'
  push:
    branches:
      - main

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install pyyaml python-frontmatter

      - name: Validate humanization
        run: |
          python scripts/blog-content/humanization-validator.py \
            --batch \
            --format json \
            --save-report reports/humanization-validation.json

      - name: Upload validation report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: humanization-validation-report
          path: reports/humanization-validation.json

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const fs = require('fs');
            const report = JSON.parse(fs.readFileSync('reports/humanization-validation.json', 'utf8'));
            const stats = report.statistics;

            const comment = `
            ## Humanization Validation Results

            - **Total Posts**: ${stats.total_posts}
            - **Passed**: ${stats.passed} (${stats.pass_rate.toFixed(1)}%)
            - **Failed**: ${stats.failed} (${stats.fail_rate.toFixed(1)}%)
            - **Average Score**: ${stats.avg_score.toFixed(1)}/100

            ${stats.failed > 0 ? '⚠️ Some posts need attention' : '✅ All posts pass humanization standards'}
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

## Exit Codes

- **0**: All posts pass (score >= min-score)
- **1**: One or more posts fail
- **2**: Error (missing files, invalid config, etc.)

## Troubleshooting

### "No markdown files found"
**Cause**: Wrong directory specified
**Fix**: Verify directory path or omit `--dir` to use default `src/posts`

### "Error: Directory not found"
**Cause**: Custom directory doesn't exist
**Fix**: Create directory or use correct path

### Slow Performance
**Cause**: Too few workers or I/O bottleneck
**Fix**: Increase workers with `--workers 8` (match CPU cores)

### Different Scores vs Single-Post Mode
**Cause**: This should never happen - report as bug if it does
**Expected**: Scores should be identical between batch and single-post modes

## Best Practices

1. **Run batch validation before committing**
   - Catches issues early
   - Fast enough for pre-commit hooks

2. **Save reports with timestamps**
   - Track improvements over time
   - Compare historical trends

3. **Use JSON format for automation**
   - Parse results programmatically
   - Integrate with dashboards

4. **Filter for efficiency**
   - Use `--filter-below` to focus on problem posts
   - Don't waste time reviewing perfect posts

5. **Adjust min-score based on goals**
   - 70: Basic humanization (default)
   - 90: High-quality humanization
   - 100: Excellent humanization with measurement data

## Advanced Usage

### Parallel Processing Tuning
```bash
# Match CPU cores for optimal performance
--workers $(nproc)

# Conservative (lower CPU usage)
--workers 2

# Aggressive (maximum speed)
--workers 16
```

### Custom Directory Validation
```bash
# Validate specific directory
python scripts/blog-content/humanization-validator.py --batch --dir drafts/
```

### Combining Filters
```bash
# Show detailed violations for posts below 80
python scripts/blog-content/humanization-validator.py \
  --batch \
  --filter-below 80 \
  --format detailed
```

## Performance Characteristics

### Scalability
- **57 posts**: 0.74s (4 workers)
- **100 posts** (estimated): ~1.3s (4 workers)
- **200 posts** (estimated): ~2.6s (4 workers)

### Resource Usage
- **CPU**: Utilizes all specified workers (default: 4 cores)
- **Memory**: ~50MB per worker (~200MB total)
- **I/O**: Parallel file reading, minimal disk wait

### Bottlenecks
- **Pattern matching**: Most CPU-intensive operation
- **Config loading**: Once per worker (negligible)
- **Progress output**: Minimal overhead (~0.01s)

## Future Enhancements

### Planned Features
1. **Report comparison** - Track improvements/regressions
2. **Trend analysis** - Score changes over time
3. **Auto-fix suggestions** - Recommended changes for violations
4. **Integration with full-post-validation** - Combined comprehensive checks
5. **Web dashboard** - Visual portfolio health monitoring

### Experimental Features
- **Incremental validation** - Only validate changed posts
- **Smart caching** - Skip unchanged posts
- **Distributed validation** - Multiple machines for large portfolios
- **Real-time monitoring** - Watch mode for continuous validation

## Support

For issues or questions:
1. Check this guide first
2. Run with `--help` for command syntax
3. Test single-post mode to verify scoring logic
4. Review `humanization-patterns.yaml` for scoring rules
5. Check backup at `humanization-validator.py.backup` if needed
