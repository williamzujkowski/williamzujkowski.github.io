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

// Function to transform data structure for dashboard
function transformDataForDashboard(data) {
  const transformed = { ...data };

  // Transform runsByDate from object to array of objects
  if (
    typeof transformed.runsByDate === "object" &&
    !Array.isArray(transformed.runsByDate)
  ) {
    transformed.runsByDate = Object.entries(transformed.runsByDate).map(
      ([date, count]) => ({
        date,
        count,
      })
    );
  }

  // Transform runsByModel from object to array of objects
  if (
    typeof transformed.runsByModel === "object" &&
    !Array.isArray(transformed.runsByModel)
  ) {
    transformed.runsByModel = Object.entries(transformed.runsByModel).map(
      ([model, count]) => ({
        model,
        count,
      })
    );
  }

  // Calculate avgTokenUsage if not already present
  if (!transformed.avgTokenUsage && transformed.totalTokens && transformed.totalRuns) {
    transformed.avgTokenUsage = transformed.totalTokens / transformed.totalRuns;
  }

  // Make sure recentRuns contains simplified data for dashboard
  if (transformed.runs && Array.isArray(transformed.runs)) {
    transformed.recentRuns = transformed.runs.map((run) => ({
      id: run.id,
      name: run.name,
      startTime: run.startTime,
      endTime: run.endTime,
      status: run.status,
      model: run.model,
      inputTokens: run.inputTokens,
      outputTokens: run.outputTokens,
      cost: run.cost,
      metadata: run.metadata,
    }));
  }

  // Add data source info
  transformed.dataSource = transformed.dataSource || "local";

  return transformed;
}

// Main function
function main() {
  try {
    console.log("Ensuring dashboard data is available...");

    // Check if source data exists
    if (fs.existsSync(sourceDataPath)) {
      console.log(`Source data found at: ${sourceDataPath}`);

      // Read the source data
      const rawData = JSON.parse(fs.readFileSync(sourceDataPath, "utf8"));

      // Transform data for dashboard
      const transformedData = transformDataForDashboard(rawData);

      // Write the transformed data to the assets directory
      fs.writeFileSync(
        targetDataPath,
        JSON.stringify(transformedData, null, 2),
        "utf8"
      );
      console.log(`Transformed data saved to: ${targetDataPath}`);
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

// Export function for direct import
export function ensureDashboardData() {
  main();
}

// Run the script when executed directly
if (import.meta.url === import.meta.main) {
  main();
}
