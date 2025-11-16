# Developer Handoff Guide

**Version:** 1.0.0
**Last Updated:** 2025-11-15
**Purpose:** Quick start for developers inheriting this codebase

## 30-Second Overview

Modern personal blog built with Eleventy (11ty), styled with Tailwind CSS and custom OKLCH color system, deployed to GitHub Pages. WCAG AAA accessible, dark mode enabled, component-based architecture.

**Tech stack:**
- Static site generator: Eleventy 3.0.0
- CSS: Tailwind 4.1.17 + custom design system
- Colors: OKLCH (perceptually uniform)
- Components: Nunjucks templates
- Build: npm scripts
- Deploy: GitHub Pages (automated)

**Quick start:**
```bash
npm install
npm run dev  # localhost:8080
npm run build  # Production build
```

## Architecture

### Directory Structure

```
williamzujkowski.github.io/
├── src/
│   ├── _data/              # Global data files
│   ├── _includes/
│   │   ├── components/     # Reusable Nunjucks components
│   │   │   ├── hero-modern.njk
│   │   │   ├── nav-modern.njk
│   │   │   ├── post-card-modern.njk
│   │   │   └── feature-card-modern.njk
│   │   └── layouts/        # Page layouts
│   ├── assets/
│   │   ├── css/
│   │   │   ├── main.css              # Import orchestrator
│   │   │   ├── tailwind.css          # Tailwind base
│   │   │   ├── theme-tokens.css      # CSS custom properties
│   │   │   ├── modern-design.css     # Design system (925 lines)
│   │   │   └── cybersecurity-effects.css
│   │   ├── js/             # Client-side JavaScript
│   │   └── images/         # Static images
│   ├── posts/              # Blog posts (Markdown)
│   └── index.njk           # Homepage
├── docs/                   # Documentation
│   ├── DESIGN_SYSTEM.md    # Color palette, typography, spacing
│   ├── ACCESSIBILITY_GUIDE.md
│   ├── DESIGN_MAINTENANCE.md
│   └── DEVELOPER_HANDOFF.md (this file)
├── scripts/                # Automation utilities
├── .eleventy.js            # Eleventy configuration
├── tailwind.config.js      # Tailwind configuration
└── package.json            # npm dependencies
```

### Build Process

**Development:**
```bash
npm run dev
# 1. Eleventy watches src/ for changes
# 2. Rebuilds on file save
# 3. Serves at http://localhost:8080
# 4. Live reload enabled
```

**Production:**
```bash
npm run build
# 1. Eleventy builds to _site/
# 2. Tailwind purges unused CSS
# 3. PostCSS minifies CSS
# 4. Output ready for deployment
```

### CSS Architecture

**Load order (main.css):**
```css
1. tailwind.css          /* Tailwind base + utilities */
2. theme-tokens.css      /* CSS custom properties */
3. modern-design.css     /* Design system components */
4. cybersecurity-effects.css
5. enhancements.css
```

**Design tokens:**
- Light mode: "Warm Canvas" (warm neutrals, burnt orange accents)
- Dark mode: "Midnight Espresso" (purple-black, coral/lime accents)
- All colors defined in OKLCH (perceptually uniform)
- Typography: 1.25 modular scale (14px → 69px)
- Spacing: 4px base unit

**File sizes:**
- modern-design.css: 45KB uncompressed (7KB gzipped)
- Total CSS bundle: 120KB uncompressed (18KB gzipped)

## Design System

### OKLCH Color System

**Why OKLCH?**
- Perceptually uniform (equal lightness looks equally bright)
- Better color mixing than HSL/RGB
- Wide gamut support for modern displays

**Browser support:** Chrome 111+, Safari 15.4+, Firefox 113+

**Light mode palette:**
```css
--clr-light-bg-base: oklch(98% 0.01 80);        /* warm off-white */
--clr-light-primary: oklch(55% 0.18 25);        /* burnt orange */
--clr-light-secondary: oklch(45% 0.15 160);     /* deep teal */
--clr-light-text-primary: oklch(25% 0.02 270);  /* rich charcoal */
```

**Dark mode palette:**
```css
--clr-dark-bg-base: oklch(15% 0.02 270);        /* purple-black */
--clr-dark-primary: oklch(75% 0.19 50);         /* warm coral */
--clr-dark-secondary: oklch(80% 0.15 110);      /* bright lime */
--clr-dark-text-primary: oklch(95% 0.01 270);   /* nearly white */
```

### Typography

**Font stack:**
```css
--font-display: "Cabinet Grotesk", "Satoshi", system-ui, sans-serif;
--font-body: "Geist", "DM Sans", system-ui, sans-serif;
--font-mono: "GeistMono", "Berkeley Mono", monospace;
```

**Modular scale (1.25 ratio):**
```css
--text-xs: 14px
--text-sm: 18px
--text-base: 22px
--text-lg: 28px
--text-xl: 35px
--text-2xl: 44px
--text-3xl: 55px
--text-4xl: 69px
```

### Spacing

**Base unit:** 4px

```css
--space-1: 4px
--space-2: 8px
--space-4: 16px
--space-6: 24px
--space-8: 32px
--space-12: 48px
--space-16: 64px
--space-24: 96px
```

## Components

### Using Existing Components

**Hero section:**
```njk
{% include "components/hero-modern.njk" %}
```

**Navigation:**
```njk
{% include "components/nav-modern.njk" %}
```

**Post card:**
```njk
{% set post = postObject %}
{% include "components/post-card-modern.njk" %}
```

**Feature card:**
```njk
{% set icon = '<path d="..." />' %}
{% set title = "Feature Title" %}
{% set description = "Feature description" %}
{% include "components/feature-card-modern.njk" %}
```

### Creating New Components

**Step 1:** Create file in `src/_includes/components/`
```bash
touch src/_includes/components/new-component.njk
```

**Step 2:** Write Nunjucks template
```njk
<div class="modern-card">
  <h3 class="text-subheading">{{ title }}</h3>
  <p class="text-body">{{ description }}</p>
</div>
```

**Step 3:** Add styles to `modern-design.css`
```css
.modern-card {
  background: var(--clr-light-bg-surface);
  padding: var(--space-8);
  border-radius: 16px;
}

.dark .modern-card {
  background: var(--clr-dark-bg-surface);
}
```

**Step 4:** Use in templates
```njk
{% set title = "Component Title" %}
{% set description = "Component description" %}
{% include "components/new-component.njk" %}
```

## Common Tasks

### Adding a New Blog Post

**Step 1:** Create Markdown file
```bash
touch src/posts/new-post.md
```

**Step 2:** Add frontmatter
```markdown
---
title: "Post Title"
description: "Post description for SEO and social sharing"
date: 2025-11-15
author: "William Zujkowski"
tags:
  - tag1
  - tag2
image: "/assets/images/post-image.jpg"
---

Post content here...
```

**Step 3:** Write content (Markdown)
```markdown
## Section Heading

Paragraph text.

- Bullet point 1
- Bullet point 2

```code
Code block
```
```

**Step 4:** Build and preview
```bash
npm run dev
# Visit http://localhost:8080/posts/new-post/
```

### Updating Colors

**Step 1:** Edit `src/assets/css/theme-tokens.css`
```css
:root {
  /* Update light mode color */
  --clr-light-primary: oklch(50% 0.20 25);  /* New value */
}

.dark {
  /* Update dark mode color */
  --clr-dark-primary: oklch(70% 0.22 50);  /* New value */
}
```

**Step 2:** Validate contrast ratios
```bash
# Use browser DevTools or contrast checker
# Ensure 7:1 minimum for body text (AAA)
```

**Step 3:** Test light/dark modes
```bash
npm run dev
# Toggle theme button in browser
# Verify colors render correctly
```

### Modifying Typography

**To change font:**
```css
/* src/assets/css/theme-tokens.css or modern-design.css */
@font-face {
  font-family: 'NewFont';
  src: url('/fonts/NewFont-Regular.woff2') format('woff2');
  font-weight: 400;
  font-display: swap;
}

:root {
  --font-body: "NewFont", system-ui, sans-serif;
}
```

**To adjust scale:**
```css
:root {
  /* Change ratio from 1.25 to 1.333 */
  --text-lg: clamp(1.777rem, 1.2vw + 1.4rem, 2.1rem);
}
```

### Managing Dark Mode

**Toggle implementation:**
```javascript
// src/assets/js/theme-toggle.js (or in base.njk)
function toggleTheme() {
  const html = document.documentElement;
  html.classList.toggle('dark');
  localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
}
```

**Initialize on page load:**
```javascript
const savedTheme = localStorage.getItem('theme');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
  document.documentElement.classList.add('dark');
}
```

**Add dark mode styles:**
```css
.element {
  background: var(--clr-light-bg-surface);
}

.dark .element {
  background: var(--clr-dark-bg-surface);
}
```

## Deployment

### GitHub Pages (Automated)

**Current setup:**
```yaml
# .github/workflows/deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run build
      - uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

**Trigger deployment:**
```bash
git add .
git commit -m "feat: update design"
git push origin main
# GitHub Actions builds and deploys automatically
```

### Manual Deployment

**Build locally:**
```bash
npm run build
# Output: _site/
```

**Deploy to any static host:**
```bash
# Upload _site/ contents to:
# - Netlify
# - Vercel
# - AWS S3 + CloudFront
# - Any static file server
```

## Testing

### Local Testing

**Development server:**
```bash
npm run dev
# http://localhost:8080
```

**Production build:**
```bash
npm run build
npx http-server _site/
# http://localhost:8080
```

### Accessibility Testing

**Automated:**
```bash
# Lighthouse (Chrome DevTools)
npx lighthouse https://williamzujkowski.github.io --view

# Target: 95+ accessibility score
```

**Manual:**
- [ ] Tab through all interactive elements (focus indicators visible)
- [ ] Toggle dark mode (smooth transition, no flashes)
- [ ] Test screen reader (NVDA/VoiceOver)
- [ ] Verify contrast ratios (WAVE or axe DevTools)
- [ ] Enable reduced motion (animations disabled)

### Cross-Browser Testing

**Minimum supported:**
- Chrome 111+ (OKLCH support)
- Safari 15.4+ (OKLCH support)
- Firefox 113+ (OKLCH support)

**Test checklist:**
- [ ] OKLCH colors render correctly
- [ ] Frosted glass navigation works
- [ ] Gradient mesh animates smoothly
- [ ] Dark mode toggle functions
- [ ] Typography scales responsively

## Troubleshooting

### Build Fails

**Symptoms:** `npm run build` errors

**Common causes:**
1. Missing dependencies: `npm install`
2. Node version mismatch: Use Node 18+ (`node -v`)
3. Syntax error in Nunjucks template: Check error message for file/line

### Colors Look Wrong

**Symptoms:** OKLCH colors not rendering

**Solutions:**
1. Check browser version (Chrome 111+, Safari 15.4+, Firefox 113+)
2. Verify CSS custom properties syntax: `var(--variable-name)`
3. Clear browser cache (Ctrl+Shift+R / Cmd+Shift+R)

### Dark Mode Not Working

**Symptoms:** Theme toggle doesn't change colors

**Solutions:**
1. Check `.dark` class on `<html>` element (inspect in DevTools)
2. Verify dark mode variables defined in CSS
3. Test localStorage: `localStorage.getItem('theme')`
4. Check JavaScript console for errors

### Fonts Not Loading

**Symptoms:** System fonts used instead of custom fonts

**Solutions:**
1. Verify font files in `/public/fonts`
2. Check @font-face `src` path matches file location
3. Preload critical fonts in `<head>`
4. Check Network tab (fonts should load with 200 status)

## Code Standards

### CSS Conventions

**Use design tokens:**
```css
/* Good */
color: var(--clr-light-text-primary);
padding: var(--space-8);

/* Avoid */
color: #1a1a1a;
padding: 32px;
```

**Dark mode pattern:**
```css
.element {
  /* Light mode (default) */
  background: var(--clr-light-bg-surface);
}

.dark .element {
  /* Dark mode override */
  background: var(--clr-dark-bg-surface);
}
```

### Component Conventions

**Naming:** `[component]-modern.njk`

**Structure:**
```njk
{# Component description #}
{# Required variables: title, description #}

<div class="modern-card">
  <h3 class="text-subheading">{{ title }}</h3>
  <p class="text-body">{{ description }}</p>
</div>
```

**Documentation:** Add to `docs/MODERN_COMPONENTS_GUIDE.md`

### Accessibility Requirements

**Contrast ratios:**
- Body text: 7:1 minimum (AAA)
- Large text: 4.5:1 minimum (AA)
- Button text: 7:1 minimum (AAA)

**Focus indicators:**
```css
:focus-visible {
  outline: 3px solid var(--clr-light-primary);
  outline-offset: 2px;
}
```

**Semantic HTML:**
- Use `<header>`, `<nav>`, `<main>`, `<footer>`
- Proper heading hierarchy (h1 → h2 → h3)
- ARIA labels on icon-only buttons

## Documentation

**Essential reading:**
- `docs/DESIGN_SYSTEM.md` - Complete design system reference
- `docs/ACCESSIBILITY_GUIDE.md` - WCAG compliance procedures
- `docs/MODERN_COMPONENTS_GUIDE.md` - Component usage examples
- `docs/DESIGN_MAINTENANCE.md` - Maintenance procedures

**Quick reference:**
- Color palette → DESIGN_SYSTEM.md
- Typography scale → DESIGN_SYSTEM.md
- Spacing system → DESIGN_SYSTEM.md
- Component API → MODERN_COMPONENTS_GUIDE.md
- Contrast ratios → ACCESSIBILITY_GUIDE.md
- Dark mode → DESIGN_MAINTENANCE.md

## Support

**Questions?**
1. Check `docs/` directory for relevant guide
2. Inspect existing components in `src/_includes/components/`
3. Review CSS architecture in `src/assets/css/`

**Common issues:**
- Build errors → Troubleshooting section above
- Design questions → DESIGN_SYSTEM.md
- Accessibility concerns → ACCESSIBILITY_GUIDE.md
- Maintenance procedures → DESIGN_MAINTENANCE.md

---

**Last updated:** 2025-11-15
**Maintained by:** William Zujkowski
**Tech stack version:** Eleventy 3.0.0, Tailwind 4.1.17, Node 18+
