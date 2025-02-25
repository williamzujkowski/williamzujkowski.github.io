#!/bin/bash

echo "🔍 Running QA checks for your 11ty website..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
  echo "❌ node_modules not found. Installing dependencies..."
  npm install
else
  echo "✅ node_modules found"
fi

# Clean the build directory
echo "🧹 Cleaning build directory..."
npm run clean

# Build the site
echo "🏗️ Building site..."
npm run build

if [ $? -eq 0 ]; then
  echo "✅ Build successful!"
else
  echo "❌ Build failed!"
  exit 1
fi

# Count generated files
FILE_COUNT=$(find _site -type f | wc -l)
echo "📊 Generated $FILE_COUNT files in _site directory"

echo "✅ QA checks completed successfully!"
echo "🚀 Run 'npm start' to preview the site locally"
echo "🌐 Run 'git push' to trigger GitHub deployment (if configured)"
