# AI Knowledge Router - williamzujkowski.github.io

**Version:** 4.5.1  
**Last Updated:** 2025-06-26  
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

**Total Tokens:** ~10,000 (estimated)  
**Primary Language:** JavaScript/Nunjucks  
**Framework:** Eleventy 2.0 + Tailwind CSS 3.0  
**Deployment:** GitHub Pages  

### Key Metrics
- **Build Time:** ~0.10 seconds (Eleventy) + ~1s (Tailwind CSS)
- **Deploy Time:** ~30 seconds via GitHub Actions
- **Content Files:** 10 pages, 8 posts
- **Standards Compliance:** Integrated via submodule
- **UI Framework:** Tailwind CSS with PostCSS pipeline
- **Navigation:** eleventy-navigation plugin for hierarchical menus
- **Professional Pages:** About (comprehensive profile), Uses, Resources
- **Blog Posts:** Security, AI/ML, career development, continuous learning

---

## 🗺️ Navigation Map

### For Site Development
| Task | Load These Sections | Standards to Apply |  
|------|---------------------|--------------------|

| Add new blog post | `content-management` + `posts-structure` | `@load CONT:writing + SEO:on-page` |
| Update styling | `tailwind-architecture` + `eleventy-config` | `@load WD:visual-design + FE:performance` |
| Fix build issues | `troubleshooting` + `github-actions` | `@load GH:actions + TOOL:javascript` |
| Add new page | `content-management` + `navigation-setup` | `@load FE:architecture + WD:ux-patterns` |
| SEO optimization | `seo-metadata` + `eleventy-config` | `@load SEO:* + CONT:seo` |
| Performance optimization | `performance-metrics` + `tailwind-architecture` | `@load FE:performance + SEO:core-web-vitals` |
| Accessibility improvements | `templates` + `tailwind-architecture` | `@load WD:accessibility + FE:accessibility` |
| Dark mode customization | `tailwind-architecture` + `templates` | `@load WD:visual-design + FE:responsive` |
| Navigation updates | `navigation-setup` + `content-management` | `@load WD:ux-patterns + FE:architecture` |

### For Content Updates
| Content Type | Location | Template Used | Current Content |
|--------------|----------|---------------|-----------------|
| Blog Posts | `src/posts/*.md` | `post.njk` layout | 8 posts on security, AI/ML, career topics |
| Static Pages | `src/pages/*.md` | `page.njk` layout | About (comprehensive professional profile), Uses, Resources, 404 |
| Homepage | `src/index.njk` | `base.njk` layout | Hero with headshot, recent posts |
| Global Data | `src/_data/*.json` | Available everywhere | Site metadata |

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
- **Templates:** Nunjucks (.njk) with eleventy-navigation plugin
- **Styling:** Tailwind CSS 3.4 with PostCSS pipeline
- **UI Features:** Dark mode, responsive design, glass morphism effects
- **Build:** Node.js 18+, PostCSS, npm-run-all for parallel builds
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
eleventyNavigation:
  key: Page Name        # Required for navigation menu
  order: 5             # Optional: controls menu order
  parent: About        # Optional: creates hierarchy
---

Page content...
```

**Navigation Integration:**
- Pages with `eleventyNavigation` appear in menus automatically
- Supports nested navigation with `parent` key
- Breadcrumbs generated automatically
- Mobile-responsive menu included

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

## 🎨 Tailwind Architecture (~1,200 tokens)

### CSS Pipeline
- **Source:** `src/assets/css/tailwind.css`
- **Output:** `_site/assets/css/main.css`
- **Process:** PostCSS → Tailwind CSS → Autoprefixer → CSSNano (production)

### Tailwind Configuration
`tailwind.config.js` customizations:
```javascript
{
  // Extended color palette
  colors: {
    primary: {
      50-900: 'custom blue scale'
    }
  },
  // Dark mode with class strategy
  darkMode: 'class',
  // Typography plugin for prose
  plugins: [
    '@tailwindcss/typography',
    '@tailwindcss/forms'
  ]
}
```

**Key Features:**
- Dark mode toggle with system preference detection
- Glass morphism effects with backdrop-blur
- Smooth animations and transitions
- Mobile-first responsive utilities
- Custom gradient text effects
- Sticky navigation with blur

### Custom Components
```css
/* In tailwind.css */
@layer components {
  .gradient-text {
    @apply bg-gradient-to-r from-primary-600 to-primary-400 
           bg-clip-text text-transparent;
  }
  .glass-effect {
    @apply bg-white/80 dark:bg-gray-900/80 backdrop-blur-xl;
  }
}
```

---

## ⚙️ Eleventy Configuration (~1,200 tokens)

### Core Config (.eleventy.js)
```javascript
// Key configurations:
- Input: src/
- Output: _site/
- Templates: Nunjucks
- Plugins: @11ty/eleventy-navigation
- Passthrough: assets/, CNAME, .nojekyll
- Filters: readableDate, htmlDateString, limit
- Layout aliases: base, page, post
- Navigation: Hierarchical menu generation
```

### Build Scripts
```bash
npm run serve        # Dev server with CSS watching (localhost:8080)
npm run build        # Production build (CSS + Eleventy)
npm run build:css    # Build Tailwind CSS only
npm run watch:css    # Watch CSS changes
npm run validate:km  # Validate Knowledge Management standards
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

## 🧭 Navigation Setup (~800 tokens)

### eleventy-navigation Plugin
Configured in `.eleventy.js`:
```javascript
const eleventyNavigationPlugin = require("@11ty/eleventy-navigation");
eleventyConfig.addPlugin(eleventyNavigationPlugin);
```

### Adding Pages to Navigation
In frontmatter:
```yaml
eleventyNavigation:
  key: Page Name      # Required - identifies the page
  title: Menu Title   # Optional - overrides page title
  order: 5           # Optional - controls menu order
  parent: About      # Optional - creates hierarchy
```

### Navigation Features
- **Automatic Menus:** Pages with `eleventyNavigation` appear automatically
- **Breadcrumbs:** Generated based on hierarchy
- **Active States:** Current page highlighted
- **Mobile Menu:** Responsive hamburger menu
- **Nested Support:** Multi-level navigation

### Navigation Helpers
```nunjucks
{# Get all navigation items #}
{{ collections.all | eleventyNavigation }}

{# Get breadcrumb trail #}
{{ collections.all | eleventyNavigationBreadcrumb(eleventyNavigation.key) }}

{# Render as HTML #}
{{ collections.all | eleventyNavigation | eleventyNavigationToHtml(options) }}
```

---

## 🔗 Quick References

### Essential Files
```
.eleventy.js         # Config - build settings, navigation plugin
package.json         # Dependencies and scripts
tailwind.config.js   # Tailwind customizations
postcss.config.js    # PostCSS pipeline config
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
  "build:css": "postcss src/assets/css/tailwind.css -o _site/assets/css/main.css",
  "build:eleventy": "eleventy",
  "build": "npm run build:css && npm run build:eleventy",
  "watch:css": "postcss src/assets/css/tailwind.css -o _site/assets/css/main.css --watch",
  "watch:eleventy": "eleventy --serve",
  "serve": "npm-run-all --parallel watch:*"
}
```

---

## 🎯 Task-Specific Guides

### Quick Tasks
- **Update copyright year:** Edit `src/_data/site.json`
- **Change site title:** Edit `src/_data/site.json`
- **Add navigation item:** Add `eleventyNavigation` to page frontmatter
- **Update Tailwind theme:** Edit `tailwind.config.js`
- **Toggle dark mode:** Click moon/sun icon in header
- **Add custom CSS:** Edit `src/assets/css/tailwind.css` with @layer

### Complex Tasks
For complex tasks, load these specific sections:
- **Redesign:** `tailwind-architecture` + `templates`
- **Add features:** `eleventy-config` + `navigation-setup`
- **Performance:** `tailwind-architecture` + `performance-metrics`
- **Dark mode customization:** `tailwind-architecture` + `templates`
- **Navigation structure:** `navigation-setup` + `content-management`
- **Migration:** Full document scan recommended

---

## 📈 Performance Metrics

**Build Performance:**
- Eleventy build: ~0.06s
- Tailwind CSS build: ~1s
- Incremental: ~0.02s (Eleventy) + ~0.5s (CSS)
- Total files: ~5-10

**Runtime Performance:**
- Minimal client JS (dark mode toggle only)
- CSS: ~25KB minified (Tailwind utilities)
- HTML: ~5-10KB per page
- Total page weight: <100KB

**Optimization Implemented:**
- ✅ CSS minified in production (cssnano)
- ✅ HTML semantic and accessible
- ✅ Responsive images ready
- ✅ Dark mode with no flash
- ✅ Smooth animations with will-change

**Future Optimizations:**
- [ ] Implement Tailwind CSS purging
- [ ] Add image optimization pipeline
- [ ] Implement service worker
- [ ] Add resource hints (preconnect, prefetch)

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

## 📊 Changelog

### [4.5.1] - 2025-06-26
#### Changed
- Updated homepage with AI interest section and Asimov quote
- Removed vestigial contact.md and projects.md pages (had permalink: false)
- Fixed internal link in uses.md to point to /about/#contact
- Updated documentation to reflect current page structure

#### Removed
- Deleted duplicate contact.md and projects.md pages that were inactive
- These pages had permalink: false and were replaced by the consolidated About page

### [4.5.0] - 2025-06-25
#### Added
- Enhanced structured data for better SEO (Person, BlogPosting, BreadcrumbList)
- Lazy loading for images with automatic filter
- Resource hints (preconnect, dns-prefetch) for performance
- Improved accessibility with better focus states and reduced motion support
- Breadcrumb structured data

#### Changed
- Enhanced site.json with comprehensive metadata and social links
- Updated structured data to include dateModified with git last modified dates
- Improved keyboard navigation with enhanced focus styles
- Added support for prefers-reduced-motion media query

### [4.4.0] - 2025-06-25
#### Changed
- Combined Experience, Skills, and Projects pages into a single comprehensive About page
- Implemented redirect pages from old URLs to new About page sections
- Improved information architecture following UX best practices
- Better SEO through consolidated professional content

### [4.3.0] - 2025-06-25
#### Added
- Search functionality for blog posts (client-side JavaScript)
- Social share buttons (LinkedIn, Hacker News, Reddit, copy link)
- Style Guide page documenting design system
- 4 additional blog posts on local LLM deployment and security mindset
- Custom security-themed favicon
- Git-based last updated dates for all pages
- External link security (rel="noopener noreferrer")
- Resources page with 86+ curated links

#### Changed
- Updated Projects page to focus on personal GitHub projects
- Enhanced Skills page to highlight AI/ML and Python expertise
- Removed Twitter references throughout the site
- Added AI interest section to homepage with Asimov quote
- Extended meta descriptions to 150-160 characters
- Updated page count to 10 pages and 8 blog posts

#### Technical Updates
- Implemented reading time filter (225 words per minute)
- Added gitLastModified filter using execSync
- Added externalLinks filter for automatic security attributes
- Fixed GitHub Pages deployment configuration (legacy to workflow)
- Added search.js and social sharing functions in base layout

### [4.2.0] - 2025-01-29
#### Added
- Reading time estimates for all blog posts
- Git-based last updated dates implementation
- External link security filter
- Two new blog posts on Raspberry Pi security and continuous learning
- Comprehensive Resources page with categorized links

#### Changed
- Enhanced SEO with extended meta descriptions (150-160 chars)
- Updated Projects page to focus on personal open-source projects
- Reorganized Skills page to reflect project-demonstrated technologies

### [4.1.0] - 2025-01-27
#### Added
- Professional pages documentation (Experience, Skills, Projects)
- Blog post creation and management guidance
- Current content inventory in navigation map
- OPSEC considerations for content

#### Changed
- Updated content metrics (6 pages, 4 posts)
- Revised blog post topics to focus on personal projects
- Enhanced navigation map with current content
- Updated build performance metrics

#### Technical Updates
- Removed government-specific content references
- Added personal project focus
- Updated task priorities based on completed work

### [4.0.0] - 2024-01-24
#### Added
- Tailwind CSS architecture section with PostCSS pipeline details
- Navigation setup section for eleventy-navigation plugin
- Dark mode implementation guidance
- Custom Tailwind components documentation
- Parallel build scripts with npm-run-all

#### Changed
- Updated technology stack to include Tailwind CSS 3.0
- Modified styling references from vanilla CSS to Tailwind
- Enhanced build scripts section with CSS commands
- Updated performance metrics for Tailwind CSS
- Improved task navigation map with new sections

#### Technical Updates
- Build time now includes CSS processing (~1s)
- CSS size increased to ~25KB (optimized Tailwind)
- Added navigation helpers and examples
- Document tokens increased to ~10,000

---

**Note:** This document follows the Knowledge Management Standards (KM) for AI-optimized documentation. For comprehensive standards guidance, always refer to [.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md).