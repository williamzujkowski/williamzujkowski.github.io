/**
 * resource-hints.js - Performance optimization through resource hints
 *
 * This module manages resource hints like preload, prefetch, and preconnect
 * to improve page load performance.
 */

/**
 * Initialize resource hints for the current page
 * Based on the current page, different resources may be preloaded/prefetched
 *
 * @returns {boolean} True if resource hints were successfully added
 */
export function initResourceHints() {
  try {
    // Detect current page type
    const currentPath = window.location.pathname;

    // Add preconnect for external domains
    addPreconnect(["https://fonts.googleapis.com", "https://fonts.gstatic.com"]);

    // Add different hints based on page type
    if (currentPath.includes("/blog/")) {
      // Blog-specific resource hints
      addPreload(["/js/components/code-highlight.js", "/css/blog-enhanced.css"]);
    } else if (currentPath.includes("/dashboard/")) {
      // Dashboard-specific resource hints
      addPreload(["/js/components/charts.js"]);
    }

    return true;
  } catch (error) {
    console.error("Error initializing resource hints:", error);
    return false;
  }
}

/**
 * Add preconnect hints for external domains
 * @param {string[]} domains - Array of domains to preconnect to
 */
function addPreconnect(domains) {
  domains.forEach((domain) => {
    const link = document.createElement("link");
    link.rel = "preconnect";
    link.href = domain;
    link.crossOrigin = "anonymous";
    document.head.appendChild(link);
  });
}

/**
 * Add preload hints for critical resources
 * @param {string[]} resources - Array of resource URLs to preload
 */
function addPreload(resources) {
  resources.forEach((resource) => {
    const link = document.createElement("link");
    link.rel = "preload";
    link.href = resource;

    // Set as attribute based on file extension
    if (resource.endsWith(".js")) {
      link.as = "script";
    } else if (resource.endsWith(".css")) {
      link.as = "style";
    } else if (resource.endsWith(".woff2") || resource.endsWith(".woff")) {
      link.as = "font";
      link.crossOrigin = "anonymous";
    } else if (
      resource.endsWith(".jpg") ||
      resource.endsWith(".png") ||
      resource.endsWith(".webp") ||
      resource.endsWith(".svg")
    ) {
      link.as = "image";
    }

    document.head.appendChild(link);
  });
}

/**
 * Add prefetch hints for resources that may be needed soon
 * @param {string[]} resources - Array of resource URLs to prefetch
 */
function addPrefetch(resources) {
  resources.forEach((resource) => {
    const link = document.createElement("link");
    link.rel = "prefetch";
    link.href = resource;
    document.head.appendChild(link);
  });
}
