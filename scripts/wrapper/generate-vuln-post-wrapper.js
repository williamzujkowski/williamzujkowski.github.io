const path = require("path");
const fs = require("fs");
const { execSync } = require("child_process");

// Get command line arguments
const args = process.argv.slice(2);

// Set the output directory to src/posts in the main repo
process.env.OUTPUT_DIR = path.resolve(__dirname, "../../src/posts");

// Ensure the output directory exists
if (!fs.existsSync(process.env.OUTPUT_DIR)) {
  fs.mkdirSync(process.env.OUTPUT_DIR, { recursive: true });
}

// Build the command to run the original script
const command = `node ${path.resolve(__dirname, "../../tools/vuln-blog/generate-vuln-post.js")} ${args.join(" ")}`;

// Run the command
try {
  console.log(`Running: ${command}`);
  const output = execSync(command, { stdio: "inherit" });
  console.log("Post generated successfully");
} catch (error) {
  console.error("Error generating post:", error);
  process.exit(1);
}
