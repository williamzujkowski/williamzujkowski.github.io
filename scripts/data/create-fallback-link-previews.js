/**
 * Create Fallback Link Previews
 *
 * This script creates empty link preview JSON files
 * for use in CI/CD or when link preview generation fails
 */

import fs from "fs";
import path from "path";

// Configuration
const categories = [
  "art_culture__exploration",
  "artists",
  "blogs",
  "creative",
  "fun__curiosities",
  "gaming",
  "miscellaneous",
  "music",
  "people",
  "projects",
  "retrocomputing",
  "rollerblading",
  "social",
  "technology__innovation",
];

// Sample link preview data for fallback
const sampleLinkPreview = {
  "https://example.com": {
    metadata: {
      title: "Example Website",
      description: "This is a fallback example website description.",
      author: null,
      publisher: "Example",
      image: null,
      logo: null,
      date: null,
      url: "https://example.com",
    },
    lastUpdated: new Date().toISOString(),
  },
};

/**
 * Create fallback link preview files
 */
async function createFallbackLinkPreviews() {
  console.log("Creating fallback link preview files...");

  // Create directory structure
  const dirs = ["./_data", "./assets/data"];

  dirs.forEach((dir) => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`Created directory: ${dir}`);
    }
  });

  // Create main link previews file
  ["_data", "assets/data"].forEach((dir) => {
    const filePath = path.join(dir, "link-previews.json");
    fs.writeFileSync(filePath, JSON.stringify(sampleLinkPreview, null, 2));
    console.log(`Created ${filePath}`);
  });

  // Create category-specific link previews files
  categories.forEach((category) => {
    const fileName = `link-previews-${category}.json`;

    ["_data", "assets/data"].forEach((dir) => {
      const filePath = path.join(dir, fileName);
      fs.writeFileSync(filePath, JSON.stringify({}, null, 2));
      console.log(`Created ${filePath}`);
    });
  });

  console.log("All fallback link preview files created successfully");
}

// Run the function
createFallbackLinkPreviews().catch((error) => {
  console.error("Error creating fallback link previews:", error);
  process.exit(1);
});
