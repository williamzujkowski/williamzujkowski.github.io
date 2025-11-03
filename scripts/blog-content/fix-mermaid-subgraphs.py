#!/usr/bin/env -S uv run python3
"""
Fix Mermaid subgraph syntax for v10 compatibility.

Mermaid v10 changed subgraph syntax:
OLD: subgraph "Name With Spaces"
NEW: subgraph id["Name With Spaces"]

This script:
1. Finds all Mermaid blocks with quoted subgraph names
2. Converts to v10-compatible syntax
3. Backs up original files
4. Reports all changes

VERSION: 1.1.0
"""

import re
import sys
import shutil
from pathlib import Path
from typing import List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

def fix_subgraph_syntax(content: str) -> Tuple[str, List[str]]:
    """
    Fix subgraph syntax in Mermaid blocks.

    Returns:
        (fixed_content, list_of_changes)
    """
    changes = []

    def fix_mermaid_block(match):
        block_content = match.group(1)
        original_block = block_content

        # Pattern: subgraph "Name" or subgraph 'Name'
        # Replace with: subgraph id["Name"]
        def replace_subgraph(m):
            quote_char = m.group(1)
            name = m.group(2)
            # Generate ID from name (lowercase, remove spaces and special chars)
            id_name = re.sub(r'[^a-z0-9]', '', name.lower())
            if not id_name:
                id_name = f'sub{hash(name) % 1000}'

            change_msg = f'subgraph "{name}" → subgraph {id_name}["{name}"]'
            if change_msg not in changes:
                changes.append(change_msg)

            return f'    subgraph {id_name}["{name}"]'

        # Fix subgraphs with quoted names
        fixed_block = re.sub(
            r'^\s*subgraph\s+(["\'])([^"\']+)\1\s*$',
            replace_subgraph,
            block_content,
            flags=re.MULTILINE
        )

        return f'```mermaid\n{fixed_block}```'

    # Find all mermaid blocks and fix them
    fixed_content = re.sub(
        r'```mermaid\n(.*?)```',
        fix_mermaid_block,
        content,
        flags=re.DOTALL
    )

    return fixed_content, changes

def process_file(filepath: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """
    Process a single markdown file.

    Returns:
        (was_modified, list_of_changes)
    """
    try:
        content = filepath.read_text(encoding='utf-8')
        fixed_content, changes = fix_subgraph_syntax(content)

        if changes:
            if not dry_run:
                # Backup original
                backup_path = filepath.with_suffix('.md.bak')
                shutil.copy2(filepath, backup_path)

                # Write fixed content
                filepath.write_text(fixed_content, encoding='utf-8')

            return True, changes
        return False, []

    except Exception as e:
        logger.error(f"Error processing {filepath}: {e}")
        return False, []

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Fix Mermaid subgraph syntax for v10')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without modifying files')
    parser.add_argument('--verbose', action='store_true', help='Show detailed progress')
    args = parser.parse_args()

    logger.info("Fixing Mermaid subgraph syntax for v10 compatibility")

    repo_root = Path(__file__).parent.parent.parent
    posts_dir = repo_root / 'src' / 'posts'

    if not posts_dir.exists():
        logger.error(f"Posts directory not found: {posts_dir}")
        sys.exit(1)

    # Find posts with Mermaid diagrams
    posts_with_mermaid = []
    for post_file in sorted(posts_dir.glob('*.md')):
        content = post_file.read_text(encoding='utf-8')
        if '```mermaid' in content:
            posts_with_mermaid.append(post_file)

    logger.info(f"Found {len(posts_with_mermaid)} posts with Mermaid diagrams")

    if args.dry_run:
        logger.info("DRY RUN MODE - No files will be modified")

    # Process each file
    modified_count = 0
    total_changes = 0

    for post_file in posts_with_mermaid:
        was_modified, changes = process_file(post_file, dry_run=args.dry_run)

        if was_modified:
            modified_count += 1
            total_changes += len(changes)

            rel_path = post_file.relative_to(repo_root)
            logger.info(f"Modified: {rel_path}")
            logger.info("=" * 80)
            for change in changes:
                logger.info(f"  • {change}")

            if args.verbose and not args.dry_run:
                logger.debug(f"Backup created: {post_file.name}.bak")

    # Summary
    logger.info("=" * 80)
    logger.info("Summary:")
    logger.info(f"  • Total posts scanned: {len(posts_with_mermaid)}")
    logger.info(f"  • Posts modified: {modified_count}")
    logger.info(f"  • Total changes: {total_changes}")

    if args.dry_run:
        logger.info("Run without --dry-run to apply changes")
    elif modified_count > 0:
        logger.info("All Mermaid subgraphs updated to v10 syntax!")
        logger.info("Backups saved with .bak extension")
    else:
        logger.info("No changes needed - all diagrams already v10 compatible!")

    return 0 if modified_count > 0 or args.dry_run else 0

if __name__ == '__main__':
    sys.exit(main())
