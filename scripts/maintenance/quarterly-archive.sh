#!/bin/bash
# scripts/maintenance/quarterly-archive.sh
# Quarterly archive rotation script
# Moves reports >90 days old to quarterly archive directories
# Part of Archive Rotation Policy v1.0.0

set -euo pipefail

# Configuration
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
REPORTS_DIR="${REPO_ROOT}/docs/reports"
ARCHIVE_ROOT="${REPO_ROOT}/docs/archive"
LOG_DIR="${REPO_ROOT}/logs"
LOG_FILE="${LOG_DIR}/quarterly-archive.log"
DRY_RUN=false
VERBOSE=false
RETENTION_DAYS=90  # 2 quarters = 180 days, but policy says >90 for initial check

# Parse command line arguments
QUARTER=""

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
    -d|--days)
      RETENTION_DAYS="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 YYYY-QX [--dry-run] [-v|--verbose] [-d|--days N] [-h|--help]"
      echo ""
      echo "Arguments:"
      echo "  YYYY-QX       Quarter identifier (e.g., 2026-Q1)"
      echo ""
      echo "Options:"
      echo "  --dry-run     Show what would be moved without moving"
      echo "  -v, --verbose Enable verbose output"
      echo "  -d, --days N  Days for retention threshold (default: 90)"
      echo "  -h, --help    Show this help message"
      echo ""
      echo "Description:"
      echo "  Moves reports older than N days to quarterly archive"
      echo "  Creates archive directory structure automatically"
      echo "  Generates README.md in archive directory"
      echo ""
      echo "Examples:"
      echo "  $0 2026-Q1                    # Archive to 2026-Q1"
      echo "  $0 2026-Q1 --dry-run          # Preview what would be archived"
      echo "  $0 2026-Q1 -d 180 -v          # Archive files >180 days with verbose output"
      exit 0
      ;;
    *)
      if [ -z "$QUARTER" ]; then
        QUARTER="$1"
      else
        echo "Unknown option: $1"
        echo "Use -h or --help for usage information"
        exit 1
      fi
      shift
      ;;
  esac
done

# Validate quarter argument
if [ -z "$QUARTER" ]; then
  echo "Error: Quarter argument required (e.g., 2026-Q1)"
  echo "Use -h or --help for usage information"
  exit 1
fi

if ! [[ "$QUARTER" =~ ^[0-9]{4}-Q[1-4]$ ]]; then
  echo "Error: Invalid quarter format. Use YYYY-QX (e.g., 2026-Q1)"
  exit 1
fi

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

# Validate file should be archived (not a completion or strategic report)
should_archive() {
  local file=$1
  local basename=$(basename "$file")

  # Never archive these high-value files
  if [[ "$basename" =~ (PHASE.*_COMPLETION_REPORT|batch-.*-completion|LESSONS_LEARNED|legacy-.*|README) ]]; then
    return 1
  fi

  # Always archive these file types
  if [[ "$basename" =~ (-analysis-report|-optimization-|-assessment|-validation-|-standardization-report) ]]; then
    return 0
  fi

  # Default: archive report files
  if [[ "$basename" =~ -report\.md$ ]]; then
    return 0
  fi

  return 1
}

# Get file category for reporting
get_file_category() {
  local file=$1
  local basename=$(basename "$file")

  if [[ "$basename" =~ -analysis ]]; then
    echo "analysis"
  elif [[ "$basename" =~ -optimization ]]; then
    echo "optimization"
  elif [[ "$basename" =~ -validation ]]; then
    echo "validation"
  elif [[ "$basename" =~ -assessment ]]; then
    echo "assessment"
  elif [[ "$basename" =~ -standardization ]]; then
    echo "standardization"
  else
    echo "other"
  fi
}

# Main execution
main() {
  local archive_dir="${ARCHIVE_ROOT}/${QUARTER}"

  log "=== Quarterly Archive: $QUARTER ==="
  log "Date: $(date)"
  log "Dry run: $DRY_RUN"
  log "Verbose: $VERBOSE"
  log "Retention threshold: $RETENTION_DAYS days"
  log "Source: $REPORTS_DIR"
  log "Destination: $archive_dir"

  # Check if reports directory exists
  if [ ! -d "$REPORTS_DIR" ]; then
    error "Reports directory does not exist: $REPORTS_DIR"
  fi

  # Create archive directory
  if [ "$DRY_RUN" = false ]; then
    mkdir -p "$archive_dir"
    log "Created archive directory: $archive_dir"
  else
    log "DRY RUN: Would create directory: $archive_dir"
  fi

  # Find eligible reports
  log "Scanning for reports older than $RETENTION_DAYS days..."

  local eligible_files=()
  local skipped_files=()
  declare -A category_counts=(
    ["analysis"]=0
    ["optimization"]=0
    ["validation"]=0
    ["assessment"]=0
    ["standardization"]=0
    ["other"]=0
  )

  while IFS= read -r -d '' file; do
    if should_archive "$file"; then
      eligible_files+=("$file")
      local category=$(get_file_category "$file")
      ((category_counts[$category]++))
    else
      skipped_files+=("$file")
    fi
  done < <(find "$REPORTS_DIR" -maxdepth 1 -type f -name "*.md" -mtime +$RETENTION_DAYS -print0 2>/dev/null)

  local total_eligible=${#eligible_files[@]}
  local total_skipped=${#skipped_files[@]}

  log "Found $total_eligible files eligible for archival"
  log "Skipped $total_skipped high-value files (completion reports, etc.)"

  # Show category breakdown
  if [ $total_eligible -gt 0 ]; then
    log ""
    log "Files by category:"
    for category in "${!category_counts[@]}"; do
      local count=${category_counts[$category]}
      if [ $count -gt 0 ]; then
        log "  $category: $count"
      fi
    done
  fi

  # Show skipped files if verbose
  if [ "$VERBOSE" = true ] && [ $total_skipped -gt 0 ]; then
    log ""
    log "Skipped high-value files:"
    for file in "${skipped_files[@]}"; do
      log "  ⊗ $(basename "$file")"
    done
  fi

  # Process eligible files
  if [ $total_eligible -eq 0 ]; then
    log ""
    log "No files to archive"

    if [ "$DRY_RUN" = false ]; then
      # Create README even if no files moved
      create_readme "$archive_dir" 0
    fi

    log "Archive operation complete (no files moved)"
    exit 0
  fi

  log ""
  if [ "$DRY_RUN" = true ]; then
    log "DRY RUN: Would move the following files to $archive_dir:"
  else
    log "Moving files to archive:"
  fi

  local moved_count=0
  for file in "${eligible_files[@]}"; do
    local basename=$(basename "$file")
    local age_days=$(( ($(date +%s) - $(stat -c %Y "$file")) / 86400 ))
    local category=$(get_file_category "$file")

    if [ "$VERBOSE" = true ]; then
      log "  → $basename (${age_days} days old, category: $category)"
    else
      log "  → $basename"
    fi

    if [ "$DRY_RUN" = false ]; then
      if mv "$file" "$archive_dir/"; then
        ((moved_count++))
      else
        log "  ERROR: Failed to move $basename"
      fi
    else
      ((moved_count++))
    fi
  done

  # Create README
  if [ "$DRY_RUN" = false ]; then
    create_readme "$archive_dir" $moved_count
    log "Created README.md in archive directory"
  fi

  # Summary
  log ""
  log "=== Archive Summary ==="
  log "Quarter: $QUARTER"
  log "Files moved: $moved_count"
  log "Files skipped (high-value): $total_skipped"
  log "Retention threshold: $RETENTION_DAYS days"

  if [ "$DRY_RUN" = true ]; then
    log ""
    log "DRY RUN COMPLETE - No files were actually moved"
    log "Run without --dry-run to execute the archival"
  else
    log ""
    log "Archive operation complete"
  fi
}

# Create README.md in archive directory
create_readme() {
  local archive_dir=$1
  local file_count=$2
  local readme_file="${archive_dir}/README.md"

  cat > "$readme_file" <<EOF
# $QUARTER Archive

**Archived on:** $(date '+%Y-%m-%d %H:%M:%S')
**Files archived:** $file_count
**Retention threshold:** $RETENTION_DAYS days

## Overview

This directory contains reports and documents from $QUARTER that have exceeded their active retention period but retain historical value for analysis and reference.

## Contents

Files in this archive include:
- Analysis reports (retention: 2 quarters)
- Optimization reports (retention: 2 quarters)
- Validation summaries (retention: 1 quarter)
- Assessment reports (retention: 2 quarters)
- Standardization reports (retention: 2 quarters)

## Policy

This archive follows the retention policies defined in:
\`docs/policies/ARCHIVE_ROTATION_POLICY.md\`

**Key policy points:**
- Reports archived after 2 quarters (180 days) in active directory
- Archive retention: 4 quarters before compression/selective deletion
- Completion reports and strategic documents kept indefinitely
- Working documents deleted after 30 days

## Accessing Archived Content

All files remain accessible in this directory. For historical analysis or reference:

1. Browse files directly in this directory
2. Search within files using grep or similar tools
3. Refer to \`MANIFEST.json\` for full repository inventory

## Next Review

This archive will be reviewed in $(date -d "+90 days" '+%Y-%m-%d') for:
- Compression opportunities
- Selective deletion of low-value content
- Migration to long-term storage if needed

## Related Archives

- Previous quarters: \`docs/archive/YYYY-QX/\`
- Legacy documentation: \`docs/archive/legacy-*.md\`
- Active reports: \`docs/reports/\`

---

*This README was automatically generated by \`scripts/maintenance/quarterly-archive.sh\`*
EOF
}

# Execute main function
main "$@"
