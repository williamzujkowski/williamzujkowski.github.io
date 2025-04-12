# Scripts Directory Structure

This document provides an overview of the scripts and tools organization in this project.

## Directory Structure

```
/scripts/                          # Main directory for all scripts and tools
  /build/                          # Build-time scripts for data generation
    build-arxiv-feed.js            # Generate arXiv feed data
    build-book-data.js             # Generate book data
    build-github-pins.js           # Generate GitHub pins data
    build-link-previews.js         # Generate link preview metadata
    build-visualizations.js        # Generate visualization data
    create-fallback-data.js        # Create fallback data files
    
  /content/                        # Content management tools
    /blog/                         # Blog post management
      process-new-posts.js         # Process new blog posts
      enhanced-post-processor.js   # Enhanced post processing
      fix-citations.js             # Fix citations in posts
      remove-header-images.js      # Remove header images from posts
      standardize-frontmatter.js   # Standardize frontmatter in posts
    
    /links/                        # Link management
      check-missing-previews.js    # Check for missing link previews
      force-update-link-previews.js # Force update links previews
    
  /screenshots/                    # Screenshot generation tools
    generate-screenshots.js        # Main screenshot generator
    index.js                       # Entry point that exports helper functions
    utils.js                       # Common utilities for screenshot generation
    screenshots.sh                 # Main CLI utility for screenshots
    verify-screenshots.html        # Test page for screenshots
    
  /validation/                     # Validation tools
    validate-config.js             # Validate site configuration
    validate-links.js              # Validate links
    
  /styling/                        # Styling tools
    optimize-css.js                # Optimize CSS
    extract-components.js          # Extract components from templates
    generate-theme.js              # Generate theme files
    
  /utils/                          # Utility scripts
    optimize-images.js             # Optimize images
    download-blog-images.js        # Download blog images
    
  /bin/                            # CLI utilities and entry points
    build.sh                       # Main build script
    dev.sh                         # Development utilities
    update-site.sh                 # Site update utilities
```

## Script Categories

### Build Scripts

Build scripts are responsible for generating data files needed by the site. These scripts typically run during the build process.

Key scripts:
- `build-arxiv-feed.js`: Generates arXiv feed data
- `build-book-data.js`: Generates book data
- `build-github-pins.js`: Generates GitHub pins data
- `build-link-previews.js`: Generates link preview metadata
- `build-visualizations.js`: Generates visualization data
- `create-fallback-data.js`: Creates fallback data files

### Content Management

These scripts manage blog posts and link data.

#### Blog Post Management

- `process-new-posts.js`: Processes new blog posts
- `enhanced-post-processor.js`: Enhanced post processing with features like citation formatting
- `fix-citations.js`: Fixes citations in posts
- `remove-header-images.js`: Removes header images from posts
- `standardize-frontmatter.js`: Standardizes frontmatter in posts

#### Link Management

- `check-missing-previews.js`: Checks for missing link previews
- `force-update-link-previews.js`: Forces update of link previews

### Screenshot Generation

Tools for generating screenshots of websites for the links page.

- `generate-screenshots.js`: Main screenshot generator
- `index.js`: Entry point that exports helper functions
- `utils.js`: Common utilities for screenshot generation
- `screenshots.sh`: Command-line interface for screenshot generation
- `verify-screenshots.html`: Test page to verify screenshots

### Validation

Tools for validating site configuration and links.

- `validate-config.js`: Validates site configuration
- `validate-links.js`: Validates links

### Styling

Tools for managing CSS and theme-related tasks.

- `optimize-css.js`: Optimizes CSS
- `extract-components.js`: Extracts components from templates
- `generate-theme.js`: Generates theme files

### Utilities

General utility scripts.

- `optimize-images.js`: Optimizes images
- `download-blog-images.js`: Downloads blog images

### CLI Utilities

Shell scripts for command-line operations.

- `build.sh`: Main build script
- `dev.sh`: Development utilities
- `update-site.sh`: Site update utilities

## NPM Scripts

The `package.json` file contains npm scripts that use these tools. For example:

- `npm run build`: Builds everything (data, site, CSS)
- `npm run build:data`: Builds just the data files
- `npm run process:posts`: Processes new blog posts
- `npm run screenshots`: Generates screenshots for the links page
- `npm run validate:all`: Validates configuration and links

See the `scripts` section in `package.json` for a complete list of available npm scripts.