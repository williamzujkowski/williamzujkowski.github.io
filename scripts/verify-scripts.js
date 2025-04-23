/**
 * Script Verification Utility
 *
 * This script verifies that all scripts referenced in package.json actually exist
 * and are in the expected locations.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Root directory
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, "..");

// Read package.json
const packageJsonPath = path.join(rootDir, "package.json");
let packageJson;

try {
  packageJson = JSON.parse(fs.readFileSync(packageJsonPath, "utf8"));
} catch (error) {
  console.error("Error reading package.json:", error.message);
  process.exit(1);
}

// Extract script paths from package.json
const scriptPaths = [];
const scriptCommands = Object.values(packageJson.scripts || {});

// Regular expression to match node script paths
const scriptPathRegex = /node\s+([^\s]+\.js)/g;

let match;
scriptCommands.forEach((command) => {
  // Reset regex for each command
  scriptPathRegex.lastIndex = 0;

  // Find all script paths in the command
  while ((match = scriptPathRegex.exec(command)) !== null) {
    scriptPaths.push(match[1]);
  }
});

console.log(`Found ${scriptPaths.length} script references in package.json`);

// Check if each script exists
const missingScripts = [];

scriptPaths.forEach((scriptPath) => {
  const fullPath = path.join(rootDir, scriptPath);

  if (!fs.existsSync(fullPath)) {
    missingScripts.push({
      path: scriptPath,
      fullPath,
    });
  }
});

// Print results
if (missingScripts.length === 0) {
  console.log("✅ All scripts referenced in package.json exist.");
} else {
  console.error(`❌ Found ${missingScripts.length} missing scripts:`);
  missingScripts.forEach((script) => {
    console.error(`   - ${script.path} (${script.fullPath})`);
  });
  process.exit(1);
}

// Check for inconsistent script naming patterns
const scriptFilenames = scriptPaths.map((p) => path.basename(p));
const scriptNamePatterns = {
  kebabCase: /^[a-z]+(-[a-z]+)*\.js$/,
  camelCase: /^[a-z]+([A-Z][a-z]+)*\.js$/,
  snake_case: /^[a-z]+(_[a-z]+)*\.js$/,
  PascalCase: /^[A-Z][a-z]+([A-Z][a-z]+)*\.js$/,
};

// Count patterns
const patternCounts = {};
Object.keys(scriptNamePatterns).forEach((pattern) => {
  patternCounts[pattern] = 0;
});

// Check each script against patterns
scriptFilenames.forEach((filename) => {
  Object.entries(scriptNamePatterns).forEach(([pattern, regex]) => {
    if (regex.test(filename)) {
      patternCounts[pattern]++;
    }
  });
});

// Determine dominant pattern
let dominantPattern = null;
let maxCount = 0;

Object.entries(patternCounts).forEach(([pattern, count]) => {
  if (count > maxCount) {
    maxCount = count;
    dominantPattern = pattern;
  }
});

console.log("\nScript naming pattern analysis:");
Object.entries(patternCounts).forEach(([pattern, count]) => {
  const percentage = ((count / scriptFilenames.length) * 100).toFixed(1);
  console.log(`   - ${pattern}: ${count} scripts (${percentage}%)`);
});

if (dominantPattern) {
  console.log(`\nDominant naming pattern: ${dominantPattern}`);

  // Check for inconsistent scripts
  const inconsistentScripts = scriptFilenames.filter(
    (filename) => !scriptNamePatterns[dominantPattern].test(filename)
  );

  if (inconsistentScripts.length > 0) {
    console.log(
      `\n⚠️ Found ${inconsistentScripts.length} scripts with inconsistent naming:`
    );
    inconsistentScripts.forEach((script) => {
      console.log(`   - ${script}`);
    });
    console.log(
      `\nConsider renaming these scripts to match the dominant ${dominantPattern} pattern for consistency.`
    );
  } else {
    console.log("\n✅ All scripts follow consistent naming patterns.");
  }
}
