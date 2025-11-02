#!/bin/bash
# Continuous Build and Metadata Monitoring Script
# Watches for file changes and validates on save

set -e

POSTS_DIR="src/posts"
WATCH_DELAY=2
LOG_FILE=".validation-monitor.log"

echo "🔍 Starting continuous validation monitor..."
echo "Watching: $POSTS_DIR"
echo "Press Ctrl+C to stop"
echo ""

# Initial validation
echo "📊 Running initial validation..."
uv run python scripts/validation/metadata-validator.py || true
echo ""

# Watch for changes using inotifywait if available
if command -v inotifywait &> /dev/null; then
    echo "✅ Using inotifywait for file monitoring"
    inotifywait -m -e modify,create,delete -r "$POSTS_DIR" --format '%w%f %e' |
    while read -r file event; do
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Detected $event: $file" | tee -a "$LOG_FILE"

        # Debounce - wait for file operations to complete
        sleep $WATCH_DELAY

        # Validate the specific file if it's a markdown file
        if [[ "$file" == *.md ]]; then
            echo "🔄 Validating metadata for: $(basename "$file")"
            uv run python scripts/validation/metadata-validator.py --format json | jq "."
            echo ""
        fi
    done
else
    echo "⚠️  inotifywait not available, falling back to polling"
    echo "Install inotify-tools for better performance: sudo apt-get install inotify-tools"
    echo ""

    # Fallback to simple polling
    LAST_HASH=""
    while true; do
        CURRENT_HASH=$(find "$POSTS_DIR" -type f -name "*.md" -exec md5sum {} \; | sort | md5sum)

        if [ "$CURRENT_HASH" != "$LAST_HASH" ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] Changes detected in $POSTS_DIR" | tee -a "$LOG_FILE"
            echo "🔄 Running validation..."
            uv run python scripts/validation/metadata-validator.py || true
            echo ""
            LAST_HASH="$CURRENT_HASH"
        fi

        sleep $WATCH_DELAY
    done
fi
