#!/usr/bin/env node

/**
 * Vulnerability Blog Post Scheduler
 *
 * This script manages the scheduling of vulnerability blog posts,
 * ensuring we maintain the desired frequency (max once per day, min weekly rollup)
 *
 * It can be run as a cron job to automatically generate and schedule posts.
 *
 * Usage:
 *   node schedule-posts.js
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");
const { format, subDays, parseISO, isAfter } = require("date-fns");

// Configuration
const MAX_FREQUENCY_DAYS = 1; // Maximum of one post per day
const MIN_FREQUENCY_DAYS = 7; // Minimum weekly rollup if no posts
const POSTS_DIRECTORY = path.join(__dirname, "../../src/posts");
const LOG_FILE = path.join(__dirname, "vulnerability-posts.log");

// Function to log activity
function logActivity(message) {
  const timestamp = format(new Date(), "yyyy-MM-dd HH:mm:ss");
  const logEntry = `[${timestamp}] ${message}\n`;

  fs.appendFileSync(LOG_FILE, logEntry);
  console.log(message);
}

// Function to find the most recent vulnerability post
function findMostRecentPost() {
  try {
    const files = fs.readdirSync(POSTS_DIRECTORY);

    // Filter for vulnerability posts
    const vulnPosts = files.filter(
      (file) => file.startsWith("20") && file.includes("vulnerability-analysis")
    );

    if (vulnPosts.length === 0) {
      return null;
    }

    // Sort by date (filenames start with date)
    vulnPosts.sort().reverse();

    // Return the most recent
    return vulnPosts[0];
  } catch (error) {
    logActivity(`Error finding most recent post: ${error.message}`);
    return null;
  }
}

// Function to extract date from filename
function extractDateFromFilename(filename) {
  const dateMatch = filename.match(/^(\d{4}-\d{2}-\d{2})/);
  if (dateMatch && dateMatch[1]) {
    return parseISO(dateMatch[1]);
  }
  return null;
}

// Function to check if we should generate a new post
function shouldGeneratePost() {
  const mostRecentPost = findMostRecentPost();

  if (!mostRecentPost) {
    logActivity("No previous posts found. Will generate a new post.");
    return { generate: true, type: "latest" };
  }

  const lastPostDate = extractDateFromFilename(mostRecentPost);
  const today = new Date();
  const daysSinceLastPost = Math.floor((today - lastPostDate) / (1000 * 60 * 60 * 24));

  if (daysSinceLastPost >= MIN_FREQUENCY_DAYS) {
    logActivity(
      `${daysSinceLastPost} days since last post. Will generate a weekly rollup.`
    );
    return { generate: true, type: "weekly" };
  }

  if (daysSinceLastPost >= MAX_FREQUENCY_DAYS) {
    logActivity(
      `${daysSinceLastPost} days since last post. Will generate a post for latest critical vulnerability.`
    );
    return { generate: true, type: "latest" };
  }

  logActivity(`Only ${daysSinceLastPost} days since last post. Skipping.`);
  return { generate: false };
}

// Function to find a recent critical CVE
function findRecentCriticalCVE() {
  try {
    // In a real implementation, this would query NVD API
    // For now, we'll return a placeholder
    logActivity("Searching for recent critical CVEs...");
    return "CVE-2023-12345"; // Placeholder
  } catch (error) {
    logActivity(`Error finding recent CVE: ${error.message}`);
    return null;
  }
}

// Main function
function main() {
  logActivity("Starting vulnerability post scheduler");

  const { generate, type } = shouldGeneratePost();

  if (!generate) {
    logActivity("No post needed at this time");
    return;
  }

  try {
    if (type === "latest") {
      const cveId = findRecentCriticalCVE();
      if (!cveId) {
        logActivity("Failed to find a recent critical CVE");
        return;
      }

      logActivity(`Generating post for ${cveId}`);
      execSync(`node ${path.join(__dirname, "generate-vuln-post.js")} --cve ${cveId}`, {
        stdio: "inherit",
      });
    } else if (type === "weekly") {
      logActivity("Generating weekly rollup");
      execSync(`node ${path.join(__dirname, "generate-vuln-post.js")} --weekly`, {
        stdio: "inherit",
      });
    }

    logActivity("Post generation completed successfully");
  } catch (error) {
    logActivity(`Error generating post: ${error.message}`);
  }
}

// Run the main function
main();
