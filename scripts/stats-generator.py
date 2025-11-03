#!/usr/bin/env -S uv run python3
"""
SCRIPT: stats-generator.py
PURPOSE: Blog Statistics Generator
CATEGORY: utilities
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-03

DESCRIPTION:
    Parses all markdown blog posts and generates comprehensive statistics
    for display on the blog. Outputs to src/_data/blogStats.json.

    Author: William Zujkowski
    Created: 2025-10-20
"""

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / "lib"))

from logging_config import setup_logger

# Setup logging
logger = setup_logger(__name__)


class BlogStatsGenerator:
    """Generate comprehensive statistics from blog posts."""

    # Average reading speed (words per minute)
    READING_SPEED_WPM = 238

    # Compiled regex patterns for performance
    REGEX_CODE_BLOCKS = re.compile(r'```.*?```', re.DOTALL)
    REGEX_INLINE_CODE = re.compile(r'`[^`]+`')
    REGEX_URLS = re.compile(r'https?://\S+')
    REGEX_MD_LINKS = re.compile(r'\[([^\]]+)\]\(([^\)]+)\)')
    REGEX_IMAGES = re.compile(r'!\[([^\]]*)\]\([^\)]+\)')

    def __init__(self, posts_dir: str = "src/posts", output_file: str = "src/_data/blogStats.json"):
        """
        Initialize the stats generator.

        Args:
            posts_dir: Directory containing blog post markdown files
            output_file: Path to output JSON file
        """
        self.posts_dir = Path(posts_dir)
        self.output_file = Path(output_file)
        self.posts_data: List[Dict[str, Any]] = []

        # Validate directories
        if not self.posts_dir.exists():
            raise FileNotFoundError(f"Posts directory not found: {self.posts_dir}")

        # Ensure output directory exists
        self.output_file.parent.mkdir(parents=True, exist_ok=True)

    def parse_frontmatter(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Extract YAML frontmatter from markdown content.

        Args:
            content: Raw markdown file content

        Returns:
            Parsed frontmatter dictionary or None if parsing fails
        """
        # Match frontmatter between --- delimiters
        match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not match:
            logger.warning("No frontmatter found in content")
            return None

        try:
            frontmatter = yaml.safe_load(match.group(1))
            return frontmatter
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error: {e}")
            return None

    def extract_content(self, content: str) -> str:
        """
        Extract main content (excluding frontmatter).

        Args:
            content: Raw markdown file content

        Returns:
            Content without frontmatter
        """
        # Remove frontmatter
        content = re.sub(r'^---\s*\n.*?\n---\s*\n', '', content, flags=re.DOTALL)
        return content

    def count_words(self, content: str) -> int:
        """
        Count words in content, excluding code blocks and special formatting.

        Args:
            content: Markdown content

        Returns:
            Word count
        """
        # Remove code blocks
        content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        # Remove inline code
        content = re.sub(r'`[^`]+`', '', content)
        # Remove URLs
        content = re.sub(r'https?://\S+', '', content)
        # Remove markdown links but keep text
        content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)
        # Remove images
        content = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', content)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        # Remove markdown formatting
        content = re.sub(r'[*_~#>-]', ' ', content)

        # Count words
        words = content.split()
        return len(words)

    def calculate_reading_time(self, word_count: int) -> int:
        """
        Calculate estimated reading time in minutes.

        Args:
            word_count: Number of words

        Returns:
            Reading time in minutes (rounded up)
        """
        import math
        return math.ceil(word_count / self.READING_SPEED_WPM)

    def extract_code_blocks(self, content: str) -> List[str]:
        """
        Extract all code blocks from content.

        Args:
            content: Markdown content

        Returns:
            List of code block strings
        """
        return self.REGEX_CODE_BLOCKS.findall(content)

    def calculate_code_to_content_ratio(self, content: str) -> float:
        """
        Calculate percentage of content that is code blocks.

        Args:
            content: Markdown content

        Returns:
            Percentage (0-100) of content that is code
        """
        code_blocks = self.extract_code_blocks(content)
        code_chars = sum(len(block) for block in code_blocks)
        total_chars = len(content)
        return (code_chars / total_chars * 100) if total_chars > 0 else 0

    def extract_links(self, content: str) -> Dict[str, Any]:
        """
        Extract and categorize links from content.

        Args:
            content: Markdown content

        Returns:
            Dictionary with link statistics
        """
        from urllib.parse import urlparse

        # Find all markdown links
        all_links = self.REGEX_MD_LINKS.findall(content)

        external_links = []
        internal_links = []

        for link_text, link_url in all_links:
            # Skip image links (they have ! prefix)
            if link_url.startswith('http'):
                # External link
                if 'williamzujkowski.github.io' not in link_url:
                    external_links.append(link_url)
            elif link_url.startswith('/'):
                # Internal link
                internal_links.append(link_url)

        # Calculate unique domains for external links
        external_domains = set()
        for url in external_links:
            try:
                domain = urlparse(url).netloc
                if domain:
                    external_domains.add(domain)
            except:
                pass

        return {
            'external_count': len(external_links),
            'internal_count': len(internal_links),
            'external_domains': len(external_domains),
            'external_links': external_links
        }

    def calculate_citation_density(self, external_count: int, word_count: int) -> float:
        """
        Calculate citation density (citations per 1000 words).

        Args:
            external_count: Number of external links
            word_count: Total word count

        Returns:
            Citations per 1000 words
        """
        return (external_count / (word_count / 1000)) if word_count > 0 else 0

    def parse_post(self, filepath: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a single blog post file.

        Args:
            filepath: Path to markdown file

        Returns:
            Parsed post data or None if parsing fails
        """
        try:
            content = filepath.read_text(encoding='utf-8')

            # Extract frontmatter
            frontmatter = self.parse_frontmatter(content)
            if not frontmatter:
                logger.warning(f"Skipping {filepath.name} - no valid frontmatter")
                return None

            # Extract content
            post_content = self.extract_content(content)

            # Count words
            word_count = self.count_words(post_content)

            # Calculate reading time
            reading_time = self.calculate_reading_time(word_count)

            # Parse date
            date_str = frontmatter.get('date')
            post_date = None

            if isinstance(date_str, datetime):
                post_date = date_str
            elif isinstance(date_str, date):
                # Handle datetime.date objects (YAML parsing)
                post_date = datetime.combine(date_str, datetime.min.time())
            elif isinstance(date_str, str):
                # Try various date formats
                date_formats = [
                    '%Y-%m-%d',                           # 2024-01-08
                    '%Y-%m-%dT%H:%M:%S.%fZ',             # 2024-04-07T00:00:00.000Z
                    '%Y-%m-%dT%H:%M:%SZ',                # 2024-04-07T00:00:00Z
                    '%Y-%m-%dT%H:%M:%S',                 # 2024-04-07T00:00:00
                ]

                for fmt in date_formats:
                    try:
                        post_date = datetime.strptime(date_str, fmt)
                        break
                    except ValueError:
                        continue

                if not post_date:
                    # Try extracting date from filename as fallback
                    filename_match = re.match(r'(\d{4}-\d{2}-\d{2})', filepath.name)
                    if filename_match:
                        try:
                            post_date = datetime.strptime(filename_match.group(1), '%Y-%m-%d')
                            logger.info(f"Using filename date for {filepath.name}: {filename_match.group(1)}")
                        except ValueError:
                            pass

            if not post_date:
                logger.warning(f"No valid date found in {filepath.name}, skipping")
                return None

            # Extract tags (ensure it's a list)
            tags = frontmatter.get('tags', [])
            if not isinstance(tags, list):
                tags = [tags] if tags else []

            # Extract code and link statistics
            code_ratio = self.calculate_code_to_content_ratio(post_content)
            link_stats = self.extract_links(post_content)
            citation_density = self.calculate_citation_density(link_stats['external_count'], word_count)

            # Build post data
            post_data = {
                'filename': filepath.name,
                'title': frontmatter.get('title', 'Untitled'),
                'date': post_date.strftime('%Y-%m-%d'),
                'year': post_date.year,
                'month': post_date.month,
                'month_name': post_date.strftime('%B'),
                'description': frontmatter.get('description', ''),
                'author': frontmatter.get('author', 'William Zujkowski'),
                'tags': tags,
                'word_count': word_count,
                'reading_time': reading_time,
                'has_images': bool(frontmatter.get('images')),
                'code_to_content_ratio': round(code_ratio, 1),
                'external_links': link_stats['external_count'],
                'internal_links': link_stats['internal_count'],
                'citation_density': round(citation_density, 2),
                'external_domains': link_stats['external_domains'],
            }

            return post_data

        except Exception as e:
            logger.error(f"Error parsing {filepath.name}: {e}")
            return None

    def parse_all_posts(self) -> List[Dict[str, Any]]:
        """
        Parse all blog posts in the posts directory.

        Returns:
            List of parsed post data
        """
        logger.info(f"Parsing posts from {self.posts_dir}")

        posts = []
        markdown_files = sorted(self.posts_dir.glob('*.md'))

        for filepath in markdown_files:
            post_data = self.parse_post(filepath)
            if post_data:
                posts.append(post_data)
                logger.info(f"Parsed: {filepath.name} ({post_data['word_count']} words)")

        logger.info(f"Successfully parsed {len(posts)} posts")
        return posts

    def calculate_statistics(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate comprehensive statistics from parsed posts.

        Args:
            posts: List of parsed post data

        Returns:
            Dictionary containing all statistics
        """
        if not posts:
            logger.warning("No posts to analyze")
            return {
                'total_posts': 0,
                'total_words': 0,
                'average_words': 0,
                'average_reading_time': 0,
                'posts_by_year': {},
                'words_by_year': {},
                'posts_by_month': {},
                'top_tags': [],
                'recent_posts': [],
                'longest_post': None,
                'shortest_post': None,
                'posts_with_images': 0,
                'posts_with_images_percentage': 0,
                'generated_at': datetime.now().isoformat(),
                'reading_speed_wpm': self.READING_SPEED_WPM
            }

        # Basic statistics
        total_posts = len(posts)
        total_words = sum(p['word_count'] for p in posts)
        average_words = total_words / total_posts if total_posts > 0 else 0
        average_reading_time = sum(p['reading_time'] for p in posts) / total_posts if total_posts > 0 else 0

        # Posts by year
        posts_by_year = defaultdict(int)
        words_by_year = defaultdict(int)
        for post in posts:
            posts_by_year[post['year']] += 1
            words_by_year[post['year']] += post['word_count']

        # Posts by month (for current year)
        current_year = datetime.now().year
        posts_by_month = defaultdict(int)
        for post in posts:
            if post['year'] == current_year:
                month_key = f"{post['year']}-{post['month']:02d}"
                posts_by_month[month_key] += 1

        # Tag frequency
        all_tags = []
        for post in posts:
            all_tags.extend(post['tags'])
        tag_counter = Counter(all_tags)

        # Top tags
        top_tags = [
            {'tag': tag, 'count': count}
            for tag, count in tag_counter.most_common(20)
        ]

        # Recent posts (last 10)
        sorted_posts = sorted(posts, key=lambda p: p['date'], reverse=True)
        recent_posts = [
            {
                'title': p['title'],
                'date': p['date'],
                'reading_time': p['reading_time'],
                'tags': p['tags']
            }
            for p in sorted_posts[:10]
        ]

        # Longest and shortest posts
        longest_post = max(posts, key=lambda p: p['word_count'])
        shortest_post = min(posts, key=lambda p: p['word_count'])

        # Posts with images
        posts_with_images = sum(1 for p in posts if p['has_images'])

        # Reading time distribution (histogram bins: 1-3, 4-6, 7-9, 10+ minutes)
        reading_time_bins = {
            '1-3 min': sum(1 for p in posts if 1 <= p['reading_time'] <= 3),
            '4-6 min': sum(1 for p in posts if 4 <= p['reading_time'] <= 6),
            '7-9 min': sum(1 for p in posts if 7 <= p['reading_time'] <= 9),
            '10+ min': sum(1 for p in posts if p['reading_time'] >= 10)
        }

        # Citation and link statistics
        total_external_links = sum(p['external_links'] for p in posts)
        total_internal_links = sum(p['internal_links'] for p in posts)
        average_citation_density = sum(p['citation_density'] for p in posts) / total_posts if total_posts > 0 else 0

        # Code-to-content ratio statistics
        average_code_ratio = sum(p['code_to_content_ratio'] for p in posts) / total_posts if total_posts > 0 else 0
        posts_with_code = sum(1 for p in posts if p['code_to_content_ratio'] > 0)

        # Compile statistics
        stats = {
            'total_posts': total_posts,
            'total_words': total_words,
            'average_words': round(average_words, 1),
            'average_reading_time': round(average_reading_time, 1),
            'posts_by_year': dict(sorted(posts_by_year.items())),
            'words_by_year': dict(sorted(words_by_year.items())),
            'posts_by_month': dict(sorted(posts_by_month.items())),
            'top_tags': top_tags,
            'recent_posts': recent_posts,
            'longest_post': {
                'title': longest_post['title'],
                'word_count': longest_post['word_count'],
                'reading_time': longest_post['reading_time']
            },
            'shortest_post': {
                'title': shortest_post['title'],
                'word_count': shortest_post['word_count'],
                'reading_time': shortest_post['reading_time']
            },
            'posts_with_images': posts_with_images,
            'posts_with_images_percentage': round((posts_with_images / total_posts * 100), 1),
            'reading_time_distribution': reading_time_bins,
            'citation_stats': {
                'total_external_links': total_external_links,
                'total_internal_links': total_internal_links,
                'average_citation_density': round(average_citation_density, 2),
                'average_external_links_per_post': round(total_external_links / total_posts, 1) if total_posts > 0 else 0
            },
            'code_stats': {
                'average_code_to_content_ratio': round(average_code_ratio, 1),
                'posts_with_code': posts_with_code,
                'posts_with_code_percentage': round((posts_with_code / total_posts * 100), 1) if total_posts > 0 else 0
            },
            'generated_at': datetime.now().isoformat(),
            'reading_speed_wpm': self.READING_SPEED_WPM
        }

        return stats

    def generate(self) -> Dict[str, Any]:
        """
        Generate complete blog statistics.

        Returns:
            Complete statistics dictionary
        """
        logger.info("Starting blog statistics generation")

        # Parse all posts
        self.posts_data = self.parse_all_posts()

        # Calculate statistics
        stats = self.calculate_statistics(self.posts_data)

        # Save to file
        try:
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(stats, f, indent=2, ensure_ascii=False)
            logger.info(f"Statistics saved to {self.output_file}")
        except Exception as e:
            logger.error(f"Error saving statistics: {e}")
            raise

        # Print summary
        self._print_summary(stats)

        return stats

    def _print_summary(self, stats: Dict[str, Any]) -> None:
        """
        Log a summary of generated statistics.

        Args:
            stats: Statistics dictionary
        """
        logger.info("\n" + "="*60)
        logger.info("BLOG STATISTICS SUMMARY")
        logger.info("="*60)
        logger.info(f"Total Posts: {stats['total_posts']}")
        logger.info(f"Total Words: {stats['total_words']:,}")
        logger.info(f"Average Words per Post: {stats['average_words']:,.1f}")
        logger.info(f"Average Reading Time: {stats['average_reading_time']:.1f} minutes")
        logger.info(f"Posts with Images: {stats['posts_with_images']} ({stats['posts_with_images_percentage']}%)")

        if stats['posts_by_year']:
            logger.info("\nPosts by Year:")
            for year, count in stats['posts_by_year'].items():
                words = stats['words_by_year'][year]
                logger.info(f"  {year}: {count} posts ({words:,} words)")

        if stats['top_tags']:
            logger.info("\nTop 10 Tags:")
            for i, tag_data in enumerate(stats['top_tags'][:10], 1):
                logger.info(f"  {i}. {tag_data['tag']}: {tag_data['count']} posts")

        if stats.get('longest_post'):
            logger.info("\nLongest Post:")
            logger.info(f"  {stats['longest_post']['title']}")
            logger.info(f"  {stats['longest_post']['word_count']:,} words ({stats['longest_post']['reading_time']} min read)")

        if stats.get('shortest_post'):
            logger.info("\nShortest Post:")
            logger.info(f"  {stats['shortest_post']['title']}")
            logger.info(f"  {stats['shortest_post']['word_count']:,} words ({stats['shortest_post']['reading_time']} min read)")

        logger.info("="*60 + "\n")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Generate comprehensive statistics from blog posts',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate statistics
  python scripts/stats-generator.py

  # Quiet mode
  python scripts/stats-generator.py --quiet

  # Specify custom posts directory
  python scripts/stats-generator.py --posts-dir src/posts
        """
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--posts-dir', default='src/posts',
                       help='Directory containing blog posts')
    parser.add_argument('--output', default='src/_data/blogStats.json',
                       help='Output JSON file path')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress output messages')

    args = parser.parse_args()

    try:
        # Initialize generator
        generator = BlogStatsGenerator(
            posts_dir=args.posts_dir,
            output_file=args.output
        )

        # Generate statistics
        stats = generator.generate()

        logger.info("Statistics generation completed successfully")
        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 2


if __name__ == "__main__":
    import argparse
    sys.exit(main())
