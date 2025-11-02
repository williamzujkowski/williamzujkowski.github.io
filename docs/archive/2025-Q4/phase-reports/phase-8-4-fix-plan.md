# Phase 8.4 Fix Plan: Code Ratio Reduction

**Date:** 2025-10-31
**Target:** Reduce code ratio from 82%/84% to <25%
**Posts:** 2 (security-scanning, mitre-dashboard)

---

## Post 1: Automated Security Scanning Pipeline

**Current State:**
- Code ratio: 82% (433/528 lines)
- Target ratio: <25% (max 132 code lines)
- **Required reduction:** 301 code lines

### Code Blocks Analysis

#### 1. GitHub Actions Workflow (Lines 163-164 region)
**Status:** ✅ Gist link present
**Issue:** Full 109-line YAML workflow still inline
**Location:** Lines 169-177 (snippet visible, full workflow likely below)
**Action:**
- ✅ Keep: 5-line snippet showing Slack notification job
- ❌ Remove: Full workflow (assumed ~100 lines based on validation report)
- Gist URL already present: `https://gist.github.com/williamzujkowski/security-scan-workflow-complete`

#### 2. Pre-Commit Hooks (Lines 188-210)
**Status:** ⚠️ No gist link
**Code block:** YAML configuration (23 lines)
**Action:**
- Create gist: `pre-commit-security-scans.yaml`
- Replace with: 3-5 line snippet showing single hook
- Add gist link

#### 3. VS Code Tasks (Lines 228-239)
**Status:** ✅ Gist link present (line 244)
**Code block:** JSON excerpt (12 lines)
**Action:**
- ✅ Keep: Current excerpt (already minimal)
- Verify gist link works

#### 4. Grype Configuration (Lines 252-262)
**Status:** ⚠️ Partial gist reference (line 266)
**Code block:** YAML (11 lines)
**Action:**
- Create gist: `grype-config.yaml`
- Replace with: 3-4 line snippet showing ignore rule
- Verify gist URL

#### 5. OSV-Scanner Configuration (Lines 272-279)
**Status:** ⚠️ Partial gist reference (line 283)
**Code block:** TOML (8 lines)
**Action:**
- Create gist: `osv-scanner.toml`
- Replace with: 2-3 line snippet showing key settings
- Verify gist URL

#### 6. Trivy OPA Policy (Lines 289-299)
**Status:** ⚠️ Partial gist reference (line 304)
**Code block:** Rego rules (11 lines)
**Action:**
- Create gist: `trivy-security-policy.rego`
- Replace with: 3-4 line snippet showing deny rule
- Verify gist URL

#### 7. Scheduled Scan Workflow (Lines 313-331)
**Status:** ⚠️ Partial gist reference (line 335)
**Code block:** YAML (19 lines)
**Action:**
- Create gist: `scheduled-security-scans.yml`
- Replace with: 4-5 line snippet showing cron schedule
- Verify gist URL

#### 8. Scan Comparison Script (Lines 341-352)
**Status:** ⚠️ Partial gist reference (line 357)
**Code block:** Python (12 lines)
**Action:**
- Create gist: `compare-security-scans.py`
- Replace with: 3-4 line snippet showing core comparison logic
- Verify gist URL

#### 9. SBOM Generation (Lines 363-373)
**Status:** ⚠️ No gist link
**Code block:** Bash commands (11 lines)
**Action:**
- Create gist: `sbom-generation-workflow.yml`
- Replace with: 2-3 line snippet showing Syft command
- Add gist link

#### 10. SBOM Workflow (Lines 382-395)
**Status:** ⚠️ Partial gist reference (line 400)
**Code block:** YAML (14 lines)
**Action:**
- Create gist: `sbom-workflow.yml`
- Replace with: 3-4 line snippet
- Verify gist URL

#### 11. Auto-Remediation Workflow (Lines 408-422)
**Status:** ⚠️ Partial gist reference (line 427)
**Code block:** YAML (15 lines)
**Action:**
- Create gist: `auto-remediate-vulnerabilities.yml`
- Replace with: 3-4 line snippet
- Verify gist URL

#### 12. Wazuh Integration Script (Lines 436-449)
**Status:** ⚠️ Partial gist reference (line 452)
**Code block:** Bash (14 lines)
**Action:**
- Create gist: `send-scans-to-wazuh.sh`
- Replace with: 3-4 line snippet
- Verify gist URL

#### 13. Wazuh Rules (Lines 458-469)
**Status:** ⚠️ Partial gist reference (line 474)
**Code block:** XML (12 lines)
**Action:**
- Create gist: `wazuh-vulnerability-rules.xml`
- Replace with: 3-4 line snippet
- Verify gist URL

#### 14. SQL Metrics (Lines 518-527)
**Status:** ⚠️ Partial gist reference (line 533)
**Code block:** SQL (10 lines)
**Action:**
- Create gist: `vulnerability-metrics.sql`
- Replace with: 2-3 line snippet showing trend query
- Verify gist URL

### Mermaid Diagrams
**Keep all Mermaid diagrams** - They're visual, not code:
- Lines 35-94: Architecture diagram ✅
- Lines 141-152: Pipeline flow ✅

### Installation Commands
**Lines 116-131:** Basic installation commands
**Action:** ✅ Keep - Essential for setup (16 lines acceptable)

### Bash Examples
**Lines 363-373, 436-449:** Operational commands
**Action:** Reduce to 2-3 line snippets, move full scripts to gists

---

## Expected Outcome (Post 1)

**Before:**
- Total lines: 528
- Code lines: 433
- Ratio: 82%

**After:**
- Total lines: ~200 (reduced prose during cleanup)
- Code lines: ~60 (snippets only)
- Ratio: ~30% (still need prose reduction)
- Target: <25% requires additional prose expansion OR further code reduction

**Code reduction breakdown:**
- Removed: ~370 lines (moved to gists)
- Kept: ~60 lines (essential snippets + Mermaid diagrams)

---

## Post 2: MITRE ATT&CK Dashboard

**Current State:**
- Code ratio: 84% (284/338 lines)
- Target ratio: <25% (max 85 code lines)
- **Required reduction:** 199 code lines

### Issues Identified
❌ **NO GIST LINKS FOUND** - Complete code extraction required

### Code Blocks to Extract

#### 1. ThreatIntelligenceDashboard Class (Lines 71-91)
**Code block:** Python class initialization (21 lines)
**Action:**
- Create gist: `threat-intelligence-dashboard.py`
- Replace with: 3-4 line snippet showing class structure
- Add gist link

#### 2. ATTACKDataLoader Class (Lines 98-139)
**Code block:** Python STIX data loading (42 lines)
**Action:**
- Create gist: `attack-data-loader.py`
- Replace with: 4-5 line snippet showing STIX query
- Add gist link

#### 3. AlienVault OTX Integration (Lines 149-178)
**Code block:** Python API integration (30 lines)
**Action:**
- Create gist: `alienvault-otx-collector.py`
- Replace with: 3-4 line snippet showing pulse fetching
- Add gist link

#### 4. CISA Alert Mapper (Lines 183-223)
**Code block:** Python vulnerability mapping (41 lines)
**Action:**
- Create gist: `cisa-alert-mapper.py`
- Replace with: 4-5 line snippet showing CVE mapping
- Add gist link

#### 5. Plotly Visualization (Lines 230-248)
**Code block:** Python visualization (19 lines)
**Action:**
- Create gist: `mitre-attack-visualizer.py`
- Replace with: 3-4 line snippet showing heatmap creation
- Add gist link

#### 6. Threat Actor Profiler (Lines 260-299)
**Code block:** Python actor profiling (40 lines)
**Action:**
- Create gist: `threat-actor-profiler.py`
- Replace with: 4-5 line snippet showing technique matching
- Add gist link

#### 7. Threat Alerting (Lines 306-356)
**Code block:** Python email alerting (51 lines)
**Action:**
- Create gist: `threat-alerting-system.py`
- Replace with: 4-5 line snippet showing alert creation
- Add gist link

#### 8. Main Dashboard Loop (Lines 363-398)
**Code block:** Python async main loop (36 lines)
**Action:**
- Create gist: `mitre-dashboard-main.py`
- Replace with: 4-5 line snippet showing collection loop
- Add gist link

### Mermaid Diagrams
**Keep all Mermaid diagrams** - Visual representation:
- Lines 44-57: ATT&CK matrix flow ✅

### Expected Outcome (Post 2)

**Before:**
- Total lines: 338
- Code lines: 284
- Ratio: 84%

**After:**
- Total lines: ~150 (reduced code, maintained prose)
- Code lines: ~35 (snippets only)
- Ratio: ~23% ✅ MEETS TARGET

**Code reduction breakdown:**
- Removed: ~250 lines (moved to 8 gists)
- Kept: ~35 lines (essential snippets + Mermaid)

---

## Implementation Checklist

### Phase 2A: Create GitHub Gists

**Post 1 (14 gists):**
- [ ] `security-scan-workflow-complete.yml` (verify exists)
- [ ] `security-scan-slack-notification.yml` (verify exists)
- [ ] `vscode-security-scan-tasks.json` (verify exists)
- [ ] `pre-commit-security-scans.yaml`
- [ ] `grype-config.yaml`
- [ ] `osv-scanner.toml`
- [ ] `trivy-security-policy.rego`
- [ ] `scheduled-security-scans.yml`
- [ ] `compare-security-scans.py`
- [ ] `sbom-generation-workflow.yml`
- [ ] `auto-remediate-vulnerabilities.yml`
- [ ] `send-scans-to-wazuh.sh`
- [ ] `wazuh-vulnerability-rules.xml`
- [ ] `vulnerability-metrics.sql`

**Post 2 (8 gists):**
- [ ] `threat-intelligence-dashboard.py`
- [ ] `attack-data-loader.py`
- [ ] `alienvault-otx-collector.py`
- [ ] `cisa-alert-mapper.py`
- [ ] `mitre-attack-visualizer.py`
- [ ] `threat-actor-profiler.py`
- [ ] `threat-alerting-system.py`
- [ ] `mitre-dashboard-main.py`

### Phase 2B: Update Blog Posts

**For each code block:**
1. Extract full code to gist
2. Create gist on github.com/williamzujkowski
3. Copy gist URL
4. Replace inline code block with:
   - 📎 emoji + gist link
   - 3-5 line essential snippet
   - "See full implementation" text

### Phase 2C: Validation

**Post-modification checks:**
- [ ] Run `npm run build` (must pass)
- [ ] Verify all gist links work (manual click-through)
- [ ] Calculate code ratio: `python /tmp/calculate_code_ratio.py [post]`
- [ ] Confirm: Post 1 <25%, Post 2 <25%
- [ ] Check Mermaid diagrams render
- [ ] Mobile preview (375px width)

---

## Gist Creation Template

**Filename pattern:** `<descriptive-name>.<ext>`
**Description:** "From blog post: [Post Title] - [Brief description]"
**Content:** Full implementation with comments
**Public visibility:** Yes

**Example:**
```
Filename: security-scan-workflow-complete.yml
Description: Complete GitHub Actions workflow for security scanning with Grype, OSV-Scanner, and Trivy - From blog post: Automated Security Scanning Pipeline
Content: [Full YAML workflow]
```

---

## Success Criteria

✅ Post 1: Code ratio <25% (currently 82%)
✅ Post 2: Code ratio <25% (currently 84%)
✅ All gist links functional
✅ Build passes without errors
✅ Mermaid diagrams render correctly
✅ Essential snippets preserved
✅ Technical accuracy maintained
✅ No content degradation

---

**Next Action:** Coder Agent to execute Phase 2A-2C
**Estimated Time:** 2 hours (gist creation + post updates + validation)
