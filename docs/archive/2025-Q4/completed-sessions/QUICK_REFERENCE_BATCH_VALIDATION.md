# Quick Reference: Batch Validation

## One-Liner Commands

### Basic Operations
```bash
# Validate all posts
python scripts/blog-content/humanization-validator.py --batch

# Show only failures (score < 70)
python scripts/blog-content/humanization-validator.py --batch --filter-below 70

# JSON output
python scripts/blog-content/humanization-validator.py --batch --format json

# Detailed violations
python scripts/blog-content/humanization-validator.py --batch --format detailed

# Save report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/validation-$(date +%Y-%m-%d).json
```

### Advanced
```bash
# Compare with previous
python scripts/blog-content/humanization-validator.py --batch --compare reports/validation-2025-10-28.json

# Custom workers
python scripts/blog-content/humanization-validator.py --batch --workers 8

# Strict mode (higher threshold)
python scripts/blog-content/humanization-validator.py --batch --min-score 90
```

## Quick Stats

| Metric | Value |
|--------|-------|
| **Total Posts** | 57 |
| **Validation Time** | 0.74s |
| **Per Post** | 0.013s |
| **Speedup** | 60x |
| **Pass Rate** | 98.2% |
| **Average Score** | 105.4/100 |

## Output Format Examples

### Summary (Default)
```
Starting batch validation...
Posts to validate: 57
Workers: 4

✓ [1/57]   1.8% | Score: 110 | ETA:   0.7s | post-name.md
...

Batch validation complete!
Total time: 0.74s
Average: 0.013s per post

Statistics:
  Total Posts: 57
  Passed: 56 (98.2%)
  Failed: 1 (1.8%)
  Average Score: 105.4
```

### JSON
```json
{
  "timestamp": "2025-10-29T10:30:00",
  "total_posts": 57,
  "statistics": {
    "total_posts": 57,
    "passed": 56,
    "failed": 1,
    "pass_rate": 98.2,
    "avg_score": 105.4
  },
  "results": [...]
}
```

### Detailed
```
================================================================================
post-name.md
Score: 55/100

Violations:
  • missing_required_pattern: Missing first-person perspective
  • banned_token: Em dash found 5 times

Warnings:
  • jargon: Corporate buzzword "leverage" found 3 times
```

## Common Workflows

### Daily Development
```bash
# Quick check before commit
python scripts/blog-content/humanization-validator.py --batch
```

### Pre-release Audit
```bash
# Full audit with report
python scripts/blog-content/humanization-validator.py --batch \
  --format detailed \
  --save-report reports/pre-release-audit.json
```

### Focus on Problems
```bash
# Show only posts needing work
python scripts/blog-content/humanization-validator.py --batch \
  --filter-below 90 \
  --format detailed
```

### Track Progress
```bash
# Compare with last week
python scripts/blog-content/humanization-validator.py --batch \
  --compare reports/validation-$(date -d '7 days ago' +%Y-%m-%d).json \
  --save-report reports/validation-$(date +%Y-%m-%d).json
```

## Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | All passed | Continue |
| 1 | Some failed | Review violations |
| 2 | Error | Check directory/config |

## Filters & Thresholds

| Flag | Purpose | Example |
|------|---------|---------|
| `--min-score 70` | Pass threshold | Fail if <70 |
| `--filter-below 90` | Display filter | Only show <90 |
| `--strict` | Fail on any violation | Zero tolerance |

## Performance Tips

1. **Match CPU cores**: `--workers $(nproc)`
2. **Use JSON for parsing**: `--format json > results.json`
3. **Filter efficiently**: `--filter-below 80` to focus efforts
4. **Save reports**: Track trends over time

## Integration Snippets

### Pre-commit Hook
```bash
#!/bin/bash
python scripts/blog-content/humanization-validator.py --batch --min-score 70 || exit 1
```

### GitHub Actions
```yaml
- run: python scripts/blog-content/humanization-validator.py --batch --format json
```

### Makefile
```makefile
validate:
	python scripts/blog-content/humanization-validator.py --batch

validate-strict:
	python scripts/blog-content/humanization-validator.py --batch --min-score 90
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No files found" | Check `--dir` path |
| Slow performance | Increase `--workers` |
| Different scores | This is a bug - report it |

## Score Interpretation

| Range | Quality | Action |
|-------|---------|--------|
| 110+ | Excellent | Maintain |
| 100-109 | Very Good | Minor polish |
| 90-99 | Good | Consider enhancements |
| 70-89 | Acceptable | Improvement recommended |
| <70 | Needs Work | Required fixes |

## Documentation

- **Full Guide**: `docs/BATCH_VALIDATION_GUIDE.md`
- **Benchmarks**: `tests/test-batch-validation-performance.md`
- **Summary**: `BATCH_VALIDATION_SUMMARY.md`
- **Patterns**: `scripts/blog-content/humanization-patterns.yaml`

## Support

```bash
# Built-in help
python scripts/blog-content/humanization-validator.py --help

# Single-post mode (for debugging)
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Test installation
python scripts/blog-content/humanization-validator.py --batch --format json | python -m json.tool
```
