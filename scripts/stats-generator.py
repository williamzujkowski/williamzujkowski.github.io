#!/usr/bin/env python3
"""
Blog Statistics Generator

Parses all markdown blog posts and generates comprehensive statistics
for display on the blog. Outputs to src/_data/blogStats.json.

Author: William Zujkowski
Created: 2025-10-20
"""

import json
import logging
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, date
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BlogStatsGenerator:
    """Generate comprehensive statistics from blog posts."""

    # Average reading speed (words per minute)
    READING_SPEED_WPM = 238

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
        Print a summary of generated statistics.

        Args:
            stats: Statistics dictionary
        """
        print("\n" + "="*60)
        print("BLOG STATISTICS SUMMARY")
        print("="*60)
        print(f"Total Posts: {stats['total_posts']}")
        print(f"Total Words: {stats['total_words']:,}")
        print(f"Average Words per Post: {stats['average_words']:,.1f}")
        print(f"Average Reading Time: {stats['average_reading_time']:.1f} minutes")
        print(f"Posts with Images: {stats['posts_with_images']} ({stats['posts_with_images_percentage']}%)")

        if stats['posts_by_year']:
            print("\nPosts by Year:")
            for year, count in stats['posts_by_year'].items():
                words = stats['words_by_year'][year]
                print(f"  {year}: {count} posts ({words:,} words)")

        if stats['top_tags']:
            print("\nTop 10 Tags:")
            for i, tag_data in enumerate(stats['top_tags'][:10], 1):
                print(f"  {i}. {tag_data['tag']}: {tag_data['count']} posts")

        if stats.get('longest_post'):
            print("\nLongest Post:")
            print(f"  {stats['longest_post']['title']}")
            print(f"  {stats['longest_post']['word_count']:,} words ({stats['longest_post']['reading_time']} min read)")

        if stats.get('shortest_post'):
            print("\nShortest Post:")
            print(f"  {stats['shortest_post']['title']}")
            print(f"  {stats['shortest_post']['word_count']:,} words ({stats['shortest_post']['reading_time']} min read)")

        print("="*60 + "\n")


def main():
    """Main execution function."""
    try:
        # Initialize generator
        generator = BlogStatsGenerator()

        # Generate statistics
        stats = generator.generate()

        logger.info("Statistics generation completed successfully")
        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
