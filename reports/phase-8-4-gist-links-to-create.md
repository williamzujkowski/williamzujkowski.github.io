# GitHub Gist Links to Create - Phase 8.4

**Post:** 2025-10-06-automated-security-scanning-pipeline.md

The following gist placeholders were added to the optimized post. These need to be created with actual gist URLs:

## Gist Files to Create

### 1. security-scan-workflow-complete
**Description:** Full GitHub Actions workflow (109 lines)
**Content:** Complete `.github/workflows/security-scan.yml` with:
- OSV-Scanner dependency scan job
- Grype container scan job
- Trivy comprehensive scan job
- Security gate with blocking logic
- SARIF report uploads
- Slack notification integration

**Current Placeholder:**
```markdown
[Complete implementation with SARIF uploads, quality gates, and Slack notifications](https://gist.github.com/williamzujkowski/security-scan-workflow-complete)
```

### 2. security-scan-slack-notification
**Description:** Complete Slack payload with formatted blocks (27 lines)
**Content:** Full Slack webhook payload YAML with:
- Formatted message blocks
- Repository, branch, commit details
- Link to failed run
- Error context

**Current Placeholder:**
```markdown
[Full implementation](https://gist.github.com/williamzujkowski/security-scan-slack-notification)
```

### 3. vscode-security-scan-tasks
**Description:** VS Code tasks.json (37 lines)
**Content:** Complete `.vscode/tasks.json` with:
- Grype scan task
- OSV scan task
- Combined "Scan All" task
- JSON output with jq formatting

**Current Placeholder:**
```markdown
[Full tasks.json with all three scanners](https://gist.github.com/williamzujkowski/vscode-security-scan-tasks)
```

### 4. grype-config
**Description:** Grype configuration (21 lines)
**Content:** Complete `.grype.yaml` with:
- Multiple vulnerability ignore rules with reasons and expiration dates
- Severity threshold configuration
- Scan scope settings
- Output formatting

**Current Placeholder:**
```markdown
[Full .grype.yaml with all ignore rules](https://gist.github.com/williamzujkowski/grype-config)
```

### 5. osv-scanner-config
**Description:** OSV-Scanner configuration (22 lines)
**Content:** Complete `osv-scanner.toml` with:
- Vulnerability ignore rules
- Dev dependencies handling
- Private package registry configuration
- Parallel scanning settings

**Current Placeholder:**
```markdown
[Full osv-scanner.toml with private registries](https://gist.github.com/williamzujkowski/osv-scanner-config)
```

### 6. trivy-opa-policy
**Description:** Trivy OPA policy (20 lines)
**Content:** Complete `policy/security.rego` with:
- Critical vulnerability deny rules
- Specific package version deny rules (Log4j example)
- High severity warning rules
- Custom vulnerability messages

**Current Placeholder:**
```markdown
[Full security.rego with all deny/warn rules](https://gist.github.com/williamzujkowski/trivy-opa-policy)
```

### 7. scheduled-security-scans
**Description:** Scheduled scan workflow (44 lines)
**Content:** Complete `.github/workflows/scheduled-scan.yml` with:
- Daily cron schedule
- Matrix strategy for multiple images
- Grype and Trivy scanning
- Baseline comparison logic
- SIEM integration (Wazuh)

**Current Placeholder:**
```markdown
[Full workflow with matrix strategy and SIEM integration](https://gist.github.com/williamzujkowski/scheduled-security-scans)
```

### 8. vulnerability-scan-comparison
**Description:** Python scan comparison script (59 lines)
**Content:** Complete `scripts/compare-scans.py` with:
- JSON loading and parsing
- Vulnerability extraction
- Set-based comparison (new/fixed)
- Alert on new vulnerabilities
- Detailed reporting output

**Current Placeholder:**
```markdown
[Full Python script with JSON parsing and reporting](https://gist.github.com/williamzujkowski/vulnerability-scan-comparison)
```

### 9. sbom-generation-workflow
**Description:** SBOM workflow (38 lines)
**Content:** Complete `.github/workflows/sbom-scan.yml` with:
- Release trigger configuration
- CycloneDX SBOM generation
- Grype SBOM scanning
- GitHub release asset upload
- S3 storage for historical comparison

**Current Placeholder:**
```markdown
[Full workflow with CycloneDX generation and S3 storage](https://gist.github.com/williamzujkowski/sbom-generation-workflow)
```

### 10. auto-remediate-vulnerabilities
**Description:** Auto-remediation workflow (47 lines)
**Content:** Complete `.github/workflows/auto-remediate.yml` with:
- Weekly schedule
- OSV vulnerability scanning
- npm audit fix automation
- Re-scan verification
- Automated PR creation with details

**Current Placeholder:**
```markdown
[Full workflow with PR creation and test validation](https://gist.github.com/williamzujkowski/auto-remediate-vulnerabilities)
```

### 11. wazuh-vulnerability-ingestion
**Description:** Wazuh integration script (19 lines)
**Content:** Complete `send-scans-to-wazuh.sh` with:
- Grype scanning
- jq JSON transformation
- Syslog message formatting
- Netcat delivery to Wazuh manager
- Error handling

**Current Placeholder:**
```markdown
[Full script with JSON transformation and error handling](https://gist.github.com/williamzujkowski/wazuh-vulnerability-ingestion)
```

### 12. wazuh-vulnerability-rules
**Description:** Wazuh rules (18 lines)
**Content:** Complete `/var/ossec/etc/rules/local_rules.xml` with:
- Base vulnerability detection rule
- Critical severity rule (level 12)
- High severity rule (level 10)
- Custom alert messages

**Current Placeholder:**
```markdown
[Full local_rules.xml with all severity levels](https://gist.github.com/williamzujkowski/wazuh-vulnerability-rules)
```

### 13. vulnerability-metrics-sql
**Description:** PostgreSQL queries (25 lines)
**Content:** Complete SQL analytics with:
- Vulnerability count by severity and date
- Mean time to remediate calculation
- Weekly trend analysis
- Historical comparison queries

**Current Placeholder:**
```markdown
[Full PostgreSQL queries for vulnerability tracking](https://gist.github.com/williamzujkowski/vulnerability-metrics-sql)
```

---

## Creation Instructions

1. **Extract Code:** Get original code blocks from pre-optimization version of post
2. **Create Gists:** For each gist, create a new GitHub gist under williamzujkowski account
3. **Update Links:** Replace placeholder URLs with actual gist URLs
4. **Verify:** Ensure all gist links are public and accessible
5. **Test:** Click each link to confirm it loads the expected content

## Alternative Approach

Instead of creating individual gists, consider:
- **Single repository:** Create `blog-code-examples` repo with organized directories
- **Better versioning:** Track changes over time with git history
- **Easier maintenance:** Update multiple files in one commit
- **Better discoverability:** All examples in one place

**Example Structure:**
```
blog-code-examples/
├── security-scanning/
│   ├── workflows/
│   │   ├── security-scan.yml
│   │   ├── scheduled-scan.yml
│   │   ├── sbom-scan.yml
│   │   └── auto-remediate.yml
│   ├── configs/
│   │   ├── .grype.yaml
│   │   ├── osv-scanner.toml
│   │   └── security.rego
│   ├── scripts/
│   │   ├── compare-scans.py
│   │   └── send-scans-to-wazuh.sh
│   └── integrations/
│       ├── slack-notification.yml
│       ├── wazuh-rules.xml
│       └── tasks.json
└── README.md
```

This approach would change gist links to repository file links:
```markdown
[Complete workflow](https://github.com/williamzujkowski/blog-code-examples/blob/main/security-scanning/workflows/security-scan.yml)
```

---

**Next Action:** Decide on gists vs repository approach, then create/populate code examples.
