# CSS Organization Guide

This document outlines the CSS organization structure used in this website. The goal is to maintain a clean, modular, and maintainable CSS architecture.

## Directory Structure

The CSS files are organized into the following structure:

```
src/css/
├── base/               # Base styles
│   ├── reset.css       # CSS reset/normalize
│   ├── typography.css  # Typography styles
│   └── layout.css      # Base layout styles
├── components/         # Component-specific styles
│   ├── header.css      # Header component
│   ├── footer.css      # Footer component
│   ├── buttons.css     # Button components
│   └── post.css        # Blog post components
├── utils/              # Utilities and helpers
│   ├── variables.css   # CSS variables
│   ├── mixins.css      # CSS utility classes
│   └── animations.css  # Animation definitions
└── main.css            # Main file that imports all others
```

## CSS Architecture Principles

1. **Component-Based**: Each UI component has its own CSS file for better organization and maintainability.
2. **Mobile-First**: We use a mobile-first approach, where base styles are written for mobile and media queries are used to adapt for larger screens.
3. **CSS Variables**: We use CSS custom properties (variables) for theming and consistent values across the codebase.
4. **Modular Imports**: All CSS files are imported into `main.css`, which is the only file included in the HTML.

## How to Use

### Adding New Styles

1. **For Component Styles**: Add a new file in the `components/` directory.
2. **For General Styles**: Add them to the appropriate file in `base/`.
3. **For Utility Classes**: Add them to `utils/mixins.css`.
4. **For New Variables**: Add them to `utils/variables.css`.
5. **For New Animations**: Add them to `utils/animations.css`.

After adding a new file, make sure to import it in `main.css`.

### Using CSS Variables

Example of using CSS variables for consistent theming:

```css
.my-component {
  background-color: var(--color-surface);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  transition: var(--transition);
}

.my-component:hover {
  transform: var(--hover-transform);
  box-shadow: var(--shadow-elevated);
}
```

### Responsive Design

We use a mobile-first approach with media queries for larger screens:

```css
.my-component {
  /* Mobile styles (default) */
  padding: 1rem;
  font-size: 1rem;
}

@media (min-width: 768px) {
  .my-component {
    /* Tablet styles */
    padding: 1.5rem;
    font-size: 1.125rem;
  }
}

@media (min-width: 1024px) {
  .my-component {
    /* Desktop styles */
    padding: 2rem;
    font-size: 1.25rem;
  }
}
```

## Build Process

The CSS build process:

1. All CSS files are imported into `main.css`
2. PostCSS processes the CSS with plugins:
   - Tailwind CSS for utility classes
   - Autoprefixer for vendor prefixes
   - CSSnano for minification
3. The output is saved to `_site/css/styles.css`

## Theme System

We use a dark/light theme system with CSS variables. The theme is controlled by adding a class to the `html` element:

- Dark theme (default): `<html class="dark">`
- Light theme: `<html class="light">`

Theme variables are defined in `utils/variables.css` with two sets of values:

```css
/* Dark theme (default) */
:root {
  --color-background: oklch(0.16 0.02 250);
  --color-text: oklch(0.93 0.02 250);
  /* etc. */
}

/* Light theme */
:root.light {
  --color-background: oklch(0.98 0.01 250);
  --color-text: oklch(0.2 0.02 250);
  /* etc. */
}
```

The theme can be toggled with JavaScript by adding/removing the `light` class on the `html` element.
