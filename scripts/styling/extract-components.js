#!/usr/bin/env node

/**
 * Component CSS Extractor
 *
 * This utility helps organize CSS by extracting component styles from styles.css
 * into separate files in a components directory, making the codebase more maintainable.
 *
 * Usage:
 * node scripts/styling/extract-components.js [--dry-run]
 *
 * Options:
 * --dry-run  Show what would be extracted without making changes
 */

import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
const STYLES_PATH = path.join(__dirname, "..", "src", "css", "styles.css");
const COMPONENTS_DIR = path.join(__dirname, "..", "src", "css", "components");
const DRY_RUN = process.argv.includes("--dry-run");

// Component definitions - add more as needed
const COMPONENTS = [
  {
    name: "buttons",
    pattern: /\/\* Button styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Button component styles */\n\n@layer components {\n  .btn {\n    @apply px-4 py-2 rounded-github;\n  }\n}\n",
  },
  {
    name: "cards",
    pattern: /\/\* Card styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Card component styles */\n\n@layer components {\n  .card {\n    @apply bg-surface rounded-github border border-border p-4;\n  }\n}\n",
  },
  {
    name: "header",
    pattern: /\/\* Header styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Header component styles */\n\n@layer components {\n  .header {\n    @apply bg-surface border-b border-border py-4;\n  }\n}\n",
  },
  {
    name: "footer",
    pattern: /\/\* Footer styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Footer component styles */\n\n@layer components {\n  .footer {\n    @apply bg-surface border-t border-border py-6;\n  }\n}\n",
  },
  {
    name: "navigation",
    pattern: /\/\* Navigation styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Navigation component styles */\n\n@layer components {\n  .nav-link {\n    @apply text-text-secondary hover:text-text transition-colors duration-200;\n  }\n}\n",
  },
  {
    name: "forms",
    pattern: /\/\* Form styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Form component styles */\n\n@layer components {\n  .form-input {\n    @apply bg-surface text-text border border-border rounded-github px-3 py-2;\n  }\n}\n",
  },
  {
    name: "utilities",
    pattern: /\/\* Custom utility styles \*\/[\s\S]*?(?=\/\* |\s*@)/,
    fallback:
      "/* Custom utility styles */\n\n@layer utilities {\n  .text-balance {\n    text-wrap: balance;\n  }\n}\n",
  },
];

// Main function
async function extractComponents() {
  try {
    console.log(
      `${DRY_RUN ? "[DRY RUN] " : ""}Extracting components from styles.css...`
    );

    // Create components directory if it doesn't exist
    if (!DRY_RUN) {
      try {
        await fs.mkdir(COMPONENTS_DIR, { recursive: true });
        console.log(`Created components directory at ${COMPONENTS_DIR}`);
      } catch (err) {
        if (err.code !== "EEXIST") {
          throw err;
        }
      }
    }

    // Read styles.css
    const stylesContent = await fs.readFile(STYLES_PATH, "utf8");
    let newStylesContent = stylesContent;
    const imports = [];

    // Extract each component
    for (const component of COMPONENTS) {
      console.log(`Processing ${component.name}...`);

      const match = stylesContent.match(component.pattern);
      const componentContent = match ? match[0] : component.fallback;

      if (match) {
        console.log(`Found ${component.name} styles`);
        newStylesContent = newStylesContent.replace(component.pattern, "");
      } else {
        console.log(`No existing ${component.name} styles found, will use fallback`);
      }

      // Add import statement
      imports.push(`@import 'components/${component.name}.css';`);

      // Write component file
      const componentPath = path.join(COMPONENTS_DIR, `${component.name}.css`);
      if (!DRY_RUN) {
        await fs.writeFile(componentPath, componentContent);
        console.log(`Wrote ${component.name}.css`);
      } else {
        console.log(
          `[DRY RUN] Would write to ${componentPath}:\n${componentContent.substring(0, 100)}...`
        );
      }
    }

    // Update styles.css with imports
    const importStatements = imports.join("\n");
    const tailwindDirectives =
      "@tailwind base;\n@tailwind components;\n@tailwind utilities;\n\n";

    // Add imports after Tailwind directives
    const updatedStylesContent =
      tailwindDirectives +
      "/* Component imports */\n" +
      importStatements +
      "\n\n" +
      newStylesContent.replace(
        /\/\* Tailwind directives \*\/[\s\S]*?@tailwind utilities;[\s\S]*?\n\n/,
        ""
      );

    if (!DRY_RUN) {
      await fs.writeFile(STYLES_PATH, updatedStylesContent);
      console.log("Updated styles.css with component imports");
    } else {
      console.log(
        `[DRY RUN] Would update styles.css with imports:\n${importStatements}`
      );
    }

    console.log(`${DRY_RUN ? "[DRY RUN] " : ""}Component extraction complete!`);
  } catch (error) {
    console.error("Error:", error);
    process.exit(1);
  }
}

// Run the extraction
extractComponents();
