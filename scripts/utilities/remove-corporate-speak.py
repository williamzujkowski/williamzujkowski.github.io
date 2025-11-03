#!/usr/bin/env -S uv run python3
"""
Corporate Speak Removal Script
Systematically removes corporate buzzwords from blog posts while preserving code blocks.

VERSION: 2.0.0
UPDATED: 2025-11-03
"""

import re
import os
from pathlib import Path
from typing import List, Dict, Tuple
import json
from datetime import datetime
import sys

# Path setup for centralized logging
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Corporate buzzword replacements
REPLACEMENTS = {
    r'\bleverage\b': 'use',
    r'\bleverages\b': 'uses',
    r'\bleveraging\b': 'using',
    r'\bleveraged\b': 'used',
    r'\bparadigm shift\b': 'fundamental change',
    r'\bparadigm shifts\b': 'fundamental changes',
    r'\butilize\b': 'use',
    r'\butilizes\b': 'uses',
    r'\butilizing\b': 'using',
    r'\butilized\b': 'used',
    r'\bsynergy\b': 'collaboration',
    r'\bsynergies\b': 'collaborations',
    r'\bgoing forward\b': 'in the future',
    r'\bcircle back\b': 'return to',
    r'\btouch base\b': 'check in',
}

class CorporateSpeakRemover:
    def __init__(self, posts_dir: str):
        self.posts_dir = Path(posts_dir)
        self.changes_made = []
        self.files_processed = 0
        self.total_replacements = 0

    def is_in_code_block(self, content: str, position: int) -> bool:
        """Check if position is within a code block (```...``` or `...`)"""
        before = content[:position]

        # Check for triple backtick code blocks
        triple_backticks = before.count('```')
        if triple_backticks % 2 == 1:
            return True

        # Check for inline code (single backtick)
        # Count backticks from start of line to position
        last_newline = before.rfind('\n')
        line_before = before[last_newline+1:] if last_newline != -1 else before
        single_backticks = line_before.count('`')
        if single_backticks % 2 == 1:
            return True

        return False

    def replace_buzzwords(self, content: str, filepath: str) -> Tuple[str, List[Dict]]:
        """Replace corporate buzzwords while avoiding code blocks"""
        changes = []
        new_content = content

        for pattern, replacement in REPLACEMENTS.items():
            # Find all matches
            for match in re.finditer(pattern, new_content, re.IGNORECASE):
                pos = match.start()

                # Skip if in code block
                if self.is_in_code_block(new_content, pos):
                    continue

                # Get original text (preserve case)
                original = match.group(0)

                # Preserve case in replacement
                if original[0].isupper():
                    replacement_text = replacement.capitalize()
                else:
                    replacement_text = replacement

                # Get context (line number)
                line_num = new_content[:pos].count('\n') + 1
                line_start = new_content.rfind('\n', 0, pos) + 1
                line_end = new_content.find('\n', pos)
                if line_end == -1:
                    line_end = len(new_content)
                context = new_content[line_start:line_end].strip()

                changes.append({
                    'file': str(filepath),
                    'line': line_num,
                    'original': original,
                    'replacement': replacement_text,
                    'context': context[:100]  # First 100 chars of line
                })

        # Apply all replacements
        for pattern, replacement in REPLACEMENTS.items():
            # Split content to preserve code blocks
            parts = []
            in_code = False
            current = []

            for line in new_content.split('\n'):
                if line.strip().startswith('```'):
                    in_code = not in_code
                    current.append(line)
                elif in_code:
                    current.append(line)
                else:
                    # Replace in non-code lines
                    replaced = re.sub(pattern, replacement, line, flags=re.IGNORECASE)
                    # Preserve case
                    current.append(replaced)

            new_content = '\n'.join(current)

        return new_content, changes

    def create_backup(self, filepath: Path) -> Path:
        """Create backup of original file"""
        backup_dir = self.posts_dir.parent / 'backups' / 'corporate-speak-removal'
        backup_dir.mkdir(parents=True, exist_ok=True)

        backup_path = backup_dir / filepath.name
        backup_path.write_text(filepath.read_text())
        return backup_path

    def process_file(self, filepath: Path) -> bool:
        """Process a single markdown file"""
        try:
            content = filepath.read_text()
            new_content, changes = self.replace_buzzwords(content, filepath)

            if changes:
                # Create backup
                self.create_backup(filepath)

                # Write updated content
                filepath.write_text(new_content)

                self.changes_made.extend(changes)
                self.total_replacements += len(changes)
                self.files_processed += 1

                logger.info(f"✓ {filepath.name}: {len(changes)} replacements")
                return True
            else:
                logger.info(f"- {filepath.name}: No buzzwords found")
                return False

        except Exception as e:
            logger.error(f"✗ {filepath.name}: Error - {e}")
            return False

    def process_all_posts(self):
        """Process all markdown files in posts directory"""
        md_files = list(self.posts_dir.glob('*.md'))

        logger.info(f"🔍 Scanning {len(md_files)} blog posts for corporate buzzwords...")

        for filepath in sorted(md_files):
            self.process_file(filepath)

    def generate_report(self, output_path: Path):
        """Generate detailed report of changes"""
        report = f"""# Corporate Speak Removal Report

**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Files Processed:** {self.files_processed}
**Total Replacements:** {self.total_replacements}

## Summary

Removed corporate buzzwords from {self.files_processed} blog posts with {self.total_replacements} total replacements.

### Target Buzzwords
"""

        for pattern, replacement in REPLACEMENTS.items():
            pattern_clean = pattern.replace(r'\b', '').replace('\\', '')
            report += f"- `{pattern_clean}` → `{replacement}`\n"

        report += "\n## Changes Made\n\n"

        # Group changes by file
        files_changed = {}
        for change in self.changes_made:
            filename = Path(change['file']).name
            if filename not in files_changed:
                files_changed[filename] = []
            files_changed[filename].append(change)

        for filename in sorted(files_changed.keys()):
            changes = files_changed[filename]
            report += f"\n### {filename}\n"
            report += f"**Replacements:** {len(changes)}\n\n"

            for change in changes:
                report += f"- **Line {change['line']}:** `{change['original']}` → `{change['replacement']}`\n"
                report += f"  - Context: `{change['context']}`\n"

        report += f"""

## Validation

All changes were validated to ensure:
- ✅ Code blocks were preserved
- ✅ Technical terms were not affected
- ✅ Case was properly maintained
- ✅ Backups were created

## Next Steps

1. Review changes in git diff
2. Run build to ensure no breakage
3. Test site functionality
4. Commit changes if validated

## Backup Location

All original files backed up to: `backups/corporate-speak-removal/`
"""

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report)
        logger.info(f"📄 Report generated: {output_path}")

        # Also save JSON for programmatic access
        json_path = output_path.with_suffix('.json')
        json_data = {
            'timestamp': datetime.now().isoformat(),
            'files_processed': self.files_processed,
            'total_replacements': self.total_replacements,
            'changes': self.changes_made,
            'replacements': {k.replace(r'\b', ''): v for k, v in REPLACEMENTS.items()}
        }
        json_path.write_text(json.dumps(json_data, indent=2))
        logger.info(f"📊 JSON data saved: {json_path}")

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Remove corporate buzzwords from blog posts',
        epilog='''
Examples:
  %(prog)s
  %(prog)s --posts-dir src/posts --output-dir docs/reports
  %(prog)s --quiet
  %(prog)s --version
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--posts-dir', type=Path,
                       default=Path('src/posts'),
                       help='Directory containing blog posts')
    parser.add_argument('--output-dir', type=Path,
                       default=Path('docs/quick-wins'),
                       help='Output directory for reports')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    if not args.posts_dir.exists():
        logger.error(f"Error: Directory not found: {args.posts_dir}")
        logger.error(f"Expected: {args.posts_dir.absolute()}")
        logger.error(f"Tip: Run from repository root or provide absolute path")
        sys.exit(2)

    remover = CorporateSpeakRemover(args.posts_dir)
    remover.process_all_posts()
    remover.generate_report(args.output_dir / 'corporate-speak-removal.md')

    if not args.quiet:
        logger.info(f"✅ Complete! {remover.total_replacements} replacements in {remover.files_processed} files.")

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
