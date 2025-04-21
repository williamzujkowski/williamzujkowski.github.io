/**
 * Global teardown for Playwright tests
 * Part of Phase 4 testing implementation
 */

/**
 * Clean up after tests
 * @param {import('@playwright/test').FullConfig} testConfig
 */
async function globalTeardown(testConfig) {
  // Only kill the server if we started it
  if (global.__SERVER_PROCESS && !global.__SERVER_ALREADY_RUNNING) {
    console.log("Shutting down development server...");

    // Kill the server process
    if (process.platform === "win32") {
      // Windows requires a different approach to kill the process tree
      const { exec } = require("child_process");
      exec(`taskkill /pid ${global.__SERVER_PROCESS.pid} /T /F`, (error) => {
        if (error) {
          console.error("Failed to kill server process:", error);
        }
      });
    } else {
      // Unix-like systems can use kill
      try {
        process.kill(-global.__SERVER_PROCESS.pid);
      } catch (error) {
        console.error("Failed to kill server process:", error);
      }
    }

    console.log("Development server shut down");
  }
}

module.exports = globalTeardown;
