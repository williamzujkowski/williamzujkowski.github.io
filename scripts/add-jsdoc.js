/**
 * Script to Add JSDoc Comments to Script Files
 *
 * @description
 * This script adds consistent JSDoc headers to JavaScript files in the scripts directory.
 * It uses the template from utils/script-docs-template.js as a reference.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { globSync } from "glob";

// Root directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");
const scriptsDir = path.join(rootDir, "scripts");

// Get the JSDoc template
const templatePath = path.join(scriptsDir, "utils", "script-docs-template.js");
let template;

try {
  template = fs.readFileSync(templatePath, "utf8");
  // Extract just the JSDoc comment part
  const commentMatch = template.match(/\/\*\*(.*?)\*\//s);
  if (commentMatch && commentMatch[0]) {
    template = commentMatch[0];
  } else {
    console.error("Could not extract JSDoc comment from template");
    process.exit(1);
  }
} catch (error) {
  console.error("Error reading template:", error.message);
  process.exit(1);
}

// Find all JavaScript files in scripts directory (excluding node_modules)
const scriptFiles = globSync("**/*.js", {
  cwd: scriptsDir,
  ignore: ["node_modules/**", "utils/script-docs-template.js", "add-jsdoc.js"],
});

console.log(`Found ${scriptFiles.length} script files`);

// Check if each file already has a JSDoc header
let updatedFiles = 0;
let skippedFiles = 0;

scriptFiles.forEach((relativeFilePath) => {
  const filePath = path.join(scriptsDir, relativeFilePath);

  try {
    let content = fs.readFileSync(filePath, "utf8");

    // Check if file already has a JSDoc comment at the top
    if (content.trim().startsWith("/**")) {
      console.log(`Skipping ${relativeFilePath} - already has JSDoc header`);
      skippedFiles++;
      return;
    }

    // Create a customized template for this file
    const fileName = path.basename(filePath);
    const scriptName = fileName.replace(/\.js$/, "");

    let customTemplate = template
      .replace("[Name of the script]", scriptName)
      .replace("[Brief description of what the script does]", `Purpose: ${scriptName}`)
      .replace("[Author name]", "William Zujkowski")
      .replace("[Creation/Update date]", new Date().toISOString().split("T")[0]);

    // Add the template to the beginning of the file
    const updatedContent = customTemplate + "\n\n" + content;

    // Write the updated content back to the file
    fs.writeFileSync(filePath, updatedContent);

    console.log(`✅ Added JSDoc header to ${relativeFilePath}`);
    updatedFiles++;
  } catch (error) {
    console.error(`Error processing ${relativeFilePath}:`, error.message);
  }
});

console.log(`\nSummary:`);
console.log(`- Updated ${updatedFiles} files with JSDoc headers`);
console.log(`- Skipped ${skippedFiles} files (already had headers)`);
console.log(`- Total: ${scriptFiles.length} files processed`);
