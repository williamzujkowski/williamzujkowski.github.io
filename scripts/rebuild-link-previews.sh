#!/bin/bash

# Script to rebuild link previews with the new categorized system
# 
# This script will:
# 1. Remove old link previews data
# 2. Rebuild the link previews with the new categorized system
# 3. Run the build process to ensure the site works with the new system

echo "===== Link Preview Rebuild Tool ====="
echo "This will rebuild all link previews using the new categorized system."
echo "The link preview data is now stored directly in assets/data."
echo ""

# Check if we're in the right directory
if [ ! -d "scripts" ] || [ ! -d "src" ]; then
  echo "ERROR: This script must be run from the root of the repository."
  exit 1
fi

# Remove old link previews data and ensure clean state
echo "Removing old link previews data..."
# Remove any vestigial files from _data directory (legacy)
rm -f _data/link-previews*.json
# Remove from assets directory (current location)
rm -f assets/data/link-previews*.json
# Remove from _site if it exists
rm -f _site/assets/data/link-previews*.json

# Create assets directory if it doesn't exist
mkdir -p assets/data

# Rebuild link previews directly to assets/data
echo "Rebuilding link previews with new categorized system..."
LINK_PREVIEW_TARGET="./assets/data" LINK_PREVIEW_FORCE=true npm run build:links

# Copy screenshots to assets directory if they exist in legacy location
if [ -d "_data/screenshots" ]; then
  echo "Copying screenshots from legacy _data/screenshots to assets/data/screenshots..."
  mkdir -p assets/data/screenshots
  cp -r _data/screenshots/* assets/data/screenshots/
  echo "Note: Consider moving screenshot generation to directly use assets/data/screenshots"
else
  echo "No legacy screenshots directory found in _data."
fi

# Build the site
echo "Building the site..."
npm run build

echo ""
echo "Done! The link previews have been rebuilt with the new categorized system."
echo "Check the links page to ensure everything is working correctly."