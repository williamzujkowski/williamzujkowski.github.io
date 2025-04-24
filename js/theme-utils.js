/**
 * theme-utils.js - Utilities for working with OKLCH color themes
 *
 * This module provides utilities for generating CSS variables from theme configuration
 * and helper functions for creating OKLCH color variants.
 */

(function () {
  // Color scale multipliers for consistent gradients
  const SCALE_MULTIPLIERS = {
    primaryChroma: {
      50: 0.33,
      100: 0.4,
      200: 0.53,
      300: 0.67,
      400: 0.8,
      500: 1,
      600: 0.87,
      700: 0.73,
      800: 0.6,
      900: 0.47,
      950: 0.27,
    },
    primaryLightness: {
      50: 0.92,
      100: 0.87,
      200: 0.82,
      300: 0.76,
      400: 0.66,
      500: 0.56,
      600: 0.46,
      700: 0.36,
      800: 0.26,
      900: 0.16,
      950: 0.11,
    },
    accentChroma: {
      50: 0.33,
      100: 0.47,
      200: 0.6,
      300: 0.73,
      400: 0.87,
      500: 1,
      600: 0.87,
      700: 0.73,
      800: 0.6,
      900: 0.47,
      950: 0.33,
    },
    accentLightness: {
      50: 0.95,
      100: 0.92,
      200: 0.87,
      300: 0.82,
      400: 0.76,
      500: 0.7,
      600: 0.6,
      700: 0.5,
      800: 0.4,
      900: 0.3,
      950: 0.2,
    },
  };

  // Default color values if not provided in theme
  const DEFAULT_COLORS = {
    primary: "oklch(0.56 0.15 145)",
    accent: "oklch(0.70 0.15 230)",
    background: "oklch(0.16 0.02 250)",
    surface: "oklch(0.20 0.02 250)",
    border: "oklch(0.30 0.02 250)",
    grayLight: "oklch(0.25 0.02 250)",
    text: "oklch(0.93 0.02 250)",
    textSecondary: "oklch(0.75 0.03 250)",
    muted: "oklch(0.65 0.02 250)",
    success: "oklch(0.56 0.15 145)",
    warning: "oklch(0.75 0.15 80)",
    danger: "oklch(0.65 0.15 25)",
    info: "oklch(0.70 0.15 230)",
  };

  /**
   * Generates CSS custom properties from theme configuration
   * @param {Object} theme - Theme configuration object
   * @returns {Object} CSS variables as key-value pairs
   */
  function generateThemeVariables(theme) {
    if (!theme || !theme.colors) {
      console.error("Invalid theme configuration");
      return {};
    }

    const variables = {
      // Primary color scale
      "--color-primary":
        theme.colors.primaryHue !== undefined
          ? `oklch(${theme.colors.primaryLightness} ${theme.colors.primaryChroma} ${theme.colors.primaryHue})`
          : theme.colors.primary || DEFAULT_COLORS.primary,
    };

    // Generate primary color scale (50-950)
    Object.keys(SCALE_MULTIPLIERS.primaryChroma).forEach((shade) => {
      variables[`--color-primary-${shade}`] = generateOklchColor(
        theme.colors.primaryHue,
        theme.colors.primaryChroma * SCALE_MULTIPLIERS.primaryChroma[shade],
        SCALE_MULTIPLIERS.primaryLightness[shade]
      );
    });

    // Accent color
    variables["--color-accent"] =
      theme.colors.accentHue !== undefined
        ? `oklch(${theme.colors.accentLightness} ${theme.colors.accentChroma} ${theme.colors.accentHue})`
        : theme.colors.accent || DEFAULT_COLORS.accent;

    // Generate accent color scale
    Object.keys(SCALE_MULTIPLIERS.accentChroma).forEach((shade) => {
      variables[`--color-accent-${shade}`] = generateOklchColor(
        theme.colors.accentHue,
        theme.colors.accentChroma * SCALE_MULTIPLIERS.accentChroma[shade],
        SCALE_MULTIPLIERS.accentLightness[shade]
      );
    });

    // UI Colors
    const uiColors = {
      "--color-background": ["backgroundColor", "background"],
      "--color-surface": ["surfaceColor", "surface"],
      "--color-border": ["borderColor", "border"],
      "--color-gray-light": ["grayLightColor", "grayLight"],
      "--color-text": ["textColor", "text"],
      "--color-text-secondary": ["textSecondaryColor", "textSecondary"],
      "--color-muted": ["mutedColor", "muted"],
    };

    // Add UI colors
    Object.entries(uiColors).forEach(([cssVar, [themeKey, defaultKey]]) => {
      variables[cssVar] = theme.colors[themeKey] || DEFAULT_COLORS[defaultKey];
    });

    // Alert/Status colors
    const statusColors = {
      "--color-success": ["successColor", "success"],
      "--color-warning": ["warningColor", "warning"],
      "--color-danger": ["dangerColor", "danger"],
      "--color-info": ["infoColor", "info"],
    };

    // Add status colors
    Object.entries(statusColors).forEach(([cssVar, [themeKey, defaultKey]]) => {
      variables[cssVar] = theme.colors[themeKey] || DEFAULT_COLORS[defaultKey];
    });

    // Add other theme properties
    Object.assign(variables, {
      // Shadows
      "--shadow-card": theme.shadows?.card || "0 0 0 1px oklch(0.30 0.02 250)",
      "--shadow-elevated":
        theme.shadows?.elevated ||
        "0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",

      // Borders
      "--border-radius": theme.borders?.radius || "6px",
      "--border-width": theme.borders?.width || "1px",

      // Animation
      "--transition": theme.animation?.transition || "0.3s ease",
      "--hover-transform": theme.animation?.hover || "-translate-y-1",
    });

    return variables;
  }

  /**
   * Generates an OKLCH color string
   * @param {number} hue - The hue value (0-360)
   * @param {number} chroma - The chroma/saturation value (0-0.4 typically)
   * @param {number} lightness - The lightness value (0-1)
   * @returns {string} OKLCH color string
   */
  function generateOklchColor(hue, chroma, lightness) {
    // Ensure values are within range
    hue = Math.max(0, Math.min(360, hue || 0));
    chroma = Math.max(0, Math.min(0.4, chroma || 0));
    lightness = Math.max(0, Math.min(1, lightness || 0.5));

    return `oklch(${lightness} ${chroma} ${hue})`;
  }

  /**
   * Parses an OKLCH color string into components
   * @param {string} color - OKLCH color string
   * @returns {Object|null} Object with l, c, h properties or null if invalid
   */
  function parseOklchColor(color) {
    const match = color?.match(/oklch\(\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*\)/i);
    if (!match) return null;

    const [, l, c, h] = match.map(Number);
    return { l, c, h };
  }

  /**
   * Applies theme variables to document root
   * @param {Object} theme - Theme configuration object
   */
  function applyTheme(theme) {
    try {
      const variables = generateThemeVariables(theme);
      const root = document.documentElement;

      Object.entries(variables).forEach(([property, value]) => {
        if (value) {
          root.style.setProperty(property, value);
        }
      });

      // Add theme name as data attribute for potential use in CSS selectors
      if (theme.name) {
        root.dataset.themeName = theme.name.toLowerCase().replace(/\s+/g, "-");
      }

      // Set dark/light mode
      if (theme.isDark) {
        root.classList.add("dark");
        root.classList.remove("light");
      } else {
        root.classList.add("light");
        root.classList.remove("dark");
      }
    } catch (error) {
      console.error("Error applying theme:", error);
    }
  }

  /**
   * Creates a lighter variant of an OKLCH color
   * @param {string} color - OKLCH color string (e.g., "oklch(0.5 0.2 180)")
   * @param {number} amount - Amount to lighten (0-1)
   * @returns {string} Lightened OKLCH color
   */
  function lighten(color, amount = 0.1) {
    const components = parseOklchColor(color);
    if (!components) return color;

    const { l, c, h } = components;
    const newL = Math.min(1, l + amount);

    return `oklch(${newL} ${c} ${h})`;
  }

  /**
   * Creates a darker variant of an OKLCH color
   * @param {string} color - OKLCH color string (e.g., "oklch(0.5 0.2 180)")
   * @param {number} amount - Amount to darken (0-1)
   * @returns {string} Darkened OKLCH color
   */
  function darken(color, amount = 0.1) {
    const components = parseOklchColor(color);
    if (!components) return color;

    const { l, c, h } = components;
    const newL = Math.max(0, l - amount);

    return `oklch(${newL} ${c} ${h})`;
  }

  /**
   * Creates a more saturated variant of an OKLCH color
   * @param {string} color - OKLCH color string (e.g., "oklch(0.5 0.2 180)")
   * @param {number} amount - Amount to saturate (0-0.4)
   * @returns {string} More saturated OKLCH color
   */
  function saturate(color, amount = 0.05) {
    const components = parseOklchColor(color);
    if (!components) return color;

    const { l, c, h } = components;
    const newC = Math.min(0.4, c + amount);

    return `oklch(${l} ${newC} ${h})`;
  }

  /**
   * Creates a less saturated variant of an OKLCH color
   * @param {string} color - OKLCH color string (e.g., "oklch(0.5 0.2 180)")
   * @param {number} amount - Amount to desaturate (0-0.4)
   * @returns {string} Less saturated OKLCH color
   */
  function desaturate(color, amount = 0.05) {
    const components = parseOklchColor(color);
    if (!components) return color;

    const { l, c, h } = components;
    const newC = Math.max(0, c - amount);

    return `oklch(${l} ${newC} ${h})`;
  }

  // Export functions to global scope
  window.themeUtils = {
    generateThemeVariables,
    generateOklchColor,
    parseOklchColor,
    applyTheme,
    lighten,
    darken,
    saturate,
    desaturate,
  };
})();
