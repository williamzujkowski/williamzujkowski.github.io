# API Keys for Vulnerability Analysis

This document provides comprehensive guidance on obtaining and configuring API keys for the vulnerability post generation system.

## Required API Keys for GitHub Secrets

These keys should be configured as GitHub Secrets in your repository settings (Settings → Secrets and variables → Actions → New repository secret).

### LLM Provider API Keys

| Secret Name      | Description                               | Required | How to Obtain                                                                                                                                                      |
| ---------------- | ----------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and other models | Yes      | 1. Sign up at https://platform.openai.com/signup<br>2. Navigate to https://platform.openai.com/api-keys<br>3. Click "Create new secret key"                        |
| `GOOGLE_API_KEY` | Google API key for Gemini models          | Yes      | 1. Sign up at https://makersuite.google.com/app/apikey<br>2. Create a new API key in the Google AI Studio<br>3. Enable the Gemini API in your Google Cloud project |
| `CLAUDE_API_KEY` | Anthropic API key for Claude models       | Yes      | 1. Sign up at https://console.anthropic.com/<br>2. Navigate to https://console.anthropic.com/settings/keys<br>3. Create a new API key                              |

### Data Source API Keys

| Secret Name              | Description                             | Required    | How to Obtain                                                                                                                           |
| ------------------------ | --------------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `NVD_API_KEY`            | National Vulnerability Database API key | Recommended | 1. Visit: https://nvd.nist.gov/developers/request-an-api-key<br>2. Register with your email address<br>3. Receive the API key via email |
| `ALIENVAULT_OTX_API_KEY` | AlienVault Open Threat Exchange API key | Optional    | 1. Visit: https://otx.alienvault.com/api<br>2. Register for a free account<br>3. Access your API key from account settings              |

### User Agent Configuration

| Secret Name        | Description                   | Required | Default Value                                   |
| ------------------ | ----------------------------- | -------- | ----------------------------------------------- |
| `VULDB_USER_AGENT` | User agent for VulDB requests | Optional | "William Zujkowski Blog Vulnerability Analyzer" |
| `MITRE_USER_AGENT` | User agent for MITRE requests | Optional | "William Zujkowski Blog Vulnerability Analyzer" |

### Feature Toggles

| Secret Name           | Description                            | Required | Default Value |
| --------------------- | -------------------------------------- | -------- | ------------- |
| `USE_EFFICIENT_MODEL` | Use smaller, more efficient LLM models | Optional | true          |
| `MITRE_API_ENABLED`   | Enable MITRE CVE API                   | Optional | true          |
| `ZDI_ENABLED`         | Enable Zero Day Initiative data        | Optional | true          |
| `CERT_CC_ENABLED`     | Enable CERT/CC Vulnerability Notes     | Optional | true          |
| `VULDB_ENABLED`       | Enable VulDB data                      | Optional | true          |
| `SANS_ISC_ENABLED`    | Enable SANS Internet Storm Center data | Optional | true          |
| `EXPLOIT_DB_ENABLED`  | Enable Exploit-DB data                 | Optional | true          |
| `CISA_KEV_ENABLED`    | Enable CISA KEV Catalog data           | Optional | true          |
| `RAG_ENABLED`         | Enable Retrieval-Augmented Generation  | Optional | true          |

## Setting Up GitHub Secrets

1. Navigate to your GitHub repository
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add each API key and configuration value with the exact name shown in the tables above
5. For toggle features, use the string value "true" or "false" (including the quotes)

## API Key Best Practices

1. **Regular Rotation**: Rotate API keys regularly (every 30-90 days) for better security
2. **Least Privilege**: Create API keys with the minimum necessary permissions
3. **Monitoring**: Set up usage monitoring for your API keys to detect unusual activity
4. **Separate Keys**: Use different API keys for development/testing and production
5. **Rate Limits**: Be aware of rate limits for each API to prevent service disruptions

## Testing Your Configuration

After configuring your GitHub Secrets, you can test your setup by:

1. Manually triggering the GitHub Actions workflow
2. Check the logs for the "Test Data Sources" and "Test LLM Provider Connectivity" steps
3. Verify that all enabled data sources and LLM providers are working correctly

## Future API Integrations

The following APIs are planned for future integration:

| API                  | Purpose                                | Status  |
| -------------------- | -------------------------------------- | ------- |
| `VIRUSTOTAL_API_KEY` | Malware and exploit detection          | Planned |
| `GITHUB_TOKEN`       | Finding POCs and exploit code          | Planned |
| `SHODAN_API_KEY`     | Identifying exposed vulnerable systems | Planned |
| `RED_HAT_API_KEY`    | Enterprise Linux vulnerability data    | Planned |
| `SNYK_API_KEY`       | Package/dependency vulnerability data  | Planned |

## Local Development vs. GitHub Actions

For local development, copy `.env.sample` to `.env` and add your API keys there. The GitHub Actions workflow will use the GitHub Secrets instead of the `.env` file.

Example `.env` file:

```
# LLM Provider API Keys
OPENAI_API_KEY=your-openai-api-key
GOOGLE_API_KEY=your-google-api-key
CLAUDE_API_KEY=your-claude-api-key

# Data Source API Keys
NVD_API_KEY=your-nvd-api-key
ALIENVAULT_OTX_API_KEY=your-alienvault-otx-api-key

# Feature Toggles
USE_EFFICIENT_MODEL=true
MITRE_API_ENABLED=true
RAG_ENABLED=true
```

## Troubleshooting

Common issues and solutions:

1. **Rate Limiting**: If you encounter rate limiting errors, check your API key's rate limits and add delays between requests
2. **Authentication Errors**: Verify that your API keys are valid and correctly formatted in GitHub Secrets
3. **Missing Data**: Enable the appropriate feature toggle for each data source you want to use
4. **Data Source Timeouts**: Some data sources may be temporarily unavailable; the system will continue with available sources

For persistent issues, check the logs in the GitHub Actions workflow for detailed error messages.
