# CLAUDE Configuration for williamzujkowski.github.io

This file contains specific instructions for Claude AI when interacting with this project. It provides guidance on project context, coding patterns, and appropriate behaviors.

## Main Instructions

- Always follow the principles outlined in the root CLAUDE.md file
- Prioritize clean, accessible code that follows web standards
- Focus on performance optimization for web content delivery
- Consider SEO implications when suggesting content changes
- Maintain consistency with the existing Eleventy-based architecture
- Respect the project's focus on technical blog content

## Project Context

This project is a personal technical blog focused on:

- Technology articles and insights
- Code samples and explanations
- Technical documentation
- Vulnerability analysis posts
- AI/ML, cloud computing, cybersecurity, and quantum computing topics

The site uses Eleventy as a static site generator with a focus on performance and accessibility.

## Technology Stack

- **Static Site Generator**: Eleventy (11ty)
- **Templates**: Nunjucks (.njk files)
- **Styling**: CSS with custom properties for theming
- **JavaScript**: ES6+ modules with Rollup bundling
- **Testing**: Jest, Playwright for E2E tests
- **Build Tools**: Node.js, npm scripts

## Coding Patterns

### JavaScript

- Use ES6+ features and syntax
- Prefer functional programming patterns where appropriate
- Implement proper error handling for asynchronous operations
- Follow modular design principles
- Use dynamic imports for code splitting when beneficial
- Maintain compatibility with modern browsers (no IE11 support required)

Example pattern for component modules:

```javascript
// Component module pattern
export class ComponentName {
  constructor(options = {}) {
    this.options = { ...this.defaults, ...options };
    this.init();
  }

  init() {
    // Initialization logic
  }

  // Public methods
}
```

### HTML/CSS

- Maintain semantic HTML structure
- Follow accessibility best practices (WCAG 2.1 AA)
- Implement responsive design patterns
- Use CSS custom properties for theming
- Optimize for Core Web Vitals
- Use BEM-like naming for component styles

### Eleventy/Nunjucks

- Keep templates modular and reusable
- Use includes for shared components
- Leverage Eleventy's data cascade effectively
- Maintain clear separation between content and presentation
- Use filters for data transformation

## File Organization

- `/src/` - Source files (templates, styles, scripts)
- `/src/posts/` - Blog post content in Markdown
- `/src/_includes/` - Reusable template components
- `/src/_data/` - Global data files
- `/src/css/` - Stylesheets organized by purpose
- `/src/js/` - JavaScript modules and components
- `/scripts/` - Build and utility scripts
- `/assets/` - Static assets (images, icons)

## Content Guidelines

When working with blog posts:

- Maintain consistent frontmatter structure
- Use appropriate topic tags from the defined set
- Ensure code blocks have proper syntax highlighting
- Add meaningful alt text for images
- Include meta descriptions for SEO

## Performance Considerations

- Lazy load images and heavy resources
- Minimize JavaScript bundle sizes
- Use resource hints (preload, prefetch) appropriately
- Implement service worker for offline support
- Optimize images before adding to repository

## Security Practices

- Sanitize any user-generated content
- Avoid inline scripts and styles
- Use Content Security Policy headers
- Keep dependencies updated
- Validate all external data sources

## Testing Requirements

- Write unit tests for new JavaScript utilities
- Add E2E tests for critical user paths
- Verify accessibility with automated tools
- Test across major browsers
- Ensure responsive design works on various devices

## Common Tasks

### Adding a New Blog Post

1. Create markdown file in `/src/posts/` with proper date prefix
2. Include required frontmatter (title, date, tags, excerpt)
3. Use existing posts as templates
4. Run build to verify rendering

### Modifying Styles

1. Check if changes belong in base, components, or utils
2. Use CSS custom properties for themeable values
3. Ensure changes work with both light and dark themes
4. Test responsive behavior

### Adding JavaScript Functionality

1. Create modular components in `/src/js/components/`
2. Use progressive enhancement
3. Handle cases where JavaScript is disabled
4. Add appropriate error handling

## Important Notes

- The site prioritizes content and performance over complex interactions
- Maintain backwards compatibility for existing URLs
- Consider RSS feed compatibility when changing post structure
- Keep build times reasonable by optimizing data processing
- Document any significant architectural changes
