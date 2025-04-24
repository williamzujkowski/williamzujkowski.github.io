/**
 * main.js - Fixed version that doesn't use ES6 imports
 */

(function () {
  // Performance metrics tracking
  window.PERFORMANCE_METRICS = {
    init: performance.now(),
    marks: {},
    measures: {},
    components: {},
    errors: [],
  };

  /**
   * Records performance timing for a specific operation
   */
  function trackPerformance(name, fn) {
    try {
      // Mark the start time
      const markName = `${name}-start`;
      performance.mark(markName);
      window.PERFORMANCE_METRICS.marks[markName] = performance.now();

      // Execute the function
      const result = fn();

      // Mark the end time
      const endMarkName = `${name}-end`;
      performance.mark(endMarkName);
      window.PERFORMANCE_METRICS.marks[endMarkName] = performance.now();

      // Measure the duration
      performance.measure(name, markName, endMarkName);

      // Store the duration in our metrics object
      const duration = performance.now() - window.PERFORMANCE_METRICS.marks[markName];
      window.PERFORMANCE_METRICS.components[name] = duration;

      console.debug(`⚡ ${name}: ${duration.toFixed(2)}ms`);

      return result;
    } catch (error) {
      // Log performance measurement errors
      window.PERFORMANCE_METRICS.errors.push({
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
    const totalTime = performance.now() - window.PERFORMANCE_METRICS.init;
    window.PERFORMANCE_METRICS.total = totalTime;

    // Report to analytics in production
    if (window.gtag) {
      gtag("event", "performance", {
        event_category: "timing",
        event_label: "initialization",
        value: Math.round(totalTime),
      });
    }

    // Log in development or when debug is enabled
    if (localStorage.getItem("debug")) {
      console.debug("📊 Performance Metrics:", window.PERFORMANCE_METRICS);
    }
  }

  /**
   * Initialize high priority components
   */
  function initHighPriority() {
    // Set up resource hints for performance optimization
    if (window.initResourceHints) {
      trackPerformance("resourceHints", window.initResourceHints);
    }

    // Initialize site configuration if available
    if (window.SITE_DATA && window.initSiteConfig) {
      trackPerformance("siteConfig", () => window.initSiteConfig(window.SITE_DATA));
    }

    // Set up accessibility features
    trackPerformance("accessibility", setupAccessibility);

    // Initialize theme system (dark/light mode)
    if (window.initThemeToggle) {
      trackPerformance("themeToggle", window.initThemeToggle);
    }
  }

  /**
   * Initialize medium priority components
   */
  function initMediumPriority() {
    // Initialize page layout components
    trackPerformance("responsiveLayout", setupResponsiveLayout);

    // Initialize scroll-based components (back to top button, etc.)
    trackPerformance("scrollEffects", setupScrollEffects);

    // Initialize joke generator
    if (
      document.querySelector("#joke-container") ||
      document.querySelector("#mobile-joke-container")
    ) {
      if (window.initJokeGenerator) {
        trackPerformance("jokeGenerator", window.initJokeGenerator);
      }
    }
  }

  /**
   * Initialize low priority components
   */
  function initLowPriority() {
    // Add entrance animations
    trackPerformance("animations", setupAnimations);

    // Set up event delegation for common interactions
    trackPerformance("eventDelegation", setupEventDelegation);
  }

  /**
   * Shows the page loader during initialization
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
   */
  function setupResponsiveLayout() {
    // This is a placeholder for responsive layout handling
  }

  /**
   * Sets up scroll-based effects
   */
  function setupScrollEffects() {
    // Back to top button functionality
    const backToTopBtn = document.getElementById("back-to-top");
    if (backToTopBtn) {
      // Add hardware acceleration class for smoother animations
      backToTopBtn.classList.add("gpu-accelerated");

      // Use passive event listener for better scroll performance
      let scrollTimeout;
      let isVisible = false;
      let lastScrollY = window.scrollY;

      // Use throttled scroll event to improve performance
      window.addEventListener(
        "scroll",
        () => {
          // Skip if we're still in timeout period
          if (scrollTimeout) return;

          // Create a timeout to limit executions
          scrollTimeout = setTimeout(() => {
            // Get current scroll position
            const currentScrollY = window.scrollY;

            // Only update if we've scrolled a significant amount or crossed the threshold
            const shouldBeVisible = currentScrollY > 300;
            if (
              shouldBeVisible !== isVisible ||
              Math.abs(currentScrollY - lastScrollY) > 50
            ) {
              // Update button visibility using requestAnimationFrame for smoother rendering
              requestAnimationFrame(() => {
                if (shouldBeVisible) {
                  backToTopBtn.classList.add("visible");
                  backToTopBtn.classList.remove("hidden");
                } else {
                  backToTopBtn.classList.remove("visible");
                  backToTopBtn.classList.add("hidden");
                }
                isVisible = shouldBeVisible;
                lastScrollY = currentScrollY;
              });
            }

            // Clear the timeout
            scrollTimeout = null;
          }, 100); // 100ms throttle
        },
        { passive: true }
      ); // Passive event improves scroll performance

      // Scroll to top when clicked with smooth behavior
      backToTopBtn.addEventListener("click", () => {
        // Check if scrollTo behavior is supported
        if ("scrollBehavior" in document.documentElement.style) {
          // Use native smooth scrolling
          window.scrollTo({
            top: 0,
            behavior: "smooth",
          });
        } else {
          // Fallback for browsers without smooth scrolling
          const scrollToTop = () => {
            const currentPosition = window.scrollY;
            if (currentPosition > 0) {
              // Use requestAnimationFrame for smoother animation
              requestAnimationFrame(scrollToTop);
              // Scroll by a percentage of the remaining distance
              window.scrollTo(0, currentPosition - currentPosition / 8);
            }
          };
          scrollToTop();
        }
      });
    }
  }

  /**
   * Sets up animations for visible elements
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
   */
  function animateElement(el, index = 0) {
    // Prepare element for animation with hardware acceleration
    el.style.opacity = "0";

    // Add hardware acceleration classes
    el.classList.add("gpu-accelerated");
    el.classList.add("animate-slide-up");

    // Clear any previous animation
    el.style.animation = "none";

    // Force browser to acknowledge the change before setting new animation
    void el.offsetWidth; // This triggers a reflow

    // Use requestAnimationFrame for smoother animation start
    requestAnimationFrame(() => {
      // Stagger animation timing based on index
      el.style.animationDelay = `${0.05 + index * 0.05}s`;

      // Cleanup: Remove hardware acceleration class when animation completes
      // This prevents memory issues from having too many accelerated elements
      el.addEventListener(
        "animationend",
        () => {
          // Keep the element visible but remove unnecessary acceleration hints
          if (el.classList.contains("gpu-accelerated")) {
            // Only modify will-change to prevent layout shifts
            el.style.willChange = "auto";
          }
        },
        { once: true }
      );
    });
  }

  /**
   * Animates all elements (fallback for older browsers)
   */
  function animateAllElements() {
    // List of elements to animate
    const elementsToAnimate = [
      ".gh-profile-header",
      ".gh-section-header",
      ".gh-post-item",
      ".gh-post-card",
    ];

    // Group animations to minimize layout thrashing
    const allElements = [];

    // Collect all elements first
    elementsToAnimate.forEach((selector) => {
      const elements = document.querySelectorAll(selector);
      elements.forEach((el) => allElements.push(el));
    });

    // Batch read operations
    allElements.forEach((el) => {
      // Initial setup - read operations
      el.style.opacity = "0";
      el.getBoundingClientRect(); // Force a reflow once to get current position
    });

    // Use requestAnimationFrame for the next visual update
    requestAnimationFrame(() => {
      // Batch write operations
      allElements.forEach((el, i) => {
        // Add hardware acceleration classes
        el.classList.add("gpu-accelerated");
        el.classList.add("animate-slide-up");

        // Stagger animation timing
        el.style.animationDelay = `${0.05 + i * 0.05}s`;

        // Clean up acceleration hints after animation completes
        el.addEventListener(
          "animationend",
          () => {
            if (el.classList.contains("gpu-accelerated")) {
              el.style.willChange = "auto";
            }
          },
          { once: true }
        );
      });
    });
  }

  /**
   * Sets up event delegation for common interactions
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
   * Main initialization function
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
      setTimeout(() => {
        trackPerformance("lowPriority", initLowPriority);

        // Report performance after all components are initialized
        reportPerformance();
      }, 0);
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

  // Initialize the application when the DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
