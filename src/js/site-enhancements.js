/**
 * site-enhancements.js - Optimized UI enhancing functionality
 *
 * Optimized features:
 * - Prioritized back-to-top button creation
 * - Improved native lazy loading with IntersectionObserver fallback
 * - Optimized reading time calculation
 * - Performance-optimized page transitions
 * - Deferred tooltip creation
 * - Progressive enhancement for accessibility
 */

// Use requestIdleCallback with fallback for non-critical operations
const requestIdleCallback =
  window.requestIdleCallback ||
  ((cb) => setTimeout(() => cb({ didTimeout: false }), 50));

// Initialize feature flags
const featureFlags = {
  enableTooltips: true,
  enablePageTransitions: true,
  prioritizeImages: true,
};

// Initialize features with prioritization
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initFeaturesWithPriority);
} else {
  initFeaturesWithPriority();
}

// Entry point - prioritize feature initialization
function initFeaturesWithPriority() {
  // HIGH priority (run immediately)
  initScrollToTopButton();
  setupNativeLazyLoading();
  document.body.classList.add("page-transition-enter");

  // MEDIUM priority (run during idle animation frame)
  requestAnimationFrame(() => {
    calculateReadingTime();
    initPageTransitions();

    // LOW priority (run when browser is idle)
    requestIdleCallback(() => {
      // These features can wait
      enhanceAccessibility();
      if (featureFlags.enableTooltips) {
        initTooltips();
      }
    });
  });
}

/**
 * Initialize back-to-top button functionality
 * High priority - affects UX immediately
 */
function initScrollToTopButton() {
  // First try to find an existing button in the DOM
  let button = document.getElementById("back-to-top");

  // If no button exists, create it
  if (!button) {
    button = document.createElement("button");
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
      <path d="M3.22 9.78c-.293-.293-.293-.767 0-1.06l4.25-4.25a.75.75 0 011.06 0l4.25 4.25a.75.75 0 01-1.06 1.06L8 6.06 4.28 9.78c-.293.293-.767.293-1.06 0z"></path>
    </svg>`;
    button.className = "scroll-top-btn hidden";
    button.id = "back-to-top";
    button.setAttribute("aria-label", "Scroll to top");
    document.body.appendChild(button);
  }

  // Passive listener for better scrolling performance
  let lastScrollY = 0;
  let ticking = false;

  window.addEventListener(
    "scroll",
    () => {
      lastScrollY = window.scrollY;

      if (!ticking) {
        window.requestAnimationFrame(() => {
          if (lastScrollY > 300) {
            button.classList.remove("hidden");
            button.classList.add("visible");
          } else {
            button.classList.remove("visible");
            button.classList.add("hidden");
          }
          ticking = false;
        });
        ticking = true;
      }
    },
    { passive: true }
  );

  // Scroll to top when clicked
  button.addEventListener("click", () => {
    // Check for smooth scroll support and use it when available
    if ("scrollBehavior" in document.documentElement.style) {
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else {
      // Fallback smooth scrolling for older browsers
      const scrollToTop = () => {
        const currentPosition = window.scrollY;
        if (currentPosition > 0) {
          window.scrollTo(0, currentPosition - currentPosition / 8);
          window.requestAnimationFrame(scrollToTop);
        }
      };
      window.requestAnimationFrame(scrollToTop);
    }
  });
}

/**
 * Use native lazy loading with IntersectionObserver as fallback
 * High priority - improves initial load performance
 */
function setupNativeLazyLoading() {
  // Check if native lazy loading is supported
  const hasNativeLazy = "loading" in HTMLImageElement.prototype;

  // Process all images that need lazy loading
  const images = document.querySelectorAll("img[data-src]");
  if (!images.length) return;

  if (hasNativeLazy) {
    // Use native lazy loading
    images.forEach((img) => {
      if (img.dataset.src) {
        img.loading = "lazy";
        img.src = img.dataset.src;
        img.removeAttribute("data-src");

        if (img.dataset.srcset) {
          img.srcset = img.dataset.srcset;
          img.removeAttribute("data-srcset");
        }
      }
    });
  } else {
    // Fallback to IntersectionObserver
    if ("IntersectionObserver" in window) {
      const lazyImageObserver = new IntersectionObserver(
        (entries) => {
          entries.forEach((entry) => {
            if (entry.isIntersecting) {
              const img = entry.target;

              if (img.dataset.src) {
                img.src = img.dataset.src;
                img.removeAttribute("data-src");

                if (img.dataset.srcset) {
                  img.srcset = img.dataset.srcset;
                  img.removeAttribute("data-srcset");
                }

                img.classList.add("loaded");
                lazyImageObserver.unobserve(img);
              }
            }
          });
        },
        {
          rootMargin: "200px", // Generous margin to start loading before visible
          threshold: 0.01,
        }
      );

      images.forEach((img) => lazyImageObserver.observe(img));
    } else {
      // Legacy fallback - load all immediately
      images.forEach((img) => {
        if (img.dataset.src) {
          img.src = img.dataset.src;
          img.removeAttribute("data-src");

          if (img.dataset.srcset) {
            img.srcset = img.dataset.srcset;
            img.removeAttribute("data-srcset");
          }
        }
      });
    }
  }
}

/**
 * Calculate and display reading time for blog posts
 * Medium priority - doesn't need to be immediate
 */
function calculateReadingTime() {
  const articleContent = document.querySelector(".prose");
  const readingTimeElement = document.getElementById("reading-time");

  if (articleContent && readingTimeElement) {
    // Get text content & remove excess whitespace
    const text = articleContent.textContent.trim();

    // Use a faster word count algorithm for long content
    const wordCount =
      text.length > 1000 ? estimateWordCount(text) : text.split(/\s+/).length;

    // Adjust reading time based on word count - 200 is average reading speed
    const baseReadingTime = wordCount / 200;
    const readingTime = Math.max(1, Math.ceil(baseReadingTime));

    readingTimeElement.textContent = `${readingTime} min read`;
    readingTimeElement.classList.remove("hidden");
  }
}

// Faster word count estimation for long text
function estimateWordCount(text) {
  // Sample method - count spaces and add 1 (simple approximation)
  return (text.match(/\s+/g) || []).length + 1;
}

/**
 * Add smooth page transitions for internal links
 * Medium priority - enhances navigation experience
 */
function initPageTransitions() {
  if (!featureFlags.enablePageTransitions) return;

  const isReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (isReducedMotion) return; // Skip animations for users who prefer reduced motion

  document
    .querySelectorAll('a[href^="/"]:not([href^="#"]):not([target="_blank"])')
    .forEach((link) => {
      // Use event delegation to improve performance
      link.addEventListener("click", (e) => {
        // Only process internal links
        if (link.hostname === window.location.hostname) {
          e.preventDefault();
          const destination = link.href;

          // Prefetch the page for faster loading
          if ("requestIdleCallback" in window) {
            const prefetcher = document.createElement("link");
            prefetcher.rel = "prefetch";
            prefetcher.href = destination;
            document.head.appendChild(prefetcher);
          }

          // Add exit animation class to body
          document.body.classList.add("page-transition-exit");

          // Navigate after transition
          setTimeout(() => {
            window.location.href = destination;
          }, 300);
        }
      });
    });
}

/**
 * Initialize tooltips for elements with data-tooltip attribute
 * Low priority - enhance experience but not critical
 */
function initTooltips() {
  // Create tooltip container once for all tooltips
  const tooltipContainer = document.createElement("div");
  tooltipContainer.className =
    "fixed z-50 p-2 bg-gray-light text-text text-xs rounded-github border border-border shadow-md opacity-0 transition-opacity duration-200 pointer-events-none";
  tooltipContainer.id = "tooltip-container";
  tooltipContainer.setAttribute("aria-hidden", "true");
  tooltipContainer.style.visibility = "hidden";
  document.body.appendChild(tooltipContainer);

  // Add event listeners to elements with tooltips
  document.querySelectorAll("[data-tooltip]").forEach((element) => {
    element.addEventListener("mouseenter", () => {
      // Position the tooltip
      const rect = element.getBoundingClientRect();
      tooltipContainer.textContent = element.getAttribute("data-tooltip");
      tooltipContainer.style.top = `${rect.top - tooltipContainer.offsetHeight - 5}px`;
      tooltipContainer.style.left = `${rect.left + rect.width / 2 - tooltipContainer.offsetWidth / 2}px`;

      // Show the tooltip
      tooltipContainer.style.visibility = "visible";
      tooltipContainer.style.opacity = "1";
    });

    element.addEventListener("mouseleave", () => {
      // Hide the tooltip
      tooltipContainer.style.opacity = "0";
      setTimeout(() => {
        if (tooltipContainer.style.opacity === "0") {
          tooltipContainer.style.visibility = "hidden";
        }
      }, 200);
    });
  });
}

/**
 * Enhance accessibility with better focus states
 * Low priority - can be applied progressively
 */
function enhanceAccessibility() {
  // Focus visible only for keyboard navigation
  const focusableElements = document.querySelectorAll(
    "a, button, input, select, textarea"
  );

  let usingMouse = false;

  // Track input method
  window.addEventListener("mousedown", () => {
    usingMouse = true;
  });

  window.addEventListener("keydown", (e) => {
    if (e.key === "Tab") {
      usingMouse = false;
    }
  });

  // Apply focus styles only to elements that don't already have them
  focusableElements.forEach((element) => {
    if (!element.classList.contains("focus-handled")) {
      // Add base classes
      element.classList.add("focus-handled");

      // Only show focus styles for keyboard navigation
      element.addEventListener("focus", () => {
        if (!usingMouse) {
          element.classList.add("focus-visible");
        }
      });

      element.addEventListener("blur", () => {
        element.classList.remove("focus-visible");
      });
    }
  });
}

// Add page entrance animation after navigation - immediate priority
window.addEventListener("pageshow", (event) => {
  // Check for reduced motion preference
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    return; // Skip animation
  }

  // Add transition class
  document.body.classList.add("page-transition-enter");

  // Remove after animation completes
  setTimeout(() => {
    document.body.classList.remove("page-transition-enter");
  }, 500);
});
