# Monthly Portfolio Validation - Quick Reference Card

## 🚀 One-Time Setup (5 minutes)

```bash
# 1. Install prerequisites
sudo apt-get install jq  # JSON processor

# 2. Verify installation
which jq python3 bash

# 3. Test script manually
bash scripts/maintenance/monthly-portfolio-validation.sh

# 4. Add to cron (runs 1st of month at 2 AM)
crontab -e
```

Add this line to crontab:
```cron
0 2 1 * * /home/william/git/williamzujkowski.github.io/scripts/maintenance/monthly-portfolio-validation.sh >> /home/william/git/williamzujkowski.github.io/logs/monthly-validation.log 2>&1
```

## 📊 Daily Commands

### View Latest Report
```bash
cat reports/monthly/summary-$(date +%Y-%m).txt
```

### Check Statistics
```bash
jq '.statistics' reports/monthly/validation-$(date +%Y-%m).json
```

### View Recent Logs
```bash
tail -20 logs/monthly-validation.log
```

### List Failing Posts (if any)
```bash
jq -r '.results[] | select(.score < 75) | .post_path' reports/monthly/validation-$(date +%Y-%m).json
```

## 🔧 Troubleshooting

### Script Won't Run
```bash
# Check permissions
chmod +x scripts/maintenance/monthly-portfolio-validation.sh

# Check prerequisites
which jq python3 bash

# Run with debug
bash -x scripts/maintenance/monthly-portfolio-validation.sh
```

### No Reports Generated
```bash
# Check directories exist
ls -ld reports/monthly logs

# Create if missing
mkdir -p reports/monthly logs

# Check disk space
df -h .
```

### Cron Not Running
```bash
# Check cron status
systemctl status cron

# View cron logs
grep CRON /var/log/syslog | tail -20

# Verify crontab entry
crontab -l | grep monthly
```

## 📧 Email Notifications (Optional)

### Setup
```bash
# Add to crontab (before the job line)
EMAIL=your.email@example.com

# Or set in environment
export EMAIL="your.email@example.com"
```

### Test
```bash
echo "Test" | mail -s "Test Email" your.email@example.com
```

## 📈 Monthly Routine

### 1st of Month (Automated)
- ✅ Script runs at 2 AM
- ✅ Generates validation report
- ✅ Compares with previous month
- ✅ Creates summary
- ✅ Sends email if failures

### After Report
```bash
# 1. View summary
cat reports/monthly/summary-$(date +%Y-%m).txt

# 2. If failures, list them
jq -r '.results[] | select(.score < 75) | "\(.post_path): \(.score)"' reports/monthly/validation-$(date +%Y-%m).json

# 3. Fix failing posts
python3 scripts/blog-content/humanization-validator.py --post src/posts/FAILING_POST.md

# 4. Re-validate
bash scripts/maintenance/monthly-portfolio-validation.sh
```

## 🎯 Key Metrics

### Portfolio Health Indicators
- **Pass Rate**: Target 100%
- **Average Score**: Target ≥100
- **Median Score**: Target ≥105
- **Min Score**: Target ≥75 (passing)

### Score Thresholds
- **110**: Perfect score
- **100-109**: Excellent
- **85-99**: Good
- **75-84**: Passing
- **<75**: Failing (requires attention)

## 📁 File Locations

| File | Purpose | Location |
|------|---------|----------|
| Script | Main validation script | `scripts/maintenance/monthly-portfolio-validation.sh` |
| Setup Guide | Detailed instructions | `docs/guides/MONTHLY_VALIDATION_SETUP.md` |
| JSON Reports | Raw validation data | `reports/monthly/validation-YYYY-MM.json` |
| Summaries | Human-readable reports | `reports/monthly/summary-YYYY-MM.txt` |
| Comparisons | Month-over-month | `reports/monthly/comparison-YYYY-MM.txt` |
| Logs | Execution audit trail | `logs/monthly-validation.log` |

## 🔍 Common Queries

### Get Overall Statistics
```bash
jq '.statistics' reports/monthly/validation-$(date +%Y-%m).json
```

### List Top 10 Posts
```bash
jq -r '.results | sort_by(.score) | reverse | .[0:10] | .[] | "\(.score): \(.post_path)"' reports/monthly/validation-$(date +%Y-%m).json
```

### Find Posts with Warnings
```bash
jq -r '.results[] | select(.warnings | length > 0) | .post_path' reports/monthly/validation-$(date +%Y-%m).json
```

### Count Posts by Score Range
```bash
jq '[.results | group_by(.score >= 100) | .[] | length]' reports/monthly/validation-$(date +%Y-%m).json
```

## 📊 Historical Analysis

### Compare Last 6 Months
```bash
for month in {0..5}; do
  date_str=$(date -d "$month months ago" +%Y-%m)
  if [ -f "reports/monthly/validation-$date_str.json" ]; then
    echo "=== $date_str ==="
    jq '.statistics | "Passed: \(.passed)/\(.total_posts) | Avg: \(.avg_score)"' "reports/monthly/validation-$date_str.json"
  fi
done
```

### View Trend
```bash
# Average scores over time
for report in reports/monthly/validation-*.json; do
  month=$(basename "$report" .json | sed 's/validation-//')
  avg=$(jq -r '.statistics.avg_score' "$report")
  echo "$month: $avg"
done | sort
```

## 🆘 Emergency Commands

### Run Validation Now (Skip Cron)
```bash
bash scripts/maintenance/monthly-portfolio-validation.sh
```

### Force Re-validation
```bash
# Delete current month report and re-run
rm reports/monthly/validation-$(date +%Y-%m).json
bash scripts/maintenance/monthly-portfolio-validation.sh
```

### Clear All Reports (Nuclear Option)
```bash
# Backup first!
tar -czf reports-backup-$(date +%Y-%m-%d).tar.gz reports/monthly/
rm reports/monthly/*.json reports/monthly/*.txt
```

### Restore from Backup
```bash
tar -xzf reports-backup-YYYY-MM-DD.tar.gz
```

## 🎓 Learn More

- **Full Documentation**: `docs/guides/MONTHLY_VALIDATION_SETUP.md`
- **Test Results**: `reports/monthly/TEST_EXECUTION_RESULTS.md`
- **Validator Help**: `python3 scripts/blog-content/humanization-validator.py --help`
- **Main Standards**: `CLAUDE.md`

## 📞 Quick Support

### Debug Checklist
1. ✅ Prerequisites installed? (`which jq python3`)
2. ✅ Script executable? (`ls -l scripts/maintenance/monthly-portfolio-validation.sh`)
3. ✅ Directories exist? (`ls -ld reports/monthly logs`)
4. ✅ Disk space? (`df -h .`)
5. ✅ Cron running? (`systemctl status cron`)

### Common Issues

| Issue | Solution |
|-------|----------|
| "jq: command not found" | `sudo apt-get install jq` |
| "Permission denied" | `chmod +x scripts/maintenance/monthly-portfolio-validation.sh` |
| "No such file or directory" | `mkdir -p reports/monthly logs` |
| Cron not running | `systemctl start cron` |
| No email | Set `EMAIL` environment variable |

---

**Remember**: This system is designed for zero maintenance. Once set up, it runs automatically every month without human intervention!

**Next Action**: Add to cron, then forget about it (until you get an alert email)
