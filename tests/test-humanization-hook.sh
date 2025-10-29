#!/bin/bash
# Test script for humanization pre-commit hook
# Tests various scenarios to ensure hook works correctly

set -e

REPO_ROOT="/home/william/git/williamzujkowski.github.io"
cd "$REPO_ROOT"

echo "🧪 Testing Humanization Pre-commit Hook"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper function to run test
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_exit_code="$3"

    echo ""
    echo "📋 Test: $test_name"
    echo "---"

    # Run command and capture exit code
    set +e
    eval "$test_command"
    actual_exit_code=$?
    set -e

    if [ "$actual_exit_code" -eq "$expected_exit_code" ]; then
        echo -e "${GREEN}✅ PASSED${NC} (exit code: $actual_exit_code)"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAILED${NC} (expected exit code: $expected_exit_code, got: $actual_exit_code)"
        ((TESTS_FAILED++))
    fi
}

# Test 1: No blog posts modified (should skip humanization check)
echo ""
echo "========================================="
echo "Test 1: No blog posts modified"
echo "========================================="
git stash --quiet 2>/dev/null || true
run_test "No modifications" "git diff --cached --name-only | grep -q 'src/posts/.*\.md' && echo 'Posts found' || echo 'No posts'" 1

# Test 2: Modify a high-scoring post (should pass)
echo ""
echo "========================================="
echo "Test 2: High-scoring post (should pass)"
echo "========================================="

# Find a post with good humanization score
GOOD_POST=$(ls src/posts/*.md | head -1)
if [ -f "$GOOD_POST" ]; then
    echo "Testing with: $GOOD_POST"

    # Check its current score
    SCORE=$(python scripts/blog-content/humanization-validator.py --post "$GOOD_POST" --output json 2>/dev/null | jq -r '.score // 0')
    echo "Current score: $SCORE"

    if (( $(echo "$SCORE >= 75" | bc -l) )); then
        # Create a test commit
        echo "# Test comment" >> "$GOOD_POST"
        git add "$GOOD_POST"

        run_test "High-scoring post commit" ".git/hooks/pre-commit" 0

        # Cleanup
        git reset HEAD "$GOOD_POST" --quiet
        git checkout -- "$GOOD_POST" --quiet
    else
        echo -e "${YELLOW}⚠️  Skipping test - post score too low ($SCORE)${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No posts found to test${NC}"
fi

# Test 3: Create a low-scoring post (should fail)
echo ""
echo "========================================="
echo "Test 3: Low-scoring post (should fail)"
echo "========================================="

# Create a temporary low-scoring post
LOW_SCORE_POST="src/posts/2025-10-28-test-low-score.md"
cat > "$LOW_SCORE_POST" << 'EOF'
---
title: "Test Low Score Post"
date: 2025-10-28
description: "This is a test post designed to score low on humanization"
tags: [test]
---

# Test Post

This post leverages cutting-edge solutions to revolutionize the paradigm.
We are pleased to announce that our innovative approach delivers unprecedented results.
The solution is robust, scalable, and enterprise-ready.
EOF

git add "$LOW_SCORE_POST"

# This should fail because the post scores low
run_test "Low-scoring post commit (should block)" ".git/hooks/pre-commit" 1

# Cleanup
rm -f "$LOW_SCORE_POST"
git reset HEAD "$LOW_SCORE_POST" --quiet 2>/dev/null || true

# Test 4: Modify welcome.md (should skip validation)
echo ""
echo "========================================="
echo "Test 4: Welcome.md modification (should skip)"
echo "========================================="

if [ -f "src/posts/welcome.md" ]; then
    echo "# Test comment" >> "src/posts/welcome.md"
    git add "src/posts/welcome.md"

    run_test "Welcome.md modification" ".git/hooks/pre-commit" 0

    # Cleanup
    git reset HEAD "src/posts/welcome.md" --quiet
    git checkout -- "src/posts/welcome.md" --quiet
else
    echo -e "${YELLOW}⚠️  welcome.md not found${NC}"
fi

# Test 5: Direct validator test with JSON output
echo ""
echo "========================================="
echo "Test 5: Direct validator JSON output"
echo "========================================="

TEST_POST=$(ls src/posts/*.md | grep -v welcome | head -1)
if [ -f "$TEST_POST" ]; then
    echo "Testing validator output for: $TEST_POST"
    OUTPUT=$(python scripts/blog-content/humanization-validator.py --post "$TEST_POST" --output json 2>/dev/null)

    if echo "$OUTPUT" | jq -e '.score' > /dev/null 2>&1; then
        SCORE=$(echo "$OUTPUT" | jq -r '.score')
        echo -e "${GREEN}✅ JSON output valid${NC}"
        echo "Score: $SCORE"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ Invalid JSON output${NC}"
        echo "$OUTPUT"
        ((TESTS_FAILED++))
    fi
else
    echo -e "${YELLOW}⚠️  No posts found for testing${NC}"
fi

# Test 6: Multiple posts at once
echo ""
echo "========================================="
echo "Test 6: Multiple posts (mixed scores)"
echo "========================================="

# Create two test posts - one good, one bad
GOOD_TEST_POST="src/posts/2025-10-28-test-good.md"
BAD_TEST_POST="src/posts/2025-10-28-test-bad.md"

# Good post with personal voice
cat > "$GOOD_TEST_POST" << 'EOF'
---
title: "My Journey with Proxmox"
date: 2025-10-28
description: "Personal experiences setting up my homelab"
tags: [homelab, proxmox]
---

# My Proxmox Journey

I spent way too long figuring this out. Like, embarrassingly long.

When I first installed Proxmox on my old Dell R940, I thought it'd be straightforward. I was wrong. The networking alone took me three tries to get right, and I'm still not convinced I fully understand what I did.

But here's what I learned: sometimes the documentation isn't enough. You need to actually break things and fix them. I've broken this setup at least five times now, and each time I learn something new about VLANs, bridges, or firewall rules.

The key? Taking notes. Lots of notes. Because in six months, you'll forget everything.
EOF

# Bad post with AI tells
cat > "$BAD_TEST_POST" << 'EOF'
---
title: "Revolutionary Cloud Solutions"
date: 2025-10-28
description: "Enterprise-grade cloud deployment"
tags: [cloud]
---

# Cloud Solutions

Leveraging cutting-edge cloud technologies revolutionizes enterprise deployments; moreover, scalable architectures deliver unprecedented performance.

The robust solution seamlessly integrates with existing infrastructure—providing enterprise-grade reliability.

Key benefits include:
- Innovative approach
- Paradigm-shifting methodology
- Best-in-class performance
EOF

git add "$GOOD_TEST_POST" "$BAD_TEST_POST"

# Should fail because one post is bad
run_test "Mixed scores commit (should block)" ".git/hooks/pre-commit" 1

# Cleanup
rm -f "$GOOD_TEST_POST" "$BAD_TEST_POST"
git reset HEAD "$GOOD_TEST_POST" "$BAD_TEST_POST" --quiet 2>/dev/null || true

# Final summary
echo ""
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    exit 1
fi
