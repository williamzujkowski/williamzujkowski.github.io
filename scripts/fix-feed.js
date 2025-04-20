// Script to fix the RSS feed author tag
const fs = require("fs");
const path = require("path");

// Path to the generated feed
const feedPath = path.join(__dirname, "..", "_site", "feed.xml");

// Read the feed content
console.log(`Reading feed from ${feedPath}`);
try {
  const feedContent = fs.readFileSync(feedPath, "utf8");

  // Check if it has the <n> tags
  if (feedContent.includes("<n>")) {
    console.log("Found <n> tags to replace with <name> tags");

    // Replace <n> with <name> tags
    const fixedContent = feedContent.replace(/<n>([^<]+)<\/n>/g, "<name>$1</name>");

    // Write the fixed content back
    fs.writeFileSync(feedPath, fixedContent, "utf8");
    console.log("Fixed feed.xml author tags successfully");
  } else {
    console.log("No <n> tags found, feed is already correct");
  }
} catch (error) {
  console.error("Error fixing feed:", error);
}
