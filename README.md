# williamzujkowski.github.io

**Last Updated:** 2026-03-12
**Status:** Active
**Type:** Personal Website & Technical Blog

Personal website of William Zujkowski, built with [Astro](https://astro.build/) and [Svelte](https://svelte.dev/), styled with [Tailwind CSS](https://tailwindcss.com/), and hosted on GitHub Pages. Features 71 blog posts about security, AI/ML, homelab projects, and career development. Showcases personal open-source projects and 15+ years of cybersecurity expertise. Includes tag-based navigation, search, social sharing, reading progress indicator, hero images, and PWA support.

> **For Development Standards**: See [CLAUDE.md](CLAUDE.md) (v4.2.0) - authoritative source for all standards and workflows.
> **For AI Assistants**: Start with [CLAUDE.md](CLAUDE.md) then load modules from `docs/context/`.

## Quick Start

### Prerequisites

- Node.js 22+ and npm
- [UV](https://docs.astral.sh/uv/) (Rust-based Python package manager) for Python scripts
- Git

### Installation

```bash
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io/astro-site
npm install
npm run dev
```

The site will be available at `http://localhost:4321/` with hot module replacement.

### Build for Production

```bash
cd astro-site
npm run build
```

The static site will be generated in the `astro-site/dist/` directory.

### Development Commands

```bash
# From astro-site/ directory:
npm run dev            # Start Astro dev server (localhost:4321)
npm run build          # Production build (Astro + Pagefind search index)
npm run preview        # Preview production build locally
npm run check          # Run Astro type checking
```

## Features

- **Technical Blog**: 71 posts about security, AI/ML, homelab, and career development
- **Professional Pages**: About, projects portfolio, resources, uses, and stats dashboard
- **Interactive Features**: Tag navigation, Pagefind search, social sharing, related posts, reading progress
- **Dark Mode**: Automatic theme switching with manual toggle and localStorage persistence
- **SEO Optimized**: Canonical URLs, Open Graph, Twitter Cards, structured data (JSON-LD), sitemap
- **Security Headers**: Content Security Policy, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- **PWA Support**: Web App Manifest, installable on mobile devices
- **Responsive Design**: Mobile-first approach with Tailwind CSS 4
- **Performance**: Static site generation, view transitions, prefetch, lazy loading
- **Accessibility**: Semantic HTML, ARIA attributes, skip-to-content, breadcrumbs
- **CI/CD**: GitHub Actions for build, compliance, security scanning, link monitoring, and deployment

## Project Structure

```
├── astro-site/             # Website source (Astro 6 + Svelte 5)
│   ├── src/
│   │   ├── components/     # Svelte & Astro components
│   │   ├── content/        # Content collections (blog posts)
│   │   ├── layouts/        # Page layouts (BaseLayout.astro)
│   │   ├── pages/          # Route pages (about, posts, projects, etc.)
│   │   └── styles/         # Global CSS (Tailwind 4)
│   ├── public/             # Static assets (images, fonts, manifest)
│   ├── astro.config.mjs    # Astro configuration
│   └── package.json        # Node.js dependencies
├── scripts/                # Link validation CI pipeline (8 Python scripts)
│   ├── lib/               # Shared logging module
│   └── link-validation/   # Citation and link health checking
├── tests/                  # Test suites (unit JS tests)
├── docs/                   # Documentation (policies, research, link-validation)
├── .github/workflows/      # CI/CD pipelines (4 workflows)
└── nexus-agents.yaml       # AI agent orchestration config
```

## Technologies

- **Static Site Generator**: [Astro 6](https://astro.build/) with Svelte 5 islands
- **Styling**: Tailwind CSS 4 with Typography plugin
- **Search**: [Pagefind](https://pagefind.app/) (static search index)
- **Charts**: D3.js for stats visualization
- **Python Tooling**: Link validation CI scripts managed with UV
- **AI Orchestration**: nexus-agents for multi-agent workflows
- **CI/CD**: GitHub Actions (build, deploy, compliance, link monitoring)
- **Hosting**: GitHub Pages

## Content Management

### Creating a New Post

1. Create a new Markdown file in `astro-site/src/content/blog/` (or `astro-site/src/pages/posts/`)
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

## Deployment

The site automatically deploys to GitHub Pages when changes are pushed to `main`. PRs run compliance checks (build, links, Lighthouse, HTML validation, security scan).

## Configuration

- **Astro Config**: `astro-site/astro.config.mjs` (integrations, prefetch, syntax highlighting)
- **TypeScript**: `astro-site/tsconfig.json` (strict mode, path aliases)
- **Tailwind CSS**: CSS-only config via `@tailwindcss/vite` plugin
- **Standards**: `.claude-rules.json` and [CLAUDE.md](CLAUDE.md)

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Development standards and AI assistant configuration
- **[docs/research/](docs/research/)** - Research notes and blog optimization reports
- **[docs/link-validation/](docs/link-validation/)** - Link validation pipeline documentation

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Links

- **Live Site**: https://williamzujkowski.github.io
- **Standards**: https://github.com/williamzujkowski/standards
- **Astro Docs**: https://docs.astro.build/
