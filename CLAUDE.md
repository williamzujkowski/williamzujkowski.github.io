# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- `npm run build` - Full build (data, eleventy, CSS)
- `npm run dev` or `npm run serve` - Start dev server
- `npm run build:css` - Build CSS with PostCSS only
- `npm run debug` - Run 11ty with debug output
- Changes to eleventy config should reference `.eleventy.simple.cjs`

## Coding Style
- Use kebab-case for filenames (e.g., `my-component.njk`)
- Follow YYYY-MM-DD-title-with-hyphens.md naming for blog posts
- Include frontmatter with title, date, layout, tags in markdown files
- Add eleventyNavigation in frontmatter for navigation integration
- Use shortcodes for images: `{% image "path/to/img.jpg", "Alt text", "100vw" %}`
- Use breadcrumbs shortcode on pages: `{% breadcrumbs page %}`
- Use Tailwind CSS for styling - refer to tailwind.config.cjs for theme colors
- Markdown formatting: h1 for titles, h2 for sections, h3 for subsections
- Always provide alt text for images and accessibility attributes

## Useful Resources
- Eleventy documentation: https://www.11ty.dev/
- Free image sources (use with proper attribution):
  - Pixabay: https://pixabay.com/
  - Unsplash: https://unsplash.com/
  - Pexels: https://www.pexels.com/
  - Wikimedia Commons: https://commons.wikimedia.org/wiki/Main_Page