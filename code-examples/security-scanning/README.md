# Security Scanning Pipeline - Full Code Examples

This directory contains the complete code referenced in the blog post:
**"Automated Security Scanning Pipeline with Grype and OSV"**

## Files

### 1. `full-workflow.yml`
Complete GitHub Actions workflow (109 lines) demonstrating:
- OSV dependency scanning
- Grype container scanning
- Trivy comprehensive scanning
- SARIF report generation
- Security quality gates

**To use:**
1. Upload to GitHub gist
2. Copy gist URL
3. Reference in blog post

### 2. `compare-scans.py`
Python script (59 lines) for comparing vulnerability scan results:
- Load and parse scan JSON
- Extract vulnerability IDs
- Compare baseline vs current scans
- Report new and fixed vulnerabilities
- Alert on new findings

**To use:**
1. Upload to GitHub gist
2. Copy gist URL
3. Reference in blog post

## Upload Instructions

```bash
# Create gists using gh CLI
gh gist create full-workflow.yml --desc "Complete security scanning workflow"
gh gist create compare-scans.py --desc "Vulnerability scan comparison script"

# Or upload manually at: https://gist.github.com/
```

## Blog Post References

Replace the verbose code blocks in the blog post with:

**For full-workflow.yml (currently 109 lines):**
```yaml
# Essential structure only
name: Security Scanning Pipeline
jobs:
  dependency-scan:  # OSV scanner
  container-scan:   # Grype scanner
  comprehensive-scan: # Trivy scanner
  security-gate:    # Quality gate

# Full workflow: [GIST_URL_HERE]
```

**For compare-scans.py (currently 59 lines):**
```python
# Essential function signatures
def compare_scans(current_file, baseline_file):
    current_vulns = extract_vulnerabilities(current)
    baseline_vulns = extract_vulnerabilities(baseline)

    new_vulns = current_vulns - baseline_vulns
    fixed_vulns = baseline_vulns - current_vulns

    # Report and alert if new vulnerabilities found
    # Full script: [GIST_URL_HERE]
```

## Note

These code examples are extracted to reduce the code-to-content ratio in the blog post from 72% to ~28%, improving readability while maintaining technical depth through gist references.
