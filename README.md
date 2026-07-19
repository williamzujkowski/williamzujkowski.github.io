# williamzujkowski.github.io

**Type:** Personal Website & Technical Blog

Personal website of William Zujkowski, built with [Astro](https://astro.build/) and [Svelte](https://svelte.dev/), styled with hand-written CSS on the Remarque design-token system, and hosted on GitHub Pages. 80+ blog posts about security, AI/ML, homelab projects, and career development, plus a projects portfolio.

> **For Development Standards**: See [AGENTS.md](AGENTS.md) — the authoritative source for all standards and workflows. `CLAUDE.md` imports it.

## Quick Start

### Prerequisites

- Node.js 22+ and [pnpm](https://pnpm.io/)
- [UV](https://docs.astral.sh/uv/) for the Python link-validation scripts
- Git

### Installation

```bash
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io/astro-site
pnpm install
pnpm dev
```

The site will be available at `http://localhost:4321/` with hot module replacement.

### Development Commands

```bash
# From astro-site/ directory:
pnpm dev            # Start Astro dev server (localhost:4321)
pnpm build          # Production build (Astro + Pagefind search index) → dist/
pnpm preview        # Preview production build locally
pnpm check          # Astro type checking
pnpm test:e2e       # Playwright smoke + a11y suites
pnpm audit          # Remarque design audits (contrast, typography, colors, APCA)
```

## Features

- **Technical Blog**: 80+ posts about security, AI/ML, homelab, and career development
- **Interactive Features**: Tag navigation, Pagefind search, related posts, series navigation
- **Dark Mode**: Automatic theme switching with manual toggle and localStorage persistence
- **SEO**: Canonical URLs, Open Graph (per-post generated OG cards), Twitter Cards, JSON-LD, sitemap
- **Security Headers**: meta CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy
- **Accessibility**: Semantic HTML, ARIA, skip-to-content, axe-tested in CI
- **CI/CD**: GitHub Actions for build, design audits, a11y, compliance, link monitoring, deployment

## Project Structure

```
├── src/                    # Content collections (loaded by astro-site)
│   ├── posts/              # Blog posts (Markdown)
│   └── projects/           # Project entries (Markdown)
├── astro-site/             # Website source (Astro 6 + Svelte 5)
│   ├── src/
│   │   ├── components/     # Svelte & Astro components
│   │   ├── content.config.ts  # Collection schemas (point at ../src/posts, ../src/projects)
│   │   ├── layouts/        # Page layouts
│   │   ├── pages/          # Route pages
│   │   └── styles/         # Hand-written CSS (Remarque design tokens)
│   ├── public/             # Static assets
│   └── astro.config.mjs    # Astro configuration
├── scripts/                # Python tooling (link validation, blog audit)
├── gists/                  # Local source-of-truth for published gists
├── docs/                   # Research notes and pipeline docs
└── .github/workflows/      # CI/CD (7 workflows — see AGENTS.md)
```

## Technologies

- **Static Site Generator**: [Astro 6](https://astro.build/) with Svelte 5 islands
- **Styling**: Hand-written CSS, Remarque design tokens (OKLCH), no framework
- **Search**: [Pagefind](https://pagefind.app/) (static search index)
- **Python Tooling**: Link validation CI scripts managed with UV
- **CI/CD**: GitHub Actions (build, deploy, design audits, a11y, compliance, link monitoring)
- **Hosting**: GitHub Pages

## Content Management

### Creating a New Post

1. Create a Markdown file in `src/posts/` (repo root) named `YYYY-MM-DD-slug.md`
2. Add front matter:

```yaml
---
title: Your Post Title
date: 2026-01-15
description: Brief description of your post
tags: [security, tutorial]
---
```

3. Write your content in Markdown; run the `blog-pre-publish` skill before committing (see AGENTS.md)
4. The post appears in the listing with reading time, tags, and a generated OG card

## Deployment

The site deploys to GitHub Pages on push to `main`. Every push/PR also runs design audits, a11y tests, and compliance checks; link health runs on a daily schedule. See the QA pipeline in [AGENTS.md](AGENTS.md).

## License

MIT — see the LICENSE file.

## Links

- **Live Site**: https://williamzujkowski.github.io
- **Standards**: https://github.com/williamzujkowski/standards
