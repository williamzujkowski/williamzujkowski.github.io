#!/bin/bash
# count-bullets.sh
# Counts bullet points and numbered lists in blog posts
# Usage: ./count-bullets.sh [file.md]

set -euo pipefail

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to count bullets in a file
count_bullets() {
    local file="$1"

    echo -e "${BLUE}=========================================${NC}"
    echo -e "${BLUE}  Bullet Point Analysis: $(basename "$file")${NC}"
    echo -e "${BLUE}=========================================${NC}"
    echo ""

    # Count unordered lists (-, *, +)
    # Exclude frontmatter (between first two ---) and code blocks (between ```)
    local unordered=$(awk '
        BEGIN { in_frontmatter=0; frontmatter_count=0; in_code=0 }
        /^---[[:space:]]*$/ {
            frontmatter_count++
            if (frontmatter_count <= 2) {
                in_frontmatter = (frontmatter_count == 1)
                next
            }
        }
        /^```/ { in_code = !in_code; next }
        !in_frontmatter && !in_code && /^[[:space:]]*[-*+][[:space:]]/ { count++ }
        END { print count+0 }
    ' "$file")

    # Count ordered lists (1., 2., etc.)
    local ordered=$(awk '
        BEGIN { in_frontmatter=0; frontmatter_count=0; in_code=0 }
        /^---[[:space:]]*$/ {
            frontmatter_count++
            if (frontmatter_count <= 2) {
                in_frontmatter = (frontmatter_count == 1)
                next
            }
        }
        /^```/ { in_code = !in_code; next }
        !in_frontmatter && !in_code && /^[[:space:]]*[0-9]+\.[[:space:]]/ { count++ }
        END { print count+0 }
    ' "$file")

    local total=$((unordered + ordered))

    # Display results
    echo -e "${GREEN}Total Bullet Points: $total${NC}"
    echo ""
    echo "Breakdown:"
    echo -e "  Unordered lists (-, *, +): ${CYAN}$unordered${NC}"
    echo -e "  Ordered lists (1., 2., ...): ${CYAN}$ordered${NC}"
    echo ""

    # Assessment
    if [ $total -ge 60 ]; then
        echo -e "${GREEN}✓ Excellent scannability (≥60 bullets)${NC}"
    elif [ $total -ge 20 ]; then
        echo -e "${YELLOW}⚠ Good but could improve (target: 60+ bullets)${NC}"
        echo -e "${YELLOW}  Consider converting more paragraphs to bullet points${NC}"
    else
        echo -e "${RED}✗ Low scannability (<20 bullets)${NC}"
        echo -e "${RED}  Significant bulletization needed${NC}"
    fi
    echo ""

    # Count total paragraphs for context
    local paragraphs=$(awk '
        BEGIN { in_frontmatter=0; frontmatter_count=0; in_code=0; count=0 }
        /^---[[:space:]]*$/ {
            frontmatter_count++
            if (frontmatter_count <= 2) {
                in_frontmatter = (frontmatter_count == 1)
                next
            }
        }
        /^```/ { in_code = !in_code; next }
        !in_frontmatter && !in_code && /^[[:space:]]*$/ { next }
        !in_frontmatter && !in_code && /^#/ { next }
        !in_frontmatter && !in_code && NF > 0 { count++ }
        END { print count }
    ' "$file")

    echo -e "Context:"
    echo -e "  Estimated content lines: ${CYAN}$paragraphs${NC}"
    if [ $paragraphs -gt 0 ]; then
        local bullet_pct=$((total * 100 / paragraphs))
        echo -e "  Bullet density: ${CYAN}$bullet_pct%${NC} (bullets/content lines)"
    fi
    echo ""

    return $total
}

# Main logic
main() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 <markdown-file>"
        echo ""
        echo "Examples:"
        echo "  $0 src/posts/2025-10-17-progressive-context-loading.md"
        echo "  $0 src/posts/*.md  # Batch count (summary only)"
        exit 1
    fi

    if [ $# -eq 1 ]; then
        # Single file - detailed analysis
        count_bullets "$1"
    else
        # Multiple files - summary only
        echo "=========================================="
        echo "  Batch Bullet Point Count"
        echo "=========================================="
        echo ""

        local total_bullets=0
        local total_files=0
        local excellent=0
        local good=0
        local needs_work=0

        for file in "$@"; do
            if [ -f "$file" ]; then
                local count=$(awk '
                    BEGIN { in_frontmatter=0; frontmatter_count=0; in_code=0; unordered=0; ordered=0 }
                    /^---[[:space:]]*$/ {
                        frontmatter_count++
                        if (frontmatter_count <= 2) {
                            in_frontmatter = (frontmatter_count == 1)
                            next
                        }
                    }
                    /^```/ { in_code = !in_code; next }
                    !in_frontmatter && !in_code && /^[[:space:]]*[-*+][[:space:]]/ { unordered++ }
                    !in_frontmatter && !in_code && /^[[:space:]]*[0-9]+\.[[:space:]]/ { ordered++ }
                    END { print unordered + ordered }
                ' "$file")

                total_bullets=$((total_bullets + count))
                ((total_files++))

                # Categorize
                if [ $count -ge 60 ]; then
                    ((excellent++))
                    status="${GREEN}✓${NC}"
                elif [ $count -ge 20 ]; then
                    ((good++))
                    status="${YELLOW}⚠${NC}"
                else
                    ((needs_work++))
                    status="${RED}✗${NC}"
                fi

                echo -e "$status $(basename "$file"): $count bullets"
            fi
        done

        echo ""
        echo "=========================================="
        echo "Summary:"
        echo "  Total bullets: $total_bullets across $total_files files"
        echo "  Average: $((total_bullets / total_files)) bullets per post"
        echo ""
        echo "Quality distribution:"
        echo -e "  ${GREEN}Excellent (≥60):${NC} $excellent files"
        echo -e "  ${YELLOW}Good (20-59):${NC} $good files"
        echo -e "  ${RED}Needs work (<20):${NC} $needs_work files"
        echo "=========================================="
    fi
}

main "$@"
