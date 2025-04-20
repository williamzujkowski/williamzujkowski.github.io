#!/bin/bash

# Set up a cron job to schedule vulnerability posts
# This script will add a daily cron job to check if a new post should be generated

# Path to the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Create the cron job line - run daily at 8 AM
CRON_JOB="0 8 * * * cd $SCRIPT_DIR && node schedule-posts.js >> $SCRIPT_DIR/cron.log 2>&1"

# Check if the cron job already exists
if (crontab -l 2>/dev/null | grep -q "schedule-posts.js"); then
  echo "Cron job already exists."
else
  # Add the new cron job
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
  echo "Cron job added. It will run daily at 8 AM."
fi

echo "To remove the cron job, use: crontab -e"
