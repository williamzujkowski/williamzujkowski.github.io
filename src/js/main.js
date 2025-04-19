/**
 * main.js - Application entry point
 *
 * This module serves as the main entry point for the application's JavaScript.
 * It initializes all components in a prioritized manner to optimize page load
 * performance while providing core functionality.
 *
 * Enhanced in Phase 4 with performance monitoring, lazy loading,
 * and optimization for the modern build system.
 *
 * @module main
 */

// Initialize performance metrics
const PERFORMANCE_METRICS = {
  init: performance.now(),
  marks: {},
  measures: {},
  components: {},
  errors: [],
};

// Import core components only - others will be lazy loaded
import { initThemeToggle } from "./components/theme-toggle.js";
import { initSiteConfig } from "./utils/site-config.js";

/**
 * Records performance timing for a specific operation
 *
 * @param {string} name - The name of the operation to measure
 * @param {Function} fn - The function to execute and measure
 * @returns {*} The result of the function execution
 */
function trackPerformance(name, fn) {
  try {
    // Mark the start time
    const markName = `${name}-start`;
    performance.mark(markName);
    PERFORMANCE_METRICS.marks[markName] = performance.now();

    // Execute the function
    const result = fn();

    // Mark the end time
    const endMarkName = `${name}-end`;
    performance.mark(endMarkName);
    PERFORMANCE_METRICS.marks[endMarkName] = performance.now();

    // Measure the duration
    performance.measure(name, markName, endMarkName);

    // Store the duration in our metrics object
    const duration = performance.now() - PERFORMANCE_METRICS.marks[markName];
    PERFORMANCE_METRICS.components[name] = duration;

    // Log for debugging in development
    if (process.env.NODE_ENV !== "production") {
      console.debug(`⚡ ${name}: ${duration.toFixed(2)}ms`);
    }

    return result;
  } catch (error) {
    // Log performance measurement errors
    PERFORMANCE_METRICS.errors.push({
      component: name,
      error: error.message,
      time: performance.now(),
    });

    // Rethrow to ensure original error handling still applies
    throw error;
  }
}

/**
 * Reports performance metrics to the console or analytics
 */
function reportPerformance() {
  // Calculate total initialization time
  const totalTime = performance.now() - PERFORMANCE_METRICS.init;
  PERFORMANCE_METRICS.total = totalTime;

  // Report to analytics in production
  if (process.env.NODE_ENV === "production" && window.gtag) {
    gtag("event", "performance", {
      event_category: "timing",
      event_label: "initialization",
      value: Math.round(totalTime),
    });
  }

  // Log in development or when debug is enabled
  if (process.env.NODE_ENV !== "production" || localStorage.getItem("debug")) {
    console.debug("📊 Performance Metrics:", PERFORMANCE_METRICS);
  }
}

/**
 * Initialize the application when the DOM is ready
 */
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

/**
 * Main initialization function
 *
 * This function orchestrates the initialization of all components in a prioritized manner:
 * 1. High-priority components (critical for page functionality)
 * 2. Medium-priority components (enhance the user experience)
 * 3. Low-priority components (can be delayed until the browser is idle)
 *
 * @returns {void}
 */
function init() {
  // Mark initialization start
  performance.mark("init-start");

  // Create and show page loader
  showPageLoader();

  // Initialize critical components immediately
  trackPerformance("highPriority", initHighPriority);

  // Schedule lower priority initializations for better performance
  requestAnimationFrame(() => {
    // Initialize medium priority components in the next animation frame
    trackPerformance("mediumPriority", initMediumPriority);

    // Schedule non-critical components for when browser is idle
    requestIdleCallback(() => {
      trackPerformance("lowPriority", initLowPriority);

      // Report performance after all components are initialized
      reportPerformance();
    });
  });

  // Hide loader when everything is fully loaded
  window.addEventListener("load", () => {
    hidePageLoader();

    // Register service worker for caching if supported
    registerServiceWorker();
  });

  // Mark initialization complete
  performance.mark("init-end");
  performance.measure("total-init", "init-start", "init-end");
}

/**
 * Initialize high priority components
 *
 * These components are critical for page functionality and user experience,
 * so they run immediately during page load.
 *
 * @returns {void}
 */
function initHighPriority() {
  // Initialize site configuration if available
  if (window.SITE_DATA) {
    trackPerformance("siteConfig", () => initSiteConfig(window.SITE_DATA));
  }

  // Set up accessibility features
  trackPerformance("accessibility", setupAccessibility);

  // Initialize theme system (dark/light mode)
  trackPerformance("themeToggle", initThemeToggle);

  // Initialize analytics if configured (using dynamic import for performance)
  if (window.analyticsId) {
    import("./utils/analytics.js")
      .then((module) => {
        trackPerformance("analytics", () =>
          module.initGoogleAnalytics(window.analyticsId)
        );
      })
      .catch((error) => {
        console.error("Failed to load analytics:", error);
        PERFORMANCE_METRICS.errors.push({
          component: "analytics",
          error: error.message,
          time: performance.now(),
        });
      });
  }
}

/**
 * Initialize medium priority components
 *
 * These components enhance the page but aren't critical for initial rendering.
 * They run after high priority items but before page is fully loaded.
 *
 * @returns {void}
 */
function initMediumPriority() {
  // Initialize page layout components
  trackPerformance("responsiveLayout", setupResponsiveLayout);

  // Initialize scroll-based components (back to top button, etc.)
  trackPerformance("scrollEffects", setupScrollEffects);

  // Initialize joke generator (content enhancement) - using dynamic import
  if (document.querySelector("#joke-container")) {
    import("./components/joke-generator.js")
      .then((module) => {
        trackPerformance("jokeGenerator", module.initJokeGenerator);
      })
      .catch((error) => {
        console.error("Failed to load joke generator:", error);
      });
  }
}

/**
 * Initialize low priority components
 *
 * These components are non-critical and can wait until the browser is idle.
 * They run when browser has spare capacity.
 *
 * @returns {void}
 */
function initLowPriority() {
  // Initialize search functionality (only if search input exists)
  if (document.querySelector("#search-input")) {
    import("./components/search.js")
      .then((module) => {
        trackPerformance("search", module.initSearch);
      })
      .catch((error) => {
        console.error("Failed to load search:", error);
      });
  }

  // Add entrance animations
  trackPerformance("animations", setupAnimations);

  // Set up event delegation for common interactions
  trackPerformance("eventDelegation", setupEventDelegation);

  // Initialize code highlighting for blog posts
  if (document.querySelector("pre code")) {
    import("./components/code-highlight.js")
      .then((module) => {
        trackPerformance("codeHighlight", module.initCodeHighlight);
      })
      .catch((error) => {
        console.error("Failed to load code highlighter:", error);
      });
  }

  // Initialize static fallbacks for dynamic content
  import("./components/static-fallbacks.js")
    .then((module) => {
      trackPerformance("staticFallbacks", module.initStaticFallbacks);
    })
    .catch((error) => {
      console.error("Failed to load static fallbacks:", error);
    });
}

/**
 * Register the service worker for caching and offline support
 */
function registerServiceWorker() {
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker
        .register("/service-worker.js")
        .then((registration) => {
          console.log("Service Worker registered with scope:", registration.scope);
        })
        .catch((error) => {
          console.error("Service Worker registration failed:", error);
        });
    });
  }
}

/**
 * Shows the page loader during initialization
 *
 * Creates a loading indicator and appends it to the document body
 * if it doesn't already exist.
 *
 * @returns {void}
 */
function showPageLoader() {
  let loader = document.getElementById("page-loader");

  // Create loader if it doesn't exist
  if (!loader) {
    loader = document.createElement("div");
    loader.id = "page-loader";
    loader.className = "page-loader";
    loader.innerHTML = `
      <div class="loader-spinner"></div>
      <div class="loader-text">Loading...</div>
    `;
    document.body.appendChild(loader);
  }
}

/**
 * Hides the page loader with a transition effect
 *
 * @returns {void}
 */
function hidePageLoader() {
  const pageLoader = document.getElementById("page-loader");
  if (pageLoader) {
    // Add class for fade-out transition
    pageLoader.classList.add("page-loader-hidden");

    // Remove from DOM after transition completes
    setTimeout(() => {
      pageLoader.remove();
    }, 500); // Match transition duration
  }
}

/**
 * Sets up accessibility features
 *
 * This includes skip links, proper ARIA attributes, and other
 * enhancements for screen readers and keyboard navigation.
 *
 * @returns {void}
 */
function setupAccessibility() {
  // Add skip link for keyboard users
  if (!document.querySelector(".skip-link")) {
    const skipLink = document.createElement("a");
    skipLink.href = "#main-content";
    skipLink.className = "skip-link";
    skipLink.textContent = "Skip to content";
    document.body.prepend(skipLink);
  }

  // Ensure main content is properly marked for skip link
  const mainContent = document.querySelector("main");
  if (mainContent && !mainContent.id) {
    mainContent.id = "main-content";
    mainContent.setAttribute("tabindex", "-1"); // Make focusable but not in tab order
  }

  // Mark current navigation items for screen readers
  const navItems = document.querySelectorAll("nav a");
  navItems.forEach((item) => {
    if (window.location.pathname === item.getAttribute("href")) {
      item.setAttribute("aria-current", "page");
    }
  });
}

/**
 * Sets up responsive layout adjustments
 *
 * Handles any dynamic layout changes based on viewport size
 * or device capabilities.
 *
 * @returns {void}
 */
function setupResponsiveLayout() {
  // This is a placeholder for responsive layout handling
  // Actual implementation can include media query listeners,
  // viewport adjustments, etc.
}

/**
 * Sets up scroll-based effects
 *
 * Initializes components and effects that respond to page scrolling,
 * such as the back-to-top button and scroll animations.
 *
 * @returns {void}
 */
function setupScrollEffects() {
  // Back to top button functionality
  const backToTopBtn = document.getElementById("back-to-top");
  if (backToTopBtn) {
    // Show/hide button based on scroll position
    window.addEventListener("scroll", () => {
      // Show button when scrolled down
      if (window.scrollY > 300) {
        backToTopBtn.classList.add("visible");
        backToTopBtn.classList.remove("hidden");
      } else {
        // Hide button when near top
        backToTopBtn.classList.remove("visible");
        backToTopBtn.classList.add("hidden");
      }
    });

    // Scroll to top when clicked with smooth behavior
    backToTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }
}

/**
 * Sets up animations for visible elements
 *
 * Uses IntersectionObserver to trigger animations when elements
 * enter the viewport, with a fallback for older browsers.
 *
 * @returns {void}
 */
function setupAnimations() {
  // Only use modern animation approach if IntersectionObserver is supported
  if ("IntersectionObserver" in window) {
    // Create an observer to watch for elements entering viewport
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Animate the element when it enters viewport
            animateElement(entry.target);
            // Stop observing once animation is triggered
            observer.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: "50px", // Start animation slightly before element enters viewport
        threshold: 0.1, // Trigger when at least 10% of element is visible
      }
    );

    // List of elements to animate on page load
    const elementsToAnimate = [
      ".gh-profile-header",
      ".gh-section-header",
      ".gh-post-item",
      ".gh-post-card",
    ];

    // Observe all matching elements
    elementsToAnimate.forEach((selector) => {
      document.querySelectorAll(selector).forEach((el) => {
        observer.observe(el);
      });
    });
  } else {
    // Fallback for browsers without IntersectionObserver
    animateAllElements();
  }
}

/**
 * Animates a specific element with fade and slide effects
 *
 * @param {Element} el - Element to animate
 * @param {number} index - Optional index for staggered animations
 * @returns {void}
 */
function animateElement(el, index = 0) {
  // Set initial invisible state
  el.style.opacity = "0";

  // Apply animations with CSS
  el.style.animation = `fadeIn 0.6s ease-out forwards, slideUp 0.6s ease-out forwards`;

  // Stagger animation timing based on index
  el.style.animationDelay = `${0.05 + index * 0.05}s`;
}

/**
 * Animates all elements (fallback for older browsers)
 *
 * @returns {void}
 */
function animateAllElements() {
  // List of elements to animate
  const elementsToAnimate = [
    ".gh-profile-header",
    ".gh-section-header",
    ".gh-post-item",
    ".gh-post-card",
  ];

  // Apply animations to all elements
  elementsToAnimate.forEach((selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, i) => {
      // Set initial invisible state
      el.style.opacity = "0";

      // Apply animations with staggered timing
      el.style.animation = `fadeIn 0.5s ease-out forwards, slideUp 0.5s ease-out forwards`;
      el.style.animationDelay = `${0.05 + i * 0.05}s`;
    });
  });
}

/**
 * Sets up event delegation for common interactions
 *
 * Uses event bubbling to efficiently handle events on multiple elements
 * without attaching individual event listeners.
 *
 * @returns {void}
 */
function setupEventDelegation() {
  // Handle clicks throughout the document
  document.addEventListener("click", (e) => {
    // Post card click handling - navigate to post if not clicking on a specific link
    const postCard = e.target.closest(".gh-post-card");
    if (postCard && !e.target.closest("a")) {
      // Find the post title link and navigate to its href
      const postLink = postCard.querySelector(".gh-post-title")?.getAttribute("href");
      if (postLink) {
        window.location.href = postLink;
      }
    }

    // Additional delegated event handlers can be added here
  });
}

/**
 * Polyfill for requestIdleCallback
 *
 * Provides a fallback implementation for browsers that don't support
 * the requestIdleCallback API.
 *
 * @type {Function}
 */
const requestIdleCallback =
  window.requestIdleCallback ||
  function (cb) {
    const start = Date.now();
    return setTimeout(() => {
      cb({
        didTimeout: false,
        timeRemaining: () => Math.max(0, 50 - (Date.now() - start)),
      });
    }, 1);
  };
