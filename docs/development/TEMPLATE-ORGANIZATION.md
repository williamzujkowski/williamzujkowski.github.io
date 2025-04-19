# Template Organization

This document outlines the template organization structure for the website.

## Directory Structure

The template files are organized into the following directories:

- `src/_includes/layouts/`: Contains base layout templates that other templates extend
- `src/_includes/partials/`: Contains reusable partial templates that are included in other templates
- `src/_includes/macros/`: Contains reusable macro functions for generating HTML

## Layout Templates

Layout templates provide the base structure for pages:

- `layouts/base.njk`: The main layout template that all pages use
- `layouts/post.njk`: Layout for blog posts (extends base.njk)

## Partial Templates

Partial templates are reusable components included in layouts:

- `partials/header.njk`: Site header with navigation
- `partials/footer.njk`: Site footer with links and copyright
- `partials/meta.njk`: Head metadata (title, description, Open Graph, etc.)

## Macro Templates

Macros are reusable template functions for generating HTML:

- `macros/buttons.njk`: Button macros (primary, secondary, icon)
- `macros/cards.njk`: Card macros (post cards, link cards)
- `macros/headings.njk`: Heading macros (section headings, page titles)

## Usage Examples

### Using Layouts

```njk
---
layout: layouts/base.njk
---
<div class="content">
  <!-- Page content here -->
</div>
```

### Including Partials

```njk
{% include "partials/header.njk" %}
```

### Using Macros

```njk
{% from "macros/buttons.njk" import primaryButton %}

{{ primaryButton("Click Me", "/destination", '<svg>...</svg>') }}
```

## JavaScript Integration

All JavaScript functionality has been moved from inline scripts to modular components:

- `src/js/components/theme-toggle.js`: Theme switching functionality
- `src/js/components/code-highlight.js`: Code block syntax highlighting
- `src/js/components/static-fallbacks.js`: Static fallbacks for dynamic content

These components are imported and initialized in `src/js/main.js` using a priority-based initialization system.

## Best Practices

1. **Use macros for repetitive UI elements**: Prefer macros over duplicating HTML patterns
2. **Keep partials focused**: Each partial should handle one specific part of the UI
3. **Follow consistent naming**: Use kebab-case for file names
4. **Use the appropriate directory**: Place templates in the correct directory based on their purpose
5. **Extract inline scripts**: Move all JavaScript to external files in the components directory
