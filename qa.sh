#!/bin/bash

echo "🔍 Running QA checks for your 11ty website..."

# Check if node_modules and package-lock.json exist
if [ ! -d "node_modules" ] || [ ! -f "package-lock.json" ]; then
  echo "❌ node_modules or package-lock.json not found. Installing dependencies..."
  npm install
else
  echo "✅ node_modules and package-lock.json found"
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

# Check GitHub Actions workflow file
if [ -f ".github/workflows/deploy.yml" ]; then
  echo "✅ GitHub Actions workflow file found"
else
  echo "❌ GitHub Actions workflow file not found"
  exit 1
fi

echo "✅ QA checks completed successfully!"
echo "🚀 Run 'npm start' to preview the site locally"
echo "🌐 Run 'git push' to trigger GitHub deployment"
