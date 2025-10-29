#!/bin/bash
# Simple focused test for humanization pre-commit hook

set -e

REPO_ROOT="/home/william/git/williamzujkowski.github.io"
cd "$REPO_ROOT"

echo "🧪 Testing Humanization Pre-commit Hook"
echo "========================================"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo "Test 1: Create low-scoring post (should fail)"
echo "----------------------------------------------"

# Create a low-scoring test post
TEST_POST="src/posts/2025-10-28-test-low-score-hook.md"
cat > "$TEST_POST" << 'EOF'
---
title: "Test Post for Hook Validation"
date: 2025-10-28
description: "Test post with low humanization score"
tags: [test]
---

# Enterprise Solutions

Leveraging cutting-edge technologies revolutionizes enterprise deployments; moreover, our robust solution seamlessly integrates with existing infrastructure—providing unprecedented performance and scalability.

The innovative platform delivers best-in-class results through paradigm-shifting methodologies that streamline workflows and optimize operational efficiency.
EOF

# Check the score
echo "Checking score..."
SCORE=$(python scripts/blog-content/humanization-validator.py --post "$TEST_POST" --output json 2>/dev/null | jq -r '.score // 0')
echo "Score: $SCORE/100"

if (( $(echo "$SCORE < 75" | bc -l) )); then
    echo -e "${GREEN}✅ Post scores below 75 as expected${NC}"

    # Stage the file
    git add "$TEST_POST"

    # Try to commit (should fail)
    echo "Attempting commit (should be blocked)..."
    set +e
    .git/hooks/pre-commit 2>&1
    EXIT_CODE=$?
    set -e

    if [ $EXIT_CODE -ne 0 ]; then
        echo -e "${GREEN}✅ PASSED: Hook correctly blocked low-scoring post${NC}"
        RESULT="PASS"
    else
        echo -e "${RED}❌ FAILED: Hook did not block low-scoring post${NC}"
        RESULT="FAIL"
    fi

    # Cleanup
    git reset HEAD "$TEST_POST" --quiet
    rm -f "$TEST_POST"
else
    echo -e "${YELLOW}⚠️  Post scored too high ($SCORE), cannot test blocking${NC}"
    RESULT="SKIP"
fi

echo ""
echo "Test 2: Modify high-scoring post (should pass)"
echo "----------------------------------------------"

# Find an existing post
EXISTING_POST=$(ls src/posts/*.md | grep -v welcome | head -1)

if [ -f "$EXISTING_POST" ]; then
    # Check its score
    SCORE=$(python scripts/blog-content/humanization-validator.py --post "$EXISTING_POST" --output json 2>/dev/null | jq -r '.score // 0')
    echo "Testing with: $EXISTING_POST"
    echo "Score: $SCORE/100"

    if (( $(echo "$SCORE >= 75" | bc -l) )); then
        # Make a trivial change
        echo "" >> "$EXISTING_POST"
        git add "$EXISTING_POST"

        # Try to commit (should pass)
        echo "Attempting commit (should pass)..."
        set +e
        .git/hooks/pre-commit 2>&1
        EXIT_CODE=$?
        set -e

        if [ $EXIT_CODE -eq 0 ]; then
            echo -e "${GREEN}✅ PASSED: Hook allowed high-scoring post${NC}"
            RESULT2="PASS"
        else
            echo -e "${RED}❌ FAILED: Hook blocked high-scoring post${NC}"
            RESULT2="FAIL"
        fi

        # Cleanup
        git reset HEAD "$EXISTING_POST" --quiet
        git checkout -- "$EXISTING_POST" --quiet
    else
        echo -e "${YELLOW}⚠️  Post scores too low ($SCORE), skipping test${NC}"
        RESULT2="SKIP"
    fi
else
    echo -e "${YELLOW}⚠️  No existing posts found${NC}"
    RESULT2="SKIP"
fi

echo ""
echo "Test 3: No blog posts modified (should skip check)"
echo "---------------------------------------------------"

# Reset everything
git reset --quiet 2>/dev/null || true

# Try hook with no staged changes
echo "Running hook with no staged changes..."
set +e
.git/hooks/pre-commit 2>&1
EXIT_CODE=$?
set -e

if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ PASSED: Hook works with no changes${NC}"
    RESULT3="PASS"
else
    echo -e "${RED}❌ FAILED: Hook failed with no changes${NC}"
    RESULT3="FAIL"
fi

echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo "Test 1 (Block low score): $RESULT"
echo "Test 2 (Allow high score): $RESULT2"
echo "Test 3 (No changes): $RESULT3"
echo ""

if [ "$RESULT" = "PASS" ] && [ "$RESULT2" = "PASS" ] && [ "$RESULT3" = "PASS" ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests were skipped or failed${NC}"
    exit 1
fi
