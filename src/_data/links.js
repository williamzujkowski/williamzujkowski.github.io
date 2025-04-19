/**
 * Consolidated links data loader that uses the merged links.json file
 * from src/_data/config/links.json instead of individual link files.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get dirname in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export default function () {
  try {
    // Path to the consolidated links file
    const linksPath = path.join(__dirname, "config", "links.json");

    // Check if the file exists
    if (fs.existsSync(linksPath)) {
      // Read and parse the consolidated JSON file
      const linksData = JSON.parse(fs.readFileSync(linksPath, "utf8"));

      // Return the links data (already organized by categories)
      return linksData;
    } else {
      console.warn("Consolidated links.json file not found at:", linksPath);
      return { categories: {} };
    }
  } catch (error) {
    console.error("Error loading links data:", error);
    return { categories: {} };
  }
}
