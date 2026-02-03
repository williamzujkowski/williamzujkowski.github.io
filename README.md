# williamzujkowski.github.io

**Last Updated:** 2026-02-02
**Status:** Active
**Type:** Personal Website & Technical Blog

Personal website of William Zujkowski, built with [Eleventy](https://www.11ty.dev/), styled with [Tailwind CSS](https://tailwindcss.com/), and hosted on GitHub Pages. Features 71 blog posts about security, AI/ML, homelab projects, and career development. Showcases personal open-source projects and 15+ years of cybersecurity expertise. Includes tag-based navigation, search, social sharing, reading progress indicator, hero images, and PWA support.

> **For Development Standards**: See [CLAUDE.md](CLAUDE.md) (v4.2.0) - authoritative source for all standards and workflows.
> **For AI Assistants**: Start with [CLAUDE.md](CLAUDE.md) then load modules from `docs/context/`.

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- [UV](https://docs.astral.sh/uv/) (Rust-based Python package manager) for Python scripts
- Git

### Installation

```bash
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io
npm install
npm run serve
```

The site will be available at `http://localhost:8080/` with live CSS updates.

### Build for Production

```bash
npm run build
```

The static site will be generated in the `_site` directory with minified CSS and bundled JS.

### Development Commands

```bash
npm run serve          # Start dev server with CSS watching
npm run build          # Production build (CSS + Eleventy + JS bundle + stats)
npm run build:css      # Build CSS only
npm run build:js       # Bundle and minify JavaScript
npm run build:stats    # Generate blog quality dashboard
npm run test           # Run unit tests
npm run test:all       # Run all tests (unit + integration + e2e)
npm run validate:km    # Validate Knowledge Management standards
```

## Features

- **Technical Blog**: 71 posts about security, AI/ML, homelab, and career development
- **Professional Pages**: Experience timeline, skills matrix, project portfolio, uses, resources, and style guide
- **Interactive Features**: Tag navigation, blog search, social sharing, related posts, reading progress
- **Dark Mode**: Automatic theme switching with manual toggle and dynamic theme-color
- **SEO Optimized**: Extended meta descriptions, structured data, git-based dates, tag pages
- **PWA Support**: Web App Manifest, installable on mobile devices
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Performance**: Static site, lazy loading, JS bundling with tree-shaking, cached build filters
- **Accessibility**: Semantic HTML, ARIA attributes, WCAG AA compliance
- **CI/CD**: GitHub Actions for build, compliance, security scanning, link monitoring, and deployment

## Project Structure

```
├── src/                    # Source files
│   ├── _includes/         # Templates and layouts
│   │   └── layouts/       # Page layouts (base, page, post)
│   ├── _data/            # Global data files (site.json, blogStats.json)
│   ├── assets/           # CSS, JS, images, fonts
│   ├── pages/            # Static pages
│   ├── posts/            # Blog posts (71 articles)
│   └── index.njk         # Homepage
├── scripts/              # Automation (87 Python scripts)
│   ├── lib/             # Shared Python modules
│   ├── blog-content/    # Blog quality tools
│   ├── blog-research/   # Research automation
│   └── link-validation/ # Link health monitoring
├── tests/               # Test suites (unit, integration, e2e)
├── docs/                # Documentation
│   └── context/         # Modular context system (36 modules)
├── .github/workflows/   # CI/CD pipelines (7 workflows)
├── .eleventy.js         # Eleventy configuration
├── tailwind.config.js   # Tailwind CSS customization
└── nexus-agents.yaml    # AI agent orchestration config
```

## Technologies

- **Static Site Generator**: Eleventy 2.0 with Nunjucks templating
- **Styling**: Tailwind CSS 4.x with PostCSS, Typography and Forms plugins
- **JavaScript**: Bundled with Terser (tree-shaking, minification)
- **Python Tooling**: 87 scripts managed with UV package manager
- **AI Orchestration**: nexus-agents for multi-agent workflows
- **CI/CD**: GitHub Actions (build, compliance, standards, security, link monitoring)
- **Hosting**: GitHub Pages

## Content Management

### Creating a New Post

1. Create a new Markdown file in `src/posts/`
2. Add front matter:

```yaml
---
title: Your Post Title
date: 2026-01-15
description: Brief description of your post
tags: [security, tutorial]
---
```

3. Write your content in Markdown
4. The post will automatically appear in the posts listing with reading time, tags, and hero image

### Adding a New Page

1. Create a new file in `src/pages/` (`.md` or `.njk`)
2. Set layout, permalink, and navigation in front matter

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to `main`. All PRs run 7 CI checks (build, compliance, standards, security scan, link monitoring, Trivy).

## Configuration

- **Site Metadata**: `src/_data/site.json`
- **Eleventy Config**: `.eleventy.js` (plugins, filters, collections)
- **Tailwind CSS**: `tailwind.config.js` (colors, fonts, dark mode)
- **Standards**: `.claude-rules.json` and [CLAUDE.md](CLAUDE.md)

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Authoritative development standards (v4.2.0)
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture
- **[docs/context/INDEX.yaml](docs/context/INDEX.yaml)** - Module catalog (36 modules)
- **[MANIFEST.json](MANIFEST.json)** - Repository inventory

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Links

- **Live Site**: https://williamzujkowski.github.io
- **Standards**: https://github.com/williamzujkowski/standards
- **Eleventy Docs**: https://www.11ty.dev/docs/
