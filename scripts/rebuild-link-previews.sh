#!/bin/bash

# rebuild-link-previews.sh
# Script to generate link preview metadata for the website
# This script uses the link-preview-generator.js file to build preview data

# Set variables
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if node is installed
if ! command -v node &> /dev/null; then
  echo "Error: Node.js is required but not installed."
  exit 1
fi

# Run the link preview generator
echo "Generating link previews..."
node "$SCRIPT_DIR/link-previews/link-preview-generator.js"

# Check the result
if [ $? -eq 0 ]; then
  echo "Link previews generated successfully!"
else
  echo "Error generating link previews."
  exit 1
fi

echo "Done!"