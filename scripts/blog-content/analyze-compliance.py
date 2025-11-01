#!/usr/bin/env -S uv run python3
"""
Analyze blog posts for CLAUDE.md compliance.

Evaluates:
- Smart Brevity violations (weak language, verbosity)
- AI skepticism presence
- BLUF structure
- Paragraph length
- Bullet usage
"""

import re
import json
import logging
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

# Weak language patterns (Polite Linus violations)
WEAK_PATTERNS = {
    'hedging': r'\b(should|could|might|perhaps|maybe|possibly|essentially|basically|actually|generally|typically)\b',
    'throat_clearing': r'\b(In this (post|article|section),|It is important to note|As (we|I) (mentioned|discussed)|Let me|Let\'s)\b',
    'filler': r'\b(very|really|quite|rather|somewhat|fairly|pretty)\b',
}

# AI hype patterns (needs skepticism)
AI_HYPE = {
    'anthropomorphism': r'\b(AI (thinks|believes|understands|knows|learns|decides|wants|feels)|the (model|algorithm) (thinks|believes))\b',
    'uncritical_benchmarks': r'\b(\d+%|\d+x) (improvement|better|faster|accuracy)\b(?! .*limitation)',
    'magic_words': r'\b(revolutionary|transformative|breakthrough|game-changing|paradigm shift)\b',
}

def count_words(text: str) -> int:
    """Count words in text."""
    return len(re.findall(r'\b\w+\b', text))

def analyze_paragraphs(text: str) -> Dict:
    """Analyze paragraph structure."""
    # Split into paragraphs (2+ newlines or heading)
    paras = re.split(r'\n\n+|^#+\s', text, flags=re.MULTILINE)
    paras = [p.strip() for p in paras if p.strip() and not p.startswith('```')]

    sentence_counts = []
    for para in paras:
        # Count sentences (rough estimate)
        sentences = len(re.findall(r'[.!?]+\s+[A-Z]|[.!?]+$', para)) + 1
        sentence_counts.append(sentences)

    return {
        'total_paragraphs': len(paras),
        'avg_sentences': sum(sentence_counts) / len(sentence_counts) if sentence_counts else 0,
        'long_paragraphs': sum(1 for s in sentence_counts if s > 5),
        'paragraph_lengths': sentence_counts,
    }

def count_bullets(text: str) -> int:
    """Count bullet points."""
    return len(re.findall(r'^\s*[-•*]\s', text, flags=re.MULTILINE))

def has_bluf(text: str) -> bool:
    """Check if post starts with BLUF (first 3 sentences after frontmatter)."""
    # Find first paragraph after frontmatter
    match = re.search(r'^---\n.*?^---\n\s*(.+?)\n\n', text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return False

    first_para = match.group(1)
    # BLUF should be 2-4 sentences max
    sentence_count = len(re.findall(r'[.!?]+', first_para))
    return 2 <= sentence_count <= 4 and count_words(first_para) <= 100

def detect_weak_language(text: str) -> Dict[str, List[str]]:
    """Detect weak language patterns."""
    violations = defaultdict(list)

    for category, pattern in WEAK_PATTERNS.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            violations[category] = matches

    return dict(violations)

def detect_ai_hype(text: str) -> Dict[str, List[str]]:
    """Detect AI hype without skepticism."""
    violations = defaultdict(list)

    for category, pattern in AI_HYPE.items():
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        if matches:
            violations[category] = matches

    return dict(violations)

def has_ai_skepticism(text: str) -> bool:
    """Check for AI skepticism/reality check sections."""
    skepticism_markers = [
        r'limitation',
        r'reality check',
        r'doesn\'t work',
        r'failure',
        r'caveat',
        r'however,',
        r'trade-?off',
        r'reproducib',
    ]

    matches = sum(1 for marker in skepticism_markers
                  if re.search(marker, text, flags=re.IGNORECASE))

    return matches >= 3

def calculate_compliance_score(analysis: Dict) -> Tuple[int, List[str]]:
    """
    Calculate compliance score (0-100) and list violations.

    Scoring:
    - BLUF present: +20
    - Weak language <5: +20
    - Paragraphs avg <=5 sentences: +20
    - Bullets >= 10: +20
    - AI skepticism (for AI posts): +20
    """
    score = 0
    violations = []

    # BLUF check
    if analysis['bluf_present']:
        score += 20
    else:
        violations.append("Missing BLUF (first para not concise)")

    # Weak language
    weak_count = sum(len(v) for v in analysis['weak_language'].values())
    if weak_count < 5:
        score += 20
    else:
        violations.append(f"Excessive weak language ({weak_count} instances)")

    # Paragraph length
    avg_sentences = analysis['paragraphs']['avg_sentences']
    if avg_sentences <= 5:
        score += 20
    else:
        violations.append(f"Paragraphs too long (avg {avg_sentences:.1f} sentences)")

    # Bullet usage
    if analysis['bullet_count'] >= 10:
        score += 20
    else:
        violations.append(f"Insufficient bullets ({analysis['bullet_count']} < 10)")

    # AI skepticism (for AI-tagged posts)
    is_ai_post = 'ai' in analysis.get('tags', []) or 'llm' in analysis.get('tags', [])
    if is_ai_post:
        if analysis['ai_skepticism_present']:
            score += 20
        else:
            violations.append("AI post missing skepticism/limitations")
    else:
        score += 20  # N/A for non-AI posts

    return score, violations

def analyze_post(filepath: Path) -> Dict:
    """Analyze a single blog post."""
    content = filepath.read_text()

    # Extract frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, flags=re.DOTALL)
    if not frontmatter_match:
        return {'error': 'Invalid frontmatter'}

    frontmatter, body = frontmatter_match.groups()

    # Extract tags from frontmatter
    tags_match = re.search(r'tags:\s*\n((?:\s*-\s*.+\n)+)', frontmatter)
    tags = []
    if tags_match:
        tags = [t.strip('- \n') for t in tags_match.group(1).split('\n') if t.strip()]

    # Basic metrics
    word_count = count_words(body)
    bullet_count = count_bullets(body)
    paragraphs = analyze_paragraphs(body)

    # Compliance checks
    bluf = has_bluf(content)
    weak_lang = detect_weak_language(body)
    ai_hype = detect_ai_hype(body)
    ai_skepticism = has_ai_skepticism(body)

    # Calculate score
    analysis = {
        'filepath': str(filepath),
        'filename': filepath.name,
        'word_count': word_count,
        'bullet_count': bullet_count,
        'paragraphs': paragraphs,
        'bluf_present': bluf,
        'weak_language': weak_lang,
        'ai_hype': ai_hype,
        'ai_skepticism_present': ai_skepticism,
        'tags': tags,
    }

    score, violations = calculate_compliance_score(analysis)
    analysis['compliance_score'] = score
    analysis['violations'] = violations

    # Effort estimate
    if score >= 80:
        effort = 'low'
        tier = 3
    elif score >= 60:
        effort = 'medium'
        tier = 2
    else:
        effort = 'high'
        tier = 1

    analysis['estimated_effort'] = effort
    analysis['priority_tier'] = tier

    return analysis

def main():
    """Analyze all blog posts."""
    parser = argparse.ArgumentParser(description='Analyze blog posts for CLAUDE.md compliance')
    parser.add_argument('--posts-dir', type=Path, help='Directory containing blog posts')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')
    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    posts_dir = args.posts_dir or (Path(__file__).parent.parent.parent / 'src' / 'posts')
    posts = sorted(posts_dir.glob('*.md'))

    results = []
    for post in posts:
        if post.name == 'welcome.md':
            continue  # Skip welcome post

        logger.info(f"Analyzing {post.name}")
        analysis = analyze_post(post)
        results.append(analysis)

    # Sort by priority (tier 1 first, then by word count descending)
    results.sort(key=lambda x: (x.get('priority_tier', 3), -x.get('word_count', 0)))

    # Generate report
    report = {
        'total_posts': len(results),
        'tier_1_count': sum(1 for r in results if r.get('priority_tier') == 1),
        'tier_2_count': sum(1 for r in results if r.get('priority_tier') == 2),
        'tier_3_count': sum(1 for r in results if r.get('priority_tier') == 3),
        'avg_compliance_score': sum(r.get('compliance_score', 0) for r in results) / len(results),
        'posts': results,
    }

    # Save to JSON
    output_path = Path(__file__).parent.parent.parent / 'docs' / 'compliance-report.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))

    logger.info("="*80)
    logger.info("COMPLIANCE ANALYSIS COMPLETE")
    logger.info("="*80)
    logger.info(f"Total posts: {report['total_posts']}")
    logger.info(f"Tier 1 (high priority): {report['tier_1_count']}")
    logger.info(f"Tier 2 (medium priority): {report['tier_2_count']}")
    logger.info(f"Tier 3 (low priority): {report['tier_3_count']}")
    logger.info(f"Average compliance score: {report['avg_compliance_score']:.1f}/100")
    logger.info(f"Report saved to: {output_path}")

    # Print top 10 worst offenders
    logger.info("="*80)
    logger.info("TOP 10 POSTS NEEDING REFACTORING (Tier 1)")
    logger.info("="*80)
    for i, post in enumerate(results[:10], 1):
        logger.info(f"{i}. {post['filename']}")
        logger.info(f"   Score: {post['compliance_score']}/100 | Words: {post['word_count']} | Tier: {post['priority_tier']}")
        logger.info(f"   Violations: {', '.join(post['violations'][:3])}")

if __name__ == '__main__':
    main()
