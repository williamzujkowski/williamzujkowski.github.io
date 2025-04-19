/**
 * theme-toggle.js - Theme toggling component
 *
 * Handles theme toggling between light and dark modes
 * and persists user preferences.
 */

import { getLocalData, setLocalData } from "../utils/storage.js";

// Constants
const THEME_STORAGE_KEY = "preferred-theme";
const DARK_CLASS = "dark";
const LIGHT_CLASS = "light";

/**
 * Initialize the theme toggle functionality
 */
export function initThemeToggle() {
  // Get the theme toggle button
  const toggleButton = document.getElementById("theme-toggle");
  if (!toggleButton) return;

  // Set up initial theme
  const currentTheme = getCurrentTheme();
  applyTheme(currentTheme);

  // Add event listener to toggle button
  toggleButton.addEventListener("click", () => {
    const newTheme = currentTheme === DARK_CLASS ? LIGHT_CLASS : DARK_CLASS;
    applyTheme(newTheme);
    setLocalData(THEME_STORAGE_KEY, newTheme);
  });
}

/**
 * Get the current theme from local storage or system preference
 * @returns {string} The current theme ('dark' or 'light')
 */
function getCurrentTheme() {
  // Check for stored preference
  const storedTheme = getLocalData(THEME_STORAGE_KEY);
  if (storedTheme === DARK_CLASS || storedTheme === LIGHT_CLASS) {
    return storedTheme;
  }

  // Check for system preference
  if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
    return DARK_CLASS;
  }

  // Default to dark theme
  return DARK_CLASS;
}

/**
 * Apply a theme to the document
 * @param {string} theme - The theme to apply ('dark' or 'light')
 */
function applyTheme(theme) {
  const root = document.documentElement;

  if (theme === LIGHT_CLASS) {
    root.classList.add(LIGHT_CLASS);
    root.classList.remove(DARK_CLASS);
    updateThemeIcon(LIGHT_CLASS);
  } else {
    root.classList.add(DARK_CLASS);
    root.classList.remove(LIGHT_CLASS);
    updateThemeIcon(DARK_CLASS);
  }
}

/**
 * Update the theme toggle icon based on current theme
 * @param {string} theme - The current theme ('dark' or 'light')
 */
function updateThemeIcon(theme) {
  const toggleButton = document.getElementById("theme-toggle");
  if (!toggleButton) return;

  // Currently using SVG inside the button, so we update the inner HTML
  if (theme === LIGHT_CLASS) {
    toggleButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
        <path d="M8 12.25A4.25 4.25 0 0 1 3.75 8 4.25 4.25 0 0 1 8 3.75 4.25 4.25 0 0 1 12.25 8 4.25 4.25 0 0 1 8 12.25ZM8 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm6.246-3.673a.75.75 0 0 1-.629.854 5.735 5.735 0 0 0-.4.082.75.75 0 0 1-.223-1.482 7.23 7.23 0 0 1 .509-.106.75.75 0 0 1 .743.652Zm-12.024.61a7.23 7.23 0 0 1 .508.107.75.75 0 1 1-.372 1.452 5.735 5.735 0 0 0-.4-.082.75.75 0 0 1 .264-1.478ZM12.323 3.68A.75.75 0 0 1 13 4.5v.085a.75.75 0 0 1-1.5 0V4.5a.75.75 0 0 1 .823-.82Zm-8.42.82a.75.75 0 0 1-.75.75h-.085a.75.75 0 0 1 0-1.5H3.154a.75.75 0 0 1 .749.75Zm7.57-4.27a.75.75 0 0 1 1.061 0l.354.354a.75.75 0 0 1-1.06 1.06l-.354-.353a.75.75 0 0 1 0-1.06Zm-6.06 1.06a.75.75 0 0 1-1.06 0l-.354-.353a.75.75 0 0 1 1.06-1.06l.354.353a.75.75 0 0 1 0 1.06ZM8 0a.75.75 0 0 1 .75.75v.085a.75.75 0 0 1-1.5 0V.75A.75.75 0 0 1 8 0Z"></path>
      </svg>
    `;
    toggleButton.setAttribute("aria-label", "Switch to dark theme");
    toggleButton.setAttribute("title", "Switch to dark theme");
  } else {
    toggleButton.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
        <path d="M9.598 1.591a.749.749 0 0 1 .785-.175 7.001 7.001 0 1 1-8.967 8.967.75.75 0 0 1 .961-.96 5.5 5.5 0 0 0 7.046-7.046.75.75 0 0 1 .175-.786Zm1.616 1.945a7 7 0 0 1-7.678 7.678 5.499 5.499 0 1 0 7.678-7.678Z"></path>
      </svg>
    `;
    toggleButton.setAttribute("aria-label", "Switch to light theme");
    toggleButton.setAttribute("title", "Switch to light theme");
  }
}

// Listen for system preference changes
if (window.matchMedia) {
  window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
    const newTheme = e.matches ? DARK_CLASS : LIGHT_CLASS;

    // Only apply if user hasn't set a preference
    if (!getLocalData(THEME_STORAGE_KEY)) {
      applyTheme(newTheme);
    }
  });
}
