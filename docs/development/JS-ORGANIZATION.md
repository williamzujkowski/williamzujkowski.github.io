# JavaScript Organization Guide

This document outlines the JavaScript organization structure used in this website. The goal is to maintain a clean, modular, and maintainable JavaScript architecture while optimizing for performance.

## Directory Structure

The JavaScript files are organized into the following structure:

```
src/js/
├── components/         # UI components and features
│   ├── code-highlight.js  # Code block highlighting
│   ├── joke-generator.js  # Joke generation feature
│   ├── search.js          # Search functionality
│   ├── static-fallbacks.js # Fallback content handlers
│   └── theme-toggle.js    # Theme switching
├── utils/              # Utility functions
│   ├── analytics.js       # Analytics integration
│   ├── dom.js            # DOM manipulation utilities
│   ├── resource-hints.js  # Resource loading optimization
│   ├── site-config.js     # Site configuration
│   ├── storage.js         # Storage utilities
│   └── theme-init.js      # Theme initialization
└── main.js             # Application entry point
```

## Build System

The JavaScript codebase uses Rollup.js for bundling with the following optimizations:

- Tree-shaking to eliminate dead code
- Code splitting for better performance
- Dynamic imports for lazy loading
- Minification in production builds
- Bundle analysis capabilities

### Build Scripts

The `package.json` includes these JavaScript build scripts:

```
"build:js": "rollup -c rollup.config.js",
"build:js:prod": "NODE_ENV=production rollup -c rollup.config.js",
"watch:js": "rollup -c rollup.config.js --watch",
"analyze:js": "ANALYZE=true rollup -c rollup.config.js",
```

## JavaScript Architecture Principles

1. **Component-Based Architecture**: Each UI component has its own JavaScript file that exports an initialization function.

2. **ES Modules**: The codebase uses ES modules for better code organization, tree-shaking, and dependency management.

3. **Progressive Enhancement**: JavaScript enhances the user experience but is not required for basic functionality.

4. **Performance-First Approach**:

   - Scripts are organized by priority (high, medium, low)
   - Non-critical JavaScript is loaded asynchronously
   - Resource hints optimize asset loading
   - Hardware acceleration for animations

5. **Error Isolation**: Components include proper error handling to prevent failures from affecting the entire application.

## Initialization Process

JavaScript initialization follows a priority-based approach managed in `main.js`:

1. **High Priority** (runs immediately):

   - Resource hints (preload, prefetch)
   - Site configuration
   - Accessibility features
   - Theme initialization
   - Critical analytics

2. **Medium Priority** (runs after high priority, in next animation frame):

   - Responsive layout adjustments
   - Scroll effects
   - Content enhancements

3. **Low Priority** (runs when browser is idle):
   - Search functionality
   - Animations
   - Code highlighting
   - Static fallbacks

This approach ensures that critical functionality is available quickly while deferring non-essential operations to improve page load performance.

## Performance Monitoring

The codebase includes built-in performance monitoring:

```javascript
// Example from main.js
function trackPerformance(name, fn) {
  // Mark the start time
  performance.mark(`${name}-start`);

  // Execute the function
  const result = fn();

  // Mark the end time
  performance.mark(`${name}-end`);

  // Measure the duration
  performance.measure(name, `${name}-start`, `${name}-end`);

  return result;
}
```

This monitoring system:

- Uses the User Timing API
- Tracks initialization performance for each component
- Records errors and timing issues
- Reports metrics for analysis

## Component Pattern

When creating components, follow this pattern:

1. **Export an initialization function**:

```javascript
export function initMyComponent() {
  // Component initialization code
}
```

2. **Handle errors properly**:

```javascript
try {
  // Component code
} catch (error) {
  console.error("Component initialization failed:", error);
  // Fallback behavior if available
}
```

3. **Clean up event listeners** when necessary:

```javascript
function setupEventListeners() {
  const button = document.querySelector(".button");

  const clickHandler = () => {
    // Handle click
  };

  button.addEventListener("click", clickHandler);

  // Return cleanup function
  return () => {
    button.removeEventListener("click", clickHandler);
  };
}
```

## Performance Optimization Techniques

### Lazy Loading

Components can be lazily loaded when needed:

```javascript
// Lazy load a component only when needed
if (document.querySelector("#search-input")) {
  import("./components/search.js")
    .then((module) => {
      trackPerformance("search", module.initSearch);
    })
    .catch((error) => {
      console.error("Failed to load search:", error);
    });
}
```

### Hardware Acceleration

Animation elements use hardware acceleration:

```javascript
// Add hardware acceleration classes
element.classList.add("gpu-accelerated");

// Optimizing with will-change
element.style.willChange = "transform";

// Clean up after animation completes
element.addEventListener(
  "animationend",
  () => {
    element.style.willChange = "auto";
  },
  { once: true }
);
```

### Event Optimization

Events are optimized using:

```javascript
// Passive event listeners for better scroll performance
window.addEventListener("scroll", scrollHandler, { passive: true });

// Throttled events to limit execution frequency
let timeout;
element.addEventListener("scroll", () => {
  if (timeout) return;
  timeout = setTimeout(() => {
    // Handle event
    timeout = null;
  }, 100);
});

// Using requestAnimationFrame for visual updates
requestAnimationFrame(() => {
  element.classList.add("visible");
});
```

### Resource Hints

The website uses various resource hints to optimize loading:

```javascript
// Preload critical resources (needed immediately)
addPreload("/css/styles.css", "style");

// Prefetch resources for future navigation
addPrefetch("/blog/index.html");

// Preconnect to external domains
addPreconnect("https://api.example.com");
```

## Browser Support

The JavaScript architecture is designed to work in modern browsers with proper fallbacks:

- Feature detection for modern APIs
- Polyfills for requestIdleCallback
- Graceful degradation for older browsers
- Progressive enhancement approach

## Testing

JavaScript code is tested using a comprehensive testing framework:

- Unit tests for individual functions and components
- Integration tests for component interactions
- End-to-end tests with Playwright
- Visual regression tests for UI components
- Accessibility testing with axe-core

Run tests using various npm scripts:

```
npm run test:unit         # Run unit tests
npm run test:e2e          # Run end-to-end tests
npm run test:visual       # Run visual regression tests
npm run test:accessibility # Run accessibility tests
```

## Adding New JavaScript

### Adding New Components

1. Create a new file in the `components/` directory
2. Export the component's initialization function
3. Import and use the component in the appropriate priority level of `main.js`

Example:

```javascript
// components/my-component.js
/**
 * My Component
 *
 * This component provides specific functionality...
 *
 * @module components/my-component
 */

import { $, $$ } from "../utils/dom.js";

/**
 * Initializes my component
 */
export function initMyComponent() {
  // Component initialization code
  setupEventListeners();
  renderInitialState();
}

// Private functions...
function setupEventListeners() {
  // ...
}

function renderInitialState() {
  // ...
}
```

### Adding Utility Functions

1. Add functions to the appropriate utility file or create a new one
2. Export the functions for use in components

Example:

```javascript
// utils/my-utils.js
/**
 * My Utilities
 *
 * Utility functions for...
 *
 * @module utils/my-utils
 */

/**
 * Performs a specific utility function
 *
 * @param {string} input - The input to process
 * @returns {string} The processed result
 */
export function myUtilityFunction(input) {
  // Utility implementation
  return processedResult;
}
```

## Related Documentation

- See `rollup.config.js` for build configuration details
- See `PERFORMANCE-OPTIMIZATION.md` for performance strategies
- See `TESTING.md` for testing approach and methodologies
