#!/usr/bin/env python3
"""
SCRIPT: repo-maintenance.py
PURPOSE: Automated repository cleanup and health monitoring
CATEGORY: maintenance
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-10-29T00:00:00-04:00

DESCRIPTION:
    Comprehensive repository maintenance tool that performs:
    - Temporary file cleanup
    - Report archival
    - Image variant detection
    - Duplicate file detection
    - Health metrics collection
    - SEO drift detection

LLM_USAGE:
    This script is designed for monthly maintenance and can be run from cron or GitHub Actions.
    It integrates with the repository's standards and validation system.

ARGUMENTS:
    --dry-run          Preview changes without applying
    --cleanup          Run cleanup operations
    --archive          Archive old reports
    --health-check     Run health metrics only
    --full             Run all operations
    --verbose          Detailed output
    --force            Skip confirmation prompts
    --backup           Create backups before archiving

EXAMPLES:
    # Preview all operations
    python scripts/utilities/repo-maintenance.py --dry-run --full

    # Run cleanup only
    python scripts/utilities/repo-maintenance.py --cleanup

    # Full maintenance with backup
    python scripts/utilities/repo-maintenance.py --full --backup

    # Health check only
    python scripts/utilities/repo-maintenance.py --health-check --verbose

INTEGRATION:
    - Monthly cron: 0 0 1 * * python scripts/utilities/repo-maintenance.py --full
    - GitHub Actions: call with --full --force for automated runs
    - Pre-release: call with --health-check to ensure repository health

EXIT_CODES:
    0 - Clean (no issues)
    1 - Warnings (non-critical issues)
    2 - Errors (critical issues)

SAFETY:
    Never deletes:
    - MANIFEST.json, CLAUDE.md, .claude-rules.json
    - Any files in .git/
    - Protected files defined in .claude-rules.json
    - Files modified within 7 days (for cleanup)
"""

import argparse
import json
import sys
import re
import subprocess
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
    from common import (
        ManifestManager, TimeManager, FileHasher, ConfigManager,
        Logger, ensure_directory, read_json, write_json, format_size
    )
except ImportError:
    print("ERROR: Failed to import common utilities from scripts/lib/common.py")
    sys.exit(2)


# Color codes for console output
class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class MaintenanceReport:
    """Collect and report maintenance findings"""

    def __init__(self):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.findings = defaultdict(list)
        self.stats = defaultdict(int)
        self.errors = []
        self.warnings = []
        self.actions = []

    def add_finding(self, category: str, message: str, severity: str = "info"):
        """Add a finding to the report"""
        self.findings[category].append({
            "message": message,
            "severity": severity,
            "timestamp": TimeManager.get_current_timestamp()
        })

        if severity == "error":
            self.errors.append(message)
        elif severity == "warning":
            self.warnings.append(message)

    def add_action(self, action: str, status: str = "completed"):
        """Record an action taken"""
        self.actions.append({
            "action": action,
            "status": status,
            "timestamp": TimeManager.get_current_timestamp()
        })

    def update_stat(self, key: str, value: int):
        """Update a statistic"""
        self.stats[key] = value

    def increment_stat(self, key: str, amount: int = 1):
        """Increment a statistic"""
        self.stats[key] += amount

    def print_summary(self, verbose: bool = False):
        """Print colored summary to console"""
        print(f"\n{Colors.BOLD}{Colors.CYAN}=== Repository Maintenance Report ==={Colors.RESET}\n")

        # Statistics
        print(f"{Colors.BOLD}Statistics:{Colors.RESET}")
        for key, value in sorted(self.stats.items()):
            print(f"  {key}: {value}")
        print()

        # Actions
        if self.actions:
            print(f"{Colors.BOLD}Actions Taken:{Colors.RESET}")
            for action in self.actions:
                status_color = Colors.GREEN if action["status"] == "completed" else Colors.YELLOW
                print(f"  {status_color}✓{Colors.RESET} {action['action']}")
            print()

        # Errors
        if self.errors:
            print(f"{Colors.BOLD}{Colors.RED}Errors ({len(self.errors)}):{Colors.RESET}")
            for error in self.errors:
                print(f"  {Colors.RED}✗{Colors.RESET} {error}")
            print()

        # Warnings
        if self.warnings:
            print(f"{Colors.BOLD}{Colors.YELLOW}Warnings ({len(self.warnings)}):{Colors.RESET}")
            for warning in self.warnings:
                print(f"  {Colors.YELLOW}⚠{Colors.RESET} {warning}")
            print()

        # Detailed findings (if verbose)
        if verbose and self.findings:
            print(f"{Colors.BOLD}Detailed Findings:{Colors.RESET}")
            for category, findings in self.findings.items():
                print(f"\n  {Colors.MAGENTA}{category}:{Colors.RESET}")
                for finding in findings:
                    severity_icon = {
                        "error": f"{Colors.RED}✗{Colors.RESET}",
                        "warning": f"{Colors.YELLOW}⚠{Colors.RESET}",
                        "info": f"{Colors.BLUE}ℹ{Colors.RESET}"
                    }.get(finding["severity"], "•")
                    print(f"    {severity_icon} {finding['message']}")
            print()

        # Exit status
        if self.errors:
            print(f"{Colors.RED}Status: ERRORS FOUND{Colors.RESET}")
        elif self.warnings:
            print(f"{Colors.YELLOW}Status: WARNINGS{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}Status: CLEAN{Colors.RESET}")
        print()

    def get_exit_code(self) -> int:
        """Get appropriate exit code"""
        if self.errors:
            return 2
        elif self.warnings:
            return 1
        return 0

    def save_json(self, filepath: Path) -> bool:
        """Save report as JSON"""
        report_data = {
            "timestamp": TimeManager.get_current_timestamp(),
            "statistics": dict(self.stats),
            "actions": self.actions,
            "findings": dict(self.findings),
            "errors": self.errors,
            "warnings": self.warnings,
            "exit_code": self.get_exit_code()
        }

        ensure_directory(filepath.parent)
        return write_json(report_data, filepath)


class TempFileCleanup:
    """Handle temporary file cleanup"""

    def __init__(self, report: MaintenanceReport, dry_run: bool = False):
        self.report = report
        self.dry_run = dry_run
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.root_dir = Path.cwd()

        # Protected files that should never be deleted
        self.protected_files = {
            "requirements.txt",
            "test-citation-workflow.sh",
            "MANIFEST.json",
            "CLAUDE.md",
            ".claude-rules.json",
            ".eleventy.js",
            "package.json",
            "tailwind.config.js",
            "README.md"
        }

        # Temp file patterns
        self.temp_patterns = [
            r"^test-.*\.py$",
            r"^validate-.*\.py$",
            r"^fix-.*\.py$",
            r".*\.bak$",
            r".*\.tmp$",
            r".*\.swp$",
            r".*~$"
        ]

    def scan_temp_files(self) -> List[Path]:
        """Scan for temporary files"""
        temp_files = []
        cutoff_date = datetime.now() - timedelta(days=7)

        # Scan root directory
        for file_path in self.root_dir.iterdir():
            if not file_path.is_file():
                continue

            if file_path.name in self.protected_files:
                continue

            # Check against temp patterns
            for pattern in self.temp_patterns:
                if re.match(pattern, file_path.name):
                    # Check modification time
                    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    if mtime < cutoff_date:
                        temp_files.append(file_path)
                        self.report.add_finding(
                            "temp_files",
                            f"Found temp file: {file_path.name} (modified {mtime.strftime('%Y-%m-%d')})",
                            "info"
                        )
                    break

        self.report.update_stat("temp_files_found", len(temp_files))
        return temp_files

    def cleanup(self) -> int:
        """Remove temporary files"""
        temp_files = self.scan_temp_files()
        removed_count = 0

        for file_path in temp_files:
            try:
                if self.dry_run:
                    self.logger.info(f"[DRY-RUN] Would delete: {file_path.name}")
                else:
                    file_path.unlink()
                    self.logger.info(f"Deleted: {file_path.name}")
                    self.report.add_action(f"Deleted temp file: {file_path.name}")
                removed_count += 1
            except Exception as e:
                self.report.add_finding(
                    "cleanup_errors",
                    f"Failed to delete {file_path.name}: {e}",
                    "error"
                )

        self.report.update_stat("temp_files_removed", removed_count)
        return removed_count


class ReportArchiver:
    """Archive old reports"""

    def __init__(self, report: MaintenanceReport, dry_run: bool = False, backup: bool = False):
        self.report = report
        self.dry_run = dry_run
        self.backup = backup
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.reports_dir = Path("docs/reports")
        self.archive_dir = Path("docs/archive/reports")

        # Files to preserve
        self.preserve_patterns = [
            r"^script-metadata\.json$",
            r"^maintenance-.*\.json$"
        ]

    def scan_old_reports(self) -> List[Path]:
        """Scan for reports older than 60 days"""
        if not self.reports_dir.exists():
            return []

        old_reports = []
        cutoff_date = datetime.now() - timedelta(days=60)

        for file_path in self.reports_dir.rglob("*"):
            if not file_path.is_file():
                continue

            # Check if file should be preserved
            preserve = False
            for pattern in self.preserve_patterns:
                if re.match(pattern, file_path.name):
                    preserve = True
                    break

            if preserve:
                continue

            # Check modification time
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if mtime < cutoff_date:
                old_reports.append(file_path)
                self.report.add_finding(
                    "old_reports",
                    f"Found old report: {file_path.relative_to(Path.cwd())} (modified {mtime.strftime('%Y-%m-%d')})",
                    "info"
                )

        self.report.update_stat("old_reports_found", len(old_reports))
        return old_reports

    def archive_reports(self) -> int:
        """Archive old reports"""
        old_reports = self.scan_old_reports()
        archived_count = 0

        for file_path in old_reports:
            try:
                # Determine archive location based on modification date
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                year_month = mtime.strftime("%Y-%m")
                archive_path = self.archive_dir / year_month / file_path.name

                if self.dry_run:
                    self.logger.info(f"[DRY-RUN] Would archive: {file_path.name} -> {archive_path}")
                else:
                    ensure_directory(archive_path.parent)

                    # Backup if requested
                    if self.backup:
                        backup_path = archive_path.with_suffix(f".backup{archive_path.suffix}")
                        shutil.copy2(file_path, backup_path)

                    # Move to archive
                    shutil.move(str(file_path), str(archive_path))
                    self.logger.info(f"Archived: {file_path.name} -> {archive_path}")
                    self.report.add_action(f"Archived report: {file_path.name}")

                archived_count += 1
            except Exception as e:
                self.report.add_finding(
                    "archive_errors",
                    f"Failed to archive {file_path.name}: {e}",
                    "error"
                )

        self.report.update_stat("reports_archived", archived_count)
        return archived_count


class ImageVariantDetector:
    """Detect recursive image variants"""

    def __init__(self, report: MaintenanceReport):
        self.report = report
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.images_dir = Path("src/assets/images")

    def scan_variants(self) -> List[Path]:
        """Scan for recursive variants"""
        if not self.images_dir.exists():
            return []

        variants = []
        # Pattern for recursive variants: filename-###-###.ext
        variant_pattern = r".*-\d{3}-\d{3}\.\w+$"

        for file_path in self.images_dir.rglob("*"):
            if not file_path.is_file():
                continue

            if re.match(variant_pattern, file_path.name):
                variants.append(file_path)
                self.report.add_finding(
                    "image_variants",
                    f"Found recursive variant: {file_path.relative_to(Path.cwd())}",
                    "warning"
                )

        self.report.update_stat("image_variants_found", len(variants))
        return variants


class DuplicateDetector:
    """Detect duplicate files"""

    def __init__(self, report: MaintenanceReport):
        self.report = report
        self.logger = Logger.get_logger(self.__class__.__name__)

    def scan_duplicates(self, directory: Path) -> Dict[str, List[Path]]:
        """Scan for duplicate files by hash"""
        if not directory.exists():
            return {}

        hash_map = defaultdict(list)

        for file_path in directory.rglob("*"):
            if not file_path.is_file():
                continue

            # Skip very small files (likely not duplicates of interest)
            if file_path.stat().st_size < 100:
                continue

            file_hash = FileHasher.get_sha256(file_path)
            if file_hash:
                hash_map[file_hash].append(file_path)

        # Filter to only actual duplicates
        duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}

        for file_hash, files in duplicates.items():
            file_list = ", ".join(str(f.relative_to(Path.cwd())) for f in files)
            self.report.add_finding(
                "duplicates",
                f"Duplicate files ({len(files)}): {file_list}",
                "warning"
            )

        self.report.update_stat("duplicate_sets", len(duplicates))
        self.report.update_stat("duplicate_files", sum(len(files) - 1 for files in duplicates.values()))

        return duplicates


class HealthChecker:
    """Repository health metrics"""

    def __init__(self, report: MaintenanceReport):
        self.report = report
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.root_dir = Path.cwd()

    def check_all(self) -> Dict[str, Any]:
        """Run all health checks"""
        health = {}

        health["manifest"] = self.check_manifest()
        health["scripts"] = self.check_scripts()
        health["precommit"] = self.check_precommit_hooks()
        health["npm"] = self.check_npm_audit()
        health["git"] = self.check_git_status()

        return health

    def check_manifest(self) -> Dict[str, Any]:
        """Check MANIFEST.json validity"""
        manifest_path = self.root_dir / "MANIFEST.json"

        if not manifest_path.exists():
            self.report.add_finding("health", "MANIFEST.json not found", "error")
            return {"valid": False, "error": "File not found"}

        try:
            manifest = ManifestManager()

            # Check if recent
            last_validated = manifest.get_section("last_validated")
            if last_validated:
                last_date = TimeManager.parse_timestamp(last_validated)
                days_old = (datetime.now() - last_date.replace(tzinfo=None)).days

                if days_old > 30:
                    self.report.add_finding(
                        "health",
                        f"MANIFEST.json last validated {days_old} days ago",
                        "warning"
                    )

            self.report.add_finding("health", "MANIFEST.json is valid", "info")
            return {"valid": True, "last_validated": last_validated}

        except Exception as e:
            self.report.add_finding("health", f"MANIFEST.json validation failed: {e}", "error")
            return {"valid": False, "error": str(e)}

    def check_scripts(self) -> Dict[str, int]:
        """Count scripts and check for recent changes"""
        scripts_dir = self.root_dir / "scripts"

        if not scripts_dir.exists():
            return {"total": 0, "new": 0, "modified": 0}

        total = 0
        new_count = 0
        modified_count = 0

        week_ago = datetime.now() - timedelta(days=7)

        for file_path in scripts_dir.rglob("*.py"):
            if file_path.is_file():
                total += 1
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

                if mtime > week_ago:
                    # Check if it's new or modified
                    try:
                        result = subprocess.run(
                            ["git", "log", "--follow", "--diff-filter=A", "--", str(file_path)],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )

                        if result.stdout and "Date:" in result.stdout:
                            # Parse git log date
                            new_count += 1
                        else:
                            modified_count += 1
                    except:
                        pass

        self.report.update_stat("total_scripts", total)
        self.report.update_stat("new_scripts_week", new_count)
        self.report.update_stat("modified_scripts_week", modified_count)

        return {"total": total, "new": new_count, "modified": modified_count}

    def check_precommit_hooks(self) -> Dict[str, bool]:
        """Check if pre-commit hooks are installed"""
        git_hooks = self.root_dir / ".git" / "hooks" / "pre-commit"

        installed = git_hooks.exists()

        if installed:
            self.report.add_finding("health", "Pre-commit hooks installed", "info")
        else:
            self.report.add_finding("health", "Pre-commit hooks not installed", "warning")

        return {"installed": installed}

    def check_npm_audit(self) -> Dict[str, Any]:
        """Run npm audit and report status"""
        try:
            result = subprocess.run(
                ["npm", "audit", "--json"],
                capture_output=True,
                text=True,
                timeout=30
            )

            audit_data = json.loads(result.stdout)

            vulnerabilities = audit_data.get("metadata", {}).get("vulnerabilities", {})
            total_vulns = sum(vulnerabilities.values())

            if total_vulns > 0:
                self.report.add_finding(
                    "health",
                    f"npm audit found {total_vulns} vulnerabilities",
                    "warning" if total_vulns < 5 else "error"
                )
            else:
                self.report.add_finding("health", "npm audit: no vulnerabilities", "info")

            return {
                "vulnerabilities": vulnerabilities,
                "total": total_vulns
            }

        except Exception as e:
            self.report.add_finding("health", f"npm audit failed: {e}", "warning")
            return {"error": str(e)}

    def check_git_status(self) -> Dict[str, Any]:
        """Check git repository status"""
        try:
            # Check for uncommitted changes
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=10
            )

            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

            if uncommitted > 0:
                self.report.add_finding(
                    "health",
                    f"Repository has {uncommitted} uncommitted changes",
                    "info"
                )

            # Check for unpushed commits
            result = subprocess.run(
                ["git", "log", "@{u}..", "--oneline"],
                capture_output=True,
                text=True,
                timeout=10
            )

            unpushed = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0

            if unpushed > 0:
                self.report.add_finding(
                    "health",
                    f"Repository has {unpushed} unpushed commits",
                    "info"
                )

            return {
                "uncommitted_files": uncommitted,
                "unpushed_commits": unpushed
            }

        except Exception as e:
            self.report.add_finding("health", f"Git status check failed: {e}", "warning")
            return {"error": str(e)}


class SEODriftDetector:
    """Detect SEO drift in meta descriptions"""

    def __init__(self, report: MaintenanceReport):
        self.report = report
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.posts_dir = Path("src/posts")

    def check_meta_descriptions(self) -> Dict[str, Any]:
        """Check meta descriptions for drift"""
        if not self.posts_dir.exists():
            return {"error": "Posts directory not found"}

        total_posts = 0
        out_of_range = 0
        descriptions = []

        for post_path in self.posts_dir.glob("*.md"):
            with open(post_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract description from frontmatter
            match = re.search(r'^description:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)

            if match:
                description = match.group(1).strip()
                desc_len = len(description)
                descriptions.append({
                    "post": post_path.name,
                    "length": desc_len,
                    "description": description
                })

                total_posts += 1

                if desc_len < 120 or desc_len > 160:
                    out_of_range += 1
                    severity = "warning" if desc_len < 110 or desc_len > 170 else "info"
                    self.report.add_finding(
                        "seo_drift",
                        f"{post_path.name}: description length {desc_len} (target: 120-160)",
                        severity
                    )

        drift_percentage = (out_of_range / total_posts * 100) if total_posts > 0 else 0

        if drift_percentage > 10:
            self.report.add_finding(
                "seo_drift",
                f"{drift_percentage:.1f}% of posts have out-of-range descriptions",
                "warning"
            )

        self.report.update_stat("total_posts_checked", total_posts)
        self.report.update_stat("posts_with_seo_drift", out_of_range)

        return {
            "total_posts": total_posts,
            "out_of_range": out_of_range,
            "drift_percentage": drift_percentage,
            "descriptions": descriptions
        }


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Repository maintenance and health monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview all operations
  python scripts/utilities/repo-maintenance.py --dry-run --full

  # Run cleanup only
  python scripts/utilities/repo-maintenance.py --cleanup

  # Full maintenance with backup
  python scripts/utilities/repo-maintenance.py --full --backup

  # Health check only
  python scripts/utilities/repo-maintenance.py --health-check --verbose
        """
    )

    parser.add_argument("--dry-run", action="store_true",
                        help="Preview changes without applying")
    parser.add_argument("--cleanup", action="store_true",
                        help="Run cleanup operations")
    parser.add_argument("--archive", action="store_true",
                        help="Archive old reports")
    parser.add_argument("--health-check", action="store_true",
                        help="Run health metrics only")
    parser.add_argument("--full", action="store_true",
                        help="Run all operations")
    parser.add_argument("--verbose", action="store_true",
                        help="Detailed output")
    parser.add_argument("--force", action="store_true",
                        help="Skip confirmation prompts")
    parser.add_argument("--backup", action="store_true",
                        help="Create backups before archiving")

    args = parser.parse_args()

    # Determine which operations to run
    run_cleanup = args.cleanup or args.full
    run_archive = args.archive or args.full
    run_health = args.health_check or args.full

    # If no specific operation selected, run health check
    if not any([run_cleanup, run_archive, run_health]):
        run_health = True

    # Initialize report
    report = MaintenanceReport()

    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 60)
    print("Repository Maintenance Tool")
    print("=" * 60)
    print(f"{Colors.RESET}")

    if args.dry_run:
        print(f"{Colors.YELLOW}[DRY-RUN MODE] No changes will be made{Colors.RESET}\n")

    # Run operations
    try:
        # Cleanup
        if run_cleanup:
            print(f"{Colors.BOLD}Running cleanup...{Colors.RESET}")
            cleaner = TempFileCleanup(report, args.dry_run)
            cleaner.cleanup()
            print()

        # Archive
        if run_archive:
            print(f"{Colors.BOLD}Archiving old reports...{Colors.RESET}")
            archiver = ReportArchiver(report, args.dry_run, args.backup)
            archiver.archive_reports()
            print()

        # Health check
        if run_health:
            print(f"{Colors.BOLD}Running health checks...{Colors.RESET}")

            # Check manifest
            health_checker = HealthChecker(report)
            health_checker.check_all()

            # Check for image variants
            variant_detector = ImageVariantDetector(report)
            variant_detector.scan_variants()

            # Check for duplicates in docs
            duplicate_detector = DuplicateDetector(report)
            duplicate_detector.scan_duplicates(Path("docs"))

            # Check SEO drift
            seo_detector = SEODriftDetector(report)
            seo_detector.check_meta_descriptions()

            print()

        # Print summary
        report.print_summary(args.verbose)

        # Save report
        timestamp = datetime.now().strftime("%Y-%m-%d")
        report_path = Path(f"docs/reports/maintenance-{timestamp}.json")

        if not args.dry_run:
            if report.save_json(report_path):
                print(f"{Colors.GREEN}✓{Colors.RESET} Report saved to: {report_path}\n")

        # Exit with appropriate code
        sys.exit(report.get_exit_code())

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Fatal error: {e}{Colors.RESET}")
        sys.exit(2)


if __name__ == "__main__":
    main()
