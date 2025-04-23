# Repository File Structure

This document provides a hierarchical representation of the project's file structure to help navigate the codebase. It is maintained to ensure AI agents can efficiently understand the repository organization.

## Root Directory

- **BLOG-POST-README.md** - Instructions for blog post creation and formatting
- **BLOG-WORKFLOW.md** - Workflow guide for blog content management
- **BACKUP/** - Backup directory for previous versions of files
- **CHANGELOG.md** - History of changes to the project
- **CLAUDE.md** - Consolidated guidance for Claude AI when working with this codebase
- **CONTRIBUTING.md** - Guidelines for contributing to the project
- **FILE_TREE.md** - This file, providing a structured overview of the repository
- **LICENSE** - Project license information
- **MAINTENANCE.md** - Instructions for maintaining the project
- **README.md** - Project overview and main documentation
- **README-VULN-BLOG-MIGRATION.md** - Guide for vulnerability blog post migration
- **UPDATES.md** - History of recent updates to the project

## Key Directories

### `/src` - Main Source Code

- **`_data/`** - Data files for the website

  - **`config/`** - Configuration files for different site components
    - **`blog.json`, `homepage.json`, etc.** - Specific component configurations
  - **`core/`** - Core data files (arxiv-feed, books, contribution-heatmap, etc.)
  - **`templates/`** - Blog post templates by category

- **`_includes/`** - Reusable template components

  - **`layouts/`** - Base layouts for different page types
  - **`macros/`** - Reusable template functions/components
  - **`partials/`** - Partial templates like header, footer, etc.

- **`_layouts/`** - Page layout templates (base, post)

- **`css/`** - Stylesheet files

  - **`base/`** - Base styles (layout, reset, typography)
  - **`components/`** - Component-specific styles
  - **`optimized/`** - Optimized CSS for production
  - **`utils/`** - CSS utility classes

- **`js/`** - JavaScript files

  - **`components/`** - UI component scripts
  - **`data/`** - Data handling scripts
  - **`utils/`** - JavaScript utilities

- **`posts/`** - Blog post content
  - **`backup/`** - Backup copies of blog posts
  - **`debug/`** - Posts used for debugging
  - **`drafts/`** - Draft blog posts not yet published

### `/scripts` - Utility Scripts

- **`bin/`** - Shell scripts and executables
- **`build/`** - Core build process scripts
- **`content/`** - Content management and processing
  - **`posts/`** - Blog post processing utilities
- **`dashboard/`** - Dashboard generation and management
- **`data/`** - Data processing scripts
- **`link-previews/`** - Link preview generation tools
- **`media/`** - Media optimization and processing
  - **`images/`** - Image optimization utilities
- **`styling/`** - CSS optimization scripts
- **`testing/`** - Test execution scripts
- **`utils/`** - Utility functions
- **`validation/`** - Configuration validation tools
- **`wrapper/`** - Wrapper scripts for external tools

### `/assets` - Static Assets

- **`data/`** - JSON data files
- **`icons/`** - Site icons and favicon files
- **`images/`** - Image files
  - **`blog/`** - Blog post images
  - **`github-style/`** - GitHub-style UI elements
  - **`links/`** - Icons for external links

### `/tests` - Test Files

- **`accessibility/`** - Accessibility test suites
- **`e2e/`** - End-to-end tests
- **`integration/`** - Integration tests
- **`performance/`** - Performance tests
- **`security/`** - Security test cases
- **`unit/`** - Unit tests
- **`visual/`** - Visual regression tests

### `/tools` - Special Tools

- **`vuln-blog/`** - Vulnerability and general blog post generation tool
  - **`prompts/`** - Prompts for LLM-based blog generation
    - **`templates/`** - General blog post templates
    - **`guidelines/`** - Style and content guidelines
  - **`src/`** - Source code for the blog generator
  - **`workflows/`** - GitHub workflow definitions

### `/docs` - Documentation

- **`development/`** - Development-focused documentation
- **`guides/`** - User and contributor guides
- **`reference/`** - Reference documentation

### `/_data` - Eleventy Data Files

- Data files for site generation with Eleventy

## Configuration Files

- **`package.json`** - NPM package definition and scripts
- **`rollup.config.js`** - Rollup.js configuration
- **`playwright.config.js`** - Playwright test configuration
- **`.eleventy.cjs`** - Eleventy configuration
- **`config/`** - Configuration files
  - **`postcss.config.cjs`** - PostCSS configuration
  - **`tailwind.config.cjs`** - Tailwind CSS configuration
  - **`site.webmanifest`** - Web app manifest

## Other Important Files

- **`index.njk`** - Main site homepage template
- **`blog.njk`** - Blog listing page template
- **`vulnerability-analysis.njk`** - Vulnerability analysis page template
- **`feed.njk`** - RSS feed template
- **`service-worker.js`** - Service worker for offline capabilities

---

_Note: This FILE_TREE.md should be updated whenever the repository structure changes to ensure AI agents can effectively navigate the codebase._
