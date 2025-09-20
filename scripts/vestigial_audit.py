#!/usr/bin/env python3
"""
SCRIPT: vestigial_audit.py
PURPOSE: Comprehensive audit to identify all vestigial content
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T14:59:30-04:00

DESCRIPTION:
    This script performs a comprehensive audit of the repository to identify
    vestigial (unnecessary, obsolete, or redundant) content. It checks for
    duplicate functionality, unreferenced files, old backups, and other
    content that can be safely removed to improve repository cleanliness.

LLM_USAGE:
    python scripts/vestigial_audit.py [--full] [--check-only] [--report]

ARGUMENTS:
    --full (bool): Perform comprehensive deep audit
    --check-only (bool): Only check, don't suggest removals
    --report (bool): Generate detailed report
    --verbose (bool): Enable detailed output

EXAMPLES:
    # Basic audit
    python scripts/vestigial_audit.py

    # Full comprehensive audit with report
    python scripts/vestigial_audit.py --full --report

    # Check only mode for CI/CD
    python scripts/vestigial_audit.py --check-only

OUTPUT:
    Prints findings to console
    Optionally generates reports/vestigial_audit_report.md

DEPENDENCIES:
    - Python 3.8+
    - Required packages: None (uses standard library)
    - Other scripts: None

RELATED_SCRIPTS:
    - remove_vestigial.py: Safely removes identified vestigial content
    - validate_manifest.py: Validates manifest after cleanup

MANIFEST_REGISTRY: scripts/vestigial_audit.py
"""

import json
import os
import re
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Tuple
from collections import defaultdict
import hashlib
import sys

# Constants
SCRIPT_PURPOSE = "Comprehensive audit to identify all vestigial content"
SCRIPT_VERSION = "1.0.0"

# Audit patterns
AUDIT_PATTERNS = {
    "obsolete_files": [
        r".*_old\.",
        r".*_backup\.",
        r".*\.bak$",
        r".*\.bak\.\d+$",
        r"test_.*",
        r"temp_.*",
        r".*_copy\.",
        r".*_orig\.",
        r".*~$",
        r".*\.tmp$",
        r".*\.swp$"
    ],
    "duplicate_scripts": {
        "similarity_threshold": 0.7,
        "check_functionality": True,
        "check_imports": True
    },
    "unreferenced_files": {
        "check_imports": True,
        "check_links": True,
        "check_manifest": True
    },
    "empty_directories": {
        "ignore_dirs": [".git", "node_modules", "__pycache__", ".cache"]
    },
    "deprecated_features": {
        "old_image_system": ["hero/", "thumbnails/"],
        "old_scripts": ["validate-*.py", "fix-*.py", "test-*.py"],
        "old_docs": ["TODO.md", "DEPRECATED_*"],
        "old_configs": ["*.old", "*.deprecated"]
    },
    "large_files": {
        "size_threshold_mb": 10,
        "check_binaries": True,
        "check_images": True
    }
}

# Protected files that should never be removed
PROTECTED_FILES = [
    "CLAUDE.md",
    "MANIFEST.json",
    "MANIFEST.yaml",  # Until we verify migration
    ".claude-rules.json",
    "README.md",
    ".eleventy.js",
    "package.json",
    "package-lock.json",
    "tailwind.config.js",
    "postcss.config.js",
    ".gitignore"
]

class VestigialAuditor:
    """Performs comprehensive vestigial content audit"""

    def __init__(self, root_dir: Path = Path.cwd()):
        self.root_dir = root_dir
        self.findings = {
            "obsolete_files": [],
            "duplicate_functionality": [],
            "unreferenced_files": [],
            "deprecated_features": [],
            "old_backups": [],
            "test_artifacts": [],
            "empty_directories": [],
            "large_unused_files": [],
            "redundant_dependencies": []
        }
        self.stats = {
            "total_files_scanned": 0,
            "vestigial_files_found": 0,
            "potential_space_saved": 0,
            "duplicate_functions": 0
        }
        self.file_references = defaultdict(set)

    def run_audit(self, full: bool = False) -> Dict:
        """Run the complete audit"""
        print("🔍 Starting Vestigial Content Audit...")
        print("=" * 60)

        # Phase 1: Find obsolete files
        self._find_obsolete_files()

        # Phase 2: Find old backups
        self._find_old_backups()

        # Phase 3: Find test artifacts
        self._find_test_artifacts()

        # Phase 4: Find empty directories
        self._find_empty_directories()

        if full:
            # Phase 5: Find duplicate functionality
            self._find_duplicate_functionality()

            # Phase 6: Find unreferenced files
            self._find_unreferenced_files()

            # Phase 7: Find large unused files
            self._find_large_unused_files()

        # Calculate statistics
        self._calculate_statistics()

        return self.findings

    def _find_obsolete_files(self):
        """Find files matching obsolete patterns"""
        print("\n📁 Checking for obsolete files...")

        for root, dirs, files in os.walk(self.root_dir):
            # Skip protected directories
            if any(skip in root for skip in ['.git', 'node_modules', '__pycache__']):
                continue

            path = Path(root)
            for file in files:
                filepath = path / file

                # Check against obsolete patterns
                for pattern in AUDIT_PATTERNS["obsolete_files"]:
                    if re.match(pattern, file):
                        if str(filepath.relative_to(self.root_dir)) not in PROTECTED_FILES:
                            self.findings["obsolete_files"].append({
                                "path": str(filepath.relative_to(self.root_dir)),
                                "pattern": pattern,
                                "size": filepath.stat().st_size,
                                "modified": datetime.fromtimestamp(filepath.stat().st_mtime)
                            })
                            break

        print(f"  Found {len(self.findings['obsolete_files'])} obsolete files")

    def _find_old_backups(self):
        """Find backup files older than 30 days"""
        print("\n💾 Checking for old backup files...")

        cutoff_date = datetime.now() - timedelta(days=30)

        for root, dirs, files in os.walk(self.root_dir):
            if any(skip in root for skip in ['.git', 'node_modules']):
                continue

            path = Path(root)
            for file in files:
                if any(ext in file for ext in ['.bak', 'backup', '.old']):
                    filepath = path / file
                    try:
                        mod_time = datetime.fromtimestamp(filepath.stat().st_mtime)
                        if mod_time < cutoff_date:
                            self.findings["old_backups"].append({
                                "path": str(filepath.relative_to(self.root_dir)),
                                "age_days": (datetime.now() - mod_time).days,
                                "size": filepath.stat().st_size,
                                "modified": mod_time
                            })
                    except:
                        pass

        print(f"  Found {len(self.findings['old_backups'])} old backup files")

    def _find_test_artifacts(self):
        """Find test artifacts and temporary files"""
        print("\n🧪 Checking for test artifacts...")

        test_patterns = [
            r"test_.*\.py$",
            r".*_test\.py$",
            r".*\.test\.",
            r"temp_.*",
            r"debug_.*",
            r".*\.log$",
            r".*\.cache$"
        ]

        for root, dirs, files in os.walk(self.root_dir):
            if any(skip in root for skip in ['.git', 'node_modules']):
                continue

            path = Path(root)
            for file in files:
                for pattern in test_patterns:
                    if re.match(pattern, file):
                        filepath = path / file
                        self.findings["test_artifacts"].append({
                            "path": str(filepath.relative_to(self.root_dir)),
                            "type": "test" if "test" in file else "temp",
                            "size": filepath.stat().st_size
                        })
                        break

        print(f"  Found {len(self.findings['test_artifacts'])} test artifacts")

    def _find_empty_directories(self):
        """Find empty directories"""
        print("\n📂 Checking for empty directories...")

        for root, dirs, files in os.walk(self.root_dir, topdown=False):
            if any(skip in root for skip in AUDIT_PATTERNS["empty_directories"]["ignore_dirs"]):
                continue

            path = Path(root)
            if path != self.root_dir and not any(path.iterdir()):
                self.findings["empty_directories"].append(
                    str(path.relative_to(self.root_dir))
                )

        print(f"  Found {len(self.findings['empty_directories'])} empty directories")

    def _find_duplicate_functionality(self):
        """Find scripts with duplicate functionality"""
        print("\n🔄 Checking for duplicate functionality...")

        scripts_dir = self.root_dir / "scripts"
        if not scripts_dir.exists():
            return

        script_signatures = {}

        for script in scripts_dir.glob("*.py"):
            try:
                with open(script, 'r') as f:
                    content = f.read()

                # Create signature based on imports and function definitions
                imports = re.findall(r'^import .*$|^from .* import .*$', content, re.MULTILINE)
                functions = re.findall(r'^def (\w+)\(', content, re.MULTILINE)
                classes = re.findall(r'^class (\w+)', content, re.MULTILINE)

                signature = {
                    "imports": sorted(imports),
                    "functions": sorted(functions),
                    "classes": sorted(classes),
                    "size": len(content),
                    "lines": content.count('\n')
                }

                script_signatures[script.name] = signature

            except:
                pass

        # Find similar scripts
        scripts = list(script_signatures.keys())
        for i, script1 in enumerate(scripts):
            for script2 in scripts[i+1:]:
                similarity = self._calculate_similarity(
                    script_signatures[script1],
                    script_signatures[script2]
                )
                if similarity > AUDIT_PATTERNS["duplicate_scripts"]["similarity_threshold"]:
                    self.findings["duplicate_functionality"].append({
                        "script1": script1,
                        "script2": script2,
                        "similarity": f"{similarity:.2%}"
                    })

        print(f"  Found {len(self.findings['duplicate_functionality'])} duplicate scripts")

    def _calculate_similarity(self, sig1: Dict, sig2: Dict) -> float:
        """Calculate similarity between two script signatures"""
        # Simple similarity based on common elements
        common_imports = set(sig1["imports"]) & set(sig2["imports"])
        common_functions = set(sig1["functions"]) & set(sig2["functions"])
        common_classes = set(sig1["classes"]) & set(sig2["classes"])

        total1 = len(sig1["imports"]) + len(sig1["functions"]) + len(sig1["classes"])
        total2 = len(sig2["imports"]) + len(sig2["functions"]) + len(sig2["classes"])
        common = len(common_imports) + len(common_functions) + len(common_classes)

        if total1 + total2 == 0:
            return 0

        return (2 * common) / (total1 + total2)

    def _find_unreferenced_files(self):
        """Find files that are not referenced anywhere"""
        print("\n🔗 Checking for unreferenced files...")

        # Build reference map
        self._build_reference_map()

        # Check each file
        for root, dirs, files in os.walk(self.root_dir):
            if any(skip in root for skip in ['.git', 'node_modules', '__pycache__']):
                continue

            path = Path(root)
            for file in files:
                filepath = path / file
                rel_path = str(filepath.relative_to(self.root_dir))

                # Skip protected files
                if rel_path in PROTECTED_FILES:
                    continue

                # Check if file is referenced
                if rel_path not in self.file_references and \
                   file not in self.file_references and \
                   filepath.name not in self.file_references:
                    self.findings["unreferenced_files"].append({
                        "path": rel_path,
                        "size": filepath.stat().st_size,
                        "type": filepath.suffix
                    })

        print(f"  Found {len(self.findings['unreferenced_files'])} unreferenced files")

    def _build_reference_map(self):
        """Build map of file references throughout the codebase"""
        # Scan all text files for references
        for root, dirs, files in os.walk(self.root_dir):
            if any(skip in root for skip in ['.git', 'node_modules']):
                continue

            path = Path(root)
            for file in files:
                if file.endswith(('.py', '.js', '.md', '.html', '.json', '.yaml')):
                    filepath = path / file
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Find file references
                        # Look for imports, requires, links, etc.
                        references = re.findall(r'["\']([^"\']+\.[a-zA-Z]+)["\']', content)
                        for ref in references:
                            self.file_references[ref].add(str(filepath.relative_to(self.root_dir)))

                    except:
                        pass

    def _find_large_unused_files(self):
        """Find large files that may be unused"""
        print("\n📦 Checking for large unused files...")

        threshold_bytes = AUDIT_PATTERNS["large_files"]["size_threshold_mb"] * 1024 * 1024

        for root, dirs, files in os.walk(self.root_dir):
            if any(skip in root for skip in ['.git', 'node_modules']):
                continue

            path = Path(root)
            for file in files:
                filepath = path / file
                try:
                    size = filepath.stat().st_size
                    if size > threshold_bytes:
                        rel_path = str(filepath.relative_to(self.root_dir))
                        # Check if it's referenced
                        if rel_path not in self.file_references:
                            self.findings["large_unused_files"].append({
                                "path": rel_path,
                                "size_mb": round(size / (1024 * 1024), 2),
                                "type": filepath.suffix
                            })
                except:
                    pass

        print(f"  Found {len(self.findings['large_unused_files'])} large unused files")

    def _calculate_statistics(self):
        """Calculate audit statistics"""
        total_vestigial = 0
        total_size = 0

        for category, items in self.findings.items():
            if isinstance(items, list):
                total_vestigial += len(items)
                for item in items:
                    if isinstance(item, dict) and 'size' in item:
                        total_size += item['size']

        self.stats["vestigial_files_found"] = total_vestigial
        self.stats["potential_space_saved"] = total_size

    def generate_report(self, output_path: Path = None) -> str:
        """Generate detailed audit report"""
        if output_path is None:
            output_path = Path("reports/vestigial_audit_report.md")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        report = []
        report.append("# Vestigial Content Audit Report")
        report.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"**Version:** {SCRIPT_VERSION}")

        # Summary
        report.append("\n## Summary")
        report.append(f"- **Vestigial files found:** {self.stats['vestigial_files_found']}")
        report.append(f"- **Potential space saved:** {self.stats['potential_space_saved'] / (1024*1024):.2f} MB")

        # Detailed findings
        report.append("\n## Detailed Findings")

        # Obsolete files
        if self.findings["obsolete_files"]:
            report.append(f"\n### Obsolete Files ({len(self.findings['obsolete_files'])})")
            for item in self.findings["obsolete_files"][:20]:  # Limit output
                report.append(f"- `{item['path']}` ({item['size']} bytes)")

        # Old backups
        if self.findings["old_backups"]:
            report.append(f"\n### Old Backup Files ({len(self.findings['old_backups'])})")
            for item in self.findings["old_backups"][:20]:
                report.append(f"- `{item['path']}` ({item['age_days']} days old, {item['size']} bytes)")

        # Test artifacts
        if self.findings["test_artifacts"]:
            report.append(f"\n### Test Artifacts ({len(self.findings['test_artifacts'])})")
            for item in self.findings["test_artifacts"][:20]:
                report.append(f"- `{item['path']}` (type: {item['type']})")

        # Empty directories
        if self.findings["empty_directories"]:
            report.append(f"\n### Empty Directories ({len(self.findings['empty_directories'])})")
            for dir_path in self.findings["empty_directories"][:20]:
                report.append(f"- `{dir_path}/`")

        # Duplicate functionality
        if self.findings["duplicate_functionality"]:
            report.append(f"\n### Duplicate Functionality ({len(self.findings['duplicate_functionality'])})")
            for item in self.findings["duplicate_functionality"]:
                report.append(f"- `{item['script1']}` ↔ `{item['script2']}` (similarity: {item['similarity']})")

        # Unreferenced files
        if self.findings["unreferenced_files"]:
            report.append(f"\n### Unreferenced Files ({len(self.findings['unreferenced_files'])})")
            for item in self.findings["unreferenced_files"][:20]:
                report.append(f"- `{item['path']}` ({item['type']}, {item['size']} bytes)")

        # Large unused files
        if self.findings["large_unused_files"]:
            report.append(f"\n### Large Unused Files ({len(self.findings['large_unused_files'])})")
            for item in self.findings["large_unused_files"]:
                report.append(f"- `{item['path']}` ({item['size_mb']} MB)")

        # Recommendations
        report.append("\n## Recommendations")
        report.append("\n### Safe to Remove")
        report.append("- All `.bak` files older than 30 days")
        report.append("- Empty directories")
        report.append("- Test artifacts in non-test directories")

        report.append("\n### Requires Review")
        report.append("- Duplicate functionality scripts")
        report.append("- Large unused files")
        report.append("- Unreferenced documentation")

        report.append("\n### Actions")
        report.append("1. Backup the repository before cleanup")
        report.append("2. Run `python scripts/remove_vestigial.py --safe` to remove safe items")
        report.append("3. Manually review duplicate functionality")
        report.append("4. Update MANIFEST.json after cleanup")

        # Write report
        report_text = "\n".join(report)
        with open(output_path, 'w') as f:
            f.write(report_text)

        print(f"\n📄 Report saved to {output_path}")
        return report_text

def main():
    """Main audit function"""
    parser = argparse.ArgumentParser(
        description=SCRIPT_PURPOSE,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('--full', action='store_true',
                       help='Perform comprehensive deep audit')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check, don\'t suggest removals')
    parser.add_argument('--report', action='store_true',
                       help='Generate detailed report')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable detailed output')

    args = parser.parse_args()

    print("=" * 60)
    print("Vestigial Content Audit")
    print(f"Version: {SCRIPT_VERSION}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Run audit
    auditor = VestigialAuditor()
    findings = auditor.run_audit(full=args.full)

    # Generate report if requested
    if args.report:
        auditor.generate_report()

    # Print summary
    print("\n" + "=" * 60)
    print("Audit Complete!")
    print(f"✅ Vestigial files found: {auditor.stats['vestigial_files_found']}")
    print(f"💾 Potential space saved: {auditor.stats['potential_space_saved'] / (1024*1024):.2f} MB")

    if args.check_only:
        print("\n⚠️  Check-only mode - no removal suggestions generated")
    else:
        print("\n💡 Run with --report for detailed findings")
        print("🗑️  Use scripts/remove_vestigial.py to clean up")

    return 0 if auditor.stats['vestigial_files_found'] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())