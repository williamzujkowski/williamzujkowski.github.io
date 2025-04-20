# API Keys for Vulnerability Analysis

This document provides guidance on obtaining and using the API keys that enhance the vulnerability post generation system.

## Priority API Keys

These keys are listed in order of priority for implementation:

### 1. NVD API Key (National Vulnerability Database)

**Purpose:** Provides higher rate limits and more reliable access to vulnerability data.

**How to obtain:** 
1. Visit: https://nvd.nist.gov/developers/request-an-api-key
2. Register with your email address
3. Receive the API key via email

**Implementation status:** Basic support implemented. The system will use this key automatically when provided in the `.env` file.

### 2. VirusTotal API Key

**Purpose:** Access to malware and exploit detection data, plus threat intelligence.

**How to obtain:**
1. Visit: https://developers.virustotal.com/reference
2. Sign up for a free or premium account
3. Access your API key from the developer dashboard

**Implementation status:** Not yet implemented. Future enhancement planned.

### 3. AlienVault OTX API Key

**Purpose:** Provides threat actor information and campaign data.

**How to obtain:**
1. Visit: https://otx.alienvault.com/api
2. Register for a free account
3. Access your API key from account settings

**Implementation status:** Not yet implemented. Future enhancement planned.

## Setup Instructions

1. Copy `.env.sample` to `.env` in the `scripts/vulnerabilities` directory
2. Add your API keys to the `.env` file
3. Uncomment the relevant lines

Example:
```
# National Vulnerability Database (NVD) API Key
NVD_API_KEY=your-actual-api-key-here
```

## Future Enhancements

These API integrations are planned for future development:

1. **GitHub API:** For finding POCs and exploit code
2. **Shodan API:** For identifying exposed vulnerable systems
3. **AWS Security Hub and Google Security Command Center:** For cloud-specific vulnerability data

## Configuration Options

The `.env` file also allows you to configure:

- `MAX_VULNERABILITY_AGE_DAYS`: How far back to search for vulnerabilities (default: 30)
- `MIN_CVSS_SCORE`: Minimum severity score to consider (default: 9.0)
- `CACHE_DIRECTORY`: Where to store cached vulnerability data

## Adding New API Keys

When adding new API keys:

1. Update the `.env.sample` file with the new key name and description
2. Document the API key in this file
3. Implement the API integration in the relevant scripts
4. Update the GitHub workflow secrets if using CI/CD