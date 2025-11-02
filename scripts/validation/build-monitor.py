#!/usr/bin/env -S uv run python3
"""
Build Monitor - Continuous build validation and comparison

Monitors build process, detects regressions, and provides detailed diagnostics

Usage:
    uv run python scripts/validation/build-monitor.py [--baseline] [--compare]
"""

import os
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

class BuildMonitor:
    def __init__(self, baseline_file: str = ".build-baseline.json"):
        self.baseline_file = Path(baseline_file)
        self.current_build = {}
        self.baseline_build = None

    def run_build(self) -> Dict:
        """Run npm build and capture metrics"""
        print(f"{Colors.HEADER}Running build process...{Colors.ENDC}\n")

        start_time = time.time()

        try:
            # Run build command
            result = subprocess.run(
                ["npm", "run", "build"],
                capture_output=True,
                text=True,
                timeout=120
            )

            build_time = time.time() - start_time

            # Parse output for metrics
            output = result.stdout + result.stderr

            build_data = {
                "timestamp": datetime.now().isoformat(),
                "success": result.returncode == 0,
                "build_time": round(build_time, 2),
                "return_code": result.returncode,
                "stats": self._parse_build_output(output),
                "warnings": self._extract_warnings(output),
                "errors": self._extract_errors(output)
            }

            self.current_build = build_data
            return build_data

        except subprocess.TimeoutExpired:
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": "Build timeout (>120s)",
                "build_time": 120
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": str(e)
            }

    def _parse_build_output(self, output: str) -> Dict:
        """Parse build output for statistics"""
        stats = {
            "posts_parsed": 0,
            "files_written": 0,
            "files_copied": 0,
            "total_words": 0,
            "js_bundles": {},
            "eleventy_time": None
        }

        # Extract post count
        if "Successfully parsed" in output:
            for line in output.split('\n'):
                if "Successfully parsed" in line:
                    try:
                        stats["posts_parsed"] = int(line.split()[-2])
                    except (ValueError, IndexError):
                        pass

        # Extract files written
        if "Wrote" in output:
            for line in output.split('\n'):
                if "Wrote" in line and "files" in line:
                    try:
                        parts = line.split()
                        stats["files_written"] = int(parts[parts.index("Wrote") + 1])
                    except (ValueError, IndexError):
                        pass

        # Extract Eleventy build time
        if "seconds" in output:
            for line in output.split('\n'):
                if "seconds" in line and "Wrote" in line:
                    try:
                        time_str = line.split("in")[1].split("seconds")[0].strip()
                        stats["eleventy_time"] = float(time_str)
                    except (ValueError, IndexError):
                        pass

        # Extract JS bundle sizes
        if "Creating bundle:" in output:
            bundle_name = None
            for line in output.split('\n'):
                if "Creating bundle:" in line:
                    bundle_name = line.split(":")[-1].strip()
                elif "Minified:" in line and bundle_name:
                    try:
                        # Parse "29.30 KB → 14.95 KB (49.0% reduction)"
                        parts = line.split("→")
                        original = parts[0].split("Minified:")[-1].strip()
                        minified_parts = parts[1].split("(")
                        minified = minified_parts[0].strip()
                        reduction = minified_parts[1].split("%")[0].strip()

                        stats["js_bundles"][bundle_name] = {
                            "original": original,
                            "minified": minified,
                            "reduction": float(reduction)
                        }
                    except (ValueError, IndexError):
                        pass

        return stats

    def _extract_warnings(self, output: str) -> List[str]:
        """Extract warning messages from build output"""
        warnings = []
        for line in output.split('\n'):
            if 'warn' in line.lower() or 'warning' in line.lower():
                warnings.append(line.strip())
        return warnings

    def _extract_errors(self, output: str) -> List[str]:
        """Extract error messages from build output"""
        errors = []
        for line in output.split('\n'):
            if 'error' in line.lower() and 'warn' not in line.lower():
                errors.append(line.strip())
        return errors

    def save_baseline(self):
        """Save current build as baseline"""
        with open(self.baseline_file, 'w') as f:
            json.dump(self.current_build, f, indent=2)

        print(f"{Colors.OKGREEN}Baseline saved to {self.baseline_file}{Colors.ENDC}")

    def load_baseline(self) -> Optional[Dict]:
        """Load baseline build data"""
        if not self.baseline_file.exists():
            return None

        with open(self.baseline_file, 'r') as f:
            self.baseline_build = json.load(f)

        return self.baseline_build

    def compare_builds(self) -> Dict:
        """Compare current build with baseline"""
        if not self.baseline_build:
            return {"error": "No baseline found"}

        comparison = {
            "status_change": None,
            "time_delta": None,
            "time_delta_percent": None,
            "stats_changes": {},
            "new_warnings": [],
            "new_errors": [],
            "regression_detected": False
        }

        # Status comparison
        baseline_success = self.baseline_build.get("success", False)
        current_success = self.current_build.get("success", False)

        if baseline_success and not current_success:
            comparison["status_change"] = "REGRESSION"
            comparison["regression_detected"] = True
        elif not baseline_success and current_success:
            comparison["status_change"] = "FIXED"
        else:
            comparison["status_change"] = "UNCHANGED"

        # Time comparison
        baseline_time = self.baseline_build.get("build_time", 0)
        current_time = self.current_build.get("build_time", 0)

        if baseline_time > 0:
            time_delta = current_time - baseline_time
            time_delta_percent = (time_delta / baseline_time) * 100
            comparison["time_delta"] = round(time_delta, 2)
            comparison["time_delta_percent"] = round(time_delta_percent, 1)

            # Flag significant time regression (>20% slower)
            if time_delta_percent > 20:
                comparison["regression_detected"] = True

        # Stats comparison
        baseline_stats = self.baseline_build.get("stats", {})
        current_stats = self.current_build.get("stats", {})

        for key in baseline_stats:
            if key in current_stats and key != "js_bundles":
                baseline_val = baseline_stats[key]
                current_val = current_stats[key]
                if baseline_val != current_val:
                    comparison["stats_changes"][key] = {
                        "baseline": baseline_val,
                        "current": current_val,
                        "delta": current_val - baseline_val if isinstance(current_val, (int, float)) else "N/A"
                    }

        # New warnings/errors
        baseline_warnings = set(self.baseline_build.get("warnings", []))
        current_warnings = set(self.current_build.get("warnings", []))
        comparison["new_warnings"] = list(current_warnings - baseline_warnings)

        baseline_errors = set(self.baseline_build.get("errors", []))
        current_errors = set(self.current_build.get("errors", []))
        comparison["new_errors"] = list(current_errors - baseline_errors)

        if comparison["new_errors"]:
            comparison["regression_detected"] = True

        return comparison

    def print_build_report(self, compare: bool = False):
        """Print formatted build report"""
        print(f"\n{Colors.HEADER}{'=' * 80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}BUILD VALIDATION REPORT{Colors.ENDC}")
        print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}\n")

        # Build status
        if self.current_build.get("success"):
            status_color = Colors.OKGREEN
            status_text = "PASSING"
        else:
            status_color = Colors.FAIL
            status_text = "FAILED"

        print(f"{Colors.BOLD}Build Status:{Colors.ENDC} {status_color}{status_text}{Colors.ENDC}")
        print(f"{Colors.BOLD}Build Time:{Colors.ENDC} {self.current_build.get('build_time', 'N/A')}s")
        print(f"{Colors.BOLD}Timestamp:{Colors.ENDC} {self.current_build.get('timestamp', 'N/A')}\n")

        # Statistics
        stats = self.current_build.get("stats", {})
        if stats:
            print(f"{Colors.OKBLUE}{Colors.BOLD}Build Statistics:{Colors.ENDC}")
            print(f"  Posts parsed: {stats.get('posts_parsed', 'N/A')}")
            print(f"  Files written: {stats.get('files_written', 'N/A')}")
            print(f"  Eleventy time: {stats.get('eleventy_time', 'N/A')}s")

            if stats.get("js_bundles"):
                print(f"\n  {Colors.BOLD}JavaScript Bundles:{Colors.ENDC}")
                for bundle, data in stats["js_bundles"].items():
                    print(f"    {bundle}: {data['original']} → {data['minified']} ({data['reduction']}%)")
            print()

        # Warnings and errors
        warnings = self.current_build.get("warnings", [])
        errors = self.current_build.get("errors", [])

        if warnings:
            print(f"{Colors.WARNING}{Colors.BOLD}Warnings ({len(warnings)}):{Colors.ENDC}")
            for warning in warnings[:5]:  # Show first 5
                print(f"  - {warning}")
            if len(warnings) > 5:
                print(f"  ... and {len(warnings) - 5} more")
            print()

        if errors:
            print(f"{Colors.FAIL}{Colors.BOLD}Errors ({len(errors)}):{Colors.ENDC}")
            for error in errors:
                print(f"  - {error}")
            print()

        # Comparison with baseline
        if compare and self.baseline_build:
            comparison = self.compare_builds()

            print(f"{Colors.OKBLUE}{Colors.BOLD}Comparison with Baseline:{Colors.ENDC}")
            print(f"  Status: {comparison['status_change']}")

            if comparison['time_delta'] is not None:
                time_color = Colors.OKGREEN if comparison['time_delta'] <= 0 else Colors.WARNING
                symbol = "+" if comparison['time_delta'] > 0 else ""
                print(f"  Time delta: {time_color}{symbol}{comparison['time_delta']}s ({symbol}{comparison['time_delta_percent']}%){Colors.ENDC}")

            if comparison['stats_changes']:
                print(f"\n  {Colors.BOLD}Statistics Changes:{Colors.ENDC}")
                for stat, change in comparison['stats_changes'].items():
                    print(f"    {stat}: {change['baseline']} → {change['current']} (Δ {change['delta']})")

            if comparison['new_warnings']:
                print(f"\n  {Colors.WARNING}New Warnings:{Colors.ENDC}")
                for warning in comparison['new_warnings']:
                    print(f"    - {warning}")

            if comparison['new_errors']:
                print(f"\n  {Colors.FAIL}New Errors:{Colors.ENDC}")
                for error in comparison['new_errors']:
                    print(f"    - {error}")

            if comparison['regression_detected']:
                print(f"\n{Colors.FAIL}{Colors.BOLD}⚠ REGRESSION DETECTED{Colors.ENDC}")
                return 1

        print(f"{Colors.HEADER}{'=' * 80}{Colors.ENDC}")

        return 0 if self.current_build.get("success") else 1

def main():
    parser = argparse.ArgumentParser(description="Monitor and validate build process")
    parser.add_argument('--baseline', action='store_true',
                       help='Save current build as baseline')
    parser.add_argument('--compare', action='store_true',
                       help='Compare with baseline')
    args = parser.parse_args()

    monitor = BuildMonitor()

    # Load baseline if comparing
    if args.compare:
        baseline = monitor.load_baseline()
        if not baseline:
            print(f"{Colors.WARNING}No baseline found. Run with --baseline first.{Colors.ENDC}")
            return 1

    # Run build
    monitor.run_build()

    # Save as baseline if requested
    if args.baseline:
        monitor.save_baseline()

    # Print report
    return monitor.print_build_report(compare=args.compare)

if __name__ == "__main__":
    sys.exit(main())
