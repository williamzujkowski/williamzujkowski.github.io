#!/bin/bash
# scripts/maintenance/archive-size-monitor.sh
# Archive size monitoring and alerting script
# Tracks archive growth and alerts on thresholds
# Part of Archive Rotation Policy v1.0.0

set -euo pipefail

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ARCHIVE_DIR="${REPO_ROOT}/docs/archive"
REPORTS_DIR="${REPO_ROOT}/docs/reports"
LOG_DIR="${REPO_ROOT}/logs"
HISTORY_FILE="${LOG_DIR}/archive-size-history.csv"
LOG_FILE="${LOG_DIR}/archive-size-monitor.log"

# Thresholds (in KB for precision)
WARN_THRESHOLD_KB=2048000   # 2.0M (80% of 2.5M target)
ALERT_THRESHOLD_KB=2560000  # 2.5M (90% of critical)
CRITICAL_THRESHOLD_KB=3072000  # 3.0M (100% - critical)

# Parse command line arguments
SHOW_TRENDS=false
VERBOSE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --trends)
      SHOW_TRENDS=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--trends] [-v|--verbose] [-h|--help]"
      echo ""
      echo "Options:"
      echo "  --trends      Show size trends over time"
      echo "  -v, --verbose Enable verbose output with file counts"
      echo "  -h, --help    Show this help message"
      echo ""
      echo "Thresholds:"
      echo "  Warning:  2.0M (80% of target)"
      echo "  Alert:    2.5M (90% of critical)"
      echo "  Critical: 3.0M (requires immediate action)"
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use -h or --help for usage information"
      exit 1
      ;;
  esac
done

# Setup logging directory
mkdir -p "$LOG_DIR"

# Initialize history file if it doesn't exist
if [ ! -f "$HISTORY_FILE" ]; then
  echo "date,archive_kb,reports_kb,total_kb,status" > "$HISTORY_FILE"
fi

# Logging function
log() {
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# Get directory size in KB
get_size_kb() {
  local dir=$1
  if [ -d "$dir" ]; then
    du -sk "$dir" 2>/dev/null | cut -f1
  else
    echo "0"
  fi
}

# Format KB to human readable
format_size() {
  local kb=$1
  if [ $kb -lt 1024 ]; then
    echo "${kb}K"
  elif [ $kb -lt 1048576 ]; then
    echo "$(awk "BEGIN {printf \"%.1f\", $kb/1024}")M"
  else
    echo "$(awk "BEGIN {printf \"%.2f\", $kb/1048576}")G"
  fi
}

# Get file count
get_file_count() {
  local dir=$1
  if [ -d "$dir" ]; then
    find "$dir" -type f | wc -l
  else
    echo "0"
  fi
}

# Determine status based on thresholds
get_status() {
  local total_kb=$1
  if [ $total_kb -ge $CRITICAL_THRESHOLD_KB ]; then
    echo "CRITICAL"
  elif [ $total_kb -ge $ALERT_THRESHOLD_KB ]; then
    echo "ALERT"
  elif [ $total_kb -ge $WARN_THRESHOLD_KB ]; then
    echo "WARNING"
  else
    echo "OK"
  fi
}

# Show trends from history
show_trends() {
  if [ ! -f "$HISTORY_FILE" ] || [ $(wc -l < "$HISTORY_FILE") -lt 2 ]; then
    echo "Insufficient historical data for trends"
    return
  fi

  echo ""
  echo "=== Size Trends (Last 10 Measurements) ==="
  echo ""
  printf "%-12s %-10s %-10s %-10s %-10s\n" "Date" "Archive" "Reports" "Total" "Status"
  printf "%-12s %-10s %-10s %-10s %-10s\n" "----" "-------" "-------" "-----" "------"

  tail -n 10 "$HISTORY_FILE" | while IFS=, read -r date archive reports total status; do
    if [ "$date" != "date" ]; then
      printf "%-12s %-10s %-10s %-10s %-10s\n" \
        "$date" \
        "$(format_size $archive)" \
        "$(format_size $reports)" \
        "$(format_size $total)" \
        "$status"
    fi
  done

  # Calculate growth rate
  local first_total=$(tail -n 10 "$HISTORY_FILE" | head -n 2 | tail -n 1 | cut -d, -f4)
  local last_total=$(tail -n 1 "$HISTORY_FILE" | cut -d, -f4)

  if [ -n "$first_total" ] && [ -n "$last_total" ] && [ "$first_total" != "total_kb" ]; then
    local growth=$((last_total - first_total))
    local growth_pct=$(awk "BEGIN {printf \"%.1f\", ($growth/$first_total)*100}")
    echo ""
    echo "Growth over period: $(format_size $growth) (${growth_pct}%)"
  fi
}

# Main execution
main() {
  local current_date=$(date +%Y-%m-%d)

  echo "Archive Size Monitor - $(date)"
  echo "================================"
  echo ""

  # Get current sizes
  local archive_kb=$(get_size_kb "$ARCHIVE_DIR")
  local reports_kb=$(get_size_kb "$REPORTS_DIR")
  local total_kb=$((archive_kb + reports_kb))

  # Determine status
  local status=$(get_status $total_kb)

  # Display current sizes
  echo "Current Sizes:"
  echo "  Archive: $(format_size $archive_kb)"
  echo "  Reports: $(format_size $reports_kb)"
  echo "  Total:   $(format_size $total_kb)"
  echo ""

  # Show thresholds
  echo "Thresholds:"
  echo "  Warning:  $(format_size $WARN_THRESHOLD_KB) (80%)"
  echo "  Alert:    $(format_size $ALERT_THRESHOLD_KB) (90%)"
  echo "  Critical: $(format_size $CRITICAL_THRESHOLD_KB) (100%)"
  echo ""

  # Verbose file counts
  if [ "$VERBOSE" = true ]; then
    echo "File Counts:"
    echo "  Archive: $(get_file_count "$ARCHIVE_DIR") files"
    echo "  Reports: $(get_file_count "$REPORTS_DIR") files"
    echo ""
  fi

  # Status display
  echo "Status: $status"

  case $status in
    CRITICAL)
      echo ""
      echo "🚨 CRITICAL: Archive size exceeds maximum threshold!"
      echo "   Total size $(format_size $total_kb) ≥ $(format_size $CRITICAL_THRESHOLD_KB)"
      echo ""
      echo "   IMMEDIATE ACTION REQUIRED:"
      echo "   1. Run quarterly rotation procedure"
      echo "   2. Review and delete old working documents"
      echo "   3. Compress old quarter directories"
      echo "   4. Consider moving historical content to separate repository"
      echo ""
      log "CRITICAL: Archive size $(format_size $total_kb) exceeds threshold"
      ;;
    ALERT)
      echo ""
      echo "⚠️  ALERT: Archive size approaching critical threshold"
      echo "   Total size $(format_size $total_kb) ≥ $(format_size $ALERT_THRESHOLD_KB)"
      echo ""
      echo "   ACTION RECOMMENDED:"
      echo "   1. Schedule quarterly rotation"
      echo "   2. Review files eligible for deletion"
      echo "   3. Plan compression of old archives"
      echo ""
      log "ALERT: Archive size $(format_size $total_kb) approaching threshold"
      ;;
    WARNING)
      echo ""
      echo "⚠️  WARNING: Archive size above warning threshold"
      echo "   Total size $(format_size $total_kb) ≥ $(format_size $WARN_THRESHOLD_KB)"
      echo ""
      echo "   CONSIDER:"
      echo "   1. Review upcoming rotation schedule"
      echo "   2. Identify candidates for early deletion"
      echo "   3. Monitor growth trend"
      echo ""
      log "WARNING: Archive size $(format_size $total_kb) above warning level"
      ;;
    OK)
      echo ""
      echo "✅ Archive size within acceptable range"
      log "OK: Archive size $(format_size $total_kb) within limits"
      ;;
  esac

  # Calculate percentage of critical threshold
  local pct_of_critical=$(awk "BEGIN {printf \"%.1f\", ($total_kb/$CRITICAL_THRESHOLD_KB)*100}")
  echo ""
  echo "Capacity: ${pct_of_critical}% of critical threshold"

  # Log to history
  echo "${current_date},${archive_kb},${reports_kb},${total_kb},${status}" >> "$HISTORY_FILE"

  # Show trends if requested
  if [ "$SHOW_TRENDS" = true ]; then
    show_trends
  fi

  echo ""
  echo "Full history: $HISTORY_FILE"
  echo "Run with --trends to see historical data"

  # Exit codes
  case $status in
    CRITICAL)
      exit 2  # Critical - requires immediate action
      ;;
    ALERT)
      exit 1  # Alert - action recommended
      ;;
    WARNING)
      exit 0  # Warning - monitor but no immediate action
      ;;
    OK)
      exit 0  # All good
      ;;
  esac
}

# Execute main function
main "$@"
