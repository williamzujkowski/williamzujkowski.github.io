# Archive Rotation Policy Implementation Checklist

**Policy Document:** docs/policies/ARCHIVE_ROTATION_POLICY.md
**Created:** 2025-11-01
**Target Completion:** 2026-01-31

## Phase 1: Immediate (Week 1) ✅

- [x] Create `docs/policies/` directory
- [x] Establish policy document
- [x] Create exception log template
- [x] Document current archive baseline

**Completion Status:** 4/4 complete

## Phase 2: Quick Wins (Week 2-4)

### 2.1 Manual Cleanup
- [ ] Delete test reports older than 7 days
  ```bash
  find docs/testing -name "*.md" -mtime +7 -delete
  ```

- [ ] Identify and flag working drafts older than 30 days
  ```bash
  find docs -name "*-working-*.md" -mtime +30 -ls
  ```

- [ ] Review and delete obvious duplicates
  ```bash
  # Manual review recommended
  ls -lh docs/archive/test-reports-2025-Q3.md
  ```

### 2.2 Monitoring Setup
- [ ] Create `logs/` directory for monitoring
  ```bash
  mkdir -p logs
  ```

- [ ] Establish size tracking baseline
  ```bash
  echo "date,archive_mb,reports_mb,total_mb" > logs/archive-size-history.csv
  du -sm docs/archive docs/reports | awk '{print $1}' | paste -sd, >> logs/archive-size-history.csv
  ```

- [ ] Create monthly compliance check reminder
  - Add to calendar: 1st of each month

### 2.3 Script Creation
- [ ] Create `scripts/maintenance/` directory
  ```bash
  mkdir -p scripts/maintenance
  ```

- [ ] Implement `weekly-cleanup.sh` (see Appendix B)
  - Location: `scripts/maintenance/weekly-cleanup.sh`
  - Make executable: `chmod +x scripts/maintenance/weekly-cleanup.sh`
  - Test run: `./scripts/maintenance/weekly-cleanup.sh`

- [ ] Implement `archive-size-monitor.sh` (see Appendix B)
  - Location: `scripts/maintenance/archive-size-monitor.sh`
  - Make executable: `chmod +x scripts/maintenance/archive-size-monitor.sh`
  - Add to cron: Weekly execution

**Target Completion:** 2025-11-15

## Phase 3: Automation (Month 2-3)

### 3.1 Quarterly Archive Script
- [ ] Implement `quarterly-archive.sh` (see Appendix B)
  - Location: `scripts/maintenance/quarterly-archive.sh`
  - Test with dry-run flag
  - Schedule for quarter-end execution

### 3.2 Duplicate Detection
- [ ] Build duplicate detector
  ```bash
  # Script to find files with identical content
  find docs/archive -type f -exec md5sum {} \; | sort | uniq -w32 -D
  ```

- [ ] Create duplicate resolution workflow
  - Compare file dates
  - Check references
  - Delete older duplicate or less authoritative version

### 3.3 Reference Checking
- [ ] Create reference checker script
  ```bash
  # Check for broken links after rotation
  grep -r "docs/reports/" docs/*.md
  grep -r "docs/archive/" docs/*.md
  ```

- [ ] Build automated reference validator
  - Parse all markdown links
  - Verify file existence
  - Report broken references

### 3.4 Alert System
- [ ] Set up size threshold alerts
  - Warning: >2.5M total
  - Critical: >3.5M total

- [ ] Create rotation reminder notifications
  - 2 weeks before quarter end
  - 1 week before quarter end
  - Quarter end execution reminder

**Target Completion:** 2026-01-31

## Phase 4: Optimization (Month 4-6)

### 4.1 Compression
- [ ] Evaluate compression tools
  - tar.gz for old quarter directories
  - Maintain searchability

- [ ] Implement selective compression
  - Compress 2025-Q3 (after Q1 2026)
  - Keep current and previous quarter uncompressed

### 4.2 Advanced Deduplication
- [ ] Build intelligent deduplication
  - Content-based comparison
  - Preserve best version (most complete, most recent)
  - Update references automatically

### 4.3 Search Indexing
- [ ] Build search index for archived content
  - Index before compression
  - Maintain searchability after archival

### 4.4 Git Archival Strategy
- [ ] Evaluate separate archive repository
  - Move very old content (>2 years)
  - Maintain git history
  - Link from main repository

**Target Completion:** 2026-04-30

## Phase 5: Continuous Improvement (Ongoing)

### 5.1 Monthly Tasks
- [ ] Collect size metrics (1st of month)
  ```bash
  ./scripts/maintenance/archive-size-monitor.sh
  ```

- [ ] Run compliance checks
  ```bash
  # Files exceeding retention in reports/
  find docs/reports -type f -mtime +180 -ls
  ```

- [ ] Update baseline tracking document

### 5.2 Quarterly Tasks
- [ ] Execute rotation procedure (quarter end)
  ```bash
  ./scripts/maintenance/quarterly-archive.sh YYYY-QX
  ```

- [ ] Audit exceptions (review all active exceptions)
- [ ] Verify no broken references
- [ ] Generate quarterly report

### 5.3 Annual Tasks
- [ ] Policy review (2026-02-01, then yearly)
- [ ] Assess automation effectiveness
- [ ] Update retention periods if needed
- [ ] Document lessons learned

**Status:** Not yet started (begins 2025-12-01)

---

## Quick Start: First Week Actions

For immediate implementation, complete these tasks in order:

**Day 1:**
1. ✅ Review this checklist
2. ✅ Read full policy document
3. ✅ Verify baseline metrics

**Day 2-3:**
1. Create `scripts/maintenance/` directory
2. Copy `weekly-cleanup.sh` from policy Appendix B
3. Test script in dry-run mode

**Day 4-5:**
1. Copy `archive-size-monitor.sh` from policy Appendix B
2. Create `logs/` directory
3. Run initial size check

**Day 6-7:**
1. Manual cleanup: Delete test reports >7 days
2. Flag working drafts >30 days for review
3. Document any immediate concerns

---

## Rollout Status

| Phase | Target Date | Status | Completion |
|-------|-------------|--------|------------|
| Phase 1 | Week 1 | ✅ Complete | 4/4 (100%) |
| Phase 2 | 2025-11-15 | 🔄 Not Started | 0/9 (0%) |
| Phase 3 | 2026-01-31 | ⏸️ Pending | 0/10 (0%) |
| Phase 4 | 2026-04-30 | ⏸️ Pending | 0/8 (0%) |
| Phase 5 | Ongoing | ⏸️ Pending | - |

**Overall Progress:** 4/31 tasks complete (13%)

---

## Success Metrics

Track these metrics to measure policy effectiveness:

| Metric | Baseline | Target | Current | Status |
|--------|----------|--------|---------|--------|
| Archive Size | 1.7M | <2.5M | 1.7M | ✅ On Track |
| Reports Size | 920K | <1.0M | 920K | ✅ On Track |
| Total Size | 2.6M | <3.0M | 2.6M | ✅ On Track |
| Growth Rate | Unknown | <200K/Q | TBD | ⏳ Monitoring |
| Maintenance Overhead | 40% | <10% | 40% | 🎯 Target Set |
| Rotation Compliance | N/A | 100% | N/A | ⏳ Not Applicable |

**Next Review:** 2025-12-01 (monthly check-in)

---

## Notes and Adjustments

### 2025-11-01 (Initial Creation)
- Policy established with comprehensive retention schedules
- Baseline metrics documented (2.6M total, 125 files)
- Implementation roadmap spans 6 months
- Immediate focus: Automation scripts and monitoring

### Future Updates
(Document any policy adjustments or implementation changes here)

---

**Last Updated:** 2025-11-01
**Next Review:** 2025-12-01
