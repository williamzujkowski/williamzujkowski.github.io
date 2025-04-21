# GitHub Actions Workflow for Vulnerability Blog Generation

This document explains how to set up and use the GitHub Actions workflow for generating vulnerability blog posts with multiple LLM providers. The workflow follows the recommendations from the PROCESS_IMPROVEMENTS.md document.

## Overview

The workflow provides:

1. **Multi-Model Support**: Run content generation across OpenAI, Gemini, and Claude providers in parallel
2. **Retrieval-Augmented Generation (RAG)**: Enhance prompts with relevant vulnerability context
3. **Secure Credential Management**: Store API keys as GitHub Secrets
4. **Automated Index Updates**: Keep vulnerability index fresh with daily updates
5. **Token Usage Tracking**: Monitor costs across providers

## Workflow Components

### 1. Main Workflow File

Located at `.github/workflows/generate-vuln-posts.yml`, this workflow orchestrates:

- **Data source testing**: Verifies connectivity to all vulnerability data sources
- **LLM provider testing**: Confirms API keys work for each provider
- **Index updating**: Refreshes the vulnerability knowledge base
- **Blog post generation**: Creates posts with each enabled provider
- **Compare and select**: Evaluates posts from different providers (future enhancement)
- **Notification**: Reports on success/failure

### 2. RAG Implementation

Retrieval-Augmented Generation enhances the prompts with knowledge from:

- **Vulnerability Index**: Updated daily and stored as a workflow artifact
- **Similarity-Based Retrieval**: Finds relevant vulnerabilities based on CWE, product, or severity
- **Context Enhancement**: Adds similar vulnerability information to the LLM prompt

### 3. Token Usage Tracking

Built-in token usage tracking for each provider:

- **OpenAI**: Direct reporting from API response
- **Claude**: Direct reporting from API response
- **Gemini**: Estimated based on text length (API doesn't provide direct counts)

## Setting Up GitHub Secrets

All API keys and configuration must be stored in GitHub Secrets for secure processing.

### Required Secrets

1. Navigate to your GitHub repository
2. Go to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Add the following required secrets:

#### LLM Provider API Keys (Required)

| Secret Name      | Description                               | Required |
| ---------------- | ----------------------------------------- | -------- |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 and other models | Yes      |
| `GOOGLE_API_KEY` | Google API key for Gemini models          | Yes      |
| `CLAUDE_API_KEY` | Anthropic API key for Claude models       | Yes      |

#### Data Source API Keys (Recommended)

| Secret Name              | Description                             | Required    |
| ------------------------ | --------------------------------------- | ----------- |
| `NVD_API_KEY`            | National Vulnerability Database API key | Recommended |
| `ALIENVAULT_OTX_API_KEY` | AlienVault Open Threat Exchange API key | Optional    |

#### Configuration Secrets (Optional)

| Secret Name           | Description                            | Default                                         |
| --------------------- | -------------------------------------- | ----------------------------------------------- |
| `USE_EFFICIENT_MODEL` | Use smaller, more efficient LLM models | true                                            |
| `VULDB_USER_AGENT`    | Custom user agent for VulDB requests   | "William Zujkowski Blog Vulnerability Analyzer" |
| `MITRE_USER_AGENT`    | Custom user agent for MITRE requests   | "William Zujkowski Blog Vulnerability Analyzer" |

#### Feature Toggle Secrets (Optional)

| Secret Name          | Description                            | Default |
| -------------------- | -------------------------------------- | ------- |
| `MITRE_API_ENABLED`  | Enable MITRE CVE API                   | true    |
| `ZDI_ENABLED`        | Enable Zero Day Initiative data        | true    |
| `CERT_CC_ENABLED`    | Enable CERT/CC Vulnerability Notes     | true    |
| `VULDB_ENABLED`      | Enable VulDB data                      | true    |
| `SANS_ISC_ENABLED`   | Enable SANS Internet Storm Center data | true    |
| `EXPLOIT_DB_ENABLED` | Enable Exploit-DB data                 | true    |
| `CISA_KEV_ENABLED`   | Enable CISA KEV Catalog data           | true    |
| `RAG_ENABLED`        | Enable Retrieval-Augmented Generation  | true    |

### Obtaining API Keys

For detailed instructions on obtaining each API key, see [API_KEYS.md](./API_KEYS.md).

## Running the Workflow

### Manual Trigger

Trigger the workflow manually from GitHub's UI with:

1. Navigate to the "Actions" tab in your repository
2. Select "Generate Vulnerability Blog Posts" workflow
3. Click "Run workflow"
4. (Optional) Provide a specific CVE ID and/or provider

### Scheduled Runs

The workflow automatically runs daily at 06:00 UTC to:

1. Update the vulnerability index
2. Check for the latest critical vulnerabilities
3. Generate new blog posts as needed

## Artifacts

The workflow produces several artifacts:

- **vuln-index**: The latest vulnerability knowledge base (JSON format)
- **blog-post-openai**: Posts generated by OpenAI models
- **blog-post-gemini**: Posts generated by Google Gemini models
- **blog-post-claude**: Posts generated by Anthropic Claude models

These artifacts are retained for 7 days before automatic deletion.

## Workflow Options

When triggering manually, you can configure:

- **CVE ID**: Specify a particular CVE to analyze (leave empty for latest critical vulnerability)
- **Provider**: Choose which LLM provider to use (or "all" to use all configured providers)

## Security Features

The workflow implements several security best practices:

1. **Secret Masking**: All API keys and sensitive values are masked in logs using GitHub's `::add-mask::` feature
2. **Least Privilege**: The workflow uses only the permissions needed for its tasks
3. **Conditional Enablement**: Features are enabled only when their corresponding API keys are available
4. **Default Fallbacks**: Secure defaults are used when optional configuration is not provided
5. **Environment Isolation**: Each job runs in a clean environment

## Troubleshooting

### Common Issues

1. **Missing Secrets**: Ensure all required API keys are set in GitHub Secrets
2. **Data Source Failures**: Check the logs from the "Test Data Sources" step
3. **LLM Provider Errors**: Review error messages in the "Generate Posts" step
4. **Authentication Issues**: Verify API keys are correctly formatted and not expired
5. **Rate Limiting**: If you encounter rate limiting, implement delays or use efficient models

### Logs and Monitoring

- The workflow logs token usage statistics for each run
- Examine job logs for detailed information on each step
- Artifacts contain the complete generated content

## Future Enhancements

1. **Quality Comparison**: Automatically compare posts from different providers and select the best
2. **Cost Optimization**: Adaptive provider selection based on content type and budget constraints
3. **Artifact Management**: Improved cleanup and retention policies
4. **Notification Integration**: Slack/Teams/Email notifications for completed posts
5. **Additional API Integrations**: Support for VirusTotal, GitHub, Shodan, and other security APIs
