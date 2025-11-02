# Token Monitoring System - Deployment Guide

**Status:** ✅ DEPLOYED
**Version:** 1.0.0
**Last Updated:** 2025-11-01
**Script:** `scripts/utilities/token-usage-monitor.py`

## Overview

Real-time token usage monitoring system that tracks consumption across operations and provides optimization recommendations. Enables data-driven decisions about context loading and documentation structure.

**Benefits:**
- Identify token-heavy operations
- Track optimization effectiveness
- Data-driven recommendations
- Historical usage analysis

## Quick Start

### 1. Start a Monitoring Session

```bash
uv run python scripts/utilities/token-usage-monitor.py \
  --start-session "blog-post-cybersecurity"
```

### 2. Log Operations During Work

```bash
# Example: Reading MANIFEST.json
uv run python scripts/utilities/token-usage-monitor.py \
  --log "read MANIFEST.json" \
  --tokens 29588 \
  --session "blog-post-cybersecurity"

# Example: Loading context modules
uv run python scripts/utilities/token-usage-monitor.py \
  --log "load blog-writing + humanization-standards" \
  --tokens 6000 \
  --session "blog-post-cybersecurity"
```

### 3. End Session and Generate Report

```bash
uv run python scripts/utilities/token-usage-monitor.py \
  --end-session "blog-post-cybersecurity"
```

## Common Use Cases

### Blog Post Creation

```bash
# Start session
uv run python scripts/utilities/token-usage-monitor.py --start-session "blog-${POST_NAME}"

# Log operations as you work:
--log "load context modules" --tokens 15000 --session "blog-${POST_NAME}"
--log "read existing posts" --tokens 5000 --session "blog-${POST_NAME}"
--log "write post content" --tokens 8000 --session "blog-${POST_NAME}"

# End and analyze
uv run python scripts/utilities/token-usage-monitor.py --end-session "blog-${POST_NAME}"
```

### Module Optimization Analysis

```bash
# Analyze historical usage
uv run python scripts/utilities/token-usage-monitor.py --analyze

# Get recommendations
uv run python scripts/utilities/token-usage-monitor.py --recommend
```

## Data Storage

**Location:** `docs/metrics/token-usage/`

```
docs/metrics/token-usage/
├── sessions.json         # Active and completed sessions
└── usage-log.jsonl       # Historical operation log
```

## Operation Categories

The monitor automatically categorizes operations:

- **manifest**: MANIFEST.json operations
- **context**: CLAUDE.md and module loading
- **blog**: Blog post creation/editing
- **scripts**: Python script execution
- **validation**: Pre-commit checks
- **git**: Git operations
- **docs**: Documentation reading
- **other**: Uncategorized

## Analysis Commands

### Historical Usage Analysis

```bash
uv run python scripts/utilities/token-usage-monitor.py --analyze
```

Shows:
- Total tokens consumed by category
- Average tokens per operation type
- Top 10 most expensive operations
- Trends over time

### Optimization Recommendations

```bash
uv run python scripts/utilities/token-usage-monitor.py --recommend
```

Provides:
- High-impact optimization opportunities
- Estimated token savings
- Implementation priorities

## Integration with Workflows

### Manual Tracking (Current)

LLMs can manually log operations:

```python
# In your workflow
log_token_usage("read MANIFEST.json", tokens=29588, session="current-task")
```

### Future: Automated Tracking

Planned enhancements:
- Pre-commit hook integration
- Automatic context loading measurement
- Real-time optimization suggestions

## Expected Savings

Based on hive mind analysis:

| Optimization | Before | After | Savings |
|-------------|--------|-------|---------|
| MANIFEST.json | 29,588 | 306 | 99% |
| Module redundancy | 48,610 | 35,000 | 28% |
| Maintenance docs | 60,000 | 10,000 | 83% |

**Total potential:** 287.5M-330M tokens/year

## Success Metrics

Track these metrics over time:

1. **Average tokens per blog post:** Target <15K (currently ~25K)
2. **Context loading efficiency:** Target >85% (currently 84.9%)
3. **Module redundancy:** Target <15% (currently 31-41%)
4. **MANIFEST.json size:** Target <2K (currently 29.6K)

## Troubleshooting

### Issue: Sessions file corrupted

```bash
# Backup and reset
cp docs/metrics/token-usage/sessions.json docs/metrics/token-usage/sessions.json.bak
echo '{"sessions": [], "active_sessions": {}}' > docs/metrics/token-usage/sessions.json
```

### Issue: Token estimates inaccurate

Update token estimates using measured data:

```python
# Use actual token counts from Claude API responses
# Update INDEX.yaml with corrected estimates
```

## Next Steps

1. ✅ Deploy monitoring system
2. ⏳ Run 5-10 sessions to gather baseline data
3. ⏳ Analyze patterns and identify quick wins
4. ⏳ Implement top 3 optimizations
5. ⏳ Measure impact and iterate

## Related Documentation

- **Optimization Analysis:** `docs/reports/hive-mind-optimization-synthesis-report.md`
- **Token Budget Tracking:** `docs/context/INDEX.yaml`
- **Module Efficiency:** `docs/reports/context-module-efficiency-report.md`
- **Script Catalog:** `docs/GUIDES/SCRIPT_CATALOG.md`

---

**Deployed by:** Hive Mind Swarm (Coder Agent)
**Part of:** Week 1 Quick Wins
**Expected Impact:** 15% additional savings through data-driven optimization
