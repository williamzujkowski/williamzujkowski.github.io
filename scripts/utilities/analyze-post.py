#!/usr/bin/env -S uv run python3
"""
SCRIPT: analyze-post.py
PURPOSE: Quick post analyzer - counts citations, weak language, and bullets
CATEGORY: utilities
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Quick post analyzer - counts citations, weak language, and bullets
"""

import re
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)

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

    # Log results
    logger.info(f"\n{'='*50}")
    logger.info(f"Analysis: {Path(filepath).name}")
    logger.info(f"{'='*50}\n")

    logger.info(f"📚 Citations: {len(citations)}")
    logger.info(f"   arXiv: {arxiv}")
    logger.info(f"   DOI: {doi}")
    logger.info(f"   GitHub: {github}")
    logger.info(f"   Other: {len(citations) - arxiv - doi - github}")

    logger.info(f"\n💬 Weak Language: {weak_count} instances")
    if weak_count > 0:
        logger.info("   ⚠️  Found:")
        for instance in weak_instances[:10]:  # Show first 10
            logger.info(f"      {instance}")
        if len(weak_instances) > 10:
            logger.info(f"      ... and {len(weak_instances) - 10} more")
    else:
        logger.info("   ✅ Clean!")

    logger.info(f"\n📝 Bullet Points: {bullets}")
    if bullets >= 60:
        logger.info("   ✅ Excellent scannability (≥60)")
    elif bullets >= 20:
        logger.info("   ⚠️  Good but could improve (target: 60+)")
    else:
        logger.info("   ❌ Low scannability (<20)")

    logger.info(f"\n{'='*50}\n")

    return {
        'citations': len(citations),
        'weak_language': weak_count,
        'bullets': bullets
    }

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Quick post analyzer - counts citations, weak language, and bullets',
        epilog='''
Examples:
  %(prog)s src/posts/my-post.md
  %(prog)s src/posts/my-post.md --quiet
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('filepath', type=str, help='Path to markdown file to analyze')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    try:
        if not Path(args.filepath).exists():
            logger.error(f"File not found: {args.filepath}")
            logger.error(f"Current directory: {Path.cwd()}")
            logger.error("Tip: Provide full path to markdown file")
            sys.exit(2)

        analyze_post(args.filepath)
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error: {e}")
        sys.exit(1)
