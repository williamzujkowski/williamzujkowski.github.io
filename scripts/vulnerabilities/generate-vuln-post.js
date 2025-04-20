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

// Load environment variables
dotenv.config();

// Get OpenAI API key from environment
const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
if (!OPENAI_API_KEY) {
  console.error("Error: OPENAI_API_KEY environment variable is required");
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

// Function to get vulnerability data from NVD
async function getVulnerabilityData(cveId) {
  try {
    const response = await axios.get(
      `https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=${cveId}`
    );
    if (
      response.data &&
      response.data.vulnerabilities &&
      response.data.vulnerabilities.length > 0
    ) {
      return response.data.vulnerabilities[0].cve;
    } else {
      console.error(`No data found for ${cveId}`);
      return null;
    }
  } catch (error) {
    console.error("Error fetching data from NVD:", error.message);
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
      const found = response.data.vulnerabilities.find((v) => v.cveID === cveId);
      return found ? `Yes - Added ${found.dateAdded}` : "No";
    }
    return "Unknown";
  } catch (error) {
    console.error("Error checking CISA KEV:", error.message);
    return "Unknown";
  }
}

// Function to search for threat actor information
async function searchThreatActors(cveId) {
  // In a real implementation, this would query threat intelligence platforms
  // For now, we'll return placeholder data
  return "No known threat actor associations at this time.";
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
  const vulnData = await getVulnerabilityData(cveId);
  if (!vulnData) return null;

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

  // Get references
  const references = vulnData.references?.map((ref) => ref.url) || [];

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
    TECHNICAL_DETAILS: description, // This would ideally come from a more in-depth analysis
    POC_INFO:
      references.length > 0
        ? "Potential POCs may be available via the provided references."
        : "No public POC information available.",
    IMPACT_ANALYSIS: `This vulnerability has a CVSS score of ${cvssScore} (${severityRating}), indicating significant impact potential.`,
    MITIGATION_GUIDANCE:
      "Update to the latest version of the affected software. Specific patches and workarounds may be available in vendor advisories.",
    REFERENCE_URLS: references.join("\n"),
    IS_KEV: isKev,
    EXPLOIT_STATUS:
      isKev === "No"
        ? "No confirmed exploitation in the wild"
        : "Exploitation confirmed by CISA",
    CWE_ID: cweId,
    THREAT_ACTORS: threatActors,
    AWS_IMPACT: awsImpact,
    CLOUD_RELEVANCE: cloudRelevance,
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
    // Use the LLM provider module to generate content
    const content = await generateContent(populatedPrompt, {
      // Provider-specific options can be set here
      temperature: 0.7,
      // For OpenAI
      model: "gpt-4-turbo",
      maxTokens: 4000,
      // For Gemini
      maxOutputTokens: 8192,
    });

    return content;
  } catch (error) {
    console.error("Error generating blog post:", error.message);
    return null;
  }
}

// Function to save the blog post
function saveBlogPost(content, cveId) {
  const date = format(new Date(), "yyyy-MM-dd");
  const slug = cveId.toLowerCase().replace(/[^a-z0-9]/g, "-");
  const filename = `${date}-vulnerability-analysis-${slug}.md`;
  const filePath = path.join(__dirname, "../../src/posts", filename);

  // Add frontmatter
  const frontmatter = `---
title: "Vulnerability Analysis: ${cveId}"
date: ${date}
description: "A detailed analysis of ${cveId}, its impact on cloud infrastructure, and mitigation strategies."
tags: ["security", "vulnerability", "${cveId}", "cloud-security"]
---\n\n`;

  const fullContent = frontmatter + content;

  fs.writeFileSync(filePath, fullContent);
  console.log(`Blog post saved to ${filePath}`);
  return filePath;
}

// Main function
async function main() {
  if (options.cve) {
    // Generate a blog post for a specific CVE
    console.log(`Generating blog post for ${options.cve}...`);
    const inputData = await createInputData(options.cve);
    if (!inputData) {
      console.error("Failed to get vulnerability data");
      process.exit(1);
    }

    const blogContent = await generateBlogPost(inputData);
    if (!blogContent) {
      console.error("Failed to generate blog post");
      process.exit(1);
    }

    saveBlogPost(blogContent, options.cve);
  } else if (options.latest) {
    // In a full implementation, this would fetch the latest critical vulnerabilities
    console.error("--latest option not yet implemented");
    process.exit(1);
  } else if (options.weekly) {
    // In a full implementation, this would generate a weekly roll-up
    console.error("--weekly option not yet implemented");
    process.exit(1);
  } else {
    console.error("Please specify --cve, --latest, or --weekly");
    process.exit(1);
  }
}

main().catch((error) => {
  console.error("Unhandled error:", error);
  process.exit(1);
});
