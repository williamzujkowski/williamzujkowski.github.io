#!/bin/bash
# scripts/maintenance/weekly-cleanup.sh
# Weekly archive cleanup script
# Deletes test reports >7 days old and warns about old working drafts
# Part of Archive Rotation Policy v1.0.0

set -euo pipefail

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TESTING_DIR="${REPO_ROOT}/docs/testing"
DOCS_DIR="${REPO_ROOT}/docs"
LOG_DIR="${REPO_ROOT}/logs"
LOG_FILE="${LOG_DIR}/weekly-cleanup.log"
DRY_RUN=false
VERBOSE=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    -h|--help)
      echo "Usage: $0 [--dry-run] [-v|--verbose] [-h|--help]"
      echo ""
      echo "Options:"
      echo "  --dry-run     Show what would be deleted without deleting"
      echo "  -v, --verbose Enable verbose output"
      echo "  -h, --help    Show this help message"
      echo ""
      echo "Description:"
      echo "  Deletes test reports older than 7 days"
      echo "  Warns about working drafts older than 30 days"
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

# Logging function
log() {
  local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
  echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# Error handling
error() {
  log "ERROR: $1"
  exit 1
}

# Main execution
main() {
  log "=== Weekly Archive Cleanup ==="
  log "Date: $(date)"
  log "Dry run: $DRY_RUN"
  log "Verbose: $VERBOSE"
  log "Repository root: $REPO_ROOT"

  # Check if testing directory exists
  if [ ! -d "$TESTING_DIR" ]; then
    log "Testing directory does not exist: $TESTING_DIR"
    log "Skipping test report cleanup"
  else
    # Find test reports older than 7 days
    log "Scanning for test reports older than 7 days..."

    local test_reports=()
    while IFS= read -r -d '' file; do
      test_reports+=("$file")
    done < <(find "$TESTING_DIR" -type f -name "*.md" -mtime +7 -print0 2>/dev/null)

    local deleted_count=${#test_reports[@]}

    if [ $deleted_count -eq 0 ]; then
      log "No test reports older than 7 days found"
    else
      log "Found $deleted_count test reports to delete"

      if [ "$VERBOSE" = true ]; then
        for file in "${test_reports[@]}"; do
          local age_days=$(( ($(date +%s) - $(stat -c %Y "$file")) / 86400 ))
          log "  - $(basename "$file") (${age_days} days old)"
        done
      fi

      if [ "$DRY_RUN" = true ]; then
        log "DRY RUN: Would delete $deleted_count test reports"
      else
        for file in "${test_reports[@]}"; do
          rm "$file" && log "Deleted: $(basename "$file")"
        done
        log "Deleted $deleted_count test reports"
      fi
    fi
  fi

  # Find working drafts older than 30 days
  log "Scanning for working drafts older than 30 days..."

  local old_drafts=()
  while IFS= read -r -d '' file; do
    old_drafts+=("$file")
  done < <(find "$DOCS_DIR" -type f \( -name "*-working-*.md" -o -name "*-draft-*.md" \) -mtime +30 -print0 2>/dev/null)

  local draft_count=${#old_drafts[@]}

  if [ $draft_count -eq 0 ]; then
    log "No old working drafts found"
  else
    log "WARNING: Found $draft_count working drafts older than 30 days"
    log "These files should be reviewed for archival or deletion:"

    for file in "${old_drafts[@]}"; do
      local age_days=$(( ($(date +%s) - $(stat -c %Y "$file")) / 86400 ))
      local rel_path="${file#$REPO_ROOT/}"
      log "  ⚠️  $rel_path (${age_days} days old)"
    done

    log ""
    log "Action required: Review and either:"
    log "  1. Move to appropriate archive location"
    log "  2. Delete if no longer needed"
    log "  3. Rename to remove -working/-draft suffix if keeping active"
  fi

  # Find pre-analysis files older than 60 days (2 quarters)
  log "Scanning for pre-analysis files older than 60 days..."

  local pre_analysis=()
  while IFS= read -r -d '' file; do
    pre_analysis+=("$file")
  done < <(find "$DOCS_DIR/archive" -type f -name "*-pre-analysis.md" -mtime +60 -print0 2>/dev/null)

  local pre_analysis_count=${#pre_analysis[@]}

  if [ $pre_analysis_count -eq 0 ]; then
    log "No old pre-analysis files found"
  else
    log "Found $pre_analysis_count pre-analysis files eligible for deletion"

    if [ "$VERBOSE" = true ]; then
      for file in "${pre_analysis[@]}"; do
        local rel_path="${file#$REPO_ROOT/}"
        log "  - $rel_path"
      done
    fi

    log "Note: Pre-analysis files can be safely deleted after 60 days per policy"
  fi

  # Summary
  log ""
  log "=== Cleanup Summary ==="
  log "Test reports deleted: $deleted_count"
  log "Old working drafts (needs review): $draft_count"
  log "Old pre-analysis files (eligible for deletion): $pre_analysis_count"
  log ""
  log "Cleanup complete"

  # Exit with warning code if old drafts found
  if [ $draft_count -gt 0 ]; then
    exit 2  # Warning: action required
  fi
}

# Execute main function
main "$@"
