---
title: Build & Deployment Automation
category: technical
priority: LOW
version: 1.0.0
last_updated: 2025-11-01
estimated_tokens: 1200
load_when:
  - Running builds
  - Debugging build issues
  - Understanding npm scripts
dependencies: []
tags: [build, npm, deployment, automation]
---

# Build & Deployment Automation

This document describes the build system, npm scripts, and deployment automation for the static site.

## Build System Overview

**Static Site Generator**: Eleventy (11ty)
**CSS Framework**: Tailwind CSS with PostCSS
**JavaScript**: Vanilla JS with esbuild bundling
**Asset Optimization**: ImageMagick, jpegoptim, optipng

## npm Scripts Reference

### Development Commands

Start local development server with hot reload:
```bash
npm run serve           # Full dev server with hot reload
npm run watch:css       # Watch and rebuild CSS only
npm run watch:eleventy  # Watch and rebuild Eleventy only
```

**What happens:**
- Eleventy starts dev server on http://localhost:8080
- CSS rebuilds on Tailwind changes
- Browser auto-refreshes on file changes

### Production Build

Build complete static site for deployment:
```bash
npm run build           # Full production build (CSS + Eleventy + JS)
npm run build:css       # Build CSS only with PostCSS
npm run build:eleventy  # Build Eleventy only
npm run build:js        # Bundle JavaScript files
```

**Build Pipeline:**
1. **CSS Build** (`build:css`):
   - Tailwind processes `src/assets/css/tailwind.css`
   - PostCSS applies plugins (autoprefixer, cssnano)
   - Outputs to `_site/assets/css/styles.css`

2. **JavaScript Build** (`build:js`):
   - esbuild bundles `src/assets/js/*.js`
   - Minifies and optimizes
   - Outputs to `_site/assets/js/bundle.js`

3. **Eleventy Build** (`build:eleventy`):
   - Processes Nunjucks templates
   - Converts Markdown posts to HTML
   - Generates sitemap, RSS feed
   - Outputs to `/_site` directory

**Build artifacts** (git-ignored):
- `/_site` - Complete static site
- `/node_modules` - npm dependencies

### Testing Commands

Run test suites:
```bash
npm run test            # Run unit tests
npm run test:unit       # Run unit tests only
npm run test:integration # Run integration tests
npm run test:e2e        # Run end-to-end tests
npm run test:all        # Run all test suites
npm run test:watch      # Run tests in watch mode
```

**Test Framework**: (Add details when implemented)

### Validation Commands

Validate standards and quality:
```bash
npm run validate:km     # Validate knowledge management standards
```

**Validation checks:**
- MANIFEST.json integrity
- File organization compliance
- Standards repository alignment

### Debugging Commands

Debug build issues:
```bash
npm run debug           # Run Eleventy with debug output
```

**Debug output includes:**
- Template processing steps
- Data file loading
- Plugin execution
- Filter applications

## Build Configuration Files

### `package.json`

Defines npm scripts and dependencies:
```json
{
  "scripts": {
    "build": "npm run build:css && npm run build:eleventy && npm run build:js",
    "serve": "eleventy --serve",
    "build:css": "postcss src/assets/css/tailwind.css -o _site/assets/css/styles.css",
    "build:eleventy": "eleventy",
    "build:js": "esbuild src/assets/js/*.js --bundle --minify --outfile=_site/assets/js/bundle.js"
  }
}
```

### `.eleventy.js`

Eleventy configuration:
- Plugins (syntax highlighting, image optimization)
- Filters (date formatting, excerpt generation)
- Collections (blog posts, tags)
- Passthroughs (assets, images)

### `tailwind.config.js`

Tailwind CSS customization:
- Content paths for purging
- Color palette
- Typography plugin
- Responsive breakpoints

### `postcss.config.js`

PostCSS plugin configuration:
- Tailwind CSS processing
- Autoprefixer for browser compatibility
- cssnano for production minification

## Build Optimization

### Asset Optimization

**Images:**
```bash
# Run image optimization
bash scripts/optimize-blog-images.sh

# Creates responsive variants:
# - Original: 1200px wide
# - Medium: 800px wide
# - Small: 400px wide
# - Thumbnail: 200px wide
```

**CSS:**
- Tailwind purges unused styles in production
- cssnano minifies CSS
- PostCSS adds vendor prefixes

**JavaScript:**
- esbuild bundles and minifies
- Tree shaking removes unused code

### Build Performance

**Current Performance:**
- **Build time**: ~3-5 seconds (full build)
- **Incremental rebuild**: <1 second (dev mode)
- **Asset generation**: Concurrent processing

**Optimization Strategies:**
- Cache Eleventy data between builds
- Parallelize asset processing
- Lazy-load non-critical JavaScript
- Optimize images before committing

## Deployment Workflow

### Automated Deployment

**Platform**: GitHub Pages (assumed based on .github workflows)

**Trigger**: Push to `main` branch

**Pipeline**:
1. GitHub Actions detects push
2. Installs dependencies (`npm ci`)
3. Runs build (`npm run build`)
4. Validates build artifacts
5. Deploys to GitHub Pages

### Manual Deployment

```bash
# 1. Build locally
npm run build

# 2. Test build
cd _site && python3 -m http.server 8000

# 3. Verify in browser
# http://localhost:8000

# 4. Deploy (if build looks good)
git add .
git commit -m "deploy: production build"
git push origin main
```

## Build Troubleshooting

### Common Build Issues

**1. CSS not updating:**
```bash
# Clear CSS cache
rm -rf _site/assets/css
npm run build:css
```

**2. Eleventy template errors:**
```bash
# Run with debug output
npm run debug

# Check for:
# - Missing frontmatter
# - Invalid Nunjucks syntax
# - Broken includes
```

**3. JavaScript bundle errors:**
```bash
# Check for syntax errors
npm run build:js

# Common issues:
# - Import/export syntax errors
# - Missing dependencies
# - Circular dependencies
```

**4. Build fails completely:**
```bash
# 1. Clear node_modules
rm -rf node_modules package-lock.json

# 2. Reinstall dependencies
npm install

# 3. Retry build
npm run build
```

### Performance Issues

**Slow builds:**
1. Check for large unoptimized images
2. Review Eleventy data file size
3. Disable unnecessary plugins
4. Use `--incremental` flag in dev

**Memory issues:**
1. Increase Node.js heap size: `NODE_OPTIONS=--max-old-space-size=4096`
2. Process images in smaller batches
3. Reduce concurrent build operations

## Build Validation

### Pre-Commit Validation

Pre-commit hooks automatically run:
```bash
# 1. MANIFEST.json validation
# 2. Standards compliance check
# 3. Humanization validation (blog posts)
# 4. Link validation (optional)
```

### Post-Build Validation

Verify build quality:
```bash
# Check build artifacts exist
ls -la _site/

# Validate HTML structure
# (Add HTML validator when implemented)

# Check asset sizes
du -sh _site/assets/*

# Verify no broken links
python scripts/link-validation/link-validator.py
```

### Production Checklist

Before deploying:
- [ ] `npm run build` succeeds
- [ ] `npm run test` passes
- [ ] Image optimization complete
- [ ] Link validation passes
- [ ] Mobile preview checked
- [ ] Lighthouse score ≥95

## Build Metrics

**Target Metrics:**
- **Lighthouse Mobile**: ≥95
- **LCP (Largest Contentful Paint)**: <2.5s
- **FID (First Input Delay)**: <100ms
- **CLS (Cumulative Layout Shift)**: <0.1
- **Total JS bundle**: <100KB
- **Total CSS**: <50KB

**Current Performance**: (Add metrics from latest build)

## Related Documentation

- **Eleventy Docs**: https://www.11ty.dev/docs/
- **Tailwind Docs**: https://tailwindcss.com/docs
- **PostCSS Plugins**: https://postcss.org/
- **esbuild**: https://esbuild.github.io/
