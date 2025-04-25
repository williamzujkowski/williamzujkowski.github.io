/**
 * Ensure Dashboard Data - CommonJS Wrapper
 *
 * This is a CommonJS wrapper around the ES Module ensure-dashboard-data.js script.
 * It allows the script to be required by CommonJS modules like .eleventy.cjs.
 */

const path = require("path");
const { execSync } = require("child_process");

// Function to execute the ES module version
function ensureDashboardData() {
  try {
    const scriptPath = path.join(__dirname, "ensure-dashboard-data.js");
    console.log(`Running dashboard data script: ${scriptPath}`);

    execSync(`node ${scriptPath}`, {
      stdio: "inherit",
    });

    return true;
  } catch (error) {
    console.error("Error running dashboard data script:", error);
    return false;
  }
}

// Export for direct importing
module.exports = {
  ensureDashboardData,
};

// Run directly if called as a script
if (require.main === module) {
  ensureDashboardData();
}
