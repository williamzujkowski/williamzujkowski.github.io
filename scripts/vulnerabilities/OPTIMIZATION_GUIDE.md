# Token Optimization Guide for Vulnerability Blog Generator

This document outlines our current approach to token optimization and cost reduction in the vulnerability blog post generator. The strategies described here can be adjusted based on your specific requirements for quality vs. cost efficiency.

## Current Optimization Strategies

### 1. Data Source Management

```javascript
// Determine which data sources are enabled
const enabledSources = {
  mitre: process.env.MITRE_API_ENABLED === "true",
  exploitDb: process.env.EXPLOIT_DB_ENABLED === "true",
  sansIsc: process.env.SANS_ISC_ENABLED === "true",
  zdi: process.env.ZDI_ENABLED === "true",
  certCc: process.env.CERT_CC_ENABLED === "true",
  vuldb: process.env.VULDB_ENABLED === "true",
};

// Only fetch from enabled sources
const [exploitInfo, sansIscData, zdiData, certCcData, vuldbData] = await Promise.all([
  enabledSources.exploitDb ? getExploitDbData(cveId) : null,
  enabledSources.sansIsc ? getSansIscData(cveId) : null,
  enabledSources.zdi ? getZdiData(cveId) : null,
  enabledSources.certCc ? getCertCcData(cveId) : null,
  enabledSources.vuldb ? getVulDbData(cveId) : null,
]);
```

**Adjustable Parameters:**

- Enable/disable specific data sources via environment variables

### 2. Content Truncation

```javascript
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
```

**Adjustable Parameters:**

- `MAX_TECHNICAL_DETAILS_LENGTH` - Maximum allowed length for technical details

### 3. Reference URL Optimization

```javascript
// Use a Set to automatically deduplicate URLs
const uniqueReferences = new Set(references);

// Add references from all sources
if (mitreCveData && mitreCveData.containers?.cna?.references) {
  mitreCveData.containers.cna.references
    .filter((ref) => ref.url)
    .forEach((ref) => uniqueReferences.add(ref.url));
}

// Limit to most important references to save tokens
const MAX_REFERENCES = 10;
const referenceArray = Array.from(uniqueReferences);
const limitedReferences =
  referenceArray.length > MAX_REFERENCES
    ? referenceArray.slice(0, MAX_REFERENCES)
    : referenceArray;
```

**Adjustable Parameters:**

- `MAX_REFERENCES` - Maximum number of references to include

### 4. Model Configuration

```javascript
// Add provider-specific options optimized for token efficiency
if (provider === "openai") {
  // Use GPT-4-turbo for better efficiency
  modelOptions.model = "gpt-4-turbo";
  modelOptions.maxTokens = 3500; // Reduce max tokens to save costs
  modelOptions.presence_penalty = 0.1; // Slightly discourage repetition
  modelOptions.frequency_penalty = 0.1; // Slightly discourage repetition
} else if (provider === "gemini") {
  // Use Flash model which is most cost-efficient
  modelOptions.model = "gemini-2.0-flash";
  modelOptions.maxOutputTokens = 4096; // Reduce from 8192 to save costs
  modelOptions.topK = 30; // Default is 40, lowering slightly improves efficiency
  modelOptions.topP = 0.85; // Default is 0.95, lowering slightly improves efficiency
} else if (provider === "claude") {
  // Use Haiku model which is most cost-efficient
  modelOptions.model =
    process.env.USE_EFFICIENT_MODEL === "true"
      ? "claude-3-haiku-20240307"
      : "claude-3-opus-20240229";
  modelOptions.maxTokens = 3500; // Reduce max tokens to save costs
}
```

**Adjustable Parameters:**

- `USE_EFFICIENT_MODEL` - Environment variable to toggle between faster/cheaper vs. higher-quality models
- Token limits for each model
- Sampling parameters (temperature, topK, topP)

### 5. System Prompts

```javascript
// More concise system prompts (reduced from lengthy descriptions)
const systemPrompt = "Security expert analyzing vulnerabilities.";
```

**Adjustable Parameter:**

- System prompt wording and length

### 6. Error Handling and Retries

```javascript
// Set up retry configuration for external API calls
const maxRetries = 3;
const retryDelay = 2000; // 2 seconds between retries
let retryCount = 0;

while (retryCount < maxRetries) {
  try {
    // API call...
    return result;
  } catch (error) {
    retryCount++;
    console.error(
      `Error fetching data (attempt ${retryCount}/${maxRetries}):`,
      error.message
    );

    if (retryCount >= maxRetries) {
      console.error("All fetch attempts failed");
      return null;
    }

    // Wait before retrying
    console.log(`Waiting ${retryDelay / 1000} seconds before retrying...`);
    await new Promise((resolve) => setTimeout(resolve, retryDelay));
  }
}
```

**Adjustable Parameters:**

- `maxRetries` - Number of retry attempts
- `retryDelay` - Milliseconds to wait between retries

## Environment Variables Summary

| Variable                 | Purpose                                      | Default |
| ------------------------ | -------------------------------------------- | ------- |
| `LLM_PROVIDER`           | Select LLM provider (openai, gemini, claude) | claude  |
| `USE_EFFICIENT_MODEL`    | Use cost-efficient models                    | true    |
| `MITRE_API_ENABLED`      | Enable MITRE CVE API                         | true    |
| `NVD_API_KEY`            | API key for NVD                              | -       |
| `ZDI_ENABLED`            | Enable Zero Day Initiative data              | true    |
| `CERT_CC_ENABLED`        | Enable CERT/CC data                          | true    |
| `VULDB_ENABLED`          | Enable VulDB data                            | true    |
| `SANS_ISC_ENABLED`       | Enable SANS ISC data                         | true    |
| `EXPLOIT_DB_ENABLED`     | Enable Exploit-DB data                       | true    |
| `CISA_KEV_ENABLED`       | Enable CISA KEV data                         | true    |
| `ALIENVAULT_OTX_ENABLED` | Enable AlienVault OTX data                   | true    |
| `ALIENVAULT_OTX_API_KEY` | API key for AlienVault OTX                   | -       |

## Cost Comparison

| Model            | Cost per 1M Input Tokens | Cost per 1M Output Tokens | Relative Quality |
| ---------------- | ------------------------ | ------------------------- | ---------------- |
| GPT-4 Turbo      | $10                      | $30                       | Very High        |
| GPT-3.5 Turbo    | $0.50                    | $1.50                     | Medium           |
| Claude 3 Opus    | $15                      | $75                       | Highest          |
| Claude 3 Sonnet  | $3                       | $15                       | High             |
| Claude 3 Haiku   | $0.25                    | $1.25                     | Medium           |
| Gemini 1.5 Flash | $0.35                    | $1.05                     | Medium           |

## Recommendations

1. **For Efficiency**: Use Claude 3 Haiku or Gemini Flash with reduced content and minimal data sources
2. **For Balance**: Use GPT-4 Turbo or Claude 3 Sonnet with moderately truncated content
3. **For Quality**: Use Claude 3 Opus with selective truncation only for extreme cases

## Making Adjustments

To adjust the token optimization approach:

1. Edit the environment variables in `.env` to enable/disable specific data sources
2. Modify the `MAX_TECHNICAL_DETAILS_LENGTH` constant in the code to allow more/less content
3. Adjust the `MAX_REFERENCES` constant to include more/fewer reference URLs
4. Set `USE_EFFICIENT_MODEL=true` for cost efficiency or `USE_EFFICIENT_MODEL=false` for higher quality
5. Modify model-specific parameters (maxTokens, temperature, etc.) to balance quality and efficiency

## Monitoring and Reporting

Consider adding code to track token usage and API costs:

```javascript
// Example token usage tracking
let totalInputTokens = 0;
let totalOutputTokens = 0;

function updateTokenCount(input, output) {
  totalInputTokens += input;
  totalOutputTokens += output;
  console.log(`Token usage - Input: ${input}, Output: ${output}`);
  console.log(
    `Total this session - Input: ${totalInputTokens}, Output: ${totalOutputTokens}`
  );
}
```

This would help evaluate the effectiveness of optimization strategies and fine-tune parameters for your specific needs.
