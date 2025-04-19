# Performance Optimization Guide

This document outlines the performance optimization strategies implemented during Phase 4 of the project refactoring. It serves as a reference for future development and maintenance.

## Table of Contents

1. [JavaScript Bundling](#javascript-bundling)
2. [Code Splitting and Dynamic Imports](#code-splitting-and-dynamic-imports)
3. [Hardware-Accelerated Animations](#hardware-accelerated-animations)
4. [Resource Hints](#resource-hints)
5. [Service Worker and Offline Support](#service-worker-and-offline-support)
6. [Performance Metrics Tracking](#performance-metrics-tracking)
7. [Event Optimization](#event-optimization)
8. [DOM Manipulation Best Practices](#dom-manipulation-best-practices)

## JavaScript Bundling

Modern JavaScript bundling was implemented using Rollup to optimize asset delivery and improve load times.

### Implementation Details

- **Multiple Entry Points**: The bundle configuration defines separate entry points for different components:

  - `main.bundle.js`: Critical path rendering
  - `blog.bundle.js`: Blog-specific functionality
  - `search.bundle.js`: Search functionality
  - Component-specific bundles for modular loading

- **Tree Shaking**: Removes unused code through ES modules and static analysis
- **Minification**: Uses Terser for optimal compression in production builds
- **Environment-Specific Builds**: Different optimizations for development and production

### Configuration

The bundling is configured in `rollup.config.js` with plugins for:

- Node module resolution
- CommonJS module conversion
- Terser minification
- Bundle visualization

```javascript
// Example rollup configuration
export default [
  {
    input: "src/js/main.js",
    output: {
      file: "_site/js/main.bundle.js",
      format: "es",
      sourcemap: !isProduction,
    },
    plugins: [...plugins],
  },
  // Additional bundles...
];
```

## Code Splitting and Dynamic Imports

Code splitting ensures that only necessary JavaScript is loaded initially, with additional code loaded on demand.

### Implementation Details

- **Dynamic Imports**: Non-critical components are loaded on demand using dynamic `import()` statements
- **Conditional Loading**: Components are only loaded if their functionality is needed on the current page
- **Prioritized Loading**: Core functionality loads immediately, enhancements load during idle time

### Example

```javascript
// Instead of static import
// import { initSearch } from './components/search.js';

// Dynamic import only when needed
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

## Hardware-Accelerated Animations

Animations are optimized to use the GPU for smoother performance and reduced CPU usage.

### Implementation Details

- **CSS Transforms**: Using `transform: translate3d()` instead of position properties
- **Will-change Property**: Hints to browsers which properties will change
- **Backface Visibility**: Prevents flickering in some browsers
- **Animation Cleanup**: Removing acceleration hints after animation completes

### CSS Enhancements

```css
/* Hardware-accelerated animation */
@keyframes slideUp {
  from {
    transform: translate3d(
      0,
      20px,
      0
    ); /* Using translate3d for hardware acceleration */
    opacity: 0;
  }
  to {
    transform: translate3d(0, 0, 0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slideUp 0.6s ease-out forwards;
  will-change: opacity, transform;
  backface-visibility: hidden;
}
```

### JavaScript Optimizations

```javascript
function animateElement(el) {
  // Add hardware acceleration classes
  el.classList.add("gpu-accelerated");
  el.classList.add("animate-slide-up");

  // Force browser to acknowledge the change before setting new animation
  void el.offsetWidth; // Triggers a reflow

  // Use requestAnimationFrame for smoother animation start
  requestAnimationFrame(() => {
    // Animation logic

    // Cleanup acceleration hints when done
    el.addEventListener(
      "animationend",
      () => {
        el.style.willChange = "auto";
      },
      { once: true }
    );
  });
}
```

## Resource Hints

Resource hints proactively load resources that may be needed soon, reducing perceived latency.

### Types of Resource Hints Implemented

1. **Preload**: Loads critical resources needed for the current page
2. **Prefetch**: Loads resources that may be needed for subsequent navigation
3. **Preconnect**: Establishes early connections to domains
4. **DNS-Prefetch**: Resolves domain names ahead of time
5. **Prerender**: Pre-renders entire pages (used sparingly)

### Implementation Details

- **Critical Assets**: Main CSS and JavaScript bundles are preloaded
- **Navigation Prediction**: Links visible in the viewport are prefetched
- **User Interaction**: Resources are loaded when users hover over links
- **Resource Prioritization**: Critical resources are marked with high importance

### Example

```javascript
// Preload critical CSS
addPreload("/css/styles.css", "style");

// Preload main JavaScript bundle
addPreload("/js/main.bundle.js", "script");

// Set up predictive loading for navigation
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const link = entry.target;
        const href = link.getAttribute("href");

        // Only prefetch internal links
        if (href && href.startsWith("/")) {
          addPrefetch(href);
        }
      }
    });
  },
  { rootMargin: "200px" }
);
```

## Service Worker and Offline Support

A service worker provides caching and offline capabilities, improving repeat visit performance.

### Implementation Details

- **Cache Strategies**: Different strategies for different resource types:

  - HTML: Network-first with cache fallback
  - CSS/JS/Images: Cache-first with network update
  - API data: Network-first with time-based cache

- **Offline Fallback**: Custom offline page when content isn't available
- **Cache Management**: Automatic cleanup of old cached resources
- **Preloading**: Core assets are pre-cached on installation

### Example

```javascript
// Cache core assets on install
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS);
    })
  );
});

// Serve from cache or network
self.addEventListener("fetch", (event) => {
  // Different strategies based on resource type
  if (event.request.headers.get("Accept").includes("text/html")) {
    // Network-first for HTML
    // ...
  } else if (event.request.url.match(/\.(js|css|png|jpg|svg)$/)) {
    // Cache-first for assets
    // ...
  }
});
```

## Performance Metrics Tracking

Performance measurement helps identify bottlenecks and track improvements over time.

### Implementation Details

- **User Timing API**: Marks and measures for key operations
- **Custom Metrics Object**: Centralized tracking of performance data
- **Component Timing**: Each component's initialization is timed
- **Analytics Integration**: Critical metrics are reported to analytics

### Example

```javascript
function trackPerformance(name, fn) {
  // Mark the start time
  const markName = `${name}-start`;
  performance.mark(markName);

  // Execute the function
  const result = fn();

  // Mark the end time
  const endMarkName = `${name}-end`;
  performance.mark(endMarkName);

  // Measure the duration
  performance.measure(name, markName, endMarkName);

  // Store the duration
  const duration = performance.now() - PERFORMANCE_METRICS.marks[markName];
  PERFORMANCE_METRICS.components[name] = duration;

  return result;
}
```

## Event Optimization

Event handling is optimized to reduce CPU usage and improve responsiveness.

### Implementation Details

- **Passive Event Listeners**: Used for scroll and touch events
- **Event Delegation**: Single listeners for multiple elements
- **Throttling and Debouncing**: Limits event handler execution
- **requestAnimationFrame**: Synchronizes visual updates with the browser's refresh cycle

### Example

```javascript
// Throttled scroll event
let scrollTimeout;
window.addEventListener(
  "scroll",
  () => {
    // Skip if we're still in timeout period
    if (scrollTimeout) return;

    // Create a timeout to limit executions
    scrollTimeout = setTimeout(() => {
      // Scroll handling logic

      // Clear the timeout
      scrollTimeout = null;
    }, 100); // 100ms throttle
  },
  { passive: true }
); // Passive for better performance
```

## DOM Manipulation Best Practices

Optimized DOM manipulation reduces layout thrashing and improves rendering performance.

### Implementation Details

- **Batch Operations**: Group read and write operations
- **Document Fragments**: Build complex DOM structures off-screen
- **Minimizing Reflows**: Reduce layout recalculations
- **Class Manipulation**: Use classList instead of direct style manipulation when possible

### Example

```javascript
// Batch DOM operations
const allElements = [];

// Batch read operations first
elements.forEach((el) => {
  // Initial setup - read operations
  el.getBoundingClientRect(); // Force a reflow once
  allElements.push(el);
});

// Use requestAnimationFrame for visual updates
requestAnimationFrame(() => {
  // Batch write operations
  allElements.forEach((el) => {
    // All style changes at once
    el.classList.add("visible");
    el.style.transform = "translate3d(0,0,0)";
  });
});
```

## Best Practices for Maintaining Performance

1. **Measure First**: Always benchmark before and after optimizations
2. **Analyze Bundles**: Regularly check bundle sizes and composition
3. **Progressive Enhancement**: Ensure core functionality works without optimizations
4. **Test on Real Devices**: Performance varies significantly across devices
5. **Prioritize Critical Path**: Focus on optimizing what users see first
6. **Avoid Premature Optimization**: Optimize based on measured bottlenecks
7. **Use Chrome DevTools**: Performance and Network panels are essential for debugging

## References

- [Web Vitals](https://web.dev/vitals/)
- [MDN Web Performance](https://developer.mozilla.org/en-US/docs/Web/Performance)
- [Google Page Speed Insights](https://developers.google.com/speed/pagespeed/insights/)
- [Rollup.js Documentation](https://rollupjs.org/guide/en/)
