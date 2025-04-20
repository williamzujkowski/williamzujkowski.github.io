// Script to verify and validate the RSS/Atom feed
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";
import xml2js from "xml2js";

// Get current directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Path to the feed file
const feedPath = path.join(__dirname, "..", "_site", "feed.xml");

// Check if the feed exists
if (!fs.existsSync(feedPath)) {
  console.error("Feed file not found.");
  process.exit(1);
}

// Read the feed
const feedContent = fs.readFileSync(feedPath, "utf8");
console.log("Feed content loaded, size:", feedContent.length);

// Look for tag patterns
const nameTagMatch = feedContent.match(/<name>([^<]+)<\/name>/);
const nTagMatch = feedContent.match(/<n>([^<]+)<\/n>/);

console.log("Author tag analysis:");
if (nameTagMatch) {
  console.log("- Found <name> tag with value:", nameTagMatch[1]);
} else {
  console.log("- No <name> tag found");
}

if (nTagMatch) {
  console.log("- Found <n> tag with value:", nTagMatch[1]);
} else {
  console.log("- No <n> tag found");
}

// Parse the XML
xml2js.parseString(feedContent, (err, result) => {
  if (err) {
    console.error("Error parsing feed XML:", err.message);
    process.exit(1);
  }

  console.log("\nFeed structure analysis:");

  try {
    // Check feed root
    if (!result.feed) {
      console.error("Invalid feed format: missing feed element");
      process.exit(1);
    }

    console.log("- Feed root element exists");

    // Check essential elements
    console.log("- Title:", result.feed.title?.[0] || "MISSING");
    console.log("- ID:", result.feed.id?.[0] || "MISSING");
    console.log("- Updated:", result.feed.updated?.[0] || "MISSING");

    // Check author element
    if (!result.feed.author) {
      console.error("Invalid feed format: missing author element");
    } else {
      console.log("- Author element exists");

      // Check author properties
      const author = result.feed.author[0];
      console.log("  Author properties:", Object.keys(author).join(", "));
    }

    // Check entries
    if (result.feed.entry && result.feed.entry.length > 0) {
      console.log("- Entries:", result.feed.entry.length);
      console.log(
        "  First entry title:",
        result.feed.entry[0]?.title?.[0] || "MISSING"
      );
    } else {
      console.warn("- No entries found in feed");
    }

    console.log("\nFeed validation successful");
  } catch (error) {
    console.error("Error validating feed:", error.message);
    process.exit(1);
  }
});
