# JavaScript Organization Guide

This document outlines the JavaScript organization structure used in this website. The goal is to maintain a clean, modular, and maintainable JavaScript architecture.

## Directory Structure

The JavaScript files are organized into the following structure:

```
src/js/
├── components/         # UI components
│   ├── search.js       # Search functionality
│   ├── theme-toggle.js # Theme switching
│   └── ...            # Other components
├── utils/             # Utility functions
│   ├── dom.js         # DOM manipulation utilities
│   ├── storage.js     # Storage utilities
│   └── ...            # Other utilities
├── data/              # Data handling
│   └── ...            # Data management
└── main.js            # Application entry point
```

## JavaScript Architecture Principles

1. **Component-Based**: Each UI component has its own JavaScript file for better organization and maintainability.
2. **ES Modules**: We use ES modules for code organization and dependency management.
3. **Progressive Enhancement**: JavaScript enhances the user experience but is not required for basic functionality.
4. **Performance Optimization**: Scripts are organized by priority (high, medium, low) to optimize loading and execution.

## How to Use

### Adding New Components

1. Create a new file in the `components/` directory.
2. Export the component's initialization function.
3. Import and use the component in `main.js`.

Example:

```javascript
// components/my-component.js
export function initMyComponent() {
  // Component initialization code
}

// main.js
import { initMyComponent } from "./components/my-component.js";

// Call the initialization function at the appropriate time
initMyComponent();
```

### Adding Utility Functions

1. Add functions to the appropriate utility file or create a new one.
2. Export the functions for use in components.

Example:

```javascript
// utils/my-utils.js
export function myUtilityFunction() {
  // Utility implementation
}

// components/my-component.js
import { myUtilityFunction } from "../utils/my-utils.js";

// Use the utility function
myUtilityFunction();
```

## Initialization Process

JavaScript initialization follows a priority-based approach:

1. **High Priority** (runs immediately):

   - Accessibility features
   - Theme initialization
   - Critical UI components

2. **Medium Priority** (runs after high priority):

   - Responsive layout adjustments
   - Navigation components
   - Scroll effects

3. **Low Priority** (runs when browser is idle):
   - Search functionality
   - Animations
   - Non-critical features

This approach ensures that critical features are available quickly while deferring non-essential operations to improve page load performance.

## Performance Considerations

### Lazy Loading

Components can be lazily loaded when needed:

```javascript
// Lazy load a component only when needed
function setupFeature() {
  import("./components/feature.js").then((module) => {
    module.initFeature();
  });
}

// Call only when user interacts with a specific element
document.querySelector(".feature-button").addEventListener("click", setupFeature);
```

### Event Delegation

We use event delegation for efficient event handling:

```javascript
// Instead of attaching events to each button
document.addEventListener("click", (e) => {
  if (e.target.matches(".action-button")) {
    // Handle button click
  }
});
```

### DOM Operations

Minimize DOM operations by:

- Using DocumentFragment for batch DOM updates
- Caching DOM references
- Using efficient selectors
- Throttling and debouncing events

## Browser Support

The JavaScript architecture is designed to work in modern browsers with fallbacks:

- ES Modules with dynamic imports for code splitting
- Polyfills for requestIdleCallback and other modern APIs
- Feature detection for progressive enhancement
- Graceful degradation for older browsers

## Error Handling

All components should include proper error handling to prevent issues from affecting the entire application:

```javascript
try {
  // Component code
} catch (error) {
  console.error("Component initialization failed:", error);
  // Fallback behavior if available
}
```
