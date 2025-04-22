#!/usr/bin/env node

/**
 * Vulnerability Blog Post Generator
 *
 * This script generates blog posts about security vulnerabilities using the
 * prompt defined in Prompts/threat-blog-post.prompt
 *
 * Usage:
 *   node generate-vuln-post.js --cve CVE-2023-XXXXX
 *   node generate-vuln-post.js --latest
 *   node generate-vuln-post.js --weekly
 *
 * Options:
 *   --cve CVE-ID     Generate a post for a specific CVE
 *   --latest         Generate a post for the latest critical vulnerability
 *   --weekly         Generate a weekly roll-up of critical vulnerabilities
 */

const fs = require("fs");
const path = require("path");
const axios = require("axios");
const { program } = require("commander");
const dotenv = require("dotenv");
const { format } = require("date-fns");
const { parseString } = require("xml2js");

// Track token usage for logging and cost monitoring
let tokenUsage = {
  input: 0,
  output: 0,
  provider: null,
};

// Load environment variables - prioritize tools/vuln-blog/.env if it exists
const envPaths = [
  path.join(__dirname, "../../tools/vuln-blog/.env"), // Primary location - tools/vuln-blog/.env
  path.join(__dirname, ".env"), // Local copy in scripts/vulnerabilities/
  process.env.ENV_FILE, // User-specified path via ENV_FILE
  ".env.test", // Last resort fallback
].filter(Boolean); // Remove undefined entries

let envLoaded = false;
for (const envPath of envPaths) {
  if (fs.existsSync(envPath)) {
    console.log(`Loading environment variables from: ${envPath}`);
    dotenv.config({ path: envPath });
    envLoaded = true;
    break;
  }
}

if (!envLoaded) {
  console.warn(
    "Warning: No .env file found in any of the searched locations. Using environment variables if available."
  );
  dotenv.config(); // Try default location as last resort
}

// Check for required API keys based on provider
const LLM_PROVIDER = process.env.LLM_PROVIDER || "openai";
if (LLM_PROVIDER === "openai" && !process.env.OPENAI_API_KEY) {
  console.error(
    "Error: OPENAI_API_KEY environment variable is required when using OpenAI provider"
  );
  process.exit(1);
} else if (LLM_PROVIDER === "gemini" && !process.env.GOOGLE_API_KEY) {
  console.error(
    "Error: GOOGLE_API_KEY environment variable is required when using Gemini provider"
  );
  process.exit(1);
} else if (LLM_PROVIDER === "claude" && !process.env.CLAUDE_API_KEY) {
  console.error(
    "Error: CLAUDE_API_KEY environment variable is required when using Claude provider"
  );
  process.exit(1);
}

program
  .option("--cve <cve-id>", "Generate a post for a specific CVE")
  .option("--latest", "Generate a post for the latest critical vulnerability")
  .option("--weekly", "Generate a weekly roll-up of critical vulnerabilities")
  .option("--provider <provider>", "LLM provider to use (openai, gemini, claude)")
  .option("--no-rag", "Disable Retrieval-Augmented Generation")
  .parse(process.argv);

const options = program.opts();

// Function to read the prompt template
function readPromptTemplate() {
  // Always use RAG-enabled prompt template unless explicitly disabled
  const useRag = options.rag !== false;
  const promptName = useRag ? "threat-blog-post-rag.prompt" : "threat-blog-post.prompt";

  // Define all possible template locations in order of preference
  const templatePaths = [
    // 1. Check tools/vuln-blog/prompts first (most likely location)
    path.join(__dirname, "../../tools/vuln-blog/prompts", promptName),
    // 2. Check main Prompts directory as backup
    path.join(__dirname, "../../Prompts", promptName),
    // 3. Check current directory in case templates are copied there
    path.join(__dirname, promptName),
  ];

  // Try each location until we find a template
  for (const templatePath of templatePaths) {
    if (fs.existsSync(templatePath)) {
      console.log(
        `Using ${useRag ? "RAG-enabled" : "standard"} template from: ${templatePath}`
      );
      return fs.readFileSync(templatePath, "utf8");
    }
  }

  // If RAG template not found in any location, try standard template
  if (useRag) {
    console.log(
      "RAG-enabled template not found in any location, trying standard template"
    );
    options.rag = false;
    return readPromptTemplate();
  }

  // If we get here, we couldn't find any template - create a basic emergency template
  // This ensures we always have a template rather than failing completely
  console.warn(
    "WARNING: No prompt templates found! Using emergency built-in template."
  );
  return `# Vulnerability Analysis: {CVE_ID}

![Placeholder: Security vulnerability in {AFFECTED_SOFTWARE}](blog/security-blog.jpg)

## Executive Summary

{VULN_SUMMARY}

## Vulnerability Snapshot

| Attribute | Value |
|-----------|-------|
| CVE ID | [{CVE_ID}](https://nvd.nist.gov/vuln/detail/{CVE_ID}) |
| Common Name | {VULN_NAME} |
| Affected Software | {AFFECTED_SOFTWARE} |
| Affected Versions | {AFFECTED_VERSIONS} |
| CVSS v3.x Base Score | {CVSS_SCORE} ([CVSS Calculator](https://www.first.org/cvss/calculator/3.1#{CVSS_VECTOR})) |
| CVSS Vector String | [{CVSS_VECTOR}](https://www.first.org/cvss/calculator/3.1#{CVSS_VECTOR}) |
| Severity Rating | {SEVERITY_RATING} |
| Key CWE ID | {CWE_ID} ([MITRE CWE](https://cwe.mitre.org/data/definitions/{CWE_ID_NUMBER}.html)) |
| CISA KEV Status | [{IS_KEV}](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) |
| Exploitation Observed | {EXPLOIT_STATUS} |
| Associated Threat Actors | {THREAT_ACTORS_LINK} |
| Cloud Provider Impact | {AWS_IMPACT} |
| Patch Availability | {MITIGATION_GUIDANCE} |

## Technical Details

{TECHNICAL_DETAILS}

## Mitigation and Remediation

{MITIGATION_GUIDANCE}

## References

### Official Advisories
- [CVE Record for {CVE_ID}](https://cve.org/CVERecord?id={CVE_ID}) - Official CVE Record with complete details
- [NVD Entry for {CVE_ID}](https://nvd.nist.gov/vuln/detail/{CVE_ID}) - National Vulnerability Database entry
- [MITRE CVE Entry](https://cve.mitre.org/cgi-bin/cvename.cgi?name={CVE_ID}) - Legacy MITRE CVE page

{REFERENCE_URLS}
`;
}

// Function to get vulnerability data from CVE.org first, then NVD, then MITRE as fallbacks
async function getVulnerabilityData(cveId) {
  try {
    // First try to get data from CVE.org (primary source)
    try {
      console.log(
        `Attempting to fetch data from CVE.org for ${cveId} (primary source)`
      );
      // Set up headers
      const cveOrgHeaders = {
        "User-Agent":
          process.env.MITRE_USER_AGENT ||
          "William Zujkowski Blog Vulnerability Analyzer",
      };

      // CVE.org API endpoint
      const cveOrgResponse = await axios.get(
        `https://cveawg.mitre.org/api/cve/${cveId}`,
        { headers: cveOrgHeaders }
      );

      if (cveOrgResponse.data && cveOrgResponse.data.cveMetadata) {
        console.log(`Successfully fetched CVE.org data for ${cveId}`);
        // Process CVE.org data format and return
        // Note: This is simplified and would need to be expanded to fully parse CVE.org API format
        const cveOrgData = cveOrgResponse.data;
        return {
          id: cveOrgData.cveMetadata.cveId,
          descriptions: cveOrgData.containers?.cna?.descriptions || [],
          metrics: cveOrgData.containers?.cna?.metrics || {},
          references: cveOrgData.containers?.cna?.references || [],
          source: "CVE.org",
        };
      }
    } catch (cveOrgError) {
      console.log(
        `Error or no data from CVE.org: ${cveOrgError.message}, trying NVD...`
      );
    }

    // If CVE.org fails, fall back to NVD
    console.log(`Attempting to fetch data from NVD for ${cveId} (secondary source)`);
    const headers = {
      "User-Agent": "William Zujkowski Blog Vulnerability Analyzer",
    };

    // Add NVD API key if available
    if (process.env.NVD_API_KEY) {
      console.log("Using NVD API key for higher rate limits");
      headers["apiKey"] = process.env.NVD_API_KEY;
    }

    try {
      const response = await axios.get(
        `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${cveId}`,
        { headers }
      );

      if (
        response.data &&
        response.data.vulnerabilities &&
        response.data.vulnerabilities.length > 0
      ) {
        console.log(`Successfully fetched NVD data for ${cveId}`);
        return response.data.vulnerabilities[0].cve;
      } else {
        console.log(`No data found in NVD for ${cveId}, trying MITRE...`);
      }
    } catch (nvdError) {
      console.log(`Error fetching from NVD: ${nvdError.message}, trying MITRE...`);
    }

    // If we reach this point, try getting data from MITRE instead
    const mitreData = await getMitreCveData(cveId);
    if (mitreData) {
      console.log(`Successfully fetched MITRE data for ${cveId}`);

      // Extract the description from MITRE data
      const description = mitreData.description || "";

      // Build metrics based on primary metric if available
      let metrics = {};
      if (mitreData.primaryMetric) {
        const metricType = mitreData.primaryMetric.type;

        if (metricType === "CVSS v3.1") {
          metrics = {
            cvssMetricV31: [
              {
                cvssData: {
                  baseScore: mitreData.primaryMetric.baseScore,
                  baseSeverity: mitreData.primaryMetric.baseSeverity,
                  vectorString: mitreData.primaryMetric.vectorString,
                  attackVector: mitreData.primaryMetric.attackVector,
                  attackComplexity: mitreData.primaryMetric.attackComplexity,
                  privilegesRequired: mitreData.primaryMetric.privilegesRequired,
                  userInteraction: mitreData.primaryMetric.userInteraction,
                  scope: mitreData.primaryMetric.scope,
                  confidentialityImpact: mitreData.primaryMetric.confidentialityImpact,
                  integrityImpact: mitreData.primaryMetric.integrityImpact,
                  availabilityImpact: mitreData.primaryMetric.availabilityImpact,
                  exploitabilityScore: mitreData.primaryMetric.exploitabilityScore,
                  impactScore: mitreData.primaryMetric.impactScore,
                },
              },
            ],
          };
        } else if (metricType === "CVSS v3.0") {
          metrics = {
            cvssMetricV30: [
              {
                cvssData: {
                  baseScore: mitreData.primaryMetric.baseScore,
                  baseSeverity: mitreData.primaryMetric.baseSeverity,
                  vectorString: mitreData.primaryMetric.vectorString,
                  attackVector: mitreData.primaryMetric.attackVector,
                  attackComplexity: mitreData.primaryMetric.attackComplexity,
                  privilegesRequired: mitreData.primaryMetric.privilegesRequired,
                  userInteraction: mitreData.primaryMetric.userInteraction,
                  scope: mitreData.primaryMetric.scope,
                  confidentialityImpact: mitreData.primaryMetric.confidentialityImpact,
                  integrityImpact: mitreData.primaryMetric.integrityImpact,
                  availabilityImpact: mitreData.primaryMetric.availabilityImpact,
                  exploitabilityScore: mitreData.primaryMetric.exploitabilityScore,
                  impactScore: mitreData.primaryMetric.impactScore,
                },
              },
            ],
          };
        } else if (metricType === "CVSS v2.0") {
          metrics = {
            cvssMetricV2: [
              {
                cvssData: {
                  baseScore: mitreData.primaryMetric.baseScore,
                  vectorString: mitreData.primaryMetric.vectorString,
                  exploitabilityScore: mitreData.primaryMetric.exploitabilityScore,
                  impactScore: mitreData.primaryMetric.impactScore,
                },
                baseSeverity: mitreData.primaryMetric.baseSeverity,
              },
            ],
          };
        }
      }

      // Build weaknesses from problem types with CWE IDs
      const weaknesses = [];
      if (mitreData.problemTypes && mitreData.problemTypes.length > 0) {
        // Group problem types by CWE ID to avoid duplicates
        const cweDescriptions = new Map();

        mitreData.problemTypes.forEach((pt) => {
          const cweId = pt.cweId || "UNKNOWN";
          if (!cweDescriptions.has(cweId)) {
            cweDescriptions.set(cweId, []);
          }

          if (pt.description) {
            cweDescriptions.get(cweId).push({
              lang: pt.lang || "en",
              value: pt.description,
            });
          }
        });

        // Convert the map to the NVD format
        cweDescriptions.forEach((descriptions, cweId) => {
          if (descriptions.length > 0) {
            weaknesses.push({
              source: "MITRE",
              type: cweId !== "UNKNOWN" ? "Primary" : "Secondary",
              description: descriptions,
            });
          }
        });
      }

      // Build configurations from product data with better version information
      const configurations = [];
      if (mitreData.vendorData && mitreData.vendorData.products.length > 0) {
        const cpeMatches = [];

        mitreData.vendorData.products.forEach((product) => {
          const vendor = product.vendor || mitreData.vendorData.vendor || "unknown";

          if (product.versions && product.versions.length > 0) {
            product.versions.forEach((ver) => {
              // Build a detailed CPE string with version information
              let criteria = null;
              let criteriaSpecification = null;

              if (ver.rangeDescription) {
                // Handle version ranges in a more standardized way
                if (ver.version) {
                  // Specific version
                  criteria = `cpe:2.3:a:${vendor}:${product.name}:${ver.version}:*:*:*:*:*:*:*`;
                  criteriaSpecification = `${product.name} ${ver.version}`;
                } else if (ver.lessThan) {
                  // Version less than
                  criteria = `cpe:2.3:a:${vendor}:${product.name}:*:*:*:*:*:*:*:*`;
                  criteriaSpecification = `${product.name} < ${ver.lessThan}`;
                } else {
                  // Complex version range - use the description
                  criteria = `cpe:2.3:a:${vendor}:${product.name}:*:*:*:*:*:*:*:*`;
                  criteriaSpecification = `${product.name} ${ver.rangeDescription}`;
                }
              } else if (ver.version) {
                // Just use the version directly if no range description
                criteria = `cpe:2.3:a:${vendor}:${product.name}:${ver.version}:*:*:*:*:*:*:*`;
                criteriaSpecification = `${product.name} ${ver.version}`;
              } else {
                // Generic product entry with no specific version
                criteria = `cpe:2.3:a:${vendor}:${product.name}:*:*:*:*:*:*:*:*`;
                criteriaSpecification = product.name;
              }

              if (criteria) {
                cpeMatches.push({
                  criteria: criteria,
                  criteriaSpecificaton: criteriaSpecification,
                  vulnerable: ver.status === "affected" || ver.status === "unknown",
                });
              }
            });
          } else {
            // Add product without version info
            const criteria = `cpe:2.3:a:${vendor}:${product.name}:*:*:*:*:*:*:*:*`;
            cpeMatches.push({
              criteria: criteria,
              criteriaSpecificaton: product.name,
              vulnerable: true,
            });
          }

          // Add platform information if available
          if (product.platforms && product.platforms.length > 0) {
            product.platforms.forEach((platform) => {
              const criteria = `cpe:2.3:o:${platform}:*:*:*:*:*:*:*:*`;
              cpeMatches.push({
                criteria: criteria,
                criteriaSpecificaton: `${product.name} on ${platform}`,
                vulnerable: true,
              });
            });
          }
        });

        if (cpeMatches.length > 0) {
          configurations.push({
            nodes: [{ cpeMatch: cpeMatches }],
          });
        }
      }

      // Build a NVD-like structure with the processed MITRE data
      return {
        id: mitreData.cveId,
        descriptions: [
          {
            lang: "en",
            value: description,
          },
        ],
        vulnStatus: mitreData.state || "Modified",
        references:
          mitreData.references.map((ref) => ({
            url: ref.url,
            source: ref.source || "MITRE",
            tags: ref.tags || [],
          })) || [],
        metrics: metrics,
        weaknesses: weaknesses,
        configurations: configurations,
        published: mitreData.datePublished,
        lastModified: mitreData.dateUpdated,
        // Add recommendations if available
        recommendations: mitreData.recommendations
          ? [
              {
                lang: "en",
                value: mitreData.recommendations,
              },
            ]
          : [],
      };
    }

    console.error(`No data found for ${cveId} in either NVD or MITRE`);
    return null;
  } catch (error) {
    console.error("Error fetching vulnerability data:", error.message);
    return null;
  }
}

// Function to check if CVE is in CISA KEV catalog
async function checkCisaKev(cveId) {
  try {
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
      return found ? `Yes - Added ${found.dateAdded}` : "No";
    }
    return "Unknown";
  } catch (error) {
    console.error("Error checking CISA KEV:", error.message);
    return "Unknown";
  }
}

// Function to get data from MITRE CVE API
async function getMitreCveData(cveId) {
  if (process.env.MITRE_API_ENABLED !== "true") {
    return null;
  }

  try {
    console.log(`Fetching data from MITRE API for ${cveId}...`);
    const headers = {
      "User-Agent":
        process.env.MITRE_USER_AGENT || "William Zujkowski Blog Vulnerability Analyzer",
      Accept: "application/json",
    };

    // MITRE API endpoint for specific CVE with timeout
    const response = await axios.get(`https://cveawg.mitre.org/api/cve/${cveId}`, {
      headers,
      timeout: 10000, // 10 second timeout to prevent hanging
    });

    if (response.data && response.data.cveMetadata) {
      const data = response.data;

      // Get primary English description or combine multiple if available
      let description = "";
      const englishDescriptions =
        data.containers?.cna?.descriptions?.filter((d) => d.lang === "en") || [];

      if (englishDescriptions.length > 0) {
        // Use the first description as primary
        description = englishDescriptions[0].value || "";

        // If there are additional descriptions, append them
        if (englishDescriptions.length > 1) {
          const additionalDescriptions = englishDescriptions
            .slice(1)
            .map((d) => d.value)
            .filter(Boolean);
          if (additionalDescriptions.length > 0) {
            description +=
              "\n\nAdditional information:\n" + additionalDescriptions.join("\n\n");
          }
        }
      }

      // Extract problem types (CWE IDs and descriptions)
      const problemTypes = extractProblemTypes(data);

      // Find the primary CWE ID if available
      let primaryCweId = null;
      if (problemTypes.length > 0) {
        // Look for the first problem type with a CWE ID
        const withCweId = problemTypes.find((pt) => pt.cweId);
        if (withCweId) {
          primaryCweId = withCweId.cweId;
        }
      }

      // Get metrics and determine primary CVSS score
      const metrics = extractMetrics(data);
      let primaryMetric = null;

      if (metrics && metrics.length > 0) {
        // Prefer CVSS v3.1, then v3.0, then v2.0
        primaryMetric =
          metrics.find((m) => m.type === "CVSS v3.1") ||
          metrics.find((m) => m.type === "CVSS v3.0") ||
          metrics.find((m) => m.type === "CVSS v2.0");
      }

      // Extract vendor and product information
      const products = extractProducts(data);

      // Determine primary vendor and product names
      let primaryVendor = "Unknown";
      let primaryProduct = "";

      if (data.containers?.cna?.affected && data.containers.cna.affected.length > 0) {
        const firstAffected = data.containers.cna.affected[0];
        primaryVendor = firstAffected.vendor || "Unknown";
        primaryProduct = firstAffected.product || "";
      }

      // Format affected version ranges for display
      let affectedVersions = [];
      if (products && products.length > 0) {
        products.forEach((product) => {
          if (product.versions && product.versions.length > 0) {
            product.versions.forEach((version) => {
              if (version.rangeDescription) {
                affectedVersions.push(`${product.name} ${version.rangeDescription}`);
              } else if (version.version) {
                affectedVersions.push(`${product.name} ${version.version}`);
              }
            });
          } else {
            affectedVersions.push(`${product.name} (version unknown)`);
          }
        });
      }

      // Process and enrich the data
      const processed = {
        raw: data,
        cveId: data.cveMetadata?.cveId,
        state: data.cveMetadata?.state,
        assigner: data.cveMetadata?.assignerShortName,
        datePublished: data.cveMetadata?.datePublished,
        dateUpdated: data.cveMetadata?.dateUpdated,
        description: description,

        // Extracted information with better structure
        affected: data.containers?.cna?.affected || [],
        references: data.containers?.cna?.references || [],
        problemTypes: problemTypes,
        primaryCweId: primaryCweId,
        metrics: metrics,
        primaryMetric: primaryMetric,

        // Vendor and product information
        vendorData: {
          vendor: primaryVendor,
          products: products,
        },

        // Formatted information for display
        formattedAffectedVersions: affectedVersions.join(", "),
        formattedCvssScore: primaryMetric ? primaryMetric.baseScore : "Unknown",
        formattedSeverity: primaryMetric ? primaryMetric.baseSeverity : "Unknown",
        formattedCvssVector: primaryMetric ? primaryMetric.vectorString : "Unknown",

        // Extract any recommendations if available
        recommendations:
          data.containers?.cna?.solutions?.map((s) => s.value).join("\n") || null,
      };

      return processed;
    } else {
      console.log(`No data found in MITRE API for ${cveId}`);
      return null;
    }
  } catch (error) {
    console.error("Error fetching data from MITRE API:", error.message);
    return null;
  }
}

// Helper function to extract problem types (CWEs) from MITRE data
function extractProblemTypes(data) {
  if (!data.containers?.cna?.problemTypes) {
    return [];
  }

  const problemTypes = [];

  data.containers.cna.problemTypes.forEach((pt) => {
    if (pt.descriptions) {
      pt.descriptions.forEach((desc) => {
        if (desc.description) {
          // Add CWE ID pattern detection (e.g., CWE-79, CWE-89)
          const cwePattern = /CWE-\d+/i;
          const match = desc.description.match(cwePattern);
          const cweId = match ? match[0] : null;

          problemTypes.push({
            description: desc.description,
            cweId: cweId,
            lang: desc.lang || "en",
          });
        }
      });
    }
  });

  return problemTypes;
}

// Helper function to extract metrics from MITRE data
function extractMetrics(data) {
  if (!data.containers?.cna?.metrics) {
    return null;
  }

  const metrics = [];

  data.containers.cna.metrics.forEach((metric) => {
    if (metric.cvssV3_1 || metric.cvssV3_0) {
      const cvssData = metric.cvssV3_1 || metric.cvssV3_0;
      metrics.push({
        type: metric.cvssV3_1 ? "CVSS v3.1" : "CVSS v3.0",
        baseScore: cvssData?.baseScore,
        baseSeverity: cvssData?.baseSeverity,
        vectorString: cvssData?.vectorString,
        exploitabilityScore: cvssData?.exploitabilityScore,
        impactScore: cvssData?.impactScore,
        attackVector: cvssData?.attackVector,
        attackComplexity: cvssData?.attackComplexity,
        privilegesRequired: cvssData?.privilegesRequired,
        userInteraction: cvssData?.userInteraction,
        scope: cvssData?.scope,
        confidentialityImpact: cvssData?.confidentialityImpact,
        integrityImpact: cvssData?.integrityImpact,
        availabilityImpact: cvssData?.availabilityImpact,
      });
    } else if (metric.cvssV2_0) {
      // Also capture CVSS v2 data if available
      const cvssData = metric.cvssV2_0;
      metrics.push({
        type: "CVSS v2.0",
        baseScore: cvssData?.baseScore,
        baseSeverity: getSeverityFromV2Score(cvssData?.baseScore),
        vectorString: cvssData?.vectorString,
        exploitabilityScore: cvssData?.exploitabilityScore,
        impactScore: cvssData?.impactScore,
      });
    }
  });

  return metrics.length > 0 ? metrics : null;
}

// Helper function to determine severity rating from CVSS v2 score
function getSeverityFromV2Score(score) {
  if (!score) return "Unknown";
  const numScore = parseFloat(score);

  if (numScore >= 9.0) return "Critical";
  if (numScore >= 7.0) return "High";
  if (numScore >= 4.0) return "Medium";
  if (numScore >= 0.1) return "Low";
  return "None";
}

// Helper function to extract product information with enhanced version handling
function extractProducts(data) {
  if (!data.containers?.cna?.affected) {
    return [];
  }

  const products = [];

  data.containers.cna.affected.forEach((affected) => {
    if (affected.product) {
      const product = {
        name: affected.product,
        vendor: affected.vendor || "Unknown",
        versions: [],
        defaultStatus: affected.defaultStatus || "affected",
      };

      // Extract detailed version information
      if (affected.versions) {
        affected.versions.forEach((version) => {
          // Handle version ranges more comprehensively
          const versionInfo = {
            version: version.version,
            status: version.status || product.defaultStatus,
            lessThan: version.lessThan || null,
            versionType: version.versionType || "unknown",
          };

          // Add version range information if available
          if (version.lessThan) {
            versionInfo.rangeDescription = `< ${version.lessThan}`;
          } else if (version.version) {
            versionInfo.rangeDescription = `= ${version.version}`;
          }

          // Add additional version details if available
          if (version.versionStartIncluding) {
            versionInfo.versionStartIncluding = version.versionStartIncluding;
            versionInfo.rangeDescription = `>= ${version.versionStartIncluding}`;

            if (version.versionEndExcluding) {
              versionInfo.versionEndExcluding = version.versionEndExcluding;
              versionInfo.rangeDescription += ` and < ${version.versionEndExcluding}`;
            } else if (version.versionEndIncluding) {
              versionInfo.versionEndIncluding = version.versionEndIncluding;
              versionInfo.rangeDescription += ` and <= ${version.versionEndIncluding}`;
            }
          } else if (version.versionStartExcluding) {
            versionInfo.versionStartExcluding = version.versionStartExcluding;
            versionInfo.rangeDescription = `> ${version.versionStartExcluding}`;

            if (version.versionEndExcluding) {
              versionInfo.versionEndExcluding = version.versionEndExcluding;
              versionInfo.rangeDescription += ` and < ${version.versionEndExcluding}`;
            } else if (version.versionEndIncluding) {
              versionInfo.versionEndIncluding = version.versionEndIncluding;
              versionInfo.rangeDescription += ` and <= ${version.versionEndIncluding}`;
            }
          }

          product.versions.push(versionInfo);
        });
      }

      // Add platform information if available
      if (affected.platforms && affected.platforms.length > 0) {
        product.platforms = affected.platforms;
      }

      products.push(product);
    }
  });

  return products;
}

// Function to get exploit information from Exploit-DB
async function getExploitDbData(cveId) {
  if (process.env.EXPLOIT_DB_ENABLED !== "true") {
    return null;
  }

  try {
    console.log(`Checking Exploit-DB for exploits related to ${cveId}...`);

    // In case the direct CSV download fails, we'll provide a fallback approach
    try {
      // Exploit-DB provides a CSV file with all exploits
      const response = await axios.get(
        "https://www.exploit-db.com/download/exploitdb.csv",
        { timeout: 5000 } // Add a timeout to prevent long hangs
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

      if (exploits.length > 0) {
        return exploits;
      }
      console.log(`No exploits found in Exploit-DB for ${cveId}`);
    } catch (csvError) {
      console.log(
        `Error fetching Exploit-DB CSV: ${csvError.message}, trying alternative approach...`
      );

      // Fallback approach: try to search by CVE ID on the Exploit-DB website
      try {
        // This is a hacky approach and might break if the site structure changes
        // But it's a good fallback when the CSV download fails
        const searchResponse = await axios.get(
          `https://www.exploit-db.com/search?cve=${cveId.replace("CVE-", "")}`,
          { timeout: 5000 }
        );

        // If we get a successful response, it means there might be exploits
        // But parsing HTML is complex, so we'll just return a generic message
        if (searchResponse.status === 200) {
          return [
            {
              id: "unknown",
              description: `Potential exploits may exist for ${cveId}`,
              date: "unknown",
              author: "unknown",
              url: `https://www.exploit-db.com/search?cve=${cveId.replace("CVE-", "")}`,
            },
          ];
        }
      } catch (searchError) {
        console.log(`Error searching Exploit-DB website: ${searchError.message}`);
      }
    }

    // If we reached here, we couldn't find any exploits
    return null;
  } catch (error) {
    console.error("Error fetching data from Exploit-DB:", error.message);
    return null;
  }
}

// Helper function to parse XML using xml2js (shared by multiple functions)
const parseXml = (xml) => {
  return new Promise((resolve, reject) => {
    parseString(xml, (err, result) => {
      if (err) reject(err);
      else resolve(result);
    });
  });
};

// Function to get data from SANS Internet Storm Center
async function getSansIscData(cveId) {
  if (process.env.SANS_ISC_ENABLED !== "true") {
    return null;
  }

  try {
    console.log(`Checking SANS Internet Storm Center for information on ${cveId}...`);

    // Fetch the SANS ISC RSS feed
    const response = await axios.get("https://isc.sans.edu/rssfeed_full.xml");

    // Parse the XML
    const xmlData = response.data;
    let parsedData = null;

    parsedData = await parseXml(xmlData);

    // Get the items from the feed
    const items = parsedData?.rss?.channel?.[0]?.item || [];

    // Filter for items related to the CVE
    const relevantItems = items.filter((item) => {
      const title = item.title?.[0] || "";
      const description = item.description?.[0] || "";

      // Look for the CVE ID in both title and description
      return title.includes(cveId) || description.includes(cveId);
    });

    if (relevantItems.length === 0) {
      console.log(`No information found in SANS ISC for ${cveId}`);

      // Check for mentions of this vulnerability by its other characteristics
      // This could be expanded with more sophisticated matching
      return null;
    }

    // Format the relevant information
    const sansData = relevantItems.map((item) => {
      return {
        title: item.title?.[0] || "",
        link: item.link?.[0] || "",
        date: item.pubDate?.[0] || "",
        description: item.description?.[0] || "",
        author: item["dc:creator"]?.[0] || "",
      };
    });

    return sansData;
  } catch (error) {
    console.error("Error fetching data from SANS ISC:", error.message);
    return null;
  }
}

// Function to get data from Zero Day Initiative (ZDI)
async function getZdiData(cveId) {
  if (process.env.ZDI_ENABLED !== "true") {
    return null;
  }

  try {
    console.log(`Checking Zero Day Initiative for information on ${cveId}...`);

    // Get the current year to try the latest feed first
    const currentYear = new Date().getFullYear();

    // Try to get data from current year and previous year feeds
    let allZdiEntries = [];

    // Try current year first
    try {
      const currentYearResponse = await axios.get(
        `https://www.zerodayinitiative.com/rss/published/${currentYear}`,
        { timeout: 10000 }
      );

      const currentYearXmlData = currentYearResponse.data;

      const currentYearParsedData = await parseXml(currentYearXmlData);
      const currentYearItems = currentYearParsedData?.rss?.channel?.[0]?.item || [];
      allZdiEntries = [...allZdiEntries, ...currentYearItems];
    } catch (currentYearError) {
      console.log(`Error fetching current year ZDI data: ${currentYearError.message}`);
    }

    // Also try previous year for completeness
    try {
      const prevYearResponse = await axios.get(
        `https://www.zerodayinitiative.com/rss/published/${currentYear - 1}`,
        { timeout: 10000 }
      );

      const prevYearXmlData = prevYearResponse.data;
      const prevYearParsedData = await parseXml(prevYearXmlData);
      const prevYearItems = prevYearParsedData?.rss?.channel?.[0]?.item || [];
      allZdiEntries = [...allZdiEntries, ...prevYearItems];
    } catch (prevYearError) {
      console.log(`Error fetching previous year ZDI data: ${prevYearError.message}`);
    }

    // If we have no entries, try the main feed as a fallback
    if (allZdiEntries.length === 0) {
      try {
        const baseResponse = await axios.get(
          "https://www.zerodayinitiative.com/rss/published/",
          { timeout: 10000 }
        );

        const baseXmlData = baseResponse.data;
        const baseParsedData = await parseXml(baseXmlData);
        const baseItems = baseParsedData?.rss?.channel?.[0]?.item || [];
        allZdiEntries = baseItems;
      } catch (baseError) {
        console.log(`Error fetching base ZDI feed: ${baseError.message}`);
      }
    }

    // Filter for items related to the CVE
    const relevantItems = allZdiEntries.filter((item) => {
      const title = item.title?.[0] || "";
      const description = item.description?.[0] || "";

      // Look for the CVE ID in both title and description
      return title.includes(cveId) || description.includes(cveId);
    });

    if (relevantItems.length === 0) {
      console.log(`No information found in ZDI for ${cveId}`);
      return null;
    }

    // Format the relevant information
    const zdiData = relevantItems.map((item) => {
      // Extract vendor, affected product, and vulnerability type from title if possible
      const title = item.title?.[0] || "";
      const description = item.description?.[0] || "";

      // ZDI titles often follow the pattern: "ZDI-21-xxx: Vendor Product Vulnerability Type"
      let vendor = "Unknown";
      let product = "Unknown";
      let vulnType = "Unknown";

      // Try to extract the ZDI ID
      const zdiIdMatch = title.match(/ZDI-\d+-\d+/);
      const zdiId = zdiIdMatch ? zdiIdMatch[0] : "Unknown";

      // Extract vulnerability details from title
      const titleParts = title.split(": ");
      if (titleParts.length > 1) {
        const vulnDetails = titleParts[1];
        const firstSpace = vulnDetails.indexOf(" ");
        if (firstSpace !== -1) {
          vendor = vulnDetails.substring(0, firstSpace).trim();

          // Try to extract product and vulnerability type
          const remainingText = vulnDetails.substring(firstSpace + 1).trim();
          const lastSpace = remainingText.lastIndexOf(" ");

          if (lastSpace !== -1 && lastSpace > 0) {
            product = remainingText.substring(0, lastSpace).trim();
            vulnType = remainingText.substring(lastSpace + 1).trim();
          } else {
            product = remainingText;
          }
        }
      }

      // Extract CVSS information if available
      let cvssScore = null;
      let severity = null;

      const cvssMatch = description.match(/CVSS Score:\s*(\d+(\.\d+)?)/i);
      if (cvssMatch) {
        cvssScore = cvssMatch[1];

        // Calculate severity based on CVSS score
        const score = parseFloat(cvssScore);
        if (score >= 9.0) severity = "Critical";
        else if (score >= 7.0) severity = "High";
        else if (score >= 4.0) severity = "Medium";
        else if (score >= 0.1) severity = "Low";
        else severity = "None";
      }

      return {
        title: title,
        link: item.link?.[0] || "",
        date: item.pubDate?.[0] || "",
        description: description,
        zdiId: zdiId,
        vendor: vendor,
        product: product,
        vulnType: vulnType,
        cvssScore: cvssScore,
        severity: severity,
      };
    });

    return zdiData;
  } catch (error) {
    console.error("Error fetching data from Zero Day Initiative:", error.message);
    return null;
  }
}

// Function to get data from VulDB (Vulnerability Database)
async function getVulDbData(cveId) {
  if (process.env.VULDB_ENABLED !== "true") {
    return null;
  }

  // Set up retry configuration
  const maxRetries = 3;
  const retryDelay = 2000; // 2 seconds between retries
  let retryCount = 0;

  while (retryCount < maxRetries) {
    try {
      console.log(
        `Checking VulDB for information on ${cveId}... (Attempt ${retryCount + 1}/${maxRetries})`
      );

      // Fetch the VulDB RSS feed for recent vulnerabilities
      const response = await axios.get("https://vuldb.com/?rss.recent", {
        timeout: 15000, // Increased timeout for better reliability
        headers: {
          // Add a user agent to prevent being blocked by some servers
          "User-Agent":
            process.env.VULDB_USER_AGENT ||
            "William Zujkowski Blog Vulnerability Analyzer",
        },
      });

      // Check if response is valid XML
      if (
        !response.data ||
        typeof response.data !== "string" ||
        !response.data.includes("<rss")
      ) {
        throw new Error("Invalid XML response from VulDB");
      }

      const parsedData = await parseXml(response.data);

      // Get items from the feed
      const items = parsedData?.rss?.channel?.[0]?.item || [];

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

      return vuldbData;
    } catch (error) {
      retryCount++;
      console.error(
        `Error fetching data from VulDB (attempt ${retryCount}/${maxRetries}):`,
        error.message
      );

      if (retryCount >= maxRetries) {
        console.error("All VulDB fetch attempts failed");
        return null;
      }

      // Wait before retrying
      console.log(`Waiting ${retryDelay / 1000} seconds before retrying...`);
      await new Promise((resolve) => setTimeout(resolve, retryDelay));
    }
  }

  // This should never be reached due to the return in the final retry attempt
  return null;
}

// Function to get data from CERT Coordination Center (CERT/CC)
async function getCertCcData(cveId) {
  if (process.env.CERT_CC_ENABLED !== "true") {
    return null;
  }

  try {
    console.log(`Checking CERT/CC for information on ${cveId}...`);

    // Fetch the CERT/CC Atom feed
    const response = await axios.get("https://www.kb.cert.org/vuls/atomfeed/", {
      timeout: 10000,
    });

    const parsedData = await parseXml(response.data);

    // Get entries from the feed
    const entries = parsedData?.feed?.entry || [];

    // Filter for entries related to the CVE
    const relevantEntries = entries.filter((entry) => {
      const title = entry.title?.[0]?._ || entry.title?.[0] || "";
      const summary = entry.summary?.[0]?._ || entry.summary?.[0] || "";
      const content = entry.content?.[0]?._ || entry.content?.[0] || "";

      // Look for the CVE ID in title, summary, and content
      return (
        title.includes(cveId) || summary.includes(cveId) || content.includes(cveId)
      );
    });

    if (relevantEntries.length === 0) {
      console.log(`No information found in CERT/CC for ${cveId}`);
      return null;
    }

    // Format the relevant information
    const certData = relevantEntries.map((entry) => {
      // Get entry data
      const title = entry.title?.[0]?._ || entry.title?.[0] || "";
      const summary = entry.summary?.[0]?._ || entry.summary?.[0] || "";
      const link = entry.link?.[0]?.$?.href || "";
      const published = entry.published?.[0] || "";
      const updated = entry.updated?.[0] || "";
      const id = entry.id?.[0] || "";

      // Extract VU# from id if available (typical CERT/CC identifier)
      let vuNumber = null;
      const vuMatch = id.match(/VU#(\d+)/i) || id.match(/vuls\/id\/(\d+)/i);
      if (vuMatch) {
        vuNumber = vuMatch[1];
      }

      // Extract severity indication if available
      let severity = null;
      const highSeverityTerms = ["critical", "high", "severe"];
      const mediumSeverityTerms = ["moderate", "medium", "important"];
      const lowSeverityTerms = ["low", "minor"];

      const titleLower = title.toLowerCase();
      const summaryLower = summary.toLowerCase();

      if (
        highSeverityTerms.some(
          (term) => titleLower.includes(term) || summaryLower.includes(term)
        )
      ) {
        severity = "High";
      } else if (
        mediumSeverityTerms.some(
          (term) => titleLower.includes(term) || summaryLower.includes(term)
        )
      ) {
        severity = "Medium";
      } else if (
        lowSeverityTerms.some(
          (term) => titleLower.includes(term) || summaryLower.includes(term)
        )
      ) {
        severity = "Low";
      }

      // Extract affected products if discernible
      let affectedProducts = [];

      // Common product patterns in CERT/CC alerts
      const productPatterns = [
        /affects\s+([^.]+)/i,
        /vulnerability in\s+([^.]+)/i,
        /([A-Za-z0-9\s]+)\s+vulnerable/i,
        /([A-Za-z0-9\s]+)\s+contains a vulnerability/i,
      ];

      for (const pattern of productPatterns) {
        const match = (title + " " + summary).match(pattern);
        if (match && match[1]) {
          affectedProducts.push(match[1].trim());
          break;
        }
      }

      return {
        title: title,
        summary: summary,
        link: link,
        published: published,
        updated: updated,
        vuNumber: vuNumber ? `VU#${vuNumber}` : null,
        severity: severity,
        affectedProducts: affectedProducts.length > 0 ? affectedProducts : null,
      };
    });

    return certData;
  } catch (error) {
    console.error("Error fetching data from CERT/CC:", error.message);
    return null;
  }
}

// Function to search for threat actor information from AlienVault OTX
async function searchThreatActors(cveId) {
  if (
    process.env.ALIENVAULT_OTX_ENABLED !== "true" ||
    !process.env.ALIENVAULT_OTX_API_KEY
  ) {
    return "No known threat actor associations at this time.";
  }

  try {
    console.log(
      `Searching AlienVault OTX for threat actor information related to ${cveId}...`
    );

    const headers = {
      "X-OTX-API-KEY": process.env.ALIENVAULT_OTX_API_KEY,
    };

    // Query AlienVault OTX for pulses related to the CVE
    const response = await axios.get(
      `https://otx.alienvault.com/api/v1/indicators/cve/${cveId}/general`,
      { headers }
    );

    if (response.data && response.data.pulse_info && response.data.pulse_info.pulses) {
      const pulses = response.data.pulse_info.pulses;

      if (pulses.length === 0) {
        return "No known threat actor associations at this time.";
      }

      // Extract threat actor information from pulses
      const threatActors = new Set();
      const campaigns = new Set();

      pulses.forEach((pulse) => {
        // Extract threat actor tags
        if (pulse.tags) {
          pulse.tags.forEach((tag) => {
            if (
              tag.toLowerCase().includes("actor") ||
              tag.toLowerCase().includes("apt") ||
              tag.toLowerCase().includes("group")
            ) {
              threatActors.add(tag);
            }
            if (tag.toLowerCase().includes("campaign")) {
              campaigns.add(tag);
            }
          });
        }

        // Extract from name if it contains common threat actor naming patterns
        if (pulse.name) {
          const name = pulse.name.toLowerCase();
          if (
            name.includes("apt") ||
            name.includes("group") ||
            name.includes("actor") ||
            name.includes("team")
          ) {
            // Try to extract the threat actor name with a regexp
            const matches = pulse.name.match(
              /(APT\d+|Group\s+\d+|TeamTNT|Lazarus|Turla|Sandworm|Fancy\s+Bear|Cozy\s+Bear|Equation\s+Group|[A-Z][a-z]+\s+Team)/g
            );
            if (matches) {
              matches.forEach((match) => threatActors.add(match));
            }
          }
        }
      });

      // Format the output
      let result = "";

      if (threatActors.size > 0) {
        result += "Threat Actors: " + Array.from(threatActors).join(", ") + "\n\n";
      }

      if (campaigns.size > 0) {
        result += "Associated Campaigns: " + Array.from(campaigns).join(", ") + "\n\n";
      }

      if (result === "") {
        result =
          "Mentioned in threat intelligence reports, but no specific threat actor associations identified.";
      }

      result += `Based on ${pulses.length} intelligence reports from AlienVault OTX.`;

      return result;
    }

    return "No known threat actor associations at this time.";
  } catch (error) {
    console.error("Error searching AlienVault OTX:", error.message);
    return "Unable to retrieve threat actor information at this time.";
  }
}

// Function to assess AWS impact
function assessAwsImpact(vulnData) {
  // This would be more sophisticated in a real implementation
  // For now, we'll make a basic assessment based on the description
  const description = vulnData.descriptions.find((d) => d.lang === "en")?.value || "";

  if (
    description.toLowerCase().includes("aws") ||
    description.toLowerCase().includes("amazon") ||
    description.toLowerCase().includes("cloud")
  ) {
    return "Direct impact on AWS services or infrastructure.";
  }

  if (
    description.toLowerCase().includes("container") ||
    description.toLowerCase().includes("kubernetes") ||
    description.toLowerCase().includes("docker")
  ) {
    return "May affect containerized workloads running on AWS.";
  }

  return "No direct AWS impact identified, but standard cloud security practices apply.";
}

// Function to assess cloud service provider relevance
function assessCloudRelevance(vulnData) {
  const description = vulnData.descriptions.find((d) => d.lang === "en")?.value || "";

  if (
    description.toLowerCase().includes("cloud") ||
    description.toLowerCase().includes("service provider") ||
    description.toLowerCase().includes("multi-tenant")
  ) {
    return "High relevance to cloud service providers.";
  }

  if (
    description.toLowerCase().includes("web service") ||
    description.toLowerCase().includes("api") ||
    description.toLowerCase().includes("remote")
  ) {
    return "Moderate relevance to cloud service providers.";
  }

  return "Limited direct relevance to cloud service providers, but should be monitored as part of general security practices.";
}

// Function to create the input data for the LLM
async function createInputData(cveId) {
  console.log(`Creating input data for ${cveId}...`);

  // Determine which data sources are enabled
  const enabledSources = {
    mitre: process.env.MITRE_API_ENABLED === "true",
    exploitDb: process.env.EXPLOIT_DB_ENABLED === "true",
    sansIsc: process.env.SANS_ISC_ENABLED === "true",
    zdi: process.env.ZDI_ENABLED === "true",
    certCc: process.env.CERT_CC_ENABLED === "true",
    vuldb: process.env.VULDB_ENABLED === "true",
  };

  // Always try to get primary data source (MITRE preferred)
  const mitreCveData = enabledSources.mitre ? await getMitreCveData(cveId) : null;

  // Always get NVD data as fallback
  const vulnData = await getVulnerabilityData(cveId);

  // Get other data sources in parallel but only if enabled
  const [exploitInfo, sansIscData, zdiData, certCcData, vuldbData] = await Promise.all([
    enabledSources.exploitDb ? getExploitDbData(cveId) : null,
    enabledSources.sansIsc ? getSansIscData(cveId) : null,
    enabledSources.zdi ? getZdiData(cveId) : null,
    enabledSources.certCc ? getCertCcData(cveId) : null,
    enabledSources.vuldb ? getVulDbData(cveId) : null,
  ]);

  // We need at least basic vulnerability data to continue
  if (!vulnData && !mitreCveData) {
    console.error(
      `Could not retrieve vulnerability data from either NVD or MITRE for ${cveId}`
    );
    // Create a minimal vulnData object with the CVE ID
    const fallbackVulnData = {
      id: cveId,
      descriptions: [
        {
          lang: "en",
          value: `No detailed information available for ${cveId}. This entry provides a placeholder for the vulnerability.`,
        },
      ],
      vulnStatus: "Unknown",
      references: [],
      metrics: {},
      weaknesses: [],
    };

    console.log(`Created minimal fallback data for ${cveId}`);
    return createMinimalInputData(cveId, fallbackVulnData, mitreCveData, zdiData);
  }

  // Use MITRE as primary source if available, otherwise fall back to NVD
  let primarySourceData = mitreCveData ? "MITRE" : "NVD";
  console.log(`Using ${primarySourceData} as primary data source`);

  const description = vulnData.descriptions.find((d) => d.lang === "en")?.value || "";
  const metrics =
    vulnData.metrics?.cvssMetricV31?.[0] || vulnData.metrics?.cvssMetricV30?.[0] || {};
  const cvssScore = metrics.cvssData?.baseScore || "Unknown";
  const cvssVector = metrics.cvssData?.vectorString || "Unknown";
  const severityRating = metrics.cvssData?.baseSeverity || "Unknown";

  // Get additional information
  const isKev = await checkCisaKev(cveId);
  const threatActors = await searchThreatActors(cveId);
  const awsImpact = assessAwsImpact(vulnData);
  const cloudRelevance = assessCloudRelevance(vulnData);

  // Extract CWE if available
  let cweId = "Unknown";
  if (vulnData.weaknesses && vulnData.weaknesses.length > 0) {
    const weakness = vulnData.weaknesses[0];
    if (weakness.description && weakness.description.length > 0) {
      cweId = weakness.description[0].value || "Unknown";
    }
  }

  // Get references from NVD
  const references = vulnData?.references?.map((ref) => ref.url) || [];

  // Use a Set to automatically deduplicate URLs
  const uniqueReferences = new Set(references);

  // Add references from MITRE if available
  if (mitreCveData && mitreCveData.containers?.cna?.references) {
    mitreCveData.containers.cna.references
      .filter((ref) => ref.url)
      .forEach((ref) => uniqueReferences.add(ref.url));
  }

  // Add references from ZDI if available
  if (zdiData && zdiData.length > 0) {
    zdiData.forEach((entry) => {
      if (entry.link) uniqueReferences.add(entry.link);
    });
  }

  // Add references from CERT/CC if available
  if (certCcData && certCcData.length > 0) {
    certCcData.forEach((entry) => {
      if (entry.link) uniqueReferences.add(entry.link);
    });
  }

  // Add references from VulDB if available
  if (vuldbData && vuldbData.length > 0) {
    vuldbData.forEach((entry) => {
      if (entry.link) uniqueReferences.add(entry.link);
    });
  }

  // Limit to most important references to save tokens
  const MAX_REFERENCES = 10;
  const referenceArray = Array.from(uniqueReferences);
  const limitedReferences =
    referenceArray.length > MAX_REFERENCES
      ? referenceArray.slice(0, MAX_REFERENCES)
      : referenceArray;

  // Enhance technical details with MITRE data if available
  let enhancedTechnicalDetails = description;
  if (mitreCveData && mitreCveData.containers?.cna?.descriptions) {
    const mitreDescription = mitreCveData.containers.cna.descriptions.find(
      (desc) => desc.lang === "en"
    )?.value;

    if (mitreDescription && mitreDescription !== description) {
      enhancedTechnicalDetails = `${description}\n\nAdditional details from MITRE:\n${mitreDescription}`;
    }
  }

  // Prepare POC information
  let pocInfo = "No public POC information available.";
  if (exploitInfo && exploitInfo.length > 0) {
    pocInfo = "Public exploits are available:\n\n";
    exploitInfo.forEach((exploit) => {
      pocInfo += `- ${exploit.description} (${exploit.date})\n  Author: ${exploit.author}\n  Link: ${exploit.url}\n\n`;
    });

    // Set exploit status based on Exploit-DB findings
    exploitStatus = "Public exploits available, see details in the POC section";
  } else if (isKev !== "No") {
    pocInfo =
      "No public exploit code found, but CISA indicates this vulnerability is being actively exploited in the wild.";
    exploitStatus = "Exploitation confirmed by CISA";
  } else {
    exploitStatus = "No confirmed exploitation in the wild";
    if (references.length > 0) {
      pocInfo =
        "No public exploit code found. Potential POCs may be available via the provided references.";
    }
  }

  // Enhance technical details with SANS ISC data if available
  if (sansIscData && sansIscData.length > 0) {
    enhancedTechnicalDetails +=
      "\n\nAdditional analysis from SANS Internet Storm Center:\n";
    sansIscData.forEach((item, index) => {
      enhancedTechnicalDetails += `\n${index + 1}. ${item.title}\n`;
      enhancedTechnicalDetails += `   Published: ${item.date}\n`;
      enhancedTechnicalDetails += `   Author: ${item.author}\n`;
      enhancedTechnicalDetails += `   Link: ${item.link}\n\n`;

      // Add a short excerpt from the description if available
      if (item.description) {
        const excerpt = item.description.replace(/<[^>]*>/g, "").substring(0, 200);
        enhancedTechnicalDetails += `   Excerpt: ${excerpt}...\n`;
      }
    });
  }

  // Enhance technical details with CERT/CC data if available
  if (certCcData && certCcData.length > 0) {
    enhancedTechnicalDetails +=
      "\n\nInformation from CERT Coordination Center (CERT/CC):\n";
    certCcData.forEach((item, index) => {
      enhancedTechnicalDetails += `\n${index + 1}. ${item.title}\n`;
      if (item.vuNumber) {
        enhancedTechnicalDetails += `   Vulnerability Note: ${item.vuNumber}\n`;
      }
      enhancedTechnicalDetails += `   Published: ${item.published}\n`;
      if (item.updated && item.updated !== item.published) {
        enhancedTechnicalDetails += `   Updated: ${item.updated}\n`;
      }
      enhancedTechnicalDetails += `   Link: ${item.link}\n`;
      if (item.severity) {
        enhancedTechnicalDetails += `   Severity: ${item.severity}\n`;
      }
      if (item.affectedProducts && item.affectedProducts.length > 0) {
        enhancedTechnicalDetails += `   Affected Products: ${item.affectedProducts.join(", ")}\n`;
      }
      enhancedTechnicalDetails += `\n`;

      // Add a short excerpt from the summary if available
      if (item.summary) {
        const excerpt = item.summary.replace(/<[^>]*>/g, "").substring(0, 300);
        enhancedTechnicalDetails += `   ${excerpt}...\n`;
      }
    });
  }

  // Enhance technical details with VulDB data if available
  if (vuldbData && vuldbData.length > 0) {
    enhancedTechnicalDetails +=
      "\n\nInformation from VulDB (Vulnerability Database):\n";
    vuldbData.forEach((item, index) => {
      enhancedTechnicalDetails += `\n${index + 1}. ${item.title}\n`;
      if (item.vuldbId) {
        enhancedTechnicalDetails += `   VulDB ID: ${item.vuldbId}\n`;
      }
      enhancedTechnicalDetails += `   Published: ${item.pubDate}\n`;
      enhancedTechnicalDetails += `   Link: ${item.link}\n`;
      if (item.severity) {
        enhancedTechnicalDetails += `   Severity: ${item.severity}\n`;
      }
      if (item.cvssScore) {
        enhancedTechnicalDetails += `   CVSS Score: ${item.cvssScore}\n`;
      }
      if (item.vulnType) {
        enhancedTechnicalDetails += `   Vulnerability Type: ${item.vulnType}\n`;
      }
      if (item.affectedProducts && item.affectedProducts.length > 0) {
        enhancedTechnicalDetails += `   Affected Products: ${item.affectedProducts.join(", ")}\n`;
      }
      enhancedTechnicalDetails += `\n`;

      // Add a cleaned excerpt from the description if available
      if (item.description) {
        // Clean HTML and extract a reasonable portion
        const excerpt = item.description.replace(/<[^>]*>/g, "").substring(0, 300);
        enhancedTechnicalDetails += `   ${excerpt}...\n`;
      }
    });
  }

  // Prepare source attribution
  const dataSources = [];

  // Only include sources that actually provided data
  if (mitreCveData) dataSources.push("MITRE CVE Program");
  if (vulnData) dataSources.push("National Vulnerability Database (NVD)");
  if (isKev !== "Unknown" && isKev !== "No")
    dataSources.push("CISA Known Exploited Vulnerabilities Catalog");
  if (exploitInfo) dataSources.push("Exploit-DB");
  if (sansIscData) dataSources.push("SANS Internet Storm Center");
  if (zdiData && zdiData.length > 0) dataSources.push("Zero Day Initiative (ZDI)");
  if (certCcData && certCcData.length > 0)
    dataSources.push("CERT Coordination Center (CERT/CC)");
  if (vuldbData && vuldbData.length > 0)
    dataSources.push("VulDB (Vulnerability Database)");
  if (
    process.env.ALIENVAULT_OTX_ENABLED === "true" &&
    process.env.ALIENVAULT_OTX_API_KEY &&
    threatActors !== "No known threat actor associations at this time." &&
    threatActors !== "Unable to retrieve threat actor information at this time."
  ) {
    dataSources.push("AlienVault Open Threat Exchange");
  }

  // If we have no sources (unlikely), add a default
  if (dataSources.length === 0) {
    dataSources.push("National Vulnerability Database (NVD)");
  }

  // Build enhanced mitigation guidance
  let mitigationGuidance = "Update to the latest version of the affected software. ";

  // Add CISA required action if in KEV
  if (isKev !== "No" && isKev !== "Unknown") {
    mitigationGuidance +=
      "CISA has added this vulnerability to the Known Exploited Vulnerabilities (KEV) catalog, which requires federal agencies to remediate. ";
  }

  mitigationGuidance +=
    "Specific patches and workarounds may be available in vendor advisories.";

  // Extract CWE_ID_NUMBER by removing "CWE-" prefix
  const cweIdNumber = cweId && cweId.startsWith("CWE-") ? cweId.substring(4) : "";

  // Create THREAT_ACTORS_LINK - link to MITRE ATT&CK if available, otherwise show "No specific information available"
  const threatActorsLink =
    threatActors &&
    threatActors !== "No known threat actor associations at this time." &&
    threatActors !== "Unable to retrieve threat actor information at this time."
      ? `[View potential threat actors on MITRE ATT&CK](https://attack.mitre.org/search/search?query=${encodeURIComponent(cveId)})`
      : "No specific information available";

  return {
    CVE_ID: cveId,
    VULN_NAME:
      vulnData.vulnStatus === "Modified"
        ? vulnData.configurations?.[0]?.nodes?.[0]?.cpeMatch?.[0]?.criteria || cveId
        : cveId,
    CVSS_SCORE: cvssScore,
    CVSS_VECTOR: cvssVector,
    SEVERITY_RATING: severityRating,
    CWE_ID_NUMBER: cweIdNumber,
    THREAT_ACTORS_LINK: threatActorsLink,
    AFFECTED_SOFTWARE:
      vulnData.configurations?.[0]?.nodes?.[0]?.cpeMatch?.[0]?.criteria?.split(
        ":"
      )[3] || "Unknown",
    AFFECTED_VERSIONS:
      vulnData.configurations?.[0]?.nodes?.[0]?.cpeMatch
        ?.map((cpe) => cpe.criteriaSpecificaton || cpe.criteria)
        ?.join(", ") || "Unknown",
    VULN_SUMMARY: description,
    TECHNICAL_DETAILS: enhancedTechnicalDetails,
    POC_INFO: pocInfo,
    IMPACT_ANALYSIS: `This vulnerability has a CVSS score of ${cvssScore} (${severityRating}), indicating significant impact potential.`,
    MITIGATION_GUIDANCE: mitigationGuidance,
    REFERENCE_URLS: limitedReferences.join("\n"),
    IS_KEV: isKev,
    EXPLOIT_STATUS: exploitStatus,
    CWE_ID: cweId,
    THREAT_ACTORS: threatActors,
    AWS_IMPACT: awsImpact,
    CLOUD_RELEVANCE: cloudRelevance,
    DATA_SOURCES: dataSources.join(", "),
  };
}

// Function to create minimal input data when normal sources fail
function createMinimalInputData(cveId, fallbackVulnData, mitreCveData, zdiData) {
  console.log(`Using minimal data creation for ${cveId}`);

  // Extract whatever information we can from MITRE data
  let description =
    fallbackVulnData.descriptions.find((d) => d.lang === "en")?.value || "";
  let references = [];
  let cvssScore = "Unknown";
  let cvssVector = "Unknown";
  let severityRating = "Unknown";
  let cweId = "Unknown";
  let affectedSoftware = "Unknown";
  let affectedVersions = "Unknown";
  let vulnName = cveId;
  let vulnType = "";
  let mitigationGuidance =
    "Follow standard security practices. Update affected software to the latest versions when available. Monitor vendor advisories for patches and workarounds.";

  // Try to extract information from ZDI data first as it often has good titles and summaries
  if (zdiData && zdiData.length > 0) {
    const firstZdiEntry = zdiData[0];

    // Use ZDI title components if available
    if (firstZdiEntry.vendor && firstZdiEntry.vendor !== "Unknown") {
      affectedSoftware = firstZdiEntry.vendor;
      if (firstZdiEntry.product && firstZdiEntry.product !== "Unknown") {
        affectedSoftware += " " + firstZdiEntry.product;
        affectedVersions = firstZdiEntry.product;
      }
    }

    // Use ZDI vulnerability type if available
    if (firstZdiEntry.vulnType && firstZdiEntry.vulnType !== "Unknown") {
      vulnType = firstZdiEntry.vulnType;
    }

    // Use ZDI CVSS score if available
    if (firstZdiEntry.cvssScore) {
      cvssScore = firstZdiEntry.cvssScore;
    }

    // Use ZDI severity if available
    if (firstZdiEntry.severity) {
      severityRating = firstZdiEntry.severity;
    }

    // If ZDI has a good description, use it
    if (firstZdiEntry.description && firstZdiEntry.description.length > 50) {
      // Check if the current description is just a placeholder
      if (description.includes("No detailed information available")) {
        description = firstZdiEntry.description;
      }
    }

    // Add ZDI link to references
    if (firstZdiEntry.link) {
      references.push(firstZdiEntry.link);
    }

    // Create a better vulnerability name using ZDI info
    if (firstZdiEntry.vendor !== "Unknown" && firstZdiEntry.vulnType !== "Unknown") {
      vulnName = `${cveId} (${firstZdiEntry.vendor} ${firstZdiEntry.vulnType})`;
    }
  }

  if (mitreCveData) {
    // Use MITRE data to populate as many fields as possible
    description = mitreCveData.description || description;
    references = mitreCveData.references?.map((ref) => ref.url) || [];

    // Use primary metrics from enhanced MITRE data
    if (mitreCveData.primaryMetric) {
      cvssScore =
        mitreCveData.formattedCvssScore ||
        mitreCveData.primaryMetric.baseScore ||
        "Unknown";
      cvssVector =
        mitreCveData.formattedCvssVector ||
        mitreCveData.primaryMetric.vectorString ||
        "Unknown";
      severityRating =
        mitreCveData.formattedSeverity ||
        mitreCveData.primaryMetric.baseSeverity ||
        "Unknown";
    } else if (mitreCveData.metrics && mitreCveData.metrics.length > 0) {
      // Fallback to first metric if primary not set
      const metric = mitreCveData.metrics[0];
      cvssScore = metric.baseScore || "Unknown";
      cvssVector = metric.vectorString || "Unknown";
      severityRating = metric.baseSeverity || "Unknown";
    }

    // Use primary CWE ID from enhanced MITRE data
    if (mitreCveData.primaryCweId) {
      cweId = mitreCveData.primaryCweId;
    } else if (mitreCveData.problemTypes && mitreCveData.problemTypes.length > 0) {
      // Prioritize problem types with CWE IDs
      const withCweId = mitreCveData.problemTypes.find((pt) => pt.cweId);
      if (withCweId) {
        cweId = withCweId.cweId;
      } else {
        // Fallback to description if no explicit CWE ID
        cweId = mitreCveData.problemTypes[0].description || "Unknown";
      }
    }

    // Use MITRE product information with improved formatting
    if (mitreCveData.vendorData && mitreCveData.vendorData.products.length > 0) {
      // Get primary affected software
      const products = mitreCveData.vendorData.products.map((p) => p.name);
      if (products.length > 0) {
        affectedSoftware = products.join(", ");
      }

      // Use formatted affected versions if available
      if (mitreCveData.formattedAffectedVersions) {
        affectedVersions = mitreCveData.formattedAffectedVersions;
      } else {
        // Fallback to building version information
        const allVersions = [];
        mitreCveData.vendorData.products.forEach((p) => {
          if (p.versions && p.versions.length > 0) {
            p.versions.forEach((v) => {
              if (v.rangeDescription) {
                allVersions.push(`${p.name} ${v.rangeDescription}`);
              } else if (v.version) {
                allVersions.push(`${p.name} ${v.version}`);
              }
            });
          } else {
            allVersions.push(`${p.name} (version unknown)`);
          }
        });

        if (allVersions.length > 0) {
          affectedVersions = allVersions.join(", ");
        }
      }

      // Create a more descriptive vulnerability name
      if (products.length > 0) {
        let vendorName = mitreCveData.vendorData.vendor;
        if (vendorName && vendorName !== "Unknown") {
          vulnName = `${cveId} (${vendorName} ${products[0]})`;
        } else {
          vulnName = `${cveId} (${products[0]})`;
        }
      }
    }

    // Use recommendations if available
    if (mitreCveData.recommendations) {
      mitigationGuidance = mitreCveData.recommendations;
    }
  }

  // Try to get KEV status even with minimal data
  const isKev = "Unknown (CISA KEV status could not be determined)";

  // Create a richer technical description if metrics are available
  let technicalDetails = description;
  if (cvssScore !== "Unknown" && cvssVector !== "Unknown") {
    technicalDetails += `\n\nThis vulnerability has a CVSS score of ${cvssScore} (${severityRating}).`;

    if (cvssVector !== "Unknown") {
      technicalDetails += ` The attack vector is represented by ${cvssVector}.`;
    }

    if (cweId !== "Unknown") {
      technicalDetails += `\n\nThis vulnerability is classified as ${cweId}, which typically involves issues with `;

      // Add some context based on common CWE IDs
      if (cweId.includes("CWE-79")) {
        technicalDetails +=
          "cross-site scripting (XSS), allowing attackers to inject malicious scripts into web pages viewed by other users.";
      } else if (cweId.includes("CWE-89")) {
        technicalDetails +=
          "SQL injection, allowing attackers to interfere with database queries and potentially access, modify, or delete data.";
      } else if (cweId.includes("CWE-20")) {
        technicalDetails +=
          "improper input validation, potentially allowing attackers to supply crafted input that could manipulate the application in unintended ways.";
      } else if (cweId.includes("CWE-200")) {
        technicalDetails +=
          "information exposure or disclosure, potentially revealing sensitive data to unauthorized parties.";
      } else if (cweId.includes("CWE-22")) {
        technicalDetails +=
          "path traversal, potentially allowing attackers to access files and directories outside of intended boundaries.";
      } else if (cweId.includes("CWE-78")) {
        technicalDetails +=
          "OS command injection, potentially allowing attackers to execute arbitrary commands on the host operating system.";
      } else if (cweId.includes("CWE-352")) {
        technicalDetails +=
          "cross-site request forgery (CSRF), potentially allowing attackers to trick users into performing unintended actions.";
      } else if (cweId.includes("CWE-287")) {
        technicalDetails +=
          "improper authentication, potentially allowing attackers to bypass authentication mechanisms.";
      } else if (cweId.includes("CWE-502")) {
        technicalDetails +=
          "deserialization of untrusted data, potentially allowing attackers to execute arbitrary code.";
      } else {
        technicalDetails += "security weaknesses that could be exploited by attackers.";
      }
    }
  }

  // Create impact assessment based on severity and CWE
  let impactAnalysis =
    "Impact analysis could not be determined due to limited information.";
  if (severityRating !== "Unknown") {
    impactAnalysis = `This vulnerability has a ${severityRating.toLowerCase()} severity rating`;

    if (cvssScore !== "Unknown") {
      impactAnalysis += ` with a CVSS score of ${cvssScore}`;
    }

    impactAnalysis += `. `;

    // Add impact details based on severity
    if (severityRating.toUpperCase() === "CRITICAL") {
      impactAnalysis +=
        "Critical vulnerabilities typically represent severe security issues that require immediate attention. Exploitation could lead to complete system compromise, unauthorized access to sensitive data, or service disruption.";
    } else if (severityRating.toUpperCase() === "HIGH") {
      impactAnalysis +=
        "High severity vulnerabilities represent significant security issues that should be prioritized for remediation. Exploitation could lead to significant data loss, system compromise, or service disruption.";
    } else if (severityRating.toUpperCase() === "MEDIUM") {
      impactAnalysis +=
        "Medium severity vulnerabilities represent moderate security issues that should be addressed in a timely manner. Exploitation might be more difficult or limited in impact compared to higher severity issues.";
    } else if (severityRating.toUpperCase() === "LOW") {
      impactAnalysis +=
        "Low severity vulnerabilities represent minor security issues with limited potential impact. While less urgent, they should still be addressed as part of routine security maintenance.";
    }
  }

  // Extract CWE_ID_NUMBER by removing "CWE-" prefix
  const cweIdNumber = cweId && cweId.startsWith("CWE-") ? cweId.substring(4) : "";

  // Set more comprehensive default values with enhanced MITRE data
  return {
    CVE_ID: cveId,
    VULN_NAME: vulnName,
    CVSS_SCORE: cvssScore,
    CVSS_VECTOR: cvssVector,
    SEVERITY_RATING: severityRating,
    CWE_ID_NUMBER: cweIdNumber,
    THREAT_ACTORS_LINK: "No specific information available",
    EPSS_SCORE: "Unknown",
    EPSS_PERCENTILE: "Unknown",
    AFFECTED_SOFTWARE: affectedSoftware,
    AFFECTED_VERSIONS: affectedVersions,
    VULN_SUMMARY: description,
    TECHNICAL_DETAILS: technicalDetails,
    POC_INFO: "No public POC information available.",
    IMPACT_ANALYSIS: impactAnalysis,
    MITIGATION_GUIDANCE: mitigationGuidance,
    REFERENCE_URLS:
      references.length > 0
        ? references.length > 10
          ? references.slice(0, 10).join("\n")
          : references.join("\n")
        : "No references available.",
    IS_KEV: isKev,
    EXPLOIT_STATUS: "Unknown",
    CWE_ID: cweId,
    THREAT_ACTORS: "No known threat actor associations at this time.",
    AWS_IMPACT:
      "Impact on AWS services could not be determined due to limited information.",
    CLOUD_RELEVANCE:
      "Cloud service provider relevance could not be determined due to limited information.",
    DATA_SOURCES: mitreCveData ? "MITRE CVE Program" : "Limited sources available",
  };
}

// Import the LLM provider utilities
const { generateContent } = require("./llm-providers");

/**
 * Retrieval-Augmented Generation (RAG) functionality
 * Enhances input data with relevant context from the vulnerability index
 */
async function enhanceWithRAG(inputData) {
  // Skip if RAG is disabled
  if (options.rag === false) {
    console.log("RAG is disabled, skipping retrieval enhancement");
    return inputData;
  }

  const indexPath = path.join(__dirname, "data/index.json");
  if (!fs.existsSync(indexPath)) {
    console.log("Vulnerability index not found, skipping RAG enhancement");
    return inputData;
  }

  try {
    // Load the vulnerability index
    const indexData = fs.readFileSync(indexPath, "utf8");
    const index = JSON.parse(indexData);

    console.log(
      `Loaded index with ${index.vulnerabilities.length} entries from ${index.metadata.timestamp}`
    );

    // Find similar vulnerabilities based on CWE, affected products, or description
    const cveId = inputData.CVE_ID;
    const relevantVulnerabilities = [];

    // Parse CWE from inputData
    let targetCwe = null;
    if (inputData.CWE_ID && inputData.CWE_ID !== "Unknown") {
      const cweMatch = inputData.CWE_ID.match(/CWE-\d+/);
      if (cweMatch) {
        targetCwe = cweMatch[0];
      }
    }

    // Find by exact CVE match first
    const exactMatch = index.vulnerabilities.find((v) => v.id === cveId);
    if (exactMatch) {
      console.log(`Found exact match for ${cveId} in the index`);
      relevantVulnerabilities.push(exactMatch);
    }

    // Then find by CWE (most relevant for similar vulnerabilities)
    if (targetCwe) {
      console.log(`Looking for vulnerabilities with CWE ${targetCwe}`);
      const cweSimilar = index.vulnerabilities
        .filter((v) => v.id !== cveId && v.cweIds && v.cweIds.includes(targetCwe))
        .sort((a, b) => b.cvssScore - a.cvssScore) // Sort by CVSS score descending
        .slice(0, 3); // Take top 3

      if (cweSimilar.length > 0) {
        console.log(
          `Found ${cweSimilar.length} similar vulnerabilities with matching CWE`
        );
        relevantVulnerabilities.push(...cweSimilar);
      }
    }

    // If we don't have enough, find by affected products
    if (
      relevantVulnerabilities.length < 4 &&
      inputData.AFFECTED_SOFTWARE !== "Unknown"
    ) {
      // Extract product info
      const affectedSoftware = inputData.AFFECTED_SOFTWARE.toLowerCase();

      console.log(`Looking for vulnerabilities affecting ${affectedSoftware}`);
      const productSimilar = index.vulnerabilities
        .filter((v) => {
          return (
            v.id !== cveId &&
            v.affectedProducts &&
            v.affectedProducts.some((p) => p.toLowerCase().includes(affectedSoftware))
          );
        })
        .sort((a, b) => b.cvssScore - a.cvssScore) // Sort by CVSS score descending
        .slice(0, 3); // Take top 3

      if (productSimilar.length > 0) {
        console.log(
          `Found ${productSimilar.length} similar vulnerabilities affecting the same product`
        );
        // Filter out any duplicates
        productSimilar.forEach((v) => {
          if (!relevantVulnerabilities.some((rv) => rv.id === v.id)) {
            relevantVulnerabilities.push(v);
          }
        });
      }
    }

    // If we still don't have enough, find by severity
    if (relevantVulnerabilities.length < 4 && inputData.SEVERITY_RATING !== "Unknown") {
      const severity = inputData.SEVERITY_RATING.toUpperCase();

      console.log(`Looking for vulnerabilities with ${severity} severity`);
      const severitySimilar = index.vulnerabilities
        .filter((v) => {
          return v.id !== cveId && v.severity === severity;
        })
        .sort((a, b) => (b.published < a.published ? -1 : 1)) // Sort by publication date descending
        .slice(0, 2); // Take only 2 for severity (less relevant than CWE/product)

      if (severitySimilar.length > 0) {
        console.log(
          `Found ${severitySimilar.length} similar vulnerabilities with ${severity} severity`
        );
        // Filter out any duplicates
        severitySimilar.forEach((v) => {
          if (!relevantVulnerabilities.some((rv) => rv.id === v.id)) {
            relevantVulnerabilities.push(v);
          }
        });
      }
    }

    // Limit to max 5 relevant vulnerabilities to avoid token bloat
    const limitedRelevant = relevantVulnerabilities.slice(0, 5);

    if (limitedRelevant.length === 0) {
      console.log("No relevant vulnerabilities found in the index");
      return inputData;
    }

    // Enhance input data with relevant vulnerability context
    console.log(
      `Enhancing input data with ${limitedRelevant.length} relevant vulnerabilities`
    );

    const relevantContext = limitedRelevant
      .map((v) => {
        return `
CVE: ${v.id}
Severity: ${v.severity} (CVSS: ${v.cvssScore})
Published: ${v.published ? new Date(v.published).toISOString().split("T")[0] : "Unknown"}
Description: ${v.description}
${v.cweIds && v.cweIds.length > 0 ? `CWE IDs: ${v.cweIds.join(", ")}` : ""}
${v.affectedProducts && v.affectedProducts.length > 0 ? `Affected Products: ${v.affectedProducts.join(", ")}` : ""}
`;
      })
      .join("\n---\n");

    // Create a new input data object with the enhanced content
    const enhancedInput = { ...inputData };

    // Add relevant context to technical details
    enhancedInput.RELEVANT_VULNERABILITIES = relevantContext;

    // If we have similar vulnerabilities, update the prompt template to use them
    if (enhancedInput.RELEVANT_VULNERABILITIES) {
      console.log("Added relevant vulnerability context to input data");
    }

    return enhancedInput;
  } catch (error) {
    console.error("Error enhancing input with RAG:", error.message);
    // Return original input data if RAG enhancement fails
    return inputData;
  }
}

// Function to generate the blog post using the configured LLM provider
async function generateBlogPost(inputData) {
  const prompt = readPromptTemplate();

  // Use the input data directly (optimizedInputData was removed)
  const dataToUse = inputData;

  // Apply RAG enhancement if enabled
  const enhancedData = await enhanceWithRAG(dataToUse);

  // Add derived fields for hyperlinks
  if (enhancedData.CWE_ID && enhancedData.CWE_ID.startsWith("CWE-")) {
    enhancedData.CWE_ID_NUMBER = enhancedData.CWE_ID.replace("CWE-", "");
  } else {
    enhancedData.CWE_ID_NUMBER = enhancedData.CWE_ID || "";
  }

  // Create threat actors link or fallback text
  if (
    enhancedData.THREAT_ACTORS &&
    enhancedData.THREAT_ACTORS !== "No specific threat actor information available"
  ) {
    enhancedData.THREAT_ACTORS_LINK = `[Threat Actor Details: ${enhancedData.THREAT_ACTORS}](https://attack.mitre.org/groups/)`;
  } else {
    enhancedData.THREAT_ACTORS_LINK = "No specific information available";
  }

  // Replace placeholders in the prompt with actual data
  let populatedPrompt = prompt;
  for (const [key, value] of Object.entries(enhancedData)) {
    populatedPrompt = populatedPrompt.replace(new RegExp(`\\{${key}\\}`, "g"), value);
  }

  try {
    // Set provider based on command line option or environment variable
    const provider = options.provider || process.env.LLM_PROVIDER || "openai";
    let modelOptions = {
      temperature: 0.7,
    };

    // Store provider for token usage tracking
    tokenUsage.provider = provider;

    // Use the latest models as specified, with smart fallbacks
    // The USE_EFFICIENT_MODEL env var can be used to override and use more efficient models
    const useEfficientModel = process.env.USE_EFFICIENT_MODEL === "true";

    if (provider === "openai") {
      // Try to use GPT-4 Turbo as preferred for OpenAI
      modelOptions.model = "gpt-4-turbo"; // Latest GPT-4 Turbo model

      // Check if a specific model version is requested
      if (process.env.OPENAI_MODEL) {
        modelOptions.model = process.env.OPENAI_MODEL;
        console.log(`Using specifically requested OpenAI model: ${modelOptions.model}`);
      }

      modelOptions.maxTokens = 8192; // Higher token limit for comprehensive blog posts
      modelOptions.presence_penalty = 0.1; // Slightly discourage repetition
      modelOptions.frequency_penalty = 0.1; // Slightly discourage repetition

      console.log(
        `Using OpenAI ${modelOptions.model} for vulnerability blog generation`
      );
    } else if (provider === "gemini") {
      // Use Gemini 1.5 Pro as the stable model
      // Note: As of mid-2024, Gemini 1.5 Pro is the reliable model
      let preferredModel = "gemini-1.5-pro"; // Use stable Gemini model
      let fallbackModel = "gemini-pro"; // Fallback to previous generation

      // Allow environment variable override
      if (process.env.GEMINI_MODEL) {
        preferredModel = process.env.GEMINI_MODEL;
        console.log(`Using specifically requested Gemini model: ${preferredModel}`);
      }

      // Try to use the preferred model, gracefully fall back if not available
      try {
        modelOptions.model = preferredModel;

        // If connection testing is needed, it would go here
        // For now, we'll just set the model and let the API handle availability
      } catch (err) {
        console.log(
          `Preferred Gemini model unavailable, falling back to ${fallbackModel}`
        );
        modelOptions.model = fallbackModel;
      }

      modelOptions.maxOutputTokens = 8192; // Higher token limit for comprehensive blogs
      modelOptions.topK = 40; // Default value for highest quality
      modelOptions.topP = 0.95; // Default value for highest quality

      console.log(
        `Using Google ${modelOptions.model} for vulnerability blog generation`
      );
    } else if (provider === "claude") {
      // Use Claude 3 Opus as the stable model
      let models = [
        "claude-3-opus-20240229", // Use Claude 3 Opus as stable model
        "claude-3-sonnet-20240229", // Then try Claude 3 Sonnet
        "claude-3-haiku-20240307", // Finally fall back to Claude 3 Haiku
      ];

      // Allow environment variable override
      if (process.env.CLAUDE_MODEL) {
        modelOptions.model = process.env.CLAUDE_MODEL;
        console.log(`Using specifically requested Claude model: ${modelOptions.model}`);
      } else {
        // Set to the first model in our prioritized list, API will handle availability
        modelOptions.model = models[0];
        console.log(`Using Anthropic ${modelOptions.model} as first choice`);
      }

      modelOptions.maxTokens = 8192; // Higher token limit for comprehensive blogs

      console.log(
        `Using Anthropic ${modelOptions.model} for vulnerability blog generation`
      );
    } else {
      console.warn(`Unknown provider '${provider}', defaulting to OpenAI GPT-4 Turbo`);
      modelOptions.model = "gpt-4-turbo"; // Default to GPT-4 Turbo as requested
      modelOptions.maxTokens = 8192;
      tokenUsage.provider = "openai";
    }

    console.log(
      `Generating content with ${tokenUsage.provider} model: ${modelOptions.model}`
    );

    // Estimate token count (very rough estimate - 1 token ≈ 4 chars for English text)
    const estimatedInputTokens = Math.ceil(populatedPrompt.length / 4);
    console.log(`Estimated input tokens: ~${estimatedInputTokens}`);

    // Use the LLM provider module to generate content
    const content = await generateContent(populatedPrompt, modelOptions);

    return content;
  } catch (error) {
    console.error("Error generating blog post:", error.message);
    return null;
  }
}

// Function to save the blog post
function saveBlogPost(content, cveId, inputData) {
  // Process content to remove any remaining placeholders
  let processedContent = content;

  // Replace image placeholder with actual image path
  processedContent = processedContent.replace(
    /\{\{IMAGE_PATH_PLACEHOLDER\}\}/g,
    "blog/security-blog.jpg"
  );

  // Check for other common placeholders that might remain in the content
  const knownPlaceholders = [
    /\{\{[A-Z_]+_PLACEHOLDER\}\}/g, // Any placeholder following the pattern {{NAME_PLACEHOLDER}}
    /\{[A-Z_]+\}/g, // Any variable that wasn't replaced {VARIABLE_NAME}
    /\$\{[A-Z_]+\}/g, // Template literals that weren't processed ${VARIABLE}
    /\[Include .+?\]/g, // Instructions like [Include X]
    /\[Based on .+?\]/g, // References like [Based on X]
  ];

  // Check for and remove each type of placeholder
  knownPlaceholders.forEach((placeholderPattern) => {
    const matches = processedContent.match(placeholderPattern);
    if (matches && matches.length > 0) {
      console.warn(
        `WARNING: Found ${matches.length} unprocessed placeholders: ${matches[0]}...`
      );

      // Replace placeholders with appropriate fallback text or remove them
      if (placeholderPattern.toString().includes("IMAGE_PATH_PLACEHOLDER")) {
        processedContent = processedContent.replace(
          placeholderPattern,
          "blog/security-blog.jpg"
        );
      } else if (placeholderPattern.toString().includes("Based on")) {
        processedContent = processedContent.replace(
          placeholderPattern,
          "Details not available"
        );
      } else if (placeholderPattern.toString().includes("Include")) {
        processedContent = processedContent.replace(placeholderPattern, "");
      } else {
        processedContent = processedContent.replace(placeholderPattern, "");
      }
    }
  });

  const date = format(new Date(), "yyyy-MM-dd");
  const slug = cveId.toLowerCase().replace(/[^a-z0-9]/g, "-");
  const filename = `${date}-vulnerability-analysis-${slug}.md`;
  const filePath = path.join(__dirname, "../../src/posts", filename);

  // Generate tags based on the vulnerability data
  const tags = ["security", "vulnerability", cveId, "cloud-security"];

  // Add AWS tag if relevant
  if (inputData.AWS_IMPACT && inputData.AWS_IMPACT.includes("Direct impact")) {
    tags.push("aws");
  }

  // Add container tag if relevant
  if (
    inputData.AFFECTED_SOFTWARE &&
    (inputData.AFFECTED_SOFTWARE.toLowerCase().includes("container") ||
      inputData.AFFECTED_SOFTWARE.toLowerCase().includes("kubernetes") ||
      inputData.AFFECTED_SOFTWARE.toLowerCase().includes("docker"))
  ) {
    tags.push("containers");
  }

  // Add severity tag
  if (inputData.SEVERITY_RATING) {
    tags.push(inputData.SEVERITY_RATING.toLowerCase());
  }

  // Add KEV tag if applicable
  if (inputData.IS_KEV && inputData.IS_KEV !== "No" && inputData.IS_KEV !== "Unknown") {
    tags.push("actively-exploited");
    tags.push("cisa-kev");
  }

  // Create a description that includes more context
  let description = `A detailed analysis of ${cveId}`;
  if (inputData.SEVERITY_RATING && inputData.SEVERITY_RATING !== "Unknown") {
    description += ` (${inputData.SEVERITY_RATING} severity)`;
  }

  if (inputData.AFFECTED_SOFTWARE && inputData.AFFECTED_SOFTWARE !== "Unknown") {
    description += ` affecting ${inputData.AFFECTED_SOFTWARE}`;
  }

  description += `, its impact on cloud infrastructure, and mitigation strategies.`;

  // Add data sources to the frontmatter
  const sources = inputData.DATA_SOURCES || "National Vulnerability Database (NVD)";

  // Truncate long fields to optimize token usage
  const MAX_TECHNICAL_DETAILS_LENGTH = 3000;

  // Create optimized inputData with truncated fields
  const optimizedInputData = { ...inputData };

  // Truncate technical details if too long
  if (
    inputData.TECHNICAL_DETAILS &&
    inputData.TECHNICAL_DETAILS.length > MAX_TECHNICAL_DETAILS_LENGTH
  ) {
    optimizedInputData.TECHNICAL_DETAILS =
      inputData.TECHNICAL_DETAILS.substring(0, MAX_TECHNICAL_DETAILS_LENGTH) +
      `\n\n[... ${inputData.TECHNICAL_DETAILS.length - MAX_TECHNICAL_DETAILS_LENGTH} more characters truncated to save tokens ...]`;
    console.log(
      `Truncated TECHNICAL_DETAILS field from ${inputData.TECHNICAL_DETAILS.length} to ${MAX_TECHNICAL_DETAILS_LENGTH} characters`
    );
  }

  // Create a standardized title in the format "CVE ID - Severity - Short Description"
  let vulnTitle = cveId; // Start with CVE ID

  // Add severity if known
  if (inputData.SEVERITY_RATING && inputData.SEVERITY_RATING !== "Unknown") {
    vulnTitle += ` - ${inputData.SEVERITY_RATING}`;
  } else {
    vulnTitle += " - Unknown Severity";
  }

  // Add a short description based on available information
  if (inputData.VULN_NAME && inputData.VULN_NAME !== cveId) {
    // If there's a vulnerability name different from the CVE ID, use it
    vulnTitle += ` - ${inputData.VULN_NAME.replace(cveId, "").trim()}`;
  } else if (inputData.AFFECTED_SOFTWARE && inputData.AFFECTED_SOFTWARE !== "Unknown") {
    // Otherwise use affected software with vulnerability type if available
    let description = inputData.AFFECTED_SOFTWARE;

    // Add vulnerability type if known
    if (inputData.CWE_ID && inputData.CWE_ID !== "Unknown") {
      const cweTypes = {
        "CWE-79": "XSS",
        "CWE-89": "SQL Injection",
        "CWE-20": "Input Validation",
        "CWE-78": "OS Command Injection",
        "CWE-22": "Path Traversal",
        "CWE-352": "CSRF",
        "CWE-287": "Authentication Bypass",
        "CWE-502": "Deserialization",
        "CWE-119": "Buffer Overflow",
        "CWE-416": "Use After Free",
        "CWE-434": "File Upload",
        "CWE-94": "Code Injection",
        "CWE-295": "Certificate Validation",
      };

      // Extract CWE ID number
      const cweIdNum = inputData.CWE_ID.match(/CWE-(\d+)/);
      if (cweIdNum && cweTypes[`CWE-${cweIdNum[1]}`]) {
        description += ` ${cweTypes[`CWE-${cweIdNum[1]}`]}`;
      } else {
        // Extract a friendly name from CWE if possible
        const cweMatch = inputData.CWE_ID.match(/CWE-\d+\s+(.+)/);
        if (cweMatch && cweMatch[1]) {
          description += ` ${cweMatch[1]}`;
        }
      }
    }

    vulnTitle += ` - ${description}`;
  } else {
    // If no specific information is available, add a generic description
    vulnTitle += " - Security Vulnerability";
  }

  // Add frontmatter
  const frontmatter = `---
layout: post.njk
title: "${vulnTitle}"
date: ${date}
description: "${description}"
tags: ${JSON.stringify(tags)}
cvss_score: "${inputData.CVSS_SCORE}"
severity: "${inputData.SEVERITY_RATING}"
cwe_id: "${inputData.CWE_ID}"
cwe_id_number: "${inputData.CWE_ID_NUMBER}"
kev_status: "${inputData.IS_KEV}"
data_sources: "${sources}"
---\n\n`;

  // Check if the content starts with ```markdown and ends with ``` - this is a common LLM formatting issue
  let cleanedContent = processedContent; // Use the processed content instead of original
  if (
    cleanedContent.trim().startsWith("```markdown") &&
    cleanedContent.trim().endsWith("```")
  ) {
    console.log("Removing markdown code block wrappers from content...");
    cleanedContent = cleanedContent
      .trim()
      .replace(/^```markdown\n/, "")
      .replace(/```$/, "");
  }

  // Remove any remaining placeholders from the content
  const placeholders = [
    "{{IMAGE_PATH_PLACEHOLDER}}",
    "{{CWE_DETAILS_PLACEHOLDER}}",
    "{{DETAILED_DESCRIPTION_PLACEHOLDER}}",
    "{{SPECIFIC_IMPACTS_PLACEHOLDER}}",
    "{{PATCH_DETAILS_PLACEHOLDER}}",
    "{{MITIGATION_STEPS_PLACEHOLDER}}",
  ];

  for (const placeholder of placeholders) {
    if (cleanedContent.includes(placeholder)) {
      console.log(`Warning: Removing placeholder ${placeholder} from final content`);
      cleanedContent = cleanedContent.replace(new RegExp(placeholder, "g"), "");
    }
  }

  // Enhanced placeholder detection and removal
  // Check for and remove any remaining variable placeholders
  const placeholderPatterns = [
    { pattern: /\{[A-Z_]+\}/g, replacement: "" }, // {VARIABLE_NAME}
    { pattern: /\[Based on [^\]]+\]/g, replacement: "Details not available" }, // [Based on X]
    { pattern: /\[Include [^\]]+\]/g, replacement: "" }, // [Include X]
    { pattern: /\[\[.*?\]\]/g, replacement: "" }, // [[template instructions]]
    { pattern: /\({.*?}\)/g, replacement: "()" }, // Empty parentheses from removed placeholders
    { pattern: /\[[^\]]*?{[^}]*?}[^\]]*?\]/g, replacement: "" }, // Links with placeholders inside
  ];

  for (const { pattern, replacement } of placeholderPatterns) {
    const matches = cleanedContent.match(pattern);
    if (matches && matches.length > 0) {
      console.warn(
        `WARNING: Found ${matches.length} instances of pattern ${pattern}: "${matches[0]}..."`
      );
      cleanedContent = cleanedContent.replace(pattern, replacement);
    }
  }

  // Remove excessive whitespace and normalize newlines
  cleanedContent = cleanedContent
    .replace(/\n\s*\n\s*\n/g, "\n\n") // Replace 3+ newlines with 2
    .replace(/\s+$/gm, "") // Trim trailing whitespace on each line
    .replace(/^\s+/gm, "") // Trim leading whitespace on each line that's just spaces
    .replace(/\n{3,}/g, "\n\n"); // Replace 3+ newlines with 2

  // Replace image placeholder with actual image path (just in case it wasn't caught earlier)
  cleanedContent = cleanedContent.replace(
    /\{\{IMAGE_PATH_PLACEHOLDER\}\}/g,
    "blog/security-blog.jpg"
  );

  const fullContent = frontmatter + cleanedContent;

  fs.writeFileSync(filePath, fullContent);
  console.log(`Blog post saved to ${filePath}`);

  // Save a backup copy for debugging if needed
  const debugPath = path.join(path.dirname(filePath), "debug", filename);
  try {
    fs.mkdirSync(path.join(path.dirname(filePath), "debug"), { recursive: true });
    fs.writeFileSync(debugPath, frontmatter + content); // Original content for comparison
    console.log(`Debug copy saved to ${debugPath}`);
  } catch (err) {
    console.warn(`Failed to save debug copy: ${err.message}`);
  }
  return filePath;
}

/**
 * Function to find the latest critical vulnerability
 * Prioritizes current year CVEs if configured
 * @returns {Promise<string|null>} The CVE ID of the latest critical vulnerability
 */
async function findLatestCriticalCVE() {
  try {
    // Get current date and year
    const now = new Date();
    const currentYear = now.getFullYear();

    // Check if we should prioritize CVEs from current year
    const prioritizeCurrentYear = process.env.PRIORITIZE_CURRENT_YEAR === "true";

    // Get max vulnerability age from config or default to 180 days
    const maxVulnerabilityAgeDays = parseInt(
      process.env.MAX_VULNERABILITY_AGE_DAYS || "180",
      10
    );

    // Format date N days ago as YYYY-MM-DD for NVD API
    const startDate = new Date(now);
    startDate.setDate(now.getDate() - maxVulnerabilityAgeDays);
    const pubStartDate = format(startDate, "yyyy-MM-dd");

    // Set up headers with API key if available
    const headers = {
      "User-Agent": "William Zujkowski Blog Vulnerability Analyzer",
    };

    // Add NVD API key if available
    if (process.env.NVD_API_KEY) {
      console.log("Using NVD API key for higher rate limits");
      headers["apiKey"] = process.env.NVD_API_KEY;
    }

    // Get minimum CVSS score from config or default to 9.0 (Critical)
    const minCvssScore = parseFloat(process.env.MIN_CVSS_SCORE || "9.0");

    // If prioritizing current year, try to get CVEs from current year first
    if (prioritizeCurrentYear) {
      console.log(
        `Prioritizing current year (${currentYear}) CVEs with critical severity`
      );

      // First try to get current year critical vulnerabilities
      const currentYearResponse = await axios.get(
        "https://services.nvd.nist.gov/rest/json/cves/2.0",
        {
          params: {
            pubStartDate: `${currentYear}-01-01`,
            cvssV3Severity: "CRITICAL",
            resultsPerPage: 10,
          },
          headers,
        }
      );

      if (
        currentYearResponse.data &&
        currentYearResponse.data.vulnerabilities &&
        currentYearResponse.data.vulnerabilities.length > 0
      ) {
        console.log(
          `Found ${currentYearResponse.data.vulnerabilities.length} critical vulnerabilities from ${currentYear}`
        );
        // Return the CVE ID of the most recent critical vulnerability from current year
        return currentYearResponse.data.vulnerabilities[0].cve.id;
      }

      console.log(
        `No critical vulnerabilities found for ${currentYear}. Trying high severity from current year...`
      );

      // Try high severity from current year
      const currentYearHighResponse = await axios.get(
        "https://services.nvd.nist.gov/rest/json/cves/2.0",
        {
          params: {
            pubStartDate: `${currentYear}-01-01`,
            cvssV3Severity: "HIGH",
            resultsPerPage: 10,
          },
          headers,
        }
      );

      if (
        currentYearHighResponse.data &&
        currentYearHighResponse.data.vulnerabilities &&
        currentYearHighResponse.data.vulnerabilities.length > 0
      ) {
        console.log(
          `Found ${currentYearHighResponse.data.vulnerabilities.length} high severity vulnerabilities from ${currentYear}`
        );
        return currentYearHighResponse.data.vulnerabilities[0].cve.id;
      }
    }

    // If we get here, either we're not prioritizing current year or we didn't find any current year CVEs
    console.log(
      `Searching for vulnerabilities from the last ${maxVulnerabilityAgeDays} days with CVSS score >= ${minCvssScore}`
    );

    // Fetch data from NVD API with filters:
    // - Published in the configured time period
    // - CVSS v3 score >= configured minimum (default: Critical severity)
    // - Sort by publishDate descending to get newest first
    const response = await axios.get(
      "https://services.nvd.nist.gov/rest/json/cves/2.0",
      {
        params: {
          pubStartDate,
          cvssV3Severity: "CRITICAL",
          resultsPerPage: 10,
        },
        headers,
      }
    );

    // Check if we have results
    if (
      response.data &&
      response.data.vulnerabilities &&
      response.data.vulnerabilities.length > 0
    ) {
      // Return the CVE ID of the most recent critical vulnerability
      return response.data.vulnerabilities[0].cve.id;
    }

    // If no critical vulnerabilities found, try with high severity
    console.log("No critical vulnerabilities found. Trying with high severity...");
    const highSeverityResponse = await axios.get(
      "https://services.nvd.nist.gov/rest/json/cves/2.0",
      {
        params: {
          pubStartDate,
          cvssV3Severity: "HIGH",
          resultsPerPage: 5,
        },
        headers,
      }
    );

    if (
      highSeverityResponse.data &&
      highSeverityResponse.data.vulnerabilities &&
      highSeverityResponse.data.vulnerabilities.length > 0
    ) {
      // Return the CVE ID of the most recent high severity vulnerability
      return highSeverityResponse.data.vulnerabilities[0].cve.id;
    }

    console.log(
      "No high or critical vulnerabilities found in the last 30 days via NVD API."
    );

    // Fallback to a known list of important CVEs for demonstration/testing (prioritizing 2024/2025 CVEs)
    const fallbackCVEs = [
      "CVE-2024-3094", // XZ Utils backdoor
      "CVE-2024-0519", // Linux kernel privilege escalation
      "CVE-2024-21626", // Microsoft Windows recovery environment vulnerability
      "CVE-2024-1086", // Linux iptables issues
      "CVE-2024-22008", // Windows Imaging Component RCE
      "CVE-2023-50164", // Apache Struts code execution
      "CVE-2023-46604", // Apache ActiveMQ Remote Code Execution
    ];

    console.log("Using fallback CVE list...");
    // Return a random CVE from the fallback list
    return fallbackCVEs[Math.floor(Math.random() * fallbackCVEs.length)];
  } catch (error) {
    console.error("Error finding latest critical CVE:", error.message);
    if (error.response) {
      console.error("API response:", error.response.data);
    }

    // Last resort fallback
    console.log("Falling back to default CVE...");
    return "CVE-2023-50164";
  }
}

// Main function
async function main() {
  try {
    if (options.cve) {
      // Generate a blog post for a specific CVE
      console.log(`Generating blog post for ${options.cve}...`);
      const inputData = await createInputData(options.cve);
      if (!inputData) {
        console.error("Failed to get any vulnerability data, even fallback data");
        process.exit(1);
      }

      console.log("Successfully created input data, generating blog post...");
      const blogContent = await generateBlogPost(inputData);
      if (!blogContent) {
        console.error("Failed to generate blog post");
        process.exit(1);
      }

      console.log("Successfully generated blog post, saving...");
      // Use original inputData for frontmatter to preserve all metadata
      saveBlogPost(blogContent, options.cve, inputData);

      // Output token usage statistics
      if (global.tokenUsage && global.tokenUsage.input) {
        console.log(`\nToken Usage Summary:`);
        console.log(`Provider: ${global.tokenUsage.provider}`);
        console.log(`Model: ${global.tokenUsage.model}`);
        console.log(
          `Input tokens: ${global.tokenUsage.input}${global.tokenUsage.estimated ? " (estimated)" : ""}`
        );
        console.log(
          `Output tokens: ${global.tokenUsage.output}${global.tokenUsage.estimated ? " (estimated)" : ""}`
        );
        console.log(
          `Total tokens: ${global.tokenUsage.input + global.tokenUsage.output}${global.tokenUsage.estimated ? " (estimated)" : ""}`
        );
      }

      console.log("Blog post generation complete!");
    } else if (options.latest) {
      console.log("Searching for latest critical vulnerabilities...");

      // Find the latest critical vulnerability
      const latestCveId = await findLatestCriticalCVE();

      if (!latestCveId) {
        console.error("Failed to find a recent critical vulnerability");
        process.exit(1);
      }

      console.log(`Found vulnerability: ${latestCveId}`);
      console.log(`Generating blog post for ${latestCveId}...`);
      const inputData = await createInputData(latestCveId);

      if (!inputData) {
        console.error("Failed to get any vulnerability data, even fallback data");
        process.exit(1);
      }

      console.log("Successfully created input data, generating blog post...");
      // Create optimizedInputData if it's not already defined (for fallback/minimal data cases)
      const optimizedData = { ...inputData };
      const blogContent = await generateBlogPost({
        ...inputData,
        optimizedInputData: optimizedData,
      });
      if (!blogContent) {
        console.error("Failed to generate blog post");
        process.exit(1);
      }

      console.log("Successfully generated blog post, saving...");
      saveBlogPost(blogContent, latestCveId, inputData);
      console.log("Blog post generation complete!");
    } else if (options.weekly) {
      // In a full implementation, this would generate a weekly roll-up
      console.error("--weekly option not yet implemented");
      process.exit(1);
    } else {
      console.error("Please specify --cve, --latest, or --weekly");
      process.exit(1);
    }
  } catch (error) {
    console.error("Unhandled error in main function:", error.message);
    if (error.response) {
      console.error("API Response Status:", error.response.status);
      console.error("API Response Data:", error.response.data);
    }
    process.exit(1);
  }
}

main().catch((error) => {
  console.error("Unhandled error:", error);
  process.exit(1);
});
