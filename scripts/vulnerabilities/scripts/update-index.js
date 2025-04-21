#!/usr/bin/env node

/**
 * Vulnerability Index Update Script
 *
 * This script creates and updates a vulnerability knowledge index for
 * Retrieval-Augmented Generation (RAG) purposes. It fetches recent
 * vulnerabilities, processes them, and stores them in a searchable index.
 */

const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { program } = require("commander");
const dotenv = require("dotenv");

// Load environment variables
dotenv.config({ path: process.env.ENV_FILE || ".env.test" });

// Set up command line arguments
program
  .option("--days <days>", "Number of days to look back for vulnerabilities", "30")
  .option("--min-cvss <score>", "Minimum CVSS score to include", "7.0")
  .option("--output <path>", "Output path for the index file", "data/index.json")
  .option("--force", "Force rebuild the entire index")
  .parse(process.argv);

const options = program.opts();

// Ensure the data directory exists
const dataDir = path.dirname(options.output);
if (!fs.existsSync(dataDir)) {
  fs.mkdirSync(dataDir, { recursive: true });
}

/**
 * Fetch recent vulnerabilities from NVD API
 */
async function fetchRecentVulnerabilities() {
  const daysToLookBack = parseInt(options.days);
  const minCvssScore = parseFloat(options.min - cvss);

  // Get current date and format it
  const now = new Date();
  const startDate = new Date(now);
  startDate.setDate(now.getDate() - daysToLookBack);

  // Format dates for NVD API
  const pubStartDate = startDate.toISOString().split("T")[0];
  const pubEndDate = now.toISOString().split("T")[0];

  console.log(
    `Fetching vulnerabilities from ${pubStartDate} to ${pubEndDate} with CVSS >= ${minCvssScore}`
  );

  // Set up headers with API key if available
  const headers = {
    "User-Agent": "William Zujkowski Blog Vulnerability Analyzer",
  };

  if (process.env.NVD_API_KEY) {
    console.log("Using NVD API key for higher rate limits");
    headers["apiKey"] = process.env.NVD_API_KEY;
  }

  try {
    // Fetch data from NVD API with proper parameters
    const response = await axios.get(
      "https://services.nvd.nist.gov/rest/json/cves/2.0",
      {
        params: {
          pubStartDate,
          pubEndDate,
          resultsPerPage: 100, // Maximum per page
        },
        headers,
      }
    );

    if (response.data && response.data.vulnerabilities) {
      // Filter by CVSS score if specified
      const filteredVulnerabilities = response.data.vulnerabilities.filter((vuln) => {
        const metrics = vuln.cve.metrics;
        if (!metrics) return false;

        // Get the highest CVSS score available (v31, v30, or v2)
        let highestScore = 0;
        if (metrics.cvssMetricV31 && metrics.cvssMetricV31.length > 0) {
          highestScore = Math.max(
            highestScore,
            metrics.cvssMetricV31[0].cvssData.baseScore
          );
        }
        if (metrics.cvssMetricV30 && metrics.cvssMetricV30.length > 0) {
          highestScore = Math.max(
            highestScore,
            metrics.cvssMetricV30[0].cvssData.baseScore
          );
        }
        if (metrics.cvssMetricV2 && metrics.cvssMetricV2.length > 0) {
          highestScore = Math.max(
            highestScore,
            metrics.cvssMetricV2[0].cvssData.baseScore
          );
        }

        return highestScore >= minCvssScore;
      });

      console.log(
        `Found ${filteredVulnerabilities.length} vulnerabilities with CVSS >= ${minCvssScore}`
      );
      return filteredVulnerabilities;
    } else {
      console.error("No vulnerability data returned from NVD API");
      return [];
    }
  } catch (error) {
    console.error("Error fetching from NVD API:", error.message);
    if (error.response) {
      console.error("API Response Status:", error.response.status);
      console.error("API Response Data:", JSON.stringify(error.response.data));
    }
    return [];
  }
}

/**
 * Process vulnerability data into a searchable format
 */
function processVulnerabilities(vulnerabilities) {
  return vulnerabilities.map((vuln) => {
    const cve = vuln.cve;

    // Extract basic information
    const cveId = cve.id;
    const publishedDate = cve.published;
    const lastModifiedDate = cve.lastModified;

    // Get description
    let description = "No description available";
    if (cve.descriptions && cve.descriptions.length > 0) {
      const englishDesc = cve.descriptions.find((d) => d.lang === "en");
      if (englishDesc) {
        description = englishDesc.value;
      }
    }

    // Get severity and CVSS score
    let severity = "Unknown";
    let cvssScore = 0;
    let cvssVector = "";
    const metrics = cve.metrics;

    if (metrics) {
      // Try to get CVSS v3.1 data first, then v3.0, then v2.0
      if (metrics.cvssMetricV31 && metrics.cvssMetricV31.length > 0) {
        const cvssData = metrics.cvssMetricV31[0].cvssData;
        cvssScore = cvssData.baseScore;
        severity =
          metrics.cvssMetricV31[0].baseSeverity ||
          (cvssData.baseSeverity ? cvssData.baseSeverity : "Unknown");
        cvssVector = cvssData.vectorString || "";
      } else if (metrics.cvssMetricV30 && metrics.cvssMetricV30.length > 0) {
        const cvssData = metrics.cvssMetricV30[0].cvssData;
        cvssScore = cvssData.baseScore;
        severity =
          metrics.cvssMetricV30[0].baseSeverity ||
          (cvssData.baseSeverity ? cvssData.baseSeverity : "Unknown");
        cvssVector = cvssData.vectorString || "";
      } else if (metrics.cvssMetricV2 && metrics.cvssMetricV2.length > 0) {
        const cvssData = metrics.cvssMetricV2[0].cvssData;
        cvssScore = cvssData.baseScore;
        // V2 doesn't have severity directly, so calculate it
        if (cvssScore >= 9.0) severity = "CRITICAL";
        else if (cvssScore >= 7.0) severity = "HIGH";
        else if (cvssScore >= 4.0) severity = "MEDIUM";
        else if (cvssScore >= 0.1) severity = "LOW";
        else severity = "NONE";
        cvssVector = cvssData.vectorString || "";
      }
    }

    // Get CWE information
    const cweIds = [];
    if (cve.weaknesses) {
      cve.weaknesses.forEach((weakness) => {
        if (weakness.description) {
          weakness.description.forEach((desc) => {
            // Extract CWE ID from description
            const cweMatch = desc.value.match(/CWE-\d+/);
            if (cweMatch) {
              cweIds.push(cweMatch[0]);
            }
          });
        }
      });
    }

    // Get affected products
    const affectedProducts = [];
    if (cve.configurations) {
      cve.configurations.forEach((config) => {
        if (config.nodes) {
          config.nodes.forEach((node) => {
            if (node.cpeMatch) {
              node.cpeMatch.forEach((cpe) => {
                if (cpe.criteria) {
                  // Extract product name from CPE
                  const parts = cpe.criteria.split(":");
                  if (parts.length > 4) {
                    const vendor = parts[3];
                    const product = parts[4];
                    if (vendor && product) {
                      affectedProducts.push(`${vendor}:${product}`);
                    }
                  }
                }
              });
            }
          });
        }
      });
    }

    // Get references
    const references = [];
    if (cve.references) {
      cve.references.forEach((ref) => {
        if (ref.url) {
          references.push(ref.url);
        }
      });
    }

    // Create the indexed entry
    return {
      id: cveId,
      published: publishedDate,
      lastModified: lastModifiedDate,
      description: description,
      severity: severity,
      cvssScore: cvssScore,
      cvssVector: cvssVector,
      cweIds: [...new Set(cweIds)], // Remove duplicates
      affectedProducts: [...new Set(affectedProducts)], // Remove duplicates
      references: references,
      // Add the full text for search purposes
      fullText: `${cveId} ${description} ${severity} ${cvssVector} ${cweIds.join(" ")} ${affectedProducts.join(" ")}`,
    };
  });
}

/**
 * Create or update the vulnerability index
 */
async function updateIndex() {
  const indexPath = path.resolve(options.output);

  // Check if index exists and should be updated incrementally
  let existingIndex = [];
  const shouldRebuild = options.force || !fs.existsSync(indexPath);

  if (!shouldRebuild) {
    try {
      const indexData = fs.readFileSync(indexPath, "utf8");
      existingIndex = JSON.parse(indexData);
      console.log(`Loaded existing index with ${existingIndex.length} entries`);
    } catch (error) {
      console.error(`Error reading existing index: ${error.message}`);
      console.log("Falling back to rebuilding the index");
      existingIndex = [];
    }
  }

  // Fetch and process new vulnerabilities
  const vulnerabilities = await fetchRecentVulnerabilities();
  const processedVulnerabilities = processVulnerabilities(vulnerabilities);

  // Create the new index
  let newIndex;
  if (shouldRebuild) {
    // Full rebuild
    newIndex = processedVulnerabilities;
    console.log(`Created new index with ${newIndex.length} entries`);
  } else {
    // Incremental update - add new entries and update existing ones
    const existingIds = new Set(existingIndex.map((entry) => entry.id));
    const newEntries = processedVulnerabilities.filter(
      (entry) => !existingIds.has(entry.id)
    );

    // Update existing entries with new information
    const updatedExisting = existingIndex.map((existing) => {
      const updated = processedVulnerabilities.find((v) => v.id === existing.id);
      return updated || existing;
    });

    // Combine updated existing entries with new ones
    newIndex = [...updatedExisting, ...newEntries];
    console.log(
      `Updated index with ${newEntries.length} new entries, total: ${newIndex.length}`
    );
  }

  // Add metadata to the index
  const indexWithMetadata = {
    metadata: {
      timestamp: new Date().toISOString(),
      count: newIndex.length,
      minCvss: parseFloat(options["min-cvss"]),
      daysBack: parseInt(options.days),
    },
    vulnerabilities: newIndex,
  };

  // Write the index to the output file
  fs.writeFileSync(indexPath, JSON.stringify(indexWithMetadata, null, 2));
  console.log(`Index saved to ${indexPath}`);

  // Print some stats
  const severityCounts = newIndex.reduce((acc, vuln) => {
    acc[vuln.severity] = (acc[vuln.severity] || 0) + 1;
    return acc;
  }, {});

  console.log("Severity distribution:");
  Object.entries(severityCounts).forEach(([severity, count]) => {
    console.log(`  ${severity}: ${count}`);
  });
}

// Main execution
updateIndex().catch((error) => {
  console.error("Error updating vulnerability index:", error.message);
  process.exit(1);
});
