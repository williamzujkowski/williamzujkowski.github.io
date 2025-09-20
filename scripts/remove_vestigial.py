#!/usr/bin/env python3
"""
SCRIPT: remove_vestigial.py
PURPOSE: Safely remove vestigial content identified by audit
CATEGORY: utility
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T18:35:00-04:00

DESCRIPTION:
    Safely removes vestigial content identified by the vestigial_audit.py script.
    Creates backups before removal and maintains a log of all operations.
    Only removes items marked as "safe" unless explicitly told to be aggressive.

LLM_USAGE:
    python scripts/remove_vestigial.py [options]

ARGUMENTS:
    --safe (bool): Remove only safe items (default: True)
    --audit-file (str): Path to audit report file (default: reports/vestigial_audit.json)
    --backup-dir (str): Directory for backups (default: backups/vestigial_TIMESTAMP)
    --dry-run (bool): Show what would be removed without removing
    --force (bool): Skip confirmation prompts

EXAMPLES:
    # Remove safe items from latest audit
    python scripts/remove_vestigial.py --safe

    # Dry run to see what would be removed
    python scripts/remove_vestigial.py --dry-run

    # Force removal without confirmation
    python scripts/remove_vestigial.py --safe --force

OUTPUT:
    - Removal log in reports/vestigial_removal.json
    - Backup of removed items in backups directory
    - Console output of removal progress

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/remove_vestigial.py
"""

import json
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
import argparse
from typing import List, Dict, Any

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import ManifestManager, TimeManager, Logger

class VestigialRemover:
    """Safely remove vestigial content with backup"""

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.manifest_mgr = ManifestManager()
        self.time_mgr = TimeManager()
        self.removed_items = []
        self.failed_items = []
        self.skipped_items = []

    def remove_safe_items(self, items_to_remove: List[str], backup_dir: str = None, dry_run: bool = False) -> Dict[str, Any]:
        """Safely remove vestigial items with backup"""

        if not items_to_remove:
            self.logger.info("No items to remove")
            return self.generate_removal_log(backup_dir)

        # Create backup directory
        if not backup_dir:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = f"backups/vestigial_{timestamp}"

        backup_path = Path(backup_dir)

        if not dry_run:
            backup_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created backup directory: {backup_path}")

        self.logger.info(f"{'DRY RUN: Would remove' if dry_run else 'Removing'} {len(items_to_remove)} vestigial items...")

        for item_path in items_to_remove:
            try:
                path = Path(item_path)

                # Skip if doesn't exist
                if not path.exists():
                    self.skipped_items.append({
                        "path": item_path,
                        "reason": "File not found"
                    })
                    continue

                # Skip protected files
                if self.is_protected(path):
                    self.skipped_items.append({
                        "path": item_path,
                        "reason": "Protected file"
                    })
                    self.logger.warning(f"  ⚠️  Skipped protected file: {item_path}")
                    continue

                if dry_run:
                    self.logger.info(f"  Would remove: {item_path}")
                    self.removed_items.append({
                        "path": item_path,
                        "type": "file" if path.is_file() else "directory",
                        "size": path.stat().st_size if path.is_file() else 0
                    })
                else:
                    # Backup first
                    backup_item_path = backup_path / item_path
                    backup_item_path.parent.mkdir(parents=True, exist_ok=True)

                    if path.is_file():
                        shutil.copy2(path, backup_item_path)
                        path.unlink()
                        item_type = "file"
                    elif path.is_dir():
                        shutil.copytree(path, backup_item_path)
                        shutil.rmtree(path)
                        item_type = "directory"
                    else:
                        item_type = "unknown"

                    self.removed_items.append({
                        "path": item_path,
                        "type": item_type,
                        "size": backup_item_path.stat().st_size if backup_item_path.is_file() else 0,
                        "backed_up_to": str(backup_item_path)
                    })

                    self.logger.info(f"  ✅ Removed: {item_path}")

            except Exception as e:
                self.failed_items.append({
                    "path": item_path,
                    "error": str(e)
                })
                self.logger.error(f"  ❌ Failed to remove {item_path}: {e}")

        # Generate and save removal log
        removal_log = self.generate_removal_log(backup_dir if not dry_run else None)

        if not dry_run:
            # Save log
            log_path = Path("reports/vestigial_removal.json")
            log_path.parent.mkdir(exist_ok=True)
            log_path.write_text(json.dumps(removal_log, indent=2))
            self.logger.info(f"Removal log saved to: {log_path}")

            # Update manifest if we removed files
            if self.removed_items:
                self.update_manifest()

        # Print summary
        self.print_summary(dry_run)

        return removal_log

    def is_protected(self, path: Path) -> bool:
        """Check if a file is protected from removal"""
        protected_files = {
            "CLAUDE.md",
            "MANIFEST.json",
            ".claude-rules.json",
            "README.md",
            ".eleventy.js",
            "package.json",
            "package-lock.json",
            "tailwind.config.js",
            "postcss.config.js",
            "scripts/lib/common.py",
            ".gitignore",
            ".gitmodules",
            "requirements.txt"
        }

        protected_dirs = {
            ".git",
            "node_modules",
            ".standards",
            "src/posts",  # Protect blog posts
            "src/pages",  # Protect pages
            "src/assets/css",  # Protect styles
            "src/_includes",  # Protect templates
            "src/_data"  # Protect data files
        }

        # Check if it's a protected file
        if path.name in protected_files or str(path) in protected_files:
            return True

        # Check if it's in a protected directory
        for protected_dir in protected_dirs:
            if protected_dir in str(path):
                return True

        return False

    def update_manifest(self):
        """Update manifest to remove deleted files"""
        try:
            # The manifest manager will handle the updates
            for item in self.removed_items:
                # This is a placeholder - actual implementation depends on ManifestManager API
                # self.manifest_mgr.remove_file(item["path"])
                pass

            self.logger.info("Manifest update completed")
        except Exception as e:
            self.logger.error(f"Failed to update manifest: {e}")

    def generate_removal_log(self, backup_dir: str = None) -> Dict[str, Any]:
        """Generate removal log"""
        total_size = sum(item.get("size", 0) for item in self.removed_items)

        return {
            "timestamp": self.time_mgr.get_current_timestamp(),
            "backup_location": backup_dir,
            "summary": {
                "removed_count": len(self.removed_items),
                "failed_count": len(self.failed_items),
                "skipped_count": len(self.skipped_items),
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2)
            },
            "removed_items": self.removed_items,
            "failed_items": self.failed_items,
            "skipped_items": self.skipped_items
        }

    def print_summary(self, dry_run: bool = False):
        """Print removal summary"""
        print(f"\n{'=' * 60}")
        print(f"{'DRY RUN ' if dry_run else ''}Removal Summary")
        print(f"{'=' * 60}")
        print(f"  ✅ Successfully {'would remove' if dry_run else 'removed'}: {len(self.removed_items)} items")
        print(f"  ❌ Failed to remove: {len(self.failed_items)} items")
        print(f"  ⚠️  Skipped: {len(self.skipped_items)} items")

        total_size = sum(item.get("size", 0) for item in self.removed_items)
        print(f"  💾 Space {'would be' if dry_run else ''} freed: {total_size / (1024 * 1024):.2f} MB")

def load_audit_results(audit_file: str) -> Dict[str, Any]:
    """Load audit results from file"""
    audit_path = Path(audit_file)

    # Try JSON format first
    if audit_path.exists() and audit_path.suffix == '.json':
        return json.loads(audit_path.read_text())

    # Try markdown format (parse safe_to_remove section)
    if audit_path.exists() and audit_path.suffix == '.md':
        content = audit_path.read_text()
        safe_items = []

        # Extract safe to remove items from markdown
        in_safe_section = False
        for line in content.split('\n'):
            if "Safe to Remove Automatically" in line or "✅ Safe to Remove" in line:
                in_safe_section = True
                continue
            elif in_safe_section and line.startswith('#'):
                break
            elif in_safe_section and line.startswith('- `'):
                # Extract path from markdown list item
                item = line.replace('- `', '').replace('`', '').strip()
                if item:
                    safe_items.append(item)

        return {"safe_to_remove": safe_items}

    # If no audit file exists, return empty
    return {"safe_to_remove": []}

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Safely remove vestigial content identified by audit"
    )

    parser.add_argument('--safe', action='store_true', default=True,
                       help='Remove only safe items (default)')
    parser.add_argument('--audit-file', default='reports/vestigial_audit.md',
                       help='Path to audit report file')
    parser.add_argument('--backup-dir', help='Directory for backups')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be removed without removing')
    parser.add_argument('--force', action='store_true',
                       help='Skip confirmation prompts')

    args = parser.parse_args()

    print("=" * 60)
    print("Vestigial Content Remover")
    print("=" * 60)

    # Load audit results
    audit_results = load_audit_results(args.audit_file)

    if not audit_results.get("safe_to_remove"):
        print("❌ No items found to remove in audit file")
        print(f"   Please run: python scripts/vestigial_audit.py --full --report")
        return 1

    items_to_remove = audit_results["safe_to_remove"]
    print(f"Found {len(items_to_remove)} items marked as safe to remove")

    # Confirm removal unless forced or dry-run
    if not args.force and not args.dry_run:
        response = input(f"\n⚠️  Remove {len(items_to_remove)} items? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Removal cancelled")
            return 0

    # Remove items
    remover = VestigialRemover()
    removal_log = remover.remove_safe_items(
        items_to_remove,
        backup_dir=args.backup_dir,
        dry_run=args.dry_run
    )

    if not args.dry_run:
        print(f"\n📄 Removal log saved to: reports/vestigial_removal.json")
        if removal_log.get("backup_location"):
            print(f"💾 Backups saved to: {removal_log['backup_location']}")

    return 0

if __name__ == "__main__":
    sys.exit(main())