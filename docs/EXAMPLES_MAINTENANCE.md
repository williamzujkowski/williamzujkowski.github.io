# Repository Maintenance - Usage Examples

## Basic Usage

### 1. First-Time User

```bash
# Step 1: Check help
python scripts/utilities/repo-maintenance.py --help

# Step 2: Preview what would happen (safe)
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose

# Step 3: Review output, then run for real
python scripts/utilities/repo-maintenance.py --full --backup
```

### 2. Quick Health Check

```bash
# Basic health check
python scripts/utilities/repo-maintenance.py --health-check

# With details
python scripts/utilities/repo-maintenance.py --health-check --verbose
```

### 3. Cleanup Only

```bash
# Preview cleanup
python scripts/utilities/repo-maintenance.py --dry-run --cleanup

# Run cleanup
python scripts/utilities/repo-maintenance.py --cleanup
```

## Advanced Usage

### 4. Monthly Maintenance Routine

```bash
#!/bin/bash
# monthly-maintenance.sh

REPO_DIR="/home/william/git/williamzujkowski.github.io"
cd "$REPO_DIR" || exit 1

echo "=== Starting Monthly Maintenance ==="
date

# Step 1: Preview
echo "Step 1: Previewing changes..."
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose

# Step 2: Pause for review
read -p "Continue with actual maintenance? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted by user"
    exit 1
fi

# Step 3: Run maintenance
echo "Step 2: Running maintenance..."
python scripts/utilities/repo-maintenance.py --full --backup --verbose

# Step 4: Check exit code
EXIT_CODE=$?
if [ $EXIT_CODE -eq 0 ]; then
    echo "✅ Maintenance completed successfully"
elif [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️ Maintenance completed with warnings"
else
    echo "❌ Maintenance failed with errors"
    exit 1
fi

# Step 5: Show report
echo "Step 3: Showing report summary..."
REPORT_FILE="docs/reports/maintenance-$(date +%Y-%m-%d).json"
if [ -f "$REPORT_FILE" ]; then
    cat "$REPORT_FILE" | jq '.statistics'
fi

echo "=== Maintenance Complete ==="
date
```

### 5. CI/CD Integration

```bash
#!/bin/bash
# .github/scripts/pre-deploy-check.sh

# Fail on any error
set -e

echo "Running pre-deployment health check..."

# Run health check
python scripts/utilities/repo-maintenance.py --health-check --verbose

# Check exit code
EXIT_CODE=$?

if [ $EXIT_CODE -eq 2 ]; then
    echo "❌ Critical errors found - deployment blocked"
    exit 1
elif [ $EXIT_CODE -eq 1 ]; then
    echo "⚠️ Warnings found - proceeding with caution"
    exit 0
else
    echo "✅ All checks passed"
    exit 0
fi
```

### 6. Automated Cleanup Script

```bash
#!/bin/bash
# scripts/auto-cleanup.sh

# Run cleanup automatically if temp files detected

TEMP_COUNT=$(python scripts/utilities/repo-maintenance.py --dry-run --cleanup 2>&1 | grep "temp_files_found:" | awk '{print $2}')

if [ "$TEMP_COUNT" -gt 0 ]; then
    echo "Found $TEMP_COUNT temp files - cleaning..."
    python scripts/utilities/repo-maintenance.py --cleanup --force
else
    echo "No temp files to clean"
fi
```

## Monitoring & Reporting

### 7. Weekly Summary Email

```bash
#!/bin/bash
# scripts/weekly-summary.sh

REPORT=$(python scripts/utilities/repo-maintenance.py --health-check --verbose 2>&1)
WARNINGS=$(echo "$REPORT" | grep -c "⚠️" || echo "0")
ERRORS=$(echo "$REPORT" | grep -c "❌" || echo "0")

# Send email if issues found
if [ "$WARNINGS" -gt 0 ] || [ "$ERRORS" -gt 0 ]; then
    echo "$REPORT" | mail -s "Repository Health Report - $(date +%Y-%m-%d)" admin@example.com
fi
```

### 8. Report Analysis

```bash
# View statistics from reports
jq '.statistics' docs/reports/maintenance-*.json

# Find all warnings
jq '.warnings[]' docs/reports/maintenance-*.json

# Check for errors
jq 'select(.exit_code == 2) | {date: .timestamp, errors: .errors}' docs/reports/maintenance-*.json

# Get SEO drift percentage over time
jq -r '[.timestamp, .statistics.posts_with_seo_drift, .statistics.total_posts_checked] | @tsv' docs/reports/maintenance-*.json
```

## Problem-Solving Examples

### 9. Fix SEO Drift

```bash
# Step 1: Identify posts with SEO issues
python scripts/utilities/repo-maintenance.py --health-check --verbose 2>&1 | \
    grep "description length" | \
    awk -F: '{print $1}' | \
    sort > /tmp/seo-issues.txt

echo "Found $(wc -l < /tmp/seo-issues.txt) posts with SEO issues"

# Step 2: Review each post
cat /tmp/seo-issues.txt | while read POST; do
    echo "=== $POST ==="
    grep "^description:" "src/posts/$POST" || echo "No description found"
done

# Step 3: Use optimization script (if available)
# python scripts/blog-content/optimize-blog-content.py --fix-descriptions
```

### 10. Clean Up After Development

```bash
# After a development session, clean up temp files
python scripts/utilities/repo-maintenance.py --cleanup --verbose

# Check for any issues introduced
python scripts/utilities/repo-maintenance.py --health-check
```

### 11. Pre-Commit Hook Integration

```bash
# .git/hooks/pre-commit (add this section)

# Run health check before commit
python scripts/utilities/repo-maintenance.py --health-check
EXIT_CODE=$?

if [ $EXIT_CODE -eq 2 ]; then
    echo "❌ Critical repository health issues detected"
    echo "Run: python scripts/utilities/repo-maintenance.py --health-check --verbose"
    exit 1
fi
```

## Automation Examples

### 12. Systemd Service

```bash
# /etc/systemd/system/repo-maintenance.service
cat > /tmp/repo-maintenance.service << 'EOF'
[Unit]
Description=Repository Maintenance
After=network.target

[Service]
Type=oneshot
User=william
WorkingDirectory=/home/william/git/williamzujkowski.github.io
ExecStart=/usr/bin/python3 scripts/utilities/repo-maintenance.py --full --force --backup
StandardOutput=append:/home/william/git/williamzujkowski.github.io/logs/maintenance.log
StandardError=append:/home/william/git/williamzujkowski.github.io/logs/maintenance.log

[Install]
WantedBy=multi-user.target
EOF

# /etc/systemd/system/repo-maintenance.timer
cat > /tmp/repo-maintenance.timer << 'EOF'
[Unit]
Description=Monthly Repository Maintenance
Requires=repo-maintenance.service

[Timer]
OnCalendar=monthly
Persistent=true

[Install]
WantedBy=timers.target
EOF

# Install and enable
sudo cp /tmp/repo-maintenance.service /etc/systemd/system/
sudo cp /tmp/repo-maintenance.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable repo-maintenance.timer
sudo systemctl start repo-maintenance.timer

# Check status
sudo systemctl status repo-maintenance.timer
sudo systemctl list-timers repo-maintenance.timer
```

### 13. Docker Integration

```dockerfile
# Dockerfile for maintenance
FROM python:3.11-slim

WORKDIR /repo

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pyyaml requests

# Copy scripts
COPY scripts/ scripts/
COPY MANIFEST.json .claude-rules.json ./
COPY src/ src/
COPY docs/ docs/

# Run maintenance
CMD ["python", "scripts/utilities/repo-maintenance.py", "--full", "--force"]
```

```bash
# Build and run
docker build -t repo-maintenance .
docker run -v $(pwd)/docs/reports:/repo/docs/reports repo-maintenance

# With docker-compose
# docker-compose.yml
cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  maintenance:
    build: .
    volumes:
      - ./docs/reports:/repo/docs/reports
      - ./logs:/repo/logs
    environment:
      - TZ=America/New_York
EOF

docker-compose run maintenance
```

## Output Examples

### 14. Parsing Output

```bash
# Extract statistics
python scripts/utilities/repo-maintenance.py --health-check 2>&1 | \
    awk '/Statistics:/,/^$/' | \
    grep -v "Statistics:" | \
    grep "^  "

# Count warnings
python scripts/utilities/repo-maintenance.py --health-check 2>&1 | \
    grep -c "⚠️"

# Get exit code
python scripts/utilities/repo-maintenance.py --health-check
echo "Exit code: $?"

# Save to file
python scripts/utilities/repo-maintenance.py --full --verbose > maintenance-output.txt 2>&1
```

### 15. Integration with Other Tools

```bash
# Run before link validation
python scripts/utilities/repo-maintenance.py --health-check && \
python scripts/link-validation/link-validator.py

# Run before content optimization
python scripts/utilities/repo-maintenance.py --cleanup && \
python scripts/blog-content/optimize-blog-content.py

# Chain with git operations
python scripts/utilities/repo-maintenance.py --full --backup && \
git add docs/reports/maintenance-*.json && \
git commit -m "chore: monthly maintenance $(date +%Y-%m-%d)" && \
git push
```

## Testing & Development

### 16. Safe Testing

```bash
# Always use dry-run when testing
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose

# Test individual components
python scripts/utilities/repo-maintenance.py --dry-run --cleanup
python scripts/utilities/repo-maintenance.py --dry-run --archive
python scripts/utilities/repo-maintenance.py --health-check

# Verify no files changed
git status
```

### 17. Debugging

```bash
# Enable Python debugging
python -m pdb scripts/utilities/repo-maintenance.py --health-check

# Verbose logging
PYTHONVERBOSE=1 python scripts/utilities/repo-maintenance.py --health-check

# Check script with linter
pylint scripts/utilities/repo-maintenance.py

# Run with error tracing
python -u scripts/utilities/repo-maintenance.py --full --verbose 2>&1 | tee maintenance-debug.log
```

## Best Practices

### 18. Recommended Workflow

```bash
# 1. Regular (weekly) - quick check
python scripts/utilities/repo-maintenance.py --health-check

# 2. Monthly - full maintenance
python scripts/utilities/repo-maintenance.py --dry-run --full --verbose
# Review output, then:
python scripts/utilities/repo-maintenance.py --full --backup

# 3. Before release - comprehensive check
python scripts/utilities/repo-maintenance.py --health-check --verbose
# Fix any issues, then:
python scripts/utilities/repo-maintenance.py --cleanup

# 4. After major changes - verify health
git pull
python scripts/utilities/repo-maintenance.py --health-check
```

### 19. Monitoring Trends

```bash
# Create monthly report
cat > scripts/monthly-trend-report.sh << 'EOF'
#!/bin/bash
echo "=== Monthly Maintenance Trends ==="
echo ""
echo "SEO Drift Over Time:"
jq -r '[.timestamp[0:7], (.statistics.posts_with_seo_drift / .statistics.total_posts_checked * 100 | tostring)] | join(": ") + "%"' docs/reports/maintenance-*.json | sort

echo ""
echo "Temp Files Cleaned:"
jq -r '[.timestamp[0:7], .statistics.temp_files_removed | tostring] | join(": ")' docs/reports/maintenance-*.json | sort

echo ""
echo "Reports Archived:"
jq -r '[.timestamp[0:7], .statistics.reports_archived | tostring] | join(": ")' docs/reports/maintenance-*.json | sort
EOF

chmod +x scripts/monthly-trend-report.sh
./scripts/monthly-trend-report.sh
```

## Support & Troubleshooting

### 20. Common Issues

```bash
# Issue: Script not found
# Solution:
cd /home/william/git/williamzujkowski.github.io
ls -la scripts/utilities/repo-maintenance.py

# Issue: Import errors
# Solution:
pip install pyyaml requests

# Issue: Permission denied
# Solution:
chmod +x scripts/utilities/repo-maintenance.py

# Issue: MANIFEST.json errors
# Solution:
python scripts/utilities/repo-maintenance.py --health-check --verbose

# Issue: npm audit fails
# Solution:
npm install
npm audit fix
```

---

**More Examples**: See `docs/GUIDES/REPO_MAINTENANCE_GUIDE.md` for comprehensive documentation.
