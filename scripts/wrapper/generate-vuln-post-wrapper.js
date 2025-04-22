#!/usr/bin/env node

import path from "path";
import fs from "fs";
import { execSync } from "child_process";
import { fileURLToPath } from "url";

// Get dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

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

// Check if index.js exists, otherwise use generate-vuln-post.js
let scriptPath;
if (fs.existsSync(path.resolve(vulnBlogPath, "index.js"))) {
  scriptPath = path.resolve(vulnBlogPath, "index.js");
} else {
  scriptPath = path.resolve(vulnBlogPath, "generate-vuln-post.js");
}

// Check for workflow and tracing flags
const useWorkflow = process.env.USE_WORKFLOW === "true" ? "--use-workflow true" : "";
const enableTracing =
  process.env.ENABLE_TRACING === "true" ? "--enable-tracing true" : "";

// Build the command to run the appropriate generator
const command = `node ${scriptPath} ${args.join(" ")} --output-dir ${process.env.OUTPUT_DIR} ${useWorkflow} ${enableTracing}`;

// Set environment variable for LLM provider if not set
if (!process.env.LLM_PROVIDER) {
  process.env.LLM_PROVIDER = "openai"; // Default to OpenAI
}

// Run the command
try {
  console.log(`Running: ${command}`);
  console.log(`Using LLM provider: ${process.env.LLM_PROVIDER}`);
  console.log(`Output directory: ${process.env.OUTPUT_DIR}`);

  const output = execSync(command, {
    stdio: "inherit",
    cwd: vulnBlogPath, // Set working directory to vuln-blog
    env: process.env, // Pass all environment variables
  });

  console.log("Post generated successfully");
} catch (error) {
  console.error("Error generating post:", error);
  process.exit(1);
}
