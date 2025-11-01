#!/usr/bin/env -S uv run python3
"""
SCRIPT: llm-script-documenter.py
PURPOSE: Automatically add LLM-friendly documentation headers to all Python scripts
CATEGORY: utility
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:50:00-04:00

DESCRIPTION:
    Scans all Python scripts in the repository and adds or updates LLM-friendly
    documentation headers. Categorizes scripts based on their purpose and
    updates the MANIFEST.json with complete script documentation.

LLM_USAGE:
    python scripts/llm-script-documenter.py [options]

ARGUMENTS:
    --scripts-dir (str): Directory containing scripts (default: scripts/)
    --update-manifest (bool): Update MANIFEST.json with documentation
    --force (bool): Overwrite existing headers
    --dry-run (bool): Preview changes without applying

EXAMPLES:
    # Document all scripts and update manifest
    python scripts/llm-script-documenter.py --update-manifest

    # Preview changes
    python scripts/llm-script-documenter.py --dry-run

OUTPUT:
    - Updated script files with LLM headers
    - Updated MANIFEST.json with script catalog
    - Documentation report in reports/script-documentation.json

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/llm-script-documenter.py
"""

import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Import shared utilities
sys.path.append(str(Path(__file__).parent))
from lib.common import (
    ManifestManager,
    TimeManager,
    Logger,
    ensure_directory,
    write_json
)

class LLMScriptDocumenter:
    """Automatically document scripts with LLM-friendly headers"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.manifest = ManifestManager()
        self.scripts_dir = Path("scripts")
        self.report = {
            "generated": TimeManager.get_current_timestamp(),
            "scripts_processed": 0,
            "headers_added": 0,
            "headers_updated": 0,
            "errors": []
        }

        # Script categorization patterns
        self.categories = {
            "blog_management": ["blog", "post", "content"],
            "image_management": ["image", "hero", "photo", "stock", "diagram"],
            "content_optimization": ["optimize", "enhance", "improve"],
            "academic_research": ["academic", "citation", "research", "arxiv"],
            "validation": ["validate", "check", "verify", "test", "audit"],
            "link_validation": ["link", "url", "repair"],
            "utilities": []  # Catch-all
        }

    def categorize_script(self, script_path: Path) -> str:
        """Determine script category based on name and content"""
        script_name = script_path.stem.lower()

        # Check name patterns
        for category, keywords in self.categories.items():
            if any(keyword in script_name for keyword in keywords):
                return category

        # Default to utilities
        return "utilities"

    def extract_purpose(self, content: str, script_name: str) -> str:
        """Extract or generate purpose from existing docstring or script name"""
        # Look for existing docstring
        docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
        if docstring_match:
            first_line = docstring_match.group(1).strip().split('\n')[0]
            # Clean up common patterns
            first_line = re.sub(r'^SCRIPT:\s*\w+\.py\s*', '', first_line)
            first_line = re.sub(r'^PURPOSE:\s*', '', first_line)
            if first_line and len(first_line) < 100:
                return first_line

        # Generate from script name
        purpose = script_name.replace('-', ' ').replace('_', ' ').title()
        return f"Process {purpose}"

    def generate_llm_header(self, script_path: Path, existing_content: str) -> str:
        """Generate LLM-friendly documentation header"""
        script_name = script_path.name
        category = self.categorize_script(script_path)
        purpose = self.extract_purpose(existing_content, script_path.stem)

        # Check if already has LLM header
        if "LLM_READY: True" in existing_content[:1000]:
            self.logger.info(f"Script already documented: {script_name}")
            return None

        header = f'''#!/usr/bin/env python3
"""
SCRIPT: {script_name}
PURPOSE: {purpose}
CATEGORY: {category}
LLM_READY: True
VERSION: 1.0.0
UPDATED: {TimeManager.get_current_timestamp()}

DESCRIPTION:
    {purpose}. This script is part of the {category.replace('_', ' ')}
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/{script_name} [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/{script_name}

    # With verbose output
    python scripts/{script_name} --verbose

OUTPUT:
    - Processed results based on script functionality
    - Log messages if verbose mode enabled

DEPENDENCIES:
    - Python 3.8+
    - See imports for specific package requirements
    - scripts/lib/common.py for shared utilities (if applicable)

RELATED_SCRIPTS:
    - scripts/lib/common.py: Shared utilities
    - [Other related scripts in {category} category]

MANIFEST_REGISTRY: scripts/{script_name}
"""'''

        return header

    def update_script(self, script_path: Path) -> bool:
        """Update a single script with LLM documentation"""
        try:
            with open(script_path, 'r') as f:
                content = f.read()

            # Skip if already has LLM header
            if "LLM_READY: True" in content[:1000]:
                self.logger.info(f"Already documented: {script_path.name}")
                return False

            # Generate new header
            new_header = self.generate_llm_header(script_path, content)
            if not new_header:
                return False

            # Remove old shebang and docstring if present
            content_lines = content.split('\n')
            start_idx = 0

            # Skip shebang
            if content_lines[0].startswith('#!'):
                start_idx = 1

            # Skip existing docstring
            if start_idx < len(content_lines) and content_lines[start_idx].strip().startswith('"""'):
                # Find end of docstring
                for i in range(start_idx + 1, len(content_lines)):
                    if '"""' in content_lines[i]:
                        start_idx = i + 1
                        break

            # Skip empty lines
            while start_idx < len(content_lines) and not content_lines[start_idx].strip():
                start_idx += 1

            # Combine new header with remaining content
            remaining_content = '\n'.join(content_lines[start_idx:])
            new_content = new_header + '\n\n' + remaining_content

            if not self.dry_run:
                with open(script_path, 'w') as f:
                    f.write(new_content)
                self.logger.info(f"Updated: {script_path.name}")
                self.report["headers_added"] += 1
            else:
                self.logger.info(f"Would update: {script_path.name}")

            return True

        except Exception as e:
            self.logger.error(f"Failed to update {script_path}: {e}")
            self.report["errors"].append({
                "script": str(script_path),
                "error": str(e)
            })
            return False

    def process_all_scripts(self) -> Dict:
        """Process all Python scripts in the repository"""
        scripts = list(self.scripts_dir.glob("**/*.py"))

        for script_path in scripts:
            # Skip lib directory (already documented)
            if "lib/common.py" in str(script_path):
                continue

            self.report["scripts_processed"] += 1
            self.update_script(script_path)

        return self.report

    def update_manifest(self):
        """Update MANIFEST.json with script documentation"""
        if self.dry_run:
            self.logger.info("Dry run - would update MANIFEST.json")
            return

        # Build script catalog
        script_catalog = {}

        for script_path in self.scripts_dir.glob("**/*.py"):
            if script_path.name.startswith('__'):
                continue

            with open(script_path, 'r') as f:
                content = f.read()

            # Extract LLM documentation
            if "LLM_READY: True" in content:
                script_info = self.extract_script_info(content)
                script_catalog[script_path.name] = script_info

        # Update manifest
        self.manifest.update_section("llm_interface.script_catalog", script_catalog)
        self.manifest.save()
        self.logger.info("Updated MANIFEST.json with script catalog")

    def extract_script_info(self, content: str) -> Dict:
        """Extract script information from LLM header"""
        info = {
            "llm_ready": True,
            "purpose": "",
            "category": "",
            "version": "",
            "usage": "",
            "dependencies": []
        }

        # Extract fields using regex
        patterns = {
            "purpose": r'PURPOSE:\s*(.+)',
            "category": r'CATEGORY:\s*(.+)',
            "version": r'VERSION:\s*(.+)',
            "usage": r'LLM_USAGE:\s*(.+)'
        }

        for field, pattern in patterns.items():
            match = re.search(pattern, content)
            if match:
                info[field] = match.group(1).strip()

        return info

    def save_report(self):
        """Save documentation report"""
        ensure_directory(Path("reports"))
        report_path = Path("reports/script-documentation.json")
        write_json(self.report, report_path)
        self.logger.info(f"Report saved to: {report_path}")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Automatically add LLM-friendly documentation to scripts",
        epilog='''
Examples:
  %(prog)s --update-manifest
  %(prog)s --dry-run
  %(prog)s --scripts-dir custom_scripts
  %(prog)s --version
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('--scripts-dir', default='scripts',
                       help='Directory containing scripts')
    parser.add_argument('--update-manifest', action='store_true',
                       help='Update MANIFEST.json with documentation')
    parser.add_argument('--force', action='store_true',
                       help='Overwrite existing headers')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without applying')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress progress messages')

    args = parser.parse_args()

    # Initialize documenter
    documenter = LLMScriptDocumenter(dry_run=args.dry_run)

    # Process scripts
    report = documenter.process_all_scripts()

    # Update manifest if requested
    if args.update_manifest:
        documenter.update_manifest()

    # Save report
    documenter.save_report()

    # Print summary
    print(f"\n{'='*60}")
    print("LLM Script Documentation Complete")
    print(f"{'='*60}")
    print(f"Scripts processed: {report['scripts_processed']}")
    print(f"Headers added: {report['headers_added']}")
    print(f"Headers updated: {report['headers_updated']}")

    if report['errors']:
        print(f"\n⚠️  Errors encountered: {len(report['errors'])}")
        for error in report['errors'][:5]:
            print(f"  - {error['script']}: {error['error']}")

    print(f"{'='*60}\n")

    return 0 if not report['errors'] else 1


if __name__ == "__main__":
    sys.exit(main())