#!/usr/bin/env -S uv run python3
"""
Update blog posts with real GitHub gist URLs.

Reads gist-mapping.json and replaces placeholder gist URLs in blog posts
with actual URLs from created gists.

Usage:
    python scripts/update-blog-gist-urls.py [--dry-run]

Prerequisites:
    - gists/gist-mapping.json exists (created by create-gists-from-folder.py)
    - Blog posts in src/posts/ with placeholder URLs

License: MIT
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# Blog posts to update
BLOG_POSTS = [
    "src/posts/2025-10-06-automated-security-scanning-pipeline.md",
    "src/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard.md",
    "src/posts/2025-09-08-zero-trust-vlan-segmentation-homelab.md",
    "src/posts/2025-09-29-proxmox-high-availability-homelab.md",
]

# Gist mapping file location
MAPPING_FILE = "gists/gist-mapping.json"


def load_gist_mapping(mapping_file: Path) -> Dict[str, Dict[str, str]]:
    """
    Load gist mapping from JSON file.

    Args:
        mapping_file: Path to gist-mapping.json

    Returns:
        Dictionary mapping file paths to gist info (url, slug)

    Raises:
        FileNotFoundError: If mapping file doesn't exist
        json.JSONDecodeError: If mapping file is invalid JSON
    """
    if not mapping_file.exists():
        raise FileNotFoundError(
            f"Gist mapping file not found: {mapping_file}\n"
            f"Run create-gists-from-folder.py first to create gists."
        )

    with open(mapping_file, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_slug_from_url(url: str) -> str:
    """
    Extract gist slug from placeholder URL.

    Args:
        url: Placeholder gist URL

    Returns:
        Gist slug (e.g., 'vlan-dhcp-config')

    Example:
        >>> extract_slug_from_url('https://gist.github.com/williamzujkowski/vlan-dhcp-config')
        'vlan-dhcp-config'
    """
    # Match: https://gist.github.com/williamzujkowski/{slug}
    match = re.search(r"github\.com/williamzujkowski/([a-z0-9-]+)", url)
    if match:
        return match.group(1)
    return ""


def find_real_url_by_slug(
    slug: str, mapping: Dict[str, Dict[str, str]]
) -> Tuple[str, str]:
    """
    Find real gist URL by matching slug.

    Args:
        slug: Gist slug from placeholder URL
        mapping: Gist mapping dictionary

    Returns:
        Tuple of (real_url, file_path) or ("", "") if not found
    """
    for file_path, gist_info in mapping.items():
        if gist_info.get("slug") == slug:
            return gist_info.get("url", ""), file_path

    return "", ""


def update_blog_post(
    post_path: Path,
    mapping: Dict[str, Dict[str, str]],
    dry_run: bool = False,
) -> Tuple[int, List[str]]:
    """
    Update placeholder gist URLs in a blog post.

    Args:
        post_path: Path to blog post markdown file
        mapping: Gist mapping dictionary
        dry_run: If True, don't write changes to file

    Returns:
        Tuple of (replacement_count, list of replacement messages)
    """
    if not post_path.exists():
        return 0, [f"⚠️  Post not found: {post_path}"]

    # Read post content
    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all placeholder gist URLs
    placeholder_pattern = r"https://gist\.github\.com/williamzujkowski/([a-z0-9-]+)"
    placeholders = re.findall(placeholder_pattern, content)

    if not placeholders:
        return 0, [f"ℹ️  No placeholder URLs found in {post_path.name}"]

    # Track replacements
    replacement_count = 0
    messages = []
    updated_content = content

    for slug in placeholders:
        placeholder_url = f"https://gist.github.com/williamzujkowski/{slug}"
        real_url, file_path = find_real_url_by_slug(slug, mapping)

        if real_url:
            # Replace placeholder with real URL
            updated_content = updated_content.replace(placeholder_url, real_url)
            replacement_count += 1
            messages.append(
                f"  ✓ Replaced {slug}\n"
                f"    Old: {placeholder_url}\n"
                f"    New: {real_url}\n"
                f"    Source: {file_path}"
            )
        else:
            messages.append(f"  ✗ No mapping found for slug: {slug}")

    # Write updated content (unless dry-run)
    if not dry_run and replacement_count > 0:
        with open(post_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

    return replacement_count, messages


def validate_all_placeholders_replaced(
    post_path: Path,
) -> Tuple[bool, List[str]]:
    """
    Validate that all placeholder URLs have been replaced.

    Args:
        post_path: Path to blog post markdown file

    Returns:
        Tuple of (all_replaced: bool, list of remaining placeholders)
    """
    if not post_path.exists():
        return True, []

    with open(post_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Find any remaining placeholder URLs
    placeholder_pattern = r"https://gist\.github\.com/williamzujkowski/([a-z0-9-]+)"
    remaining = re.findall(placeholder_pattern, content)

    # Filter out placeholders that might be legitimate (contain hex hash)
    # Real gist URLs have format: https://gist.github.com/username/{32-char-hex}
    remaining = [
        slug for slug in remaining if len(slug) < 32 and not all(c in "0123456789abcdef" for c in slug)
    ]

    return len(remaining) == 0, remaining


def main():
    """Main execution function."""
    # Parse arguments
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("🔍 DRY RUN MODE - No changes will be written\n")

    # Get repository root
    repo_root = Path(__file__).parent.parent

    # Load gist mapping
    mapping_file = repo_root / MAPPING_FILE
    print(f"📖 Loading gist mapping from: {mapping_file}")

    try:
        mapping = load_gist_mapping(mapping_file)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in {mapping_file}: {e}")
        sys.exit(1)

    print(f"✓ Loaded {len(mapping)} gist mappings\n")

    # Process each blog post
    total_replacements = 0
    all_valid = True

    for post_file in BLOG_POSTS:
        post_path = repo_root / post_file
        print(f"📝 Processing: {post_path.name}")
        print("-" * 60)

        # Update placeholders
        count, messages = update_blog_post(post_path, mapping, dry_run)

        if count > 0:
            print(f"\n✓ Made {count} replacement(s):\n")
            for msg in messages:
                print(msg)
        else:
            for msg in messages:
                print(msg)

        total_replacements += count

        # Validate all placeholders replaced (only if not dry-run)
        if not dry_run and count > 0:
            is_valid, remaining = validate_all_placeholders_replaced(post_path)
            if not is_valid:
                all_valid = False
                print(f"\n⚠️  WARNING: {len(remaining)} placeholder(s) still remain:")
                for slug in remaining:
                    print(f"    - {slug}")
            else:
                print("\n✓ All placeholders successfully replaced")

        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total replacements: {total_replacements}")
    print(f"Posts processed: {len(BLOG_POSTS)}")

    if dry_run:
        print("\n🔍 DRY RUN - No files were modified")
        print("Run without --dry-run to apply changes")
    elif total_replacements > 0:
        if all_valid:
            print("\n✓ All placeholder URLs successfully replaced!")
        else:
            print("\n⚠️  Some placeholders could not be replaced")
            print("Check the warnings above for details")
            sys.exit(1)
    else:
        print("\nℹ️  No placeholders found in any posts")


if __name__ == "__main__":
    main()
