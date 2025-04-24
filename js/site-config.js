/**
 * site-config.js
 *
 * Centralized management of site configuration.
 * This script initializes the window.siteConfig object
 * which is used by various components.
 */

(function () {
  // Make function available globally
  window.initSiteConfig = function (siteData) {
    // Set site configuration on the window object
    window.siteConfig = siteData;

    // Return the config for direct use
    return siteData;
  };

  // Initialize with any existing data
  if (window.SITE_DATA) {
    window.initSiteConfig(window.SITE_DATA);
  }
})();
