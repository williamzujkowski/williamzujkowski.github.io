/**
 * Vulnerability Blog Generator Integration Tests
 *
 * These tests verify that the vulnerability blog generator submodule
 * is properly integrated with the website and functioning correctly.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const assert = require("assert");

describe("Vulnerability Blog Generator Integration", () => {
  const submodulePath = path.join(process.cwd(), "tools", "vuln-blog");
  const postsPath = path.join(process.cwd(), "src", "posts");

  // Test that the submodule exists and has the expected files
  describe("Submodule Structure", () => {
    it("should have submodule directory", () => {
      assert.ok(fs.existsSync(submodulePath), "Submodule directory does not exist");
    });

    it("should contain essential files", () => {
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
    });

    it("should have prompts directory with templates", () => {
      const promptsDir = path.join(submodulePath, "prompts");
      assert.ok(fs.existsSync(promptsDir), "Prompts directory does not exist");

      const requiredPrompts = [
        "threat-blog-post.prompt",
        "threat-blog-post-rag.prompt",
      ];

      for (const file of requiredPrompts) {
        assert.ok(
          fs.existsSync(path.join(promptsDir, file)),
          `Required prompt template ${file} is missing`
        );
      }
    });
  });

  // Test that package.json scripts are properly updated
  describe("Package.json Scripts", () => {
    let packageJson;

    before(() => {
      const packageJsonPath = path.join(process.cwd(), "package.json");
      packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
    });

    it("should have vulnerability generator scripts", () => {
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
    });

    it("should point scripts to the submodule directory", () => {
      const scriptsToCheck = [
        "generate:vuln",
        "generate:latest",
        "schedule:vuln",
        "test:openai",
      ];

      for (const script of scriptsToCheck) {
        assert.ok(
          packageJson.scripts[script].includes("tools/vuln-blog"),
          `Script ${script} does not point to the submodule directory`
        );
      }
    });
  });

  // Test workflow files
  describe("GitHub Actions Workflows", () => {
    let vulnerabilityWorkflow;
    let testProvidersWorkflow;

    before(() => {
      const workflowsDir = path.join(process.cwd(), ".github", "workflows");

      // Note: In a real test, we'd use a YAML parser here instead of this simplistic approach
      vulnerabilityWorkflow = fs.readFileSync(
        path.join(workflowsDir, "vulnerability-posts.yml"),
        "utf8"
      );

      testProvidersWorkflow = fs.readFileSync(
        path.join(workflowsDir, "test-llm-providers.yml"),
        "utf8"
      );
    });

    it("should have submodules: recursive in checkout step", () => {
      assert.ok(
        vulnerabilityWorkflow.includes("submodules: recursive"),
        "vulnerability-posts.yml does not checkout with submodules: recursive"
      );

      assert.ok(
        testProvidersWorkflow.includes("submodules: recursive"),
        "test-llm-providers.yml does not checkout with submodules: recursive"
      );
    });

    it("should install submodule dependencies", () => {
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
    });

    it("should set OUTPUT_DIR environment variable", () => {
      assert.ok(
        vulnerabilityWorkflow.includes("OUTPUT_DIR:"),
        "vulnerability-posts.yml does not set OUTPUT_DIR environment variable"
      );
    });
  });

  // Test npm scripts functionality (mocked)
  describe("Script Functionality", () => {
    // This is a mock test that doesn't actually run the scripts
    // In a real test, you would either run with mock API keys or use dependency injection

    it("should be able to list scripts", () => {
      const output = execSync("npm run --if-present | grep vuln", {
        encoding: "utf8",
        stdio: ["pipe", "pipe", "ignore"],
      });

      assert.ok(
        output.includes("generate:vuln") && output.includes("test:llm"),
        "Vulnerability scripts not found in npm run output"
      );
    });
  });
});
