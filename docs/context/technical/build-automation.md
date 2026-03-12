---
title: Build & Deployment Automation
category: technical
priority: LOW
version: 2.0.0
last_updated: 2026-03-12
estimated_tokens: 1000
load_when:
  - Running builds
  - Debugging build issues
  - Understanding npm scripts
dependencies: []
tags: [build, npm, deployment, automation, astro]
---

# Build & Deployment Automation

This document describes the build system, npm scripts, and deployment automation for the static site.

## Build System Overview

**Static Site Generator**: Astro 6 with Svelte 5 islands
**CSS Framework**: Tailwind CSS 4 via @tailwindcss/vite plugin
**Search**: Pagefind (static search index)
**Charts**: D3.js for stats visualization
**TypeScript**: Strict mode with path aliases

## npm Scripts Reference

All commands run from the `astro-site/` directory.

### Development Commands

Start local development server with hot module replacement:
```bash
cd astro-site
npm run dev             # Astro dev server with HMR
```

**What happens:**
- Astro starts dev server on http://localhost:4321
- Tailwind CSS rebuilds on changes via Vite plugin
- Browser auto-refreshes on file changes

### Production Build

Build complete static site for deployment:
```bash
cd astro-site
npm run build           # Astro build + Pagefind search index
npm run preview         # Preview production build locally
npm run check           # Run Astro type checking
```

**Build Pipeline:**
1. **Astro Build**: Processes .astro and .svelte components, renders Markdown content from `../src/posts/` via content collections, generates static HTML
2. **Pagefind**: Indexes all pages for client-side search
3. **Output**: `astro-site/dist/` directory

**Build artifacts** (git-ignored):
- `astro-site/dist/` - Complete static site
- `astro-site/node_modules/` - npm dependencies

## Build Configuration Files

### `astro-site/package.json`

Defines npm scripts and dependencies.

### `astro-site/astro.config.mjs`

Astro configuration:
- Integrations: Svelte, Sitemap
- Prefetch: enabled for instant navigation
- Vite plugins: Tailwind CSS
- Markdown: Shiki syntax highlighting (github-light/dark themes)
- Rollup: Pagefind external

### `astro-site/tsconfig.json`

TypeScript strict mode with path aliases:
- `@/*` → `src/*`
- `@components/*` → `src/components/*`
- `@layouts/*` → `src/layouts/*`
- `@styles/*` → `src/styles/*`

### `astro-site/src/content.config.ts`

Content collection definitions:
- **posts**: Glob loader from `../src/posts/*.md` with Zod schema
- **projects**: Glob loader from `../src/projects/*.md` with Zod schema

## Build Optimization

### Asset Optimization

**CSS:**
- Tailwind 4 CSS-only config (no tailwind.config.js needed)
- Automatic purging of unused styles
- Vite handles minification

**JavaScript:**
- Astro islands: only hydrates interactive components
- Svelte components compile to minimal JS
- Pagefind search loaded on demand

### Build Performance

**Current Performance:**
- **Build time**: ~10-15 seconds (full build with Pagefind)
- **Dev server startup**: ~2 seconds
- **Hot module replacement**: instant

## Deployment Workflow

### Automated Deployment

**Platform**: GitHub Pages
**Trigger**: Push to `main` branch
**Workflow**: `.github/workflows/deploy.yml`

**Pipeline**:
1. GitHub Actions detects push to main
2. Installs dependencies (`cd astro-site && npm ci`)
3. Runs build (`npm run build`) with NODE_ENV=production
4. Uploads `astro-site/dist/` as Pages artifact
5. Deploys to GitHub Pages

### Manual Deployment

```bash
# 1. Build locally
cd astro-site && npm run build

# 2. Preview build
npm run preview
# Visit http://localhost:4321

# 3. Deploy (if build looks good)
git add .
git commit -m "deploy: production build"
git push origin main
```

## Build Troubleshooting

### Common Build Issues

**1. CSS not updating:**
```bash
# Restart dev server (Vite caches aggressively)
cd astro-site && npm run dev
```

**2. Content collection errors:**
```bash
# Run type checking
cd astro-site && npm run check

# Common issues:
# - Missing required frontmatter fields
# - Invalid date format in posts
# - Schema validation failures
```

**3. Build fails completely:**
```bash
# 1. Clear node_modules and reinstall
cd astro-site
rm -rf node_modules package-lock.json
npm install

# 2. Clear Astro cache
rm -rf .astro

# 3. Retry build
npm run build
```

## Build Validation

### Pre-Commit Validation

Pre-commit hooks automatically run:
- MANIFEST.json validation
- Standards compliance check
- Blog post code ratios
- Python logging enforcement
- NDA compliance scanning

### Post-Build Validation

Verify build quality:
```bash
# Check build artifacts exist
ls -la astro-site/dist/

# Verify page count
find astro-site/dist -name "*.html" | wc -l

# Check asset sizes
du -sh astro-site/dist/
```

### Production Checklist

Before deploying:
- [ ] `npm run build` succeeds (from astro-site/)
- [ ] `npm run check` passes (TypeScript/Astro validation)
- [ ] Lighthouse score ≥90
- [ ] Link validation passes

## Build Metrics

**Target Metrics:**
- **Lighthouse Performance**: ≥90
- **Lighthouse Accessibility**: ≥90
- **LCP (Largest Contentful Paint)**: <2.5s
- **CLS (Cumulative Layout Shift)**: <0.1
- **Total JS bundle**: minimal (Astro islands architecture)

## Related Documentation

- **Astro Docs**: https://docs.astro.build/
- **Svelte Docs**: https://svelte.dev/docs
- **Tailwind CSS 4**: https://tailwindcss.com/docs
- **Pagefind**: https://pagefind.app/
