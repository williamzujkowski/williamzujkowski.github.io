#!/usr/bin/env -S uv run python3
"""
SCRIPT: fix-mermaid-subgraphs.py
PURPOSE: Fix Mermaid subgraph syntax for v10 compatibility
CATEGORY: blog_content
LLM_READY: True
VERSION: 2.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Fixes Mermaid diagram subgraph syntax to be compatible with Mermaid v10.

    Mermaid v10 changed subgraph syntax:
    - OLD: subgraph "Name With Spaces"
    - NEW: subgraph id["Name With Spaces"]

    This script:
    1. Finds all Mermaid blocks with quoted subgraph names
    2. Converts to v10-compatible syntax with generated IDs
    3. Creates backups of original files (.bak extension)
    4. Reports all changes with detailed summary

USAGE:
    # Dry run (show changes without modifying)
    uv run python scripts/blog-content/fix-mermaid-subgraphs.py --dry-run

    # Apply fixes
    uv run python scripts/blog-content/fix-mermaid-subgraphs.py

    # Verbose output with backup confirmation
    uv run python scripts/blog-content/fix-mermaid-subgraphs.py --verbose

ARGUMENTS:
    --dry-run: Show changes without modifying files
    --verbose: Show detailed progress including backup confirmations
    --posts-dir: Custom posts directory (default: src/posts)

OUTPUT:
    - Number of posts scanned
    - Posts modified with specific changes
    - Total changes applied
    - Backup file locations

DEPENDENCIES:
    - Python 3.8+
    - logging_config for consistent logging

RELATED_SCRIPTS:
    - scripts/blog-content/validate-mermaid-syntax.py: Mermaid syntax validation

MANIFEST_REGISTRY: scripts/blog-content/fix-mermaid-subgraphs.py
"""

import re
import sys
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Optional

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)


class MermaidSubgraphFixer:
    """Fix Mermaid v10 subgraph syntax in blog posts."""

    def __init__(self, posts_dir: Path, dry_run: bool = False, verbose: bool = False):
        """
        Initialize the subgraph fixer.

        Args:
            posts_dir: Directory containing blog post markdown files
            dry_run: If True, show changes without modifying files
            verbose: If True, show detailed progress information
        """
        self.posts_dir = posts_dir
        self.dry_run = dry_run
        self.verbose = verbose
        self.stats = {
            'posts_scanned': 0,
            'posts_with_mermaid': 0,
            'posts_modified': 0,
            'total_changes': 0
        }

    def generate_subgraph_id(self, name: str) -> str:
        """
        Generate a valid Mermaid subgraph ID from a name.

        Args:
            name: Subgraph display name

        Returns:
            Valid subgraph ID (lowercase alphanumeric)
        """
        # Remove special characters and convert to lowercase
        id_name = re.sub(r'[^a-z0-9]', '', name.lower())

        # If empty after cleaning, generate from hash
        if not id_name:
            id_name = f'sub{hash(name) % 1000}'

        return id_name

    def fix_subgraph_syntax(self, content: str) -> Tuple[str, List[str]]:
        """
        Fix subgraph syntax in Mermaid blocks.

        Args:
            content: Markdown file content

        Returns:
            Tuple of (fixed_content, list_of_changes)
        """
        changes = []

        def fix_mermaid_block(match):
            """Process a single Mermaid code block."""
            block_content = match.group(1)

            def replace_subgraph(m):
                """Replace old subgraph syntax with new."""
                quote_char = m.group(1)
                name = m.group(2)

                # Generate ID from name
                id_name = self.generate_subgraph_id(name)

                # Track change
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

        # Find and fix all Mermaid blocks
        fixed_content = re.sub(
            r'```mermaid\n(.*?)```',
            fix_mermaid_block,
            content,
            flags=re.DOTALL
        )

        return fixed_content, changes

    def process_file(self, filepath: Path) -> Tuple[bool, List[str]]:
        """
        Process a single markdown file.

        Args:
            filepath: Path to markdown file

        Returns:
            Tuple of (was_modified, list_of_changes)

        Raises:
            IOError: If file cannot be read or written
            ValueError: If file content is invalid
        """
        try:
            logger.debug(f"Processing {filepath.name}")
            content = filepath.read_text(encoding='utf-8')
            fixed_content, changes = self.fix_subgraph_syntax(content)

            if changes:
                if not self.dry_run:
                    # Backup original file
                    backup_path = filepath.with_suffix('.md.bak')
                    shutil.copy2(filepath, backup_path)
                    logger.debug(f"Created backup: {backup_path}")

                    # Write fixed content
                    filepath.write_text(fixed_content, encoding='utf-8')
                    logger.info(f"Fixed {len(changes)} subgraph(s) in {filepath.name}")

                return True, changes

            return False, []

        except UnicodeDecodeError as e:
            logger.error(f"Encoding error in {filepath}: {e}")
            raise
        except IOError as e:
            logger.error(f"I/O error processing {filepath}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error processing {filepath}: {e}", exc_info=True)
            raise

    def find_posts_with_mermaid(self) -> List[Path]:
        """
        Find all markdown files containing Mermaid diagrams.

        Returns:
            List of file paths containing Mermaid code blocks
        """
        posts_with_mermaid = []

        for post_file in sorted(self.posts_dir.glob('*.md')):
            self.stats['posts_scanned'] += 1
            try:
                content = post_file.read_text(encoding='utf-8')
                if '```mermaid' in content:
                    posts_with_mermaid.append(post_file)
                    self.stats['posts_with_mermaid'] += 1
            except UnicodeDecodeError:
                logger.warning(f"Skipping {post_file.name}: encoding error")
            except IOError as e:
                logger.warning(f"Skipping {post_file.name}: {e}")

        return posts_with_mermaid

    def run(self) -> int:
        """
        Run the subgraph fixing process.

        Returns:
            Exit code (0 for success, 1 for errors)
        """
        logger.info("🔧 Fixing Mermaid subgraph syntax for v10 compatibility")

        # Validate posts directory
        if not self.posts_dir.exists():
            logger.error(f"Posts directory not found: {self.posts_dir}")
            return 1

        # Find posts with Mermaid diagrams
        posts_with_mermaid = self.find_posts_with_mermaid()
        logger.info(f"Found {len(posts_with_mermaid)} posts with Mermaid diagrams")

        if self.dry_run:
            logger.info("🔍 DRY RUN MODE - No files will be modified")

        # Process each file
        for post_file in posts_with_mermaid:
            try:
                was_modified, changes = self.process_file(post_file)

                if was_modified:
                    self.stats['posts_modified'] += 1
                    self.stats['total_changes'] += len(changes)

                    rel_path = post_file.relative_to(self.posts_dir.parent.parent)
                    logger.info(f"\n✏️  {rel_path}")
                    logger.info("=" * 80)
                    for change in changes:
                        logger.info(f"  • {change}")

                    if self.verbose and not self.dry_run:
                        logger.info(f"  ✓ Backup created: {post_file.name}.bak")

            except Exception as e:
                logger.error(f"Failed to process {post_file.name}: {e}")
                # Continue processing other files

        # Print summary
        self._print_summary()

        return 0

    def _print_summary(self) -> None:
        """Print processing summary."""
        logger.info("\n" + "=" * 80)
        logger.info("\n📊 Summary:")
        logger.info(f"  • Total posts scanned: {self.stats['posts_scanned']}")
        logger.info(f"  • Posts with Mermaid: {self.stats['posts_with_mermaid']}")
        logger.info(f"  • Posts modified: {self.stats['posts_modified']}")
        logger.info(f"  • Total changes: {self.stats['total_changes']}")

        if self.dry_run:
            logger.info("\n💡 Run without --dry-run to apply changes")
        elif self.stats['posts_modified'] > 0:
            logger.info("\n✅ All Mermaid subgraphs updated to v10 syntax!")
            logger.info("   Backups saved with .bak extension")
        else:
            logger.info("\n✅ No changes needed - all diagrams already v10 compatible!")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Fix Mermaid subgraph syntax for v10 compatibility',
        epilog='Example: %(prog)s --dry-run --verbose'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show changes without modifying files'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed progress'
    )
    parser.add_argument(
        '--posts-dir',
        type=Path,
        default=Path(__file__).parent.parent.parent / 'src' / 'posts',
        help='Posts directory (default: src/posts)'
    )

    args = parser.parse_args()

    try:
        fixer = MermaidSubgraphFixer(
            posts_dir=args.posts_dir,
            dry_run=args.dry_run,
            verbose=args.verbose
        )
        return fixer.run()

    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
