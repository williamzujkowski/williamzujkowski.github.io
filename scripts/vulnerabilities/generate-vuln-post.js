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

// Load environment variables
dotenv.config();

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
  .parse(process.argv);

const options = program.opts();

// Function to read the prompt template
function readPromptTemplate() {
  const promptPath = path.join(__dirname, "../../Prompts/threat-blog-post.prompt");
  return fs.readFileSync(promptPath, "utf8");
}

// Function to get vulnerability data from NVD or fallback to MITRE if NVD fails
async function getVulnerabilityData(cveId) {
  try {
    // Set up headers with API key if available
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

      // Convert MITRE data to a format similar to NVD
      const description =
        mitreData.containers?.cna?.descriptions?.find((d) => d.lang === "en")?.value ||
        "";

      // Build a basic NVD-like structure with the information from MITRE
      return {
        id: mitreData.cveMetadata?.cveId,
        descriptions: [
          {
            lang: "en",
            value: description,
          },
        ],
        vulnStatus: "Modified",
        references:
          mitreData.containers?.cna?.references?.map((ref) => ({ url: ref.url })) || [],
        metrics: {}, // No metrics available from MITRE
        weaknesses: [], // No weaknesses available from MITRE
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
    };

    // MITRE API endpoint for specific CVE
    const response = await axios.get(`https://cveawg.mitre.org/api/cve/${cveId}`, {
      headers,
    });

    if (response.data && response.data.cveMetadata) {
      return response.data;
    } else {
      console.log(`No data found in MITRE API for ${cveId}`);
      return null;
    }
  } catch (error) {
    console.error("Error fetching data from MITRE API:", error.message);
    return null;
  }
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

    // Use xml2js to parse the XML
    const parseXml = (xml) => {
      return new Promise((resolve, reject) => {
        parseString(xml, (err, result) => {
          if (err) reject(err);
          else resolve(result);
        });
      });
    };

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

  // Get data from primary sources in parallel
  const [vulnData, mitreCveData, exploitInfo, sansIscData] = await Promise.all([
    getVulnerabilityData(cveId),
    getMitreCveData(cveId),
    getExploitDbData(cveId),
    getSansIscData(cveId),
  ]);

  // We need at least basic vulnerability data to continue
  if (!vulnData) {
    console.error(`Could not retrieve basic vulnerability data for ${cveId}`);
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
    return createMinimalInputData(cveId, fallbackVulnData, mitreCveData);
  }

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
  const references = vulnData.references?.map((ref) => ref.url) || [];

  // Add references from MITRE if available and not already included
  if (mitreCveData && mitreCveData.containers?.cna?.references) {
    const mitreReferences = mitreCveData.containers.cna.references
      .map((ref) => ref.url)
      .filter((url) => !references.includes(url));

    references.push(...mitreReferences);
  }

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

  // Prepare source attribution
  const dataSources = ["National Vulnerability Database (NVD)"];
  if (mitreCveData) dataSources.push("MITRE CVE Program");
  if (isKev !== "Unknown")
    dataSources.push("CISA Known Exploited Vulnerabilities Catalog");
  if (exploitInfo) dataSources.push("Exploit-DB");
  if (sansIscData) dataSources.push("SANS Internet Storm Center");
  if (
    process.env.ALIENVAULT_OTX_ENABLED === "true" &&
    process.env.ALIENVAULT_OTX_API_KEY
  ) {
    dataSources.push("AlienVault Open Threat Exchange");
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

  return {
    CVE_ID: cveId,
    VULN_NAME:
      vulnData.vulnStatus === "Modified"
        ? vulnData.configurations?.[0]?.nodes?.[0]?.cpeMatch?.[0]?.criteria || cveId
        : cveId,
    CVSS_SCORE: cvssScore,
    CVSS_VECTOR: cvssVector,
    SEVERITY_RATING: severityRating,
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
    REFERENCE_URLS: references.join("\n"),
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
function createMinimalInputData(cveId, fallbackVulnData, mitreCveData) {
  console.log(`Using minimal data creation for ${cveId}`);

  // Extract whatever information we can from MITRE data
  let description =
    fallbackVulnData.descriptions.find((d) => d.lang === "en")?.value || "";
  let references = [];

  if (mitreCveData) {
    // Override description with MITRE data if available
    const mitreDescription = mitreCveData.containers?.cna?.descriptions?.find(
      (d) => d.lang === "en"
    )?.value;
    if (mitreDescription) {
      description = mitreDescription;
    }

    // Get references from MITRE if available
    if (mitreCveData.containers?.cna?.references) {
      references = mitreCveData.containers.cna.references.map((ref) => ref.url);
    }
  }

  // Try to get KEV status even with minimal data
  const isKev = "Unknown (CISA KEV status could not be determined)";

  // Set default values for minimal data
  return {
    CVE_ID: cveId,
    VULN_NAME: cveId,
    CVSS_SCORE: "Unknown",
    CVSS_VECTOR: "Unknown",
    SEVERITY_RATING: "Unknown",
    AFFECTED_SOFTWARE: "Unknown",
    AFFECTED_VERSIONS: "Unknown",
    VULN_SUMMARY: description,
    TECHNICAL_DETAILS: description,
    POC_INFO: "No public POC information available.",
    IMPACT_ANALYSIS:
      "Impact analysis could not be determined due to limited information.",
    MITIGATION_GUIDANCE:
      "Follow standard security practices. Monitor vendor advisories for patches and updates.",
    REFERENCE_URLS: references.join("\n") || "No references available.",
    IS_KEV: isKev,
    EXPLOIT_STATUS: "Unknown",
    CWE_ID: "Unknown",
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

// Function to generate the blog post using the configured LLM provider
async function generateBlogPost(inputData) {
  const prompt = readPromptTemplate();

  // Replace placeholders in the prompt with actual data
  let populatedPrompt = prompt;
  for (const [key, value] of Object.entries(inputData)) {
    populatedPrompt = populatedPrompt.replace(new RegExp(`\\{${key}\\}`, "g"), value);
  }

  try {
    // Set model options based on provider
    const provider = process.env.LLM_PROVIDER || "openai";
    let modelOptions = {
      temperature: 0.7,
    };

    // Add provider-specific options
    if (provider === "openai") {
      modelOptions.model = "gpt-4-turbo";
      modelOptions.maxTokens = 4000;
    } else if (provider === "gemini") {
      modelOptions.model = "gemini-2.0-flash";
      modelOptions.maxOutputTokens = 8192;
    } else if (provider === "claude") {
      modelOptions.model = "claude-3-opus-20240229";
      modelOptions.maxTokens = 4000;
    }

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

  // Add frontmatter
  const frontmatter = `---
title: "Vulnerability Analysis: ${cveId}"
date: ${date}
description: "${description}"
tags: ${JSON.stringify(tags)}
cvss_score: "${inputData.CVSS_SCORE}"
severity: "${inputData.SEVERITY_RATING}"
cwe_id: "${inputData.CWE_ID}"
kev_status: "${inputData.IS_KEV}"
data_sources: "${sources}"
---\n\n`;

  // Check if the content starts with ```markdown and ends with ``` - this is a common LLM formatting issue
  let cleanedContent = content;
  if (content.trim().startsWith("```markdown") && content.trim().endsWith("```")) {
    console.log("Removing markdown code block wrappers from content...");
    cleanedContent = content
      .trim()
      .replace(/^```markdown\n/, "")
      .replace(/```$/, "");
  }

  const fullContent = frontmatter + cleanedContent;

  fs.writeFileSync(filePath, fullContent);
  console.log(`Blog post saved to ${filePath}`);
  return filePath;
}

/**
 * Function to find the latest critical vulnerability
 * @returns {Promise<string|null>} The CVE ID of the latest critical vulnerability
 */
async function findLatestCriticalCVE() {
  try {
    // Get current date
    const now = new Date();

    // Get max vulnerability age from config or default to 30 days
    const maxVulnerabilityAgeDays = parseInt(
      process.env.MAX_VULNERABILITY_AGE_DAYS || "30",
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
          resultsPerPage: 5,
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

    // Fallback to a known list of important CVEs for demonstration/testing
    const fallbackCVEs = [
      "CVE-2023-50164", // Kubernetes ingress-nginx Path Traversal
      "CVE-2024-21413", // Windows Mark of the Web Security Feature Bypass
      "CVE-2023-46604", // Apache ActiveMQ Remote Code Execution
      "CVE-2023-4863", // WebP Zero-Day Remote Code Execution
      "CVE-2023-36025", // Windows SmartScreen Security Feature Bypass
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
      saveBlogPost(blogContent, options.cve, inputData);
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
      const blogContent = await generateBlogPost(inputData);
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
