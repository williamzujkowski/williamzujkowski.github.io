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

// Function to transform metrics data to dashboard format
function transformMetricsData(metricsData) {
  // Create dashboard data that matches the format expected by the UI
  return {
    totalRuns: metricsData.totalRuns || 0,
    avgProcessingTime: metricsData.avgProcessingTime || 0,
    avgTokenUsage:
      metricsData.totalRuns > 0
        ? (metricsData.totalTokens || 0) / metricsData.totalRuns
        : 0,
    totalCost: metricsData.totalCost || 0,
    // Transform runsByDate from object to array format
    runsByDate: Object.entries(metricsData.runsByDate || {})
      .map(([date, count]) => ({ date, count }))
      .sort((a, b) => a.date.localeCompare(b.date)),
    // Transform runsByModel from object to array format
    runsByModel: Object.entries(metricsData.runsByModel || {})
      .map(([model, count]) => ({ model, count }))
      .sort((a, b) => b.count - a.count),
    // Use runs array as recentRuns, transforming as needed
    recentRuns: (metricsData.runs || []).map((run) => ({
      id: run.id,
      name: run.name,
      startTime: run.startTime,
      endTime: run.endTime,
      status: run.status,
      model: run.model,
      inputTokens: run.inputTokens || 0,
      outputTokens: run.outputTokens || 0,
      cost: run.cost || 0,
    })),
    lastUpdated: metricsData.lastUpdated || new Date().toISOString(),
    dataSource: "local",
  };
}

// Main function
function main() {
  try {
    console.log("Ensuring dashboard data is available...");

    // Check if source data exists
    if (fs.existsSync(sourceDataPath)) {
      console.log(`Source data found at: ${sourceDataPath}`);

      // Read the metrics data
      const metricsData = JSON.parse(fs.readFileSync(sourceDataPath, "utf8"));

      // Transform data for dashboard format
      const dashboardData = transformMetricsData(metricsData);

      // Write the transformed data to the assets directory
      fs.writeFileSync(targetDataPath, JSON.stringify(dashboardData, null, 2), "utf8");
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
