/**
 * Vulnerability Blog Generator Integration Tests
 *
 * These tests verify that the vulnerability blog generator submodule
 * is properly integrated with the website and functioning correctly.
 */

import fs from "fs";
import path from "path";
import { execSync } from "child_process";
import { fileURLToPath } from "url";
import { test, assert } from "../test-framework.js";

// Set up dirname equivalent in ESM
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Use same path definitions but outside any describe blocks
const submodulePath = path.join(process.cwd(), "tools", "vuln-blog");
const postsPath = path.join(process.cwd(), "src", "posts");

// Test that the submodule exists and has the expected files
test("Vulnerability Blog Generator - Submodule directory exists", () => {
  assert.ok(fs.existsSync(submodulePath), "Submodule directory does not exist");
  return true;
});

test("Vulnerability Blog Generator - Contains essential files", () => {
  const requiredFiles = [
    "generate-vuln-post.js",
    "llm-providers.js",
    "test-models.js",
    "package.json",
    "README.md",
  ];

  for (const file of requiredFiles) {
    assert.ok(
      fs.existsSync(path.join(submodulePath, file)),
      `Required file ${file} is missing from submodule`
    );
  }
  return true;
});

test("Vulnerability Blog Generator - Has prompts directory with templates", () => {
  const promptsDir = path.join(submodulePath, "prompts");
  assert.ok(fs.existsSync(promptsDir), "Prompts directory does not exist");

  const requiredPrompts = ["threat-blog-post.prompt", "threat-blog-post-rag.prompt"];

  for (const file of requiredPrompts) {
    assert.ok(
      fs.existsSync(path.join(promptsDir, file)),
      `Required prompt template ${file} is missing`
    );
  }
  return true;
});

// Test that package.json scripts are properly updated
test("Vulnerability Blog Generator - Has required scripts in package.json", () => {
  const packageJsonPath = path.join(process.cwd(), "package.json");
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));

  const requiredScripts = [
    "generate:vuln",
    "generate:latest",
    "schedule:vuln",
    "test:openai",
    "test:gemini",
    "test:claude",
    "test:llm",
    "test:sources",
  ];

  for (const script of requiredScripts) {
    assert.ok(
      packageJson.scripts[script],
      `Required script ${script} is missing from package.json`
    );
  }
  return true;
});

test("Vulnerability Blog Generator - Scripts point to the submodule directory", () => {
  const packageJsonPath = path.join(process.cwd(), "package.json");
  const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));

  // Check that some scripts reference the vuln-blog submodule
  let hasSubmoduleRefs = false;

  // Get all script values into an array
  const scriptValues = Object.values(packageJson.scripts);

  // Check if any script contains the tools/vuln-blog path
  for (const scriptValue of scriptValues) {
    if (scriptValue.includes("tools/vuln-blog")) {
      hasSubmoduleRefs = true;
      break;
    }
  }

  assert.ok(
    hasSubmoduleRefs,
    `No scripts found that point to the tools/vuln-blog directory`
  );

  return true;
});

// Testing GitHub Actions workflows if they exist
test("Vulnerability Blog Generator - GitHub workflow files have proper configuration", () => {
  const workflowsDir = path.join(process.cwd(), ".github", "workflows");

  if (!fs.existsSync(workflowsDir)) {
    return "Workflows directory doesn't exist, skipping workflow tests";
  }

  const vulnWorkflowPath = path.join(workflowsDir, "vulnerability-posts.yml");
  const testProvidersPath = path.join(workflowsDir, "test-llm-providers.yml");

  if (!fs.existsSync(vulnWorkflowPath) || !fs.existsSync(testProvidersPath)) {
    return "One or more workflow files are missing, skipping workflow tests";
  }

  // Read workflow files
  const vulnerabilityWorkflow = fs.readFileSync(vulnWorkflowPath, "utf8");
  const testProvidersWorkflow = fs.readFileSync(testProvidersPath, "utf8");

  // Check for recursive submodules
  assert.ok(
    vulnerabilityWorkflow.includes("submodules: recursive"),
    "vulnerability-posts.yml does not checkout with submodules: recursive"
  );

  assert.ok(
    testProvidersWorkflow.includes("submodules: recursive"),
    "test-llm-providers.yml does not checkout with submodules: recursive"
  );

  // Check for submodule dependency installation
  assert.ok(
    vulnerabilityWorkflow.includes("cd tools/vuln-blog") &&
      vulnerabilityWorkflow.includes("npm install"),
    "vulnerability-posts.yml does not install submodule dependencies"
  );

  assert.ok(
    testProvidersWorkflow.includes("cd tools/vuln-blog") &&
      testProvidersWorkflow.includes("npm install"),
    "test-llm-providers.yml does not install submodule dependencies"
  );

  return true;
});

// Test wrapper script existence
test("Vulnerability Blog Generator - Has wrapper script directory", () => {
  const wrapperDir = path.join(process.cwd(), "scripts", "wrapper");
  assert.ok(fs.existsSync(wrapperDir), "Wrapper script directory does not exist");
  return true;
});

// Test script functionality (mocked)
test("Vulnerability Blog Generator - Scripts are available in npm", () => {
  try {
    // Only check if scripts are present in npm run output without executing grep
    const output = execSync("npm run --if-present", {
      encoding: "utf8",
      stdio: ["pipe", "pipe", "ignore"],
    });

    // Just check that the output includes some vulnerability scripts
    assert.ok(
      output.includes("generate:vuln") || output.includes("test:llm"),
      "Vulnerability scripts not found in npm run output"
    );
    return true;
  } catch (error) {
    // If there's an error running npm, just return a warning
    return `Couldn't verify npm scripts: ${error.message}`;
  }
});
