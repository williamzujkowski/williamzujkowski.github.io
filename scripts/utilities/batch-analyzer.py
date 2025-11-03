#!/usr/bin/env -S uv run python3
"""
Batch analyzer - Scans all posts and ranks them for refactoring priority
Usage: python batch-analyzer.py

Version: 2.0.0
Updated: 2025-11-03
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List

# Setup logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

WEAK_WORDS = [
    'really', 'very', 'quite', 'just', 'actually', 'basically',
    'simply', 'extremely', 'incredibly', 'totally', 'literally'
]

@dataclass
class PostAnalysis:
    filename: str
    word_count: int
    citations: int
    weak_language: int
    bullets: int
    priority_score: int

def analyze_post(filepath: Path) -> PostAnalysis:
    """Analyze a single post and return metrics"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove frontmatter
    content_no_front = re.sub(r'^---.*?---\n', '', content, flags=re.DOTALL)

    # Remove code blocks for weak language analysis
    content_no_code = re.sub(r'```.*?```', '', content_no_front, flags=re.DOTALL)

    # Count words (rough estimate)
    word_count = len(content_no_front.split())

    # Count citations
    citations = len(re.findall(r'\[.*?\]\((https?://[^\)]+)\)', content))

    # Count weak language
    weak_count = sum(
        len(re.findall(r'\b' + word + r'\b', content_no_code, re.IGNORECASE))
        for word in WEAK_WORDS
    )

    # Count bullets
    bullets = len(re.findall(r'^[\s]*[-*+]\s', content_no_front, re.MULTILINE))
    bullets += len(re.findall(r'^[\s]*\d+\.\s', content_no_front, re.MULTILINE))

    # Calculate priority score (higher = more needs refactoring)
    # Weak language is highest priority
    # Low bullets second priority
    # Low citations third priority
    priority = (weak_count * 10) + max(0, (60 - bullets)) + max(0, (10 - citations))

    return PostAnalysis(
        filename=filepath.name,
        word_count=word_count,
        citations=citations,
        weak_language=weak_count,
        bullets=bullets,
        priority_score=priority
    )

def main():
    parser = argparse.ArgumentParser(
        description='Scan blog posts and rank them for refactoring priority',
        epilog='''
Examples:
  %(prog)s
  %(prog)s --posts-dir src/posts
  %(prog)s --top 10 --quiet
  %(prog)s --version
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                       help='Directory containing blog posts')
    parser.add_argument('--top', type=int, default=20,
                       help='Number of top candidates to show')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    posts_dir = args.posts_dir

    if not posts_dir.exists():
        logger.error(f"Error: Directory not found: {posts_dir}")
        logger.error(f"Expected: {posts_dir.absolute()}")
        logger.error(f"Tip: Run from repository root or provide absolute path")
        sys.exit(2)

    # Skip Batch 1 completed posts
    batch1_posts = [
        '2025-10-17-progressive-context-loading-llm-workflows.md',
        '2025-08-09-ai-cognitive-infrastructure.md',
        '2025-10-13-embodied-ai-robots-physical-world.md'
    ]

    analyses: List[PostAnalysis] = []

    if not args.quiet:
        logger.info("Scanning all blog posts...")
        logger.info("="*80)

    for post_file in sorted(posts_dir.glob('*.md')):
        if post_file.name in batch1_posts:
            continue

        analysis = analyze_post(post_file)
        analyses.append(analysis)

    # Sort by priority score (descending)
    analyses.sort(key=lambda x: x.priority_score, reverse=True)

    # Print top candidates
    if not args.quiet:
        logger.info(f"\n{'Rank':<6} {'Filename':<50} {'Weak':<6} {'Bullets':<8} {'Cites':<7} {'Score':<6}")
        logger.info("="*80)

        for i, analysis in enumerate(analyses[:args.top], 1):
            logger.info(f"{i:<6} {analysis.filename:<50} {analysis.weak_language:<6} {analysis.bullets:<8} {analysis.citations:<7} {analysis.priority_score:<6}")

        logger.info("\n" + "="*80)
        logger.info(f"\nTop 8 candidates for Batch 2:")
        logger.info("-"*80)

    batch2_candidates = []
    for i, analysis in enumerate(analyses[:8], 1):
        status = "🔴" if analysis.weak_language > 15 else "🟡" if analysis.weak_language > 5 else "🟢"
        if not args.quiet:
            logger.info(f"{i}. {status} {analysis.filename}")
            logger.info(f"   Weak: {analysis.weak_language}, Bullets: {analysis.bullets}, Citations: {analysis.citations}")
        batch2_candidates.append(analysis.filename)

    # Save batch2 selection
    output_dir = Path('docs/batch-2')
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_dir / 'batch-2-selection.txt', 'w') as f:
        f.write("# Batch 2 Selected Posts\n\n")
        for i, filename in enumerate(batch2_candidates, 1):
            f.write(f"{i}. {filename}\n")

    if not args.quiet:
        logger.info(f"\n✅ Batch 2 selection saved to docs/batch-2/batch-2-selection.txt")

    return 0

if __name__ == '__main__':
    sys.exit(main())
