// Script to fix the RSS feed after generation
const fs = require("fs");
const path = require("path");

// Path to the generated feed
const feedPath = path.join(__dirname, "..", "_site", "feed.xml");

// Check if the feed exists
if (fs.existsSync(feedPath)) {
  console.log(`Fixing RSS feed at ${feedPath}`);

  // Read the current content
  const content = fs.readFileSync(feedPath, "utf8");

  // Log the relevant part for debugging
  const authorMatch = content.match(/<author>[\s\S]*?<\/author>/);
  if (authorMatch) {
    console.log("Current author tag:", authorMatch[0]);
  }

  // First, try to ensure the closing tag matches the opening tag
  let fixed = content;

  // Replace <n>name</n> with <name>name</name>
  fixed = fixed.replace(/<author>\s*<n>([^<]+)<\/n>/g, "<author>\n    <name>$1</name>");

  // Also handle case where there might be mixed closing tags
  fixed = fixed.replace(/<name>([^<]+)<\/name>/g, "<name>$1</name>");

  // Write the fixed content back
  fs.writeFileSync(feedPath, fixed, "utf8");

  // Verify the fix worked
  const fixedContent = fs.readFileSync(feedPath, "utf8");
  const fixedAuthorMatch = fixedContent.match(/<author>[\s\S]*?<\/author>/);
  if (fixedAuthorMatch) {
    console.log("Fixed author tag:", fixedAuthorMatch[0]);
  }

  console.log("RSS feed fixed with correct author tag format");
} else {
  console.error(`Feed file not found at ${feedPath}`);
}
