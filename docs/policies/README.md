# Repository Policies

This directory contains formal policies governing repository operations, maintenance, and compliance.

## Policy Documents

### Active Policies

**[ARCHIVE_ROTATION_POLICY.md](ARCHIVE_ROTATION_POLICY.md)**
- **Status:** Active
- **Effective:** 2025-11-01
- **Purpose:** Establish retention schedules and rotation procedures for documentation archives
- **Scope:** All files in `docs/archive/` and `docs/reports/`
- **Review:** Quarterly
- **Next Review:** 2026-02-01

**Key Points:**
- Retention schedules by file type (7 days to indefinite)
- Quarterly rotation procedures
- Automation recommendations
- 40% maintenance overhead reduction target

## Supporting Documents

### [ARCHIVE_BASELINE.md](ARCHIVE_BASELINE.md)
Baseline metrics for archive rotation policy effectiveness tracking.

**Current Metrics (2025-11-01):**
- Archive: 1.7M (89 files)
- Reports: 920K (36 files)
- Total: 2.6M
- Growth Rate: ~300K per quarter

### [IMPLEMENTATION_CHECKLIST.md](IMPLEMENTATION_CHECKLIST.md)
Phased implementation roadmap for archive rotation policy.

**Phases:**
1. ✅ Immediate (Week 1) - Policy establishment
2. 🔄 Quick Wins (Week 2-4) - Manual cleanup and monitoring
3. ⏸️ Automation (Month 2-3) - Script development
4. ⏸️ Optimization (Month 4-6) - Advanced features
5. ⏸️ Continuous Improvement (Ongoing) - Maintenance

**Progress:** 4/31 tasks complete (13%)

### [archive-exceptions.log](archive-exceptions.log)
Exception tracking log for policy deviations.

**Current Exceptions:** None

## Usage Guidelines

### For LLM Agents

**Before Archive Operations:**
1. Read `ARCHIVE_ROTATION_POLICY.md` Section 3 (What to Keep vs. Delete)
2. Check file against decision matrix (Section 3.4)
3. If unsure, request exception via `archive-exceptions.log`

**Before Deleting Files:**
1. Verify file meets deletion criteria per policy
2. Check for active references: `grep -r "filename" docs/`
3. Document in commit message: "Deleted per archive rotation policy Section X.Y"

**Monthly Monitoring:**
1. Run size check: `du -sh docs/archive docs/reports`
2. Identify overdue rotations: `find docs/reports -mtime +180`
3. Update `ARCHIVE_BASELINE.md` with current metrics

### For Repository Maintainers

**Monthly Tasks (1st of month):**
- Run `scripts/maintenance/archive-size-monitor.sh`
- Update baseline tracking
- Review exception log

**Quarterly Tasks (end of quarter):**
- Execute `scripts/maintenance/quarterly-archive.sh YYYY-QX`
- Generate quarterly report
- Audit all active exceptions

**Annual Tasks (February):**
- Policy review and update
- Assess automation effectiveness
- Update retention periods if needed

## Policy Development

### Adding New Policies

**Process:**
1. Draft policy document in `docs/policies/`
2. Use existing policies as template
3. Include: Purpose, Scope, Procedures, Compliance, Review Schedule
4. Add to this README under "Active Policies"
5. Update implementation checklist if needed

**Required Sections:**
- Policy Overview (goals, scope, current state)
- Detailed Procedures
- Compliance and Monitoring
- Implementation Roadmap
- Related Documents
- Version History

**Naming Convention:**
- Use ALL_CAPS_WITH_UNDERSCORES.md
- Be descriptive: `ARCHIVE_ROTATION_POLICY.md` not `ARCHIVE.md`
- Include policy type: POLICY, STANDARD, GUIDELINE

### Policy Review Process

**Monthly:** Compliance checks and metric collection
**Quarterly:** Implementation progress and policy audit
**Annually:** Comprehensive policy review and updates

**Review Checklist:**
- [ ] Policy achieving stated goals?
- [ ] Compliance metrics on track?
- [ ] Implementation proceeding as planned?
- [ ] Adjustments needed?
- [ ] Version update required?

## Compliance

### Active Compliance Requirements

**Archive Rotation Policy:**
- ✅ All files categorized properly
- ✅ Retention periods defined by type
- ✅ Automation roadmap established
- ⏳ Monthly monitoring (not yet started)
- ⏳ Quarterly rotation (next: 2025-12-31)

**Enforcement:**
- Pre-commit hooks validate file locations
- GitHub Actions check documentation compliance
- `.claude-rules.json` enforces mandatory rules

See: `CLAUDE.md` for enforcement framework

## Future Policies

**Planned (Priority Order):**

1. **DATA_RETENTION_POLICY.md** (Q1 2026)
   - JSON data file retention
   - Generated report cleanup
   - Backup and archival procedures

2. **DOCUMENTATION_STANDARDS.md** (Q1 2026)
   - Markdown formatting requirements
   - Documentation structure standards
   - Review and approval process

3. **SCRIPT_MAINTENANCE_POLICY.md** (Q2 2026)
   - Script deprecation procedures
   - Version control requirements
   - Documentation standards

4. **SECURITY_POLICY.md** (Q2 2026)
   - Secrets management
   - Dependency scanning
   - Vulnerability disclosure

## Related Documentation

**Repository Standards:**
- `/CLAUDE.md` - Master repository configuration
- `/.claude-rules.json` - Enforcement rules
- `/docs/ENFORCEMENT.md` - Extended enforcement guidelines

**Implementation Guides:**
- `/docs/GUIDES/SCRIPT_CATALOG.md` - Script reference
- `/docs/GUIDES/LLM_ONBOARDING.md` - Agent onboarding
- `/docs/ARCHITECTURE.md` - Repository structure

**Maintenance:**
- `/docs/archive/ARCHIVAL_SUMMARY.md` - Historical context
- `/MANIFEST.json` - File registry

## Change Log

| Date | Change | Version | Author |
|------|--------|---------|--------|
| 2025-11-01 | Created policies directory and archive rotation policy | 1.0.0 | Documentation Agent |

---

**Directory Status:** Active
**Last Updated:** 2025-11-01
**Next Review:** 2025-12-01
