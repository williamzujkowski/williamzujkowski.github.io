# Complexity Comparison: Current vs. Simplified Architecture

This document provides a visual comparison between the current complex architecture and the proposed simplified architecture, highlighting the key differences and benefits.

## Directory Structure

### Current Structure (Complex)
```
williamzujkowski.github.io/
├── _data/                       # Data files (duplicate 1)
├── _includes/                   # Includes (legacy)
├── _layouts/                    # Layouts (legacy)
├── _site/                       # Build output
├── assets/
│   ├── data/                    # Data files (duplicate 2)
│   ├── icons/                   # Icons
│   └── images/                  # Images
├── config/
│   ├── .eleventy.simple.cjs     # Eleventy config
│   ├── postcss.config.cjs       # PostCSS config
│   ├── site.webmanifest         # Manifest
│   └── tailwind.config.cjs      # Tailwind config
├── docs/                        # Documentation
├── new_posts/                   # New posts directory
│   └── processed/               # Processed posts
├── removed_posts/               # Removed posts
├── scripts/
│   ├── _data/                   # Data files (duplicate 3)
│   ├── build/                   # Build scripts
│   ├── content/                 # Content scripts
│   ├── screenshots/             # Screenshot scripts
│   ├── styling/                 # Style scripts
│   ├── utils/                   # Utility scripts
│   └── validation/              # Validation scripts
├── src/
│   ├── _data/                   # Source data
│   │   ├── config/              # Configuration data
│   │   └── site.js              # Site data
│   ├── _includes/               # Include templates
│   ├── _layouts/                # Layout templates
│   ├── css/                     # CSS files
│   │   ├── backup/              # CSS backups
│   │   ├── optimized/           # Optimized CSS
│   │   └── styles.css           # Main CSS
│   ├── js/                      # JavaScript files
│   └── posts/                   # Blog posts
│       ├── backup/              # Post backups
│       └── drafts/              # Post drafts
└── tools/                       # Additional tools
```

### Simplified Structure (Proposed)
```
williamzujkowski.github.io/
├── _site/                       # Build output
├── assets/
│   ├── icons/                   # Icons
│   └── images/                  # Images
├── scripts/
│   ├── build/                   # Core build scripts
│   ├── content/                 # Content scripts
│   └── utils/                   # Utility scripts
├── src/
│   ├── _data/                   # All data in one place
│   │   ├── core/                # Core data files
│   │   ├── config/              # Configuration
│   │   └── cache/               # Generated data
│   ├── _includes/               # Include templates
│   │   ├── layouts/             # Layout templates
│   │   ├── partials/            # Partial templates
│   │   └── macros/              # Template macros
│   ├── css/                     # CSS files
│   │   ├── base/                # Base styles
│   │   ├── components/          # Component styles
│   │   ├── utils/               # Utility styles
│   │   └── main.css             # Main CSS entry
│   ├── js/                      # JavaScript files
│   │   ├── components/          # JS components
│   │   ├── utils/               # JS utilities
│   │   └── main.js              # Main JS entry
│   ├── pages/                   # Site pages
│   └── posts/                   # Blog posts
├── .eleventy.js                 # Single Eleventy config
└── postcss.config.js            # Single PostCSS config
```

## Build Process

### Current Process (Complex)
```
npm run build
  ├── npm run build:data
  │   ├── node scripts/build/create-fallback-data.js
  │   ├── npm run build:arxiv
  │   ├── npm run build:viz
  │   ├── npm run build:books
  │   ├── npm run build:links (optional)
  │   └── npm run build:blog-images (optional)
  ├── eleventy --config=config/.eleventy.simple.cjs
  └── npm run build:css
      └── postcss src/css/styles.css -o _site/css/styles.css --config=config/postcss.config.cjs
```

### Simplified Process (Proposed)
```
npm run build
  ├── npm run build:data
  │   └── node scripts/build/create-core-data.js
  ├── eleventy --config=.eleventy.js
  └── npm run build:css
      └── postcss src/css/main.css -o _site/css/main.css
```

## Data Flow

### Current Flow (Complex)
```
scripts/build/build-*.js
  ├── Generate data
  ├── Write to _data/
  ├── Copy to assets/data/
  └── Copy to scripts/_data/ (sometimes)

templates
  ├── Read from _data/
  ├── Read from src/_data/
  ├── Process with scripts
  └── Generate HTML
```

### Simplified Flow (Proposed)
```
scripts/build/create-core-data.js
  └── Write to src/_data/core/

templates
  └── Read from src/_data/
      └── Generate HTML
```

## Template Structure

### Current Structure (Complex)
```
_includes/
  ├── header.njk
  ├── footer.njk
  └── ...

_layouts/
  ├── base.njk
  └── post.njk

src/_includes/
  ├── header.njk
  ├── footer.njk
  └── ...

src/_layouts/
  ├── base.njk
  └── post.njk
```

### Simplified Structure (Proposed)
```
src/_includes/
  ├── layouts/
  │   ├── base.njk
  │   └── post.njk
  ├── partials/
  │   ├── header.njk
  │   ├── footer.njk
  │   └── ...
  └── macros/
      ├── formatting.njk
      ├── image.njk
      └── ...
```

## CSS Organization

### Current Organization (Complex)
```
src/css/
  ├── basic.css              # Base styles
  ├── blog-enhanced.css      # Blog-specific styles
  ├── styles.css             # Combined styles
  ├── backup/                # CSS backups
  └── optimized/             # Alternative optimization
      ├── base.css
      ├── components.css
      ├── main.css
      ├── mobile.css
      ├── theme.css
      └── utilities.css
```

### Simplified Organization (Implemented)
```
src/css/
  ├── base/
  │   ├── reset.css          # CSS reset
  │   ├── typography.css     # Text styles
  │   └── layout.css         # Layout grid
  ├── components/
  │   ├── header.css         # Header component
  │   ├── footer.css         # Footer component
  │   ├── buttons.css        # Button components
  │   └── post.css           # Post component
  ├── utils/
  │   ├── variables.css      # CSS variables
  │   ├── mixins.css         # CSS utility classes
  │   └── animations.css     # Animation definitions
  └── main.css               # Imports all styles
```

## JavaScript Organization

### Current Organization (Complex)
```
src/js/
  ├── blog-search.js
  ├── heatmap.js
  ├── main.js
  ├── microlink-integration.js
  ├── search.js
  ├── site-enhancements.js
  ├── theme-switcher.js
  ├── theme-utils.js
  └── url-validator.js
```

### Simplified Organization (Proposed)
```
src/js/
  ├── components/
  │   ├── search.js          # Search functionality
  │   ├── theme-toggle.js    # Theme switching
  │   ├── heatmap.js         # Contribution heatmap
  │   └── ...                # Other components
  ├── utils/
  │   ├── dom.js             # DOM utilities
  │   ├── data.js            # Data utilities
  │   └── ...                # Other utilities
  ├── data/
  │   └── api.js             # API interactions
  └── main.js                # Entry point
```

## Content Workflow

### Current Workflow (Complex)
```
Write content in new_posts/
  ├── Run process:posts:batch or process:posts:enhanced
  ├── Content processed to new_posts/processed/
  ├── Files moved to src/posts/
  ├── Backup created in src/posts/backup/
  └── Custom fields added with standardize:frontmatter
```

### Simplified Workflow (Proposed)
```
Run post:new
  ├── Interactive prompts for title, tags, etc.
  ├── Template created in src/posts/
  ├── Images automatically selected
  └── Date scheduling managed automatically
```

## Benefits of Simplification

1. **Reduced Codebase Size**
   - Fewer files and directories
   - Less duplicate code
   - Clearer organization

2. **Simplified Mental Model**
   - Clear, logical structure
   - Predictable locations for files
   - Consistent naming patterns

3. **Improved Build Performance**
   - Fewer build steps
   - Less file copying
   - More efficient resource usage

4. **Enhanced Maintainability**
   - Easier to update and modify
   - Better separation of concerns
   - More intuitive architecture

5. **Streamlined Development**
   - Fewer commands to remember
   - More consistent processes
   - Better developer experience