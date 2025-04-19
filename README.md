# William Zujkowski's Personal Website

This is my personal website and blog, built with [11ty](https://www.11ty.dev/), a simpler static site generator. The site features a GitHub-style dark theme with responsive design, blog functionality, and dynamic content integration.

## Features

- GitHub-style dark theme with responsive design
- Blog with markdown support and tag filtering
- Configurable homepage with customizable sections
- Links page with categorized resources in a grid layout
- Rich link previews with metadata using metascraper
- GitHub repository pinning and showcase
- arXiv research papers feed showing latest AI/ML and cybersecurity papers
- Social media integration
- RSS feed
- Automated blog post processing and publishing workflow
- Link validation and management tools
- Optimized build system with incremental builds and parallel processing
- Smart data management with caching and payload optimization
- Responsive image optimization and delivery

## Documentation

All documentation has been consolidated in the `docs/` directory for better organization:

### Guides

- [Blog Workflow](docs/guides/BLOG-WORKFLOW.md) - Instructions for creating and publishing blog posts
- [Blog Post Templates](docs/guides/BLOG-POST-README.md) - Templates and examples for blog posts
- [Theme System](docs/guides/THEME-SYSTEM.md) - Guide to the site's OKLCH-based theming system

### Reference

- [Maintenance Guide](docs/reference/MAINTENANCE.md) - Complete guide to maintaining and updating the website
- [Changelog](docs/reference/CHANGELOG.md) - History of changes to the website
- [Update History](docs/reference/UPDATES.md) - Detailed update logs

### Development

- [Claude AI Guidelines](docs/development/CLAUDE.md) - Guidelines for AI assistance with this codebase
- [Contributing](docs/development/CONTRIBUTING.md) - Guidelines for contributing to the project
- [Link Previews](docs/development/LINK-PREVIEWS.md) - How link previews are generated and managed
- [Data Management](docs/guides/DATA-MANAGEMENT.md) - Smart data management system documentation

#### Using Claude AI

This project is configured to work with Claude.ai/code assistance. When using Claude with this repository:

1. Claude will automatically reference the guidelines in the `CLAUDE.md` file
2. This provides Claude with important context about build commands, directory structure, and coding standards
3. For best results, point Claude to the documentation files in the `/docs` directory

## Project Structure

```
williamzujkowski.github.io/
├── _data/               # Global data files
├── _includes/           # Include templates
├── _layouts/            # Layout templates
├── _site/               # Build output directory
├── assets/              # Static assets
│   ├── data/            # Data assets (screenshots, etc.)
│   ├── icons/           # Site icons
│   └── images/          # Site images
├── config/              # Configuration files
│   ├── .eleventy.cjs
│   ├── .eleventy.simple.cjs
│   ├── postcss.config.cjs
│   └── tailwind.config.cjs
├── docs/                # Documentation
│   ├── development/     # Development guides
│   ├── guides/          # User guides
│   └── reference/       # Reference documentation
├── new_posts/           # Directory for new blog posts
│   └── processed/       # Processed posts archive
├── scripts/             # Scripts and utilities
│   ├── bin/             # CLI utilities and entry points
│   ├── build/           # Build scripts for data generation
│   ├── content/         # Content management tools
│   │   ├── blog/        # Blog post management
│   │   └── links/       # Link management
│   ├── screenshots/     # Screenshot generation tools
│   ├── styling/         # Styling tools
│   ├── utils/           # Utility scripts
│   └── validation/      # Validation tools
├── src/                 # Source files
│   ├── _data/           # Site configuration data
│   ├── _includes/       # Template includes
│   ├── _layouts/        # Template layouts
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── posts/           # Blog posts
```

For a detailed overview of the scripts organization, see [Scripts Documentation](docs/development/SCRIPTS.md).

## Development

To work on this site locally:

1. Clone the repository
2. Install dependencies: `npm install`
3. Start the development server:

   ```bash
   # Using npm script
   npm run dev

   # Or using the CLI utility
   ./scripts/bin/dev.sh serve
   ```

4. Visit `http://localhost:8082` in your browser

Other development commands:

```bash
# Watch CSS files for changes
./scripts/bin/dev.sh css

# Run with debug output
./scripts/bin/dev.sh debug

# Lint JavaScript files
./scripts/bin/dev.sh lint

# Format files with Prettier
./scripts/bin/dev.sh format
```

## Build

To build the site for production:

```bash
# Using npm script (standard build)
npm run build

# Using optimized build system
npm run build:optimized

# Or using the CLI utility
./scripts/bin/build.sh all
```

Other build commands:

```bash
# Build only data files
./scripts/bin/build.sh data

# Build only CSS
./scripts/bin/build.sh css

# Build site without rebuilding data
./scripts/bin/build.sh site

# Production build with optimizations
npm run build:prod

# Debug build with detailed output
npm run build:optimized:debug

# Force rebuild everything (ignore cache)
npm run build:optimized:force

# Optimize data files only
npm run optimize:data
```

The built site will be in the `_site` directory.

### Optimized Build System

The site includes an advanced build system with:

1. **Parallel Processing** - Runs multiple build tasks simultaneously where possible
2. **Incremental Builds** - Only rebuilds what has changed to improve performance
3. **Smart Caching** - Reduces redundant operations using intelligent cache management
4. **Comprehensive Monitoring** - Provides detailed timing and progress feedback

For development with the optimized build system:

```bash
# Start dev server with optimized builds
npm run dev:optimized
```

## Site Configuration

The majority of site configuration is managed through JSON files in the `src/_data` directory.

### Main Configuration (site.json)

The `site.json` file contains the primary configuration for the website:

```json
{
  "title": "Your Name",
  "description": "Personal website and technology blog",
  "url": "https://yourdomain.com",
  "author": "Your Name",
  "email": "your.email@example.com",
  "theme": "system",
  "seo": { ... },
  "homepage": { ... },
  "social_media": [ ... ],
  "navigation": [ ... ],
  "linkGroups": [ ... ],
  "links": [ ... ],
  "blog": { ... }
}
```

### Homepage Configuration

The homepage is highly customizable through the `homepage` section in `site.json`:

```json
"homepage": {
  "welcome_heading": "Welcome",
  "welcome_subtitle": "IT Engineer & Technology Enthusiast",
  "about_me_title": "About Me",
  "about_me_content": "Your bio text here...",
  "show_recent_posts": true,
  "recent_posts_count": 3,
  "show_activity_timeline": false,
  "show_github_pins": true,
  "show_github_repos_on_links": false,
  "show_arxiv_papers": true,
  "pinned_repositories": [ ... ],
  "skills": [ ... ],
  "interests": "Your interests text here..."
}
```

Toggle features on/off by changing the boolean values:

- `show_recent_posts`: Display recent blog posts
- `show_activity_timeline`: Show the blog post activity timeline
- `show_github_pins`: Display pinned GitHub repositories on homepage
- `show_github_repos_on_links`: Display GitHub repositories on links page
- `show_arxiv_papers`: Show the arXiv papers section

### Navigation

Site navigation is configured in the `navigation` array:

```json
"navigation": [
  { "name": "Home", "url": "/", "icon": "" },
  { "name": "Links", "url": "/links/", "icon": "" },
  { "name": "Blog", "url": "/blog/", "icon": "" }
]
```

Add, remove, or modify navigation items by editing this array.

### Social Media Links

Social media profiles are configured in the `social_media` array:

```json
"social_media": [
  {
    "name": "GitHub",
    "url": "https://github.com/yourusername",
    "icon": "<svg>...</svg>",
    "enabled": true,
    "display_on_home": false,
    "display_in_header": true,
    "display_in_footer": true
  },
  // Additional social profiles...
]
```

For each social profile, you can control:

- `enabled`: Whether the profile is active
- `display_on_home`: Show on homepage
- `display_in_header`: Show in site header
- `display_in_footer`: Show in site footer

### Links Page

The links page is organized by categories defined in `linkGroups` and populated from the `links` array:

```json
"linkGroups": [
  { "name": "Social", "icon": "🔗" },
  { "name": "Projects", "icon": "💻" },
  // Additional categories...
],
"links": [
  {
    "name": "GitHub",
    "url": "https://github.com/yourusername",
    "group": "Social",
    "icon": "GitHub"
  },
  // Additional links...
]
```

Each link must have a `group` that corresponds to one of the defined `linkGroups`.

### Blog Configuration

Blog settings are managed in the `blog` section:

```json
"blog": {
  "postsPerPage": 5,
  "showDates": true,
  "dateFormat": "%B %d, %Y"
}
```

## Content Management

### Blog Posts

#### Option 1: Automated Blog Post Processing

The recommended way to add blog posts is using our automated processing system:

1. Create a file in the `new_posts/` directory using either:

   - A `.txt` file with the title on the first line
   - A `.md` file with an H1 header or front matter for the title

2. Run the processing script:

   ```bash
   # Using npm script
   npm run process:posts

   # Or using the CLI utility
   ./scripts/bin/content.sh blog:process
   ```

3. The script will:
   - Format the post with proper frontmatter
   - Schedule it appropriately (10-14 days after the most recent post)
   - Add appropriate tags based on content analysis
   - Suggest relevant images
   - Place the final post in `src/posts/`

For detailed instructions, see [BLOG-WORKFLOW.md](docs/guides/BLOG-WORKFLOW.md).

#### Option 2: Manual Blog Post Creation

You can also manually create posts as markdown files in the `src/posts` directory. Each post should include front matter at the top:

```markdown
---
title: Your Post Title
date: 2024-07-15
description: A brief description of your post
tags: ["tag1", "tag2"]
image: /assets/images/blog/your-post-image.jpg
---

Your post content here...
```

Required front matter:

- `title`: The post title
- `date`: Publication date (YYYY-MM-DD format)

Optional front matter:

- `description`: Brief summary of the post
- `tags`: Array of relevant tags
- `image`: Featured image path

### Adding Images

Store images in the `assets/images` directory:

- Blog post images: `assets/images/blog/`
- General site images: `assets/images/`

## GitHub Pins

To update the GitHub repository pins, edit the `homepage.pinned_repositories` array in `site.json` or run:

```
npm run build:github-pins
```

This fetches public repository information for the specified GitHub username.

## arXiv Integration

The site includes an integration with arXiv to fetch and display recent AI/ML and cybersecurity research papers. The integration:

1. Fetches papers from the arXiv API (cs.AI, cs.LG, and cs.CR categories)
2. Categorizes papers by AI/ML and Cybersecurity
3. Displays the most recent paper from each category on the homepage

To update the arXiv feed:

```
npm run build:arxiv
```

## Styling

The site uses Tailwind CSS for styling. Main CSS files:

- `src/css/styles.css`: Main stylesheet
- `tailwind.config.cjs`: Tailwind configuration

## Deployment

The site is configured for GitHub Pages deployment. When you push to the repository, GitHub Actions will automatically build and deploy the site.

## Link Preview System

The site features a link preview system that enhances the links page with rich metadata:

- During the build process, `link-preview-generator.js` extracts metadata for external links
- The data includes page titles, descriptions, author information, and publication dates
- This data is stored as JSON and used by the templates to display rich link previews
- The system is designed to be lightweight and efficient, without requiring screenshots

For detailed information about the link preview system, see [Link Previews](docs/development/LINK-PREVIEWS.md)

### Link Preview Generation

The site includes a metadata-based link management system that handles:

- Generating metadata for links (title, description, author, etc.)
- Validating link health
- Organizing links by category

Available commands:

```bash
# Generate or update link previews
npm run build:link-previews

# Or using the shell script directly
./scripts/rebuild-link-previews.sh
```

For detailed instructions on link management, see [MAINTENANCE.md](docs/reference/MAINTENANCE.md).

### How Link Preview Generation Works

1. **Metadata Extraction**: The system uses `metascraper` to extract rich metadata from each link URL.

2. **Data Storage**: The extracted metadata is stored in JSON files:

   - `_data/link-previews.json` - Master file with all link previews
   - `assets/data/link-previews.json` - Copy for the built site
   - `assets/data/link-previews-{category}.json` - Category-specific preview files

3. **Integration**: The data is integrated into the site configuration during build and used in the templates to display rich link information.

The tooling uses:

- `metascraper` for metadata extraction
- Various metascraper plugins for specific types of metadata (author, date, description, etc.)
- The `got` library for HTTP requests

## License

MIT
