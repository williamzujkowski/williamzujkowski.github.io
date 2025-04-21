# Tool and Script Reorganization Plan

## New Directory Structure

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
    generate-screenshots.js        # Main screenshot generator (fast version)
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

## Migration Plan

1. Create all necessary directories
2. Move files to their new locations
3. Update imports/requires in JavaScript files
4. Update file references in shell scripts and package.json
5. Create consolidated script files where needed
6. Document the new structure in README.md
