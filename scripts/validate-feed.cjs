// Script to verify and validate the RSS/Atom feed
const fs = require("fs");
const path = require("path");
const { promisify } = require("util");
const exec = promisify(require("child_process").exec);
const parseXml = require("xml2js").parseString;

const feedPath = path.join(__dirname, "..", "_site", "feed.xml");

// Check if the feed exists
if (!fs.existsSync(feedPath)) {
  console.error("Feed file not found.");
  process.exit(1);
}

// Read the feed
const feedContent = fs.readFileSync(feedPath, "utf8");

// Parse the XML for validation
parseXml(feedContent, (err, result) => {
  if (err) {
    console.error("Error parsing feed XML:", err.message);
    process.exit(1);
  }

  try {
    // Check feed root
    if (!result.feed) {
      console.error("Invalid feed format: missing feed element");
      process.exit(1);
    }

    // Check essential elements
    if (!result.feed.title) {
      console.error("Invalid feed format: missing title element");
      process.exit(1);
    }

    if (!result.feed.id) {
      console.error("Invalid feed format: missing id element");
      process.exit(1);
    }

    if (!result.feed.updated) {
      console.error("Invalid feed format: missing updated element");
      process.exit(1);
    }

    // Check author element
    if (!result.feed.author) {
      console.error("Invalid feed format: missing author element");
      process.exit(1);
    }

    // Specifically check author name format
    const author = result.feed.author[0];

    if (!author.name && !author.n) {
      console.error("Invalid feed format: missing author name element");
      process.exit(1);
    }

    // Print feed validation results
    console.log("Feed validation results:");
    console.log("- Title:", result.feed.title[0]);

    if (author.name) {
      console.log("- Author: <name> tag found with value:", author.name[0]);
    } else if (author.n) {
      console.log("- Author: <n> tag found with value:", author.n[0]);
      console.warn("  NOTE: <n> tag is non-standard. Consider changing to <name>");
    }

    // Check entries
    if (result.feed.entry && result.feed.entry.length > 0) {
      console.log("- Entries:", result.feed.entry.length);
      console.log("  First entry title:", result.feed.entry[0].title[0]);
    } else {
      console.warn("- No entries found in feed");
    }

    console.log("Feed validation successful");
  } catch (error) {
    console.error("Error validating feed:", error.message);
    process.exit(1);
  }
});
