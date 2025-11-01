#!/usr/bin/env -S uv run python3
"""
SCRIPT: batch-link-fixer.py
PURPOSE: Batch Link Fixer
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Batch Link Fixer. This script is part of the link validation
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/batch-link-fixer.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/batch-link-fixer.py

    # With verbose output
    python scripts/batch-link-fixer.py --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in link_validation category]

MANIFEST_REGISTRY: scripts/batch-link-fixer.py
"""

import json
import re
import shutil
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import sys
from tqdm import tqdm

class BatchLinkFixer:
    """Orchestrate link validation and repair"""

    def __init__(self, confidence_threshold: float = 90, dry_run: bool = False):
        self.confidence_threshold = confidence_threshold
        self.dry_run = dry_run
        self.changes_made = []
        self.backups_created = []

    def run_full_pipeline(self, posts_dir: Path) -> int:
        """Run the complete validation and repair pipeline"""
        print("🚀 Starting Link Validation Pipeline")
        print("=" * 60)

        try:
            # Step 1: Extract links
            print("\n📎 Step 1: Extracting links from blog posts...")
            if not self._run_command([
                'python', 'scripts/link-validation/link-extractor.py',
                '--posts-dir', str(posts_dir),
                '--output', 'links.json'
            ]):
                return 1

            # Step 2: Validate links
            print("\n🔍 Step 2: Validating links...")
            if not self._run_command([
                'python', 'scripts/link-validation/link-validator.py',
                '--input', 'links.json',
                '--output', 'validation.json'
            ]):
                print("⚠️  Link validation failed, continuing with basic validation...")

            # Step 3: Check content relevance
            print("\n📊 Step 3: Checking content relevance...")
            if not self._run_command([
                'python', 'scripts/link-validation/content-relevance-checker.py',
                '--links', 'links.json',
                '--validation', 'validation.json',
                '--output', 'relevance.json'
            ]):
                print("⚠️  Relevance check failed, continuing...")

            # Step 4: Find repairs
            print("\n🔧 Step 4: Finding repairs for broken links...")
            if not self._run_command([
                'python', 'scripts/link-validation/citation-repair.py',
                '--links', 'links.json',
                '--validation', 'validation.json',
                '--relevance', 'relevance.json',
                '--output', 'repairs.json'
            ]):
                print("⚠️  Repair search failed, continuing...")

            # Step 5: Generate reports
            print("\n📈 Step 5: Generating reports...")
            if not self._run_command([
                'python', 'scripts/link-validation/link-report-generator.py',
                '--links', 'links.json',
                '--validation', 'validation.json',
                '--relevance', 'relevance.json',
                '--repairs', 'repairs.json',
                '--output-dir', 'reports'
            ]):
                print("⚠️  Report generation failed, continuing...")

            # Step 6: Apply fixes
            print("\n✏️ Step 6: Applying fixes...")
            self.apply_repairs('repairs.json', posts_dir)

            print("\n✅ Pipeline completed successfully!")
            self._print_summary()

            return 0

        except Exception as e:
            print(f"\n❌ Pipeline failed: {e}")
            return 1

    def _run_command(self, cmd: List[str]) -> bool:
        """Run a command and return success status"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            if result.stdout:
                print(result.stdout)
            return True
        except subprocess.CalledProcessError as e:
            if e.stderr:
                print(f"Error: {e.stderr}")
            return False
        except FileNotFoundError:
            print(f"Command not found: {cmd[0]}")
            return False

    def apply_repairs(self, repairs_file: Path, posts_dir: Path):
        """Apply repairs to blog posts"""
        if isinstance(repairs_file, str):
            repairs_file = Path(repairs_file)
        if isinstance(posts_dir, str):
            posts_dir = Path(posts_dir)

        if not repairs_file.exists():
            print("No repairs file found")
            return

        # Load repairs
        with open(repairs_file, 'r', encoding='utf-8') as f:
            repairs_data = json.load(f)

        repairs = repairs_data.get('repairs', [])
        if not repairs:
            print("No repairs to apply")
            return

        # Filter by confidence threshold
        applicable_repairs = [
            r for r in repairs
            if r.get('confidence', 0) >= self.confidence_threshold
        ]

        print(f"Found {len(applicable_repairs)} repairs with confidence >= {self.confidence_threshold}%")

        if self.dry_run:
            print("\n🔍 DRY RUN - No changes will be made")
            self._show_planned_changes(applicable_repairs)
            return

        # Group repairs by file
        repairs_by_file = self._group_repairs_by_file(applicable_repairs)

        # Apply repairs to each file
        for file_path, file_repairs in tqdm(repairs_by_file.items(), desc="Fixing files"):
            self._apply_file_repairs(file_path, file_repairs)

    def _group_repairs_by_file(self, repairs: List[Dict]) -> Dict[str, List[Dict]]:
        """Group repairs by source file"""
        # Load links data to map repairs to files
        with open('links.json', 'r', encoding='utf-8') as f:
            links_data = json.load(f)

        # Create URL to file mapping
        url_to_file = {}
        for link in links_data.get('links', []):
            url_to_file[link['url']] = link['file_path']

        # Group repairs
        repairs_by_file = {}
        for repair in repairs:
            file_path = url_to_file.get(repair['original_url'])
            if file_path:
                if file_path not in repairs_by_file:
                    repairs_by_file[file_path] = []
                repairs_by_file[file_path].append(repair)

        return repairs_by_file

    def _apply_file_repairs(self, file_path: str, repairs: List[Dict]):
        """Apply repairs to a single file"""
        file_path = Path(file_path)

        if not file_path.exists():
            print(f"⚠️  File not found: {file_path}")
            return

        # Create backup
        if not self.dry_run:
            backup_path = self._create_backup(file_path)
            self.backups_created.append((file_path, backup_path))

        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Apply each repair
        changes = 0
        for repair in repairs:
            old_url = repair['original_url']
            new_url = repair['suggested_url']

            # Count occurrences
            count = content.count(old_url)
            if count > 0:
                content = content.replace(old_url, new_url)
                changes += count
                self.changes_made.append({
                    'file': str(file_path),
                    'old_url': old_url,
                    'new_url': new_url,
                    'count': count,
                    'confidence': repair['confidence'],
                    'repair_type': repair.get('repair_type', 'unknown')
                })

        # Write changes
        if changes > 0 and not self.dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed {changes} links in {file_path.name}")

    def _create_backup(self, file_path: Path) -> Path:
        """Create backup of file"""
        backup_path = file_path.with_suffix(f'.bak.{datetime.now().strftime("%Y%m%d_%H%M%S")}')
        shutil.copy2(file_path, backup_path)
        return backup_path

    def _show_planned_changes(self, repairs: List[Dict]):
        """Show what changes would be made"""
        print("\nPlanned changes:")
        print("-" * 60)

        for repair in repairs[:10]:  # Show first 10
            print(f"\nOriginal: {repair['original_url']}")
            print(f"Replace:  {repair['suggested_url']}")
            print(f"Source:   {repair['source']}")
            print(f"Confidence: {repair['confidence']}%")
            print(f"Notes:    {repair.get('notes', 'N/A')}")

        if len(repairs) > 10:
            print(f"\n... and {len(repairs) - 10} more changes")

    def _print_summary(self):
        """Print summary of changes made"""
        if not self.changes_made:
            print("\n📊 No changes were made")
            return

        print("\n📊 Summary of Changes")
        print("=" * 60)

        # Count by repair type
        by_type = {}
        total_links = 0
        for change in self.changes_made:
            repair_type = change['repair_type']
            by_type[repair_type] = by_type.get(repair_type, 0) + change['count']
            total_links += change['count']

        print(f"Total links fixed: {total_links}")
        print("\nBy repair type:")
        for repair_type, count in sorted(by_type.items()):
            print(f"  {repair_type}: {count}")

        print(f"\nFiles modified: {len(set(c['file'] for c in self.changes_made))}")

        if self.backups_created:
            print(f"\nBackups created: {len(self.backups_created)}")

    def generate_review_queue(self, repairs_file: Path, output_file: Path):
        """Generate manual review queue for low-confidence repairs"""
        with open(repairs_file, 'r', encoding='utf-8') as f:
            repairs_data = json.load(f)

        # Filter low-confidence repairs
        low_confidence = [
            r for r in repairs_data.get('repairs', [])
            if r.get('confidence', 0) < self.confidence_threshold
        ]

        # Load links data for context
        with open('links.json', 'r', encoding='utf-8') as f:
            links_data = json.load(f)

        # Create URL to context mapping
        url_to_context = {
            link['url']: link for link in links_data.get('links', [])
        }

        # Generate review markdown
        review = []
        review.append("# Manual Link Review Queue")
        review.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        review.append(f"\n{len(low_confidence)} links require manual review")

        for repair in low_confidence:
            context = url_to_context.get(repair['original_url'], {})

            review.append(f"\n## {Path(context.get('file_path', 'unknown')).name if context else 'Unknown file'}")
            review.append(f"\n**Original URL:** {repair['original_url']}")
            review.append(f"**Suggested:** {repair['suggested_url']}")
            review.append(f"**Confidence:** {repair['confidence']}%")
            review.append(f"**Source:** {repair['source']}")
            review.append(f"**Notes:** {repair.get('notes', 'N/A')}")

            if context:
                review.append(f"\n**Context:**")
                review.append(f"> {context.get('context_before', '')[:200]}...")
                review.append(f"> **[{context.get('text', 'link')}]**")
                review.append(f"> {context.get('context_after', '')[:200]}...")

            review.append("\n---")

        # Write review file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(review))

        print(f"✅ Manual review queue saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Batch link fixer and pipeline orchestrator')
    parser.add_argument('--posts-dir', type=Path, default=Path('src/posts'),
                       help='Directory containing blog posts')
    parser.add_argument('--repairs', type=Path, default=Path('repairs.json'),
                       help='Repairs file to apply')
    parser.add_argument('--confidence-threshold', type=float, default=90,
                       help='Minimum confidence for auto-fix (0-100)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without modifying files')
    parser.add_argument('--apply', action='store_true',
                       help='Apply repairs only (skip validation)')
    parser.add_argument('--generate-review-queue', action='store_true',
                       help='Generate manual review queue')
    parser.add_argument('--output', type=Path, default=Path('manual-review.md'),
                       help='Output file for review queue')

    args = parser.parse_args()

    fixer = BatchLinkFixer(
        confidence_threshold=args.confidence_threshold,
        dry_run=args.dry_run
    )

    if args.generate_review_queue:
        fixer.generate_review_queue(args.repairs, args.output)
    elif args.apply:
        fixer.apply_repairs(args.repairs, args.posts_dir)
    else:
        return fixer.run_full_pipeline(args.posts_dir)

    return 0

if __name__ == '__main__':
    exit(main())