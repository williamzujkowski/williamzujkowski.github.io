#!/usr/bin/env -S uv run python3
"""
SCRIPT: optimize-seo-descriptions.py
PURPOSE: SEO Meta Description Optimizer with Keyword Analysis
CATEGORY: blog_content
LLM_READY: True
VERSION: 3.0.0
UPDATED: 2025-11-10

DESCRIPTION:
    Automatically analyzes and optimizes blog post meta descriptions for SEO:
    - Validates length (130-155 chars optimal for CTR)
    - Extracts and validates primary keywords
    - Checks uniqueness across all posts
    - Generates quality scores (0-100)
    - Provides actionable recommendations

    Based on research: 130-155 char descriptions with keywords improve CTR by 40%

LLM_USAGE:
    python scripts/blog-content/optimize-seo-descriptions.py [options]

ARGUMENTS:
    --post PATH: Analyze single post
    --batch: Analyze all posts in src/posts/
    --csv PATH: Output CSV report
    --generate: Generate optimized recommendations
    --debug: Enable debug logging
    --verbose, -v: Enable verbose output

EXAMPLES:
    # Analyze single post
    python scripts/blog-content/optimize-seo-descriptions.py --post src/posts/welcome.md

    # Batch analysis with CSV report
    python scripts/blog-content/optimize-seo-descriptions.py --batch --csv reports/seo-analysis.csv

    # Generate recommendations for all posts
    python scripts/blog-content/optimize-seo-descriptions.py --batch --generate

OUTPUT:
    - Quality scores for each description (0-100)
    - Keyword analysis and validation
    - Uniqueness check across all posts
    - Optimized description recommendations
    - CSV report with detailed metrics

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for frontmatter parsing
    - scripts/lib/logging_config.py for centralized logging

RELATED_SCRIPTS:
    - scripts/blog-content/analyze-blog-content.py: Content analysis
    - scripts/blog-content/metadata-validator.py: Metadata validation

MANIFEST_REGISTRY: scripts/blog-content/optimize-seo-descriptions.py
"""

import os
import re
import csv
import json
import yaml
import sys
import logging
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Set
from collections import Counter
from difflib import SequenceMatcher

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Configuration
POSTS_DIR = Path("src/posts")
REPORT_DIR = Path("docs/reports")
MIN_CHARS = 120
OPTIMAL_MIN = 130
OPTIMAL_MAX = 155
MAX_CHARS = 160

# Action verbs for compelling descriptions
ACTION_VERBS = [
    "Implement", "Build", "Secure", "Deploy", "Explore", "Master",
    "Learn", "Discover", "Create", "Optimize", "Configure", "Analyze",
    "Protect", "Enhance", "Automate", "Monitor", "Test", "Debug"
]

# Stop words to ignore in keyword extraction
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "should", "could", "may", "might", "must", "can", "this",
    "that", "these", "those", "i", "you", "he", "she", "it", "we", "they",
    "my", "your", "his", "her", "its", "our", "their"
}


class DescriptionOptimizer:
    """Optimizes blog post meta descriptions for SEO with keyword analysis."""

    def __init__(self, logger=None):
        self.posts_dir = POSTS_DIR
        self.report_dir = REPORT_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
        self.all_descriptions = {}  # Cache for uniqueness checking
        self.logger = logger or logging.getLogger(__name__)

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, str]:
        """Extract YAML frontmatter from markdown content."""
        pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)$'
        match = re.match(pattern, content, re.DOTALL)

        if not match:
            return None, "", content

        frontmatter_text = match.group(1)
        body = match.group(2)

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            if frontmatter is None:
                frontmatter = {}
        except yaml.YAMLError as e:
            self.logger.warning(f"YAML parse error: {e}")
            return None, frontmatter_text, body

        return frontmatter, frontmatter_text, body

    def extract_primary_keyword(self, post_content: str, post_title: str, post_tags: List[str]) -> str:
        """
        Extract 1-2 primary keywords from content/title.

        Strategy:
        - Use first technical term from title (2+ words)
        - Count word frequency in H2 headings
        - Prefer multi-word technical terms
        - Fall back to most frequent tag

        Returns: str (primary keyword)
        """
        # Try title first (often contains primary topic)
        title_words = [w.lower() for w in post_title.split() if w.lower() not in STOP_WORDS]
        if len(title_words) >= 2:
            # Multi-word title is likely the primary keyword
            candidate = " ".join(title_words[:2])
            if len(candidate) > 3:  # Avoid short words
                return candidate

        # Extract H2 headings
        h2_pattern = r'^##\s+(.+)$'
        h2_headings = re.findall(h2_pattern, post_content, re.MULTILINE)

        # Count word frequency in headings
        word_freq = Counter()
        for heading in h2_headings:
            words = [w.lower() for w in heading.split()
                    if w.lower() not in STOP_WORDS and len(w) > 3]
            word_freq.update(words)

        # Get most common technical term
        if word_freq:
            primary_word = word_freq.most_common(1)[0][0]
            return primary_word

        # Fall back to first tag
        if post_tags:
            return post_tags[0].replace("-", " ")

        return title_words[0] if title_words else "guide"

    def check_uniqueness(self, description: str, current_post: str) -> Tuple[bool, Optional[str]]:
        """
        Check if description is unique across all posts.

        Returns: (is_unique: bool, duplicate_post: Optional[str])
        """
        for post_name, other_desc in self.all_descriptions.items():
            if post_name == current_post:
                continue

            # Use fuzzy matching (80%+ similarity = duplicate)
            similarity = SequenceMatcher(None, description.lower(), other_desc.lower()).ratio()
            if similarity > 0.80:
                return False, post_name

        return True, None

    def analyze_description(self,
                          post_name: str,
                          post_metadata: Dict,
                          post_content: str,
                          post_title: str) -> Dict:
        """
        Analyze meta description quality.

        Returns:
            dict: {
                'post': str,
                'current_description': str,
                'length': int,
                'length_compliant': bool,  # 130-155 chars
                'has_primary_keyword': bool,
                'primary_keyword': str,
                'is_unique': bool,
                'duplicate_of': Optional[str],
                'has_action_verb': bool,
                'quality_score': int,  # 0-100
                'recommendation': str,
                'issues': [str]
            }
        """
        description = post_metadata.get('description', '')
        tags = post_metadata.get('tags', [])

        # Extract primary keyword
        primary_keyword = self.extract_primary_keyword(post_content, post_title, tags)

        # Check length compliance
        length = len(description)
        length_compliant = OPTIMAL_MIN <= length <= OPTIMAL_MAX

        # Check for primary keyword
        has_keyword = primary_keyword.lower() in description.lower()

        # Check uniqueness
        is_unique, duplicate_of = self.check_uniqueness(description, post_name)

        # Check for action verb
        has_action_verb = any(verb.lower() in description.lower() for verb in ACTION_VERBS)

        # Calculate quality score (0-100)
        score = 0
        issues = []

        # Length: 40 points
        if OPTIMAL_MIN <= length <= OPTIMAL_MAX:
            score += 40
        elif MIN_CHARS <= length < OPTIMAL_MIN:
            score += 30
            issues.append(f"Length {length} chars (expand to {OPTIMAL_MIN}-{OPTIMAL_MAX} for optimal CTR)")
        elif OPTIMAL_MAX < length <= MAX_CHARS:
            score += 30
            issues.append(f"Length {length} chars (reduce to {OPTIMAL_MIN}-{OPTIMAL_MAX} for optimal CTR)")
        elif length < MIN_CHARS:
            score += 10
            issues.append(f"Too short ({length} chars, minimum {MIN_CHARS})")
        else:
            score += 5
            issues.append(f"Too long ({length} chars, maximum {MAX_CHARS})")

        # Primary keyword: 30 points
        if has_keyword:
            score += 30
        else:
            issues.append(f"Missing primary keyword: '{primary_keyword}'")

        # Uniqueness: 20 points
        if is_unique:
            score += 20
        else:
            issues.append(f"Similar to: {duplicate_of}")

        # Action verb: 10 points
        if has_action_verb:
            score += 10
        else:
            issues.append("No action verb (Implement, Build, Secure, etc.)")

        # Generate recommendation
        recommendation = self.generate_optimized_description(
            post_content, primary_keyword, post_title, description
        )

        return {
            'post': post_name,
            'current_description': description,
            'length': length,
            'length_compliant': length_compliant,
            'has_primary_keyword': has_keyword,
            'primary_keyword': primary_keyword,
            'is_unique': is_unique,
            'duplicate_of': duplicate_of,
            'has_action_verb': has_action_verb,
            'quality_score': score,
            'recommendation': recommendation,
            'issues': issues
        }

    def generate_optimized_description(self,
                                      post_content: str,
                                      primary_keyword: str,
                                      post_title: str,
                                      current_description: str = None) -> str:
        """
        Generate SEO-optimized description.

        Template: "[Action verb] [primary keyword] [benefit/outcome] - [scope]"
        Length: 130-155 characters
        Includes: primary_keyword

        Strategy:
        - Extract key benefit from intro paragraph
        - Use active voice (Implement, Build, Secure)
        - Include specific outcome/timeframe
        - Optimize for 145 chars (mobile + desktop)

        Returns: str (optimized description)
        """
        if current_description and OPTIMAL_MIN <= len(current_description) <= OPTIMAL_MAX:
            # Already optimal length
            if primary_keyword.lower() in current_description.lower():
                return current_description

            # Just add keyword
            return f"{primary_keyword.title()}: {current_description}"[:OPTIMAL_MAX]

        # Extract first paragraph (intro)
        paragraphs = [p.strip() for p in post_content.split('\n\n') if p.strip()]
        intro = paragraphs[0] if paragraphs else post_title

        # Extract key benefit (look for words like: learn, build, secure, implement)
        benefit_words = ["learn", "build", "secure", "implement", "deploy", "configure"]
        benefit = None
        for word in benefit_words:
            if word in intro.lower():
                # Extract sentence containing benefit word
                sentences = intro.split('.')
                for sent in sentences:
                    if word in sent.lower():
                        benefit = sent.strip()
                        break
                if benefit:
                    break

        # Select action verb
        action_verb = "Explore"
        for verb in ACTION_VERBS:
            if verb.lower() in intro.lower():
                action_verb = verb
                break

        # Build optimized description
        # Template: "[Verb] [keyword] [benefit] - [scope]"
        if benefit and len(benefit) > 20:
            # Use extracted benefit
            description = f"{action_verb} {primary_keyword}: {benefit[:100]}"
        else:
            # Generic template
            description = f"{action_verb} {primary_keyword} with practical examples, implementation guide, and security considerations"

        # Trim to optimal length (145 chars target)
        if len(description) > OPTIMAL_MAX:
            description = description[:OPTIMAL_MAX-3] + "..."

        return description

    def load_all_descriptions(self) -> None:
        """Load all post descriptions for uniqueness checking."""
        for filepath in self.posts_dir.glob("*.md"):
            try:
                content = filepath.read_text(encoding='utf-8')
                frontmatter, _, _ = self.extract_frontmatter(content)
                if frontmatter and 'description' in frontmatter:
                    self.all_descriptions[filepath.name] = frontmatter['description']
            except Exception as e:
                self.logger.warning(f"Error loading {filepath.name}: {e}")

    def analyze_post(self, filepath: Path) -> Optional[Dict]:
        """Analyze a single blog post."""
        try:
            content = filepath.read_text(encoding='utf-8')
            frontmatter, _, body = self.extract_frontmatter(content)

            if not frontmatter:
                self.logger.warning(f"Skipping {filepath.name}: No frontmatter")
                return None

            if 'description' not in frontmatter:
                self.logger.warning(f"Skipping {filepath.name}: No description")
                return None

            title = frontmatter.get('title', filepath.stem)

            analysis = self.analyze_description(
                filepath.name, frontmatter, body, title
            )

            return analysis

        except Exception as e:
            self.logger.error(f"Error analyzing {filepath.name}: {e}")
            return None

    def batch_analyze(self, output_csv: Optional[Path] = None) -> List[Dict]:
        """Analyze all descriptions, optionally generate CSV report."""
        self.logger.info("Loading all descriptions for uniqueness check...")
        self.load_all_descriptions()

        self.logger.info(f"Analyzing {len(self.all_descriptions)} posts...")

        results = []
        for filepath in sorted(self.posts_dir.glob("*.md")):
            analysis = self.analyze_post(filepath)
            if analysis:
                results.append(analysis)

                # Log summary
                score = analysis['quality_score']
                emoji = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
                self.logger.info(
                    f"{emoji} {filepath.name}: {score}/100 "
                    f"({analysis['length']} chars, keyword: {analysis['primary_keyword']})"
                )

        # Generate CSV if requested
        if output_csv and results:
            self._write_csv_report(results, output_csv)

        return results

    def _write_csv_report(self, results: List[Dict], output_path: Path) -> None:
        """Write analysis results to CSV."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            fieldnames = [
                'post', 'quality_score', 'length', 'length_compliant',
                'has_primary_keyword', 'primary_keyword', 'is_unique',
                'has_action_verb', 'issues', 'current_description', 'recommendation'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for result in results:
                row = {
                    'post': result['post'],
                    'quality_score': result['quality_score'],
                    'length': result['length'],
                    'length_compliant': result['length_compliant'],
                    'has_primary_keyword': result['has_primary_keyword'],
                    'primary_keyword': result['primary_keyword'],
                    'is_unique': result['is_unique'],
                    'has_action_verb': result['has_action_verb'],
                    'issues': '; '.join(result['issues']),
                    'current_description': result['current_description'],
                    'recommendation': result['recommendation']
                }
                writer.writerow(row)

        self.logger.info(f"CSV report saved to: {output_path}")

    def print_summary(self, results: List[Dict]) -> None:
        """Print summary statistics."""
        if not results:
            self.logger.warning("No results to summarize")
            return

        total = len(results)
        avg_score = sum(r['quality_score'] for r in results) / total
        avg_length = sum(r['length'] for r in results) / total

        length_compliant = sum(1 for r in results if r['length_compliant'])
        has_keyword = sum(1 for r in results if r['has_primary_keyword'])
        is_unique = sum(1 for r in results if r['is_unique'])
        has_action = sum(1 for r in results if r['has_action_verb'])

        high_quality = sum(1 for r in results if r['quality_score'] >= 80)
        medium_quality = sum(1 for r in results if 60 <= r['quality_score'] < 80)
        low_quality = sum(1 for r in results if r['quality_score'] < 60)

        self.logger.info("\n" + "="*70)
        self.logger.info("SEO META DESCRIPTION ANALYSIS SUMMARY")
        self.logger.info("="*70)

        self.logger.info(f"\n📊 Overall Statistics:")
        self.logger.info(f"   Total posts analyzed: {total}")
        self.logger.info(f"   Average quality score: {avg_score:.1f}/100")
        self.logger.info(f"   Average description length: {avg_length:.1f} chars")

        self.logger.info(f"\n📏 Length Compliance (130-155 chars):")
        self.logger.info(f"   Optimal length: {length_compliant}/{total} ({length_compliant/total*100:.1f}%)")

        self.logger.info(f"\n🔑 Keyword Analysis:")
        self.logger.info(f"   Has primary keyword: {has_keyword}/{total} ({has_keyword/total*100:.1f}%)")

        self.logger.info(f"\n✨ Uniqueness:")
        self.logger.info(f"   Unique descriptions: {is_unique}/{total} ({is_unique/total*100:.1f}%)")

        self.logger.info(f"\n💪 Action Verbs:")
        self.logger.info(f"   Has action verb: {has_action}/{total} ({has_action/total*100:.1f}%)")

        self.logger.info(f"\n🎯 Quality Distribution:")
        self.logger.info(f"   High (80-100): {high_quality} ({high_quality/total*100:.1f}%)")
        self.logger.info(f"   Medium (60-79): {medium_quality} ({medium_quality/total*100:.1f}%)")
        self.logger.info(f"   Low (<60): {low_quality} ({low_quality/total*100:.1f}%)")

        self.logger.info("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Optimize SEO Meta Descriptions with Keyword Analysis'
    )
    parser.add_argument('--post', type=Path, help='Analyze single post')
    parser.add_argument('--batch', action='store_true', help='Analyze all posts')
    parser.add_argument('--csv', type=Path, help='Output CSV report path')
    parser.add_argument('--generate', action='store_true', help='Generate recommendations')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.debug else logging.INFO
    logger = setup_logger(__name__, level=level)

    logger.info("SEO Meta Description Optimizer v3.0.0")
    logger.info("="*70)

    optimizer = DescriptionOptimizer(logger=logger)

    # Single post analysis
    if args.post:
        if not args.post.exists():
            logger.error(f"Post not found: {args.post}")
            return 1

        logger.info(f"Analyzing: {args.post.name}")
        optimizer.load_all_descriptions()

        analysis = optimizer.analyze_post(args.post)
        if analysis:
            logger.info(f"\n📊 Analysis Results:")
            logger.info(f"   Quality Score: {analysis['quality_score']}/100")
            logger.info(f"   Length: {analysis['length']} chars")
            logger.info(f"   Primary Keyword: {analysis['primary_keyword']}")
            logger.info(f"   Has Keyword: {analysis['has_primary_keyword']}")
            logger.info(f"   Unique: {analysis['is_unique']}")
            logger.info(f"   Action Verb: {analysis['has_action_verb']}")

            if analysis['issues']:
                logger.info(f"\n⚠️  Issues:")
                for issue in analysis['issues']:
                    logger.info(f"   - {issue}")

            if args.generate:
                logger.info(f"\n💡 Recommended Description:")
                logger.info(f"   {analysis['recommendation']}")
                logger.info(f"   ({len(analysis['recommendation'])} chars)")

        return 0

    # Batch analysis
    if args.batch:
        results = optimizer.batch_analyze(args.csv)
        optimizer.print_summary(results)

        if args.generate:
            logger.info("\n📝 Top 5 Posts Needing Optimization:")
            sorted_results = sorted(results, key=lambda x: x['quality_score'])
            for i, result in enumerate(sorted_results[:5], 1):
                logger.info(f"\n{i}. {result['post']} (Score: {result['quality_score']}/100)")
                logger.info(f"   Current: {result['current_description']}")
                logger.info(f"   Recommended: {result['recommendation']}")

        return 0

    # No action specified
    parser.print_help()
    return 1


if __name__ == "__main__":
    exit(main())
