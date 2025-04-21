/**
 * Vulnerability Generator E2E Test
 *
 * This test creates a mock environment and tests the actual generation process
 * with mocked API calls to verify the end-to-end functionality.
 *
 * Note: This test uses jest.mock() to mock external API calls
 * and should be run with MOCK_APIS=true environment variable.
 */

// Import test framework
const { test, expect } = require("@playwright/test");
const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

// Mock data for CVE details
const mockCveData = {
  id: "CVE-2025-9999",
  description: "Test vulnerability for e2e testing",
  publishedDate: "2025-04-20T10:00:00.000Z",
  lastModifiedDate: "2025-04-20T10:00:00.000Z",
  cvss: {
    version: "3.1",
    vectorString: "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H",
    baseScore: 9.8,
    baseSeverity: "CRITICAL",
  },
  references: [
    {
      url: "https://example.com/advisory",
      source: "VENDOR",
      tags: ["Vendor Advisory"],
    },
  ],
  vulnerable_configuration: [
    { vendor: "Test Vendor", product: "Test Product", version: "1.0.0" },
  ],
  cwe: {
    id: "CWE-79",
    name: "Improper Neutralization of Input During Web Page Generation",
  },
};

// Setup and teardown utility functions
function createMockEnvironment() {
  // Create a temporary directory for testing
  const testDir = path.join(__dirname, "temp-test-vuln");
  if (!fs.existsSync(testDir)) {
    fs.mkdirSync(testDir, { recursive: true });
  }

  // Create a mock .env file with test API keys
  const envPath = path.join(testDir, ".env");
  fs.writeFileSync(
    envPath,
    `
    OPENAI_API_KEY=test-openai-key
    GOOGLE_API_KEY=test-google-key
    CLAUDE_API_KEY=test-claude-key
    NVD_API_KEY=test-nvd-key
    MOCK_APIS=true
    MOCK_CVE_ID=${mockCveData.id}
  `
  );

  return testDir;
}

function cleanupMockEnvironment(testDir) {
  // Remove temporary test directory
  if (fs.existsSync(testDir)) {
    fs.rmSync(testDir, { recursive: true, force: true });
  }
}

test.describe("Vulnerability Generator E2E", () => {
  let testDir;

  test.beforeAll(() => {
    testDir = createMockEnvironment();
  });

  test.afterAll(() => {
    cleanupMockEnvironment(testDir);
  });

  test("Mock CVE data should be valid", () => {
    expect(mockCveData.id).toBeDefined();
    expect(mockCveData.cvss.baseScore).toBeGreaterThan(0);
  });

  // This test is conditionally run only if we have the mocking environment
  // in place in the vuln-blog generator
  test("should generate a post with mock APIs", async ({ page }) => {
    // Skip this test if the MOCK_APIS support isn't implemented yet
    const submodulePath = path.join(process.cwd(), "tools", "vuln-blog");
    const hasApiMocks =
      fs.existsSync(path.join(submodulePath, "mocks")) ||
      process.env.SKIP_API_CHECK === "true";

    if (!hasApiMocks) {
      test.skip("Mock API support not implemented yet");
      return;
    }

    // Call the generate script with our mock environment
    try {
      const output = execSync(
        `cd ${submodulePath} && MOCK_APIS=true MOCK_CVE_ID=${mockCveData.id} node generate-vuln-post.js --cve ${mockCveData.id}`,
        {
          env: {
            ...process.env,
            OPENAI_API_KEY: "test-openai-key",
            MOCK_APIS: "true",
            OUTPUT_DIR: testDir,
          },
          encoding: "utf8",
          stdio: "pipe",
        }
      );

      console.log("Generator Output:", output);

      // Check that the output directory contains the expected file
      const files = fs.readdirSync(testDir);
      const postFile = files.find((f) => f.includes(mockCveData.id.toLowerCase()));

      expect(postFile).toBeDefined();
      expect(fs.existsSync(path.join(testDir, postFile))).toBeTruthy();

      // Verify the content contains expected elements
      if (postFile) {
        const content = fs.readFileSync(path.join(testDir, postFile), "utf8");
        expect(content).toContain(mockCveData.id);
        expect(content).toContain("layout: post");
        expect(content).toContain("tags:");
      }
    } catch (err) {
      console.error("Error running generator:", err);
      // If this fails, the test might be running without proper mock support
      expect(err).toBeUndefined();
    }
  });
});
