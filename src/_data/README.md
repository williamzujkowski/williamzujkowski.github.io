# Site Configuration Structure

This directory contains the site configuration data, organized in a modular fashion for easier maintenance and updates.

## Structure

- `site.js` - The main entry point that combines all configuration files
- `config/` - Directory containing all config modules
  - `meta.json` - Basic site metadata (title, description, etc.)
  - `blog/` - Blog-related configurations
    - `settings.json` - Blog display settings (post counts, pagination, formats)
  - `homepage/` - Homepage configurations
    - `about.json` - About me section content and display options
    - `display.json` - Display settings for homepage sections (visibility toggles)
    - `reading.json` - Reading lists and current research papers
    - `repositories.json` - Featured GitHub repositories
  - `links/` - Link collections
    - `groups.json` - Link group definitions and categories
    - `social_links.json` - Social media profile links
    - `projects.json` - Personal and professional project links
    - `technology.json` - Technology and innovation resource links
    - `art_culture.json` - Art and culture resource links
    - `fun.json` - Fun and interesting curiosity links
  - `navigation.json` - Site navigation structure and menu items
  - `social/` - Social media configurations
    - `social_media.json` - Social media account settings and display options

## How It Works

The `site.js` file uses ES modules to read and combine all configuration files into a single `site` object that is accessible in templates. Key features:

- **Automatic merging**: All JSON files are automatically merged into a structured object
- **Special handling**: Some directories like `links/` and `homepage/` have special processing logic
- **Error handling**: Invalid or missing files are gracefully handled with warnings
- **Hierarchical structure**: Configuration is organized by function and purpose

## How to Modify

### General Updates

1. Find the appropriate configuration file for what you want to change
2. Make your edits to the JSON file
3. Run `npm run build` or `npm run dev` to see your changes
4. The changes will be automatically processed by `site.js`

### Adding New Sections

1. Create a new JSON file in the appropriate subdirectory
2. Follow the existing JSON format patterns
3. Site.js will automatically include your new configuration

### Examples

#### Adding a new featured repository:

Edit `config/homepage/repositories.json`:

```json
{
  "featured_repositories": [
    {
      "name": "My New Project",
      "description": "A cool new tool I built",
      "url": "https://github.com/username/project",
      "language": "JavaScript",
      "stars": 25
    }
    // Other existing repositories...
  ]
}
```

#### Adding a new link group:

1. First add the group definition in `config/links/groups.json`:

```json
{
  "linkGroups": [
    {
      "id": "new-group",
      "title": "My New Link Category",
      "description": "Cool new resources",
      "icon": "icon-name"
    }
    // Other existing groups...
  ]
}
```

2. Then create a new file `config/links/new_group.json`:

```json
{
  "items": [
    {
      "title": "New Resource",
      "url": "https://example.com",
      "description": "A helpful resource",
      "group": "new-group"
    }
  ]
}
```

## Troubleshooting

- If your changes don't appear, check the browser console for errors
- Verify your JSON is valid (no trailing commas, properly closed brackets)
- Check that your file is in the correct directory
- Run with `npm run debug` to see detailed configuration loading information
