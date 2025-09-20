# Link Repair Action Plan

**Generated:** 2025-09-20 12:34:06

## Phase 1: Automatic Fixes (38 links)

These fixes have high confidence and can be applied automatically:

```bash
python scripts/link-validation/batch-link-fixer.py \
    --repairs repairs.json \
    --confidence-threshold 90 \
    --apply
```

## Phase 2: Semi-Automatic Fixes (11 links)

These fixes should be reviewed before applying:

```bash
python scripts/link-validation/batch-link-fixer.py \
    --repairs repairs.json \
    --confidence-threshold 70 \
    --dry-run
```

## Phase 3: Manual Review (0 links)

These require manual investigation:

Review the `manual_review.md` file for detailed items.

## Validation Commands

After applying fixes, rerun validation:

```bash
# Re-extract links
python scripts/link-validation/link-extractor.py

# Re-validate
python scripts/link-validation/link-validator.py

# Check relevance
python scripts/link-validation/content-relevance-checker.py
```