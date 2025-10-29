#!/bin/bash
# Test script for citation validation workflow
# Simulates what the GitHub Action will run

set -e

echo "🧪 Testing Citation Validation Workflow"
echo "========================================"
echo ""

# Clean up any previous test files
rm -f test-citation-links.json test-citation-validation.json test-citation-report.md

echo "📋 Step 1: Extract citation links"
python scripts/link-validation/link-extractor.py \
    --posts-dir src/posts \
    --output test-citation-links.json \
    --citations-only

if [ ! -f test-citation-links.json ]; then
    echo "❌ Failed to extract citation links"
    exit 1
fi

# Count total citations
TOTAL_CITATIONS=$(jq '.links | length' test-citation-links.json)
echo "✅ Found $TOTAL_CITATIONS citation links"
echo ""

if [ "$TOTAL_CITATIONS" -eq 0 ]; then
    echo "⚠️  No citation links found. Skipping validation."
    exit 0
fi

echo "🔍 Step 2: Validate citation links"
python scripts/link-validation/link-validator.py \
    --input test-citation-links.json \
    --output test-citation-validation.json \
    --max-retries 3 \
    --timeout 30

if [ ! -f test-citation-validation.json ]; then
    echo "❌ Failed to validate citation links"
    exit 1
fi

# Check if any broken links found
BROKEN_COUNT=$(jq '[.results[] | select(.status == "broken")] | length' test-citation-validation.json)
VALID_COUNT=$(jq '.stats.valid' test-citation-validation.json)
REDIRECT_COUNT=$(jq '.stats.redirects' test-citation-validation.json)
TIMEOUT_COUNT=$(jq '.stats.timeouts' test-citation-validation.json)
ERROR_COUNT=$(jq '.stats.errors' test-citation-validation.json)

echo "✅ Validation complete:"
echo "   Valid: $VALID_COUNT"
echo "   Broken: $BROKEN_COUNT"
echo "   Redirects: $REDIRECT_COUNT"
echo "   Timeouts: $TIMEOUT_COUNT"
echo "   Errors: $ERROR_COUNT"
echo ""

if [ "$BROKEN_COUNT" -gt 0 ]; then
    echo "📝 Step 3: Generate report"
    python scripts/link-validation/citation-report.py \
        --input test-citation-validation.json \
        --links test-citation-links.json \
        --output test-citation-report.md

    if [ ! -f test-citation-report.md ]; then
        echo "❌ Failed to generate report"
        exit 1
    fi

    echo "✅ Report generated: test-citation-report.md"
    echo ""
    echo "📄 Report Preview:"
    echo "=================="
    head -n 30 test-citation-report.md
    echo ""
    echo "⚠️  Found broken citation links! See full report in test-citation-report.md"
    exit 1
else
    echo "✅ All citation links are valid!"
    exit 0
fi
