---
title: Directory Structure & Organization
category: reference
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1000
load_when:
  - Understanding repository layout
  - Finding specific directories
  - Organizing new files
dependencies: []
tags: [structure, directories, organization, reference]
---

# Directory Structure & Organization

## Module Metadata
- **Category:** reference
- **Priority:** LOW
- **Load frequency:** As needed for repository navigation and file organization tasks
- **Dependencies:** None

## Purpose

This module provides comprehensive reference documentation for the repository's directory structure, key directories, configuration files, and documentation retention policies. Essential for understanding where files belong and how the project is organized.

## When to Load This Module

- Understanding repository layout
- Finding specific directories or files
- Organizing new files or scripts
- Archive/retention decisions
- Setting up development environment

---

## Project Directory Structure

### Root Directory

```
williamzujkowski.github.io/
├── src/                    # Source files for the static site
│   ├── _data/             # Global data files for Eleventy
│   ├── _includes/         # Reusable templates and layouts
│   │   ├── layouts/       # Page layout templates
│   │   └── partials/      # Reusable component templates
│   ├── assets/            # Static assets
│   │   ├── css/          # Stylesheets (Tailwind)
│   │   ├── images/       # Site images
│   │   │   └── blog/     # Blog post images
│   │   ├── js/           # JavaScript files
│   │   └── fonts/        # Custom fonts
│   ├── pages/            # Static pages (about, contact, etc.)
│   ├── posts/            # Blog posts in Markdown
│   ├── redirects/        # URL redirect configurations
│   └── index.njk         # Homepage template
├── scripts/              # Utility and automation scripts
│   ├── blog-content/    # Content management (6 scripts)
│   ├── blog-images/     # Image management (6 scripts)
│   ├── blog-research/   # Citations & research (7 scripts)
│   ├── link-validation/ # Link validation (12 scripts)
│   ├── lib/             # Shared libraries
│   └── utilities/       # General utilities (3 scripts)
├── docs/                 # Documentation
│   ├── context/         # Modular context system
│   ├── guides/          # Development guides
│   ├── standards/       # Coding standards
│   └── archive/         # Historical documentation
├── _site/               # Built static site (git-ignored)
├── node_modules/        # npm dependencies (git-ignored)
├── .eleventy.js        # Eleventy configuration
├── package.json        # npm configuration
├── tailwind.config.js  # Tailwind CSS configuration
├── postcss.config.js   # PostCSS configuration
├── CLAUDE.md           # Root anchor documentation
└── MANIFEST.json       # Repository inventory
```

**Total Active Scripts**: 35 Python scripts + 2 Shell scripts

---

## Key Directories Explained

### `/src` - Source Directory
- **Purpose:** Contains all source files for the Eleventy static site generator
- **Key Files:**
  - `index.njk`: Homepage template
  - `404.md`: 404 error page
  - `feed.njk`: RSS feed template
  - `sitemap.njk`: XML sitemap template
  - `tags.njk`: Tag listing page template

### `/scripts` - Automation Scripts
- **Purpose:** Organized Python and shell scripts for blog management
- **Structure:** Scripts organized into logical categories:
  - `blog-content/` - Content management & optimization (6 scripts)
  - `blog-images/` - Image generation & management (6 scripts)
  - `blog-research/` - Academic citations & research (7 scripts)
  - `link-validation/` - Link validation & repair (12 scripts)
  - `lib/` - Shared libraries (common.py, memory-file.sh)
  - `utilities/` - General utilities (3 scripts)

### `/docs` - Documentation
- **Purpose:** Project documentation and guides
- **Structure:**
  - `context/` - Modular context system (21 modules across 6 categories)
  - `guides/` - Development guides
  - `standards/` - Coding standards
  - `archive/` - Historical documentation by quarter

### `/_site` - Build Output
- **Purpose:** Generated static site files
- **Note:** Git-ignored, regenerated on build

---

## Configuration Files

| File | Purpose |
|------|---------|
| `.eleventy.js` | Eleventy configuration, plugins, filters |
| `package.json` | npm scripts, dependencies |
| `tailwind.config.js` | Tailwind CSS customization |
| `postcss.config.js` | PostCSS plugins configuration |
| `.gitignore` | Git ignore patterns |
| `MANIFEST.json` | Repository inventory and metadata |
| `CLAUDE.md` | Root anchor documentation (7,372 tokens) |
| `.claude-rules.json` | Enforcement rules |

---

## Documentation Retention Policy

### Active Documentation (0-30 days)
**Location:** Root `/reports` or `/docs`

**Keep:**
- Current phase work
- Recent completion reports
- Actively referenced methodology documents

### Archive (30-180 days)
**Location:** `/docs/archive/YYYY-QX/`

**Move:**
- Completed batch reports (Batch 1-6)
- Phase completion reports (Phase 8.4, 8.5, etc.)
- Historical test reports

**Archive Locations:**
- **Q3 2025**: `docs/archive/2025-Q3/` (Batches 1-6, Smart Brevity transformation)
- **Q4 2025**: `docs/archive/2025-Q4/` (Phase 8 code reduction, security refinements)

### Purge (180+ days)
**Action:** Delete

**Remove:**
- Non-reference documentation
- Superseded plans and intermediate reports
- Redundant status updates

### Never Delete
**Permanent retention:**
- `LESSONS_LEARNED.md` files (all batches)
- Final completion reports (latest per phase)
- Methodology documentation (`CLAUDE_MD_UPDATES.md`, `UNIFIED_HUMANIZATION_METHODOLOGY.md`)
- Validation tools and pattern definitions
- Architecture and enforcement guides

---

## File Organization Rules

**Never save to root.** Use these directories:

```
/src         → Source code
/tests       → Test files
/docs        → Documentation
/scripts     → Automation utilities
/config      → Configuration files
```

### Common Mistakes

❌ **Bad:**
- `validate-claims.py` in root
- `test-citations.md` in root
- `working-notes.txt` anywhere

✅ **Good:**
- `scripts/blog-research/validate-claims.py`
- `tests/test-citations.py`
- `docs/working-notes.md`

---

## Build Commands Reference

```bash
# Development
npm run serve           # Start dev server with hot reload
npm run watch:css       # Watch and rebuild CSS on changes
npm run watch:eleventy  # Watch and rebuild Eleventy on changes

# Production
npm run build           # Build production site (CSS + Eleventy + JS)
npm run build:css       # Build CSS only with PostCSS
npm run build:eleventy  # Build Eleventy only
npm run build:js        # Bundle JavaScript files

# Testing
npm run test            # Run unit tests
npm run test:unit       # Run unit tests only
npm run test:integration # Run integration tests
npm run test:e2e        # Run end-to-end tests
npm run test:all        # Run all tests
npm run test:watch      # Run tests in watch mode

# Validation
npm run validate:km     # Validate knowledge management standards

# Debugging
npm run debug           # Run Eleventy with debug output
```

---

## Cross-References

**Related modules:**
- `core/file-management` - File organization and cleanup rules
- `core/enforcement` - Pre-commit hook validation
- `core/standards-integration` - MANIFEST.json management

**External documentation:**
- [docs/ARCHITECTURE.md](../../ARCHITECTURE.md) - System architecture
- [docs/GUIDES/SCRIPT_CATALOG.md](../../GUIDES/SCRIPT_CATALOG.md) - Complete script catalog
- [MANIFEST.json](../../../MANIFEST.json) - Repository inventory

---

## Quick Reference Commands

```bash
# Find file location
find . -name "filename" -not -path "./node_modules/*" -not -path "./_site/*"

# List scripts by category
ls -la scripts/blog-content/
ls -la scripts/blog-images/
ls -la scripts/blog-research/

# Check directory sizes
du -sh src/ docs/ scripts/

# Count total files
find src/posts -name "*.md" | wc -l
```

---

## Changelog
- 2025-11-01: Initial module creation from CLAUDE.md v3.0.0 backup
