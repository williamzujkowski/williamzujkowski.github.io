# Vulnerability Data Sources

This document describes the data sources used by the vulnerability blog post generator and how they are integrated.

## Overview

The vulnerability blog post generator pulls data from multiple authoritative sources to create comprehensive, accurate content. By combining information from various systems, we get a more complete picture of each vulnerability, including:

- Core vulnerability details (description, affected systems, severity)
- Exploitation status and active threats
- Technical details and context
- Mitigation guidance and references

## Configured Data Sources

| Source                                | Description                                             | API Key Required | `.env` Keys                                        |
| ------------------------------------- | ------------------------------------------------------- | ---------------- | -------------------------------------------------- |
| National Vulnerability Database (NVD) | NIST's comprehensive vulnerability database             | Recommended      | `NVD_API_KEY`                                      |
| MITRE CVE                             | Authoritative source for CVE information                | No               | `MITRE_API_ENABLED`, `MITRE_USER_AGENT`            |
| CISA KEV                              | List of vulnerabilities known to be exploited           | No               | `CISA_KEV_ENABLED`                                 |
| SANS Internet Storm Center            | Security community analysis and early warnings          | No               | `SANS_ISC_ENABLED`                                 |
| Exploit-DB                            | Database of public exploits                             | No               | `EXPLOIT_DB_ENABLED`                               |
| AlienVault OTX                        | Threat intelligence platform with info on threat actors | Yes              | `ALIENVAULT_OTX_API_KEY`, `ALIENVAULT_OTX_ENABLED` |

## Integration Details

### National Vulnerability Database (NVD)

The NVD is our primary source for vulnerability information, providing:

- Basic CVE information and descriptions
- CVSS scores and vectors
- Affected software and versions (CPE data)
- CWE weaknesses
- References

**Implementation Details:**

- Function: `getVulnerabilityData()`
- Uses NVD REST API v2.0
- Higher rate limits with API key (recommended but not required)
- Fetches complete vulnerability record

### MITRE CVE Program

MITRE maintains the official CVE list and often has additional details:

- Authoritative vulnerability descriptions
- Additional references
- More detailed technical information

**Implementation Details:**

- Function: `getMitreCveData()`
- Uses MITRE CVE API from cveawg.mitre.org
- No API key required
- Enhances technical details section with additional context

### CISA Known Exploited Vulnerabilities (KEV) Catalog

The CISA KEV catalog lists vulnerabilities actively exploited in the wild:

- Indicates if a vulnerability is actively exploited
- Provides date added to KEV list
- Helps prioritize vulnerabilities that need immediate attention

**Implementation Details:**

- Function: `checkCisaKev()`
- Uses JSON feed from CISA's website
- No API key required
- Adds "actively-exploited" tag to posts for KEV vulnerabilities

### Exploit-DB

Exploit-DB catalogs public exploits for vulnerabilities:

- Indicates if public exploit code exists
- Provides links to exploit code
- Includes descriptions and author information

**Implementation Details:**

- Function: `getExploitDbData()`
- Parses Exploit-DB's CSV database
- No API key required
- Enhances POC information section with exploit details

### SANS Internet Storm Center

SANS ISC provides community-driven security analysis and early warnings:

- Expert analysis from security professionals
- Real-world context for vulnerabilities
- Trends and techniques used by attackers
- Links to detailed write-ups

**Implementation Details:**

- Function: `getSansIscData()`
- Parses the SANS ISC RSS feed
- No API key required
- Enhances technical details with expert analysis

### AlienVault Open Threat Exchange (OTX)

OTX provides threat intelligence information:

- Threat actor information
- Malware campaigns associated with vulnerabilities
- Industry-targeted attacks

**Implementation Details:**

- Function: `searchThreatActors()`
- Uses OTX API v1
- Requires API key
- Enhances threat actor information section

## Testing Data Sources

You can test the integration with each data source using the test-data-sources.js script:

```bash
# Test with default CVE
npm run test:sources

# Test with specific CVE
npm run test:sources:cve CVE-2023-46604
```

This will check each data source and report on its availability and the data retrieved.

## Data Flow

The vulnerability data processing follows this flow:

1. Fetch data from multiple sources in parallel (NVD, MITRE, Exploit-DB)
2. Combine and enhance data in the `createInputData()` function
3. Additional API calls for threat actor info (AlienVault OTX) and KEV status (CISA)
4. Format data for input to the LLM prompt
5. Generate blog post content
6. Save with enhanced frontmatter including data source attribution

## Extending with New Sources

To add a new data source:

1. Add configuration in `.env.sample`
2. Create a function to fetch and process data from the source
3. Integrate the function in `createInputData()`
4. Add the source to the data attribution in the blog post

## Future Enhancements

Planned data source integrations:

- **Red Hat Security Data API**: For enhanced Linux/enterprise vulnerability details
- **Snyk Vulnerability Database**: For deeper package/dependency vulnerability context
- **VirusTotal**: For malware intelligence related to the vulnerability
- **GitHub Security Advisories**: For community security patches and developer context
