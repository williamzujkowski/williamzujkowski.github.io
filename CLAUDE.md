# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- `npm run build` - Full build (data, eleventy, CSS)
- `npm run dev` or `npm run serve` - Start dev server
- `npm run build:css` - Build CSS with PostCSS only
- `npm run build:link-previews` - Generate link preview metadata
- `npm run debug` - Run 11ty with debug output
- `npm run process:posts` - Process blog posts from new_posts/ directory
- This site uses Eleventy 3.0 and Tailwind CSS 3.4.1 - make sure all code is compatible with these versions
- Requires Node.js 20+ and npm 10+
- Changes to eleventy config should reference `config/.eleventy.simple.cjs`

## Directory Structure
- `src/` - Source files (templates, posts, CSS, JS)
- `_site/` - Build output directory
- `assets/` - Static assets (images, icons, data)
- `config/` - Configuration files
- `scripts/` - Build scripts
- `tools/` - Utility scripts
- `new_posts/` - Directory for new blog posts to be processed

## Configuration Files
- Main Eleventy config: `config/.eleventy.simple.cjs`
- Fallback Eleventy config (GitHub Actions): `.eleventy.simple.cjs`
- PostCSS config: `config/postcss.config.cjs`
- Tailwind config: `config/tailwind.config.cjs`

## Coding Style
- Use kebab-case for filenames (e.g., `my-component.njk`)
- Follow YYYY-MM-DD-title-with-hyphens.md naming for blog posts
- Include frontmatter with title, date, layout, tags in markdown files
- Add eleventyNavigation in frontmatter for navigation integration
- Use shortcodes for images: `{% image "path/to/img.jpg", "Alt text", "100vw" %}`
- Use breadcrumbs shortcode on pages: `{% breadcrumbs page %}`
- Use Tailwind CSS for styling - refer to config/tailwind.config.cjs for theme colors
- Markdown formatting: h1 for titles, h2 for sections, h3 for subsections
- Always provide alt text for images and accessibility attributes

## Useful Resources
- Eleventy documentation: https://www.11ty.dev/
- Free image sources (use with proper attribution):
  - Pixabay: https://pixabay.com/
  - Unsplash: https://unsplash.com/
  - Pexels: https://www.pexels.com/
  - Wikimedia Commons: https://commons.wikimedia.org/wiki/Main_Page