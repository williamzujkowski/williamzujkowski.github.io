/**
 * Unit tests for theme-utils.js
 */

import {
  generateThemeVariables,
  generateOklchColor,
  parseOklchColor,
  lighten,
  darken,
  saturate,
  desaturate,
  applyTheme,
} from "../../src/js/theme-utils.js";
import { test, assert } from "../test-framework.js";

// Mock document for testing
globalThis.document = {
  documentElement: {
    style: {
      setProperty: () => {},
    },
    classList: {
      add: () => {},
      remove: () => {},
    },
    dataset: {},
  },
};

test("generateOklchColor generates correctly formatted OKLCH color string", () => {
  const result = generateOklchColor(180, 0.2, 0.5);
  assert.equal(result, "oklch(0.5 0.2 180)");
  return true;
});

test("generateOklchColor clamps values to valid ranges", () => {
  // Test clamping hue (0-360)
  assert.equal(generateOklchColor(-10, 0.1, 0.5), "oklch(0.5 0.1 0)");
  assert.equal(generateOklchColor(400, 0.1, 0.5), "oklch(0.5 0.1 360)");

  // Test clamping chroma (0-0.4)
  assert.equal(generateOklchColor(180, -0.1, 0.5), "oklch(0.5 0 180)");
  assert.equal(generateOklchColor(180, 0.5, 0.5), "oklch(0.5 0.4 180)");

  // Test clamping lightness (0-1)
  assert.equal(generateOklchColor(180, 0.2, -0.1), "oklch(0 0.2 180)");
  assert.equal(generateOklchColor(180, 0.2, 1.5), "oklch(1 0.2 180)");
  return true;
});

test("generateOklchColor handles missing or invalid parameters", () => {
  // Missing all parameters defaults to hue 0, chroma 0, lightness 0.5
  assert.equal(generateOklchColor(), "oklch(0.5 0 0)");

  // Missing some parameters
  assert.equal(generateOklchColor(180), "oklch(0.5 0 180)");
  assert.equal(generateOklchColor(180, 0.2), "oklch(0.5 0.2 180)");

  // Invalid parameters (NaN)
  assert.equal(generateOklchColor(NaN, 0.2, 0.5), "oklch(0.5 0.2 0)");
  assert.equal(generateOklchColor(180, NaN, 0.5), "oklch(0.5 0 180)");
  assert.equal(generateOklchColor(180, 0.2, NaN), "oklch(0.5 0.2 180)");
  return true;
});

test("parseOklchColor parses valid OKLCH color string", () => {
  const result = parseOklchColor("oklch(0.5 0.2 180)");
  assert.equal(result.l, 0.5);
  assert.equal(result.c, 0.2);
  assert.equal(result.h, 180);
  return true;
});

test("parseOklchColor handles invalid color strings", () => {
  assert.equal(parseOklchColor("rgb(255, 0, 0)"), null);
  assert.equal(parseOklchColor("not a color"), null);
  assert.equal(parseOklchColor(""), null);
  assert.equal(parseOklchColor(null), null);
  assert.equal(parseOklchColor(undefined), null);
  return true;
});

test("parseOklchColor works with whitespace variations", () => {
  const result1 = parseOklchColor("oklch(0.5   0.2   180)");
  assert.equal(result1.l, 0.5);
  assert.equal(result1.c, 0.2);
  assert.equal(result1.h, 180);

  const result2 = parseOklchColor("oklch(0.5 0.2 180)");
  assert.equal(result2.l, 0.5);
  assert.equal(result2.c, 0.2);
  assert.equal(result2.h, 180);

  const result3 = parseOklchColor("oklch(  0.5 0.2 180  )");
  assert.equal(result3.l, 0.5);
  assert.equal(result3.c, 0.2);
  assert.equal(result3.h, 180);
  return true;
});

test("generateThemeVariables creates variables from a complete theme configuration", () => {
  const theme = {
    colors: {
      primaryHue: 200,
      primaryChroma: 0.15,
      primaryLightness: 0.6,
      accentHue: 300,
      accentChroma: 0.2,
      accentLightness: 0.7,
      backgroundColor: "oklch(0.1 0.01 200)",
      surfaceColor: "oklch(0.15 0.01 200)",
      borderColor: "oklch(0.2 0.01 200)",
      textColor: "oklch(0.9 0.01 200)",
      textSecondaryColor: "oklch(0.7 0.01 200)",
      mutedColor: "oklch(0.6 0.01 200)",
      successColor: "oklch(0.6 0.1 150)",
      warningColor: "oklch(0.7 0.1 80)",
      dangerColor: "oklch(0.65 0.1 30)",
      infoColor: "oklch(0.6 0.1 250)",
    },
    shadows: {
      card: "0 2px 4px rgba(0,0,0,0.1)",
      elevated: "0 4px 8px rgba(0,0,0,0.2)",
    },
    borders: {
      radius: "8px",
      width: "2px",
    },
    animation: {
      transition: "0.5s ease",
      hover: "-translate-y-2",
    },
  };

  const variables = generateThemeVariables(theme);

  // Check primary and accent color variables
  assert.equal(variables["--color-primary"], "oklch(0.6 0.15 200)");
  assert.equal(variables["--color-accent"], "oklch(0.7 0.2 300)");

  // Check UI colors
  assert.equal(variables["--color-background"], "oklch(0.1 0.01 200)");
  assert.equal(variables["--color-surface"], "oklch(0.15 0.01 200)");
  assert.equal(variables["--color-text"], "oklch(0.9 0.01 200)");

  // Check status colors
  assert.equal(variables["--color-success"], "oklch(0.6 0.1 150)");
  assert.equal(variables["--color-warning"], "oklch(0.7 0.1 80)");
  assert.equal(variables["--color-danger"], "oklch(0.65 0.1 30)");
  assert.equal(variables["--color-info"], "oklch(0.6 0.1 250)");

  // Check other properties
  assert.equal(variables["--shadow-card"], "0 2px 4px rgba(0,0,0,0.1)");
  assert.equal(variables["--border-radius"], "8px");
  assert.equal(variables["--transition"], "0.5s ease");

  return true;
});

test("generateThemeVariables uses default values for missing properties", () => {
  const theme = {
    colors: {
      primaryHue: 200,
    },
  };

  const variables = generateThemeVariables(theme);

  // Some default should be applied
  assert.ok(variables["--color-primary"], "Should define primary color");
  assert.ok(variables["--color-accent"], "Should define accent color");
  assert.ok(variables["--color-background"], "Should define background color");
  assert.equal(variables["--border-radius"], "6px", "Should use default border radius");

  return true;
});

test("generateThemeVariables handles invalid theme configuration", () => {
  // Save original console.error
  const originalConsoleError = console.error;

  // Replace with mock function
  console.error = () => {};

  // Test with null theme
  const nullResult = generateThemeVariables(null);
  assert.ok(
    Object.keys(nullResult).length === 0,
    "Should return empty object for null theme"
  );

  // Test with missing colors
  const emptyResult = generateThemeVariables({});
  assert.ok(
    Object.keys(emptyResult).length === 0,
    "Should return empty object for empty theme"
  );

  // Restore console.error
  console.error = originalConsoleError;

  return true;
});

test("lighten increases lightness of a color correctly", () => {
  const result = lighten("oklch(0.5 0.2 180)", 0.1);
  assert.equal(result, "oklch(0.6 0.2 180)");
  return true;
});

test("lighten clamps lightness to maximum 1", () => {
  const result = lighten("oklch(0.95 0.2 180)", 0.1);
  assert.equal(result, "oklch(1 0.2 180)");
  return true;
});

test("lighten returns original color for invalid input", () => {
  assert.equal(lighten("not a color", 0.1), "not a color");
  assert.equal(lighten(null, 0.1), null);
  return true;
});

test("darken decreases lightness of a color correctly", () => {
  const result = darken("oklch(0.5 0.2 180)", 0.1);
  assert.equal(result, "oklch(0.4 0.2 180)");
  return true;
});

test("darken clamps lightness to minimum 0", () => {
  const result = darken("oklch(0.05 0.2 180)", 0.1);
  assert.equal(result, "oklch(0 0.2 180)");
  return true;
});

test("darken returns original color for invalid input", () => {
  assert.equal(darken("not a color", 0.1), "not a color");
  assert.equal(darken(null, 0.1), null);
  return true;
});

test("saturate increases chroma of a color correctly", () => {
  const result = saturate("oklch(0.5 0.2 180)", 0.05);
  assert.equal(result, "oklch(0.5 0.25 180)");
  return true;
});

test("saturate clamps chroma to maximum 0.4", () => {
  const result = saturate("oklch(0.5 0.38 180)", 0.05);
  assert.equal(result, "oklch(0.5 0.4 180)");
  return true;
});

test("saturate returns original color for invalid input", () => {
  assert.equal(saturate("not a color", 0.05), "not a color");
  assert.equal(saturate(null, 0.05), null);
  return true;
});

test("desaturate decreases chroma of a color correctly", () => {
  const result = desaturate("oklch(0.5 0.2 180)", 0.05);
  // Use a regex to handle floating point precision issues
  assert.ok(
    /oklch\(0\.5 0\.1[45]\d* 180\)/.test(result),
    `Expected around 0.15 but got ${result}`
  );
  return true;
});

test("desaturate clamps chroma to minimum 0", () => {
  const result = desaturate("oklch(0.5 0.03 180)", 0.05);
  assert.equal(result, "oklch(0.5 0 180)");
  return true;
});

test("desaturate returns original color for invalid input", () => {
  assert.equal(desaturate("not a color", 0.05), "not a color");
  assert.equal(desaturate(null, 0.05), null);
  return true;
});

test("applyTheme applies theme variables to document root", () => {
  // Create a mock document.documentElement
  let propValues = {};
  let addedClasses = [];
  let removedClasses = [];
  let datasetValues = {};

  document.documentElement = {
    style: {
      setProperty: (name, value) => {
        propValues[name] = value;
      },
    },
    classList: {
      add: (cls) => {
        addedClasses.push(cls);
      },
      remove: (cls) => {
        removedClasses.push(cls);
      },
    },
    dataset: datasetValues,
  };

  const theme = {
    name: "Test Theme",
    isDark: true,
    colors: {
      primaryHue: 200,
      primaryChroma: 0.15,
      primaryLightness: 0.6,
    },
  };

  applyTheme(theme);

  // Check that variables were set
  assert.equal(
    propValues["--color-primary"],
    "oklch(0.6 0.15 200)",
    "Should set primary color variable"
  );

  // Check that dark mode was set
  assert.ok(addedClasses.includes("dark"), "Should add dark class");
  assert.ok(removedClasses.includes("light"), "Should remove light class");

  // Check that theme name was set
  assert.equal(
    datasetValues.themeName,
    "test-theme",
    "Should set theme name in dataset"
  );

  return true;
});

test("applyTheme handles light mode correctly", () => {
  // Create a mock document.documentElement
  let addedClasses = [];
  let removedClasses = [];

  document.documentElement = {
    style: {
      setProperty: () => {},
    },
    classList: {
      add: (cls) => {
        addedClasses.push(cls);
      },
      remove: (cls) => {
        removedClasses.push(cls);
      },
    },
    dataset: {},
  };

  const theme = {
    name: "Light Theme",
    isDark: false,
    colors: {
      primaryHue: 200,
      primaryChroma: 0.15,
      primaryLightness: 0.6,
    },
  };

  applyTheme(theme);

  // Check that light mode was set
  assert.ok(addedClasses.includes("light"), "Should add light class");
  assert.ok(removedClasses.includes("dark"), "Should remove dark class");

  return true;
});

test("applyTheme handles error gracefully", () => {
  // Create a mock document.documentElement
  document.documentElement = {
    style: {
      setProperty: () => {},
    },
    classList: {
      add: () => {},
      remove: () => {},
    },
    dataset: {},
  };

  // Save original console.error
  const originalConsoleError = console.error;

  // Replace with mock function
  let errorCalled = false;
  console.error = () => {
    errorCalled = true;
  };

  // Test with a theme that will cause an error
  const invalidTheme = null;

  try {
    // Should not throw
    applyTheme(invalidTheme);
    assert.ok(true, "Should not throw an error");
  } catch (e) {
    assert.ok(false, "Should not throw but did: " + e.message);
  }

  // Error should be logged
  assert.ok(errorCalled, "Should log an error");

  // Restore console.error
  console.error = originalConsoleError;

  return true;
});
