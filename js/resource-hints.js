/**
 * resource-hints.js - Performance optimization via resource hints
 */

(function () {
  /**
   * Add preconnect hint for external domain
   * @param {string} url - The URL to preconnect to
   */
  function addPreconnect(url) {
    if (!url || !document.head) return;

    // Check if preconnect already exists
    const existingHint = document.querySelector(
      `link[rel="preconnect"][href="${url}"]`
    );
    if (existingHint) return;

    // Create and append preconnect hint
    const hint = document.createElement("link");
    hint.rel = "preconnect";
    hint.href = url;
    hint.crossOrigin = "anonymous";
    document.head.appendChild(hint);
  }

  // Make function available globally
  window.initResourceHints = function () {
    // Preconnect to external domains
    addPreconnect("https://v2.jokeapi.dev");

    // Other resource hints would be added here

    return true;
  };

  // Run automatically if document is ready
  if (document.readyState !== "loading") {
    window.initResourceHints();
  } else {
    document.addEventListener("DOMContentLoaded", window.initResourceHints);
  }
})();
