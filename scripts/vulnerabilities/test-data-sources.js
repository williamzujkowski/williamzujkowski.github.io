#!/usr/bin/env node

/**
 * Data Sources Integration Test Script
 *
 * This script tests each of the integrated data sources to verify
 * they are working correctly.
 *
 * Usage:
 *   node test-data-sources.js [--cve CVE-ID]
 */

const axios = require("axios");
const dotenv = require("dotenv");
const { program } = require("commander");

// Load environment variables
dotenv.config({ path: process.env.ENV_FILE || ".env.test" });

program
  .option("--cve <cve-id>", "Test with a specific CVE (default: CVE-2023-50164)")
  .parse(process.argv);

const options = program.opts();
const cveId = options.cve || "CVE-2023-50164";

// Function to set up a standardized test
async function runTest(name, testFunction) {
  console.log(`\n========== Testing ${name} ==========`);
  try {
    console.time(name);
    const result = await testFunction(cveId);
    console.timeEnd(name);

    if (result === null) {
      console.log(`✅ Test completed: No data available from ${name}`);
      return;
    }

    console.log(`✅ Test completed successfully: ${name}`);

    // Print a summary of the data received
    console.log("\nData Summary:");
    if (typeof result === "string") {
      console.log(result);
    } else if (Array.isArray(result)) {
      console.log(`Received ${result.length} items`);
      if (result.length > 0) {
        console.log("First item sample:");
        console.log(JSON.stringify(result[0], null, 2).substring(0, 300) + "...");
      }
    } else {
      const summary = JSON.stringify(result, null, 2);
      console.log(summary.substring(0, 500) + (summary.length > 500 ? "..." : ""));
    }
  } catch (error) {
    console.log(`❌ Test failed: ${error.message}`);
    if (error.response) {
      console.log(`Status: ${error.response.status}`);
      console.log("Response data:", error.response.data);
    }
  }
}

// Test NVD API
async function testNvdApi(cveId) {
  console.log(`Testing NVD API for ${cveId}...`);

  // Set up headers with API key if available
  const headers = {
    "User-Agent": "William Zujkowski Blog Vulnerability Analyzer",
  };

  // Add NVD API key if available
  if (process.env.NVD_API_KEY) {
    console.log("Using NVD API key for higher rate limits");
    headers["apiKey"] = process.env.NVD_API_KEY;
  }

  const response = await axios.get(
    `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${cveId}`,
    { headers }
  );
  if (
    response.data &&
    response.data.vulnerabilities &&
    response.data.vulnerabilities.length > 0
  ) {
    return response.data.vulnerabilities[0].cve;
  }
  return null;
}

// Test MITRE API
async function testMitreApi(cveId) {
  if (process.env.MITRE_API_ENABLED !== "true") {
    console.log("MITRE API is disabled in .env file");
    return null;
  }

  console.log(`Fetching data from MITRE API for ${cveId}...`);
  const headers = {
    "User-Agent":
      process.env.MITRE_USER_AGENT || "William Zujkowski Blog Vulnerability Analyzer",
  };

  // MITRE API endpoint for specific CVE
  const response = await axios.get(`https://cveawg.mitre.org/api/cve/${cveId}`, {
    headers,
  });

  if (response.data && response.data.cveMetadata) {
    return response.data;
  }
  return null;
}

// Test CISA KEV
async function testCisaKev(cveId) {
  if (process.env.CISA_KEV_ENABLED !== "true") {
    console.log("CISA KEV is disabled in .env file");
    return null;
  }

  console.log(`Checking if ${cveId} is in CISA KEV catalog...`);
  const response = await axios.get(
    "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
  );
  if (response.data && response.data.vulnerabilities) {
    // Match regardless of format (some are CVE-YYYY-NNNNN, others are CVE-YYYY-NNNNN...)
    const normalizedCveId = cveId.toUpperCase().trim();
    const found = response.data.vulnerabilities.find((v) => {
      const kevId = v.cveID || ""; // Handle potentially undefined cveID
      return kevId.toUpperCase().trim() === normalizedCveId;
    });

    if (found) {
      return found;
    }

    // Return the first few vulnerabilities as a sample
    return {
      message: `${cveId} not found in KEV catalog`,
      sample: response.data.vulnerabilities.slice(0, 3),
    };
  }
  return null;
}

// Test Exploit-DB
async function testExploitDb(cveId) {
  if (process.env.EXPLOIT_DB_ENABLED !== "true") {
    console.log("Exploit-DB is disabled in .env file");
    return null;
  }

  console.log(`Checking Exploit-DB for exploits related to ${cveId}...`);

  try {
    // Exploit-DB provides a CSV file with all exploits
    const response = await axios.get(
      "https://www.exploit-db.com/download/exploitdb.csv"
    );

    // Simple parsing of CSV to find entries matching our CVE
    const lines = response.data.split("\n");
    const exploits = [];

    // Skip header line
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i];
      if (line.includes(cveId)) {
        const fields = line.split(",");
        // CSV format: id,file,description,date,author,platform,type,port,verified,vulnerable_app
        exploits.push({
          id: fields[0]?.trim(),
          description: fields[2]?.trim().replace(/"/g, ""),
          date: fields[3]?.trim(),
          author: fields[4]?.trim(),
          url: `https://www.exploit-db.com/exploits/${fields[0]?.trim()}`,
        });
      }
    }

    return exploits.length > 0 ? exploits : null;
  } catch (error) {
    console.error("Error fetching data from Exploit-DB:", error.message);
    return null;
  }
}

// Test AlienVault OTX
async function testAlienVaultOtx(cveId) {
  if (
    process.env.ALIENVAULT_OTX_ENABLED !== "true" ||
    !process.env.ALIENVAULT_OTX_API_KEY
  ) {
    console.log("AlienVault OTX is disabled or missing API key in .env file");
    return null;
  }

  console.log(`Searching AlienVault OTX for information related to ${cveId}...`);

  const headers = {
    "X-OTX-API-KEY": process.env.ALIENVAULT_OTX_API_KEY,
  };

  // Query AlienVault OTX for pulses related to the CVE
  const response = await axios.get(
    `https://otx.alienvault.com/api/v1/indicators/cve/${cveId}/general`,
    { headers }
  );

  if (response.data && response.data.pulse_info && response.data.pulse_info.pulses) {
    // Return summary of the pulses
    const pulses = response.data.pulse_info.pulses;
    return {
      pulse_count: pulses.length,
      samples: pulses.slice(0, 2),
    };
  }

  return null;
}

// Test SANS Internet Storm Center
async function testSansIsc(cveId) {
  if (process.env.SANS_ISC_ENABLED !== "true") {
    console.log("SANS ISC is disabled in .env file");
    return null;
  }

  console.log(`Checking SANS Internet Storm Center for information on ${cveId}...`);

  try {
    // Fetch the SANS ISC RSS feed
    const response = await axios.get("https://isc.sans.edu/rssfeed_full.xml");

    // We need to parse the XML
    // In a real implementation we would use xml2js, but for this test
    // we'll just check if the response contains the CVE ID
    if (response.data.includes(cveId)) {
      return `Found references to ${cveId} in SANS ISC feed`;
    }

    // Check for any recent entries as a sample
    const items = response.data.match(/<item>([\s\S]*?)<\/item>/g);
    if (items && items.length > 0) {
      // Extract the titles of the first 3 items
      const titles = items.slice(0, 3).map((item) => {
        const match = item.match(/<title>(.*?)<\/title>/);
        return match ? match[1] : "Unknown title";
      });

      return {
        message: `${cveId} not found in SANS ISC feed, but here are recent entries:`,
        recentEntries: titles,
      };
    }

    return null;
  } catch (error) {
    console.error("Error fetching data from SANS ISC:", error.message);
    return null;
  }
}

// Test CERT Coordination Center (CERT/CC)
async function testCertCcData(cveId) {
  if (process.env.CERT_CC_ENABLED !== "true") {
    console.log("CERT/CC is disabled in .env file");
    return null;
  }

  console.log(`Checking CERT/CC for information on ${cveId}...`);

  try {
    const response = await axios.get("https://www.kb.cert.org/vuls/atomfeed/", {
      timeout: 10000,
    });

    // Check if the CVE ID is mentioned in the feed
    if (response.data.includes(cveId)) {
      return {
        message: `Found reference to ${cveId} in CERT/CC feed`,
        url: "https://www.kb.cert.org/vuls/atomfeed/",
      };
    }

    // Return info about recent entries in the feed
    return {
      message: `${cveId} not found in CERT/CC feed, but feed is available`,
      url: "https://www.kb.cert.org/vuls/atomfeed/",
    };
  } catch (error) {
    console.error("Error fetching from CERT/CC:", error.message);
    return null;
  }
}

// Test Zero Day Initiative (ZDI)
async function testZdiData(cveId) {
  if (process.env.ZDI_ENABLED !== "true") {
    console.log("Zero Day Initiative is disabled in .env file");
    return null;
  }

  console.log(`Checking Zero Day Initiative for information on ${cveId}...`);

  // Get the current year
  const currentYear = new Date().getFullYear();
  let allEntries = [];

  // Try current year feed
  try {
    const response = await axios.get(
      `https://www.zerodayinitiative.com/rss/published/${currentYear}`,
      { timeout: 10000 }
    );

    // Parse the XML using a simple approach for testing
    const content = response.data;
    const regex = new RegExp(`${cveId}`, "i");

    // Check if CVE is mentioned anywhere in the feed
    if (regex.test(content)) {
      return {
        message: `Found reference to ${cveId} in ZDI feed for year ${currentYear}`,
        feedYear: currentYear,
        url: `https://www.zerodayinitiative.com/rss/published/${currentYear}`,
      };
    }

    // Try previous year as well
    const prevYearResponse = await axios.get(
      `https://www.zerodayinitiative.com/rss/published/${currentYear - 1}`,
      { timeout: 10000 }
    );

    if (regex.test(prevYearResponse.data)) {
      return {
        message: `Found reference to ${cveId} in ZDI feed for year ${currentYear - 1}`,
        feedYear: currentYear - 1,
        url: `https://www.zerodayinitiative.com/rss/published/${currentYear - 1}`,
      };
    }

    // Try base feed as last resort
    const baseResponse = await axios.get(
      "https://www.zerodayinitiative.com/rss/published/",
      { timeout: 10000 }
    );

    if (regex.test(baseResponse.data)) {
      return {
        message: `Found reference to ${cveId} in ZDI base feed`,
        url: "https://www.zerodayinitiative.com/rss/published/",
      };
    }

    return {
      message: `No information found in ZDI feeds for ${cveId}`,
      checkedYears: [currentYear, currentYear - 1],
      checkedBase: true,
    };
  } catch (error) {
    console.error("Error fetching from ZDI:", error.message);
    return null;
  }
}

// Test VulDB (Vulnerability Database)
async function testVulDbData(cveId) {
  if (process.env.VULDB_ENABLED !== "true") {
    console.log("VulDB is disabled in .env file");
    return null;
  }

  console.log(`Checking VulDB for information on ${cveId}...`);

  try {
    // Fetch the VulDB RSS feed for recent vulnerabilities
    const response = await axios.get("https://vuldb.com/?rss.recent", {
      timeout: 10000,
    });

    // Check if the CVE ID is mentioned in the feed
    if (response.data.includes(cveId)) {
      return {
        message: `Found reference to ${cveId} in VulDB feed`,
        url: "https://vuldb.com/?rss.recent",
      };
    }

    // Extract some sample entries to show feed is working
    const itemMatch = response.data.match(/<item>([\s\S]*?)<\/item>/g);
    if (itemMatch && itemMatch.length > 0) {
      // Extract titles of the first 3 items
      const titles = itemMatch.slice(0, 3).map((item) => {
        const titleMatch = item.match(/<title>(.*?)<\/title>/);
        return titleMatch ? titleMatch[1] : "Unknown title";
      });

      return {
        message: `${cveId} not found in VulDB feed, but feed is available`,
        sampleEntries: titles,
        url: "https://vuldb.com/?rss.recent",
      };
    }

    return {
      message: `No information found in VulDB feed for ${cveId}`,
      url: "https://vuldb.com/?rss.recent",
    };
  } catch (error) {
    console.error("Error fetching from VulDB:", error.message);
    return null;
  }
}

// Main function to run all tests
async function main() {
  console.log(`Running tests for ${cveId}...\n`);

  await runTest("NVD API", testNvdApi);
  await runTest("MITRE API", testMitreApi);
  await runTest("CISA KEV", testCisaKev);
  await runTest("ZDI (Zero Day Initiative)", testZdiData);
  await runTest("Exploit-DB", testExploitDb);
  await runTest("SANS ISC", testSansIsc);
  await runTest("CERT/CC", testCertCcData);
  await runTest("VulDB", testVulDbData);
  await runTest("AlienVault OTX", testAlienVaultOtx);

  console.log("\nAll tests completed!");
}

main().catch((error) => {
  console.error("Unhandled error:", error);
  process.exit(1);
});
