#!/usr/bin/env -S uv run python3
"""
SCRIPT: tag-manager.py
PURPOSE: Tag Strategy Management - Analyze, consolidate, and optimize blog post tags
CATEGORY: blog_content
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-11-11

DESCRIPTION:
    Manages tag strategy across all blog posts to improve discoverability and SEO:
    - Audits current tag distribution and usage patterns
    - Identifies consolidation opportunities (plurals, synonyms, similar terms)
    - Enforces 3-5 tags per post guideline (blog-patterns.md standard)
    - Validates tag consistency and naming conventions
    - Generates quality scores and actionable recommendations
    - Applies tag strategy changes with dry-run support

    Target: 3-5 tags/post for optimal SEO and user navigation
    Focus: Technical accuracy, discoverability, and consistency

LLM_USAGE:
    python scripts/blog-content/tag-manager.py [options]

ARGUMENTS:
    --audit: Analyze current tag distribution and usage
    --consolidate: Suggest tag consolidation opportunities
    --apply: Apply recommended tag strategy to posts
    --post PATH: Analyze/update single post
    --batch: Process all posts in src/posts/
    --dry-run: Preview changes without writing to files
    --csv PATH: Output CSV report
    --debug: Enable debug logging
    --verbose, -v: Enable verbose output
    --quiet, -q: Suppress info messages

EXAMPLES:
    # Audit current tag usage across all posts
    python scripts/blog-content/tag-manager.py --audit --batch

    # Identify consolidation opportunities
    python scripts/blog-content/tag-manager.py --consolidate --batch --csv reports/tag-consolidation.csv

    # Preview tag strategy changes (dry-run)
    python scripts/blog-content/tag-manager.py --apply --batch --dry-run

    # Apply tag strategy to single post
    python scripts/blog-content/tag-manager.py --apply --post src/posts/welcome.md

    # Full workflow: audit + consolidate + apply
    python scripts/blog-content/tag-manager.py --audit --consolidate --apply --batch

OUTPUT:
    - Tag distribution statistics (frequency, co-occurrence patterns)
    - Posts violating 3-5 tag guideline with recommendations
    - Consolidation suggestions (plural→singular, synonyms, merges)
    - Quality scores per post (0-100 based on tag strategy compliance)
    - CSV report with detailed metrics
    - Applied changes summary (if --apply used)

TAG STRATEGY PATTERNS:
    - Plural→Singular: "containers" → "container"
    - Synonym consolidation: "machine-learning" ↔ "ml" → "machine-learning"
    - Category standardization: "k8s" → "kubernetes"
    - Hyphenation consistency: "machine_learning" → "machine-learning"
    - Case normalization: "Docker" → "docker"

QUALITY SCORING (0-100):
    - Tag count compliance (3-5): +40 points
    - No duplicate tags: +20 points
    - Consistent naming conventions: +20 points
    - Co-occurrence with hub tags: +10 points
    - No deprecated/synonym tags: +10 points

DEPENDENCIES:
    - Python 3.8+
    - PyYAML for frontmatter parsing
    - scripts/lib/logging_config.py for centralized logging

RELATED_SCRIPTS:
    - scripts/blog-content/metadata-validator.py: Metadata validation
    - scripts/blog-content/optimize-seo-descriptions.py: SEO optimization
    - scripts/blog-content/analyze-compliance.py: Content compliance

MANIFEST_REGISTRY: scripts/blog-content/tag-manager.py
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
from collections import Counter, defaultdict
from difflib import SequenceMatcher

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Configuration
VERSION = "1.0.0"
POSTS_DIR = Path("src/posts")
REPORT_DIR = Path("docs/reports")
MIN_TAGS = 3
MAX_TAGS = 5
OPTIMAL_TAGS = 4

# Hub post tags (from blog-patterns.md - high-value tags for internal linking)
HUB_TAGS = {
    "kubernetes", "docker", "security", "ai", "llm", "homelab",
    "machine-learning", "cryptography", "privacy", "automation"
}

# Known synonym mappings (will be expanded by audit)
SYNONYM_MAP = {
    "k8s": "kubernetes",
    "ml": "machine-learning",
    "ai-ml": "machine-learning",
    "containers": "container",
}

# Deprecated tags (should be replaced)
DEPRECATED_TAGS = {
    "posts",  # Generic, provides no value
    "blog",   # All content is blog posts
}


class TagManager:
    """Manages tag strategy across blog posts."""

    def __init__(self, logger=None):
        self.posts_dir = POSTS_DIR
        self.report_dir = REPORT_DIR
        self.report_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger or logging.getLogger(__name__)

        # Analysis state
        self.tag_frequency: Counter = Counter()
        self.tag_co_occurrence: Dict[str, Counter] = defaultdict(Counter)
        self.post_tags: Dict[str, List[str]] = {}  # filename -> tags
        self.all_tags: Set[str] = set()

    def extract_frontmatter(self, content: str) -> Tuple[Optional[Dict], str, str]:
        """
        Extract YAML frontmatter from markdown content.

        Args:
            content: Raw markdown file content

        Returns:
            Tuple of (frontmatter_dict, frontmatter_text, body)
            frontmatter_dict is None if parsing fails
        """
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

    def parse_tags(self, frontmatter: Dict) -> List[str]:
        """
        Parse tags from frontmatter.

        Handles both YAML list format and array format:
        - tags: [tag1, tag2, tag3]
        - tags:\n  - tag1\n  - tag2

        Args:
            frontmatter: Parsed YAML frontmatter dict

        Returns:
            List of normalized tag strings
        """
        tags = frontmatter.get('tags', [])

        if not tags:
            return []

        # Normalize tags (lowercase, strip whitespace)
        if isinstance(tags, list):
            return [str(tag).lower().strip() for tag in tags if tag]
        elif isinstance(tags, str):
            # Handle single string tag
            return [tags.lower().strip()]

        return []

    def analyze_tag_distribution(self, posts: List[Path]) -> Dict:
        """
        Analyze tag usage across all posts.

        Calculates:
        - Tag frequency (how many posts use each tag)
        - Co-occurrence patterns (which tags appear together)
        - Posts per tag count (distribution of 0, 1-2, 3-5, 6+ tags)

        Args:
            posts: List of post file paths

        Returns:
            Analysis dict with statistics
        """
        self.logger.info(f"Analyzing tag distribution across {len(posts)} posts...")

        for filepath in posts:
            try:
                content = filepath.read_text(encoding='utf-8')
                frontmatter, _, _ = self.extract_frontmatter(content)

                if not frontmatter:
                    self.logger.debug(f"Skipping {filepath.name}: No frontmatter")
                    continue

                tags = self.parse_tags(frontmatter)
                self.post_tags[filepath.name] = tags
                self.all_tags.update(tags)

                # Update frequency
                self.tag_frequency.update(tags)

                # Update co-occurrence matrix
                for i, tag1 in enumerate(tags):
                    for tag2 in tags[i+1:]:
                        self.tag_co_occurrence[tag1][tag2] += 1
                        self.tag_co_occurrence[tag2][tag1] += 1

            except Exception as e:
                self.logger.error(f"Error analyzing {filepath.name}: {e}")

        # Calculate distribution statistics
        tag_counts = Counter(len(tags) for tags in self.post_tags.values())

        analysis = {
            'total_posts': len(posts),
            'total_unique_tags': len(self.all_tags),
            'avg_tags_per_post': sum(len(tags) for tags in self.post_tags.values()) / len(posts) if posts else 0,
            'tag_frequency': dict(self.tag_frequency.most_common()),
            'tag_co_occurrence': {k: dict(v.most_common(5)) for k, v in self.tag_co_occurrence.items()},
            'posts_by_tag_count': dict(tag_counts),
            'posts_with_0_tags': tag_counts[0],
            'posts_with_1_2_tags': tag_counts[1] + tag_counts[2],
            'posts_with_3_5_tags': sum(tag_counts[i] for i in range(3, 6)),
            'posts_with_6plus_tags': sum(tag_counts[i] for i in range(6, max(tag_counts.keys()) + 1)) if tag_counts else 0,
        }

        return analysis

    def identify_consolidation_opportunities(self) -> List[Dict]:
        """
        Identify tag consolidation opportunities.

        Patterns detected:
        - Plural/singular variants (containers ↔ container)
        - Hyphenation inconsistencies (machine_learning ↔ machine-learning)
        - Known synonyms (k8s ↔ kubernetes)
        - Similar tags via fuzzy matching (>80% similarity)
        - Deprecated tags (posts, blog)

        Returns:
            List of consolidation suggestions with rationale
        """
        # TODO: Implement after researcher provides baseline
        # Will analyze self.all_tags for patterns
        pass

    def calculate_quality_score(self, post_name: str, tags: List[str]) -> Tuple[int, List[str]]:
        """
        Calculate tag quality score (0-100) for a post.

        Scoring criteria:
        - Tag count compliance (3-5): +40 points
        - No duplicate tags: +20 points
        - Consistent naming conventions: +20 points
        - Co-occurrence with hub tags: +10 points
        - No deprecated/synonym tags: +10 points

        Args:
            post_name: Post filename
            tags: List of tags for the post

        Returns:
            Tuple of (score, issues_list)
        """
        score = 0
        issues = []

        # Tag count compliance (40 points)
        tag_count = len(tags)
        if MIN_TAGS <= tag_count <= MAX_TAGS:
            score += 40
        elif tag_count == 0:
            issues.append("No tags assigned")
        elif tag_count < MIN_TAGS:
            score += 20
            issues.append(f"Too few tags ({tag_count} < {MIN_TAGS})")
        else:  # > MAX_TAGS
            score += 20
            issues.append(f"Too many tags ({tag_count} > {MAX_TAGS})")

        # No duplicate tags (20 points)
        if len(tags) == len(set(tags)):
            score += 20
        else:
            duplicates = [tag for tag in set(tags) if tags.count(tag) > 1]
            issues.append(f"Duplicate tags: {', '.join(duplicates)}")

        # Consistent naming conventions (20 points)
        # Check: lowercase, hyphen-separated, no underscores, no spaces
        naming_violations = [
            tag for tag in tags
            if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', tag)
        ]
        if not naming_violations:
            score += 20
        else:
            issues.append(f"Naming violations: {', '.join(naming_violations)}")

        # Hub tag co-occurrence (10 points)
        if any(tag in HUB_TAGS for tag in tags):
            score += 10
        else:
            issues.append("No hub tags (consider adding: kubernetes, security, ai, etc.)")

        # No deprecated/synonym tags (10 points)
        deprecated = [tag for tag in tags if tag in DEPRECATED_TAGS]
        synonyms = [tag for tag in tags if tag in SYNONYM_MAP]

        if not deprecated and not synonyms:
            score += 10
        else:
            if deprecated:
                issues.append(f"Deprecated tags: {', '.join(deprecated)}")
            if synonyms:
                replacements = [f"{tag}→{SYNONYM_MAP[tag]}" for tag in synonyms]
                issues.append(f"Synonym tags: {', '.join(replacements)}")

        return score, issues

    def generate_recommendations(self, post_name: str, tags: List[str], score: int, issues: List[str]) -> str:
        """
        Generate actionable recommendations for tag improvement.

        Args:
            post_name: Post filename
            tags: Current tags
            score: Quality score
            issues: List of detected issues

        Returns:
            Recommendation string
        """
        # TODO: Implement after researcher provides baseline
        # Will generate specific recommendations based on issues
        pass

    def audit_posts(self, posts: List[Path], output_csv: Optional[Path] = None) -> Dict:
        """
        Audit all posts for tag strategy compliance.

        Args:
            posts: List of post file paths
            output_csv: Optional CSV output path

        Returns:
            Audit results dict
        """
        # TODO: Implement after researcher provides baseline
        pass

    def consolidate_tags(self, posts: List[Path], dry_run: bool = True) -> Dict:
        """
        Apply tag consolidation strategy.

        Args:
            posts: List of post file paths
            dry_run: If True, preview changes without writing

        Returns:
            Consolidation results dict
        """
        # TODO: Implement after researcher provides baseline
        pass

    def apply_tag_strategy(self, filepath: Path, new_tags: List[str], dry_run: bool = True) -> bool:
        """
        Apply new tag strategy to a post.

        Args:
            filepath: Post file path
            new_tags: New tag list to apply
            dry_run: If True, preview without writing

        Returns:
            True if successful, False otherwise
        """
        # TODO: Implement after researcher provides baseline
        pass

    def print_summary(self, analysis: Dict) -> None:
        """
        Print summary statistics.

        Args:
            analysis: Analysis results dict
        """
        self.logger.info("\n" + "="*70)
        self.logger.info("TAG STRATEGY ANALYSIS SUMMARY")
        self.logger.info("="*70)

        self.logger.info(f"\n📊 Overall Statistics:")
        self.logger.info(f"   Total posts: {analysis['total_posts']}")
        self.logger.info(f"   Unique tags: {analysis['total_unique_tags']}")
        self.logger.info(f"   Average tags/post: {analysis['avg_tags_per_post']:.1f}")

        self.logger.info(f"\n📏 Tag Count Distribution:")
        self.logger.info(f"   0 tags: {analysis['posts_with_0_tags']} posts")
        self.logger.info(f"   1-2 tags: {analysis['posts_with_1_2_tags']} posts")
        self.logger.info(f"   3-5 tags (COMPLIANT): {analysis['posts_with_3_5_tags']} posts")
        self.logger.info(f"   6+ tags: {analysis['posts_with_6plus_tags']} posts")

        self.logger.info(f"\n🔝 Top 10 Most Used Tags:")
        for i, (tag, count) in enumerate(list(analysis['tag_frequency'].items())[:10], 1):
            self.logger.info(f"   {i}. {tag}: {count} posts")

        self.logger.info("\n" + "="*70)


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description=f'Tag Strategy Management v{VERSION}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit current tag usage
  %(prog)s --audit --batch

  # Identify consolidation opportunities
  %(prog)s --consolidate --batch --csv reports/tag-consolidation.csv

  # Preview tag strategy changes
  %(prog)s --apply --batch --dry-run

  # Apply strategy to single post
  %(prog)s --apply --post src/posts/welcome.md
        """
    )
    parser.add_argument('--audit', action='store_true', help='Analyze current tag distribution')
    parser.add_argument('--consolidate', action='store_true', help='Suggest tag consolidation')
    parser.add_argument('--apply', action='store_true', help='Apply tag strategy changes')
    parser.add_argument('--post', type=Path, help='Analyze/update single post')
    parser.add_argument('--batch', action='store_true', help='Process all posts')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    parser.add_argument('--csv', type=Path, help='Output CSV report path')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.debug else logging.INFO
    logger = setup_logger(__name__, level=level, quiet=args.quiet)

    logger.info(f"Tag Strategy Manager v{VERSION}")
    logger.info("="*70)

    manager = TagManager(logger=logger)

    # Get post list
    if args.post:
        if not args.post.exists():
            logger.error(f"Post not found: {args.post}")
            return 1
        posts = [args.post]
    elif args.batch:
        posts = sorted(POSTS_DIR.glob("*.md"))
        posts = [p for p in posts if p.name != 'welcome.md']  # Skip welcome page
    else:
        parser.print_help()
        return 1

    # Execute requested actions
    if args.audit:
        logger.info("Running tag distribution audit...")
        analysis = manager.analyze_tag_distribution(posts)
        manager.print_summary(analysis)

        if args.csv:
            # TODO: Generate CSV report
            logger.info(f"CSV output not yet implemented")

    if args.consolidate:
        logger.info("Identifying consolidation opportunities...")
        # TODO: Implement consolidation logic
        logger.info("Consolidation analysis not yet implemented")

    if args.apply:
        logger.info("Applying tag strategy changes...")
        if args.dry_run:
            logger.info("DRY RUN MODE - No files will be modified")
        # TODO: Implement apply logic
        logger.info("Tag application not yet implemented")

    if not (args.audit or args.consolidate or args.apply):
        logger.warning("No action specified. Use --audit, --consolidate, or --apply")
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
