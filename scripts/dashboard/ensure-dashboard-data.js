#!/usr/bin/env node

/**
 * Ensure Dashboard Data
 *
 * This script ensures that the dashboard data is available in the assets directory
 * by either copying the data or creating a symbolic link.
 */

import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

// Get dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Define paths
const sourceDataPath = path.resolve(__dirname, "../../src/_data/core/llm-metrics.json");
const assetsDir = path.resolve(__dirname, "../../assets/data");
const targetDataPath = path.resolve(assetsDir, "langsmith-data.json");

// Ensure assets/data directory exists
if (!fs.existsSync(assetsDir)) {
  console.log(`Creating directory: ${assetsDir}`);
  fs.mkdirSync(assetsDir, { recursive: true });
}

// Function to create empty default data
function createDefaultData() {
  const defaultData = {
    totalRuns: 0,
    avgProcessingTime: 0,
    avgTokenUsage: 0,
    runsByDate: [],
    runsByModel: [],
    recentRuns: [],
    lastUpdated: new Date().toISOString(),
    isDefault: true,
  };

  fs.writeFileSync(targetDataPath, JSON.stringify(defaultData, null, 2), "utf8");
  console.log(`Created default dashboard data at: ${targetDataPath}`);
}

// Main function
function main() {
  try {
    console.log("Ensuring dashboard data is available...");

    // Check if source data exists
    if (fs.existsSync(sourceDataPath)) {
      console.log(`Source data found at: ${sourceDataPath}`);

      // Copy the data to the assets directory
      fs.copyFileSync(sourceDataPath, targetDataPath);
      console.log(`Data copied to: ${targetDataPath}`);
    } else {
      console.log(`Source data not found at: ${sourceDataPath}`);

      // Check if target already exists
      if (!fs.existsSync(targetDataPath)) {
        console.log("Creating default dashboard data...");
        createDefaultData();
      } else {
        console.log(`Target data already exists at: ${targetDataPath}`);
      }
    }

    console.log("Dashboard data check complete!");
  } catch (error) {
    console.error("Error ensuring dashboard data:", error);
    process.exit(1);
  }
}

// Run the script
main();
