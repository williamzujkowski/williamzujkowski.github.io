# Website Simplification: Phase 1 Implementation Plan

This document provides specific, actionable steps for the first phase of simplifying the website architecture while maintaining all current functionality.

## 1. Data Directory Consolidation

### Current Issues:
- Data is spread across multiple directories (`_data/`, `assets/data/`, `scripts/_data/`)
- Duplicate files exist in different locations
- Scripts reference different paths for the same data
- Build process has to synchronize data across locations

### Implementation Steps:

1. **Create unified data structure in `/src/_data`**
   ```bash
   mkdir -p /src/_data/core
   mkdir -p /src/_data/config
   mkdir -p /src/_data/cache
   ```

2. **Move core data files to the central location**
   ```bash
   # Move essential data files
   cp _data/arxiv-feed.json src/_data/core/
   cp _data/books.json src/_data/core/
   cp _data/current-reading.json src/_data/core/
   cp _data/contribution-heatmap.json src/_data/core/
   cp _data/github-pins.json src/_data/core/
   
   # Move configuration files
   cp -r src/_data/config/* src/_data/config/
   ```

3. **Update data file references in Eleventy config**
   ```javascript
   // In .eleventy.simple.cjs
   // Change from:
   const arxivPath = path.join(__dirname, '..', '_data', 'arxiv-feed.json');
   
   // To:
   const arxivPath = path.join(__dirname, 'src', '_data', 'core', 'arxiv-feed.json');
   ```

4. **Update build scripts to use the unified data location**
   ```javascript
   // In create-fallback-data.js and other scripts
   // Change from:
   const dataDir = './_data';
   const publicDataDir = './assets/data';
   
   // To:
   const dataDir = './src/_data/core';
   ```

5. **Remove redundant data directories after verifying builds**
   ```bash
   # After successful testing
   rm -rf _data/
   rm -rf assets/data/
   rm -rf scripts/_data/
   ```

## 2. Build Process Simplification

### Current Issues:
- Too many npm scripts (30+) with overlapping functionality
- Multiple post processing scripts
- Redundant CSS build processes
- Excessive build steps for development

### Implementation Steps:

1. **Consolidate npm scripts in package.json**
   ```javascript
   // Simplify build scripts to:
   "scripts": {
     "build": "npm run build:data && eleventy --config=.eleventy.js && npm run build:css",
     "build:data": "node scripts/build/create-core-data.js",
     "build:css": "postcss src/css/styles.css -o _site/css/styles.css",
     "dev": "npm run build:data && concurrently \"eleventy --config=.eleventy.js --serve\" \"npm run watch:css\"",
     "watch:css": "postcss src/css/styles.css -o _site/css/styles.css --watch",
     "post:new": "node scripts/content/create-post.js",
     "lint": "eslint \"src/**/*.js\"",
     "format": "prettier --write \"src/**/*.{js,json,css,md,njk}\""
   }
   ```

2. **Create unified post processing script**
   ```javascript
   // Create a single post processor in scripts/content/create-post.js
   // that handles:
   // - New post creation
   // - Date scheduling
   // - Frontmatter generation
   // - Image selection
   ```

3. **Simplify Eleventy configuration**
   ```javascript
   // Consolidate .eleventy.simple.cjs into .eleventy.js in project root
   // Move all configuration into this single file
   // Remove any GitHub-specific configuration paths
   ```

4. **Create unified CSS build process**
   ```javascript
   // Consolidate PostCSS configurations
   // Simplify Tailwind configuration
   // Remove multiple CSS optimization approaches
   ```

5. **Simplify data generation process**
   ```javascript
   // Create a single create-core-data.js script that:
   // - Creates necessary data structure
   // - Generates minimal data required for development
   // - Uses static fallback data where appropriate
   ```

## 3. Template Structure Simplification

### Current Issues:
- Excessive template nesting
- Inline JavaScript in templates
- Redundant template sections
- Inconsistent template naming

### Implementation Steps:

1. **Create a clear template hierarchy**
   ```
   src/
     _includes/
       layouts/         # Base page layouts
         base.njk       # Main site layout
         post.njk       # Post layout
       partials/        # Reusable components
         header.njk
         footer.njk
         post-list.njk
       macros/          # Utility functions
         formatting.njk
         image.njk
   ```

2. **Extract inline JavaScript to separate files**
   ```javascript
   // Move inline scripts from templates to:
   src/js/components/search.js
   src/js/components/theme-toggle.js
   src/js/components/post-navigation.js
   ```

3. **Standardize template inclusion patterns**
   ```njk
   {# Consistent include pattern #}
   {% include "partials/header.njk" %}
   
   {# Consistent macro usage #}
   {% from "macros/image.njk" import image %}
   {{ image("path.jpg", "Alt text", "100vw") }}
   ```

4. **Simplify page templates**
   ```njk
   {# Remove duplicate template code #}
   {# Standardize block names #}
   {% extends "layouts/base.njk" %}
   
   {% block content %}
     {# Page-specific content #}
   {% endblock %}
   ```

## 4. CSS Organization Simplification

### Current Issues:
- Large, monolithic CSS files
- Multiple CSS approaches (basic, optimized, enhanced)
- Duplicate styles and variables
- Complex responsive behavior

### Implementation Steps:

1. **Adopt a component-based CSS structure**
   ```
   src/
     css/
       base/         # Base styles
         reset.css
         typography.css
         layout.css
       components/   # Component styles
         header.css
         footer.css
         post.css
       utils/        # Utilities
         variables.css
         mixins.css
       main.css      # Imports all styles
   ```

2. **Implement CSS custom properties for theming**
   ```css
   /* variables.css */
   :root {
     --color-primary: #3498db;
     --color-secondary: #2ecc71;
     --color-text: #333333;
     --color-background: #ffffff;
     /* etc. */
   }
   
   [data-theme="dark"] {
     --color-primary: #3498db;
     --color-secondary: #2ecc71;
     --color-text: #eeeeee;
     --color-background: #121212;
     /* etc. */
   }
   ```

3. **Simplify responsive design approach**
   ```css
   /* Using mobile-first approach consistently */
   .component {
     /* Base mobile styles */
     
     @media (min-width: 768px) {
       /* Tablet styles */
     }
     
     @media (min-width: 1024px) {
       /* Desktop styles */
     }
   }
   ```

4. **Reduce CSS size with better selector strategy**
   ```css
   /* Instead of verbose selectors */
   .blog-post .blog-post-header .blog-post-title {
     /* styles */
   }
   
   /* Use more efficient class-based targeting */
   .post-title {
     /* styles */
   }
   ```

## 5. JavaScript Simplification

### Current Issues:
- Multiple utility scripts with overlapping functionality
- Inline scripts in templates
- Lack of module organization
- Complex DOM manipulation

### Implementation Steps:

1. **Organize JavaScript into modules**
   ```
   src/
     js/
       components/      # UI components
       utils/           # Utility functions
       data/            # Data handling
       main.js          # Entry point
   ```

2. **Use ES modules consistently**
   ```javascript
   // utils/dom.js
   export function $(selector) {
     return document.querySelector(selector);
   }
   
   // components/theme-toggle.js
   import { $ } from '../utils/dom.js';
   
   export function initThemeToggle() {
     const toggle = $('.theme-toggle');
     // Implementation
   }
   
   // main.js
   import { initThemeToggle } from './components/theme-toggle.js';
   
   document.addEventListener('DOMContentLoaded', () => {
     initThemeToggle();
     // Initialize other components
   });
   ```

3. **Simplify event handling**
   ```javascript
   // Instead of multiple event bindings
   document.querySelectorAll('.tag').forEach(tag => {
     tag.addEventListener('click', handleTagClick);
   });
   
   // Use event delegation
   document.addEventListener('click', e => {
     if (e.target.matches('.tag')) {
       handleTagClick(e);
     }
   });
   ```

4. **Reduce runtime complexity**
   ```javascript
   // Instead of complex DOM updates
   function updateList() {
     // Clear container
     container.innerHTML = '';
     
     // Create all items
     items.forEach(item => {
       const el = document.createElement('div');
       // Complex setup
       container.appendChild(el);
     });
   }
   
   // Use document fragments for better performance
   function updateList() {
     const fragment = document.createDocumentFragment();
     
     items.forEach(item => {
       const el = document.createElement('div');
       // Setup
       fragment.appendChild(el);
     });
     
     // Single DOM operation
     container.innerHTML = '';
     container.appendChild(fragment);
   }
   ```

## Expected Benefits of Phase 1

1. **Reduced Complexity**
   - Fewer directories and files to maintain
   - Clearer organization of code and assets
   - More intuitive project navigation

2. **Improved Performance**
   - Faster build times with simplified process
   - Reduced CSS payload with better organization
   - More efficient JavaScript execution

3. **Enhanced Maintainability**
   - Clearer separation of concerns
   - More consistent coding patterns
   - Better documentation of architecture

4. **Simplified Workflow**
   - Fewer commands needed for common tasks
   - More reliable build process
   - Clearer path for creating new content

## Next Steps After Phase 1

1. Evaluate performance improvements from Phase 1
2. Gather feedback on the simplified architecture
3. Identify remaining areas of unnecessary complexity
4. Plan Phase 2 focusing on content workflow simplification
5. Update documentation to reflect the new architecture