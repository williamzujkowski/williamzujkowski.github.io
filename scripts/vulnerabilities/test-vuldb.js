#!/usr/bin/env node

/**
 * VulDB Integration Test Script
 *
 * This script tests the VulDB integration to verify
 * it is working correctly with a specific CVE.
 *
 * Usage:
 *   node test-vuldb.js [--cve CVE-ID]
 */

const axios = require("axios");
const dotenv = require("dotenv");
const { program } = require("commander");
const { parseString } = require("xml2js");

// Load environment variables
dotenv.config({ path: process.env.ENV_FILE || ".env.test" });

program
  .option("--cve <cve-id>", "Test with a specific CVE (default: CVE-2023-50164)")
  .parse(process.argv);

const options = program.opts();
const cveId = options.cve || "CVE-2023-50164";

// Helper function to parse XML using xml2js
const parseXml = (xml) => {
  return new Promise((resolve, reject) => {
    parseString(xml, (err, result) => {
      if (err) reject(err);
      else resolve(result);
    });
  });
};

// Function to test VulDB data retrieval
async function testVulDb(cveId) {
  try {
    console.log(`Checking VulDB for information on ${cveId}...`);

    // Fetch the VulDB RSS feed for recent vulnerabilities
    const response = await axios.get("https://vuldb.com/?rss.recent", {
      timeout: 10000,
    });

    const parsedData = await parseXml(response.data);

    // Get items from the feed
    const items = parsedData?.rss?.channel?.[0]?.item || [];

    console.log(`Found ${items.length} items in VulDB feed`);

    // Filter for items related to the CVE
    const relevantItems = items.filter((item) => {
      const title = item.title?.[0] || "";
      const description = item.description?.[0] || "";
      const guid = item.guid?.[0]?._ || item.guid?.[0] || "";

      // Look for the CVE ID in title, description, and guid
      return (
        title.includes(cveId) || description.includes(cveId) || guid.includes(cveId)
      );
    });

    if (relevantItems.length === 0) {
      console.log(`No information found in VulDB for ${cveId}`);

      // Show sample items instead
      console.log("\nSample items from VulDB feed:");
      if (items.length > 0) {
        const sampleItems = items.slice(0, 3);
        sampleItems.forEach((item, index) => {
          console.log(`\n${index + 1}. ${item.title?.[0] || "Unknown Title"}`);
          console.log(`   Published: ${item.pubDate?.[0] || "Unknown"}`);
          console.log(`   Link: ${item.link?.[0] || "Unknown"}`);
        });
      }

      return null;
    }

    console.log(
      `Found ${relevantItems.length} items in VulDB feed related to ${cveId}`
    );

    // Format the relevant information
    const vuldbData = relevantItems.map((item) => {
      // Extract data from the item
      const title = item.title?.[0] || "";
      const description = item.description?.[0] || "";
      const pubDate = item.pubDate?.[0] || "";
      const link = item.link?.[0] || "";
      const guid = item.guid?.[0]?._ || item.guid?.[0] || "";

      // Try to extract VulDB ID from the guid or link
      let vuldbId = null;
      const vuldbIdMatch = guid.match(/vuldb-id-(\d+)/) || link.match(/id=(\d+)/);
      if (vuldbIdMatch) {
        vuldbId = vuldbIdMatch[1];
      }

      // Try to extract severity
      let severity = null;
      const severityMatch =
        description.match(/Risk Level:\s*(Critical|High|Medium|Low)/i) ||
        title.match(/(Critical|High|Medium|Low)\s+Risk/i);
      if (severityMatch) {
        severity = severityMatch[1];
      }

      // Try to extract CVSS score
      let cvssScore = null;
      const cvssMatch =
        description.match(/CVSS Base Score:\s*(\d+(\.\d+)?)/i) ||
        description.match(/CVSS v\d\s+Score:\s*(\d+(\.\d+)?)/i);
      if (cvssMatch) {
        cvssScore = cvssMatch[1];
      }

      // Try to extract affected products
      let affectedProducts = [];
      // VulDB often lists affected products after "Affected products:" or similar phrases
      const productSection = description.match(/Affected products?:([^.]*)\.?/i);
      if (productSection && productSection[1]) {
        // Split by commas and clean up each entry
        affectedProducts = productSection[1]
          .split(/,|;/)
          .map((p) => p.trim())
          .filter(Boolean);
      }

      // Extract vulnerability type from title if possible
      let vulnType = null;
      // VulDB titles often follow pattern: "Product - Vulnerability Type (CVSS Score)"
      const vulnTypeMatch = title.match(/.*?-\s*(.*?)\s*(\(|$)/);
      if (vulnTypeMatch && vulnTypeMatch[1]) {
        vulnType = vulnTypeMatch[1].trim();
      }

      return {
        title: title,
        description: description,
        pubDate: pubDate,
        link: link,
        vuldbId: vuldbId ? `VDB-${vuldbId}` : null,
        severity: severity,
        cvssScore: cvssScore,
        affectedProducts: affectedProducts.length > 0 ? affectedProducts : null,
        vulnType: vulnType,
      };
    });

    // Print the results
    console.log("\nVulDB Data Results:");
    vuldbData.forEach((item, index) => {
      console.log(`\n${index + 1}. ${item.title}`);
      if (item.vuldbId) {
        console.log(`   VulDB ID: ${item.vuldbId}`);
      }
      console.log(`   Published: ${item.pubDate}`);
      console.log(`   Link: ${item.link}`);
      if (item.severity) {
        console.log(`   Severity: ${item.severity}`);
      }
      if (item.cvssScore) {
        console.log(`   CVSS Score: ${item.cvssScore}`);
      }
      if (item.vulnType) {
        console.log(`   Vulnerability Type: ${item.vulnType}`);
      }
      if (item.affectedProducts) {
        console.log(`   Affected Products: ${item.affectedProducts.join(", ")}`);
      }

      // Print a short excerpt of the description
      if (item.description) {
        const excerpt = item.description.replace(/<[^>]*>/g, "").substring(0, 150);
        console.log(`   Description: ${excerpt}...`);
      }
    });

    return vuldbData;
  } catch (error) {
    console.error("Error fetching data from VulDB:", error.message);
    if (error.response) {
      console.error("Status:", error.response.status);
      console.error("Headers:", error.response.headers);
    }
    return null;
  }
}

// Run the test
async function main() {
  console.log(`=== Testing VulDB Integration with ${cveId} ===\n`);

  try {
    console.time("VulDB Test");
    const result = await testVulDb(cveId);
    console.timeEnd("VulDB Test");

    if (result) {
      console.log(`\n✅ Successfully retrieved data from VulDB for ${cveId}!`);
    } else {
      console.log(`\n❌ No relevant data found in VulDB for ${cveId}.`);
      console.log("This could be because:");
      console.log("1. The vulnerability is not in the recent VulDB feed");
      console.log("2. VulDB uses a different identifier for this vulnerability");
      console.log("3. The feed format has changed and needs updating");
    }
  } catch (error) {
    console.error("\n❌ Test failed with error:", error.message);
  }
}

// Execute the main function
main().catch((error) => {
  console.error("Unhandled error:", error);
  process.exit(1);
});
