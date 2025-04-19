/**
 * main.js - Application entry point
 *
 * Initializes all components and provides core functionality
 */

// Import components
import { initSearch } from "./components/search.js";
import { initThemeToggle } from "./components/theme-toggle.js";
import { initCodeHighlight } from "./components/code-highlight.js";
import { initStaticFallbacks } from "./components/static-fallbacks.js";
import { initGoogleAnalytics } from "./utils/analytics.js";
import { initJokeGenerator } from "./components/joke-generator.js";
import { initSiteConfig } from "./utils/site-config.js";

// DOM ready state check - run initialization when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}

/**
 * Initialize the application
 */
function init() {
  // Create and show page loader
  showPageLoader();

  // Initialize components
  initHighPriority();

  // Schedule lower priority initializations
  requestAnimationFrame(() => {
    // Initialize medium priority components
    initMediumPriority();

    // Schedule low priority components for when browser is idle
    requestIdleCallback(initLowPriority);
  });

  // Hide loader when everything is fully loaded
  window.addEventListener("load", hidePageLoader);
}

/**
 * Initialize high priority components
 * These run immediately during page load
 */
function initHighPriority() {
  // Initialize site configuration
  if (window.SITE_DATA) {
    initSiteConfig(window.SITE_DATA);
  }

  // Set up accessibility features
  setupAccessibility();

  // Initialize theme
  initThemeToggle();

  // Initialize analytics if configured
  if (window.analyticsId) {
    initGoogleAnalytics(window.analyticsId);
  }
}

/**
 * Initialize medium priority components
 * These run after high priority items but before page is fully loaded
 */
function initMediumPriority() {
  // Initialize page layout components
  setupResponsiveLayout();

  // Initialize scroll-based components
  setupScrollEffects();

  // Initialize joke generator
  initJokeGenerator();
}

/**
 * Initialize low priority components
 * These run when browser is idle
 */
function initLowPriority() {
  // Initialize search
  initSearch();

  // Add animations
  setupAnimations();

  // Set up event delegation for common interactions
  setupEventDelegation();

  // Initialize code highlighting for blog posts
  initCodeHighlight();

  // Initialize static fallbacks
  initStaticFallbacks();
}

/**
 * Show page loader
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
 * Hide page loader
 */
function hidePageLoader() {
  const pageLoader = document.getElementById("page-loader");
  if (pageLoader) {
    pageLoader.classList.add("page-loader-hidden");
    setTimeout(() => {
      pageLoader.remove();
    }, 500);
  }
}

/**
 * Set up accessibility features
 */
function setupAccessibility() {
  // Add skip link if it doesn't exist
  if (!document.querySelector(".skip-link")) {
    const skipLink = document.createElement("a");
    skipLink.href = "#main-content";
    skipLink.className = "skip-link";
    skipLink.textContent = "Skip to content";
    document.body.prepend(skipLink);
  }

  // Ensure main content is properly marked
  const mainContent = document.querySelector("main");
  if (mainContent && !mainContent.id) {
    mainContent.id = "main-content";
    mainContent.setAttribute("tabindex", "-1");
  }

  // Mark current navigation items
  const navItems = document.querySelectorAll("nav a");
  navItems.forEach((item) => {
    if (window.location.pathname === item.getAttribute("href")) {
      item.setAttribute("aria-current", "page");
    }
  });
}

/**
 * Set up responsive layout adjustments
 */
function setupResponsiveLayout() {
  // Responsive handling can be added here
}

/**
 * Set up scroll-based effects
 */
function setupScrollEffects() {
  // Back to top button
  const backToTopBtn = document.getElementById("back-to-top");
  if (backToTopBtn) {
    // Show/hide button based on scroll position
    window.addEventListener("scroll", () => {
      if (window.scrollY > 300) {
        backToTopBtn.classList.add("visible");
        backToTopBtn.classList.remove("hidden");
      } else {
        backToTopBtn.classList.remove("visible");
        backToTopBtn.classList.add("hidden");
      }
    });

    // Scroll to top when clicked
    backToTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
    });
  }
}

/**
 * Set up animations for visible elements
 */
function setupAnimations() {
  // Only animate elements in viewport if supported
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            animateElement(entry.target);
            observer.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: "50px",
        threshold: 0.1,
      }
    );

    // Elements to animate on page load
    const elementsToAnimate = [
      ".gh-profile-header",
      ".gh-section-header",
      ".gh-post-item",
      ".gh-post-card",
    ];

    // Observe elements
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
 * Animate a specific element
 * @param {Element} el - Element to animate
 * @param {number} index - Optional index for staggered animations
 */
function animateElement(el, index = 0) {
  el.style.opacity = "0";
  el.style.animation = `fadeIn 0.6s ease-out forwards, slideUp 0.6s ease-out forwards`;
  el.style.animationDelay = `${0.05 + index * 0.05}s`;
}

/**
 * Animate all elements (fallback)
 */
function animateAllElements() {
  const elementsToAnimate = [
    ".gh-profile-header",
    ".gh-section-header",
    ".gh-post-item",
    ".gh-post-card",
  ];

  elementsToAnimate.forEach((selector) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, i) => {
      el.style.opacity = "0";
      el.style.animation = `fadeIn 0.5s ease-out forwards, slideUp 0.5s ease-out forwards`;
      el.style.animationDelay = `${0.05 + i * 0.05}s`;
    });
  });
}

/**
 * Set up event delegation for common interactions
 */
function setupEventDelegation() {
  // Example: Handle clicks on post cards
  document.addEventListener("click", (e) => {
    // Post card click - navigate to post if not clicking on a specific link
    const postCard = e.target.closest(".gh-post-card");
    if (postCard && !e.target.closest("a")) {
      const postLink = postCard.querySelector(".gh-post-title")?.getAttribute("href");
      if (postLink) {
        window.location.href = postLink;
      }
    }
  });
}

// Polyfill for requestIdleCallback
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
