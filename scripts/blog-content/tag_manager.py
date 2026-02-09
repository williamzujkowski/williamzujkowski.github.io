#!/usr/bin/env -S uv run python3
"""
SCRIPT: tag-manager.py
PURPOSE: Tag Strategy Management - Analyze, consolidate, and optimize blog post tags
CATEGORY: blog_content
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-11

DESCRIPTION:
    Manages tag strategy across all blog posts to improve discoverability and SEO:
    - Audits current tag distribution and usage patterns
    - Applies tag consolidation using research-backed mapping (120 → 44 tags)
    - Enforces 3-5 tags per post guideline (blog-patterns.md standard)
    - Validates tag consistency and naming conventions
    - Generates quality scores and actionable recommendations
    - Auto-suggests tags from content for posts without tags

    Target: 3-5 tags/post for optimal SEO and user navigation
    Focus: Technical accuracy, discoverability, and consistency

LLM_USAGE:
    python scripts/blog-content/tag-manager.py [options]

ARGUMENTS:
    --audit: Analyze current tag distribution and usage
    --consolidate: Apply tag consolidation using mapping file
    --consolidation-map PATH: Path to consolidation map JSON (default: tmp/tag-consolidation-map.json)
    --apply-suggestions: Apply auto-suggested tags to posts without tags
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

    # Preview consolidation (dry-run)
    python scripts/blog-content/tag-manager.py --consolidate --dry-run --batch

    # Apply consolidation
    python scripts/blog-content/tag-manager.py --consolidate --batch

    # Apply suggestions to posts without tags
    python scripts/blog-content/tag-manager.py --consolidate --apply-suggestions --batch

    # Verify results
    python scripts/blog-content/tag-manager.py --audit --batch

CONSOLIDATION WORKFLOW:
    1. Audit current state:
       python scripts/blog-content/tag-manager.py --audit --batch

    2. Preview consolidation (dry-run):
       python scripts/blog-content/tag-manager.py --consolidate --dry-run --batch

    3. Apply consolidation:
       python scripts/blog-content/tag-manager.py --consolidate --batch

    4. Apply suggestions to posts without tags:
       python scripts/blog-content/tag-manager.py --consolidate --apply-suggestions --batch

    5. Verify results:
       python scripts/blog-content/tag-manager.py --audit --batch

OUTPUT:
    - Tag distribution statistics (frequency, co-occurrence patterns)
    - Posts violating 3-5 tag guideline with recommendations
    - Consolidation results (120 → 44 tags, 63.3% reduction)
    - Quality scores per post (0-100 based on tag strategy compliance)
    - CSV report with detailed metrics
    - Applied changes summary

TAG CONSOLIDATION PATTERNS:
    - Direct 1:1: "cybersecurity" → "security"
    - Synonym merge: "ai-ml" → "ai"
    - Technology consolidation: "containers" → "docker"
    - Category standardization: "pytorch" → "machine-learning"
    - Deprecated removal: "posts", "projects"

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
from typing import Any, Dict, List, Tuple, Optional, Set
from collections import Counter, defaultdict
from difflib import SequenceMatcher

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Configuration
VERSION = "2.0.0"
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

        # Consolidation state
        self.consolidation_map: Optional[Dict[str, Any]] = None

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

    def load_consolidation_map(self, map_path: str) -> Dict[str, Any]:
        """
        Load and validate tag consolidation mapping.

        Args:
            map_path: Path to consolidation map JSON

        Returns:
            Dict with consolidations, deprecated, canonical_tags, taxonomy

        Raises:
            FileNotFoundError: If map file doesn't exist
            ValueError: If JSON invalid or missing required keys
        """
        map_file = Path(map_path)
        if not map_file.exists():
            raise FileNotFoundError(f"Consolidation map not found: {map_path}")

        try:
            with open(map_file, 'r') as f:
                consolidation_map = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in consolidation map: {e}")

        # Validate required keys
        required_keys = ['consolidations', 'deprecated', 'canonical_tags', 'taxonomy']
        missing = [k for k in required_keys if k not in consolidation_map]
        if missing:
            raise ValueError(f"Consolidation map missing required keys: {missing}")

        self.logger.info(f"Loaded consolidation map: {len(consolidation_map['consolidations'])} rules, "
                        f"{len(consolidation_map['canonical_tags'])} canonical tags")

        self.consolidation_map = consolidation_map
        return consolidation_map

    def consolidate_tags(self, tags: List[str]) -> Tuple[List[str], List[str]]:
        """
        Apply consolidation rules to tag list.

        Args:
            tags: Original tag list from post

        Returns:
            Tuple of (consolidated_tags, changes_made)
            - consolidated_tags: List of canonical tags
            - changes_made: List of change descriptions (for logging/reporting)

        Logic:
            1. Normalize tags (lowercase, strip whitespace)
            2. Apply consolidation rules (map old → new)
            3. Remove deprecated tags
            4. Remove duplicates (after consolidation)
            5. Sort alphabetically
            6. Validate all tags are canonical
        """
        if not self.consolidation_map:
            raise ValueError("Consolidation map not loaded. Call load_consolidation_map() first.")

        self.logger.debug(f"consolidate_tags called with: {tags}")

        if not tags:
            self.logger.debug("No tags to consolidate, returning empty lists")
            return [], []

        consolidations = self.consolidation_map['consolidations']
        deprecated = self.consolidation_map['deprecated']
        canonical_tags = self.consolidation_map['canonical_tags']

        changes = []
        result_tags = []

        for tag in tags:
            # Normalize
            normalized = tag.lower().strip()

            # Check if deprecated
            if normalized in deprecated:
                changes.append(f"Removed deprecated tag: {normalized}")
                continue

            # Apply consolidation rule
            if normalized in consolidations:
                new_tag = consolidations[normalized]
                changes.append(f"Consolidated {normalized} → {new_tag}")
                result_tags.append(new_tag)
            else:
                # Keep as-is if already canonical
                if normalized in canonical_tags:
                    result_tags.append(normalized)
                else:
                    # Unrecognized tag (not in map), keep but warn
                    self.logger.warning(f"Unrecognized tag (not in consolidation map): {normalized}")
                    result_tags.append(normalized)

        # Remove duplicates (can occur after consolidation)
        unique_tags = []
        seen = set()
        for tag in result_tags:
            if tag not in seen:
                unique_tags.append(tag)
                seen.add(tag)
            else:
                changes.append(f"Removed duplicate: {tag}")

        # Sort alphabetically
        unique_tags.sort()

        self.logger.debug(f"Returning consolidated_tags={unique_tags}, changes={changes}")
        result = (unique_tags, changes)
        self.logger.debug(f"Result type: {type(result)}, Result: {result}")
        return result

    def suggest_tags_from_content(self, post_path: str, max_suggestions: int = 5) -> List[str]:
        """
        Extract tag suggestions from post content.

        Args:
            post_path: Path to markdown post
            max_suggestions: Maximum tags to suggest (default 5)

        Returns:
            List of suggested canonical tags

        Logic:
            1. Read post frontmatter and content
            2. Extract keywords from title and meta description
            3. Match keywords against taxonomy categories
            4. Parse code block language tags (Python → python)
            5. Rank suggestions by confidence
            6. Return top N suggestions (3-5 target)
        """
        if not self.consolidation_map:
            raise ValueError("Consolidation map not loaded. Call load_consolidation_map() first.")

        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"Failed to read post {post_path}: {e}")
            return []

        suggestions = []
        confidence_scores = {}

        # Extract frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_text = parts[1]
                body = parts[2]

                # Extract title
                title_match = re.search(r'title:\s*["\']?(.+?)["\']?\s*$', frontmatter_text, re.MULTILINE)
                title = title_match.group(1).lower() if title_match else ""

                # Extract description
                desc_match = re.search(r'description:\s*["\']?(.+?)["\']?\s*$', frontmatter_text, re.MULTILINE)
                description = desc_match.group(1).lower() if desc_match else ""

                # Combine search text
                search_text = f"{title} {description}"

                # Match against canonical tags (keyword matching)
                canonical_tags = self.consolidation_map['canonical_tags']
                for tag in canonical_tags:
                    # Simple keyword matching (can be improved with fuzzy matching)
                    tag_keywords = tag.replace('-', ' ').split()
                    matches = sum(1 for keyword in tag_keywords if keyword in search_text)
                    if matches > 0:
                        confidence_scores[tag] = matches

                # Parse code blocks for language tags
                code_langs = re.findall(r'```(\w+)', body)
                lang_map = {
                    'python': 'python', 'py': 'python',
                    'javascript': 'javascript', 'js': 'javascript',
                    'bash': 'bash', 'shell': 'bash',
                    'yaml': 'devops', 'yml': 'devops',
                    'dockerfile': 'docker'
                }
                for lang in set(code_langs):
                    mapped = lang_map.get(lang.lower())
                    if mapped and mapped in canonical_tags:
                        confidence_scores[mapped] = confidence_scores.get(mapped, 0) + 2

        # Sort by confidence and take top N
        sorted_suggestions = sorted(confidence_scores.items(), key=lambda x: x[1], reverse=True)
        suggestions = [tag for tag, score in sorted_suggestions[:max_suggestions]]

        self.logger.info(f"Generated {len(suggestions)} tag suggestions for {Path(post_path).name}")
        return suggestions

    def update_frontmatter_tags(self, frontmatter_text: str, tags: List[str]) -> str:
        """
        Update tags field in YAML frontmatter.

        Args:
            frontmatter_text: Original frontmatter string
            tags: New tag list

        Returns:
            Updated frontmatter string
        """
        # Remove existing tags section (both array and list formats)
        lines = frontmatter_text.split('\n')
        new_lines = []
        in_tags = False

        for line in lines:
            if line.startswith('tags:'):
                in_tags = True
                continue
            elif in_tags and (line.startswith('  -') or line.startswith('- ')):
                continue
            elif in_tags and line.strip() and not line.startswith(' '):
                in_tags = False

            if not in_tags:
                new_lines.append(line)

        # Add new tags section (YAML list format)
        tags_section = 'tags:\n' + '\n'.join(f'  - {tag}' for tag in tags)

        # Insert before last line (usually empty)
        if new_lines and not new_lines[-1].strip():
            new_lines.insert(-1, tags_section)
        else:
            new_lines.append(tags_section)

        return '\n'.join(new_lines)

    def apply_consolidation_to_post(self, post_path: str, dry_run: bool = False,
                                   apply_suggestions: bool = False) -> Dict[str, Any]:
        """
        Consolidate tags for single post and optionally write back.

        Args:
            post_path: Path to markdown post
            dry_run: If True, don't write files (preview only)
            apply_suggestions: If True, suggest tags for posts without tags

        Returns:
            Dict with:
                - original_tags: List[str]
                - consolidated_tags: List[str]
                - changes: List[str] (descriptions of changes)
                - compliant: bool (3-5 tag target met)
                - suggestion_applied: bool
        """
        if not self.consolidation_map:
            raise ValueError("Consolidation map not loaded. Call load_consolidation_map() first.")

        # Read post
        try:
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            self.logger.error(f"Failed to read post {post_path}: {e}")
            return {'error': str(e)}

        # Extract frontmatter
        if not content.startswith('---'):
            self.logger.warning(f"Post missing frontmatter: {post_path}")
            return {'error': 'No frontmatter'}

        parts = content.split('---', 2)
        if len(parts) < 3:
            self.logger.warning(f"Invalid frontmatter structure: {post_path}")
            return {'error': 'Invalid frontmatter'}

        frontmatter_text = parts[1]
        body = parts[2]

        # Parse frontmatter to get current tags
        try:
            frontmatter_dict = yaml.safe_load(frontmatter_text)
            if frontmatter_dict is None:
                frontmatter_dict = {}
        except yaml.YAMLError as e:
            self.logger.error(f"YAML parse error in {post_path}: {e}")
            return {'error': f'YAML parse error: {e}'}

        # Extract current tags
        original_tags = self.parse_tags(frontmatter_dict)

        # Decide: consolidate or suggest
        if not original_tags and apply_suggestions:
            # Suggest tags from content
            suggested_tags = self.suggest_tags_from_content(post_path)
            consolidated_tags = suggested_tags
            changes = [f"Suggested {len(suggested_tags)} tags from content"]
            suggestion_applied = True
        else:
            # Consolidate existing tags
            consolidated_tags, changes = self.consolidate_tags(original_tags)
            suggestion_applied = False

        # Validate compliance (3-5 tags)
        compliant = MIN_TAGS <= len(consolidated_tags) <= MAX_TAGS

        # Write back if not dry-run
        if not dry_run and (original_tags != consolidated_tags):
            # Update frontmatter with new tags
            updated_frontmatter = self.update_frontmatter_tags(frontmatter_text, consolidated_tags)
            updated_content = f"---\n{updated_frontmatter}\n---{body}"

            try:
                with open(post_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                self.logger.info(f"Updated tags in {Path(post_path).name}")
            except Exception as e:
                self.logger.error(f"Failed to write post {post_path}: {e}")
                return {'error': str(e)}

        return {
            'original_tags': original_tags,
            'consolidated_tags': consolidated_tags,
            'changes': changes,
            'compliant': compliant,
            'suggestion_applied': suggestion_applied
        }

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

    def consolidate_tags_batch(self, posts: List[Path], dry_run: bool = True) -> Dict:
        """
        Apply tag consolidation strategy (DEPRECATED - use apply_consolidation_to_post).

        Args:
            posts: List of post file paths
            dry_run: If True, preview changes without writing

        Returns:
            Consolidation results dict
        """
        # Deprecated method - functionality moved to apply_consolidation_to_post
        raise NotImplementedError("Use apply_consolidation_to_post instead")

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

    def generate_json_metrics(self, analysis: Dict, output_path: Path) -> None:
        """
        Generate JSON metrics for dashboard consumption.

        Args:
            analysis: Analysis results from analyze_tag_distribution()
            output_path: Path to output JSON file
        """
        if not analysis:
            self.logger.warning("No analysis data available for JSON generation")
            return

        # Calculate compliance rate (posts with 3-5 tags)
        total_posts = analysis['total_posts']
        compliant_posts = analysis['posts_with_3_5_tags']
        compliance_rate = (compliant_posts / total_posts * 100) if total_posts > 0 else 0

        # Get top 10 tags
        top_10_tags = [
            {"tag": tag, "count": count}
            for tag, count in list(analysis['tag_frequency'].items())[:10]
        ]

        # Build metrics JSON
        metrics = {
            "generated": datetime.now().isoformat(),
            "total_unique_tags": analysis['total_unique_tags'],
            "avg_tags_per_post": round(analysis['avg_tags_per_post'], 1),
            "posts_with_0_tags": analysis['posts_with_0_tags'],
            "posts_with_1_2_tags": analysis['posts_with_1_2_tags'],
            "posts_with_3_5_tags": analysis['posts_with_3_5_tags'],
            "posts_with_6plus_tags": analysis['posts_with_6plus_tags'],
            "compliance_rate": round(compliance_rate, 1),
            "top_10_tags": top_10_tags
        }

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)

        self.logger.info(f"JSON metrics written to {output_path}")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description=f'Tag Strategy Management v{VERSION}',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit current tag usage
  %(prog)s --audit --batch

  # Preview consolidation (dry-run)
  %(prog)s --consolidate --dry-run --batch

  # Apply consolidation
  %(prog)s --consolidate --batch

  # Apply consolidation to single post
  %(prog)s --consolidate --post src/posts/example.md
        """
    )
    parser.add_argument('--audit', action='store_true', help='Analyze current tag distribution')
    parser.add_argument('--consolidate', action='store_true', help='Apply tag consolidation using mapping file')
    parser.add_argument('--consolidation-map', default='tmp/tag-consolidation-map.json',
                       help='Path to consolidation map JSON (default: tmp/tag-consolidation-map.json)')
    parser.add_argument('--apply-suggestions', action='store_true',
                       help='Apply auto-suggested tags to posts without tags')
    parser.add_argument('--post', type=Path, help='Analyze/update single post')
    parser.add_argument('--batch', action='store_true', help='Process all posts')
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without writing')
    parser.add_argument('--csv', type=Path, help='Output CSV report path')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose output')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress info messages')
    parser.add_argument('--json', action='store_true',
                       help='Generate JSON metrics for dashboard (saved to docs/reports/tag-metrics.json)')
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

        # Generate JSON metrics if requested
        if args.json:
            json_output = Path("docs/reports/tag-metrics.json")
            manager.generate_json_metrics(analysis, json_output)

        if args.csv:
            # TODO: Generate CSV report
            logger.info(f"CSV output not yet implemented")

    if args.consolidate:
        try:
            # Load consolidation map
            consolidation_map = manager.load_consolidation_map(args.consolidation_map)

            if args.dry_run:
                logger.info("DRY RUN MODE - No files will be modified")

            if args.batch:
                # Process all posts
                logger.info(f"Processing {len(posts)} posts...")

                results = []
                for post in posts:
                    try:
                        result = manager.apply_consolidation_to_post(
                            str(post),
                            dry_run=args.dry_run,
                            apply_suggestions=args.apply_suggestions
                        )
                        if result is None:
                            result = {'error': 'Unknown error - returned None'}
                        results.append((post.name, result))
                    except Exception as e:
                        logger.error(f"Failed to process {post.name}: {e}")
                        results.append((post.name, {'error': str(e)}))

                # Report results
                compliant_count = sum(1 for _, r in results if r.get('compliant'))
                changed_count = sum(1 for _, r in results if r.get('changes'))
                suggestion_count = sum(1 for _, r in results if r.get('suggestion_applied'))
                error_count = sum(1 for _, r in results if 'error' in r)

                logger.info("\n" + "="*70)
                logger.info("CONSOLIDATION RESULTS")
                logger.info("="*70)
                logger.info(f"\n📊 Overall Statistics:")
                logger.info(f"   Posts processed: {len(results)}")
                logger.info(f"   Posts changed: {changed_count}")
                logger.info(f"   Posts with suggestions applied: {suggestion_count}")
                logger.info(f"   Posts compliant (3-5 tags): {compliant_count}/{len(results)} ({100*compliant_count/len(results):.1f}%)")
                if error_count > 0:
                    logger.warning(f"   Posts with errors: {error_count}")

                # Show detailed changes for verbose mode
                if args.verbose:
                    logger.info(f"\n📝 Detailed Changes:")
                    for post_name, result in results:
                        if result.get('changes'):
                            logger.info(f"\n   {post_name}:")
                            logger.info(f"      Original tags: {result.get('original_tags', [])}")
                            logger.info(f"      Consolidated tags: {result.get('consolidated_tags', [])}")
                            for change in result.get('changes', []):
                                logger.info(f"      - {change}")

                logger.info("\n" + "="*70)

            elif args.post:
                # Process single post
                try:
                    result = manager.apply_consolidation_to_post(
                        str(args.post),
                        dry_run=args.dry_run,
                        apply_suggestions=args.apply_suggestions
                    )

                    if result is None:
                        logger.error("apply_consolidation_to_post returned None")
                        return 1

                    logger.info(f"\nPost: {args.post.name}")
                    logger.info(f"  Original tags: {result.get('original_tags', [])}")
                    logger.info(f"  Consolidated tags: {result.get('consolidated_tags', [])}")
                    logger.info(f"  Changes: {len(result.get('changes', []))}")
                    for change in result.get('changes', []):
                        logger.info(f"    - {change}")
                    logger.info(f"  Compliant: {'YES' if result.get('compliant') else 'NO'}")
                    if result.get('suggestion_applied'):
                        logger.info(f"  Suggestions applied: YES")
                except Exception as e:
                    import traceback
                    logger.error(f"Failed to process post: {e}")
                    logger.error(traceback.format_exc())
                    return 1

        except Exception as e:
            logger.error(f"Consolidation failed: {e}")
            return 1

    if not (args.audit or args.consolidate):
        logger.warning("No action specified. Use --audit or --consolidate")
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
