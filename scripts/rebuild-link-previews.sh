#!/bin/bash

# Script to rebuild link previews with the new categorized system
# 
# This script will:
# 1. Remove old link previews data
# 2. Rebuild the link previews with the new categorized system
# 3. Run the build process to ensure the site works with the new system

echo "===== Link Preview Rebuild Tool ====="
echo "This will rebuild all link previews using the new categorized system."
echo "Make sure all screenshots already exist in the _data/screenshots directory."
echo ""

# Check if we're in the right directory
if [ ! -d "scripts" ] || [ ! -d "src" ]; then
  echo "ERROR: This script must be run from the root of the repository."
  exit 1
fi

# Remove old link previews data and ensure clean state
echo "Removing old link previews data..."
rm -f _data/link-previews*.json
rm -f assets/data/link-previews*.json
rm -f _site/assets/data/link-previews*.json

# Rebuild link previews
echo "Rebuilding link previews with new categorized system..."
LINK_PREVIEW_FORCE=true npm run build:links

# Create assets directory if it doesn't exist
mkdir -p assets/data

# Copy link preview files to assets directory
echo "Copying link preview files to assets directory..."
cp _data/link-previews*.json assets/data/

# Copy screenshots to assets directory if they exist
if [ -d "_data/screenshots" ]; then
  echo "Copying screenshots to assets directory..."
  mkdir -p assets/data/screenshots
  cp -r _data/screenshots/* assets/data/screenshots/
else
  echo "No screenshots directory found in _data. Skipping copy."
fi

# Build the site
echo "Building the site..."
npm run build

echo ""
echo "Done! The link previews have been rebuilt with the new categorized system."
echo "Check the links page to ensure everything is working correctly."