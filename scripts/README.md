# Scripts Directory

This directory contains utility scripts for building, optimizing, and managing the website.

## Directory Structure

- **bin/**: Shell scripts and executables
- **build/**: Core build process scripts
- **content/**: Content management and processing
  - **posts/**: Blog post processing utilities
- **dashboard/**: Dashboard generation and management
- **data/**: Data processing and optimization
- **link-previews/**: Link preview generation
- **media/**: Media optimization and processing
  - **images/**: Image optimization utilities
- **styling/**: CSS optimization and theme generation
- **testing/**: Test automation
- **utils/**: Utility functions
- **validation/**: Validation tools
- **wrapper/**: Wrapper scripts for integrations

## Core Scripts

### Build Process

- `build/optimized-build.js`: Comprehensive build process with optimizations
- `build/create-core-data.js`: Generates core site data
- `build/verify-build-config.js`: Validates build configuration

### Content Management

- `content/posts/process-new-posts.js`: Processes new blog posts
- `content/posts/enhance-post-processor.js`: Enhanced blog post processing
- `content/posts/fix-citations.js`: Fixes citations in blog posts
- `content/posts/standardize-frontmatter.js`: Standardizes frontmatter in blog posts
- `link-previews/link-preview-generator.js`: Generates link previews
- `media/images/optimize-images.js`: Optimizes images
- `media/images/image-shortcode.js`: Image shortcode processor
- `wrapper/generate-blog-post-wrapper.js`: Wrapper for blog post generation
- `wrapper/generate-vuln-post-wrapper.js`: Wrapper for vulnerability post generation

### Styling

- `styling/enhanced-optimize-css.js`: Advanced CSS optimization
- `styling/generate-theme.js`: Theme generation

### Testing & Validation

- `testing/run-tests.js`: Runs automated tests
- `testing/verify-templates.js`: Validates templates
- `testing/verify-build.js`: Validates build output
- `validation/validate-config.js`: Validates configuration files

## Usage

Most scripts can be run via npm scripts defined in package.json. For direct execution:

```bash
node scripts/[category]/[script-name].js
```

## Maintenance

When adding new scripts:

1. Follow the established directory structure
2. Document purpose and usage in this README
3. Add appropriate npm scripts to package.json
4. Avoid creating duplicate functionality
