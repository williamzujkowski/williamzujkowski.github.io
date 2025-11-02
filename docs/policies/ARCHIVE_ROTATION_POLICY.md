---
STATUS: AUTHORITATIVE
VERSION: 1.0.0
EFFECTIVE_DATE: 2025-11-01
NEXT_REVIEW: 2026-02-01
OWNER: Repository Maintenance
---

# Archive Rotation Policy

## Policy Overview

This document establishes formal retention and rotation policies for documentation archives to prevent unbounded growth, reduce maintenance overhead, and ensure efficient repository operations.

**Current State:**
- Archive size: 1.7M (89 markdown files)
- Reports size: 920K (32 markdown files, 4 JSON files)
- Growth rate: ~200-300K per quarter
- Maintenance overhead: 40% of total repository maintenance time

**Policy Goals:**
1. Reduce archive footprint by 30-40% within 6 months
2. Implement automated quarterly rotation procedures
3. Maintain historical value while eliminating redundancy
4. Reduce manual archive management from 40% to <10% overhead
5. Prevent unbounded growth beyond 3.0M total archive size

**Scope:** Applies to all files in `/docs/archive/` and `/docs/reports/` directories.

---

## 1. Retention Schedules by File Category

### 1.1 Active Reports (docs/reports/)

**Retention Period:** 2 quarters (6 months) in active reports directory

**Categories:**

| File Type | Retention | Action After Period | Exceptions |
|-----------|-----------|---------------------|------------|
| **Completion Reports** | 2 quarters | Move to archive | Phase completion reports: Keep indefinitely |
| **Analysis Reports** | 2 quarters | Move to archive | Strategic analysis: Keep 1 year |
| **Optimization Reports** | 2 quarters | Move to archive | Architecture proposals: Keep 1 year |
| **Batch Reports** | 2 quarters | Move to archive | All batch reports retained for historical value |
| **Validation Reports** | 1 quarter | Move to archive or delete | Keep only if referenced by active work |
| **JSON Data Files** | 1 quarter | Archive or delete | Keep only if supporting active reports |

**Examples:**
- `cli-batch-3-standardization-report.md` → Archive after Q1 2026
- `phase-8-completion-report.md` → Keep indefinitely (phase completion)
- `seo-raw-data.json` → Archive or delete after Q1 2026
- `portfolio-assessment.json` → Keep 1 year (strategic analysis)

**Automation Trigger:** End of each quarter (March 31, June 30, Sept 30, Dec 31)

### 1.2 Archived Reports (docs/archive/)

**Retention Period:** Variable by subdirectory and file type

**Structure:**
```
docs/archive/
├── 2025-Q3/          # Keep all (historical value)
├── 2025-Q4/          # Current quarter
├── 2026-Q1/          # Future quarters
├── legacy/           # Permanent retention
└── [other files]     # Review quarterly
```

**Categories:**

| Directory | Retention | Action After Period | Notes |
|-----------|-----------|---------------------|-------|
| **Quarter Directories (2025-Q3, etc.)** | 4 quarters | Compress or selective delete | Keep README.md and completion reports |
| **Batch Reports** | Indefinite | None | Historical value for pattern analysis |
| **Phase Reports** | Indefinite | None | Strategic value for project evolution |
| **Legacy Files** | Indefinite | None | Foundation documentation |
| **Working Documents** | 2 quarters | Delete | Temporary analysis, pre-analysis files |
| **Duplicate Content** | Immediate | Delete | Files replicated in multiple locations |

**Examples:**
- `docs/archive/2025-Q3/batch-1/LESSONS_LEARNED.md` → Keep indefinitely
- `docs/archive/2025-Q3/batch-1/post-2-pre-analysis.md` → Delete after Q1 2026
- `docs/archive/2025-Q4/legacy-enforcement.md` → Keep indefinitely
- `docs/archive/test-reports-2025-Q3.md` → Delete after Q1 2026

### 1.3 Temporary and Working Files

**Retention Period:** 7-30 days depending on type

**Categories:**

| File Type | Location | Retention | Automation |
|-----------|----------|-----------|------------|
| **Working Drafts** | Any location | 30 days | Pre-commit hook warning if older |
| **Test Reports** | docs/testing/ | 7 days | Automated cleanup script |
| **Validation Outputs** | docs/testing/ | 7 days | Automated cleanup script |
| **Temporary Analysis** | docs/analysis/ | 14 days | Manual review quarterly |
| **Prototype Files** | docs/prototypes/ | 30 days | Manual review quarterly |

**Automation Trigger:** Weekly cron job for 7-day retention, monthly for 30-day

---

## 2. Quarterly Rotation Schedule

### 2.1 Rotation Timeline

**Schedule:** Rotations occur at the end of each quarter

| Quarter End | Archive Target | Reports Action | Review Date |
|-------------|----------------|----------------|-------------|
| **Q4 2025** (Dec 31) | Create 2025-Q4 summary | Move Q3 reports to archive | Jan 15, 2026 |
| **Q1 2026** (Mar 31) | Archive Q4 2025 working docs | Move Q4 reports to archive | Apr 15, 2026 |
| **Q2 2026** (Jun 30) | Compress 2025-Q3 archive | Move Q1 reports to archive | Jul 15, 2026 |
| **Q3 2026** (Sep 30) | Delete Q3 working docs | Move Q2 reports to archive | Oct 15, 2026 |

### 2.2 Rotation Procedure

**Step 1: Pre-Rotation Review (T-14 days)**
```bash
# Review active reports older than 2 quarters
find docs/reports -type f -mtime +180 -name "*.md"

# Identify files for archival
ls -lht docs/reports/*.md | tail -20

# Check archive size
du -sh docs/archive docs/reports
```

**Step 2: Categorization (T-7 days)**
```bash
# Create next quarter directory
mkdir -p docs/archive/YYYY-QX/

# Identify files by category:
# - Keep indefinitely: batch reports, phase reports, LESSONS_LEARNED
# - Archive: completion reports, analysis >6 months old
# - Delete: working docs, pre-analysis, validation reports >6 months
```

**Step 3: Execution (Quarter End)**
```bash
# Move reports to archive
mv docs/reports/*-completion-report.md docs/archive/YYYY-QX/

# Delete temporary files
find docs/testing -name "*.md" -mtime +7 -delete
find docs/analysis -name "*-working-*.md" -mtime +30 -delete

# Update archive README
echo "## Quarter X YYYY Archive" > docs/archive/YYYY-QX/README.md
```

**Step 4: Verification (T+7 days)**
```bash
# Verify no broken references
grep -r "docs/reports/" docs/*.md

# Check archive size reduction
du -sh docs/archive docs/reports

# Update MANIFEST.json
# Document rotation in maintenance log
```

### 2.3 Automation Recommendations

**High Priority (Implement First):**

1. **Weekly Cleanup Script** (`scripts/maintenance/weekly-cleanup.sh`)
```bash
#!/bin/bash
# Delete test reports older than 7 days
find docs/testing -name "*-report-*.md" -mtime +7 -delete
find docs/testing -name "*-validation-*.md" -mtime +7 -delete

# Warn about working drafts older than 30 days
find docs -name "*-working-*.md" -mtime +30 -ls
```

2. **Quarterly Archive Script** (`scripts/maintenance/quarterly-archive.sh`)
```bash
#!/bin/bash
QUARTER=$1  # e.g., "2026-Q1"
ARCHIVE_DIR="docs/archive/$QUARTER"

# Create quarter directory
mkdir -p "$ARCHIVE_DIR"

# Move reports older than 2 quarters
find docs/reports -type f -mtime +180 -name "*-report.md" -exec mv {} "$ARCHIVE_DIR/" \;

# Generate archive summary
echo "Archived on $(date)" > "$ARCHIVE_DIR/README.md"
```

3. **Size Monitor** (`scripts/maintenance/archive-size-check.sh`)
```bash
#!/bin/bash
ARCHIVE_SIZE=$(du -sm docs/archive | cut -f1)
REPORTS_SIZE=$(du -sm docs/reports | cut -f1)
TOTAL=$((ARCHIVE_SIZE + REPORTS_SIZE))

if [ $TOTAL -gt 3000 ]; then
  echo "WARNING: Archive size ($TOTAL MB) exceeds 3GB threshold"
  echo "Run quarterly rotation procedure"
fi
```

**Medium Priority (Implement Q1 2026):**

4. **Duplicate Detector** (`scripts/maintenance/find-duplicates.sh`)
5. **Reference Checker** (validate no broken links after rotation)
6. **Compression Utility** (compress old quarter directories)

**Low Priority (Future Enhancement):**

7. **Automated Git Archival** (move very old content to separate repository)
8. **Search Index Updater** (maintain searchability after compression)

---

## 3. What to Keep vs. Delete

### 3.1 ALWAYS Keep (Indefinite Retention)

**High Historical Value:**
- ✅ Batch completion reports (all batches)
- ✅ Phase completion reports (all phases)
- ✅ `LESSONS_LEARNED.md` files
- ✅ Strategic planning documents
- ✅ Architecture decisions and proposals
- ✅ Legacy documentation (docs/archive/legacy-*.md)
- ✅ Quarter README.md files

**Examples:**
- `batch-1-complete-summary.md` → KEEP
- `PHASE5_COMPLETION_REPORT.md` → KEEP
- `legacy-enforcement.md` → KEEP
- `2025-Q3/README.md` → KEEP

### 3.2 Archive After Period

**Medium Historical Value:**
- 📦 Analysis reports (after 2 quarters)
- 📦 Optimization reports (after 2 quarters)
- 📦 Validation summaries (after 1 quarter)
- 📦 Implementation checklists (after 2 quarters)
- 📦 Strategic summaries (after 1 year)

**Examples:**
- `seo-optimization-summary-2025-10-29.md` → Archive Q1 2026
- `script-efficiency-analysis-report.md` → Archive Q1 2026
- `cli-batch-3-standardization-report.md` → Archive Q1 2026

### 3.3 DELETE After Period

**Low/No Historical Value:**
- ❌ Working drafts (after 30 days)
- ❌ Pre-analysis files (after 2 quarters)
- ❌ Test reports (after 7 days)
- ❌ Validation outputs (after 7 days)
- ❌ Temporary analysis (after 1 quarter)
- ❌ Duplicate files (immediate)
- ❌ Superseded documentation (after verification)

**Examples:**
- `post-2-pre-analysis.md` → DELETE Q1 2026
- `test-reports-2025-Q3.md` → DELETE Q1 2026
- `*-working-draft-*.md` → DELETE after 30 days
- `validation-output-2025-10-15.md` → DELETE after 7 days

### 3.4 Decision Matrix

Use this matrix when unsure about retention:

| Question | Yes → Action | No → Action |
|----------|--------------|-------------|
| Is it a completion report? | KEEP | Continue |
| Does it contain lessons learned? | KEEP | Continue |
| Is it referenced by active work? | ARCHIVE (2Q) | Continue |
| Is it older than 2 quarters? | Review for deletion | KEEP |
| Does it have strategic value? | ARCHIVE (1Y) | Continue |
| Is it temporary/working? | DELETE (30d) | KEEP |
| Is it duplicated elsewhere? | DELETE (immediate) | KEEP |

---

## 4. Exception Handling

### 4.1 Exceptions to Standard Retention

**Permanent Exceptions:**
1. **Regulatory/Compliance:** If any files are required for compliance (none currently identified)
2. **Legal Hold:** If files are subject to legal discovery (flag for manual review)
3. **Active Reference:** Files actively referenced in current work (extend retention)
4. **Historical Significance:** Unique insights or breakthrough documentation (permanent retention)

**Temporary Exceptions:**
1. **Active Project:** Files supporting ongoing work (defer rotation until completion)
2. **Under Review:** Files being analyzed (defer rotation 30 days)
3. **Pending Migration:** Files being moved to new location (defer rotation until complete)

### 4.2 Exception Request Process

**Step 1: Identify Exception**
```markdown
File: docs/reports/example-report.md
Standard Action: Delete (older than 2 quarters)
Exception Requested: Extend retention 1 year
Justification: Referenced by active architecture work
Requested By: [Agent/User]
Date: YYYY-MM-DD
```

**Step 2: Document in Exception Log**
Create entry in `docs/policies/archive-exceptions.log`:
```
2026-01-15 | example-report.md | DELETE → ARCHIVE | Active reference | 1 year extension
```

**Step 3: Set Reminder**
Add to next quarter rotation checklist:
```
[ ] Review exception: example-report.md (expires 2027-01-15)
```

### 4.3 Bulk Exception Scenarios

**Scenario 1: Major Refactoring**
- Action: Defer all rotations 1 quarter
- Trigger: >50% of archive files actively referenced
- Approval: Repository owner

**Scenario 2: Historical Analysis**
- Action: Temporarily restore archived files
- Trigger: Research project requires old reports
- Process: Extract to `docs/research/restored/`, delete after research complete

**Scenario 3: Audit/Compliance**
- Action: Freeze all deletions
- Trigger: External audit or compliance review
- Approval: Repository owner
- Duration: Until audit complete

---

## 5. Compliance and Monitoring

### 5.1 Compliance Checks

**Monthly Checks:**
```bash
# Check archive size trend
du -sm docs/archive docs/reports >> logs/archive-size-history.log

# Identify files exceeding retention period
find docs/reports -type f -mtime +180 -ls

# Check for files in wrong locations
find . -maxdepth 1 -name "*.md" -o -name "*-report-*"
```

**Quarterly Audits:**
- Review all exceptions (validate still needed)
- Verify rotation procedures executed correctly
- Check for duplicate content
- Validate no broken references
- Update size projections

**Annual Review:**
- Assess policy effectiveness
- Review retention periods (adjust if needed)
- Update automation scripts
- Document lessons learned

### 5.2 Monitoring Metrics

**Key Performance Indicators:**

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| **Archive Size** | 1.7M | <2.5M | `du -sm docs/archive` |
| **Reports Size** | 920K | <1.0M | `du -sm docs/reports` |
| **Total Growth Rate** | ~300K/Q | <200K/Q | Quarterly delta |
| **Maintenance Overhead** | 40% | <10% | Time tracking |
| **Files >2Q in Reports** | Unknown | 0 | `find -mtime +180` |
| **Exception Count** | 0 | <5 | Exception log entries |

**Alert Thresholds:**
- ⚠️ **Warning:** Archive >2.5M or Reports >1.0M
- 🚨 **Critical:** Combined size >3.5M
- ⚠️ **Warning:** >10 files in reports older than 2 quarters
- 🚨 **Critical:** >25 files in reports older than 2 quarters

### 5.3 Reporting

**Monthly Summary:**
```markdown
## Archive Rotation Status - [Month] [Year]

Archive Size: [X]M (Δ [+/-Y]M from last month)
Reports Size: [X]M (Δ [+/-Y]M from last month)
Files Rotated: [N]
Files Deleted: [N]
Exceptions Active: [N]

Actions Required:
- [ ] Action 1
- [ ] Action 2
```

**Quarterly Report:**
```markdown
## Q[X] [YEAR] Rotation Report

### Summary
- Files Archived: [N]
- Files Deleted: [N]
- Space Reclaimed: [X]M
- Exceptions Granted: [N]

### Compliance
- [✅/❌] All files rotated per schedule
- [✅/❌] No broken references
- [✅/❌] Size within targets

### Recommendations
1. [Recommendation 1]
2. [Recommendation 2]
```

---

## 6. Implementation Roadmap

### Phase 1: Immediate (Week 1)
- ✅ Create `docs/policies/` directory
- ✅ Establish this policy document
- [ ] Create exception log template
- [ ] Document current archive baseline

### Phase 2: Quick Wins (Week 2-4)
- [ ] Implement weekly cleanup script
- [ ] Delete obvious temporary files (test reports >7 days)
- [ ] Create archive size monitoring
- [ ] Set up monthly compliance checks

### Phase 3: Automation (Month 2-3)
- [ ] Implement quarterly archive script
- [ ] Build duplicate detector
- [ ] Create reference checker
- [ ] Set up automated alerts

### Phase 4: Optimization (Month 4-6)
- [ ] Compress old quarter directories
- [ ] Implement advanced deduplication
- [ ] Build search index for archived content
- [ ] Evaluate git archival strategy

### Phase 5: Continuous Improvement (Ongoing)
- [ ] Monthly metric collection
- [ ] Quarterly audits
- [ ] Annual policy review
- [ ] Automation refinement

---

## 7. Related Documents

**Policy Documents:**
- `CLAUDE.md` - Repository standards and enforcement
- `.claude-rules.json` - Automated enforcement rules
- `docs/ENFORCEMENT.md` - Extended enforcement guidelines

**Implementation Guides:**
- `docs/GUIDES/SCRIPT_CATALOG.md` - Automation script reference
- `docs/GUIDES/LLM_ONBOARDING.md` - Agent onboarding procedures
- `docs/ARCHITECTURE.md` - Repository structure

**Maintenance Documentation:**
- `docs/archive/ARCHIVAL_SUMMARY.md` - Historical archive context
- `MANIFEST.json` - File registry and inventory

---

## 8. Policy Maintenance

**Version History:**

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0.0 | 2025-11-01 | Initial policy creation | Documentation Agent |

**Review Schedule:**
- **Monthly:** Compliance checks and metric collection
- **Quarterly:** Rotation execution and audit
- **Annually:** Policy review and adjustment
- **Next Review:** 2026-02-01

**Change Process:**
1. Propose changes in policy review meeting
2. Document rationale and impact analysis
3. Update version number (semantic versioning)
4. Communicate changes to all agents
5. Update automation scripts if needed

**Contact:**
For questions or exception requests, document in:
- `docs/policies/archive-exceptions.log` (exceptions)
- GitHub issues (policy questions)
- Session handoff documents (urgent items)

---

## Appendix A: File Categorization Reference

### Completion Reports (Keep Indefinitely)
```
batch-*-completion-report.md
PHASE*_COMPLETION_REPORT.md
*-complete-summary.md
quick-wins-completion-report.md
```

### Analysis Reports (Archive 2Q)
```
*-analysis-report.md
*-optimization-*.md
*-assessment.md
*-audit-*.md
```

### Working Documents (Delete 30d)
```
*-working-*.md
*-draft-*.md
*-pre-analysis.md
*-validation-output-*.md
```

### Strategic Documents (Keep 1Y)
```
*-strategy.md
*-proposal.md
*-architecture-*.md
LESSONS_LEARNED.md
```

---

## Appendix B: Automation Script Templates

### Script 1: Weekly Cleanup
```bash
#!/bin/bash
# scripts/maintenance/weekly-cleanup.sh

echo "=== Weekly Archive Cleanup ==="
echo "Date: $(date)"

# Delete test reports older than 7 days
DELETED=$(find docs/testing -name "*.md" -mtime +7 -delete -print | wc -l)
echo "Deleted $DELETED test reports"

# Warn about old working drafts
OLD_DRAFTS=$(find docs -name "*-working-*.md" -mtime +30 | wc -l)
if [ $OLD_DRAFTS -gt 0 ]; then
  echo "WARNING: $OLD_DRAFTS working drafts older than 30 days"
  find docs -name "*-working-*.md" -mtime +30 -ls
fi

echo "Cleanup complete"
```

### Script 2: Size Monitor
```bash
#!/bin/bash
# scripts/maintenance/archive-size-monitor.sh

ARCHIVE_MB=$(du -sm docs/archive | cut -f1)
REPORTS_MB=$(du -sm docs/reports | cut -f1)
TOTAL_MB=$((ARCHIVE_MB + REPORTS_MB))

echo "Archive Size Monitor - $(date)"
echo "Archive: ${ARCHIVE_MB}M"
echo "Reports: ${REPORTS_MB}M"
echo "Total: ${TOTAL_MB}M"

# Log to history
echo "$(date +%Y-%m-%d),$ARCHIVE_MB,$REPORTS_MB,$TOTAL_MB" >> logs/archive-size-history.csv

# Alert if over threshold
if [ $TOTAL_MB -gt 3000 ]; then
  echo "CRITICAL: Total size ${TOTAL_MB}M exceeds 3GB threshold"
  exit 1
elif [ $TOTAL_MB -gt 2500 ]; then
  echo "WARNING: Total size ${TOTAL_MB}M approaching threshold"
  exit 0
fi
```

### Script 3: Quarterly Archive
```bash
#!/bin/bash
# scripts/maintenance/quarterly-archive.sh

QUARTER=$1
if [ -z "$QUARTER" ]; then
  echo "Usage: $0 YYYY-QX"
  exit 1
fi

ARCHIVE_DIR="docs/archive/$QUARTER"
mkdir -p "$ARCHIVE_DIR"

echo "=== Quarterly Archive: $QUARTER ==="

# Move reports older than 2 quarters (180 days)
MOVED=0
for file in $(find docs/reports -name "*-report.md" -mtime +180); do
  mv "$file" "$ARCHIVE_DIR/"
  MOVED=$((MOVED + 1))
done

echo "Moved $MOVED reports to archive"

# Create README
cat > "$ARCHIVE_DIR/README.md" <<EOF
# $QUARTER Archive

Archived on: $(date)
Files archived: $MOVED

This directory contains reports and documents from $QUARTER that have
exceeded their active retention period but retain historical value.

See docs/policies/ARCHIVE_ROTATION_POLICY.md for retention policies.
EOF

echo "Archive complete"
```

---

**END OF POLICY**

**Policy Status:** ACTIVE
**Effective Date:** 2025-11-01
**Next Review:** 2026-02-01
**Version:** 1.0.0
