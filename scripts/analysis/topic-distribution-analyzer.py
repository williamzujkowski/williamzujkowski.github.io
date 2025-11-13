#!/usr/bin/env -S uv run python3
"""
Analyze blog post topic distribution and patterns.
Generates comprehensive report on tags, categories, and content themes.
"""

import re
from pathlib import Path
from collections import Counter, defaultdict
from datetime import datetime
import json
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))
from logging_config import setup_logger

logger = setup_logger(__name__)

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown file."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def parse_tags(frontmatter):
    """Extract tags from frontmatter."""
    tags = []
    in_tags = False
    for line in frontmatter.split('\n'):
        if line.startswith('tags:'):
            in_tags = True
            continue
        if in_tags:
            if line.startswith('  -'):
                tag = line.strip('- ').strip()
                tags.append(tag)
            elif not line.startswith(' '):
                break
    return tags

def extract_metadata(filepath):
    """Extract metadata from blog post."""
    content = filepath.read_text()
    frontmatter = extract_frontmatter(content)

    # Extract title
    title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
    title = title_match.group(1) if title_match else filepath.stem

    # Extract date
    date_match = re.search(r'^date:\s*(\d{4}-\d{2}-\d{2})', frontmatter, re.MULTILINE)
    date = date_match.group(1) if date_match else filepath.stem[:10]

    # Extract tags
    tags = parse_tags(frontmatter)

    # Extract description
    desc_match = re.search(r'^description:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
    description = desc_match.group(1) if desc_match else ""

    # Word count (rough)
    body = content.split('---', 2)[-1] if '---' in content else content
    word_count = len(body.split())

    return {
        'file': filepath.name,
        'title': title,
        'date': date,
        'year': date[:4],
        'month': date[5:7],
        'tags': tags,
        'description': description,
        'word_count': word_count
    }

def analyze_posts(posts_dir):
    """Analyze all blog posts."""
    posts_path = Path(posts_dir)
    posts = []

    for filepath in sorted(posts_path.glob('*.md')):
        if filepath.name == 'welcome.md':
            continue
        try:
            metadata = extract_metadata(filepath)
            posts.append(metadata)
        except Exception as e:
            logger.error(f"Error processing {filepath.name}: {e}")

    return posts

def generate_report(posts):
    """Generate comprehensive analysis report."""
    # Tag distribution
    all_tags = []
    for post in posts:
        all_tags.extend(post['tags'])
    tag_counts = Counter(all_tags)

    # Year distribution
    year_counts = Counter(post['year'] for post in posts)

    # Posts per month (recent year)
    recent_posts = [p for p in posts if p['year'] in ['2024', '2025']]
    month_counts = Counter(f"{p['year']}-{p['month']}" for p in recent_posts)

    # Tag co-occurrence
    tag_pairs = defaultdict(int)
    for post in posts:
        tags = post['tags']
        for i, tag1 in enumerate(tags):
            for tag2 in tags[i+1:]:
                pair = tuple(sorted([tag1, tag2]))
                tag_pairs[pair] += 1

    # Posts by tag combination
    tag_combos = Counter(tuple(sorted(post['tags'])) for post in posts if post['tags'])

    # Average word count per tag
    tag_words = defaultdict(list)
    for post in posts:
        for tag in post['tags']:
            tag_words[tag].append(post['word_count'])
    tag_avg_words = {tag: sum(words)//len(words) for tag, words in tag_words.items()}

    # Convert tuple keys to strings
    top_pairs = sorted(tag_pairs.items(), key=lambda x: x[1], reverse=True)[:20]
    top_pairs_str = {f"{pair[0]} + {pair[1]}": count for (pair, count) in top_pairs}

    return {
        'total_posts': len(posts),
        'date_range': f"{min(p['date'] for p in posts)} to {max(p['date'] for p in posts)}",
        'tag_distribution': dict(tag_counts.most_common(30)),
        'year_distribution': dict(year_counts),
        'month_distribution_recent': dict(sorted(month_counts.items())),
        'top_tag_pairs': top_pairs_str,
        'posts_without_tags': len([p for p in posts if not p['tags']]),
        'avg_tags_per_post': round(sum(len(p['tags']) for p in posts) / len(posts), 2),
        'avg_word_count': sum(p['word_count'] for p in posts) // len(posts),
        'tag_avg_words': dict(sorted(tag_avg_words.items(), key=lambda x: x[1], reverse=True)[:20])
    }

def main():
    posts_dir = 'src/posts'
    posts = analyze_posts(posts_dir)
    report = generate_report(posts)

    # Output JSON to stdout for piping (intentional print for data output)
    print(json.dumps(report, indent=2))  # noqa: T201

if __name__ == '__main__':
    main()
