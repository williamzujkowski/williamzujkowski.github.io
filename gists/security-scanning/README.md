# Security Scanning Pipeline - Code Examples

This directory contains all code examples from the blog post: [Automated Security Scanning Pipeline with Grype and OSV](https://williamzujkowski.github.io/posts/2025-10-06-automated-security-scanning-pipeline/)

## Overview

A complete automated security scanning pipeline integrating Grype, OSV-Scanner, and Trivy for vulnerability detection in CI/CD workflows. This implementation includes:

- GitHub Actions workflows for automated scanning
- Configuration files for each scanner
- Integration scripts for Wazuh SIEM
- SBOM generation and tracking
- Automated remediation workflows
- VS Code integration for local development

## Directory Structure

```
security-scanning/
├── workflows/              # GitHub Actions workflow files
│   ├── security-scan-workflow-complete.yml    # Main security scanning pipeline
│   ├── scheduled-security-scans.yml           # Daily scheduled scans
│   ├── sbom-generation-workflow.yml           # SBOM generation and scanning
│   └── auto-remediate-vulnerabilities.yml     # Automated dependency updates
├── configs/                # Scanner configuration files
│   ├── grype-config.yaml                      # Grype scanner settings
│   ├── osv-scanner-config.toml                # OSV-Scanner configuration
│   └── trivy-opa-policy.rego                  # Trivy OPA policies
├── scripts/                # Utility scripts
│   ├── vulnerability-scan-comparison.py       # Compare scan results
│   └── wazuh-vulnerability-ingestion.sh       # Send results to Wazuh
└── integrations/           # Integration files
    ├── security-scan-slack-notification.yml   # Slack webhook config
    ├── vscode-security-scan-tasks.json        # VS Code tasks
    ├── wazuh-vulnerability-rules.xml          # Wazuh detection rules
    └── vulnerability-metrics.sql              # PostgreSQL analytics
```

## Quick Start

### 1. Install Security Scanners

```bash
# Install Grype
curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin

# Install OSV-Scanner (requires Go 1.21+)
go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Install Trivy
wget https://github.com/aquasecurity/trivy/releases/download/v0.48.0/trivy_0.48.0_Linux-64bit.deb
sudo dpkg -i trivy_0.48.0_Linux-64bit.deb
```

### 2. Setup GitHub Actions

1. Copy `workflows/security-scan-workflow-complete.yml` to `.github/workflows/security-scan.yml`
2. Configure GitHub secrets (if using Slack/Wazuh):
   - `SLACK_WEBHOOK`: Slack webhook URL
   - `WAZUH_TOKEN`: Wazuh API token
3. Customize scanner configurations in `configs/`

### 3. Local Development Setup

```bash
# Install VS Code tasks
cp integrations/vscode-security-scan-tasks.json .vscode/tasks.json

# Copy scanner configs
cp configs/grype-config.yaml .grype.yaml
cp configs/osv-scanner-config.toml osv-scanner.toml
cp configs/trivy-opa-policy.rego policy/security.rego
```

### 4. Run Security Scans

**From VS Code:**
- Press `Ctrl+Shift+P` → `Tasks: Run Task` → `Security Scan: All`

**From command line:**
```bash
# Scan with Grype
grype dir:. -o json | jq

# Scan with OSV-Scanner
osv-scanner --lockfile=package-lock.json --format=json

# Scan with Trivy
trivy fs . --severity CRITICAL,HIGH
```

## Features

### Automated Scanning
- **Three complementary scanners**: Grype (containers), OSV-Scanner (dependencies), Trivy (comprehensive)
- **Quality gates**: Block deployments on critical findings
- **SARIF reporting**: Upload results to GitHub Security tab
- **Daily scheduled scans**: Continuous monitoring of production images

### Integration
- **Slack notifications**: Real-time alerts on scan failures
- **Wazuh SIEM**: Ship vulnerability data for trend analysis
- **VS Code tasks**: Run scans directly from IDE
- **SBOM generation**: Track dependencies with CycloneDX

### Automation
- **Auto-remediation**: Weekly automated dependency updates
- **Baseline comparison**: Detect new vulnerabilities vs. known issues
- **Metrics dashboard**: PostgreSQL queries for tracking trends

## Scan Results Interpretation

### Severity Levels
- **CRITICAL**: Immediate action required - blocks deployment
- **HIGH**: High priority - should fix within 7 days
- **MEDIUM**: Review and plan remediation
- **LOW**: Track but no urgent action needed

### False Positive Handling
Add to respective config files:
- **Grype**: `.grype.yaml` → `ignore` section
- **OSV-Scanner**: `osv-scanner.toml` → `[ignore]` section
- **Trivy**: Use OPA policies in `security.rego`

## Performance Metrics

Actual scan times from homelab testing (Intel i9-9900K, GitHub-hosted runners):

| Stage | Time | Notes |
|-------|------|-------|
| OSV Scan | 12s | npm + Python dependencies |
| Grype Scan | 35s | Container image layers |
| Trivy Scan | 1m 10s | Comprehensive scan |
| **Total** | **2m** | With parallel execution |

### Optimization Tips
1. **Cache vulnerability databases**: Saves ~40s per run
2. **Parallel scanning**: Use GitHub Actions matrix strategy
3. **Scope scanning**: Exclude `node_modules`, test files
4. **Early failure**: Stop on first critical CVE

## Wazuh Integration

### Setup
1. Copy `scripts/wazuh-vulnerability-ingestion.sh` to `/usr/local/bin/`
2. Configure Wazuh manager IP in script
3. Add `integrations/wazuh-vulnerability-rules.xml` to `/var/ossec/etc/rules/local_rules.xml`
4. Restart Wazuh manager

### Metrics Dashboard
Run `integrations/vulnerability-metrics.sql` queries against your vulnerability tracking database to generate:
- Vulnerability counts by severity
- Mean time to remediate (MTTR)
- Weekly trends

## Scheduled Maintenance

### Daily Tasks
- Review Slack notifications from failed scans
- Investigate new critical vulnerabilities
- Update baselines after legitimate changes

### Weekly Tasks
- Review auto-remediation PRs
- Update ignore lists for confirmed false positives
- Check Wazuh dashboard for trends

### Monthly Tasks
- Update scanner versions
- Review and expire temporary ignores
- Audit security posture metrics

## Troubleshooting

### Common Issues

**OSV-Scanner installation fails:**
- Ensure Go 1.21+ is installed
- Check `$GOPATH/bin` is in `$PATH`

**Grype slow on first run:**
- Database download takes 2-3 minutes initially
- Subsequent runs use cached database

**Too many false positives:**
- Add specific CVEs to ignore lists
- Use `--fail-on-severity high` instead of `medium`
- Review OPA policies to tune thresholds

**GitHub Actions timeout:**
- Increase `timeout-minutes` in workflow
- Consider self-hosted runners for larger projects

## Security Considerations

⚠️ **Important Notes:**
1. **Secrets management**: Never hardcode API tokens or webhook URLs
2. **SBOM storage**: Encrypt SBOMs if they contain sensitive dependency info
3. **Rate limiting**: GitHub API has rate limits for SARIF uploads
4. **Scanner updates**: Vulnerability databases update frequently - expect occasional false positives

## Limitations

- **Coverage gaps**: No single scanner catches everything (60-65% overlap observed)
- **False positives**: Manual review still required for edge cases
- **Maintenance burden**: Database updates can break pipelines unexpectedly
- **Cost**: GitHub-hosted runners cost ~$8/month at homelab scale

## Contributing

Found an issue or have improvements? File an issue at the blog repository or contact via the blog post.

## License

MIT License - Free to use, modify, and distribute

## Related Blog Posts

- [Automated Security Scanning Pipeline with Grype and OSV](https://williamzujkowski.github.io/posts/2025-10-06-automated-security-scanning-pipeline/)
- [Threat Intelligence MITRE ATT&CK Dashboard](https://williamzujkowski.github.io/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard/)
- [Zero Trust VLAN Segmentation](https://williamzujkowski.github.io/posts/2025-09-08-zero-trust-vlan-segmentation-homelab/)

## Acknowledgments

Built and tested in homelab environment with:
- Intel i9-9900K processor
- 64GB RAM
- Dell R940 server
- Ubuntu 22.04 LTS

**Author:** William Zujkowski
**Blog:** https://williamzujkowski.github.io
**Last Updated:** October 2025
