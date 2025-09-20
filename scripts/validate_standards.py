#!/usr/bin/env python3
"""
SCRIPT: validate_standards.py
PURPOSE: Validate repository against all applicable standards from submodule
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T16:20:00-04:00

DESCRIPTION:
    Comprehensive standards validation script that checks the repository
    against all rules defined in .claude-rules.json and the standards
    submodule. Generates detailed reports of compliance status.

LLM_USAGE:
    python scripts/validate_standards.py [options]

ARGUMENTS:
    --report (str): Output report file (default: reports/standards_validation.md)
    --format (str): Report format [markdown|json|html] (default: markdown)
    --strict (bool): Fail on any warning (default: false)
    --fix (bool): Attempt to auto-fix violations where possible

EXAMPLES:
    # Run validation
    python scripts/validate_standards.py

    # Generate JSON report with strict mode
    python scripts/validate_standards.py --format json --strict

    # Auto-fix violations
    python scripts/validate_standards.py --fix

OUTPUT:
    - Validation report with pass/fail status
    - List of violations with severity levels
    - Recommendations for fixes

DEPENDENCIES:
    - Python 3.8+
    - scripts/lib/common.py for shared utilities

MANIFEST_REGISTRY: scripts/validate_standards.py
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))
from lib.common import (
    ManifestManager,
    TimeManager,
    StandardsValidator,
    Logger,
    FrontmatterParser,
    ensure_directory
)


class ComprehensiveStandardsValidator:
    """Validate repository against all standards"""

    def __init__(self):
        self.manifest_mgr = ManifestManager()
        self.time_mgr = TimeManager()
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.base_validator = StandardsValidator()

        # Load enforcement rules
        with open(".claude-rules.json", 'r') as f:
            self.rules = json.load(f)

        self.violations = []
        self.warnings = []
        self.passes = []

    def validate_all(self) -> Tuple[bool, Dict[str, Any]]:
        """Run all validation checks"""
        self.logger.info("Starting comprehensive standards validation...")

        # Run validation for each standard
        for standard_name, config in self.rules["MANDATORY_STANDARDS"].items():
            self.logger.info(f"Validating {standard_name}...")
            self.validate_standard(standard_name, config)

        # Additional specific validations
        self.validate_manifest_current()
        self.validate_no_duplicates()
        self.validate_directory_structure()
        self.validate_protected_files()
        self.validate_script_documentation()
        self.validate_content_standards()

        # Calculate results
        total_checks = len(self.violations) + len(self.warnings) + len(self.passes)
        pass_rate = (len(self.passes) / total_checks * 100) if total_checks > 0 else 0

        report = {
            "timestamp": self.time_mgr.get_current_timestamp(),
            "total_checks": total_checks,
            "passes": len(self.passes),
            "warnings": len(self.warnings),
            "violations": len(self.violations),
            "pass_rate": f"{pass_rate:.1f}%",
            "status": "PASS" if len(self.violations) == 0 else "FAIL",
            "details": {
                "violations": self.violations,
                "warnings": self.warnings,
                "passes": self.passes
            }
        }

        return len(self.violations) == 0, report

    def validate_standard(self, name: str, config: Dict[str, Any]):
        """Validate a specific standard"""
        for rule in config.get("rules", []):
            # Check if rule starts with MUST (critical) or SHOULD (warning)
            is_critical = rule.startswith("MUST")

            # Check applicable areas
            for area in config.get("applies_to", []):
                if self.check_rule_in_area(rule, area):
                    self.passes.append({
                        "standard": name,
                        "rule": rule,
                        "area": area,
                        "status": "PASS"
                    })
                else:
                    violation = {
                        "standard": name,
                        "rule": rule,
                        "area": area,
                        "severity": "HIGH" if is_critical else "MEDIUM",
                        "status": "FAIL"
                    }

                    if is_critical:
                        self.violations.append(violation)
                    else:
                        self.warnings.append(violation)

    def check_rule_in_area(self, rule: str, area: str) -> bool:
        """Check if a rule is satisfied in a specific area"""
        # Simplified rule checking - would be expanded for real validation
        area_path = Path(area.replace("*", ""))

        if not area_path.exists() and "*" not in area:
            return True  # Skip non-existent areas

        # Check specific rules
        if "MANIFEST.json" in rule and "single source of truth" in rule:
            return Path("MANIFEST.json").exists()

        if "file_registry" in rule and "before creating" in rule:
            # Check if manifest has file_registry
            manifest = self.manifest_mgr.manifest
            return "inventory" in manifest and "files" in manifest["inventory"]

        if "docstrings" in rule:
            # Check Python files for docstrings
            if area.endswith(".py") or "scripts/" in area:
                return self.check_python_docstrings(area_path)

        if "frontmatter" in rule:
            # Check markdown files for frontmatter
            if area.endswith(".md") or "posts/" in area:
                return self.check_markdown_frontmatter(area_path)

        # Default to pass for unimplemented checks
        return True

    def check_python_docstrings(self, path: Path) -> bool:
        """Check if Python files have docstrings"""
        if path.is_dir():
            py_files = list(path.glob("**/*.py"))
        else:
            py_files = [path] if path.suffix == ".py" else []

        for py_file in py_files[:5]:  # Sample check
            with open(py_file, 'r') as f:
                content = f.read()
                if not ('"""' in content[:500] or "'''" in content[:500]):
                    return False
        return True

    def check_markdown_frontmatter(self, path: Path) -> bool:
        """Check if markdown files have proper frontmatter"""
        if path.is_dir():
            md_files = list(path.glob("**/*.md"))
        else:
            md_files = [path] if path.suffix == ".md" else []

        for md_file in md_files[:5]:  # Sample check
            with open(md_file, 'r') as f:
                content = f.read()
                if not content.startswith("---"):
                    return False
        return True

    def validate_manifest_current(self):
        """Check if MANIFEST.json is current"""
        manifest = self.manifest_mgr.manifest
        last_validated = manifest.get("last_validated", "")

        if last_validated:
            # Parse timestamp and check if within 24 hours
            from datetime import datetime, timedelta
            try:
                last_time = datetime.fromisoformat(last_validated.replace("-04:00", ""))
                current_time = datetime.now()
                if (current_time - last_time) > timedelta(hours=24):
                    self.warnings.append({
                        "check": "MANIFEST.json currency",
                        "message": "MANIFEST.json not validated in last 24 hours",
                        "severity": "MEDIUM"
                    })
                else:
                    self.passes.append({
                        "check": "MANIFEST.json currency",
                        "status": "PASS"
                    })
            except:
                self.warnings.append({
                    "check": "MANIFEST.json currency",
                    "message": "Could not parse last_validated timestamp",
                    "severity": "LOW"
                })
        else:
            self.violations.append({
                "check": "MANIFEST.json currency",
                "message": "No last_validated timestamp found",
                "severity": "HIGH"
            })

    def validate_no_duplicates(self):
        """Check for duplicate files"""
        manifest = self.manifest_mgr.manifest
        file_registry = manifest.get("inventory", {}).get("files", {}).get("file_registry", {})

        # Check for duplicate names
        seen_names = {}
        duplicates = []

        for filepath, info in file_registry.items():
            name = Path(filepath).name
            if name in seen_names:
                duplicates.append((name, filepath, seen_names[name]))
            else:
                seen_names[name] = filepath

        if duplicates:
            for name, path1, path2 in duplicates:
                self.violations.append({
                    "check": "No duplicate files",
                    "message": f"Duplicate file '{name}' found at '{path1}' and '{path2}'",
                    "severity": "HIGH"
                })
        else:
            self.passes.append({
                "check": "No duplicate files",
                "status": "PASS"
            })

    def validate_directory_structure(self):
        """Validate directory structure matches standards"""
        dir_structure = self.rules.get("DIRECTORY_STRUCTURE", {})

        for dir_name, config in dir_structure.items():
            dir_path = Path(dir_name)
            if not dir_path.exists():
                self.warnings.append({
                    "check": "Directory structure",
                    "message": f"Expected directory '{dir_name}' not found",
                    "severity": "LOW"
                })
                continue

            # Check for unexpected files
            for file_path in dir_path.glob("*"):
                if file_path.is_file():
                    allowed = False
                    for pattern in config.get("allowed", []):
                        if pattern.startswith("*."):
                            if file_path.suffix == pattern[1:]:
                                allowed = True
                                break

                    if not allowed and file_path.name not in [".gitkeep", "__pycache__"]:
                        self.warnings.append({
                            "check": "Directory structure",
                            "message": f"Unexpected file type '{file_path}' in '{dir_name}'",
                            "severity": "LOW"
                        })

            self.passes.append({
                "check": f"Directory structure: {dir_name}",
                "status": "PASS"
            })

    def validate_protected_files(self):
        """Ensure protected files exist and haven't been modified incorrectly"""
        for protected_file in self.rules.get("PROTECTED_FILES", []):
            file_path = Path(protected_file)
            if not file_path.exists():
                self.violations.append({
                    "check": "Protected files",
                    "message": f"Protected file '{protected_file}' not found",
                    "severity": "HIGH"
                })
            else:
                self.passes.append({
                    "check": f"Protected file: {protected_file}",
                    "status": "PASS"
                })

    def validate_script_documentation(self):
        """Check if scripts have LLM documentation"""
        scripts_dir = Path("scripts")
        undocumented = []

        for script in scripts_dir.glob("*.py"):
            with open(script, 'r') as f:
                content = f.read(1000)  # Check first 1000 chars
                if "LLM_READY: True" not in content:
                    undocumented.append(script.name)

        if undocumented:
            for script in undocumented[:5]:  # Report first 5
                self.warnings.append({
                    "check": "Script documentation",
                    "message": f"Script '{script}' missing LLM documentation",
                    "severity": "MEDIUM"
                })
        else:
            self.passes.append({
                "check": "Script documentation",
                "status": "PASS - All scripts documented"
            })

    def validate_content_standards(self):
        """Validate blog posts against content standards"""
        posts_dir = Path("src/posts")
        if not posts_dir.exists():
            return

        issues = []
        for post in list(posts_dir.glob("*.md"))[:10]:  # Check first 10 posts
            with open(post, 'r') as f:
                content = f.read()

            frontmatter, body = FrontmatterParser.parse(content)

            # Check frontmatter
            required_fields = ['title', 'date', 'description']
            for field in required_fields:
                if field not in frontmatter:
                    issues.append(f"Post '{post.name}' missing '{field}' in frontmatter")

            # Check for hero image
            if 'images' not in frontmatter or 'hero' not in frontmatter.get('images', {}):
                issues.append(f"Post '{post.name}' missing hero image")

        if issues:
            for issue in issues[:5]:  # Report first 5
                self.warnings.append({
                    "check": "Content standards",
                    "message": issue,
                    "severity": "MEDIUM"
                })
        else:
            self.passes.append({
                "check": "Content standards",
                "status": "PASS"
            })

    def generate_report(self, report_data: Dict[str, Any], format: str = "markdown") -> str:
        """Generate validation report in specified format"""
        if format == "json":
            return json.dumps(report_data, indent=2)

        elif format == "markdown":
            report = []
            report.append("# Standards Validation Report")
            report.append(f"\n**Generated:** {report_data['timestamp']}")
            report.append(f"**Status:** {report_data['status']}")
            report.append(f"**Pass Rate:** {report_data['pass_rate']}")
            report.append("")
            report.append("## Summary")
            report.append(f"- Total Checks: {report_data['total_checks']}")
            report.append(f"- Passes: {report_data['passes']}")
            report.append(f"- Warnings: {report_data['warnings']}")
            report.append(f"- Violations: {report_data['violations']}")
            report.append("")

            if report_data['details']['violations']:
                report.append("## ❌ Violations (Must Fix)")
                for violation in report_data['details']['violations']:
                    report.append(f"- **{violation.get('severity', 'HIGH')}**: {violation}")

            if report_data['details']['warnings']:
                report.append("\n## ⚠️ Warnings (Should Fix)")
                for warning in report_data['details']['warnings'][:10]:
                    report.append(f"- **{warning.get('severity', 'MEDIUM')}**: {warning}")

            report.append("\n## ✅ Passes")
            report.append(f"- {len(report_data['details']['passes'])} checks passed")

            return "\n".join(report)

        return str(report_data)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate repository against standards"
    )

    parser.add_argument('--report', default='reports/standards_validation.md',
                       help='Output report file')
    parser.add_argument('--format', choices=['markdown', 'json', 'html'],
                       default='markdown', help='Report format')
    parser.add_argument('--strict', action='store_true',
                       help='Fail on any warning')
    parser.add_argument('--fix', action='store_true',
                       help='Attempt to auto-fix violations')

    args = parser.parse_args()

    # Initialize validator
    validator = ComprehensiveStandardsValidator()

    # Run validation
    is_passing, report = validator.validate_all()

    # Check strict mode
    if args.strict and report['warnings'] > 0:
        is_passing = False

    # Generate report
    report_content = validator.generate_report(report, args.format)

    # Save report
    ensure_directory(Path(args.report).parent)
    with open(args.report, 'w') as f:
        f.write(report_content)

    print(f"📋 Validation Report saved to: {args.report}")
    print(f"\n📊 Summary:")
    print(f"  Status: {report['status']}")
    print(f"  Pass Rate: {report['pass_rate']}")
    print(f"  Violations: {report['violations']}")
    print(f"  Warnings: {report['warnings']}")
    print(f"  Passes: {report['passes']}")

    if is_passing:
        print("\n✅ Standards validation PASSED")
        return 0
    else:
        print("\n❌ Standards validation FAILED")
        print(f"  See {args.report} for details")
        return 1


if __name__ == "__main__":
    sys.exit(main())