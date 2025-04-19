# Website Maintenance Guide

> This document is part of the [website documentation](../README.md).

This document provides detailed instructions for maintaining and updating the website using the various tools and scripts we've set up.

## Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Regular Maintenance Tasks](#regular-maintenance-tasks)
3. [Adding New Blog Posts](#adding-new-blog-posts)
4. [Managing Links](#managing-links)
5. [Updating GitHub Repository Information](#updating-github-repository-information)
6. [Working with Website Configuration](#working-with-website-configuration)
7. [Build and Deployment Process](#build-and-deployment-process)
8. [Troubleshooting](#troubleshooting)

## Development Environment Setup

To work on the website, you need to have Node.js installed (version 18 or higher).

1. **Clone the repository:**

   ```bash
   git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
   cd williamzujkowski.github.io
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```
   This will launch the website at http://localhost:8082/

## Regular Maintenance Tasks

### General Website Updates

1. **Update all dependencies:**

   ```bash
   npm update
   ```

2. **Run security audit:**

   ```bash
   npm audit fix
   ```

3. **Check for broken links:**
   ```bash
   npm run validate:links
   ```
   This script will check all external links on the website and report any issues.

### Full Site Rebuild

To rebuild the entire site:

```bash
npm run build
```

This command runs all data generation scripts and builds the site with Eleventy.

## Adding New Blog Posts

We have a streamlined process for adding new blog posts:

### Option 1: Text Files (.txt)

1. Create a `.txt` file in the `new_posts/` directory
2. Format it as follows:
   - First line: Post title
   - Second line: Blank
   - Remaining lines: Post content

Example:

```
Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

### Option 2: Markdown Files (.md)

1. Create a `.md` file in the `new_posts/` directory
2. Use any of these formats:
   - Use an H1 header (`# Title`) for the title
   - Use front matter with a title field
   - Or the filename will be used as the title

Example with H1:

```markdown
# Understanding Quantum Computing

Quantum computing represents a fundamental shift in how we process information...
```

### Processing and Publishing Posts

1. **Run the post processor:**

   ```bash
   npm run process:posts
   ```

   This will:

   - Extract the title and content
   - Add proper frontmatter
   - Assign publication dates (10-14 days apart)
   - Suggest relevant tags based on content
   - Add appropriate feature images
   - Move processed files to `new_posts/processed/`

2. **Review the generated posts:**
   Check the output files in `src/posts/` and make any needed adjustments.

3. **Build the site to preview your changes:**

   ```bash
   npm run build
   npm run dev
   ```

4. **Commit the changes:**
   ```bash
   git add src/posts/
   git commit -m "Add new blog posts"
   git push
   ```

## Managing Links

Links are stored in `src/_data/site.json` and can be displayed on the links page.

### Adding New Links

1. Edit `src/_data/site.json`
2. Add your link to the appropriate section:

   ```json
   "links": [
     {
       "name": "Example Link",
       "url": "https://example.com",
       "group": "Technology & Innovation",
       "description": "Brief description of the link"
     }
   ]
   ```

3. Rebuild the link previews:
   ```bash
   npm run build:links
   ```

### Validating Links

To check all links for validity:

```bash
npm run validate:links
```

This will:

- Check if all links are accessible
- Update link preview data with validation results
- Generate a report of any broken links

### Refreshing Link Previews

To refresh all link previews:

```bash
npm run process:links:initial
```

For normal operation (updating just the oldest links):

```bash
npm run build:links
```

## Updating GitHub Repository Information

GitHub repository information is stored in `src/_data/site.json` in the `homepage.pinned_repositories` section.

To update repository information:

1. Edit `src/_data/site.json`
2. Update the repository information:

   ```json
   "pinned_repositories": [
     {
       "name": "Repository Name",
       "description": "Repository description",
       "url": "https://github.com/username/repo",
       "language": "JavaScript",
       "language_color": "#f1e05a",
       "stars": 42,
       "forks": 10,
       "updated": "2 days ago"
     }
   ]
   ```

3. Rebuild the GitHub data:
   ```bash
   npm run build:github
   ```

### Toggling GitHub Repositories on Links Page

To show/hide GitHub repositories on the links page:

1. Edit `src/_data/site.json`
2. Update the `show_github_repos_on_links` flag:
   ```json
   "homepage": {
     "show_github_repos_on_links": true,
     // other settings...
   }
   ```

## Working with Website Configuration

The main configuration file is `src/_data/site.json`, which controls:

- Site title, description, and metadata
- Social media links
- Navigation structure
- Blog settings
- Link groups
- Homepage configuration

To update the configuration:

1. Edit `src/_data/site.json`
2. Rebuild the site:
   ```bash
   npm run build
   ```

## Build and Deployment Process

The website uses a multi-step build process:

1. **Data Generation:**

   - `npm run build:arxiv` - Fetches and processes arXiv papers
   - `npm run build:github` - Fetches and processes GitHub repository data
   - `npm run build:viz` - Generates visualization data like contribution heatmaps
   - `npm run build:links` - Processes link previews

2. **Site Generation:**

   - Eleventy builds the HTML pages from templates
   - PostCSS processes the CSS files

3. **Complete Build:**
   - `npm run build` - Runs all data generation steps and builds the site

### GitHub Pages Deployment

The site is automatically deployed to GitHub Pages when changes are pushed to the main branch.

For manual deployment:

1. Build the site:

   ```bash
   npm run build
   ```

2. Commit and push the changes:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```

## Troubleshooting

### Common Issues and Solutions

1. **Link preview generation fails:**

   - Check your internet connection
   - Verify the link is accessible
   - Check if the site blocks automated access
   - Run with the `--initial` flag to force a fresh start:
     ```bash
     npm run process:links:initial
     ```

2. **Post processing issues:**

   - Verify file format is correct
   - Check for proper line breaks
   - Ensure there's an H1 header or proper frontmatter in markdown files

3. **Build process fails:**
   - Check console error messages
   - Verify all dependencies are installed
   - Check for syntax errors in templates

### Directory Structure Overview

```
/
├── _data/                # Generated data files
├── assets/               # Static assets
│   ├── images/           # Image files
│   └── data/             # Generated data files
├── config/               # Configuration files
├── new_posts/            # New blog posts to process
│   └── processed/        # Processed blog posts
├── scripts/              # Build scripts
├── src/                  # Source files
│   ├── _data/            # Site configuration
│   ├── _includes/        # Template partials
│   ├── css/              # CSS files
│   ├── js/               # JavaScript files
│   └── posts/            # Blog posts
├── tools/                # Utility scripts
│   └── validation/       # Validation tools
└── _site/                # Generated site (after build)
```

### Key Scripts Reference

| Script                   | Purpose                      |
| ------------------------ | ---------------------------- |
| `npm run dev`            | Start development server     |
| `npm run build`          | Build entire site            |
| `npm run build:links`    | Generate link previews       |
| `npm run validate:links` | Check links for validity     |
| `npm run process:posts`  | Process new blog posts       |
| `npm run build:arxiv`    | Fetch arXiv paper data       |
| `npm run build:github`   | Fetch GitHub repository data |
| `npm run build:viz`      | Generate visualization data  |
| `npm run build:css`      | Build CSS files              |

---

[Back to Documentation Home](../index.md) | [Reference Docs](./)
