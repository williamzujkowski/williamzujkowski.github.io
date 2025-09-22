#!/bin/bash

echo "Smart Memory Population with File References"
echo "==========================================="

# Create a review context file
cat << 'EOF' > review-context.txt
REVIEW CONTEXT AND INSTRUCTIONS

FILES TO REVIEW:
- All posts in src/posts/
- All pages in src/pages/
- Verify against src/pages/uses.md

SECURITY BOUNDARIES:
- NO current/recent work incidents
- Only "years ago" (2-3+ years minimum)
- Personal projects/homelab OK
- Generic examples only

VOICE REQUIREMENTS:
- Conversational and genuine
- Personal but professional
- Helpful but humble
- Learning-focused

CHECK FOR:
1. Boundary violations
2. Tone consistency
3. Citation quality
4. Technical accuracy
EOF

# Store the review context
npx claude-flow@alpha memory store "review-context" "$(cat review-context.txt)" --namespace review

# Create a simple checklist
cat << 'EOF' > review-checklist.txt
[ ] No current work mentions
[ ] All incidents 2+ years old
[ ] Hardware matches uses.md
[ ] Conversational tone
[ ] Proper citations
[ ] Value to readers
EOF

npx claude-flow@alpha memory store "checklist" "$(cat review-checklist.txt)" --namespace review

echo "Memory populated with review context!"