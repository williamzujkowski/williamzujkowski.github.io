# Vestigial Content Audit Report

**Generated:** 2025-09-20 15:01:53
**Version:** 1.0.0

## Summary
- **Vestigial files found:** 15
- **Potential space saved:** 0.00 MB

## Detailed Findings

### Duplicate Functionality (15)
- `integrate-diagrams.py` ↔ `add-tech-images.py` (similarity: 80.00%)
- `integrate-diagrams.py` ↔ `remove-hero-images.py` (similarity: 72.73%)
- `integrate-diagrams.py` ↔ `create-blog-diagrams.py` (similarity: 72.73%)
- `integrate-diagrams.py` ↔ `add-diagrams-to-live-posts.py` (similarity: 80.00%)
- `add-tech-images.py` ↔ `remove-hero-images.py` (similarity: 72.73%)
- `add-tech-images.py` ↔ `create-blog-diagrams.py` (similarity: 72.73%)
- `add-tech-images.py` ↔ `add-diagrams-to-live-posts.py` (similarity: 80.00%)
- `remove-hero-images.py` ↔ `add-diagrams-to-live-posts.py` (similarity: 72.73%)
- `create-blog-diagrams.py` ↔ `add-diagrams-to-live-posts.py` (similarity: 72.73%)
- `batch-improve-blog-posts.py` ↔ `research-validator.py` (similarity: 77.78%)
- `batch-improve-blog-posts.py` ↔ `comprehensive-blog-enhancement.py` (similarity: 88.89%)
- `batch-improve-blog-posts.py` ↔ `analyze-blog-content.py` (similarity: 84.21%)
- `research-validator.py` ↔ `comprehensive-blog-enhancement.py` (similarity: 77.78%)
- `research-validator.py` ↔ `analyze-blog-content.py` (similarity: 84.21%)
- `comprehensive-blog-enhancement.py` ↔ `analyze-blog-content.py` (similarity: 84.21%)

## Recommendations

### Safe to Remove
- All `.bak` files older than 30 days
- Empty directories
- Test artifacts in non-test directories

### Requires Review
- Duplicate functionality scripts
- Large unused files
- Unreferenced documentation

### Actions
1. Backup the repository before cleanup
2. Run `python scripts/remove_vestigial.py --safe` to remove safe items
3. Manually review duplicate functionality
4. Update MANIFEST.json after cleanup