# William Zujkowski's Personal Website

This is my personal website and blog, built with [11ty](https://www.11ty.dev/), a simpler static site generator. The site features a GitHub-style dark theme with responsive design, blog functionality, and dynamic content integration.

## Features

- GitHub-style dark theme with responsive design
- Blog with markdown support and tag filtering
- Configurable homepage with customizable sections
- Links page with categorized resources in a grid layout
- Rich link previews with metadata and screenshots using Microlink
- GitHub repository pinning and showcase
- arXiv research papers feed showing latest AI/ML and cybersecurity papers
- Social media integration
- RSS feed
- Automated blog post processing and publishing workflow
- Link validation and management tools

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
- [Link Screenshots](docs/reference/LINK-SCREENSHOTS.md) - How website screenshots for links are generated and used

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
# Using npm script
npm run build

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
./scripts/bin/build.sh production
```

The built site will be in the `_site` directory.

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
tags: ['tag1', 'tag2']
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

## Microlink Integration

The site uses Microlink's open source tools to enhance link previews:

- During the build process, `build-link-previews.js` generates screenshots and extracts metadata for external links
- The script is designed to process new links and update the 20 oldest links on each build
- This data is stored as JSON and used by the frontend to display rich link previews
- In case pre-generated data is unavailable, the site falls back to using the Microlink API in real-time
- You can also use `tools/generate-test-screenshots.js` to manually generate screenshots for testing

For detailed information about how website screenshots work, see [Link Screenshots](docs/reference/LINK-SCREENSHOTS.md)

### Link Preview Generation

The site includes a comprehensive link management system that handles:
- Generating metadata for links (title, description, author, etc.)
- Creating screenshots of linked websites
- Validating link health
- Managing incremental updates to minimize processing time

Available commands:

```bash
# Initial setup (generates previews for all links)
npm run process:links:initial

# Regular updates (automatically included in the build process)
npm run build:links

# Link health validation
npm run validate:links

# Check for missing link previews
npm run check:links
# Or using the CLI utility
./scripts/bin/content.sh links:check

# Generate website screenshots
npm run screenshots
# Or using the CLI utility
./scripts/bin/content.sh screenshots
```

For detailed instructions on link management, see [MAINTENANCE.md](docs/reference/MAINTENANCE.md).

### How Link Preview Generation Works

1. **Initial Run**: When you first run `process:links:initial`, the script processes all links and generates metadata and screenshots.

2. **Incremental Updates**: During normal builds with `build:links`, the script:
   - Processes any new links that have been added
   - Updates the 10 oldest links (based on their last check date)
   - Preserves existing data for all other links

3. **Validation**: The `validate:links` command checks if links are still accessible without regenerating previews.

The tooling uses:
- `metascraper` for metadata extraction
- `puppeteer` and `@browserless/goto` for screenshot generation
- Microlink's API as a fallback for real-time preview generation

## License

MIT
