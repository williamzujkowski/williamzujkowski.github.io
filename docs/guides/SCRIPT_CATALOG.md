# Script Catalog

**Generated:** 2025-11-02
**Total Scripts:** 56
**Categories:** 9

This catalog provides comprehensive documentation for all automation scripts in the repository. Scripts are organized by category with usage examples, dependencies, and related tools.

---

## Table of Contents

- [Blog Content Management (12 scripts)](#blog-content-management)
- [Blog Research & Citations (7 scripts)](#blog-research--citations)
- [Blog Images (6 scripts)](#blog-images)
- [Link Validation (12 scripts)](#link-validation)
- [Validation & Monitoring (4 scripts)](#validation--monitoring)
- [Utilities (10 scripts)](#utilities)
- [Maintenance (1 script)](#maintenance)
- [Library (2 scripts)](#library)
- [Root Scripts (2 scripts)](#root-scripts)

---

## Blog Content Management

Scripts for analyzing, optimizing, and enhancing blog post content quality.

### analyze-blog-content.py

**Location:** `scripts/blog-content/analyze-blog-content.py`
**Purpose:** Analyze blog posts for content quality metrics and improvement opportunities
**Version:** 2.0.0

**Description:**
Comprehensive blog content analysis tool that evaluates posts for readability scores (Flesch-Kincaid), code-to-content ratio, SEO optimization, image usage, citation quality, and content structure.

**Usage:**
```bash
# Analyze all posts
python scripts/blog-content/analyze-blog-content.py

# Generate markdown report
python scripts/blog-content/analyze-blog-content.py --format markdown

# Check specific metrics
python scripts/blog-content/analyze-blog-content.py --metrics readability,seo
```

**Key Dependencies:** re, frontmatter, argparse
**Related Scripts:** optimize-blog-content.py, batch-improve-blog-posts.py
**File Size:** 15,228 bytes | Lines: 374

---

### batch-improve-blog-posts.py

**Location:** `scripts/blog-content/batch-improve-blog-posts.py`
**Purpose:** Systematically improve all blog posts with diagrams, reduced code, and enhanced content
**Version:** 2.0.0

**Description:**
Batch processing tool for comprehensive blog post improvements including Mermaid diagram generation, code block reduction, content enhancement, SEO optimization, image integration, and citation addition.

**Usage:**
```bash
# Improve all posts
python scripts/blog-content/batch-improve-blog-posts.py

# Process specific improvements
python scripts/blog-content/batch-improve-blog-posts.py --improvements diagrams,code

# Batch process with parallel execution
python scripts/blog-content/batch-improve-blog-posts.py --parallel --batch-size 10
```

**Key Dependencies:** frontmatter, argparse
**Related Scripts:** analyze-blog-content.py, optimize-blog-content.py
**File Size:** 19,171 bytes | Lines: 612

---

### blog-manager.py

**Location:** `scripts/blog-content/blog-manager.py`
**Purpose:** Unified Blog Management Tool for williamzujkowski.github.io
**Version:** 1.0.0

**Description:**
Central management tool for all blog-related operations including content analysis, validation, and automation workflows.

**Usage:**
```bash
# Basic usage
python scripts/blog-content/blog-manager.py

# With verbose output
python scripts/blog-content/blog-manager.py --verbose
```

**Key Dependencies:** yaml, argparse, subprocess
**Related Scripts:** analyze-blog-content.py, validate-all-posts.py
**File Size:** 16,008 bytes | Lines: 460

---

### comprehensive-blog-enhancement.py

**Location:** `scripts/blog-content/comprehensive-blog-enhancement.py`
**Purpose:** Comprehensive Blog Enhancement Tool
**Version:** 1.0.0

**Description:**
Comprehensive enhancement tool combining multiple optimization techniques for complete blog post improvement workflows.

**Usage:**
```bash
# Basic usage
python scripts/blog-content/comprehensive-blog-enhancement.py

# With verbose output
python scripts/blog-content/comprehensive-blog-enhancement.py --verbose
```

**Key Dependencies:** frontmatter, argparse
**Related Scripts:** batch-improve-blog-posts.py
**File Size:** 15,685 bytes | Lines: 409

---

### full-post-validation.py

**Location:** `scripts/blog-content/full-post-validation.py`
**Purpose:** Comprehensive blog post validation combining humanization, citations, and content quality checks
**Version:** 1.0.0

**Description:**
Comprehensive pre-publish validation tool that combines humanization checks (AI-tells, tone, sentiment), citation coverage and link validation, content quality (bullets, weak language, readability), Smart Brevity principles, and accessibility requirements.

**Usage:**
```bash
# Validate single post
python scripts/blog-content/full-post-validation.py --post src/posts/2025-01-15-example.md

# Strict validation with report
python scripts/blog-content/full-post-validation.py --post src/posts/example.md --strict --report-file validation-report.md

# JSON output for CI/CD
python scripts/blog-content/full-post-validation.py --post src/posts/example.md --output json
```

**Key Dependencies:** yaml, frontmatter
**Related Scripts:** humanization-validator.py, research-validator.py
**File Size:** 20,024 bytes | Lines: 530

---

### humanization-validator.py

**Location:** `scripts/blog-content/humanization-validator.py`
**Purpose:** Validate blog posts for human tone and detect AI-generated content tells
**Version:** 2.0.0

**Description:**
Validates blog posts against humanization requirements to ensure authentic, engaging content. Checks for AI-tells (em dashes, semicolons, generic transitions), required humanization elements (first-person, uncertainty, specificity), sentiment analysis, and corporate jargon. Version 2.0 includes batch processing with parallel execution.

**Usage:**
```bash
# Validate single post
python scripts/blog-content/humanization-validator.py --post src/posts/2025-01-15-example.md

# Batch validate all posts
python scripts/blog-content/humanization-validator.py --batch

# Batch with filtering and JSON output
python scripts/blog-content/humanization-validator.py --batch --filter-below 90 --format json

# Save batch report
python scripts/blog-content/humanization-validator.py --batch --save-report reports/validation-2025-10-29.json
```

**Key Dependencies:** multiprocessing, collections
**Related Scripts:** full-post-validation.py
**File Size:** 48,302 bytes | Lines: 1,157

---

### optimize-blog-content.py

**Location:** `scripts/blog-content/optimize-blog-content.py`
**Purpose:** Analyze and optimize blog posts for readability by reducing code-to-content ratio
**Version:** 2.0.0

**Description:**
Analyzes blog posts to identify where code can be reduced and replaced with diagrams. Targets posts with >25% code-to-content ratio and suggests optimizations including Mermaid diagrams, GitHub gists, and visual alternatives.

**Usage:**
```bash
# Analyze all posts
python scripts/blog-content/optimize-blog-content.py

# Fix posts with high code ratio
python scripts/blog-content/optimize-blog-content.py --fix --threshold 0.30

# Generate detailed report
python scripts/blog-content/optimize-blog-content.py --output reports/optimization.json
```

**Key Dependencies:** yaml
**Related Scripts:** diagram-manager.py, analyze-blog-content.py
**File Size:** 16,900 bytes | Lines: 398

---

### analyze-compliance.py

**Location:** `scripts/blog-content/analyze-compliance.py`
**Purpose:** Analyze blog posts for CLAUDE.md compliance

**Description:**
Evaluates Smart Brevity violations (weak language, verbosity), AI skepticism presence, BLUF structure, paragraph length, and bullet usage.

**Usage:**
```bash
python scripts/blog-content/analyze-compliance.py
```

**Key Dependencies:** collections
**File Size:** 9,176 bytes | Lines: 279

---

### generate-stats-dashboard.py

**Location:** `scripts/blog-content/generate-stats-dashboard.py`
**Purpose:** Generate HTML statistics dashboard for blog post quality metrics

**Description:**
Reads from portfolio-assessment.json and generates an interactive dashboard with blog statistics and quality metrics.

**Usage:**
```bash
python scripts/blog-content/generate-stats-dashboard.py
```

**Key Dependencies:** collections, datetime
**File Size:** 15,663 bytes | Lines: 528

---

### validate-all-posts.py

**Location:** `scripts/blog-content/validate-all-posts.py`
**Purpose:** Portfolio-Wide Humanization Validation

**Description:**
Validates all blog posts and generates comprehensive assessment report for portfolio-wide quality checks.

**Usage:**
```bash
python scripts/blog-content/validate-all-posts.py --output docs/reports/
python scripts/blog-content/validate-all-posts.py --format json
python scripts/blog-content/validate-all-posts.py --threshold 75
```

**Key Dependencies:** subprocess, collections
**File Size:** 12,030 bytes | Lines: 368

---

### fix-mermaid-subgraphs.py

**Location:** `scripts/blog-content/fix-mermaid-subgraphs.py`
**Purpose:** Fix Mermaid subgraph syntax errors in blog posts
**Version:** 1.0.0

**Description:**
Automatically detects and fixes Mermaid subgraph syntax errors across all blog posts. Creates backup files before modification and provides detailed logging of changes.

**Usage:**
```bash
# Fix all Mermaid subgraph syntax errors
python scripts/blog-content/fix-mermaid-subgraphs.py

# Dry run to preview changes
python scripts/blog-content/fix-mermaid-subgraphs.py --dry-run
```

**Key Dependencies:** re, pathlib
**Related Scripts:** validate-mermaid-syntax.py
**File Size:** 5,054 bytes | Lines: 166

---

### validate-mermaid-syntax.py

**Location:** `scripts/blog-content/validate-mermaid-syntax.py`
**Purpose:** Validate Mermaid diagram syntax across all blog posts
**Version:** 1.0.0

**Description:**
Pattern-based syntax validation for Mermaid diagrams. Detects common errors including subgraph syntax, quote mismatches, arrow syntax, and bracket errors. Generates comprehensive validation reports without modifying files.

**Usage:**
```bash
# Validate all blog posts
python scripts/blog-content/validate-mermaid-syntax.py

# Validate with detailed output
python scripts/blog-content/validate-mermaid-syntax.py --verbose

# Generate JSON report
python scripts/blog-content/validate-mermaid-syntax.py --format json
```

**Key Dependencies:** re, pathlib, collections
**Related Scripts:** fix-mermaid-subgraphs.py
**File Size:** 6,342 bytes | Lines: 184

---

## Blog Research & Citations

Scripts for academic research, citation management, and source validation.

### academic-search.py

**Location:** `scripts/blog-research/academic-search.py`
**Purpose:** Academic Search - Use Playwright to search reputable academic sources
**Version:** 1.0.0

**Description:**
Automated academic source searching using Playwright browser automation to find credible citations for blog posts.

**Usage:**
```bash
# Basic usage
python scripts/blog-research/academic-search.py

# With verbose output
python scripts/blog-research/academic-search.py --verbose
```

**Key Dependencies:** playwright.async_api, asyncio, argparse
**Related Scripts:** search-reputable-sources.py, add-academic-citations.py
**File Size:** 13,989 bytes | Lines: 375

---

### add-academic-citations.py

**Location:** `scripts/blog-research/add-academic-citations.py`
**Purpose:** Add academic citations to blog posts based on research validation results
**Version:** 1.0.0

**Description:**
Automatically adds properly formatted academic citations to blog posts from research validation results.

**Usage:**
```bash
python scripts/blog-research/add-academic-citations.py
python scripts/blog-research/add-academic-citations.py --verbose
```

**Key Dependencies:** frontmatter
**Related Scripts:** research-validator.py, academic-search.py
**File Size:** 14,475 bytes | Lines: 353

---

### add-reputable-sources-to-posts.py

**Location:** `scripts/blog-research/add-reputable-sources-to-posts.py`
**Purpose:** Add reputable academic sources to blog posts based on Google Scholar findings
**Version:** 1.0.0

**Description:**
Integrates reputable academic sources from Google Scholar searches into existing blog posts.

**Usage:**
```bash
python scripts/blog-research/add-reputable-sources-to-posts.py
```

**Key Dependencies:** frontmatter
**File Size:** 8,231 bytes | Lines: 194

---

### check-citation-hyperlinks.py

**Location:** `scripts/blog-research/check-citation-hyperlinks.py`
**Purpose:** Check all blog posts for citations that lack hyperlinks
**Version:** 1.0.0

**Description:**
Validates that all citations in blog posts include proper hyperlinks to their sources, ensuring citation coverage standards.

**Usage:**
```bash
python scripts/blog-research/check-citation-hyperlinks.py
python scripts/blog-research/check-citation-hyperlinks.py --verbose
```

**Key Dependencies:** pathlib
**Related Scripts:** research-validator.py
**File Size:** 6,420 bytes | Lines: 179

---

### enhance-more-posts-citations.py

**Location:** `scripts/blog-research/enhance-more-posts-citations.py`
**Purpose:** Add academic citations to additional blog posts
**Version:** 1.0.0

**Description:**
Batch enhancement tool for adding citations to multiple blog posts in a single operation.

**Usage:**
```bash
python scripts/blog-research/enhance-more-posts-citations.py
```

**Key Dependencies:** frontmatter
**File Size:** 10,959 bytes | Lines: 300

---

### research-validator.py

**Location:** `scripts/blog-research/research-validator.py`
**Purpose:** Research Validator - Ensures all blog post claims are backed by reputable sources
**Version:** 1.0.0

**Description:**
Comprehensive validation tool that checks blog posts for proper citation coverage, ensuring all factual claims are backed by reputable sources.

**Usage:**
```bash
python scripts/blog-research/research-validator.py
python scripts/blog-research/research-validator.py --verbose
```

**Key Dependencies:** frontmatter, argparse
**Related Scripts:** check-citation-hyperlinks.py, add-academic-citations.py
**File Size:** 11,727 bytes | Lines: 296

---

### search-reputable-sources.py

**Location:** `scripts/blog-research/search-reputable-sources.py`
**Purpose:** Search for reputable sources using Playwright to back up technical claims in blog posts
**Version:** 1.0.0

**Description:**
Browser automation tool for searching and validating reputable sources for technical claims in blog content.

**Usage:**
```bash
python scripts/blog-research/search-reputable-sources.py
```

**Key Dependencies:** playwright.async_api, asyncio, frontmatter
**File Size:** 8,057 bytes | Lines: 227

---

## Blog Images

Scripts for image generation, optimization, and management.

### enhanced-blog-image-search.py

**Location:** `scripts/blog-images/enhanced-blog-image-search.py`
**Purpose:** Enhanced Blog Image Search Tool
**Version:** 1.0.0

**Description:**
Advanced image search and download tool for finding relevant blog post images from copyright-free sources.

**Usage:**
```bash
python scripts/blog-images/enhanced-blog-image-search.py
python scripts/blog-images/enhanced-blog-image-search.py --verbose
```

**Key Dependencies:** PIL, argparse
**File Size:** 14,882 bytes | Lines: 357

---

### fetch-stock-images.py

**Location:** `scripts/blog-images/fetch-stock-images.py`
**Purpose:** Stock Image Fetcher for Blog Posts
**Version:** 1.0.0

**Description:**
Automated stock image fetching from free image repositories with proper attribution handling.

**Usage:**
```bash
python scripts/blog-images/fetch-stock-images.py
```

**Key Dependencies:** yaml, requests, hashlib
**File Size:** 11,568 bytes | Lines: 311

---

### generate-blog-hero-images.py

**Location:** `scripts/blog-images/generate-blog-hero-images.py`
**Purpose:** Generate Hero Images for Blog Posts
**Version:** 1.0.0

**Description:**
Automated hero image generation with topic-based color schemes and pattern overlays for visual consistency.

**Usage:**
```bash
python scripts/blog-images/generate-blog-hero-images.py
```

**Key Dependencies:** PIL, yaml, hashlib, colorsys
**File Size:** 16,842 bytes | Lines: 452

---

### generate-og-image.py

**Location:** `scripts/blog-images/generate-og-image.py`
**Purpose:** Generate Open Graph images for social sharing
**Version:** 1.0.0

**Description:**
Creates optimized Open Graph images (1200x630px) for social media sharing previews.

**Usage:**
```bash
python scripts/blog-images/generate-og-image.py
```

**Key Dependencies:** PIL, textwrap
**File Size:** 5,820 bytes | Lines: 163

---

### playwright-image-search.py

**Location:** `scripts/blog-images/playwright-image-search.py`
**Purpose:** Playwright-based Stock Image Search and Download
**Version:** 1.0.0

**Description:**
Browser automation for searching and downloading stock images with proper licensing verification.

**Usage:**
```bash
python scripts/blog-images/playwright-image-search.py
```

**Key Dependencies:** playwright.async_api, aiohttp, aiofiles, yaml
**File Size:** 16,005 bytes | Lines: 406

---

### update-blog-images.py

**Location:** `scripts/blog-images/update-blog-images.py`
**Purpose:** Blog Image Standards Implementation Script
**Version:** 1.0.0

**Description:**
Updates blog post frontmatter with proper image metadata following the blog image standards.

**Usage:**
```bash
python scripts/blog-images/update-blog-images.py
```

**Key Dependencies:** yaml
**File Size:** 9,714 bytes | Lines: 259

---

## Link Validation

Scripts for link checking, validation, and repair across all blog posts.

### advanced-link-repair.py

**Location:** `scripts/link-validation/advanced-link-repair.py`
**Purpose:** Advanced Link Repair System
**Version:** 1.0.0

**Description:**
Sophisticated link repair system using multiple strategies including Wayback Machine lookup, URL pattern matching, and domain resolution.

**Usage:**
```bash
python scripts/link-validation/advanced-link-repair.py
python scripts/link-validation/advanced-link-repair.py --verbose
```

**Key Dependencies:** asyncio, urllib.parse, difflib, argparse
**File Size:** 17,954 bytes | Lines: 479

---

### batch-link-fixer.py

**Location:** `scripts/link-validation/batch-link-fixer.py`
**Purpose:** Batch Link Fixer
**Version:** 1.0.0

**Description:**
Batch processing tool for fixing broken links across multiple blog posts simultaneously.

**Usage:**
```bash
python scripts/link-validation/batch-link-fixer.py
```

**Key Dependencies:** subprocess, shutil, argparse
**File Size:** 14,057 bytes | Lines: 388

---

### citation-repair.py

**Location:** `scripts/link-validation/citation-repair.py`
**Purpose:** Citation Repair Tool
**Version:** 1.0.0

**Description:**
Specialized tool for repairing broken citation links with academic source verification.

**Usage:**
```bash
python scripts/link-validation/citation-repair.py
```

**Key Dependencies:** aiohttp, asyncio, urllib.parse, argparse
**File Size:** 21,803 bytes | Lines: 597

---

### citation-report.py

**Location:** `scripts/link-validation/citation-report.py`
**Purpose:** Generate citation-specific validation report for GitHub Actions
**Version:** 1.0.0

**Description:**
Generates markdown reports specifically for citation link validation, designed for GitHub Actions workflows.

**Usage:**
```bash
python scripts/link-validation/citation-report.py --input validation.json --links links.json --output report.md
```

**Key Dependencies:** collections, argparse
**File Size:** 9,224 bytes | Lines: 264

---

### citation-updater.py

**Location:** `scripts/link-validation/citation-updater.py`
**Purpose:** Citation Updater
**Version:** 1.0.0

**Description:**
Updates citation links with latest working URLs while maintaining proper academic formatting.

**Usage:**
```bash
python scripts/link-validation/citation-updater.py
```

**Key Dependencies:** aiohttp, asyncio, dataclasses, argparse
**File Size:** 19,225 bytes | Lines: 489

---

### content-relevance-checker.py

**Location:** `scripts/link-validation/content-relevance-checker.py`
**Purpose:** Content Relevance Checker
**Version:** 1.0.0

**Description:**
Validates that linked content is still relevant to the blog post context using similarity scoring.

**Usage:**
```bash
python scripts/link-validation/content-relevance-checker.py
```

**Key Dependencies:** sklearn.metrics.pairwise, numpy, difflib
**File Size:** 18,347 bytes | Lines: 534

---

### link-extractor.py

**Location:** `scripts/link-validation/link-extractor.py`
**Purpose:** Link Extractor for Blog Posts
**Version:** 1.0.0

**Description:**
Extracts all links from blog posts for validation and analysis purposes.

**Usage:**
```bash
python scripts/link-validation/link-extractor.py
```

**Key Dependencies:** dataclasses, argparse, hashlib
**File Size:** 11,318 bytes | Lines: 327

---

### link-monitor.py

**Location:** `scripts/link-validation/link-monitor.py`
**Purpose:** Link Monitor
**Version:** 1.0.0

**Description:**
Continuous monitoring system for tracking link health over time with alerting capabilities.

**Usage:**
```bash
python scripts/link-validation/link-monitor.py
```

**Key Dependencies:** aiohttp, asyncio, email.mime.text, smtplib, dataclasses
**File Size:** 18,054 bytes | Lines: 486

---

### link-report-generator.py

**Location:** `scripts/link-validation/link-report-generator.py`
**Purpose:** Link Validation Report Generator
**Version:** 1.0.0

**Description:**
Generates comprehensive reports on link validation results with multiple output formats.

**Usage:**
```bash
python scripts/link-validation/link-report-generator.py
```

**Key Dependencies:** collections, urllib.parse, csv, argparse
**File Size:** 17,609 bytes | Lines: 434

---

### link-validator.py

**Location:** `scripts/link-validation/link-validator.py`
**Purpose:** Link Validator using Playwright
**Version:** 1.0.0

**Description:**
Primary link validation tool using Playwright for JavaScript-rendered page validation.

**Usage:**
```bash
python scripts/link-validation/link-validator.py
```

**Key Dependencies:** aiohttp, asyncio, ssl, certifi
**File Size:** 17,967 bytes | Lines: 544

---

### simple-validator.py

**Location:** `scripts/link-validation/simple-validator.py`
**Purpose:** Simple Link Validator
**Version:** 1.0.0

**Description:**
Lightweight link validation tool for quick checks without browser automation.

**Usage:**
```bash
python scripts/link-validation/simple-validator.py
```

**Key Dependencies:** aiohttp, asyncio, urllib.parse, argparse
**File Size:** 6,741 bytes | Lines: 211

---

### specialized-validators.py

**Location:** `scripts/link-validation/specialized-validators.py`
**Purpose:** Specialized Link Validators
**Version:** 1.0.0

**Description:**
Domain-specific validators for GitHub, arXiv, DOI links, and other special link types.

**Usage:**
```bash
python scripts/link-validation/specialized-validators.py
```

**Key Dependencies:** aiohttp, asyncio, packaging, urllib.parse, dataclasses
**File Size:** 18,074 bytes | Lines: 490

---

### wayback-archiver.py

**Location:** `scripts/link-validation/wayback-archiver.py`
**Purpose:** Wayback Machine Archiver
**Version:** 1.0.0

**Description:**
Archives important links to Wayback Machine and retrieves archived versions of broken links.

**Usage:**
```bash
python scripts/link-validation/wayback-archiver.py
```

**Key Dependencies:** aiohttp, asyncio, dataclasses, argparse
**File Size:** 16,420 bytes | Lines: 460

---

### test-citation-workflow.sh

**Location:** `scripts/link-validation/test-citation-workflow.sh`
**Purpose:** Test script for citation validation workflow

**Description:**
Simulates what the GitHub Action will run for citation validation testing.

**Usage:**
```bash
bash scripts/link-validation/test-citation-workflow.sh
```

**File Size:** 2,560 bytes | Lines: 85

---

## Validation & Monitoring

Scripts for build monitoring, metadata validation, and syntax checking.

### build-monitor.py

**Location:** `scripts/validation/build-monitor.py`
**Purpose:** Continuous build monitoring and health checks
**Version:** 1.0.0

**Description:**
Real-time build monitoring system that tracks build performance, detects errors, and provides health metrics. Integrates with CI/CD pipelines through JSON output and supports continuous monitoring with alerting capabilities.

**Usage:**
```bash
# Monitor build once
python scripts/validation/build-monitor.py

# Continuous monitoring mode
python scripts/validation/build-monitor.py --continuous --interval 60

# Generate JSON report for CI/CD
python scripts/validation/build-monitor.py --format json --output build-report.json
```

**Key Dependencies:** subprocess, datetime, pathlib
**Related Scripts:** continuous-monitor.sh, metadata-validator.py
**File Size:** 13,721 bytes | Lines: 365

---

### metadata-validator.py

**Location:** `scripts/validation/metadata-validator.py`
**Purpose:** Validate blog post metadata and frontmatter
**Version:** 1.0.0

**Description:**
Comprehensive frontmatter validation ensuring all blog posts meet metadata requirements. Validates required fields, date formats, tag consistency, and schema compliance. Generates detailed validation reports with fix suggestions.

**Usage:**
```bash
# Validate all posts
python scripts/validation/metadata-validator.py

# Validate specific post
python scripts/validation/metadata-validator.py --post src/posts/2025-01-15-example.md

# Strict mode with schema validation
python scripts/validation/metadata-validator.py --strict --schema
```

**Key Dependencies:** yaml, frontmatter, datetime
**Related Scripts:** build-monitor.py
**File Size:** 12,188 bytes | Lines: 314

---

### continuous-monitor.sh

**Location:** `scripts/validation/continuous-monitor.sh`
**Purpose:** Wrapper for continuous build monitoring
**Version:** 1.0.0

**Description:**
Shell wrapper script for daemonizing build-monitor.py. Provides process management, log rotation, and system integration for continuous monitoring deployments.

**Usage:**
```bash
# Start monitoring daemon
bash scripts/validation/continuous-monitor.sh start

# Stop monitoring daemon
bash scripts/validation/continuous-monitor.sh stop

# Check monitoring status
bash scripts/validation/continuous-monitor.sh status
```

**Key Dependencies:** bash, build-monitor.py
**Related Scripts:** build-monitor.py
**File Size:** 1,931 bytes | Lines: 58

---

### validate-mermaid-syntax.py

**Location:** `scripts/blog-content/validate-mermaid-syntax.py`
**Purpose:** Validate Mermaid diagram syntax across all blog posts
**Version:** 1.0.0

**Description:**
Pattern-based syntax validation for Mermaid diagrams. Detects common errors including subgraph syntax, quote mismatches, arrow syntax, and bracket errors. Part of the validation infrastructure to ensure diagram quality.

**Usage:**
```bash
# Validate all blog posts
python scripts/blog-content/validate-mermaid-syntax.py

# Detailed validation report
python scripts/blog-content/validate-mermaid-syntax.py --verbose --format markdown
```

**Key Dependencies:** re, pathlib, collections
**Related Scripts:** fix-mermaid-subgraphs.py (in Blog Content Management)
**File Size:** 6,342 bytes | Lines: 184

---

## Utilities

General-purpose utility scripts for blog maintenance and analysis.

### analyze-post.py

**Location:** `scripts/utilities/analyze-post.py`
**Purpose:** Quick post analyzer - counts citations, weak language, and bullets

**Description:**
Lightweight analysis tool for quick post quality checks.

**Usage:**
```bash
python scripts/utilities/analyze-post.py <markdown-file>
```

**Key Dependencies:** pathlib
**File Size:** 3,021 bytes | Lines: 96

---

### batch-analyzer.py

**Location:** `scripts/utilities/batch-analyzer.py`
**Purpose:** Batch analyzer - Scans all posts and ranks them for refactoring priority

**Description:**
Analyzes all posts and prioritizes which ones need refactoring based on quality metrics.

**Usage:**
```bash
python scripts/utilities/batch-analyzer.py
```

**Key Dependencies:** dataclasses
**File Size:** 3,859 bytes | Lines: 121

---

### blog-compliance-analyzer.py

**Location:** `scripts/utilities/blog-compliance-analyzer.py`
**Purpose:** Blog Compliance Analyzer - CLAUDE.md Standards

**Description:**
Analyzes all blog posts for compliance with new content standards including Smart Brevity, Polite Linus Tone, and AI Skepticism.

**Usage:**
```bash
python scripts/utilities/blog-compliance-analyzer.py
```

**Key Dependencies:** collections
**File Size:** 18,630 bytes | Lines: 452

---

### diagram-manager.py

**Location:** `scripts/utilities/diagram-manager.py`
**Purpose:** Unified diagram and technical image management for blog posts
**Version:** 2.0.0

**Description:**
Comprehensive diagram management tool for creating, integrating, and managing technical diagrams. Consolidates functionality from multiple diagram scripts with commands for create, integrate, update, validate, and optimize.

**Usage:**
```bash
# Create diagrams for a specific post
python scripts/utilities/diagram-manager.py create --post="2024-03-15-claude-flow"

# Integrate diagrams into all posts
python scripts/utilities/diagram-manager.py integrate --all

# Validate diagram references
python scripts/utilities/diagram-manager.py validate --all

# Optimize all diagram files
python scripts/utilities/diagram-manager.py optimize --force
```

**Key Dependencies:** subprocess, lib.common, argparse
**Related Scripts:** generate-blog-hero-images.py, optimize-blog-content.py
**File Size:** 17,534 bytes | Lines: 482

---

### final-validation.py

**Location:** `scripts/utilities/final-validation.py`
**Purpose:** Final validation of live site after deployment
**Version:** 1.0.0

**Description:**
Post-deployment validation tool for verifying live site functionality and content integrity.

**Usage:**
```bash
python scripts/utilities/final-validation.py
```

**Key Dependencies:** playwright.async_api, asyncio
**File Size:** 4,090 bytes | Lines: 111

---

### llm-script-documenter.py

**Location:** `scripts/utilities/llm-script-documenter.py`
**Purpose:** Automatically add LLM-friendly documentation headers to all Python scripts
**Version:** 1.0.0

**Description:**
Scans all Python scripts and adds or updates LLM-friendly documentation headers. Categorizes scripts based on purpose and updates MANIFEST.json with complete script documentation.

**Usage:**
```bash
# Document all scripts and update manifest
python scripts/utilities/llm-script-documenter.py --update-manifest

# Preview changes
python scripts/utilities/llm-script-documenter.py --dry-run
```

**Key Dependencies:** lib.common, argparse
**Related Scripts:** common.py
**File Size:** 11,678 bytes | Lines: 355

---

### remove-corporate-speak.py

**Location:** `scripts/utilities/remove-corporate-speak.py`
**Purpose:** Corporate Speak Removal Script

**Description:**
Systematically removes corporate buzzwords from blog posts while preserving code blocks.

**Usage:**
```bash
python scripts/utilities/remove-corporate-speak.py
```

**File Size:** 8,732 bytes | Lines: 253

---

### count-bullets.sh

**Location:** `scripts/utilities/count-bullets.sh`
**Purpose:** Counts bullet points and numbered lists in blog posts

**Description:**
Shell utility for counting bullet points and numbered lists across blog posts.

**Usage:**
```bash
./scripts/utilities/count-bullets.sh [file.md]
```

**File Size:** 6,125 bytes | Lines: 183

---

## Maintenance

Scheduled maintenance and monitoring scripts.

### monthly-portfolio-validation.sh

**Location:** `scripts/maintenance/monthly-portfolio-validation.sh`
**Purpose:** Monthly Portfolio Validation Script
**Version:** 1.0.0

**Description:**
Automated monthly health checks with comprehensive reporting. Scheduled to run on the first of every month at 2 AM via cron.

**Usage:**
```bash
bash scripts/maintenance/monthly-portfolio-validation.sh
```

**File Size:** 11,538 bytes | Lines: 323

---

## Library

Shared utility libraries used across multiple scripts.

### common.py

**Location:** `scripts/lib/common.py`
**Purpose:** Shared utilities for all scripts - DRY/SOLID implementation
**Version:** 1.0.0

**Description:**
Core utility library implementing SOLID principles. Provides shared functionality for file operations, frontmatter parsing, validation, and common patterns used across all scripts. All scripts should import from this module instead of duplicating common code.

**SOLID Principles:**
- S - Single Responsibility: Each class has one clear purpose
- O - Open/Closed: Classes are open for extension, closed for modification
- L - Liskov Substitution: Derived classes can substitute base classes
- I - Interface Segregation: Specific interfaces over general ones
- D - Dependency Inversion: Depend on abstractions, not concretions

**Key Dependencies:** yaml, logging, subprocess, abc
**File Size:** 18,186 bytes | Lines: 579

---

### memory-file.sh

**Location:** `scripts/lib/memory-file.sh`
**Purpose:** Create a review context file

**Description:**
Shell utility for creating context files for code review workflows.

**Usage:**
```bash
source scripts/lib/memory-file.sh
```

**File Size:** 1,183 bytes | Lines: 49

---

## Root Scripts

Core scripts at the repository root level.

### optimize-blog-images.sh

**Location:** `scripts/optimize-blog-images.sh`
**Purpose:** Blog Image Optimization Script

**Description:**
Optimizes images and creates responsive variants for all blog post images to improve site performance.

**Usage:**
```bash
bash scripts/optimize-blog-images.sh
```

**File Size:** 4,874 bytes | Lines: 161

---

### stats-generator.py

**Location:** `scripts/stats-generator.py`
**Purpose:** Blog Statistics Generator
**Author:** William Zujkowski
**Created:** 2025-10-20

**Description:**
Parses all markdown blog posts and generates comprehensive statistics for display on the blog. Outputs to src/_data/blogStats.json.

**Usage:**
```bash
python scripts/stats-generator.py
```

**Key Dependencies:** yaml, urllib.parse, collections, math
**File Size:** 20,409 bytes | Lines: 579

---

## Quick Reference

### By File Size (Top 10)

1. humanization-validator.py - 48,302 bytes
2. citation-repair.py - 21,803 bytes
3. stats-generator.py - 20,409 bytes
4. full-post-validation.py - 20,024 bytes
5. citation-updater.py - 19,225 bytes
6. batch-improve-blog-posts.py - 19,171 bytes
7. blog-compliance-analyzer.py - 18,630 bytes
8. content-relevance-checker.py - 18,347 bytes
9. common.py - 18,186 bytes
10. link-monitor.py - 18,054 bytes

### Newest Scripts (Added 2025-11-02)

1. **build-monitor.py** - 13,721 bytes | 365 lines - Build health monitoring
2. **metadata-validator.py** - 12,188 bytes | 314 lines - Frontmatter validation
3. **validate-mermaid-syntax.py** - 6,342 bytes | 184 lines - Mermaid syntax checking
4. **fix-mermaid-subgraphs.py** - 5,054 bytes | 166 lines - Mermaid syntax repair
5. **continuous-monitor.sh** - 1,931 bytes | 58 lines - Monitoring daemon wrapper
6. **test-mermaid-rendering.html** - 3KB | Test harness - Browser-based validation

### Most Complex (Lines of Code)

1. humanization-validator.py - 1,157 lines
2. batch-improve-blog-posts.py - 612 lines
3. citation-repair.py - 597 lines
4. stats-generator.py - 579 lines
5. common.py - 579 lines
6. build-monitor.py - 365 lines (NEW)
7. metadata-validator.py - 314 lines (NEW)

### Key Integration Points

**Content Pipeline:**
```
write post → humanization-validator.py → research-validator.py →
full-post-validation.py → link-validator.py → deploy
```

**Image Pipeline:**
```
create post → update-blog-images.py → generate-blog-hero-images.py →
optimize-blog-images.sh → deploy
```

**Citation Pipeline:**
```
identify claims → academic-search.py → add-academic-citations.py →
check-citation-hyperlinks.py → citation-repair.py
```

**Validation Pipeline (NEW):**
```
pre-commit → metadata-validator.py → validate-mermaid-syntax.py →
build-monitor.py → continuous-monitor.sh (production)
```

---

**Maintenance Notes:**

- Run `python scripts/utilities/llm-script-documenter.py --update-manifest` after adding new scripts
- All scripts should import from `scripts/lib/common.py` for shared functionality
- Follow SOLID principles when extending script capabilities
- Update this catalog when adding/removing/modifying scripts
- Version numbers follow semantic versioning (MAJOR.MINOR.PATCH)

---

**Change Log:**

- **2025-11-02:** Added 6 new scripts (2 Mermaid, 3 validation, 1 test harness). New "Validation & Monitoring" category. Total: 56 scripts across 9 categories.
- **2025-10-29:** Initial catalog with 50 scripts across 8 categories.

---

*This catalog is automatically maintained. Do not edit manually - regenerate using script-metadata.json.*
