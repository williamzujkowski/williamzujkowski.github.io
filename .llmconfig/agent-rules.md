# Agent Rules for williamzujkowski.github.io

This document defines the coding standards and best practices that LLM agents should follow when working with this codebase.

## Core Principles

1. **Content First**: This is a technical blog - prioritize readability and content delivery
2. **Performance Matters**: Every addition should consider its impact on page load times
3. **Accessibility is Required**: All features must be accessible to all users
4. **Progressive Enhancement**: Core functionality must work without JavaScript
5. **Maintainability**: Code should be easy to understand and modify

## Code Style Rules

### JavaScript

```javascript
// GOOD: Clear, modular, testable
export function processData(input) {
  if (!input || typeof input !== "string") {
    throw new TypeError("Input must be a non-empty string");
  }

  return input.trim().toLowerCase().replace(/\s+/g, "-");
}

// BAD: Global state, no error handling
function process() {
  window.data = window.input.toLowerCase().replace(/ /g, "-");
}
```

### CSS

```css
/* GOOD: Uses custom properties, BEM-like naming */
.blog-card {
  background: var(--color-surface);
  padding: var(--spacing-md);
  border-radius: var(--radius-sm);
}

.blog-card__title {
  color: var(--color-primary);
  font-size: var(--font-size-lg);
}

/* BAD: Hard-coded values, unclear naming */
.card1 {
  background: #ffffff;
  padding: 16px;
  border-radius: 4px;
}
```

### HTML/Nunjucks

```njk
{# GOOD: Semantic, accessible #}
<article class="blog-post" aria-labelledby="post-title">
  <header>
    <h1 id="post-title">{{ title }}</h1>
    <time datetime="{{ date | dateToISO }}">{{ date | dateToFormat }}</time>
  </header>
  <div class="blog-post__content">
    {{ content | safe }}
  </div>
</article>

{# BAD: Non-semantic, missing accessibility #}
<div class="post">
  <div class="title">{{ title }}</div>
  <div>{{ date }}</div>
  <div>{{ content | safe }}</div>
</div>
```

## File Naming Conventions

- **Blog Posts**: `YYYY-MM-DD-title-in-kebab-case.md`
- **Components**: `component-name.js` (kebab-case)
- **Styles**: Match component names or use descriptive names
- **Templates**: Use `.njk` extension for Nunjucks templates
- **Scripts**: Descriptive names indicating purpose (e.g., `optimize-images.js`)

## Git Commit Standards

Use conventional commits format:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `perf:` Performance improvements
- `test:` Test additions or changes
- `chore:` Build process or auxiliary tool changes

Examples:

```
feat: add dark mode toggle to blog posts
fix: correct RSS feed generation for future-dated posts
docs: update README with new build instructions
perf: implement lazy loading for blog images
```

## Testing Requirements

1. **Unit Tests**: Required for utility functions and data transformations
2. **E2E Tests**: Required for critical user paths (blog navigation, search)
3. **Accessibility Tests**: Run automated checks on all new pages
4. **Visual Regression**: For major style changes
5. **Performance Tests**: Monitor bundle sizes and load times

## Performance Guidelines

1. **Images**:

   - Use appropriate formats (WebP with fallbacks)
   - Implement responsive images with srcset
   - Always include width and height attributes
   - Lazy load below-the-fold images

2. **JavaScript**:

   - Bundle size limit: 50KB for main bundle (gzipped)
   - Use dynamic imports for feature-specific code
   - Avoid blocking the main thread
   - Implement code splitting where beneficial

3. **CSS**:
   - Critical CSS should be inlined
   - Non-critical styles should be loaded asynchronously
   - Avoid expensive selectors
   - Use CSS containment where appropriate

## Security Requirements

1. **Content Security Policy**: Maintain strict CSP headers
2. **Dependencies**: Regular updates and vulnerability scanning
3. **User Input**: Always sanitize (though minimal in static site)
4. **External Resources**: Verify and use SRI for CDN resources
5. **HTTPS**: Ensure all resources use HTTPS

## Accessibility Checklist

- [ ] Keyboard navigation works for all interactive elements
- [ ] Focus indicators are visible
- [ ] Color contrast meets WCAG AA standards
- [ ] Images have appropriate alt text
- [ ] Page has proper heading hierarchy
- [ ] ARIA labels used where needed
- [ ] Forms have associated labels
- [ ] Error messages are accessible

## Common Patterns

### Component Initialization

```javascript
// Pattern for initializing components
document.addEventListener("DOMContentLoaded", () => {
  const components = document.querySelectorAll("[data-component]");

  components.forEach((element) => {
    const componentName = element.dataset.component;
    const Component = componentRegistry[componentName];

    if (Component) {
      new Component(element);
    }
  });
});
```

### Data Loading

```javascript
// Pattern for loading and caching data
const dataCache = new Map();

export async function loadData(endpoint) {
  if (dataCache.has(endpoint)) {
    return dataCache.get(endpoint);
  }

  try {
    const response = await fetch(endpoint);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    const data = await response.json();
    dataCache.set(endpoint, data);
    return data;
  } catch (error) {
    console.error(`Failed to load data from ${endpoint}:`, error);
    throw error;
  }
}
```

### Responsive Images

```html
<!-- Pattern for responsive images -->
<picture>
  <source
    type="image/webp"
    srcset="
      /images/hero-sm.webp  640w,
      /images/hero-md.webp 1024w,
      /images/hero-lg.webp 1920w
    "
    sizes="(max-width: 640px) 100vw,
           (max-width: 1024px) 100vw,
           1920px"
  />
  <img
    src="/images/hero-lg.jpg"
    alt="Descriptive alt text"
    width="1920"
    height="1080"
    loading="lazy"
  />
</picture>
```

## Do's and Don'ts

### Do's

- ✅ Write self-documenting code
- ✅ Add comments for complex logic
- ✅ Use meaningful variable names
- ✅ Handle errors gracefully
- ✅ Consider mobile users first
- ✅ Test in multiple browsers
- ✅ Optimize for performance
- ✅ Follow existing patterns

### Don'ts

- ❌ Don't add unnecessary dependencies
- ❌ Don't use inline styles or scripts
- ❌ Don't ignore accessibility
- ❌ Don't break existing functionality
- ❌ Don't hardcode values that should be configurable
- ❌ Don't create overly complex solutions
- ❌ Don't forget to update documentation
- ❌ Don't commit without testing

## Review Checklist

Before submitting code:

1. Code follows style guidelines
2. Tests pass and coverage maintained
3. No console errors or warnings
4. Performance budget maintained
5. Accessibility checks pass
6. Documentation updated if needed
7. Commit messages follow conventions
8. No sensitive data exposed
