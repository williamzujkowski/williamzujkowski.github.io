#!/usr/bin/env -S uv run python3
"""
Quick post analyzer - counts citations, weak language, and bullets
Usage: python analyze-post.py <markdown-file>
"""

import re
import sys
from pathlib import Path

WEAK_WORDS = [
    'really', 'very', 'quite', 'just', 'actually', 'basically',
    'simply', 'extremely', 'incredibly', 'totally', 'literally',
    'obviously', 'clearly', 'essentially'
]

def analyze_post(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter
    content_no_front = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)

    # Remove code blocks
    content_no_code = re.sub(r'```.*?```', '', content_no_front, flags=re.DOTALL)

    # Count citations
    citations = re.findall(r'\[.*?\]\((https?://[^\)]+)\)', content)
    arxiv = len([c for c in citations if 'arxiv.org' in c])
    doi = len([c for c in citations if 'doi.org' in c])
    github = len([c for c in citations if 'github.com' in c])

    # Count weak language (word boundaries)
    weak_count = 0
    weak_instances = []
    for word in WEAK_WORDS:
        pattern = r'\b' + word + r'\b'
        matches = list(re.finditer(pattern, content_no_code, re.IGNORECASE))
        for match in matches:
            # Get line number
            line_num = content_no_code[:match.start()].count('\n') + 1
            weak_instances.append(f"Line {line_num}: {word}")
        weak_count += len(matches)

    # Count bullets
    bullets = len(re.findall(r'^[\s]*[-*+]\s', content_no_front, re.MULTILINE))
    bullets += len(re.findall(r'^[\s]*\d+\.\s', content_no_front, re.MULTILINE))

    # Print results
    print(f"\n{'='*50}")
    print(f"Analysis: {Path(filepath).name}")
    print(f"{'='*50}\n")

    print(f"📚 Citations: {len(citations)}")
    print(f"   arXiv: {arxiv}")
    print(f"   DOI: {doi}")
    print(f"   GitHub: {github}")
    print(f"   Other: {len(citations) - arxiv - doi - github}")

    print(f"\n💬 Weak Language: {weak_count} instances")
    if weak_count > 0:
        print("   ⚠️  Found:")
        for instance in weak_instances[:10]:  # Show first 10
            print(f"      {instance}")
        if len(weak_instances) > 10:
            print(f"      ... and {len(weak_instances) - 10} more")
    else:
        print("   ✅ Clean!")

    print(f"\n📝 Bullet Points: {bullets}")
    if bullets >= 60:
        print("   ✅ Excellent scannability (≥60)")
    elif bullets >= 20:
        print("   ⚠️  Good but could improve (target: 60+)")
    else:
        print("   ❌ Low scannability (<20)")

    print(f"\n{'='*50}\n")

    return {
        'citations': len(citations),
        'weak_language': weak_count,
        'bullets': bullets
    }

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python analyze-post.py <markdown-file>")
        sys.exit(1)

    filepath = sys.argv[1]
    if not Path(filepath).exists():
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    analyze_post(filepath)
