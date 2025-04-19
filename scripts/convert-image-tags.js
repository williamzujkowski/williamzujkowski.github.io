/**
 * convert-image-tags.js
 *
 * Script to convert manual image tags in blog posts to the {% image %} shortcode format.
 * Converts markdown image syntax like ![Alt text](/assets/images/path/to/image.jpg)
 * to {% image "path/to/image.jpg", "Alt text", "100vw" %}
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import { globSync } from "glob";

// Set up paths
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const projectRoot = path.resolve(__dirname, "../");
const postsDir = path.join(projectRoot, "src/posts");

// Regular expression to match markdown image syntax
// Captures the alt text and the image path
const markdownImageRegex = /!\[(.*?)\]\((\/assets\/images\/)(.*?)\)/g;

// Main function
async function convertImageTags() {
  console.log("Starting conversion of manual image tags to shortcodes...");

  // Get all markdown files in posts directory
  const postFiles = globSync("*.md", { cwd: postsDir });
  console.log(`Found ${postFiles.length} blog posts to process`);

  let modifiedCount = 0;
  let imageCount = 0;

  for (const file of postFiles) {
    const filePath = path.join(postsDir, file);
    let fileContent = fs.readFileSync(filePath, "utf8");

    // Track if this file was modified
    let fileModified = false;

    // Find and replace all markdown image tags
    const newContent = fileContent.replace(
      markdownImageRegex,
      (match, altText, assetPrefix, imagePath) => {
        fileModified = true;
        imageCount++;

        // Build the image shortcode
        return `{% image "${imagePath}", "${altText}", "100vw" %}`;
      }
    );

    // Update the file if changes were made
    if (fileModified) {
      fs.writeFileSync(filePath, newContent);
      modifiedCount++;
      console.log(`Updated ${file} - converted manual image tags to shortcodes`);
    }
  }

  console.log(
    `Conversion complete. Modified ${modifiedCount} files, converting ${imageCount} image tags.`
  );
}

// Run the function
convertImageTags().catch((error) => {
  console.error("Error converting image tags:", error);
  process.exit(1);
});
