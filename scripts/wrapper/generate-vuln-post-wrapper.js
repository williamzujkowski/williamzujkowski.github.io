#!/usr/bin/env node

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

// Get the path to the tools/vuln-blog directory
const vulnBlogPath = path.resolve(__dirname, "../../tools/vuln-blog");

// Build the command to run the new modular generator
const command = `node ${path.resolve(vulnBlogPath, "index.js")} ${args.join(" ")} --output-dir ${process.env.OUTPUT_DIR}`;

// Run the command
try {
  console.log(`Running: ${command}`);
  const output = execSync(command, {
    stdio: "inherit",
    cwd: vulnBlogPath, // Set working directory to vuln-blog
  });
  console.log("Post generated successfully");
} catch (error) {
  console.error("Error generating post:", error);
  process.exit(1);
}
