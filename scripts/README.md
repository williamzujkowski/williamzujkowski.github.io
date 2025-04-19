# Scripts Directory

This directory contains utility scripts for building, optimizing, and managing the website.

## Directory Structure

- **bin/**: Shell scripts and executables
- **blog/**: Blog post processing utilities
- **build/**: Core build process scripts
- **data/**: Data processing and optimization
- **link-previews/**: Link preview generation
- **media/**: Image and media optimization
- **styling/**: CSS optimization and theme generation
- **testing/**: Test automation
- **validation/**: Validation tools
- **archive/**: Deprecated scripts (kept for reference)

## Core Scripts

### Build Process

- `build/optimized-build.js`: Comprehensive build process with optimizations
- `build/create-core-data.js`: Generates core site data
- `build/verify-build-config.js`: Validates build configuration

### Content Management

- `blog/enhance-post-processor.js`: Enhanced blog post processing
- `link-previews/link-preview-generator.js`: Generates link previews
- `media/optimize-images.js`: Optimizes images

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
