# Repository Maintenance Setup Checklist

**Purpose**: Ensure proper setup and integration of the repository maintenance system

## Initial Setup

### 1. Verify Script Installation
- [ ] Script exists at `scripts/utilities/repo-maintenance.py`
- [ ] Script is executable: `chmod +x scripts/utilities/repo-maintenance.py`
- [ ] Help works: `python scripts/utilities/repo-maintenance.py --help`
- [ ] Dry-run works: `python scripts/utilities/repo-maintenance.py --dry-run --health-check`

### 2. Check Dependencies
- [ ] Python 3.11+ installed: `python --version`
- [ ] pyyaml installed: `pip install pyyaml`
- [ ] requests installed: `pip install requests`
- [ ] Common lib exists: `scripts/lib/common.py`
- [ ] Git available: `git --version`
- [ ] npm available: `npm --version`

### 3. Create Required Directories
```bash
mkdir -p logs
mkdir -p docs/reports
mkdir -p docs/archive/reports
```

- [ ] `logs/` directory created
- [ ] `docs/reports/` directory created
- [ ] `docs/archive/reports/` directory created

## Testing Phase

### 4. Run Initial Tests
```bash
# Test 1: Health check
python scripts/utilities/repo-maintenance.py --health-check

# Test 2: Full dry-run
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose

# Test 3: Cleanup only
python scripts/utilities/repo-maintenance.py --dry-run --cleanup

# Test 4: Archive only
python scripts/utilities/repo-maintenance.py --dry-run --archive
```

- [ ] Health check completes without errors
- [ ] Full dry-run shows expected results
- [ ] Cleanup detection works
- [ ] Archive detection works
- [ ] Exit codes are correct (0, 1, or 2)

### 5. Review Test Results
- [ ] MANIFEST.json validation passes
- [ ] Pre-commit hooks status shown
- [ ] npm audit runs (or gracefully fails)
- [ ] Git status checked
- [ ] Script count accurate
- [ ] SEO drift detected (if applicable)
- [ ] No protected files flagged for deletion

## Configuration

### 6. Review Protected Files
Check `.claude-rules.json` includes:
- [ ] MANIFEST.json
- [ ] CLAUDE.md
- [ ] .claude-rules.json
- [ ] .eleventy.js
- [ ] package.json
- [ ] tailwind.config.js
- [ ] README.md
- [ ] scripts/lib/common.py

### 7. Configure Automation (Choose One)

#### Option A: Cron Setup
```bash
# Edit crontab
crontab -e

# Add monthly maintenance (1st of month at 2 AM)
0 2 1 * * cd /home/william/git/williamzujkowski.github.io && python scripts/utilities/repo-maintenance.py --full --force --backup >> logs/maintenance.log 2>&1
```

- [ ] Cron entry added
- [ ] Log directory exists
- [ ] Test cron: `crontab -l | grep maintenance`

#### Option B: Systemd Timer
```bash
# Copy service files
sudo cp scripts/utilities/cron-maintenance.example /etc/systemd/system/repo-maintenance.service
# Edit paths in service file
sudo systemctl daemon-reload
sudo systemctl enable repo-maintenance.timer
sudo systemctl start repo-maintenance.timer
```

- [ ] Service file created and edited
- [ ] Timer enabled
- [ ] Timer started
- [ ] Status verified: `systemctl status repo-maintenance.timer`

#### Option C: GitHub Actions
```bash
# Copy workflow
cp .github/workflows/maintenance.yml.example .github/workflows/maintenance.yml
# Commit and push
git add .github/workflows/maintenance.yml
git commit -m "feat: add automated maintenance workflow"
git push
```

- [ ] Workflow file copied and customized
- [ ] File committed to repository
- [ ] Workflow appears in GitHub Actions tab
- [ ] Manual trigger tested (workflow_dispatch)

## Integration Testing

### 8. End-to-End Test
```bash
# Full maintenance run with backup
python scripts/utilities/repo-maintenance.py --full --backup --verbose
```

- [ ] Cleanup runs successfully
- [ ] Archive runs successfully (if old reports exist)
- [ ] Health checks complete
- [ ] Report generated in `docs/reports/`
- [ ] No unexpected errors

### 9. Verify Report Generation
```bash
# Check latest report
ls -lh docs/reports/maintenance-*.json
cat docs/reports/maintenance-$(date +%Y-%m-%d).json | jq
```

- [ ] JSON report exists
- [ ] Report is valid JSON
- [ ] Statistics section populated
- [ ] Findings section populated
- [ ] Actions section populated (if applicable)
- [ ] Correct exit code recorded

## Documentation Review

### 10. Review Documentation
- [ ] Read `docs/GUIDES/REPO_MAINTENANCE_GUIDE.md`
- [ ] Review `docs/QUICK_REFERENCE_MAINTENANCE.md`
- [ ] Check `docs/EXAMPLES_MAINTENANCE.md` for use cases
- [ ] Understand `docs/MAINTENANCE_SUMMARY.md`

### 11. Customize for Your Workflow
- [ ] Adjust cleanup patterns if needed
- [ ] Set archive age threshold (default: 60 days)
- [ ] Configure SEO drift threshold (default: 10%)
- [ ] Add custom protected files if needed

## Monitoring Setup

### 12. Set Up Monitoring
```bash
# Create monitoring script
cat > scripts/check-maintenance-status.sh << 'EOF'
#!/bin/bash
LATEST_REPORT=$(ls -t docs/reports/maintenance-*.json | head -1)
if [ -z "$LATEST_REPORT" ]; then
    echo "⚠️ No maintenance reports found"
    exit 1
fi

AGE_DAYS=$(( ($(date +%s) - $(stat -c %Y "$LATEST_REPORT")) / 86400 ))
if [ $AGE_DAYS -gt 35 ]; then
    echo "⚠️ Last maintenance was $AGE_DAYS days ago"
    exit 1
fi

EXIT_CODE=$(jq -r '.exit_code' "$LATEST_REPORT")
if [ "$EXIT_CODE" -eq 2 ]; then
    echo "❌ Last maintenance had errors"
    exit 2
elif [ "$EXIT_CODE" -eq 1 ]; then
    echo "⚠️ Last maintenance had warnings"
    exit 1
else
    echo "✅ Maintenance status: OK"
    exit 0
fi
EOF

chmod +x scripts/check-maintenance-status.sh
```

- [ ] Monitoring script created
- [ ] Script is executable
- [ ] Script runs successfully

### 13. Configure Notifications (Optional)
```bash
# Email notifications via cron
# Add MAILTO to crontab
MAILTO=your-email@example.com
```

- [ ] Email configured (if desired)
- [ ] Test email: run maintenance and verify receipt

## Operational Readiness

### 14. Create Runbook
Create `docs/RUNBOOKS/maintenance.md` with:
- [ ] When to run maintenance (monthly/as-needed)
- [ ] How to interpret results
- [ ] What to do if errors occur
- [ ] Who to contact for issues

### 15. Train Team (if applicable)
- [ ] Share documentation with team
- [ ] Demonstrate dry-run mode
- [ ] Explain exit codes
- [ ] Review common issues

## Final Verification

### 16. Pre-Production Checklist
- [ ] All tests passing
- [ ] Documentation complete
- [ ] Automation configured
- [ ] Monitoring set up
- [ ] Team trained (if applicable)
- [ ] Runbook created

### 17. Production Deployment
```bash
# Commit all changes
git add scripts/utilities/repo-maintenance.py
git add docs/GUIDES/REPO_MAINTENANCE_GUIDE.md
git add docs/QUICK_REFERENCE_MAINTENANCE.md
git add docs/EXAMPLES_MAINTENANCE.md
git add docs/MAINTENANCE_SUMMARY.md
git add .github/workflows/maintenance.yml
git commit -m "feat: add comprehensive repository maintenance system"
git push
```

- [ ] All files committed
- [ ] Changes pushed to remote
- [ ] GitHub Actions workflow visible
- [ ] Documentation accessible

### 18. Post-Deployment Verification
- [ ] First automated run successful (wait for scheduled time)
- [ ] Report generated as expected
- [ ] No issues with protected files
- [ ] Exit codes appropriate
- [ ] Logs readable and useful

## Maintenance Schedule

### 19. Regular Operations
Set up calendar reminders:
- [ ] **Monthly**: Review maintenance reports
- [ ] **Quarterly**: Review automation effectiveness
- [ ] **Bi-annually**: Update documentation
- [ ] **Annually**: Review and optimize scripts

### 20. Continuous Improvement
Track these metrics over time:
- [ ] Temp files cleaned per month
- [ ] Reports archived per quarter
- [ ] SEO drift percentage trend
- [ ] Script count growth
- [ ] Duplicate files detected

## Troubleshooting Preparation

### 21. Common Issues Documentation
Document solutions for:
- [ ] MANIFEST.json validation failures
- [ ] npm audit issues
- [ ] Pre-commit hook problems
- [ ] Git status errors
- [ ] SEO drift increases

### 22. Rollback Plan
Know how to:
- [ ] Restore from backup: `docs/archive/reports/`
- [ ] Disable automation if needed
- [ ] Revert script changes
- [ ] Contact support

## Success Criteria

### 23. Final Sign-Off
All checks pass:
- [x] Script installed and tested ✅
- [x] Dependencies verified ✅
- [x] Directories created ✅
- [x] Tests completed ✅
- [x] Documentation reviewed ✅
- [ ] Automation configured (user choice)
- [ ] Monitoring set up (user choice)
- [x] Team trained (N/A for solo use) ✅

## Next Steps After Setup

### 24. First Month
- [ ] Week 1: Run health checks manually
- [ ] Week 2: Review any warnings
- [ ] Week 3: Test cleanup functionality
- [ ] Week 4: Ensure automation runs successfully

### 25. Ongoing
- [ ] Review monthly reports
- [ ] Address warnings promptly
- [ ] Update protected files list as needed
- [ ] Share improvements with community

## Support Resources

- **Full Guide**: `docs/GUIDES/REPO_MAINTENANCE_GUIDE.md`
- **Quick Reference**: `docs/QUICK_REFERENCE_MAINTENANCE.md`
- **Examples**: `docs/EXAMPLES_MAINTENANCE.md`
- **Summary**: `docs/MAINTENANCE_SUMMARY.md`
- **Script Help**: `python scripts/utilities/repo-maintenance.py --help`

## Notes

- Always use `--dry-run` first when testing
- Review protected files list regularly
- Keep documentation updated
- Monitor exit codes in automation
- Archive reports periodically

---

**Setup Date**: _______________
**Setup By**: _______________
**Automation Method**: ☐ Cron ☐ Systemd ☐ GitHub Actions ☐ Manual
**Status**: ☐ In Progress ☐ Complete ☐ Deferred

**Signature**: _______________
