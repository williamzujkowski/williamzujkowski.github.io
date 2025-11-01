#!/usr/bin/env -S uv run python3
"""
Validate GitHub gist links in blog posts.

Scans all blog posts for gist URLs and verifies each one returns HTTP 200.
Reports broken links with post filename and line number.

Usage:
    python scripts/validate-gist-links.py [--verbose] [--json]

Exit codes:
    0 - All gist links valid
    1 - Broken links found
    2 - Error (can't read files, network error, etc.)

License: MIT
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("❌ ERROR: requests library not installed")
    print("   Install with: pip install requests")
    sys.exit(2)


class GistValidator:
    """Validates GitHub gist links in blog posts."""

    def __init__(self, verbose: bool = False, timeout: int = 10):
        self.verbose = verbose
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; GistValidator/1.0)'
        })

    def find_gists_in_file(self, filepath: Path) -> List[Tuple[int, str]]:
        """
        Find all gist URLs in a file.

        Args:
            filepath: Path to markdown file

        Returns:
            List of (line_number, gist_url) tuples
        """
        # Match gist URLs with 32-character hex IDs (actual gist IDs)
        gist_pattern = re.compile(
            r'https://gist\.github\.com/williamzujkowski/([a-f0-9]{32})'
        )
        # Pattern to detect HTML comments
        comment_pattern = re.compile(r'<!--.*?-->', re.DOTALL)

        gists = []

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

                # Remove HTML comments before processing
                content_no_comments = comment_pattern.sub('', content)

                # Find gists in non-commented content
                for line_num, line in enumerate(content_no_comments.split('\n'), start=1):
                    matches = gist_pattern.findall(line)
                    for gist_id in matches:
                        full_url = f'https://gist.github.com/williamzujkowski/{gist_id}'
                        gists.append((line_num, full_url))
        except Exception as e:
            print(f"❌ ERROR: Cannot read {filepath}: {e}", file=sys.stderr)
            return []

        return gists

    def validate_gist(self, url: str) -> Tuple[bool, int, str]:
        """
        Validate a single gist URL.

        Args:
            url: Gist URL to validate

        Returns:
            Tuple of (is_valid, status_code, error_message)
        """
        try:
            response = self.session.head(url, timeout=self.timeout, allow_redirects=True)

            # Accept 200 (OK) or 301 (redirect) as valid
            if response.status_code in [200, 301]:
                return (True, response.status_code, "")
            else:
                return (False, response.status_code, f"HTTP {response.status_code}")

        except requests.exceptions.Timeout:
            return (False, 0, f"Timeout after {self.timeout}s")
        except requests.exceptions.ConnectionError as e:
            return (False, 0, f"Connection error: {str(e)}")
        except requests.exceptions.RequestException as e:
            return (False, 0, f"Request error: {str(e)}")
        except Exception as e:
            return (False, 0, f"Unknown error: {str(e)}")

    def scan_posts(self, posts_dir: Path) -> Dict[str, List[Tuple[int, str]]]:
        """
        Scan all blog posts for gist links.

        Args:
            posts_dir: Directory containing blog posts

        Returns:
            Dict mapping post filename to list of (line_number, gist_url) tuples
        """
        post_gists = {}

        if not posts_dir.exists():
            print(f"❌ ERROR: Posts directory not found: {posts_dir}", file=sys.stderr)
            sys.exit(2)

        for post_file in sorted(posts_dir.glob("*.md")):
            gists = self.find_gists_in_file(post_file)
            if gists:
                post_gists[post_file.name] = gists

        return post_gists

    def validate_all(self, posts_dir: Path, json_output: bool = False) -> Tuple[int, int, List[Dict]]:
        """
        Validate all gist links in blog posts.

        Args:
            posts_dir: Directory containing blog posts
            json_output: If True, route progress to stderr

        Returns:
            Tuple of (valid_count, broken_count, broken_links)
        """
        start_time = time.time()
        post_gists = self.scan_posts(posts_dir)

        # Route output based on format
        out = sys.stderr if json_output else sys.stdout

        if not post_gists:
            print("ℹ️  No gist links found in blog posts", file=out)
            return (0, 0, [])

        # Count total gists
        total_gists = sum(len(gists) for gists in post_gists.values())

        print(f"📎 Validating {total_gists} GitHub gist links...\n", file=out)

        valid_count = 0
        broken_count = 0
        broken_links = []

        # Group by post for better reporting
        post_results = {}

        for post_name, gists in post_gists.items():
            post_valid = 0
            post_broken = 0

            # Deduplicate gists (same URL may appear multiple times)
            unique_gists = {}
            for line_num, url in gists:
                if url not in unique_gists:
                    unique_gists[url] = []
                unique_gists[url].append(line_num)

            for url, line_nums in unique_gists.items():
                if self.verbose:
                    print(f"  Checking {url}...", end=" ", flush=True, file=out)

                is_valid, status_code, error_msg = self.validate_gist(url)

                if is_valid:
                    valid_count += 1
                    post_valid += 1
                    if self.verbose:
                        print("✅", file=out)
                else:
                    broken_count += 1
                    post_broken += 1
                    if self.verbose:
                        print(f"❌ {error_msg}", file=out)

                    for line_num in line_nums:
                        broken_links.append({
                            'post': post_name,
                            'line': line_num,
                            'url': url,
                            'error': error_msg
                        })

            post_results[post_name] = (post_valid, post_broken, len(unique_gists))

        # Print summary by post
        print(file=out)
        for post_name, (post_valid, post_broken, post_total) in sorted(post_results.items()):
            # Extract post title from filename (remove date and extension)
            title_parts = post_name.replace('.md', '').split('-')[3:]
            title = ' '.join(word.capitalize() for word in title_parts)

            if post_broken == 0:
                print(f"✅ {title} ({post_valid}/{post_total} gists valid)", file=out)
            else:
                print(f"❌ {title} ({post_valid}/{post_total} gists valid, {post_broken} broken)", file=out)

        # Print summary
        elapsed = time.time() - start_time
        print("\n" + "=" * 60, file=out)
        print("📊 SUMMARY", file=out)
        print("=" * 60, file=out)
        print(f"✅ Valid:   {valid_count}/{total_gists} gists ({valid_count*100//total_gists}%)", file=out)
        print(f"❌ Broken:  {broken_count}/{total_gists} gists ({broken_count*100//total_gists}%)", file=out)
        print(f"⏱️  Time:   {elapsed:.1f}s", file=out)

        return (valid_count, broken_count, broken_links)


def main():
    parser = argparse.ArgumentParser(
        description="Validate GitHub gist links in blog posts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/validate-gist-links.py
  python scripts/validate-gist-links.py --verbose
  python scripts/validate-gist-links.py --json > validation-report.json
        """
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show each gist as it is checked'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Timeout in seconds per gist (default: 10)'
    )

    args = parser.parse_args()

    # Determine repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    posts_dir = repo_root / "src" / "posts"

    validator = GistValidator(verbose=args.verbose, timeout=args.timeout)

    try:
        valid_count, broken_count, broken_links = validator.validate_all(posts_dir, json_output=args.json)
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        sys.exit(2)

    # Output results
    if args.json:
        result = {
            'valid': valid_count,
            'broken': broken_count,
            'total': valid_count + broken_count,
            'broken_links': broken_links
        }
        print(json.dumps(result, indent=2))

    if broken_count > 0:
        if not args.json:
            print("\n❌ BROKEN LINKS FOUND:\n", file=sys.stderr)
            for broken in broken_links:
                print(f"src/posts/{broken['post']}:{broken['line']}", file=sys.stderr)
                print(f"  {broken['url']}", file=sys.stderr)
                print(f"  {broken['error']}\n", file=sys.stderr)
        sys.exit(1)
    else:
        if not args.json:
            print(file=sys.stdout)
        sys.exit(0)


if __name__ == '__main__':
    main()
