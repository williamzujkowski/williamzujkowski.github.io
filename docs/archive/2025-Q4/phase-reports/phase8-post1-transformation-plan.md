# Post 1 Transformation Plan: Security Scanning Pipeline

**Target:** Reduce from 72% code → ~40% code (first pass)
**Method:** Replace 2 largest code blocks with essentials + diagrams

## Changes to Make

### Change 1: GitHub Actions Workflow (109 lines → 12 lines + diagram)

**Location:** Lines 140-249
**Current:** Full 109-line YAML workflow
**Replace with:**

```markdown
### GitHub Actions Integration

The pipeline integrates three scanners in parallel:

```mermaid
[Insert "Scanning Workflow" flowchart from templates]
```

Essential workflow structure:

```yaml
# .github/workflows/security-scan.yml
name: Security Scanning Pipeline

jobs:
  dependency-scan:    # OSV scanner for dependencies
  container-scan:     # Grype for container images
  comprehensive-scan: # Trivy for comprehensive analysis
  security-gate:      # Quality gate with blocking

# Full workflow with SARIF uploads and alerting:
# https://gist.github.com/[UPLOAD_full-workflow.yml]
```
```

**Impact:** -97 lines

### Change 2: Python Comparison Script (59 lines → 10 lines + note)

**Location:** Lines 507-567
**Current:** Full 59-line Python script
**Replace with:**

```markdown
### Scan Comparison Script

```python
# scripts/compare-scans.py
def compare_scans(current_file, baseline_file):
    """Compare vulnerability scans and report differences"""
    current_vulns = extract_vulnerabilities(current)
    baseline_vulns = extract_vulnerabilities(baseline)

    new_vulns = current_vulns - baseline_vulns
    fixed_vulns = baseline_vulns - current_vulns
    # Alert if new vulnerabilities found

# Full script with JSON parsing and reporting:
# https://gist.github.com/[UPLOAD_compare-scans.py]
```
```

**Impact:** -49 lines

## Optional Enhancements (Future Iteration)

### Add "Security Scanning Architecture" diagram
- Location: After line 96 (after existing Mermaid)
- Source: diagram_templates/2025-10-06-automated-security-scanning-pipeline_diagrams.md
- Shows: Grype → OSV → Wazuh → Alerting flow

### Add "Severity Classification" diagram
- Location: After severity discussion section
- Shows: CVSS/EPSS/KEV routing logic

### Reduce other large blocks
- Block 12: 44-line scheduled workflow
- Block 15: 38-line SBOM workflow
- Block 16: 47-line auto-remediate workflow

## Expected Results

### Before:
- Total lines: 854
- Code blocks: 19
- Largest blocks: 109, 59, 47, 44, 38 lines
- Code ratio: 72%

### After (First Pass):
- Total lines: ~708 (-146 lines)
- Code blocks: 19 (same count, smaller size)
- Largest blocks: 47, 44, 38, 37, 27 lines
- **Estimated code ratio: ~45%** (-27 percentage points)

### After (Full Enhancement):
- Add 2-3 Mermaid diagrams (+150 lines of visual content)
- Reduce 3 more blocks (-90 lines)
- **Target code ratio: ~28%** (-44 percentage points total)

## Implementation Steps

1. ✅ Extract code to gists directory
2. ✅ Create this transformation plan
3. ⏭️ Update blog post with Change 1
4. ⏭️ Update blog post with Change 2
5. ⏭️ Test build
6. ⏭️ Commit if passing
7. ⏭️ Upload gists to GitHub
8. ⏭️ Update gist URLs in post
9. ⏭️ Second iteration: add diagrams + reduce more code

## Files Ready

- ✅ `code-examples/security-scanning/full-workflow.yml`
- ✅ `code-examples/security-scanning/compare-scans.py`
- ✅ `code-examples/security-scanning/README.md`
- ✅ `diagram_templates/2025-10-06-automated-security-scanning-pipeline_diagrams.md`

## Manual Steps (User)

1. Upload code-examples to GitHub gists:
   ```bash
   cd code-examples/security-scanning
   gh gist create full-workflow.yml --public
   gh gist create compare-scans.py --public
   ```

2. Copy gist URLs and update placeholders in blog post

3. Review and approve changes before final commit

---

**Status:** Ready for implementation
**Risk:** Low (only 2 changes, well-documented)
**Estimated time:** 10-15 minutes
**Rollback:** Git revert if needed
