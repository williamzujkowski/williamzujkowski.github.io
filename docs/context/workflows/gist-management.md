---
title: GitHub Gist Management Workflow
category: workflows
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1800
load_when:
  - Managing code examples
  - Blog post code ratio >20%
  - Creating shareable code snippets
dependencies: []
tags: [gist, code, github, management]
---

# GitHub Gist Management Workflow

## Module Metadata

**Category:** workflows
**Priority:** LOW
**Load When:** Managing code examples, blog post code ratio >20%, creating shareable code snippets
**Dependencies:** None
**Estimated Size:** ~1,800 tokens

---

## Purpose

This module documents the complete workflow for extracting blog code to GitHub gists to maintain <25% code-to-content ratio while keeping full implementations shareable.

---

## When to Load This Module

**Load this module when:**
- Managing code examples
- Blog post code ratio exceeds 20%
- Creating shareable code snippets
- Extracting verbose code blocks

**Skip this module if:**
- Code blocks <30 lines
- Essential 5-10 line patterns
- Mermaid diagrams (visual aids, not code)

---

## Quick Reference

**When to Extract:**
- Blog post code ratio >20% (target: <25%)
- Code blocks >30 lines
- Multiple related files (configs, scripts, workflows)

**Complete Gist Workflow:**
1. Create local gists folder (Phase 8.5)
2. Batch create GitHub gists (Phase 8.6)
3. Update blog posts with real gist URLs
4. Validate all gist links

---

## Overview

Blog posts maintain <25% code-to-content ratio by linking to GitHub gists instead of embedding verbose code blocks. The gist workflow extracts full implementations to shareable gists while keeping blog posts readable.

**Why use gists:**
- Keep blog posts focused (text + essential 5-10 line snippets)
- Share full implementations via direct links
- Enable download, fork, embed, and star features
- Improve reader experience with syntax highlighting

---

## When to Extract Code to Gists

**Extract to gists when:**
- Blog post code ratio >20% (target: <25%)
- Code blocks >30 lines (verbose implementations)
- Multiple related files (configs, scripts, workflows)
- Reusable code examples readers will copy

**Keep inline when:**
- Essential 5-10 line patterns demonstrating concepts
- Single commands or configuration snippets
- Mermaid diagrams (visual aids, not code)

---

## Complete Gist Workflow

### Phase 1: Create Local Gists Folder (Phase 8.5)

**1. Organize code by blog post category:**
```bash
mkdir -p gists/{category-name}/{workflows,configs,scripts,integrations}
```

**2. Extract code from blog posts to individual files:**
- Add descriptive headers with source attribution
- Include usage instructions and prerequisites
- Add MIT license

**3. Create category READMEs:**
- Quick start guide
- File descriptions
- Troubleshooting tips

**Example file structure:**
```
gists/
├── security-scanning/        # 13 files
│   ├── README.md
│   ├── workflows/           # GitHub Actions
│   ├── configs/             # Scanner configs
│   ├── scripts/             # Python/Bash scripts
│   └── integrations/        # Slack, Wazuh, etc.
├── mitre-dashboard/         # 8 files
├── vlan-segmentation/       # 14 files
└── proxmox-ha/              # 10 files
```

### Phase 2: Create GitHub Gists (Phase 8.6)

**1. Test gist creation (3 files first):**
```bash
python scripts/create-gists-from-folder.py --test-only
```

**2. Batch create all gists:**
```bash
python scripts/create-gists-from-folder.py
```

**Features:**
- Rate limiting (1 gist/second)
- Progress reporting
- Generates `gists/gist-mapping.json`
- `--dry-run` flag for testing

**3. Update blog posts with real gist URLs:**
```bash
python scripts/update-blog-gist-urls.py
```

**Replaces:**
`https://gist.github.com/williamzujkowski/{slug}` →
`https://gist.github.com/williamzujkowski/{real-gist-id}`

**4. Validate all gist links:**
```bash
python scripts/validate-gist-links.py
```

Checks all 45+ gist links return HTTP 200.

---

## Gist File Format Standards

**Required header for all code files:**
```python
#!/usr/bin/env python3
"""
Title: [Descriptive name]
Source: https://williamzujkowski.github.io/posts/[slug]/
Purpose: [What this code does]
Prerequisites: [Required tools/dependencies]
Usage:
    [Example commands]

License: MIT
"""
```

---

## Gist Mapping File

**Location:** `gists/gist-mapping.json`

**Format:**
```json
{
  "category/subcategory/filename.ext": {
    "url": "https://gist.github.com/williamzujkowski/abc123...",
    "slug": "descriptive-slug-name",
    "description": "Brief description for gist"
  }
}
```

**Usage:**
- Source of truth for all gist URLs
- Used by `update-blog-gist-urls.py` to replace placeholders
- Used by `validate-gist-links.py` to verify links

---

## Maintenance

**Weekly validation:**
```bash
python scripts/validate-gist-links.py --verbose
```

**Update existing gist:**
1. Edit file in `/gists` directory
2. Manually update gist on GitHub
3. No URL change needed (gist ID stays the same)

**Add new gist:**
1. Create file in appropriate `/gists` subdirectory
2. Add metadata to `scripts/create-gists-from-folder.py` GIST_METADATA
3. Run: `python scripts/create-gists-from-folder.py`
4. Update blog post with new gist URL

---

## Troubleshooting

**Slug mismatch errors:**
- Check blog post uses correct slug from `gist-mapping.json`
- Run: `python scripts/update-blog-gist-urls.py` to fix

**Gist creation fails:**
- Verify `gh` CLI authenticated: `gh auth status`
- Check rate limiting (1 gist/second)
- Ensure file exists in `/gists` directory

**Broken gist links:**
- Run validator: `python scripts/validate-gist-links.py`
- Check gist not deleted on GitHub
- Verify URL in blog post matches `gist-mapping.json`

---

## Cross-References

### Related Modules
- [blog-writing.md](./blog-writing.md) - Code integration standards

### External References
- [GitHub Gist Documentation](https://docs.github.com/en/get-started/writing-on-github/editing-and-sharing-content-with-gists)

---

## Examples

### Example 1: Extract Code from Blog Post

```bash
# 1. Analyze blog post code ratio
python scripts/blog-content/optimize-blog-content.py

# Output: Post has 35% code ratio (target: <25%)
# Extract: 3 code blocks (120+ lines each)

# 2. Create gist directory
mkdir -p gists/security-scanning/scripts

# 3. Extract code blocks to files
# (manual extraction with proper headers)

# 4. Create gists
python scripts/create-gists-from-folder.py

# 5. Update blog post with gist links
python scripts/update-blog-gist-urls.py

# 6. Validate
python scripts/validate-gist-links.py

# Result: Code ratio reduced to 18%
```

**Explanation:** Complete workflow from analysis to validation.

### Example 2: Required Gist Header Format

```python
#!/usr/bin/env python3
"""
Title: Container Security Scanner with Slack Integration
Source: https://williamzujkowski.github.io/posts/2024-03-15-container-security/
Purpose: Automated Docker image vulnerability scanning with Trivy and Slack notifications
Prerequisites:
    - Python 3.8+
    - Docker installed
    - Trivy CLI installed
    - Slack webhook URL (set SLACK_WEBHOOK environment variable)
Usage:
    python security_scanner.py --image nginx:latest
    python security_scanner.py --image nginx:latest --severity HIGH,CRITICAL

License: MIT
"""
```

**Explanation:** Proper attribution and usage instructions for readers.

---

## Common Pitfalls

### Pitfall 1: Forgetting Rate Limiting
**Problem:** Batch creating 50 gists triggers GitHub rate limits
**Solution:** Script enforces 1 gist/second (built-in)
**Prevention:** Use `--test-only` flag first

### Pitfall 2: Missing Gist Mapping Updates
**Problem:** Blog post links to placeholder URL, not real gist
**Solution:** Run `update-blog-gist-urls.py` after creating gists
**Prevention:** Include URL update in workflow checklist

### Pitfall 3: Deleting Gists on GitHub
**Problem:** Broken links in blog posts
**Solution:** Don't delete gists, update content in place
**Prevention:** Treat gists as permanent, versioned resources

---

## Validation

### How to Verify Correct Application

**Checklist:**
- [ ] Blog post code ratio <25%
- [ ] All gist files have proper headers
- [ ] `gist-mapping.json` updated
- [ ] Blog posts use real gist URLs (not placeholders)
- [ ] All gist links return HTTP 200

**Commands:**
```bash
# Check blog post code ratio
python scripts/blog-content/optimize-blog-content.py

# Validate all gist links
python scripts/validate-gist-links.py --verbose

# Verify gist mapping
cat gists/gist-mapping.json | jq 'keys'
```

---

## Changelog

### Version 1.0.0 (2025-11-01)
- Initial extraction from CLAUDE.md section "GitHub Gist Management"
- Complete workflow with all phases
- Troubleshooting and validation added
- Examples with proper formatting

---

## Maintenance Notes

**Review Schedule:** Quarterly
**Last Review:** 2025-11-01
**Next Review:** 2026-02-01
**Maintainer:** Content Team

---

**Parent Index:** [../../INDEX.yaml](../../INDEX.yaml)
**Category Index:** [../index.md](../index.md)
