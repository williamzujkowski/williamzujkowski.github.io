# Website Documentation

This directory contains comprehensive documentation for William Zujkowski's personal website. It is organized into several sections for easier navigation.

## Documentation Structure

- **Guides**: Step-by-step instructions for common tasks
- **Reference**: Detailed reference material and specifications
- **Development**: Information for developers contributing to the site

## Guides

- [Blog Workflow](./guides/BLOG-WORKFLOW.md): Step-by-step process for creating and publishing blog posts
- [Blog Post Templates](./guides/BLOG-POST-README.md): Templates and examples for blog posts
- [Theme System](./guides/THEME-SYSTEM.md): Comprehensive documentation on the OKLCH-based theme system

## Reference

- [Maintenance Guide](./reference/MAINTENANCE.md): Complete guide to maintaining and updating the website
- [Changelog](./reference/CHANGELOG.md): History of changes to the website
- [Update History](./reference/UPDATES.md): Detailed update logs

## Development

- [Claude AI Guidelines](./development/CLAUDE.md): Guidelines for AI assistance with this codebase
- [Contributing](./development/CONTRIBUTING.md): Guidelines for contributing to the project

## Project Organization

The website is built with the following technologies:

- **Eleventy 3.0**: Static site generator
- **Tailwind CSS 3.4.1**: Utility-first CSS framework
- **Node.js & npm**: Development environment

### Key Directories

- `/src/`: Source files (templates, posts, CSS, JS)
- `/_site/`: Build output directory (generated)
- `/assets/`: Static assets (images, icons, data)
- `/config/`: Configuration files
- `/scripts/`: Build scripts
- `/tools/`: Utility scripts
- `/docs/`: Technical documentation

### Configuration

The site uses a modular configuration system:

- Main Eleventy config: `config/.eleventy.simple.cjs`
- PostCSS config: `config/postcss.config.cjs` 
- Tailwind config: `config/tailwind.config.cjs`
- Site config: `src/_data/config/` (modular JSON files)

## Utility Scripts

The site includes several helpful utility scripts:

### CSS Tools

- `npm run extract:components`: Extract CSS components into separate files
- `npm run extract:components:dry`: Preview component extraction without making changes

### Validation Tools

- `npm run validate:links`: Check external links for validity
- `npm run validate:config`: Verify configuration file integrity
- `npm run validate:all`: Run all validation checks
- `npm run fix:config`: Automatically fix configuration issues when possible

### Theme Tools

- `npm run generate:theme`: Generate a new theme file

### Content Processing

- `npm run process:posts`: Process blog posts from the new_posts directory

## Build Commands

- `npm run build`: Full build (data, Eleventy, CSS)
- `npm run dev` or `npm run serve`: Start development server
- `npm run build:css`: Build CSS with PostCSS only
- `npm run debug`: Run Eleventy with debug output
- `npm run build:prod`: Production build with environment flag

## Contributing

When contributing to the project, please refer to the [CONTRIBUTING.md](../CONTRIBUTING.md) file in the root directory.