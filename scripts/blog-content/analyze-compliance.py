#!/usr/bin/env -S uv run python3
"""
Analyze blog posts for CLAUDE.md compliance.

Version: 2.0.0

Evaluates:
- Smart Brevity violations (weak language, verbosity)
- AI skepticism presence
- BLUF structure
- Paragraph structure (3-4 sentence standard for mobile readability)
- Bullet usage

New in v2.0.0:
- Enhanced sentence counting (handles abbreviations, code blocks)
- Detailed paragraph structure analysis with compliance rates
- CSV export for batch analysis
- Actionable refactoring recommendations
"""

import re
import json
import logging
import sys
import argparse
import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Add parent directory to path for lib imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from lib.logging_config import setup_logger

VERSION = "2.0.0"

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

def count_sentences_in_paragraph(paragraph_text: str) -> int:
    """
    Count sentences in a paragraph with proper handling of edge cases.

    Handles:
    - Common abbreviations (Dr., Mr., Mrs., Ph.D., etc.)
    - Decimal numbers (3.14, 10.5)
    - Code snippets (inline code with backticks)
    - URLs and file paths

    Args:
        paragraph_text: Raw paragraph text

    Returns:
        Number of sentences in paragraph
    """
    text = paragraph_text

    # Common abbreviations that shouldn't trigger sentence breaks
    # Strategy: Only replace abbreviations NOT followed by uppercase (not sentence boundaries)
    abbreviations = [
        r'Dr\.', r'Mr\.', r'Mrs\.', r'Ms\.', r'Prof\.',
        r'Ph\.D\.', r'M\.D\.', r'B\.A\.', r'M\.A\.', r'B\.S\.', r'M\.S\.',
        r'i\.e\.', r'e\.g\.', r'etc\.', r'vs\.', r'Inc\.', r'Ltd\.', r'Co\.',
        r'Jan\.', r'Feb\.', r'Mar\.', r'Apr\.', r'Aug\.', r'Sept\.', r'Oct\.', r'Nov\.', r'Dec\.',
    ]

    # Replace period in abbreviations ONLY when NOT followed by uppercase letter (not sentence end)
    # Example: "Dr. Smith" → "Dr__ABBR__ Smith" (not sentence boundary)
    # Example: "Tech Inc. He" → keep "Inc." because followed by uppercase (IS sentence boundary)
    for abbr in abbreviations:
        # Replace abbrev period when followed by lowercase or non-letter
        text = re.sub(abbr + r'(?=\s+[a-z])', abbr[:-2] + '__ABBR__', text, flags=re.IGNORECASE)

    # Replace decimal numbers (3.14 -> 3__DOT__14)
    text = re.sub(r'(\d+)\.(\d+)', r'\1__DOT__\2', text)

    # Handle inline code blocks with special care
    # Replace code blocks entirely but mark if they end sentences
    code_blocks = re.findall(r'`[^`]+`', text)
    for cb in code_blocks:
        if cb.endswith('`.') or cb.endswith('`!') or cb.endswith('`?'):
            # Code block at sentence end - keep punctuation after removal
            text = text.replace(cb, ' __CODE__', 1)
        else:
            # Code block mid-sentence
            text = text.replace(cb, ' __CODE__ ', 1)

    # Remove URLs (prevent false breaks on domain extensions)
    text = re.sub(r'https?://[^\s]+', ' __URL__ ', text)

    # Count sentence-ending punctuation followed by:
    # - Space + any character (new sentence starts)
    # - End of string (last sentence)
    sentences = re.findall(r'[.!?](?:\s+\S|\s*$)', text)
    sentence_count = len(sentences)

    # Handle case where paragraph has no ending punctuation
    if sentence_count == 0 and text.strip():
        sentence_count = 1

    return sentence_count

def analyze_paragraphs(text: str) -> Dict:
    """
    Analyze paragraph structure for compliance with 3-4 sentence standard.

    Returns:
        dict with keys:
        - total_paragraphs: Total paragraph count
        - avg_sentences: Average sentences per paragraph
        - compliant_paragraphs: Count of paragraphs with 3-4 sentences
        - compliance_rate: Percentage of compliant paragraphs
        - violations: List of non-compliant paragraphs with recommendations
        - paragraph_details: List of (index, sentence_count) tuples
    """
    # Remove code blocks (```...```) before analysis
    text_no_code = re.sub(r'```[\s\S]*?```', '', text, flags=re.MULTILINE)

    # Split into paragraphs (2+ newlines or heading)
    # Filter out empty paragraphs and headings
    paras = re.split(r'\n\n+', text_no_code)
    paras = [p.strip() for p in paras if p.strip() and not re.match(r'^#+\s', p)]

    paragraph_details = []
    violations = []
    compliant_count = 0

    for i, para in enumerate(paras):
        # Skip bullet lists and numbered lists
        if re.match(r'^\s*[-•*\d]+[\.\)]\s', para, flags=re.MULTILINE):
            continue

        sentence_count = count_sentences_in_paragraph(para)
        paragraph_details.append((i + 1, sentence_count))

        # Check compliance (3-4 sentences)
        if 3 <= sentence_count <= 4:
            compliant_count += 1
        else:
            # Generate recommendation
            if sentence_count < 3:
                if sentence_count == 1:
                    recommendation = "Expand with supporting detail or combine with adjacent paragraph"
                else:
                    recommendation = "Add 1 supporting sentence or combine with adjacent paragraph"
            elif sentence_count == 5:
                recommendation = "Remove 1 sentence or split into 2 paragraphs"
            else:  # >5
                recommendation = f"Split into {(sentence_count + 2) // 3} paragraphs (target 3-4 sentences each)"

            violations.append({
                'paragraph_index': i + 1,
                'sentence_count': sentence_count,
                'recommendation': recommendation,
            })

    total_paragraphs = len(paragraph_details)
    avg_sentences = sum(s for _, s in paragraph_details) / total_paragraphs if total_paragraphs else 0
    compliance_rate = (compliant_count / total_paragraphs * 100) if total_paragraphs else 0

    return {
        'total_paragraphs': total_paragraphs,
        'avg_sentences': avg_sentences,
        'compliant_paragraphs': compliant_count,
        'compliance_rate': compliance_rate,
        'violations': violations,
        'paragraph_details': paragraph_details,
        'long_paragraphs': sum(1 for _, s in paragraph_details if s > 5),  # Legacy compatibility
        'paragraph_lengths': [s for _, s in paragraph_details],  # Legacy compatibility
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

def generate_csv_report(results: List[Dict], output_path: Path, logger):
    """Generate CSV report of paragraph structure analysis."""
    logger.info(f"Generating CSV report: {output_path}")

    with output_path.open('w', newline='') as csvfile:
        fieldnames = [
            'post_name',
            'total_paragraphs',
            'compliant_paragraphs',
            'compliance_rate',
            'avg_sentences',
            'violation_count',
            'word_count',
            'priority_tier',
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            paragraphs = result.get('paragraphs', {})
            writer.writerow({
                'post_name': result['filename'],
                'total_paragraphs': paragraphs.get('total_paragraphs', 0),
                'compliant_paragraphs': paragraphs.get('compliant_paragraphs', 0),
                'compliance_rate': f"{paragraphs.get('compliance_rate', 0):.1f}%",
                'avg_sentences': f"{paragraphs.get('avg_sentences', 0):.1f}",
                'violation_count': len(paragraphs.get('violations', [])),
                'word_count': result.get('word_count', 0),
                'priority_tier': result.get('priority_tier', 3),
            })

    logger.info(f"CSV report saved to: {output_path}")

def generate_refactoring_plan(results: List[Dict], logger):
    """Generate prioritized refactoring plan based on paragraph compliance."""
    logger.info("="*80)
    logger.info("PARAGRAPH STRUCTURE REFACTORING PLAN")
    logger.info("="*80)

    # Sort by compliance rate (lowest first)
    sorted_posts = sorted(
        results,
        key=lambda x: x.get('paragraphs', {}).get('compliance_rate', 100)
    )

    # Filter posts with <80% compliance (target from blog-patterns.md)
    needs_refactoring = [
        p for p in sorted_posts
        if p.get('paragraphs', {}).get('compliance_rate', 100) < 80
    ]

    if not needs_refactoring:
        logger.info("✓ All posts meet 80%+ paragraph structure compliance!")
        return

    logger.info(f"Found {len(needs_refactoring)} posts below 80% compliance\n")

    for i, post in enumerate(needs_refactoring[:15], 1):  # Top 15 worst
        paragraphs = post.get('paragraphs', {})
        compliance = paragraphs.get('compliance_rate', 0)
        violations = paragraphs.get('violations', [])

        logger.info(f"{i}. {post['filename']}")
        logger.info(f"   Compliance: {compliance:.1f}% ({paragraphs.get('compliant_paragraphs', 0)}/{paragraphs.get('total_paragraphs', 0)} paragraphs)")
        logger.info(f"   Violations: {len(violations)}")

        # Show top 3 violations
        for v in violations[:3]:
            logger.info(f"      ¶{v['paragraph_index']}: {v['sentence_count']} sentences → {v['recommendation']}")

        logger.info("")

def main():
    """Analyze all blog posts."""
    parser = argparse.ArgumentParser(
        description='Analyze blog posts for CLAUDE.md compliance (v2.0.0)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze all posts, generate full report
  %(prog)s

  # Analyze single post
  %(prog)s --post src/posts/2024-01-08-writing-secure-code.md

  # Batch analysis with CSV export
  %(prog)s --batch --csv docs/paragraph-analysis.csv

  # Focus on paragraph structure only
  %(prog)s --paragraph-focus
        """
    )
    parser.add_argument('--post', type=Path, help='Analyze single post')
    parser.add_argument('--batch', action='store_true', help='Batch analyze all posts')
    parser.add_argument('--csv', type=Path, help='Output CSV report path')
    parser.add_argument('--paragraph-focus', action='store_true', help='Focus report on paragraph structure')
    parser.add_argument('--posts-dir', type=Path, help='Directory containing blog posts')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable debug output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--log-file', type=Path, help='Write logs to file')
    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logger = setup_logger(__name__, level=level, log_file=args.log_file, quiet=args.quiet)

    logger.info(f"Paragraph Structure Analyzer v{VERSION}")

    posts_dir = args.posts_dir or (Path(__file__).parent.parent.parent / 'src' / 'posts')

    # Single post analysis
    if args.post:
        logger.info(f"Analyzing single post: {args.post.name}")
        analysis = analyze_post(args.post)

        # Print detailed paragraph analysis
        paragraphs = analysis.get('paragraphs', {})
        logger.info("="*80)
        logger.info("PARAGRAPH STRUCTURE ANALYSIS")
        logger.info("="*80)
        logger.info(f"Total paragraphs: {paragraphs.get('total_paragraphs', 0)}")
        logger.info(f"Compliant (3-4 sentences): {paragraphs.get('compliant_paragraphs', 0)}")
        logger.info(f"Compliance rate: {paragraphs.get('compliance_rate', 0):.1f}%")
        logger.info(f"Average sentences/paragraph: {paragraphs.get('avg_sentences', 0):.1f}")
        logger.info(f"\nViolations: {len(paragraphs.get('violations', []))}")

        for v in paragraphs.get('violations', []):
            logger.info(f"  ¶{v['paragraph_index']}: {v['sentence_count']} sentences")
            logger.info(f"     → {v['recommendation']}")

        return

    # Batch analysis
    posts = sorted(posts_dir.glob('*.md'))
    results = []

    for post in posts:
        if post.name == 'welcome.md':
            continue

        logger.info(f"Analyzing {post.name}")
        analysis = analyze_post(post)
        results.append(analysis)

    # Sort by priority (tier 1 first, then by word count descending)
    results.sort(key=lambda x: (x.get('priority_tier', 3), -x.get('word_count', 0)))

    # CSV export if requested
    if args.csv:
        generate_csv_report(results, args.csv, logger)

    # Calculate paragraph compliance statistics
    total_posts = len(results)
    avg_para_compliance = sum(
        r.get('paragraphs', {}).get('compliance_rate', 0) for r in results
    ) / total_posts if total_posts else 0

    posts_meeting_target = sum(
        1 for r in results
        if r.get('paragraphs', {}).get('compliance_rate', 0) >= 80
    )

    # Generate full report
    report = {
        'version': VERSION,
        'total_posts': total_posts,
        'tier_1_count': sum(1 for r in results if r.get('priority_tier') == 1),
        'tier_2_count': sum(1 for r in results if r.get('priority_tier') == 2),
        'tier_3_count': sum(1 for r in results if r.get('priority_tier') == 3),
        'avg_compliance_score': sum(r.get('compliance_score', 0) for r in results) / total_posts,
        'avg_paragraph_compliance': avg_para_compliance,
        'posts_meeting_80_percent': posts_meeting_target,
        'posts': results,
    }

    # Save to JSON
    output_path = Path(__file__).parent.parent.parent / 'docs' / 'compliance-report.json'
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2))

    # Print summary
    logger.info("="*80)
    logger.info("COMPLIANCE ANALYSIS COMPLETE")
    logger.info("="*80)
    logger.info(f"Total posts: {report['total_posts']}")
    logger.info(f"Tier 1 (high priority): {report['tier_1_count']}")
    logger.info(f"Tier 2 (medium priority): {report['tier_2_count']}")
    logger.info(f"Tier 3 (low priority): {report['tier_3_count']}")
    logger.info(f"Average compliance score: {report['avg_compliance_score']:.1f}/100")
    logger.info("")
    logger.info("PARAGRAPH STRUCTURE COMPLIANCE")
    logger.info(f"Average paragraph compliance: {avg_para_compliance:.1f}%")
    logger.info(f"Posts meeting 80%+ target: {posts_meeting_target}/{total_posts} ({posts_meeting_target/total_posts*100:.1f}%)")
    logger.info(f"Report saved to: {output_path}")

    # Paragraph-focused output
    if args.paragraph_focus:
        generate_refactoring_plan(results, logger)
    else:
        # Standard top 10 worst offenders
        logger.info("="*80)
        logger.info("TOP 10 POSTS NEEDING REFACTORING")
        logger.info("="*80)
        for i, post in enumerate(results[:10], 1):
            para_compliance = post.get('paragraphs', {}).get('compliance_rate', 0)
            logger.info(f"{i}. {post['filename']}")
            logger.info(f"   Score: {post['compliance_score']}/100 | Para compliance: {para_compliance:.1f}%")
            logger.info(f"   Violations: {', '.join(post['violations'][:3])}")

if __name__ == '__main__':
    main()
