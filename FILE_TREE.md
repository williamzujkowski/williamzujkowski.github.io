# Repository File Structure

This document provides a hierarchical representation of the project's file structure to help navigate the codebase. It is maintained to ensure AI agents can efficiently understand the repository organization.

## Root Directory

- **BLOG-POST-README.md** - Instructions for blog post creation and formatting
- **BLOG-WORKFLOW.md** - Workflow guide for blog content management
- **CHANGELOG.md** - History of changes to the project
- **CLAUDE.md** - Consolidated guidance for Claude AI when working with this codebase
- **COMPLETION-SUMMARY.md** - Summary of completed optimization work
- **CONTRIBUTING.md** - Guidelines for contributing to the project
- **FILE_TREE.md** - This file, providing a structured overview of the repository
- **LICENSE** - Project license information
- **MAINTENANCE.md** - Instructions for maintaining the project
- **README.md** - Project overview and main documentation
- **README-VULN-BLOG-MIGRATION.md** - Guide for vulnerability blog post migration
- **SIMPLIFICATION-PROGRESS.md** - Tracks progress of codebase simplification efforts
- **SIMPLIFICATION-SUCCESS.md** - Confirmation of successful simplification
- **UPDATES.md** - History of recent updates to the project
- **site.webmanifest** - Web app manifest file for PWA support

### `/.llmconfig` - LLM Configuration Directory

- **CLAUDE.md** - Primary configuration file for Claude AI
- **agent-rules.md** - Coding standards and best practices for LLM agents
- **loaders.js** - Utility functions for loading LLM configurations
- **prompt-templates/** - Reusable prompt templates
  - **index.js** - Exports template functions for code generation, refactoring, and bug fixes
- **context/** - Context information for LLM agents
  - **context-types.js** - Type definitions for context objects
- **examples/** - Example interactions for few-shot learning
  - **index.js** - Example responses for various types of requests
- **system-prompts/** - System-level instructions for different AI agents
  - **index.js** - System prompts for different agent roles

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
    - **`code-highlight.js`** - Code syntax highlighting
    - **`joke-generator.js`** - Joke generator component
    - **`search.js`** - Search functionality
    - **`static-fallbacks.js`** - Static fallback components
    - **`theme-toggle.js`** - Theme toggle component
  - **`utils/`** - JavaScript utilities
    - **`analytics.js`** - Analytics integration
    - **`dom.js`** - DOM manipulation utilities
    - **`resource-hints.js`** - Resource hints utilities
    - **`site-config.js`** - Site configuration utilities
    - **`storage.js`** - Storage utilities
    - **`theme-init.js`** - Theme initialization
  - **`blog-search.js`** - Blog search functionality
  - **`heatmap.js`** - GitHub-style contribution heatmap
  - **`main.js`** - Main JavaScript entry point
  - **`resource-hints.js`** - Resource hints implementation
  - **`search.js`** - General search functionality
  - **`site-enhancements.js`** - Site enhancement utilities
  - **`test-utility.js`** - Testing utilities
  - **`theme-switcher.js`** - Theme switching functionality
  - **`theme-utils.js`** - Theme utility functions
  - **`url-validator.js`** - URL validation utilities

- **`posts/`** - Blog post content
  - **`backup/`** - Backup copies of blog posts
  - **`debug/`** - Posts used for debugging
  - **`drafts/`** - Draft blog posts not yet published

### `/scripts` - Utility Scripts

- **`README.md`** - Documentation for scripts
- **`bin/`** - Shell scripts and executables
- **`build/`** - Core build process scripts
  - **`create-core-data.js`** - Core data generation script
- **`content/`** - Content management and processing
  - **`posts/`** - Blog post processing utilities
- **`convert-image-tags.js`** - Tool for converting image tags
- **`dashboard/`** - Dashboard generation and management
  - **`ensure-dashboard-data.js`** - Dashboard data verification
- **`data/`** - Data processing scripts
  - **`create-fallback-data.js`** - Fallback data creation
  - **`create-fallback-link-previews.js`** - Link previews fallback
  - **`data-compression.js`** - Data compression utilities
  - **`incremental-data-converter.js`** - Incremental data updates
  - **`optimize-data-management.js`** - Data optimization
  - **`smart-data-loader.js`** - Smart data loading utilities
- **`fix-feed.js`** - RSS feed fixup script
- **`link-previews/`** - Link preview generation tools
  - **`link-preview-generator.js`** - Tool for generating link previews
- **`media/`** - Media optimization and processing
  - **`images/`** - Image optimization utilities
    - **`image-shortcode.js`** - Image shortcode implementation
    - **`optimize-images.js`** - Image optimization tools
  - **`optimize-images.js`** - Main image optimization script
- **`rebuild-link-previews.sh`** - Shell script for rebuilding link previews
- **`standardize-frontmatter.js`** - Markdown frontmatter standardization
- **`styling/`** - CSS optimization scripts
  - **`backup-old-css.js`** - CSS backup script
  - **`enhanced-optimize-css.js`** - Enhanced CSS optimization
  - **`extract-components.js`** - CSS component extraction
  - **`generate-theme.js`** - Theme generation script
- **`testing/`** - Test execution scripts
  - **`run-accessibility-tests.js`** - Accessibility testing
  - **`run-component-tests.js`** - Component tests
  - **`run-tests.js`** - Main test runner
  - **`verify-build.js`** - Build verification
  - **`verify-templates.js`** - Template verification
- **`utils/`** - Utility functions
- **`validation/`** - Configuration validation tools
  - **`validate-config.js`** - Configuration validator
- **`verify-scripts.js`** - Script verification utility
- **`wrapper/`** - Wrapper scripts for external tools
  - **`generate-blog-post-wrapper.js`** - Blog post generation wrapper
  - **`generate-vuln-post-wrapper.js`** - Vulnerability post generation wrapper

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
  - **`site.webmanifest`** - Backup of web app manifest

## Other Important Files

- **`index.njk`** - Main site homepage template
- **`blog.njk`** - Blog listing page template
- **`vulnerability-analysis.njk`** - Vulnerability analysis page template
- **`feed.njk`** - RSS feed template
- **`service-worker.js`** - Service worker for offline capabilities

---

_Note: This FILE_TREE.md should be updated whenever the repository structure changes to ensure AI agents can effectively navigate the codebase._
