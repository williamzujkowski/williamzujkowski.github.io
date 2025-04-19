/**
 * theme-switcher.js - Theme management and switching functionality
 *
 * This module loads theme configuration and applies it to the document
 * by setting CSS variables. It also provides functionality for theme switching.
 */

import { applyTheme } from "./theme-utils.js";

// Default theme name
const DEFAULT_THEME = "github-dark";

/**
 * Initialize theme from configuration
 * Loads theme from site config and applies it to the document
 * @param {Object} themeConfig - Optional theme configuration object
 */
export function initTheme(themeConfig = null) {
  try {
    // First check for a saved preference
    const savedTheme = getSavedTheme();

    // If no saved theme and no theme config provided,
    // try to load it from the window object (set by the Eleventy template)
    if (!savedTheme && !themeConfig && window.siteConfig?.theme) {
      themeConfig = window.siteConfig.theme;
    }

    // Apply the theme if we have one
    if (themeConfig) {
      applyTheme(themeConfig);
    } else if (savedTheme) {
      // This will be implemented when multiple themes are supported
      loadTheme(savedTheme).catch((error) => {
        console.error("Failed to load saved theme:", error);
        // Fall back to default
        document.documentElement.classList.add("dark");
      });
    }

    // Add theme toggle functionality
    setupThemeToggle();
  } catch (error) {
    console.error("Error initializing theme:", error);
    // Ensure dark mode is applied as fallback
    document.documentElement.classList.add("dark");
  }
}

/**
 * Get saved theme preference from localStorage
 * @returns {string|null} Saved theme name or null if none
 */
function getSavedTheme() {
  return localStorage.getItem("preferred-theme");
}

/**
 * Setup theme toggle button if it exists
 */
function setupThemeToggle() {
  const themeToggle = document.getElementById("theme-toggle");
  if (!themeToggle) return;

  themeToggle.addEventListener("click", () => {
    // Show a notification that this will be implemented in a future update
    alert(
      "Theme switching will be available in a future update! Currently using the GitHub Dark theme."
    );

    // You could also toggle between light/dark mode in the future:
    // document.documentElement.classList.toggle('dark');
  });
}

/**
 * Load a theme by name
 * @param {string} themeName - Name of the theme to load
 * @returns {Promise<boolean>} Success status
 */
export async function loadTheme(themeName) {
  try {
    // This would fetch a theme from a themes directory
    const response = await fetch(`/themes/${themeName}.json`);
    if (!response.ok) {
      throw new Error(`Failed to load theme: ${response.statusText}`);
    }

    const themeConfig = await response.json();
    applyTheme(themeConfig);

    // Save preference
    localStorage.setItem("preferred-theme", themeName);

    return true;
  } catch (error) {
    console.error(`Error loading theme '${themeName}':`, error);
    return false;
  }
}

/**
 * Set theme preference by name without immediately loading it
 * Useful for setting a preference that will apply on next page load
 * @param {string} themeName - Name of theme to save as preference
 */
export function setThemePreference(themeName) {
  localStorage.setItem("preferred-theme", themeName);
}

// Initialize theme when DOM is ready
document.addEventListener("DOMContentLoaded", initTheme);
