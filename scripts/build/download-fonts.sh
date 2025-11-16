#!/bin/bash
# Download and prepare self-hosted fonts
# This script downloads fonts from Google Fonts for self-hosting

set -e

FONTS_DIR="/home/william/git/williamzujkowski.github.io/src/assets/fonts"

echo "📥 Downloading fonts for self-hosting..."
echo "Target directory: $FONTS_DIR"

# Note: For production, you should:
# 1. Download fonts from Google Fonts
# 2. Use a tool like glyphhanger or fonttools to subset
# 3. Convert to woff2 format
# 4. Include only Latin basic (U+0020-007F) for optimal size

# For now, we'll document the process and use Google Fonts CDN
# Full implementation requires:
# - npm install -g glyphhanger
# - pyftsubset (from fonttools)

echo "⚠️  Font subsetting requires additional tools:"
echo "   npm install -g glyphhanger"
echo "   pip install fonttools brotli"
echo ""
echo "Manual process:"
echo "1. Download fonts from Google Fonts"
echo "2. Subset with: pyftsubset font.ttf --output-file=font.woff2 --flavor=woff2 --unicodes=U+0020-007F"
echo "3. Place in $FONTS_DIR"
echo ""
echo "For this implementation, we'll use a simplified approach with preload hints"

exit 0
