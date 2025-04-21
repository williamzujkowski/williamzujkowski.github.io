# Vulnerability Blog Generation Workflow Guide

This document provides a comprehensive overview of the vulnerability blog post generation workflow, including the data collection process, prompting approach, blog post creation, and scheduling mechanisms.

## Overview of the Process

The vulnerability blog generator works through the following steps:

1. **CVE Selection**: Identify a specific CVE to analyze or find the latest critical vulnerability
2. **Data Collection**: Gather vulnerability data from multiple security data sources
3. **Input Preparation**: Process and structure the collected data for the LLM
4. **Content Generation**: Generate blog post content using selected LLM provider
5. **Post Creation**: Format and save the blog post with proper frontmatter
6. **Scheduling**: Schedule posts for regular publication (optional)

## 1. CVE Selection Process

### Manual Selection

```bash
node generate-vuln-post.js --cve CVE-2023-XXXXX
```

This method allows you to specify a particular CVE ID to analyze.

### Automatic Selection

```bash
node generate-vuln-post.js --latest
```

The automatic selection process:

1. Queries the NVD API for recent vulnerabilities, filtering for:

   - Published within `MAX_VULNERABILITY_AGE_DAYS` (default: 30 days)
   - CVSS severity of "CRITICAL" or "HIGH"
   - Sorted by publish date (newest first)

2. Returns the most recent critical vulnerability, or falls back to high severity if no critical ones are found

3. Uses fallback CVEs if API fails:
   ```javascript
   const fallbackCVEs = [
     "CVE-2023-50164", // Kubernetes ingress-nginx Path Traversal
     "CVE-2024-21413", // Windows Mark of the Web Security Feature Bypass
     "CVE-2023-46604", // Apache ActiveMQ Remote Code Execution
     "CVE-2023-4863", // WebP Zero-Day Remote Code Execution
     "CVE-2023-36025", // Windows SmartScreen Security Feature Bypass
   ];
   ```

**Adjustable Parameters:**

- `MAX_VULNERABILITY_AGE_DAYS` - Configure how far back to look for vulnerabilities
- `MIN_CVSS_SCORE` - Minimum CVSS score to consider (default: 9.0 for Critical)

## 2. Data Collection Architecture

The system uses a multi-source data collection approach to create comprehensive vulnerability analysis:

```
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   MITRE CVE API  │  │      NVD API     │  │    VulDB Feed    │  │    ZDI Feeds     │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │                     │
         ▼                     ▼                     ▼                     ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              Data Collection Layer                                   │
│                                                                                     │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│   │getMitreCveData│  │getVulnData   │  │getVulDbData  │  │getZdiData    │  ...more  │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘           │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              createInputData Function                                │
│                                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                │
│  │Primary Data │  │ References  │  │  Technical  │  │POC & Exploit│                │
│  │Aggregation  │  │Consolidation│  │Details Merge│  │Information  │                │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              LLM Prompt Generation                                   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Data Source Hierarchy

Sources are prioritized in this order:

1. **MITRE CVE Program** (primary preferred source)

   - First-party authoritative data
   - Function: `getMitreCveData()`

2. **National Vulnerability Database (NVD)**

   - Comprehensive second-party data
   - Function: `getVulnerabilityData()`

3. **Enrichment Sources** (parallel fetching)

   - **CERT/CC**: Detailed vulnerability notes (function: `getCertCcData()`)
   - **ZDI**: Security researcher details (function: `getZdiData()`)
   - **VulDB**: Additional vulnerability data (function: `getVulDbData()`)
   - **Exploit-DB**: Exploit information (function: `getExploitDbData()`)
   - **SANS ISC**: Security community analysis (function: `getSansIscData()`)

4. **Threat Intelligence**
   - **CISA KEV**: Known exploited status (function: `checkCisaKev()`)
   - **AlienVault OTX**: Threat actor information (function: `searchThreatActors()`)

### Fallback Mechanisms

The system implements three-tier fallback for resilience:

1. **Primary Tier**: Try MITRE and NVD sources
2. **Secondary Tier**: Use enrichment sources if primary fails
3. **Minimal Data Fallback**: Create essential data with whatever is available

```javascript
// Fallback to minimal data if both primary sources fail
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
```

## 3. Prompt Engineering Approach

The system uses a template-based approach to prompt engineering:

### Prompt Template Structure

The prompt template is stored in `/Prompts/threat-blog-post.prompt` and follows this structure:

1. **System Context**: Brief definition of the assistant's role as a security expert
2. **Task Definition**: Clear instructions on creating a vulnerability analysis blog post
3. **Input Data**: Placeholders for vulnerability data (replaced at runtime)
4. **Output Format**: Guidelines for blog post structure and formatting
5. **Tone and Style**: Instructions on writing style appropriate for security professionals

### Data-to-Prompt Integration

The following process populates the prompt template:

1. **Template Loading**: Read prompt template from file

   ```javascript
   function readPromptTemplate() {
     const promptPath = path.join(__dirname, "../../Prompts/threat-blog-post.prompt");
     return fs.readFileSync(promptPath, "utf8");
   }
   ```

2. **Data Preparation**: Clean and structure collected data

   ```javascript
   // Use optimized input data if available, otherwise use original
   const dataToUse = inputData.optimizedInputData || inputData;
   ```

3. **Placeholder Replacement**: Replace all placeholders with actual data
   ```javascript
   let populatedPrompt = prompt;
   for (const [key, value] of Object.entries(dataToUse)) {
     populatedPrompt = populatedPrompt.replace(new RegExp(`\\{${key}\\}`, "g"), value);
   }
   ```

### Key Input Fields

Important placeholders in the prompt template:

| Placeholder           | Description                    | Example                                              |
| --------------------- | ------------------------------ | ---------------------------------------------------- |
| `{CVE_ID}`            | The CVE identifier             | CVE-2023-44487                                       |
| `{VULN_NAME}`         | Descriptive name               | [Critical] CVE-2023-44487: HTTP/2 Rapid Reset Attack |
| `{CVSS_SCORE}`        | Numerical severity score       | 7.5                                                  |
| `{SEVERITY_RATING}`   | Textual severity               | High                                                 |
| `{AFFECTED_SOFTWARE}` | Primary affected software      | nginx                                                |
| `{AFFECTED_VERSIONS}` | Specific versions              | nginx 1.25.0, nginx 1.24.0                           |
| `{VULN_SUMMARY}`      | Brief description              | A vulnerability in HTTP/2 protocol...                |
| `{TECHNICAL_DETAILS}` | Extended technical information | The "rapid reset" attack occurs when...              |
| `{POC_INFO}`          | Available exploits             | Public exploits are available: [details]             |
| `{REFERENCE_URLS}`    | Source links                   | https://nvd.nist.gov/vuln/detail/CVE-2023-44487      |
| `{IS_KEV}`            | CISA KEV status                | Yes - Added 2023-10-10                               |
| `{THREAT_ACTORS}`     | Known attackers                | No known threat actor associations at this time      |
| `{DATA_SOURCES}`      | Information sources            | MITRE CVE Program, NVD, SANS ISC                     |

## 4. LLM Integration for Content Generation

### Multi-Provider Support

The system supports three LLM providers with a unified interface:

```javascript
// Set model options based on provider
const provider = process.env.LLM_PROVIDER || "openai";
let modelOptions = {
  temperature: 0.7,
};

// Add provider-specific options
if (provider === "openai") {
  modelOptions.model = "gpt-4-turbo";
  // ...OpenAI-specific options
} else if (provider === "gemini") {
  modelOptions.model = "gemini-2.0-flash";
  // ...Gemini-specific options
} else if (provider === "claude") {
  modelOptions.model = "claude-3-opus-20240229";
  // ...Claude-specific options
}

// Use the LLM provider module to generate content
const content = await generateContent(populatedPrompt, modelOptions);
```

### Provider-Specific Implementations

Each provider has a custom implementation in `llm-providers.js`:

1. **OpenAI**:

   ```javascript
   async function generateWithOpenAI(prompt, options = {}) {
     // ...implementation using OpenAI's API
   }
   ```

2. **Google Gemini**:

   ```javascript
   async function generateWithGemini(prompt, options = {}) {
     // ...implementation using Google's GenerativeAI
   }
   ```

3. **Anthropic Claude**:
   ```javascript
   async function generateWithClaude(prompt, options = {}) {
     // ...implementation using Anthropic's API
   }
   ```

## 5. Blog Post Creation and Formatting

### Post Structure

Each blog post is created with proper frontmatter for the 11ty-based website:

```markdown
---
layout: post.njk
title: "[Critical] CVE-2023-44487: HTTP/2 Rapid Reset Attack"
date: 2023-10-15
description: "A detailed analysis of CVE-2023-44487 (Critical severity) affecting HTTP/2 implementations, its impact on cloud infrastructure, and mitigation strategies."
tags: ["security", "vulnerability", "CVE-2023-44487", "cloud-security", "critical"]
cvss_score: "7.5"
severity: "High"
cwe_id: "CWE-400"
kev_status: "Yes - Added 2023-10-10"
data_sources: "MITRE CVE Program, National Vulnerability Database (NVD)"
---

# [Critical] CVE-2023-44487: HTTP/2 Rapid Reset Attack

[Blog content generated by the LLM...]
```

### Filename Generation

```javascript
// Generate a filename based on date and CVE ID
const date = format(new Date(), "yyyy-MM-dd");
const slug = cveId.toLowerCase().replace(/[^a-z0-9]/g, "-");
const filename = `${date}-vulnerability-analysis-${slug}.md`;
const filePath = path.join(__dirname, "../../src/posts", filename);
```

### Tag Generation

Tags are dynamically generated based on vulnerability properties:

```javascript
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
```

## 6. Post Scheduling and Automation

### Manual Schedule

```bash
node schedule-posts.js
```

The scheduler:

1. Checks if a new post should be generated based on configured frequency
2. If yes, runs the generator with the `--latest` option to find a recent vulnerability
3. Logs the post generation event

### Automatic Schedule (Cron)

```bash
./setup-cron.sh
```

This script sets up a cron job to run the scheduler daily:

```bash
# Add cron job to run the scheduler daily at 8 AM
(crontab -l 2>/dev/null; echo "0 8 * * * cd $(pwd) && node schedule-posts.js >> cron.log 2>&1") | crontab -
```

### Post Frequency Control

The scheduler respects the configured post frequency:

- `MAX_DAYS_BETWEEN_POSTS` (default: 7) - Maximum days before forcing a new post
- `MIN_DAYS_BETWEEN_POSTS` (default: 1) - Minimum days between posts

## 7. Testing and Validation

### Data Source Testing

```bash
npm run test:sources
```

This runs `test-data-sources.js` which:

1. Tests connectivity to each data source
2. Verifies API keys are working
3. Displays sample data from each source

### LLM Provider Testing

```bash
npm run test:openai
npm run test:gemini
npm run test:claude
```

These run `test-models.js` which:

1. Tests connectivity to the selected LLM provider
2. Verifies API keys are working
3. Displays a sample response to a simple prompt

### VulDB Specific Testing

```bash
npm run test:vuldb
```

This runs `test-vuldb.js` which tests the VulDB integration specifically.

## Command Line Interface

```
Usage:
  node generate-vuln-post.js --cve CVE-2023-XXXXX
  node generate-vuln-post.js --latest
  node generate-vuln-post.js --weekly

Options:
  --cve CVE-ID     Generate a post for a specific CVE
  --latest         Generate a post for the latest critical vulnerability
  --weekly         Generate a weekly roll-up of critical vulnerabilities
```

## Dependencies and Environment Setup

### Required Dependencies

```json
"dependencies": {
  "@google/generative-ai": "^0.2.0",
  "axios": "^1.6.2",
  "commander": "^11.1.0",
  "date-fns": "^2.30.0",
  "dotenv": "^16.3.1",
  "lru-cache": "^10.2.0",
  "rimraf": "^5.0.5",
  "glob": "^10.3.10"
}
```

### Environment Variables

See `.env.sample` for a complete list of environment variables.

## Customization Points

To customize the blog post generation:

1. **Prompt Template**: Edit `/Prompts/threat-blog-post.prompt` to change the instructions and format
2. **Data Sources**: Enable/disable sources via environment variables
3. **LLM Provider**: Set `LLM_PROVIDER` and corresponding API keys
4. **Post Frequency**: Adjust `MIN_DAYS_BETWEEN_POSTS` and `MAX_DAYS_BETWEEN_POSTS`
5. **CVE Selection**: Modify `MAX_VULNERABILITY_AGE_DAYS` and `MIN_CVSS_SCORE`
6. **Content Formatting**: Edit the frontmatter generation in `saveBlogPost()`

## Workflow Examples

### Example 1: Generate a Post for a Specific CVE

```bash
# Generate a post for CVE-2023-44487 (HTTP/2 Rapid Reset)
node generate-vuln-post.js --cve CVE-2023-44487
```

### Example 2: Find and Generate for the Latest Critical Vulnerability

```bash
# Generate a post for the most recent critical vulnerability
node generate-vuln-post.js --latest
```

### Example 3: Set Up Automated Posting

```bash
# Configure the environment
cp .env.sample .env
# Edit .env to set API keys and preferences

# Set up the cron job
./setup-cron.sh

# Check cron job status
crontab -l
```

## Troubleshooting

Common issues and solutions:

1. **Missing Data**: If a post lacks detail, check data source connectivity

   ```bash
   npm run test:sources
   ```

2. **API Rate Limits**: If hitting rate limits, add API keys where possible:

   - NVD: Register for API key at https://nvd.nist.gov/developers/request-an-api-key
   - AlienVault OTX: Register at https://otx.alienvault.com/

3. **Quality Issues**: If post quality is inadequate:
   - Set `USE_EFFICIENT_MODEL=false` to use higher-quality models
   - Increase token limits for more detailed content
   - Edit the prompt template for better instructions
