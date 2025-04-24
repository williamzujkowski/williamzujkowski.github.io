/**
 * site-enhancements.js
 * Various site-wide enhancements and utilities
 */

(function () {
  // Utility functions
  function ready(fn) {
    if (document.readyState !== "loading") {
      fn();
    } else {
      document.addEventListener("DOMContentLoaded", fn);
    }
  }

  // Simple polyfill for requestIdleCallback for browsers that don't support it
  if (!window.requestIdleCallback) {
    window.requestIdleCallback = function (cb) {
      const start = Date.now();
      return setTimeout(function () {
        cb({
          didTimeout: false,
          timeRemaining: function () {
            return Math.max(0, 50 - (Date.now() - start));
          },
        });
      }, 1);
    };
  }

  // External links handling - open in new tab and add security attributes
  function setupExternalLinks() {
    const externalLinks = Array.from(document.querySelectorAll('a[href^="http"]'));

    externalLinks.forEach((link) => {
      const href = link.getAttribute("href");
      const isExternal = !href.startsWith(window.location.origin);

      if (isExternal) {
        // Only modify external links
        if (!link.hasAttribute("target")) {
          link.setAttribute("target", "_blank");
        }
        if (!link.hasAttribute("rel")) {
          link.setAttribute("rel", "noopener noreferrer");
        }
      }
    });
  }

  // Add current year to footer copyright if .copyright-year element exists
  function updateCopyrightYear() {
    const yearElem = document.querySelector(".copyright-year");
    if (yearElem) {
      const currentYear = new Date().getFullYear();
      yearElem.textContent = currentYear;
    }
  }

  // Enhance code blocks with features like copy-to-clipboard
  function enhanceCodeBlocks() {
    const codeBlocks = document.querySelectorAll("pre code");

    if (codeBlocks.length === 0) return;

    // Wait for idle time to enhance code blocks (non-critical)
    window.requestIdleCallback(
      () => {
        codeBlocks.forEach((codeBlock, index) => {
          const pre = codeBlock.parentNode;
          const wrapper = document.createElement("div");
          wrapper.className = "code-block-wrapper relative group";

          // Create copy button
          const copyButton = document.createElement("button");
          copyButton.className =
            "copy-code-button absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity bg-gray-700 hover:bg-gray-600 text-white rounded px-2 py-1 text-xs";
          copyButton.textContent = "Copy";
          copyButton.setAttribute("aria-label", "Copy code to clipboard");
          copyButton.dataset.index = index;

          // Copy functionality
          copyButton.addEventListener("click", () => {
            const code = codeBlock.textContent;
            navigator.clipboard
              .writeText(code)
              .then(() => {
                // Change button text temporarily
                copyButton.textContent = "Copied!";
                setTimeout(() => {
                  copyButton.textContent = "Copy";
                }, 2000);
              })
              .catch((err) => {
                console.error("Failed to copy code:", err);
                copyButton.textContent = "Error!";
                setTimeout(() => {
                  copyButton.textContent = "Copy";
                }, 2000);
              });
          });

          // Insert the wrapper and button
          pre.parentNode.insertBefore(wrapper, pre);
          wrapper.appendChild(pre);
          wrapper.appendChild(copyButton);
        });
      },
      { timeout: 2000 }
    );
  }

  // Initialize all enhancements
  function init() {
    updateCopyrightYear();
    setupExternalLinks();
    enhanceCodeBlocks();
  }

  // Run when DOM is ready
  ready(init);
})();
