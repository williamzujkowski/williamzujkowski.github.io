# Python Logging Migration - Next Steps
**Date:** 2025-11-02
**Priority:** HIGH
**Estimated Time:** 1.0 hour for next batch

---

## Current Status

```
[█████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 19.5%

15/77 scripts migrated | 62 remaining
```

**Correction:** TODO.md claims 23/77 (29.9%) - **INCORRECT by -8 scripts**

---

## 🚀 IMMEDIATE ACTION: Batch 1 (Critical Path)

### Scripts to Migrate (5 total, ~1 hour)

#### 1. scripts/validation/build-monitor.py
- **Lines:** 710
- **Priority:** P0 - Critical
- **Reason:** Pre-commit validation, used in every commit
- **Complexity:** Medium (similar to metadata-validator)
- **Time Estimate:** 15 minutes

#### 2. scripts/lib/precommit_validators.py
- **Lines:** 1,027
- **Priority:** P0 - Critical
- **Reason:** Git hooks infrastructure, enforces standards
- **Complexity:** High (largest in batch)
- **Time Estimate:** 20 minutes

#### 3. scripts/lib/cache_utils.py
- **Lines:** 711
- **Priority:** P1 - High
- **Reason:** Infrastructure dependency, used by multiple scripts
- **Complexity:** Medium
- **Time Estimate:** 15 minutes

#### 4. scripts/lib/manifest_loader.py
- **Lines:** 396
- **Priority:** P1 - High
- **Reason:** Central dependency, validation pipeline
- **Complexity:** Low-Medium
- **Time Estimate:** 10 minutes

#### 5. scripts/link-validation/citation-report.py
- **Lines:** 264
- **Priority:** P0 - Critical
- **Reason:** High frequency use, citation audits
- **Complexity:** Low (quick win)
- **Time Estimate:** 8 minutes

**Total Estimated Time:** 68 minutes (~1.1 hours with buffer)

---

## Migration Checklist (Per Script)

### Pre-Migration
- [ ] Read script to understand current functionality
- [ ] Check dependencies (imports, external calls)
- [ ] Identify all `print()` statements
- [ ] Note complexity (dataclasses? async? threading?)

### During Migration
- [ ] Add import: `from lib.logging_config import setup_logger`
- [ ] Initialize logger: `logger = setup_logger(__name__)`
- [ ] Replace print statements:
  - `print(f"Info: {x}")` → `logger.info(f"Info: {x}")`
  - `print(f"Error: {x}")` → `logger.error(f"Error: {x}")`
  - `print(f"Warning: {x}")` → `logger.warning(f"Warning: {x}")`
  - `print(f"Debug: {x}")` → `logger.debug(f"Debug: {x}")`
- [ ] Add type hints to function signatures
- [ ] Wrap risky operations in try/except with `logger.error()`
- [ ] Add comprehensive docstrings (Google style)
- [ ] Update shebang: `#!/usr/bin/env -S uv run python3`

### Post-Migration
- [ ] Test script functionality (manual run)
- [ ] Check output formatting (logs vs. stdout)
- [ ] Verify error handling works
- [ ] Update MANIFEST.json if needed
- [ ] Run pre-commit hooks: `git add ... && git commit -m "..."`

---

## Expected Outcomes (After Batch 1)

**Progress:**
- 15/77 → 20/77 scripts (26.0% completion)
- +6.5% progress
- P0 critical: 1/7 → 5/7 (71.4% of P0 complete)

**Impact:**
- ✅ Pre-commit validation fully on centralized logging
- ✅ Git hooks infrastructure standardized
- ✅ Cache + manifest utilities production-ready
- ✅ Citation reporting consistent with other validators

**Remaining P0 Critical (2 scripts):**
- `blog-content/humanization-validator.py` (1,184 lines)
- `blog-content/code-ratio-calculator.py` (526 lines)

---

## Follow-Up Actions

### Session 7: Complete P0
**Batch 2 - Content Quality (5 scripts, 1.2 hours)**

1. `blog-content/humanization-validator.py` (P0, 1,184 lines)
2. `blog-content/code-ratio-calculator.py` (P0, 526 lines)
3. `link-validation/link-monitor.py` (P0, 501 lines)
4. `blog-content/batch-improve-blog-posts.py` (P1, 628 lines)
5. `link-validation/batch-link-fixer.py` (P1, 420 lines)

**After Session 7:**
- P0 complete: 7/7 (100%)
- Overall: 25/77 (32.5%)

### Session 8: Complete P1
**Batch 3 - Infrastructure (6 scripts, 1.0 hour)**

1. `lib/parallel_validator.py` (153 lines)
2. `utilities/repo-maintenance.py` (848 lines)
3. `link-validation/link-report-generator.py` (457 lines)
4. `blog-research/check-citation-hyperlinks.py` (264 lines)
5. `blog-research/search-reputable-sources.py` (255 lines)
6. `blog-content/fix-mermaid-subgraphs.py` (166 lines)

**After Session 8:**
- P0+P1 complete: 15/15 (100%)
- Overall: 31/77 (40.3%)

### Sessions 9-10: P2 + P3 Audit
**Batch 4 - Research/Images (7 scripts, 1.2 hours)**

Plus: Audit P3 scripts for archival (37 scripts → reduce to ~20-25 actively maintained)

---

## Reference: Migration Pattern

```python
#!/usr/bin/env -S uv run python3
"""
SCRIPT: example.py
PURPOSE: Brief description
CATEGORY: category-name
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-02
"""

from pathlib import Path
from typing import List, Optional
from lib.logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)

def main() -> None:
    """Main entry point."""
    try:
        logger.info("Starting example process...")

        # Your logic here

        logger.info("Process completed successfully")
    except Exception as e:
        logger.error(f"Process failed: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

---

## Time Estimates Summary

| Batch | Scripts | Time | Completion % | Status |
|-------|---------|------|--------------|--------|
| **Batch 1** | 5 | 1.0 hr | 26.0% | ⚠ Next |
| **Batch 2** | 5 | 1.2 hrs | 32.5% | 🔜 Queued |
| **Batch 3** | 6 | 1.0 hr | 40.3% | 🔜 Queued |
| **Batch 4** | 7 | 1.2 hrs | 49.4% | 🔜 Queued |
| **Batch 5+** | 39 | 8.1 hrs | 100.0% | ⏸ Audit first |

**Total remaining:** 62 scripts, 12.5 hours

---

## Success Metrics

### After Batch 1 (Next Session)
- ✅ P0 critical path: 71.4% complete (5/7)
- ✅ Infrastructure (lib/) logging: 37.5% complete (3/8)
- ✅ Validation scripts: 50% complete (1/2)

### After Batches 1-3 (Sessions 6-8)
- ✅ P0+P1 complete: 100% (15/15)
- ✅ All critical + high-priority scripts migrated
- ✅ 40%+ overall completion
- ✅ Daily-use tools standardized

### Final Goal (All Batches)
- ✅ 100% of actively maintained scripts on centralized logging
- ✅ P3 scripts audited, archived, or migrated
- ✅ Total script count reduced (77 → 50-60)
- ✅ Documentation updated (SCRIPT_CATALOG.md)

---

## Related Documentation

- **Full Analysis:** `/home/william/git/williamzujkowski.github.io/reports/python-logging-migration-analysis.md`
- **Template:** `docs/context/templates/script-template.md` (503 lines)
- **Logging Config:** `scripts/lib/logging_config.py`
- **TODO.md:** Update after each batch completion

---

**Next Action:** Migrate Batch 1 (5 scripts, 1.0 hour)
**Expected Completion:** 2025-11-02 (same session or next)
**Blocker:** None - ready to execute
