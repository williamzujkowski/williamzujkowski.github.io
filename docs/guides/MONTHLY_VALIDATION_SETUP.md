# Monthly Portfolio Validation Setup Guide

## Overview

This guide explains how to set up automated monthly portfolio validation that runs on the first of every month at 2 AM, generating comprehensive health reports with zero manual intervention.

## Features

- ✅ **Automated Validation**: Runs monthly batch validation on all blog posts
- ✅ **Historical Comparison**: Compares with previous month's results
- ✅ **Comprehensive Reporting**: JSON data + human-readable summaries
- ✅ **Alert System**: Flags failing posts automatically
- ✅ **Email Notifications**: Optional email alerts (configurable)
- ✅ **Automatic Archiving**: Keeps last 12 months, archives older reports
- ✅ **Detailed Logging**: Full audit trail of all validations
- ✅ **Error Handling**: Graceful failure with detailed error messages

## Prerequisites

### Required Software

1. **Python 3.x**
   ```bash
   python3 --version
   # Should show Python 3.6 or higher
   ```

2. **jq (JSON processor)**
   ```bash
   sudo apt-get install jq
   # Or on macOS:
   brew install jq
   ```

3. **Bash 4.0+**
   ```bash
   bash --version
   ```

### Optional Software

4. **mail/mailx** (for email notifications)
   ```bash
   sudo apt-get install mailutils
   # Or on macOS:
   brew install mailutils
   ```

## Installation

### 1. Create Required Directories

```bash
# Navigate to repository
cd /home/william/git/williamzujkowski.github.io

# Create reports directory
mkdir -p reports/monthly

# Create logs directory
mkdir -p logs

# Verify directories
ls -ld reports/monthly logs
```

### 2. Make Script Executable

```bash
chmod +x scripts/maintenance/monthly-portfolio-validation.sh

# Verify permissions
ls -lh scripts/maintenance/monthly-portfolio-validation.sh
```

### 3. Test Manual Execution

```bash
# Run script manually to test
bash scripts/maintenance/monthly-portfolio-validation.sh

# Check output
ls -lh reports/monthly/
cat reports/monthly/summary-$(date +%Y-%m).txt
```

## Cron Setup

### Option 1: User Crontab (Recommended)

1. **Edit crontab**:
   ```bash
   crontab -e
   ```

2. **Add the following line**:
   ```cron
   # Monthly portfolio validation - runs 1st of month at 2 AM
   0 2 1 * * /home/william/git/williamzujkowski.github.io/scripts/maintenance/monthly-portfolio-validation.sh >> /home/william/git/williamzujkowski.github.io/logs/monthly-validation.log 2>&1
   ```

3. **Verify cron job**:
   ```bash
   crontab -l | grep monthly-portfolio
   ```

### Option 2: System Crontab

1. **Edit system crontab**:
   ```bash
   sudo vim /etc/crontab
   ```

2. **Add line with user**:
   ```cron
   0 2 1 * * william /home/william/git/williamzujkowski.github.io/scripts/maintenance/monthly-portfolio-validation.sh >> /home/william/git/williamzujkowski.github.io/logs/monthly-validation.log 2>&1
   ```

### Cron Schedule Explanation

```
0 2 1 * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday=0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

- **0 2 1 * ***: Run at 2:00 AM on the 1st day of every month

### Alternative Schedules

```cron
# Run monthly on 1st at 3 AM
0 3 1 * * /path/to/monthly-portfolio-validation.sh

# Run monthly on last day at 11 PM
0 23 L * * /path/to/monthly-portfolio-validation.sh

# Run twice monthly (1st and 15th at 2 AM)
0 2 1,15 * * /path/to/monthly-portfolio-validation.sh

# Run quarterly (1st of Jan, Apr, Jul, Oct at 2 AM)
0 2 1 1,4,7,10 * /path/to/monthly-portfolio-validation.sh
```

## Email Notifications Setup

### Configure Email Alerts

1. **Set EMAIL environment variable**:
   ```bash
   # In crontab (crontab -e), add at the top:
   EMAIL=your.email@example.com

   # Then your cron job line:
   0 2 1 * * /path/to/monthly-portfolio-validation.sh
   ```

2. **Or set in shell profile**:
   ```bash
   # Add to ~/.bashrc or ~/.zshrc
   export EMAIL="your.email@example.com"
   ```

3. **Test email functionality**:
   ```bash
   echo "Test message" | mail -s "Test Subject" your.email@example.com
   ```

### Email Notification Behavior

- **Success**: Email sent only if posts are failing (alert mode)
- **Failure**: Email sent with error details
- **Content**: Full summary report included in email body
- **Subject**: Includes status emoji and failure count

## Configuration Options

### Environment Variables

The script supports these environment variables:

```bash
# Set repository directory (default: current script location)
export REPO_DIR="/home/william/git/williamzujkowski.github.io"

# Set custom report directory (default: $REPO_DIR/reports/monthly)
export REPORT_DIR="/custom/path/to/reports"

# Set email for notifications (default: none)
export EMAIL="your.email@example.com"
```

### Customizing the Script

Edit `scripts/maintenance/monthly-portfolio-validation.sh` to customize:

1. **Change validation threshold** (line with `select(.score < 75)`):
   ```bash
   # Change from 75 to 80 for stricter validation
   jq -r '.results[] | select(.score < 80) | "\(.post_path) - Score: \(.score)"'
   ```

2. **Archive duration** (line with `12 months ago`):
   ```bash
   # Keep 6 months instead of 12
   local cutoff_date=$(date -d "6 months ago" +%Y-%m)
   ```

3. **Add Slack notifications** (add to `send_notification` function):
   ```bash
   if [ -n "${SLACK_WEBHOOK:-}" ]; then
       curl -X POST -H 'Content-type: application/json' \
           --data "{\"text\":\"$(cat $summary_file)\"}" \
           "$SLACK_WEBHOOK"
   fi
   ```

## Directory Structure

After setup, your structure will look like:

```
williamzujkowski.github.io/
├── scripts/
│   └── maintenance/
│       └── monthly-portfolio-validation.sh  # Main script
├── reports/
│   └── monthly/
│       ├── validation-2025-01.json          # Raw validation data
│       ├── validation-2025-02.json
│       ├── summary-2025-01.txt              # Human-readable summary
│       ├── summary-2025-02.txt
│       ├── comparison-2025-02.txt           # Month-over-month comparison
│       └── validation-2024-01.json.gz       # Archived old reports
├── logs/
│   └── monthly-validation.log               # Execution logs
└── docs/
    └── guides/
        └── MONTHLY_VALIDATION_SETUP.md      # This file
```

## Troubleshooting

### Script Not Running

1. **Check cron is running**:
   ```bash
   systemctl status cron
   # Or on some systems:
   service cron status
   ```

2. **Check cron logs**:
   ```bash
   grep CRON /var/log/syslog | tail -20
   # Or:
   journalctl -u cron | tail -20
   ```

3. **Verify script path**:
   ```bash
   which monthly-portfolio-validation.sh
   # Or:
   ls -lh /home/william/git/williamzujkowski.github.io/scripts/maintenance/monthly-portfolio-validation.sh
   ```

### Script Failing

1. **Check script logs**:
   ```bash
   tail -50 logs/monthly-validation.log
   ```

2. **Run manually with verbose output**:
   ```bash
   bash -x scripts/maintenance/monthly-portfolio-validation.sh
   ```

3. **Verify prerequisites**:
   ```bash
   # Check Python
   python3 --version

   # Check jq
   jq --version

   # Check validator script
   ls -lh scripts/blog-content/humanization-validator.py
   ```

### Missing Reports

1. **Check permissions**:
   ```bash
   ls -ld reports/monthly/
   chmod 755 reports/monthly/
   ```

2. **Check disk space**:
   ```bash
   df -h /home/william/git/williamzujkowski.github.io/
   ```

3. **Check validator output**:
   ```bash
   python3 scripts/blog-content/humanization-validator.py --batch --format json
   ```

### Email Not Sending

1. **Test mail command**:
   ```bash
   echo "Test" | mail -s "Test" your.email@example.com
   ```

2. **Check mail logs**:
   ```bash
   tail -20 /var/log/mail.log
   # Or:
   journalctl -u postfix | tail -20
   ```

3. **Verify EMAIL variable**:
   ```bash
   # In cron context
   crontab -l | grep EMAIL

   # In shell
   echo $EMAIL
   ```

## Manual Execution

### Run Validation On-Demand

```bash
# Full monthly validation
bash scripts/maintenance/monthly-portfolio-validation.sh

# Just the validation (no comparison/summary)
python3 scripts/blog-content/humanization-validator.py --batch \
    --save-report reports/monthly/manual-$(date +%Y-%m-%d).json \
    --format json
```

### View Latest Report

```bash
# View summary
cat reports/monthly/summary-$(date +%Y-%m).txt

# View JSON data
jq '.' reports/monthly/validation-$(date +%Y-%m).json

# View specific metrics
jq '.statistics' reports/monthly/validation-$(date +%Y-%m).json
```

### Compare Two Months

```bash
# Compare January and February
python3 scripts/blog-content/humanization-validator.py --batch \
    --compare reports/monthly/validation-2025-01.json \
    > reports/monthly/comparison-custom.txt

cat reports/monthly/comparison-custom.txt
```

## Monitoring & Maintenance

### Check Validation Status

```bash
# View last 10 validation runs
tail -100 logs/monthly-validation.log | grep "Starting monthly\|completed successfully\|failed"

# Check current month status
cat reports/monthly/summary-$(date +%Y-%m).txt
```

### Review Failing Posts

```bash
# List all failing posts from current month
jq -r '.results[] | select(.score < 75) | .post_path' \
    reports/monthly/validation-$(date +%Y-%m).json
```

### Historical Analysis

```bash
# Compare last 6 months
for month in {0..5}; do
    date_str=$(date -d "$month months ago" +%Y-%m)
    if [ -f "reports/monthly/validation-$date_str.json" ]; then
        echo "=== $date_str ==="
        jq '.statistics' "reports/monthly/validation-$date_str.json"
    fi
done
```

### Cleanup Old Reports

```bash
# Archive runs automatically, but you can manually clean:
find reports/monthly/ -name "*.json" -mtime +365 -exec gzip {} \;

# Remove very old archives (2+ years)
find reports/monthly/ -name "*.json.gz" -mtime +730 -delete
```

## Best Practices

### 1. Regular Review
- Check summary reports monthly
- Address failing posts promptly
- Track trends over time

### 2. Proactive Maintenance
- Fix posts scoring below 80
- Update outdated content
- Maintain citation quality

### 3. Documentation
- Keep this guide updated
- Document customizations
- Note recurring issues

### 4. Backup
- Backup reports directory monthly
- Keep logs for audit trail
- Archive important findings

## Integration with Git

### Auto-commit Reports (Optional)

Add to end of `monthly-portfolio-validation.sh`:

```bash
# Auto-commit monthly reports
cd "$REPO_DIR"
git add reports/monthly/validation-$CURRENT_MONTH.json
git add reports/monthly/summary-$CURRENT_MONTH.txt
git commit -m "chore: monthly validation report for $CURRENT_MONTH"
git push origin main
```

### Create GitHub Issue for Failures (Advanced)

```bash
# If posts failing, create GitHub issue
if [ "$failed" -gt 0 ]; then
    gh issue create \
        --title "Monthly Validation: $failed posts failing" \
        --body "$(cat $summary_file)" \
        --label "validation" \
        --label "automated"
fi
```

## Support & Resources

### Key Files
- **Script**: `scripts/maintenance/monthly-portfolio-validation.sh`
- **Validator**: `scripts/blog-content/humanization-validator.py`
- **Reports**: `reports/monthly/`
- **Logs**: `logs/monthly-validation.log`

### Documentation
- **Main Guide**: `CLAUDE.md` (project standards)
- **Validator Docs**: `scripts/blog-content/humanization-validator.py --help`
- **SPARC Workflow**: `docs/ARCHITECTURE.md`

### Getting Help

1. Check logs: `tail -50 logs/monthly-validation.log`
2. Run manual test: `bash scripts/maintenance/monthly-portfolio-validation.sh`
3. Review validator help: `python3 scripts/blog-content/humanization-validator.py --help`
4. Check cron logs: `grep CRON /var/log/syslog`

## Quick Reference

### Essential Commands

```bash
# Setup
chmod +x scripts/maintenance/monthly-portfolio-validation.sh
mkdir -p reports/monthly logs
crontab -e  # Add: 0 2 1 * * /path/to/script

# Test
bash scripts/maintenance/monthly-portfolio-validation.sh

# Monitor
tail -f logs/monthly-validation.log
cat reports/monthly/summary-$(date +%Y-%m).txt

# Review
jq '.statistics' reports/monthly/validation-$(date +%Y-%m).json
```

### Cron Template

```cron
# Email for notifications
EMAIL=your.email@example.com

# Monthly validation (1st of month at 2 AM)
0 2 1 * * /home/william/git/williamzujkowski.github.io/scripts/maintenance/monthly-portfolio-validation.sh >> /home/william/git/williamzujkowski.github.io/logs/monthly-validation.log 2>&1
```

---

**Zero-Maintenance Philosophy**: Once configured, this system requires no human intervention. Reports are generated, compared, and archived automatically. You only need to act when alerted to failing posts.
