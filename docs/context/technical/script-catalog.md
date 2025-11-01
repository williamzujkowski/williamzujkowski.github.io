---
title: Script Catalog & Reference
category: technical
priority: MEDIUM
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 2000
load_when:
  - Finding automation scripts
  - Understanding script organization
  - Running blog utilities
dependencies:
  - reference/directory-structure
tags: [scripts, automation, utilities, catalog]
---

# Script Catalog & Reference

This document catalogs all automation scripts in the repository, organized by category for quick reference.

## Total Scripts Inventory

**Total Active Scripts**: 35 Python scripts + 2 Shell scripts

## Script Organization

### `/scripts/blog-content/` - Content Management & Optimization (6 scripts)

Content analysis, enhancement, and validation tools.

**Scripts:**
- `analyze-blog-content.py` - Analyze blog posts for code ratios, citations, structure
- `batch-improve-blog-posts.py` - Batch transform posts using Smart Brevity methodology
- `blog-manager.py` - Central management interface for blog operations
- `comprehensive-blog-enhancement.py` - Full enhancement pipeline (citations, structure, humanization)
- `humanization-validator.py` - v2.0: 155x faster batch validation (0.74s for 57 posts)
- `optimize-blog-content.py` - Identify and fix high code-to-content ratios

**Quick Commands:**
```bash
# Analyze code ratios
python scripts/blog-content/optimize-blog-content.py

# Validate humanization (single post)
python scripts/blog-content/humanization-validator.py --post src/posts/example.md

# Batch validate all posts
python scripts/blog-content/humanization-validator.py --batch

# Find posts needing attention
python scripts/blog-content/humanization-validator.py --batch --filter-below 90
```

### `/scripts/blog-images/` - Image Generation & Management (6 scripts)

Hero image generation, optimization, and metadata management.

**Scripts:**
- `enhanced-blog-image-search.py` - Advanced image search with multiple sources
- `fetch-stock-images.py` - Download copyright-free stock images
- `generate-blog-hero-images.py` - Create hero images with topic-based styling
- `generate-og-image.py` - Generate Open Graph images for social sharing
- `playwright-image-search.py` - Automated image search using Playwright
- `update-blog-images.py` - Update blog post image metadata

**Quick Commands:**
```bash
# Update image metadata
python scripts/blog-images/update-blog-images.py

# Generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# Optimize images
bash scripts/optimize-blog-images.sh
```

### `/scripts/blog-research/` - Academic Citations & Research (7 scripts)

Research validation, citation management, and academic source discovery.

**Scripts:**
- `academic-search.py` - Search arXiv, Zenodo, CORE for academic papers
- `add-academic-citations.py` - Add citations to blog posts
- `add-reputable-sources-to-posts.py` - Integrate reputable sources automatically
- `check-citation-hyperlinks.py` - Validate all citation links are working
- `enhance-more-posts-citations.py` - Batch citation enhancement
- `research-validator.py` - Validate research claims in posts
- `search-reputable-sources.py` - Find authoritative sources for claims

**Quick Commands:**
```bash
# Validate research claims
python scripts/blog-research/research-validator.py --post src/posts/example.md

# Search academic sources
python scripts/blog-research/academic-search.py --query "quantum computing" --sources "arxiv,zenodo,core"

# Add citations
python scripts/blog-research/add-academic-citations.py --post src/posts/example.md

# Check citation hyperlinks
python scripts/blog-research/check-citation-hyperlinks.py
```

### `/scripts/link-validation/` - Link Validation & Repair (12 scripts)

Comprehensive link validation, repair, and archival tools.

**Scripts:**
- `advanced-link-repair.py` - Intelligent link repair with fallbacks
- `batch-link-fixer.py` - Batch fix broken links across all posts
- `citation-repair.py` - Repair broken citation links
- `citation-updater.py` - Update citation URLs systematically
- `content-relevance-checker.py` - Verify link relevance to content
- `link-extractor.py` - Extract all links from blog posts
- `link-monitor.py` - Continuous link health monitoring
- `link-report-generator.py` - Generate link health reports
- `link-validator.py` - Validate all links return HTTP 200
- `simple-validator.py` - Quick link validation
- `specialized-validators.py` - Domain-specific validation (arXiv, GitHub, etc.)
- `wayback-archiver.py` - Archive broken links using Wayback Machine

**Quick Commands:**
```bash
# Validate all links
python scripts/link-validation/link-validator.py

# Fix broken links
python scripts/link-validation/batch-link-fixer.py

# Generate link health report
python scripts/link-validation/link-report-generator.py
```

### `/scripts/utilities/` - General Utilities (3 scripts)

Cross-cutting utilities for diagrams, validation, and documentation.

**Scripts:**
- `diagram-manager.py` - Generate and manage Mermaid diagrams
- `final-validation.py` - Pre-deployment validation checks
- `llm-script-documenter.py` - Auto-document scripts for LLM understanding

**Quick Commands:**
```bash
# Generate diagram templates
python scripts/utilities/diagram-manager.py

# Run final validation
python scripts/utilities/final-validation.py
```

### `/scripts/lib/` - Shared Libraries (2 files)

Common functions and utilities used by other scripts.

**Files:**
- `common.py` - Common Python functions (file I/O, frontmatter parsing, logging)
- `memory-file.sh` - Memory management shell functions for build optimization

### Shell Scripts (2 scripts)

**Root-level scripts:**
- `scripts/optimize-blog-images.sh` - Optimize images and create responsive variants

## Script Usage Patterns

### Daily Blog Workflow

When creating/editing blog posts:
```bash
# 1. Update image metadata
python scripts/blog-images/update-blog-images.py

# 2. Generate hero images
python scripts/blog-images/generate-blog-hero-images.py

# 3. Optimize images
bash scripts/optimize-blog-images.sh

# 4. Validate citations
python scripts/blog-research/research-validator.py

# 5. Check links
python scripts/blog-research/check-citation-hyperlinks.py

# 6. Validate humanization (MANDATORY before commit)
python scripts/blog-content/humanization-validator.py --post src/posts/[file].md
```

### Monthly Maintenance

```bash
# Portfolio-wide humanization report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/monthly-$(date +%Y-%m).json

# Link health check
python scripts/link-validation/link-validator.py

# Generate link report
python scripts/link-validation/link-report-generator.py
```

### Research Enhancement

```bash
# Find posts needing more citations
python scripts/blog-content/optimize-blog-content.py

# Search academic sources
python scripts/blog-research/academic-search.py --query "specific topic" --sources "arxiv,zenodo,core"

# Add citations
python scripts/blog-research/add-academic-citations.py --post src/posts/[file].md
```

## Script Development Guidelines

### Adding New Scripts

1. **Choose appropriate category**: blog-content, blog-images, blog-research, link-validation, utilities
2. **Follow naming convention**: descriptive-action-target.py
3. **Add to this catalog**: Update this document with script purpose and commands
4. **Document in docstrings**: Include usage examples, parameters, return values
5. **Add to MANIFEST.json**: Update file registry

### Common Functions

Use `/scripts/lib/common.py` for shared functionality:
- File I/O operations
- Frontmatter parsing
- Logging configuration
- Error handling
- Progress reporting

### Testing Scripts

```bash
# Test single script
python scripts/category/script-name.py --help

# Dry-run mode (if available)
python scripts/category/script-name.py --dry-run

# Verbose output
python scripts/category/script-name.py --verbose
```

## Maintenance Notes

**Script Retention Policy:**
- Keep production scripts referenced in CLAUDE.md
- Archive superseded scripts to `/docs/archive/`
- Delete temporary troubleshooting scripts after use
- Update this catalog when adding/removing scripts

**Common Script Patterns:**
- All scripts support `--help` flag
- Most support `--dry-run` for testing
- Many support `--verbose` for detailed output
- Batch operations support `--limit` for testing

## Quick Reference

| Task | Script | Category |
|------|--------|----------|
| Validate humanization | `humanization-validator.py` | blog-content |
| Generate hero images | `generate-blog-hero-images.py` | blog-images |
| Check citations | `check-citation-hyperlinks.py` | blog-research |
| Validate links | `link-validator.py` | link-validation |
| Optimize images | `optimize-blog-images.sh` | root |
| Search academic papers | `academic-search.py` | blog-research |
| Generate diagrams | `diagram-manager.py` | utilities |

## Related Documentation

- **Script Catalog Guide**: `docs/GUIDES/SCRIPT_CATALOG.md` (comprehensive reference)
- **LLM Onboarding**: `docs/GUIDES/LLM_ONBOARDING.md` (quick start)
- **Directory Structure**: `docs/ARCHITECTURE.md` (repository organization)
