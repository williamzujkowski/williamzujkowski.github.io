/**
 * Theme Generator Utility
 *
 * This script generates a theme.json file from command line arguments
 * to make it easy to create and modify themes.
 *
 * Usage:
 * node scripts/styling/generate-theme.js --name "GitHub Dark" --primary-hue 145 --primary-chroma 0.15 --accent-hue 230
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Parse command line arguments
const args = process.argv.slice(2);
const params = {};

for (let i = 0; i < args.length; i += 2) {
  const key = args[i].replace(/^--/, "");
  const value = args[i + 1];

  // Convert numeric values
  if (!isNaN(parseFloat(value))) {
    params[key] = Number(value);
  } else {
    params[key] = value;
  }
}

// Default theme template
const defaultTheme = {
  name: params.name || "GitHub Dark",
  description:
    params.description ||
    "Dark theme inspired by GitHub's dark mode with OKLCH colors for better color accuracy and accessibility",
  isDark: params.isDark !== undefined ? params.isDark : true,
  version: params.version || "1.0.0",
  colors: {
    primaryHue: params["primary-hue"] || 145,
    primaryChroma: params["primary-chroma"] || 0.15,
    primaryLightness: params["primary-lightness"] || 0.56,

    accentHue: params["accent-hue"] || 230,
    accentChroma: params["accent-chroma"] || 0.15,
    accentLightness: params["accent-lightness"] || 0.7,

    backgroundColor: params["background-color"] || "oklch(0.16 0.02 250)",
    surfaceColor: params["surface-color"] || "oklch(0.20 0.02 250)",
    borderColor: params["border-color"] || "oklch(0.30 0.02 250)",
    grayLightColor: params["gray-light-color"] || "oklch(0.25 0.02 250)",
    textColor: params["text-color"] || "oklch(0.93 0.02 250)",
    textSecondaryColor: params["text-secondary-color"] || "oklch(0.75 0.03 250)",
    mutedColor: params["muted-color"] || "oklch(0.65 0.02 250)",
    successColor: params["success-color"] || "oklch(0.56 0.15 145)",
    warningColor: params["warning-color"] || "oklch(0.75 0.15 80)",
    dangerColor: params["danger-color"] || "oklch(0.65 0.15 25)",
    infoColor: params["info-color"] || "oklch(0.70 0.15 230)",
  },
  shadows: {
    card: params["shadow-card"] || "0 0 0 1px oklch(0.30 0.02 250)",
    elevated:
      params["shadow-elevated"] ||
      "0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -2px rgba(0, 0, 0, 0.1)",
  },
  borders: {
    radius: params["border-radius"] || "6px",
    width: params["border-width"] || "1px",
  },
  animation: {
    transition: params["transition"] || "0.3s ease",
    hover: params["hover-transform"] || "-translate-y-1",
  },
};

// Define the output path
const themePath =
  params.output || path.join(__dirname, "..", "src", "_data", "config", "theme.json");

// Ensure the directory exists
const themeDir = path.dirname(themePath);
if (!fs.existsSync(themeDir)) {
  fs.mkdirSync(themeDir, { recursive: true });
}

// Write the theme file
try {
  // Ensure the directory exists
  if (!fs.existsSync(path.dirname(themePath))) {
    fs.mkdirSync(path.dirname(themePath), { recursive: true });
  }

  // Write the file
  fs.writeFileSync(themePath, JSON.stringify(defaultTheme, null, 2), "utf-8");

  console.log(`Theme generated and saved to ${themePath}`);

  // Print theme preview
  console.log("\nTheme Preview:");
  console.log("=============");
  console.log(`Name: ${defaultTheme.name}`);
  console.log(
    `Primary: oklch(${defaultTheme.colors.primaryLightness} ${defaultTheme.colors.primaryChroma} ${defaultTheme.colors.primaryHue})`
  );
  console.log(
    `Accent: oklch(${defaultTheme.colors.accentLightness} ${defaultTheme.colors.accentChroma} ${defaultTheme.colors.accentHue})`
  );
  console.log(`Background: ${defaultTheme.colors.backgroundColor}`);
  console.log(`Surface: ${defaultTheme.colors.surfaceColor}`);
  console.log(`Border: ${defaultTheme.colors.borderColor}`);
  console.log(`Text: ${defaultTheme.colors.textColor}`);
  console.log(`Text Secondary: ${defaultTheme.colors.textSecondaryColor}`);
  console.log("=============\n");

  // Example commands to generate other themes
  console.log("Example commands for other themes:");
  console.log("--------------------------------");
  console.log("# Blue theme");
  console.log(
    'node tools/generate-theme.js --name "Ocean Blue" --primary-hue 220 --primary-chroma 0.15 --accent-hue 280'
  );
  console.log("");
  console.log("# Purple theme");
  console.log(
    'node tools/generate-theme.js --name "Deep Purple" --primary-hue 270 --primary-chroma 0.15 --accent-hue 330'
  );
  console.log("");
  console.log("# Amber theme");
  console.log(
    'node tools/generate-theme.js --name "Amber Glow" --primary-hue 60 --primary-chroma 0.13 --accent-hue 30'
  );
  console.log("");
} catch (error) {
  console.error("Error generating theme:", error.message);
  process.exit(1);
}
