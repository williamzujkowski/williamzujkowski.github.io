/**
 * debug-config.js - Debug script to check navigation configuration loading
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get the directory name in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function readJsonFile(filePath) {
  try {
    const data = fs.readFileSync(filePath, "utf8");
    return JSON.parse(data);
  } catch (error) {
    console.error(`Error reading JSON file ${filePath}:`, error.message);
    return {};
  }
}

// Check navigation config
console.log("DEBUGGING NAVIGATION CONFIG LOADING");

// Check all possible locations for navigation.json
const possibleNavPaths = [
  path.join(__dirname, "config", "navigation.json"),
  path.join(__dirname, "navigation.json"),
  path.join(__dirname, "..", "_data", "config", "navigation.json"),
  path.join(__dirname, "..", "config", "navigation.json"),
  path.join(__dirname, "..", "..", "config", "navigation.json"),
  path.join(__dirname, "..", "..", "src", "_data", "config", "navigation.json")
];

console.log("Checking all possible navigation.json locations:");
possibleNavPaths.forEach(navPath => {
  console.log(`Path: ${navPath}`);
  console.log(`File exists: ${fs.existsSync(navPath)}`);
  
  if (fs.existsSync(navPath)) {
    const navData = readJsonFile(navPath);
    console.log("Navigation data contents:");
    console.log(JSON.stringify(navData, null, 2));
  }
});

// Check where config directory exists relative to different paths
const baseLocations = [
  __dirname,
  path.join(__dirname, ".."),
  path.join(__dirname, "..", ".."),
  path.join(__dirname, "..", "..", "src")
];

console.log("\nChecking for config directories:");
baseLocations.forEach(baseDir => {
  const configDir = path.join(baseDir, "config");
  console.log(`Config dir at ${configDir} exists: ${fs.existsSync(configDir)}`);
  
  if (fs.existsSync(configDir)) {
    console.log(`Files in ${configDir}:`);
    fs.readdirSync(configDir).forEach(file => {
      console.log(`- ${file}`);
    });
  }
});

// Tracing the site.js loading process
console.log("\nDEBUGGING SITE.JS EXECUTION FLOW");

// Check site.js location and its imports
const siteJsPath = path.join(__dirname, "site.js");
console.log(`site.js exists: ${fs.existsSync(siteJsPath)}`);

if (fs.existsSync(siteJsPath)) {
  try {
    const siteJsContent = fs.readFileSync(siteJsPath, "utf8");
    console.log("First 500 chars of site.js:");
    console.log(siteJsContent.substring(0, 500));
    
    // Extract the navigation loading logic from site.js
    const navLoadSection = siteJsContent.match(/\/\/ Load navigation\.json[\s\S]*?}/s) || 
                          siteJsContent.match(/navigation\.json[\s\S]*?}/s) || 
                          siteJsContent.match(/navPath[\s\S]*?}/s);
    
    if (navLoadSection) {
      console.log("\nNavigation loading section in site.js:");
      console.log(navLoadSection[0]);
    } else {
      console.log("\nCouldn't find navigation loading section in site.js");
    }
  } catch (error) {
    console.error(`Error reading site.js:`, error.message);
  }
}

// Check if eleventy-navigation plugin is installed
const nodeModulesPath = path.join(__dirname, "..", "..", "node_modules", "@11ty", "eleventy-navigation");
console.log(`\neleventy-navigation plugin exists: ${fs.existsSync(nodeModulesPath)}`);

export default {
  debug: true,
  navigationPaths: possibleNavPaths.filter(p => fs.existsSync(p)),
  configDirs: baseLocations.filter(p => fs.existsSync(path.join(p, "config")))
};