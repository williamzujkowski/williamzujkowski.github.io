# Site Configuration Structure

This directory contains the site configuration data, organized in a modular fashion for easier maintenance.

## Structure

- `site.js` - The main entry point that combines all configuration files
- `config/` - Directory containing all config modules
  - `meta.json` - Basic site metadata (title, description, etc.)
  - `blog/` - Blog-related configurations
    - `settings.json` - Blog display settings
  - `homepage/` - Homepage configurations
    - `about.json` - About me section
    - `display.json` - Display settings for the homepage
    - `reading.json` - Reading lists
    - `repositories.json` - Featured GitHub repositories
  - `links/` - Link collections
    - `groups.json` - Link group definitions
    - `social_links.json` - Social media links
    - `projects.json` - Project links
    - `technology.json` - Technology and innovation links
    - `art_culture.json` - Art and culture links
    - `fun.json` - Fun and curiosity links
  - `navigation.json` - Site navigation
  - `social/` - Social media configurations
    - `social_media.json` - Social media account settings

## How It Works

The `site.js` file uses Node.js to read and combine all these configuration files into a single `site` object that is accessible in templates. This modular approach makes it easier to find and edit specific parts of the site configuration without dealing with one large JSON file.

## How to Modify

1. Find the appropriate configuration file for what you want to change
2. Make your edits
3. The changes will be automatically picked up when the site builds

For example, to add or edit a featured project, edit the `config/homepage/repositories.json` file.