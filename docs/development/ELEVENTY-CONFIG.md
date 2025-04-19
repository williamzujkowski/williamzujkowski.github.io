# Eleventy Configuration Guide

This document explains the Eleventy configuration files in the project and when to use each one.

## Configuration Files

The project uses two main Eleventy configuration files:

1. **`.eleventy.cjs`**: The primary configuration file used for local development and production builds. This is a comprehensive configuration with:

   - Advanced image processing with metadata support
   - Full data loading from the unified data directory (`src/_data/core`)
   - Complete set of filters and shortcodes
   - Detailed logging and debugging

2. **`.eleventy.simple.cjs`**: A simplified configuration mainly used for GitHub Actions CI/CD builds. This configuration:
   - Uses simpler image handling without metadata processing
   - Contains hardcoded fallback data for blog images
   - Provides basic filters and shortcodes
   - Is optimized for faster builds in CI/CD environments

## Configuration File Usage

- **Local Development**: Use `.eleventy.cjs` via `npm run dev` or `npm run serve`
- **Production Build**: Use `.eleventy.cjs` via `npm run build` or `npm run build:prod`
- **CI/CD Builds**: Use `.eleventy.simple.cjs` for faster builds in GitHub Actions

## Configuration Copies

For backup and reference purposes, copies of these configurations are also stored in:

- `/config/.eleventy.cjs`
- `/config/.eleventy.simple.cjs`

These backup copies should be kept in sync with the main versions but are not directly used by the build process.

## When To Modify

When making changes to the Eleventy configuration:

1. First, determine if the change is needed for both configurations or only the primary one
2. For changes affecting core functionality, update both `.eleventy.cjs` and `.eleventy.simple.cjs`
3. For advanced features that aren't critical for CI builds, only update `.eleventy.cjs`
4. After testing, consider updating the backup copies in the `/config/` directory

## Key Configuration Areas

The main configuration areas include:

- **Collections**: Custom collection definitions, particularly the `posts` collection
- **Filters**: Data transformation functions used in templates
- **Shortcodes**: Reusable components like `image` and `breadcrumbs`
- **Data Loading**: Methods for accessing site data
- **Asset Handling**: Configuration for handling static assets
