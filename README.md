# williamzujkowski.github.io

**Version:** 2.0.0  
**Last Updated:** 2024-01-24  
**Status:** Active  
**Type:** Personal Website

Personal website of William Zujkowski, built with [Eleventy](https://www.11ty.dev/) and hosted on GitHub Pages.

> **Note:** This repository implements comprehensive development standards via the [.standards](https://github.com/williamzujkowski/standards) submodule.
> 
> - **For AI assistants:** Use [CLAUDE.md](CLAUDE.md) for site navigation and [.standards/docs/core/CLAUDE.md](.standards/docs/core/CLAUDE.md) for standards guidance
> - **For developers:** See [Standards Implementation Checklist](docs/STANDARDS_IMPLEMENTATION_CHECKLIST.md)

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io

# Install dependencies (including Tailwind CSS)
npm install

# Start development server with hot-reload
npm run serve
```

The site will be available at `http://localhost:8080/` with live CSS updates.

### Build for Production

```bash
# Build optimized CSS and site
npm run build
```

The static site will be generated in the `_site` directory with minified CSS.

### Development Commands

```bash
npm run serve        # Start dev server with CSS watching
npm run build        # Production build
npm run build:css    # Build CSS only
npm run watch:css    # Watch CSS changes
npm run validate:km  # Validate Knowledge Management standards
```

## 📁 Project Structure

```
├── src/                    # Source files
│   ├── _includes/         # Templates and layouts
│   │   └── layouts/       # Page layouts
│   ├── _data/            # Global data files
│   ├── assets/           # CSS, JS, images
│   ├── pages/            # Static pages
│   ├── posts/            # Blog posts
│   └── index.njk         # Homepage
├── _site/                # Build output (git-ignored)
├── .eleventy.js          # Eleventy configuration
├── .github/workflows/    # GitHub Actions
├── .standards/           # Development standards (submodule)
└── package.json          # Dependencies
```

## 🛠️ Technologies

- **Static Site Generator**: Eleventy 2.0
- **Templating**: Nunjucks with eleventy-navigation
- **Styling**: Tailwind CSS 3.0 with PostCSS
- **UI Features**: Dark mode, responsive design, animations
- **Typography**: Inter font with Tailwind Typography plugin
- **Hosting**: GitHub Pages
- **CI/CD**: GitHub Actions
- **Standards**: Integrated via [standards repository](https://github.com/williamzujkowski/standards)

## 📝 Content Management

### Creating a New Post

1. Create a new Markdown file in `src/posts/`
2. Add front matter:

```yaml
---
title: Your Post Title
date: 2024-01-15
description: Brief description of your post
tags: [web-development, tutorial]  # Optional tags
---
```

3. Write your content in Markdown
4. The post will automatically appear in the posts listing

### Adding a New Page

1. Create a new file in `src/pages/`
2. Use either Markdown (`.md`) or Nunjucks (`.njk`)
3. Set the layout, permalink, and navigation in front matter:

```yaml
---
layout: page
title: Page Title
description: Page description
permalink: /page-url/
eleventyNavigation:
  key: Page Name      # Required for navigation
  order: 5           # Optional: controls menu order
  parent: About      # Optional: creates hierarchy
---
```

## 🚀 Deployment

The site automatically deploys to GitHub Pages when changes are pushed to the `main` branch.

### Manual Deployment

1. Push changes to the `main` branch
2. GitHub Actions will build and deploy the site
3. View at https://williamzujkowski.github.io

## 🔧 Configuration

### Site Metadata

Edit `src/_data/site.json` to update:
- Site title
- Description
- Author information
- URL

### Eleventy Configuration

Modify `.eleventy.js` to:
- Add plugins (eleventy-navigation included)
- Configure collections
- Set up filters
- Adjust build settings

### Tailwind CSS Customization

Edit `tailwind.config.js` to customize:
- **Colors**: Extended primary color palette
- **Fonts**: Currently using Inter font family
- **Dark Mode**: Configured with class-based toggle
- **Plugins**: Typography and Forms plugins included

Common customizations:
```javascript
// Add custom colors
colors: {
  brand: {
    50: '#your-color',
    // ... more shades
  }
}

// Add custom fonts
fontFamily: {
  sans: ['Your-Font', ...defaultTheme.fontFamily.sans],
}
```

### CSS Architecture

- **Main CSS**: `src/assets/css/tailwind.css`
- **Components**: Custom component classes using `@layer components`
- **Utilities**: Custom utilities using `@layer utilities`
- **Dark Mode**: Automatic with `.dark` class on `<html>`

## 📚 Knowledge Management

This project implements comprehensive knowledge management:

### Documentation
- **[CLAUDE.md](CLAUDE.md)** - AI-optimized interface for assistants
- **[MANIFEST.yaml](MANIFEST.yaml)** - Machine-readable metadata
- **[Content Guide](docs/guides/CONTENT_GUIDE.md)** - How to create content
- **[Documentation Standards](docs/standards/SITE_DOCUMENTATION_STANDARDS.md)** - Documentation guidelines

### Standards Integration

This project follows the guidelines from the [standards repository](https://github.com/williamzujkowski/standards), which is included as a submodule at `.standards/`.

Key standards applied:
- **KM** - Knowledge Management Standards (this README structure)
- **CS** - Coding Standards (via submodule)
- **TS** - Testing Standards (build verification)
- **SEC** - Security Standards (GitHub Pages model)

### For AI Assistants

Use these commands in CLAUDE.md:
- `@load content-management` - Learn about posts/pages
- `@load troubleshooting` - Debug issues
- `@summary` - Get quick overview

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- **Live Site**: https://williamzujkowski.github.io
- **Standards**: https://github.com/williamzujkowski/standards
- **Eleventy Docs**: https://www.11ty.dev/docs/

---

## 📊 Changelog

### [3.0.0] - 2024-01-24
#### Added
- Tailwind CSS 3.0 with PostCSS pipeline
- eleventy-navigation plugin for hierarchical navigation
- Dark mode support with system preference detection
- Responsive mobile menu
- Breadcrumb navigation
- Beautiful animations and transitions
- Glass morphism UI effects
- Social sharing buttons on posts

#### Changed
- Complete UI redesign with modern aesthetics
- Migrated from vanilla CSS to Tailwind CSS
- Enhanced navigation with automatic menu generation
- Improved typography with Tailwind Typography plugin

### [2.0.0] - 2024-01-24
#### Added
- Full integration with .standards submodule router
- Standards implementation checklist
- Applied standards: FE, WD, SEO, CONT, GH, TOOL
- Enhanced CLAUDE.md with standards commands

### [1.0.0] - 2024-01-24
#### Added
- Initial Eleventy site setup
- Knowledge Management Standards implementation
- CLAUDE.md AI interface
- MANIFEST.yaml metadata
- GitHub Actions CI/CD
- Documentation structure

---

**Note:** This README follows Knowledge Management Standards v1.0.0. For detailed documentation navigation, consult [CLAUDE.md](CLAUDE.md).