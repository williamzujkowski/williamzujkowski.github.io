# AI Knowledge Router - williamzujkowski.github.io

**Version:** 2.0.0  
**Last Updated:** 2024-01-24  
**Status:** Active  
**Type:** AI Interface Document

---

## 🤖 Quick Start for AI Assistants

This document helps AI assistants efficiently navigate and understand this personal website repository. It implements the Knowledge Management Standards (KM) for optimal token usage and progressive disclosure.

> **Important:** This project integrates with [.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md) for comprehensive standards management. Use the standards router for all development standards queries.

### Primary Purpose
Personal website built with Eleventy, featuring blog posts, project documentation, and professional information. Deployed via GitHub Pages with automated CI/CD.

### Quick Commands
```
# Site-specific commands
@load [section] - Load specific section of this document
@summary - Get executive summary only
@find "query" - Natural language search
@status - Current deployment and build status

# Standards commands (via .standards/docs/core/CLAUDE.md)
@load standards:[standard-code] - Load specific standard
@load FE:* - Load Frontend standards
@load WD:* - Load Web Design standards
@load SEO:* - Load SEO standards
@load GH:pages - Load GitHub Pages standards
```

---

## 📊 Repository Overview

**Total Tokens:** ~8,000 (estimated)  
**Primary Language:** JavaScript/Nunjucks  
**Framework:** Eleventy 2.0  
**Deployment:** GitHub Pages  

### Key Metrics
- **Build Time:** ~0.06 seconds
- **Deploy Time:** ~30 seconds via GitHub Actions
- **Content Files:** 5 pages, 1 post
- **Standards Compliance:** Integrated via submodule

---

## 🗺️ Navigation Map

### For Site Development
| Task | Load These Sections | Standards to Apply |  
|------|---------------------|--------------------|

| Add new blog post | `content-management` + `posts-structure` | `@load CONT:writing + SEO:on-page` |
| Update styling | `styling-architecture` + `eleventy-config` | `@load WD:visual-design + FE:performance` |
| Fix build issues | `troubleshooting` + `github-actions` | `@load GH:actions + TOOL:javascript` |
| Add new page | `content-management` + `templates` | `@load FE:architecture + WD:ux-patterns` |
| SEO optimization | `seo-metadata` + `eleventy-config` | `@load SEO:* + CONT:seo` |
| Performance optimization | `performance-metrics` | `@load FE:performance + SEO:core-web-vitals` |
| Accessibility improvements | `templates` + `styling-architecture` | `@load WD:accessibility + FE:accessibility` |

### For Content Updates
| Content Type | Location | Template Used |
|--------------|----------|---------------|
| Blog Posts | `src/posts/*.md` | `post.njk` layout |
| Static Pages | `src/pages/*.md` | `page.njk` layout |
| Homepage | `src/index.njk` | `base.njk` layout |
| Global Data | `src/_data/*.json` | Available everywhere |

---

## 📁 Architecture Overview (~500 tokens)

### Directory Structure
```
williamzujkowski.github.io/
├── src/                    # Source files (Eleventy input)
│   ├── _includes/         # Templates and partials
│   │   └── layouts/       # Page layouts (base, page, post)
│   ├── _data/            # Global data (site.json)
│   ├── assets/           # Static assets (CSS, JS, images)
│   ├── pages/            # Static pages (about, contact)
│   ├── posts/            # Blog posts (Markdown)
│   └── index.njk         # Homepage
├── _site/                # Build output (git-ignored)
├── .eleventy.js          # Eleventy configuration
├── .github/workflows/    # CI/CD automation
├── .standards/           # Development standards (submodule)
└── package.json          # Dependencies and scripts
```

### Technology Stack
- **SSG:** Eleventy 2.0.1
- **Templates:** Nunjucks (.njk)
- **Styling:** Vanilla CSS with CSS Custom Properties
- **Build:** Node.js 18+
- **Deploy:** GitHub Actions → GitHub Pages
- **Standards:** Integrated via `.standards` submodule

---

## 📝 Content Management (~1,000 tokens)

### Posts Structure
All blog posts live in `src/posts/` with this frontmatter:

```yaml
---
title: Your Post Title
date: 2024-01-24
description: Brief description for SEO and listings
tags: [optional, tags, here]
---

Your markdown content here...
```

**Auto-generated from posts:**
- URL: `/posts/[title-slug]/`
- Listed on: `/posts/` page
- Sorted by: Date (newest first)

### Pages Structure
Static pages in `src/pages/` use:

```yaml
---
layout: page
title: Page Title
description: SEO description
permalink: /custom-url/
---

Page content...
```

### Global Data
Edit `src/_data/site.json`:
```json
{
  "title": "William Zujkowski",
  "description": "Personal website of William Zujkowski",
  "url": "https://williamzujkowski.github.io",
  "author": "William Zujkowski",
  "currentYear": 2024
}
```

---

## 🎨 Styling Architecture (~800 tokens)

### CSS Structure
Main stylesheet: `src/assets/css/main.css`

**Design Tokens:**
```css
:root {
  --color-primary: #1a1a1a;
  --color-secondary: #666;
  --color-accent: #0066cc;
  --color-background: #ffffff;
  --color-surface: #f5f5f5;
  --font-body: system-ui, sans-serif;
  --max-width: 1200px;
  --spacing: 1rem;
}
```

**Key Features:**
- Mobile-first responsive design
- Semantic HTML5 elements
- Accessibility-first approach
- No JavaScript required for core functionality

---

## ⚙️ Eleventy Configuration (~1,200 tokens)

### Core Config (.eleventy.js)
```javascript
// Key configurations:
- Input: src/
- Output: _site/
- Templates: Nunjucks
- Passthrough: assets/, CNAME, .nojekyll
- Filters: readableDate, htmlDateString
- Layout aliases: base, page, post
```

### Build Scripts
```bash
npm run build    # Production build
npm run serve    # Dev server (localhost:8080)
npm run debug    # Debug mode with verbose output
```

### Collections
Currently uses tags for posts collection:
- Posts tagged with "posts" appear in blog listing
- Sorted by date in reverse order
- Automatic pagination ready to implement

---

## 🚀 GitHub Actions (~1,000 tokens)

### Deployment Workflow
`.github/workflows/eleventy_build.yml`:
- Triggers on push to main
- Builds site with Eleventy
- Deploys to GitHub Pages
- ~30 second deployment time

### Standards Compliance
`.github/workflows/standards-compliance.yml`:
- HTML validation
- Build verification
- Runs on all PRs

### Debugging Deployments
```bash
# Check workflow status
gh run list --limit 5

# View specific run
gh run view [RUN_ID]

# Check deployment
curl -I https://williamzujkowski.github.io/
```

---

## 🔍 SEO & Metadata (~600 tokens)

### Page Metadata
Each page includes:
```html
<!-- Basic Meta -->
<meta name="description" content="...">
<meta name="author" content="...">

<!-- Open Graph -->
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:type" content="website">
<meta property="og:url" content="...">

<!-- Twitter -->
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="...">
```

### Structured Data Ready
Templates prepared for:
- JSON-LD schema markup
- RSS feed generation
- Sitemap.xml
- Robots.txt

---

## 🐛 Troubleshooting (~800 tokens)

### Common Issues

**Build Fails Locally:**
```bash
rm -rf node_modules package-lock.json
npm install
npm run build
```

**GitHub Actions Failing:**
1. Check workflow logs: `gh run view --log`
2. Verify Node version matches locally
3. Check for submodule issues
4. Ensure .nojekyll exists in src/

**Page Not Updating:**
- GitHub Pages cache: wait 5-10 minutes
- Check _site/ contains expected files
- Verify GitHub Pages enabled in Settings
- Check branch settings (should use workflow)

**CSS Not Loading:**
- Check asset paths are absolute (/assets/...)
- Verify passthrough copy in .eleventy.js
- Check browser console for 404s

---

## 📚 Templates System (~1,000 tokens)

### Layout Hierarchy
```
base.njk          # HTML skeleton, header, footer
├── page.njk      # Static pages wrapper
└── post.njk      # Blog post wrapper
```

### Base Layout Features
- Semantic HTML5 structure
- Skip navigation link
- Accessible navigation menu
- SEO meta tags
- Social media cards

### Creating New Templates
1. Add to `src/_includes/layouts/`
2. Register in `.eleventy.js`:
   ```javascript
   eleventyConfig.addLayoutAlias("custom", "layouts/custom.njk");
   ```
3. Use in frontmatter: `layout: custom`

### Template Variables
Available in all templates:
- `site.*` - Global site data
- `page.*` - Current page metadata
- `content` - Page content
- `title` - Page title
- `date` - Page date

---

## 🏗️ Development Workflow (~600 tokens)

### Local Development
```bash
# Install dependencies
npm install

# Start dev server
npm run serve
# → http://localhost:8080

# Production build
npm run build
# → Output in _site/
```

### Adding Content
1. **New Post:** Create `src/posts/yyyy-mm-dd-title.md`
2. **New Page:** Create `src/pages/pagename.md`
3. **Update Menu:** Edit `src/_includes/layouts/base.njk`

### Git Workflow
```bash
# Feature branch
git checkout -b feature/new-post

# Make changes
git add -A
git commit -m "feat: add new post about X"

# Push and create PR
git push origin feature/new-post
```

---

## 🔗 Quick References

### Essential Files
```
.eleventy.js         # Config - build settings
package.json         # Dependencies and scripts
src/_data/site.json  # Global site data
src/index.njk        # Homepage
README.md           # Project documentation
```

### Key URLs
- **Live Site:** https://williamzujkowski.github.io/
- **GitHub:** https://github.com/williamzujkowski/williamzujkowski.github.io
- **Actions:** https://github.com/williamzujkowski/williamzujkowski.github.io/actions
- **Standards:** [Integrated via submodule]

### NPM Scripts
```json
{
  "build": "eleventy",
  "serve": "eleventy --serve",
  "debug": "DEBUG=* eleventy"
}
```

---

## 🎯 Task-Specific Guides

### Quick Tasks
- **Update copyright year:** Edit `src/_data/site.json`
- **Change site title:** Edit `src/_data/site.json`
- **Add navigation item:** Edit `src/_includes/layouts/base.njk`
- **Update CSS:** Edit `src/assets/css/main.css`

### Complex Tasks
For complex tasks, load these specific sections:
- **Redesign:** `styling-architecture` + `templates`
- **Add features:** `eleventy-config` + `development-workflow`
- **Performance:** `troubleshooting` + `github-actions`
- **Migration:** Full document scan recommended

---

## 📈 Performance Metrics

**Build Performance:**
- Initial build: ~0.06s
- Incremental: ~0.02s
- Total files: ~5-10

**Runtime Performance:**
- No client JS required
- CSS: ~3KB (unminified)
- HTML: ~2-5KB per page
- Total page weight: <50KB

**Optimization Opportunities:**
- [ ] Minify CSS/HTML
- [ ] Add image optimization
- [ ] Implement CSS purging
- [ ] Add service worker

---

## 🤝 Integration with Standards

### Standards Router
For comprehensive standards guidance, use: **[.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md)**

### Applied Standards
This repository implements the following standards from the submodule:

#### Primary Standards
- **KM** (Knowledge Management): Documentation structure and AI optimization
- **FE** (Frontend & Mobile): Component architecture, performance optimization
- **WD** (Web Design & UX): Design principles, typography, accessibility
- **SEO** (SEO & Web Marketing): Technical SEO, meta tags, structured data
- **CONT** (Content Standards): Writing guidelines, content governance
- **GH** (GitHub Platform): GitHub Pages deployment, Actions workflows

#### Supporting Standards
- **CS** (Coding Standards): JavaScript/TypeScript patterns
- **TS** (Testing Standards): Build verification
- **SEC** (Security): GitHub Pages security model
- **TOOL** (Toolchain): Development tools configuration

### Standards Commands
```bash
# Load frontend standards for Eleventy
@load FE:architecture + FE:performance

# Load web design standards
@load WD:visual-design + WD:typography

# Load SEO optimization
@load SEO:technical + SEO:on-page

# Load GitHub Pages deployment
@load GH:pages + GH:actions

# Load content guidelines
@load CONT:writing + CONT:seo
```

---

## 📚 Standards Application Guide

### Quick Reference for Eleventy Sites
```
# Initial setup
@load FE:architecture + GH:pages + TOOL:javascript

# Design implementation
@load WD:* + FE:responsive + SEO:technical

# Content creation
@load CONT:* + SEO:on-page + KM:documentation

# Deployment
@load GH:actions + GH:pages + SEC:github
```

### Natural Language Queries
Use these patterns with the standards router:
- "How to optimize Eleventy performance" → Loads FE:performance + SEO:core-web-vitals
- "Best practices for blog posts" → Loads CONT:writing + SEO:content
- "Setting up GitHub Pages" → Loads GH:pages + GH:actions
- "Accessibility checklist" → Loads WD:accessibility + FE:accessibility

---

**Note:** This document follows the Knowledge Management Standards (KM) for AI-optimized documentation. For comprehensive standards guidance, always refer to [.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md).