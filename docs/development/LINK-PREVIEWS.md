# Link Preview System

This document explains how the link preview system works in the website.

## Overview

The website includes a link collection that is displayed on the `/links` page. For each link, we generate metadata-rich previews that contain information such as title, description, image URLs, and more, without requiring screenshots.

## How Link Data is Structured

Links are defined in modular configuration files located in `src/_data/config/links/`. Each file corresponds to a category of links (e.g., `technology.json`, `art_culture.json`).

The link groups are defined in `src/_data/config/links/groups.json`.

Example link definition:

```json
{
  "items": [
    { 
      "name": "Learn X in Y Minutes", 
      "url": "https://learnxinyminutes.com/", 
      "group": "Technology & Innovation", 
      "description": "Quick programming language tutorials" 
    }
  ]
}
```

## How Link Previews are Generated

Link previews are generated using the `metascraper` library, which extracts metadata from each URL. The data is saved as JSON files that can be used during site rendering.

### Preview Generation Scripts

1. `scripts/content/link-preview-generator.js` - Main script that generates preview data
2. `scripts/rebuild-link-previews.sh` - Bash script to run the generator

### Generated Data Files

The system generates the following data files:

- `_data/link-previews.json` - Master file with all link previews
- `assets/data/link-previews.json` - Copy for the built site
- `assets/data/link-previews-{category}.json` - Category-specific preview files
- `assets/data/link-previews-index.json` - URL to ID mapping

## How to Generate Link Previews

Run the following command to generate link previews:

```bash
npm run build:link-previews
```

You can also directly use the shell script:

```bash
./scripts/rebuild-link-previews.sh
```

The link preview data is now generated during the build process or can be manually updated with these commands.

## Preview Data Structure

Each link preview contains the following data:

```json
{
  "id": "unique-id-derived-from-name",
  "url": "https://example.com",
  "name": "Display Name",
  "type": "link",
  "group": "Category",
  "metadata": {
    "author": "Page Author",
    "date": "2025-04-13T02:55:51.814Z",
    "description": "Page description from metadata",
    "image": "https://example.com/image.jpg",
    "logo": "https://example.com/logo.png",
    "publisher": "Publisher Name",
    "title": "Page Title",
    "url": "https://example.com",
    "status": "success"
  },
  "description": "Custom description or metadata description",
  "last_checked": "2025-04-13T02:55:51.814Z"
}
```

## Integration with the Build Process

When you run `npm run build`, the script checks for the existence of link preview data and warns if it's missing, suggesting to run the generation command.

## Future Improvements

Planned improvements include:

1. Automatic refreshing of stale preview data (older than X days)
2. Fallback to Open Graph images for sites without explicit images
3. Caching failed requests to avoid repeated failures
4. UI improvements to show more preview metadata in the link listing