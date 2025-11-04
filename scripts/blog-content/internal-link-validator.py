#!/usr/bin/env -S uv run python3
"""
Internal Link Validator for Blog Posts

Analyzes blog posts to detect internal linking opportunities,
validate existing links, and track link density metrics.

Based on research: 40% organic traffic increase with 6-10 internal links/post
(Backlinko 2024, Moz Study)

Version: 1.0.0
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from logging_config import setup_logger
import re
import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter, defaultdict
from datetime import datetime

logger = setup_logger(__name__)

@dataclass
class BlogPost:
    """Represents a blog post with metadata and content."""
    filepath: Path
    slug: str
    title: str
    date: str
    tags: List[str]
    description: str
    content: str
    internal_links: List[str] = field(default_factory=list)

    def link_density(self) -> int:
        """Calculate internal links per post."""
        return len(self.internal_links)

    def is_foundational(self) -> bool:
        """Check if post is foundational (basic/beginner content)."""
        foundational_keywords = {
            'introduction', 'intro', 'getting started', 'basics',
            'beginner', 'setup', 'installation', 'guide'
        }
        title_lower = self.title.lower()
        desc_lower = self.description.lower()
        return any(kw in title_lower or kw in desc_lower for kw in foundational_keywords)

    def is_advanced(self) -> bool:
        """Check if post is advanced content."""
        advanced_keywords = {
            'advanced', 'deep dive', 'optimization', 'performance',
            'architecture', 'enterprise', 'production', 'scaling'
        }
        title_lower = self.title.lower()
        desc_lower = self.description.lower()
        return any(kw in title_lower or kw in desc_lower for kw in advanced_keywords)

    def extract_keywords(self) -> Set[str]:
        """Extract meaningful keywords from title and description."""
        # Combine title and description
        text = f"{self.title} {self.description}".lower()

        # Remove common words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'how', 'your', 'this', 'that', 'these', 'those', 'my', 'i', 'you', 'is',
            'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had'
        }

        # Extract words (alphanumeric sequences)
        words = re.findall(r'\b[a-z0-9]+(?:-[a-z0-9]+)*\b', text)

        # Filter stop words and short words
        keywords = {w for w in words if w not in stop_words and len(w) > 2}

        # Add tags as keywords
        keywords.update(tag.lower() for tag in self.tags)

        return keywords

@dataclass
class LinkSuggestion:
    """Represents a suggested internal link."""
    from_post: str
    to_post: str
    to_title: str
    relevance_score: float
    reason: str  # "tag_overlap", "topic_progression", "complementary", "keyword_match"
    suggested_section: str  # "introduction", "body", "conclusion"
    anchor_text: str
    shared_tags: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        """Format suggestion for display."""
        return (f"  → {self.to_title}\n"
                f"    Relevance: {self.relevance_score:.2f}\n"
                f"    Reason: {self.reason}\n"
                f"    Section: {self.suggested_section}\n"
                f"    Anchor: {self.anchor_text}\n"
                f"    Shared tags: {', '.join(self.shared_tags) if self.shared_tags else 'N/A'}")

class InternalLinkValidator:
    """Validates and suggests internal links for blog posts."""

    def __init__(self, posts_dir: Path):
        self.posts_dir = Path(posts_dir)
        self.posts: List[BlogPost] = []
        self.posts_by_slug: Dict[str, BlogPost] = {}
        self.link_graph: Dict[str, Set[str]] = defaultdict(set)  # outgoing links per post
        self.incoming_links: Dict[str, Set[str]] = defaultdict(set)  # incoming links per post

    def parse_posts(self) -> None:
        """Parse all blog posts and extract metadata + links."""
        logger.info(f"Parsing posts from {self.posts_dir}")

        if not self.posts_dir.exists():
            logger.error(f"Posts directory not found: {self.posts_dir}")
            return

        post_files = sorted(self.posts_dir.glob("*.md"))
        logger.info(f"Found {len(post_files)} post files")

        for filepath in post_files:
            try:
                post = self._parse_post(filepath)
                if post:
                    self.posts.append(post)
                    self.posts_by_slug[post.slug] = post
            except Exception as e:
                logger.error(f"Error parsing {filepath.name}: {e}")

        logger.info(f"Successfully parsed {len(self.posts)} posts")

        # Build link graph
        self._build_link_graph()

    def _parse_post(self, filepath: Path) -> Optional[BlogPost]:
        """Parse a single blog post file."""
        content = filepath.read_text(encoding='utf-8')

        # Extract frontmatter
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', content, re.DOTALL)
        if not match:
            logger.warning(f"No frontmatter found in {filepath.name}")
            return None

        frontmatter_text, body = match.groups()

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
        except yaml.YAMLError as e:
            logger.error(f"YAML parse error in {filepath.name}: {e}")
            return None

        # Extract required fields
        title = frontmatter.get('title', '')
        date = frontmatter.get('date', '')
        tags = frontmatter.get('tags', [])
        description = frontmatter.get('description', '')

        if not all([title, date, tags]):
            logger.warning(f"Missing required fields in {filepath.name}")
            return None

        # Generate slug from filename
        slug = filepath.stem

        # Extract internal links from body
        internal_links = self._extract_internal_links(body)

        return BlogPost(
            filepath=filepath,
            slug=slug,
            title=title,
            date=str(date),
            tags=tags if isinstance(tags, list) else [tags],
            description=description,
            content=body,
            internal_links=internal_links
        )

    def _extract_internal_links(self, content: str) -> List[str]:
        """Extract internal links from markdown content."""
        # Pattern: [text](/posts/slug) or [text](/posts/slug/)
        pattern = r'\[([^\]]+)\]\(/posts/([^/)]+)/?[^)]*\)'
        matches = re.findall(pattern, content)

        # Return just the slugs
        return [slug for _, slug in matches]

    def _build_link_graph(self) -> None:
        """Build graph of outgoing and incoming links."""
        for post in self.posts:
            for linked_slug in post.internal_links:
                # Add to outgoing links
                self.link_graph[post.slug].add(linked_slug)

                # Add to incoming links (if target post exists)
                if linked_slug in self.posts_by_slug:
                    self.incoming_links[linked_slug].add(post.slug)

        logger.info(f"Built link graph: {len(self.link_graph)} posts with outgoing links")

    def detect_related_posts(self, post: BlogPost, min_score: float = 0.3) -> List[Tuple[BlogPost, float]]:
        """
        Find related posts based on tag overlap and topic similarity.

        Returns list of (related_post, relevance_score) tuples sorted by relevance.
        Relevance score: 0.0-1.0 (higher = more related)
        """
        related = []
        post_keywords = post.extract_keywords()

        for other_post in self.posts:
            if other_post.slug == post.slug:
                continue

            score = 0.0

            # Tag overlap scoring (weighted heavily)
            shared_tags = set(post.tags) & set(other_post.tags)
            if shared_tags:
                # Score: shared_tags / min(tags1, tags2)
                tag_score = len(shared_tags) / min(len(post.tags), len(other_post.tags))
                score += tag_score * 0.7  # 70% weight

            # Keyword overlap scoring
            other_keywords = other_post.extract_keywords()
            shared_keywords = post_keywords & other_keywords
            if shared_keywords and post_keywords:
                keyword_score = len(shared_keywords) / len(post_keywords)
                score += keyword_score * 0.3  # 30% weight

            if score >= min_score:
                related.append((other_post, score))

        # Sort by relevance (highest first)
        related.sort(key=lambda x: x[1], reverse=True)

        return related

    def suggest_links(self, post: BlogPost, max_suggestions: int = 10) -> List[LinkSuggestion]:
        """
        Generate contextual link suggestions for a post.

        Target: 6-10 links per post
        - Introduction: 1-2 foundational links
        - Body: 3-6 contextual links
        - Conclusion: 1-2 next steps links
        """
        suggestions = []

        # Get related posts
        related_posts = self.detect_related_posts(post)

        if not related_posts:
            logger.debug(f"No related posts found for {post.slug}")
            return suggestions

        # Track already linked posts
        already_linked = set(post.internal_links)

        # Count suggestions by section
        intro_count = 0
        body_count = 0
        conclusion_count = 0

        for related_post, relevance in related_posts:
            # Skip if already linked
            if related_post.slug in already_linked:
                continue

            # Skip if we have enough suggestions
            if len(suggestions) >= max_suggestions:
                break

            # Determine section and reason
            section = "body"  # default
            reason = "tag_overlap"

            shared_tags = list(set(post.tags) & set(related_post.tags))

            # Introduction: foundational posts
            if intro_count < 2 and related_post.is_foundational() and not post.is_foundational():
                section = "introduction"
                reason = "topic_progression"
                intro_count += 1
            # Conclusion: advanced posts or newer posts
            elif conclusion_count < 2 and (related_post.is_advanced() or related_post.date > post.date):
                section = "conclusion"
                reason = "topic_progression"
                conclusion_count += 1
            # Body: related by tags/keywords
            elif body_count < 6:
                section = "body"
                if shared_tags:
                    reason = "tag_overlap"
                else:
                    reason = "keyword_match"
                body_count += 1
            else:
                continue  # Skip if section quotas full

            # Generate anchor text
            anchor_text = self._generate_anchor_text(related_post, reason)

            suggestion = LinkSuggestion(
                from_post=post.slug,
                to_post=related_post.slug,
                to_title=related_post.title,
                relevance_score=relevance,
                reason=reason,
                suggested_section=section,
                anchor_text=anchor_text,
                shared_tags=shared_tags
            )

            suggestions.append(suggestion)

        # Sort by section priority (intro -> body -> conclusion) then relevance
        section_order = {"introduction": 0, "body": 1, "conclusion": 2}
        suggestions.sort(key=lambda s: (section_order[s.suggested_section], -s.relevance_score))

        return suggestions

    def _generate_anchor_text(self, post: BlogPost, reason: str) -> str:
        """Generate descriptive anchor text for a link."""
        # Use title as base
        title = post.title

        # Simplify title for anchor text
        # Remove common prefixes
        title = re.sub(r'^(How to|Guide to|Introduction to|Understanding)\s+', '', title, flags=re.IGNORECASE)

        # Add context based on reason
        if reason == "topic_progression":
            if post.is_foundational():
                return f"introduction to {title.lower()}"
            elif post.is_advanced():
                return f"advanced {title.lower()}"

        return title.lower()

    def validate_links(self) -> Dict[str, List[Tuple]]:
        """
        Validate existing internal links.

        Returns:
        {
            "broken_links": [(post_slug, link, reason)],
            "duplicate_links": [(post_slug, link, count)],
            "poor_anchor_text": [(post_slug, link, text)]
        }
        """
        broken_links = []
        duplicate_links = []
        poor_anchor_text = []

        logger.info("Validating existing internal links...")

        for post in self.posts:
            # Check for broken links
            link_counts = Counter(post.internal_links)

            for linked_slug, count in link_counts.items():
                # Check if target exists
                if linked_slug not in self.posts_by_slug:
                    broken_links.append((post.slug, linked_slug, "Post not found"))

                # Check for duplicates
                if count > 1:
                    duplicate_links.append((post.slug, linked_slug, count))

            # Check anchor text quality
            pattern = r'\[([^\]]+)\]\(/posts/([^/)]+)/?[^)]*\)'
            matches = re.findall(pattern, post.content)

            for anchor, slug in matches:
                # Flag generic anchor text
                generic_anchors = {'here', 'click here', 'this', 'link', 'read more', 'this post'}
                if anchor.lower().strip() in generic_anchors:
                    poor_anchor_text.append((post.slug, slug, anchor))

        logger.info(f"Validation complete: {len(broken_links)} broken, "
                   f"{len(duplicate_links)} duplicates, "
                   f"{len(poor_anchor_text)} poor anchors")

        return {
            "broken_links": broken_links,
            "duplicate_links": duplicate_links,
            "poor_anchor_text": poor_anchor_text
        }

    def find_orphaned_posts(self) -> List[BlogPost]:
        """Find posts with no incoming links."""
        orphaned = []

        for post in self.posts:
            if post.slug not in self.incoming_links or not self.incoming_links[post.slug]:
                orphaned.append(post)

        return orphaned

    def suggest_links_for_all_posts(self) -> Dict[str, List[LinkSuggestion]]:
        """Generate link suggestions for all posts."""
        all_suggestions = {}

        logger.info("Generating link suggestions for all posts...")

        for post in self.posts:
            suggestions = self.suggest_links(post)
            if suggestions:
                all_suggestions[post.slug] = suggestions

        logger.info(f"Generated suggestions for {len(all_suggestions)} posts")

        return all_suggestions

    def generate_report(self, suggestions: Optional[Dict[str, List[LinkSuggestion]]] = None,
                       validation_results: Optional[Dict[str, List[Tuple]]] = None) -> None:
        """Generate comprehensive internal linking report."""
        logger.info("=" * 80)
        logger.info("INTERNAL LINKING REPORT")
        logger.info("=" * 80)

        if not self.posts:
            logger.warning("No posts parsed. Run parse_posts() first.")
            return

        # Summary statistics
        total_posts = len(self.posts)
        total_links = sum(p.link_density() for p in self.posts)
        avg_links = total_links / total_posts if total_posts > 0 else 0
        posts_below_target = sum(1 for p in self.posts if p.link_density() < 6)
        posts_above_target = sum(1 for p in self.posts if p.link_density() > 10)
        posts_in_target = total_posts - posts_below_target - posts_above_target

        logger.info(f"\n{'Summary':-^80}")
        logger.info(f"  Total posts: {total_posts}")
        logger.info(f"  Total internal links: {total_links}")
        logger.info(f"  Average links/post: {avg_links:.2f}")
        logger.info(f"  Posts below target (<6): {posts_below_target} ({posts_below_target/total_posts*100:.1f}%)")
        logger.info(f"  Posts in target (6-10): {posts_in_target} ({posts_in_target/total_posts*100:.1f}%)")
        logger.info(f"  Posts above target (>10): {posts_above_target} ({posts_above_target/total_posts*100:.1f}%)")

        # Orphaned posts
        orphaned = self.find_orphaned_posts()
        logger.info(f"\n{'Orphaned Posts (no incoming links)':-^80}")
        logger.info(f"  Count: {len(orphaned)} ({len(orphaned)/total_posts*100:.1f}%)")
        if orphaned:
            for post in orphaned[:10]:  # Show first 10
                logger.info(f"  - {post.slug}")
                logger.info(f"    Title: {post.title}")
                logger.info(f"    Outgoing links: {post.link_density()}")
            if len(orphaned) > 10:
                logger.info(f"  ... and {len(orphaned) - 10} more")

        # Validation results
        if validation_results:
            logger.info(f"\n{'Validation Results':-^80}")

            broken = validation_results.get("broken_links", [])
            if broken:
                logger.info(f"  Broken links: {len(broken)}")
                for post_slug, link, reason in broken[:5]:
                    logger.info(f"  - {post_slug} → {link} ({reason})")
                if len(broken) > 5:
                    logger.info(f"  ... and {len(broken) - 5} more")

            duplicates = validation_results.get("duplicate_links", [])
            if duplicates:
                logger.info(f"\n  Duplicate links: {len(duplicates)}")
                for post_slug, link, count in duplicates[:5]:
                    logger.info(f"  - {post_slug} → {link} ({count} times)")
                if len(duplicates) > 5:
                    logger.info(f"  ... and {len(duplicates) - 5} more")

            poor_anchors = validation_results.get("poor_anchor_text", [])
            if poor_anchors:
                logger.info(f"\n  Poor anchor text: {len(poor_anchors)}")
                for post_slug, link, text in poor_anchors[:5]:
                    logger.info(f"  - {post_slug} → {link} ('{text}')")
                if len(poor_anchors) > 5:
                    logger.info(f"  ... and {len(poor_anchors) - 5} more")

        # Link suggestions
        if suggestions:
            logger.info(f"\n{'Top Link Opportunities':-^80}")

            # Find posts with fewest links and most suggestions
            posts_needing_links = []
            for post in self.posts:
                if post.slug in suggestions:
                    posts_needing_links.append((post, len(suggestions[post.slug])))

            posts_needing_links.sort(key=lambda x: (x[0].link_density(), -x[1]))

            logger.info(f"  Showing top 5 posts needing internal links:\n")

            for post, suggestion_count in posts_needing_links[:5]:
                logger.info(f"  [{post.slug}]")
                logger.info(f"  Title: {post.title}")
                logger.info(f"  Current links: {post.link_density()}")
                logger.info(f"  Suggested links: {suggestion_count}\n")

                # Show top 3 suggestions
                for suggestion in suggestions[post.slug][:3]:
                    logger.info(str(suggestion))
                    logger.info("")

                logger.info("")

        # Distribution of links
        logger.info(f"\n{'Link Distribution':-^80}")
        link_counts = Counter(p.link_density() for p in self.posts)
        for count in sorted(link_counts.keys()):
            posts_count = link_counts[count]
            bar = "█" * (posts_count // 2)  # Scale bar
            logger.info(f"  {count:2d} links: {posts_count:3d} posts {bar}")

        logger.info(f"\n{'='*80}\n")

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate and suggest internal links for blog posts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate full report
  %(prog)s --report

  # Test on 5 pilot posts
  %(prog)s --pilot 5 --report

  # Only validate existing links
  %(prog)s --validate

  # Only generate suggestions
  %(prog)s --suggest

  # Custom posts directory
  %(prog)s --posts-dir content/posts --report
        """
    )

    parser.add_argument("--posts-dir", default="src/posts",
                       help="Posts directory (default: src/posts)")
    parser.add_argument("--suggest", action="store_true",
                       help="Generate link suggestions")
    parser.add_argument("--validate", action="store_true",
                       help="Validate existing links")
    parser.add_argument("--report", action="store_true",
                       help="Generate full report (implies --suggest and --validate)")
    parser.add_argument("--pilot", type=int, metavar="N",
                       help="Test on N pilot posts")
    parser.add_argument("--output", type=str, metavar="FILE",
                       help="Save detailed suggestions to file")

    args = parser.parse_args()

    # Setup validator
    validator = InternalLinkValidator(Path(args.posts_dir))
    validator.parse_posts()

    if not validator.posts:
        logger.error("No posts found. Exiting.")
        return 1

    # Limit to pilot posts if specified
    if args.pilot:
        logger.info(f"Limiting to {args.pilot} pilot posts")
        validator.posts = validator.posts[:args.pilot]
        validator.posts_by_slug = {p.slug: p for p in validator.posts}
        validator._build_link_graph()

    # Full report mode
    if args.report:
        args.validate = True
        args.suggest = True

    # Validate existing links
    validation_results = None
    if args.validate:
        validation_results = validator.validate_links()

    # Generate suggestions
    suggestions = None
    if args.suggest:
        suggestions = validator.suggest_links_for_all_posts()

    # Generate report
    if args.report:
        validator.generate_report(suggestions, validation_results)
    elif args.validate and validation_results:
        # Print validation summary
        logger.info(f"Validation: {len(validation_results['broken_links'])} broken links, "
                   f"{len(validation_results['duplicate_links'])} duplicates, "
                   f"{len(validation_results['poor_anchor_text'])} poor anchors")
    elif args.suggest and suggestions:
        # Print suggestions summary
        total_suggestions = sum(len(s) for s in suggestions.values())
        logger.info(f"Generated {total_suggestions} suggestions for {len(suggestions)} posts")

    # Save detailed output if requested
    if args.output and suggestions:
        output_path = Path(args.output)
        logger.info(f"Saving detailed suggestions to {output_path}")

        with output_path.open('w', encoding='utf-8') as f:
            f.write("# Internal Link Suggestions\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")

            for post_slug, post_suggestions in sorted(suggestions.items()):
                post = validator.posts_by_slug[post_slug]
                f.write(f"## {post.title}\n")
                f.write(f"File: {post_slug}\n")
                f.write(f"Current links: {post.link_density()}\n")
                f.write(f"Suggested links: {len(post_suggestions)}\n\n")

                for suggestion in post_suggestions:
                    f.write(f"### → {suggestion.to_title}\n")
                    f.write(f"- **Relevance**: {suggestion.relevance_score:.2f}\n")
                    f.write(f"- **Reason**: {suggestion.reason}\n")
                    f.write(f"- **Section**: {suggestion.suggested_section}\n")
                    f.write(f"- **Anchor text**: {suggestion.anchor_text}\n")
                    if suggestion.shared_tags:
                        f.write(f"- **Shared tags**: {', '.join(suggestion.shared_tags)}\n")
                    f.write(f"- **Link**: `/posts/{suggestion.to_post}`\n\n")

                f.write("\n")

        logger.info(f"Detailed suggestions saved to {output_path}")

    return 0

if __name__ == "__main__":
    sys.exit(main())
