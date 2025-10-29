#!/bin/bash
###############################################################################
# Monthly Portfolio Validation Script
# Purpose: Automated monthly health checks with comprehensive reporting
# Schedule: First of every month at 2 AM (via cron)
# Maintainer: William Zujkowski
# Version: 1.0.0
###############################################################################

set -euo pipefail

# Configuration
REPO_DIR="${REPO_DIR:-/home/william/git/williamzujkowski.github.io}"
REPORT_DIR="$REPO_DIR/reports/monthly"
LOG_DIR="$REPO_DIR/logs"
CURRENT_MONTH=$(date +%Y-%m)
PREVIOUS_MONTH=$(date -d "last month" +%Y-%m)
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/monthly-validation.log"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" | tee -a "$LOG_DIR/monthly-validation.log" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*" | tee -a "$LOG_DIR/monthly-validation.log"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*" | tee -a "$LOG_DIR/monthly-validation.log"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p "$REPORT_DIR"
    mkdir -p "$LOG_DIR"
    success "Directories created"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if validator script exists
    if [ ! -f "$REPO_DIR/scripts/blog-content/humanization-validator.py" ]; then
        error "Validator script not found"
        exit 1
    fi

    # Check if jq is installed
    if ! command -v jq &> /dev/null; then
        error "jq is not installed. Install with: sudo apt-get install jq"
        exit 1
    fi

    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed"
        exit 1
    fi

    success "All prerequisites met"
}

# Run batch validation
run_validation() {
    log "Running batch validation for $CURRENT_MONTH..."

    cd "$REPO_DIR"

    if python3 scripts/blog-content/humanization-validator.py --batch \
        --save-report "$REPORT_DIR/validation-$CURRENT_MONTH.json" \
        --format json; then
        success "Validation completed successfully"
        return 0
    else
        error "Validation failed"
        return 1
    fi
}

# Compare with previous month
compare_with_previous() {
    log "Comparing with previous month ($PREVIOUS_MONTH)..."

    if [ ! -f "$REPORT_DIR/validation-$PREVIOUS_MONTH.json" ]; then
        warning "No previous month report found for comparison"
        return 0
    fi

    if python3 scripts/blog-content/humanization-validator.py --batch \
        --compare "$REPORT_DIR/validation-$PREVIOUS_MONTH.json" \
        > "$REPORT_DIR/comparison-$CURRENT_MONTH.txt" 2>&1; then
        success "Comparison completed"
    else
        warning "Comparison failed but continuing"
    fi
}

# Generate summary report
generate_summary() {
    log "Generating summary report..."

    local report_file="$REPORT_DIR/validation-$CURRENT_MONTH.json"
    local summary_file="$REPORT_DIR/summary-$CURRENT_MONTH.txt"

    if [ ! -f "$report_file" ]; then
        error "Report file not found: $report_file"
        return 1
    fi

    # Extract statistics
    local total=$(jq -r '.statistics.total_posts // 0' "$report_file")
    local passing=$(jq -r '.statistics.passed // 0' "$report_file")
    local failed=$(jq -r '.statistics.failed // 0' "$report_file")
    local avg_score=$(jq -r '.statistics.avg_score // 0' "$report_file")

    # Create summary
    cat > "$summary_file" <<EOF
╔════════════════════════════════════════════════════════════════╗
║         Portfolio Health Report - $CURRENT_MONTH                  ║
╚════════════════════════════════════════════════════════════════╝

Generated: $(date +'%Y-%m-%d %H:%M:%S')
Report Period: $CURRENT_MONTH

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OVERALL STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Posts:        $total
Passing Posts:      $passing
Failing Posts:      $failed
Average Score:      $avg_score

Pass Rate:          $(awk "BEGIN {printf \"%.1f%%\", ($passing/$total)*100}")

EOF

    # Add alerts if there are failing posts
    if [ "$failed" -gt 0 ]; then
        cat >> "$summary_file" <<EOF

⚠️  ALERT: $failed posts failing validation!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FAILING POSTS (Score < 75)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
        jq -r '.results[] | select(.score < 75) | "\(.post_path) - Score: \(.score)"' "$report_file" >> "$summary_file"

        cat >> "$summary_file" <<EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ACTION REQUIRED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Please review and improve the failing posts to maintain portfolio quality.

Run detailed validation:
    python3 scripts/blog-content/humanization-validator.py --post <path>

EOF
    else
        cat >> "$summary_file" <<EOF

✅ All posts passing validation!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
QUALITY BREAKDOWN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

EOF
        jq -r '.results[] | "\(.post_path) - Score: \(.score)"' "$report_file" | sort -t: -k2 -rn >> "$summary_file"
    fi

    # Add comparison if available
    if [ -f "$REPORT_DIR/comparison-$CURRENT_MONTH.txt" ]; then
        cat >> "$summary_file" <<EOF

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPARISON WITH PREVIOUS MONTH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$(cat "$REPORT_DIR/comparison-$CURRENT_MONTH.txt")

EOF
    fi

    # Add footer
    cat >> "$summary_file" <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Full report available at:
    $report_file

Generated by: monthly-portfolio-validation.sh
Documentation: docs/guides/MONTHLY_VALIDATION_SETUP.md

EOF

    success "Summary report generated: $summary_file"
}

# Send email notification (optional)
send_notification() {
    log "Checking for email notification setup..."

    local summary_file="$REPORT_DIR/summary-$CURRENT_MONTH.txt"
    local failed=$(jq -r '.statistics.failed // 0' "$REPORT_DIR/validation-$CURRENT_MONTH.json")

    # Check if mail command is available and EMAIL is set
    if command -v mail &> /dev/null && [ -n "${EMAIL:-}" ]; then
        log "Sending email notification to $EMAIL..."

        if [ "$failed" -gt 0 ]; then
            local subject="⚠️  Portfolio Validation Alert - $failed posts failing"
        else
            local subject="✅ Portfolio Validation Success - All posts passing"
        fi

        if mail -s "$subject" "$EMAIL" < "$summary_file"; then
            success "Email notification sent"
        else
            warning "Failed to send email notification"
        fi
    else
        log "Email notifications not configured (set EMAIL environment variable)"
    fi
}

# Archive old reports (keep last 12 months)
archive_old_reports() {
    log "Archiving old reports..."

    local cutoff_date=$(date -d "12 months ago" +%Y-%m)
    local archived=0

    for report in "$REPORT_DIR"/validation-*.json; do
        if [ -f "$report" ]; then
            local report_month=$(basename "$report" | sed 's/validation-\(.*\)\.json/\1/')
            if [[ "$report_month" < "$cutoff_date" ]]; then
                log "Archiving report: $report"
                gzip "$report" 2>/dev/null || true
                ((archived++))
            fi
        fi
    done

    if [ $archived -gt 0 ]; then
        success "Archived $archived old reports"
    else
        log "No old reports to archive"
    fi
}

# Generate quick stats
generate_quick_stats() {
    local report_file="$REPORT_DIR/validation-$CURRENT_MONTH.json"

    if [ ! -f "$report_file" ]; then
        return
    fi

    local total=$(jq -r '.statistics.total_posts // 0' "$report_file")
    local passing=$(jq -r '.statistics.passed // 0' "$report_file")
    local failed=$(jq -r '.statistics.failed // 0' "$report_file")
    local avg_score=$(jq -r '.statistics.avg_score // 0' "$report_file")

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "QUICK STATS - $CURRENT_MONTH"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Total: $total | Passing: $passing | Failing: $failed | Avg: $avg_score"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
}

# Main execution
main() {
    log "Starting monthly portfolio validation..."
    log "Month: $CURRENT_MONTH"
    log "Repository: $REPO_DIR"

    # Execute validation pipeline
    create_directories
    check_prerequisites

    if run_validation; then
        compare_with_previous
        generate_summary
        generate_quick_stats
        send_notification
        archive_old_reports

        success "Monthly validation completed successfully"
        log "Reports saved to: $REPORT_DIR"
        log "Summary: $REPORT_DIR/summary-$CURRENT_MONTH.txt"

        # Display summary file
        cat "$REPORT_DIR/summary-$CURRENT_MONTH.txt"

        exit 0
    else
        error "Monthly validation failed"
        exit 1
    fi
}

# Run main function
main "$@"
