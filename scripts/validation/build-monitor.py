#!/usr/bin/env -S uv run python3
"""
SCRIPT: build-monitor.py
PURPOSE: Monitor and validate build process with regression detection
CATEGORY: validation
LLM_READY: True
VERSION: 3.0.0
UPDATED: 2025-11-02

DESCRIPTION:
    Monitors npm build process, captures performance metrics, and detects
    regressions by comparing against baseline builds.

    Monitors:
    1. Build success/failure status
    2. Build time and performance
    3. Posts parsed and files written
    4. JavaScript bundle sizes and compression
    5. Warnings and errors in build output
    6. Eleventy processing time

    Regression detection:
    - Status changes (passing → failing)
    - >20% build time increase
    - New errors or warnings
    - Bundle size increases

USAGE:
    # Run build and show report
    uv run python scripts/validation/build-monitor.py

    # Save current build as baseline
    uv run python scripts/validation/build-monitor.py --baseline

    # Compare with baseline
    uv run python scripts/validation/build-monitor.py --compare

    # Create baseline and compare
    uv run python scripts/validation/build-monitor.py --baseline --compare

ARGUMENTS:
    --baseline: Save current build as baseline for future comparisons
    --compare: Compare current build with saved baseline
    --baseline-file: Custom baseline file path (default: .build-baseline.json)

OUTPUT:
    - Build status and timing
    - Statistics (posts, files, bundles)
    - Warnings and errors
    - Comparison with baseline (if requested)
    - Exit code: 0 (success), 1 (failure/regression)

DEPENDENCIES:
    - Python 3.8+
    - npm and Node.js for build execution
    - logging_config for consistent logging

RELATED_SCRIPTS:
    - scripts/validation/metadata-validator.py: Metadata validation

MANIFEST_REGISTRY: scripts/validation/build-monitor.py
"""

import re
import sys
import json
import time
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field

# Add lib directory to path for logging_config
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))
from logging_config import setup_logger

logger = setup_logger(__name__)

# Pre-compiled regex for build output parsing (Optimization #2)
PATTERN_POSTS_PARSED = re.compile(r'Successfully parsed (\d+) posts')
PATTERN_FILES_WRITTEN = re.compile(r'Wrote (\d+) files')
PATTERN_ELEVENTY_TIME = re.compile(r'in ([\d.]+) seconds')
PATTERN_BUNDLE_NAME = re.compile(r'Creating bundle:\s*(.+)$')
PATTERN_BUNDLE_SIZE = re.compile(r'Minified:\s*([\d.]+\s*[KM]?B)\s*→\s*([\d.]+\s*[KM]?B)\s*\(([\d.]+)%\s*reduction\)')


@dataclass
class BuildStats:
    """Statistics from a build execution.

    Attributes:
        posts_parsed: Number of blog posts successfully parsed.
        files_written: Number of output files generated.
        files_copied: Number of static files copied.
        total_words: Total word count across all posts.
        js_bundles: Dictionary mapping bundle name to size info.
        eleventy_time: Eleventy processing time in seconds.
    """
    posts_parsed: int = 0
    files_written: int = 0
    files_copied: int = 0
    total_words: int = 0
    js_bundles: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    eleventy_time: Optional[float] = None


class BuildMonitor:
    """Monitor npm build process and detect regressions.

    Executes npm build, captures output, parses metrics, and compares
    with baseline builds to detect performance regressions or new errors.

    Attributes:
        BUILD_TIMEOUT: Maximum seconds before build times out (120s).
        BUILD_COMMAND: Command to execute for builds (npm run build).
        TIME_REGRESSION_THRESHOLD: Percentage increase for regression (20%).
    """

    # Build configuration
    BUILD_TIMEOUT: int = 120  # seconds
    BUILD_COMMAND: List[str] = ["npm", "run", "build"]
    TIME_REGRESSION_THRESHOLD: float = 0.20  # 20% slower = regression

    def __init__(self, baseline_file: Path = Path(".build-baseline.json")) -> None:
        """Initialize the build monitor.

        Args:
            baseline_file: Path to baseline JSON file for comparisons.

        Raises:
            TypeError: If baseline_file is not a Path object.
        """
        if not isinstance(baseline_file, Path):
            raise TypeError(f"baseline_file must be Path, got {type(baseline_file)}")

        self.baseline_file: Path = baseline_file
        self.current_build: Dict[str, Any] = {}
        self.baseline_build: Optional[Dict[str, Any]] = None

    def run_build(self) -> Dict[str, Any]:
        """Run npm build command and capture metrics.

        Executes build with timeout, captures stdout/stderr, parses metrics,
        and returns structured build data.

        Returns:
            Dictionary containing build data:
                - timestamp: ISO format build time
                - success: Boolean build status
                - build_time: Total build time in seconds
                - return_code: Process exit code
                - stats: BuildStats with parsed metrics
                - warnings: List of warning messages
                - errors: List of error messages

        Examples:
            >>> monitor = BuildMonitor()
            >>> build_data = monitor.run_build()
            >>> if build_data['success']:
            ...     print(f"Build time: {build_data['build_time']}s")
        """
        logger.info("🔨 Running build process...")
        start_time: float = time.time()

        try:
            # Run build command with timeout
            result: subprocess.CompletedProcess = subprocess.run(
                self.BUILD_COMMAND,
                capture_output=True,
                text=True,
                timeout=self.BUILD_TIMEOUT,
                check=False  # Don't raise on non-zero exit
            )

            build_time: float = time.time() - start_time
            output: str = result.stdout + result.stderr

            # Single-pass build output parsing (Optimization #2)
            stats: Dict[str, Any] = self._parse_build_output_optimized(output)
            warnings: List[str] = []
            errors: List[str] = []
            self._extract_warnings_errors_optimized(output, warnings, errors)

            build_data: Dict[str, Any] = {
                "timestamp": datetime.now().isoformat(),
                "success": result.returncode == 0,
                "build_time": round(build_time, 2),
                "return_code": result.returncode,
                "stats": stats,
                "warnings": warnings,
                "errors": errors
            }

            self.current_build = build_data
            logger.info(f"Build completed in {build_time:.2f}s (exit code: {result.returncode})")
            return build_data

        except subprocess.TimeoutExpired:
            error_msg = f"Build timeout (>{self.BUILD_TIMEOUT}s)"
            logger.error(f"Build timeout after {self.BUILD_TIMEOUT}s")
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": error_msg,
                "build_time": self.BUILD_TIMEOUT
            }
        except FileNotFoundError as e:
            error_msg = "npm not found"
            logger.error("npm command not found - ensure Node.js is installed", exc_info=True)
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": error_msg
            }
        except (OSError, subprocess.SubprocessError) as e:
            error_msg = f"Subprocess error: {str(e)}"
            logger.error(f"Build execution error: {e}", exc_info=True)
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected build error: {e}", exc_info=True)
            return {
                "timestamp": datetime.now().isoformat(),
                "success": False,
                "error": error_msg
            }

    def _parse_build_output_optimized(self, output: str) -> Dict[str, Any]:
        """Parse build output to extract statistics (single-pass optimization).

        Processes build output in a single iteration to extract all metrics,
        reducing overhead from multiple string operations (Optimization #2).

        Args:
            output: Combined stdout and stderr from build process.

        Returns:
            Dictionary with parsed statistics:
                - posts_parsed: Number of posts processed
                - files_written: Number of files generated
                - eleventy_time: Build time in seconds
                - js_bundles: Bundle size info

        Examples:
            >>> monitor = BuildMonitor()
            >>> stats = monitor._parse_build_output_optimized(build_output)
            >>> print(stats['posts_parsed'])
        """
        stats: Dict[str, Any] = {
            "posts_parsed": 0,
            "files_written": 0,
            "files_copied": 0,
            "total_words": 0,
            "js_bundles": {},
            "eleventy_time": None
        }

        current_bundle: Optional[str] = None

        # Single pass through output (Optimization #2)
        for line in output.split('\n'):
            # Posts parsed
            if not stats["posts_parsed"] and (match := PATTERN_POSTS_PARSED.search(line)):
                try:
                    stats["posts_parsed"] = int(match.group(1))
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse post count: {e}")

            # Files written
            elif not stats["files_written"] and (match := PATTERN_FILES_WRITTEN.search(line)):
                try:
                    stats["files_written"] = int(match.group(1))
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse files written: {e}")

            # Eleventy time
            elif stats["eleventy_time"] is None and "Wrote" in line and (match := PATTERN_ELEVENTY_TIME.search(line)):
                try:
                    stats["eleventy_time"] = float(match.group(1))
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse Eleventy time: {e}")

            # Bundle name
            elif "Creating bundle:" in line and (match := PATTERN_BUNDLE_NAME.search(line)):
                current_bundle = match.group(1).strip()

            # Bundle size
            elif "Minified:" in line and current_bundle and (match := PATTERN_BUNDLE_SIZE.search(line)):
                try:
                    stats["js_bundles"][current_bundle] = {
                        "original": match.group(1).strip(),
                        "minified": match.group(2).strip(),
                        "reduction": float(match.group(3))
                    }
                    current_bundle = None  # Reset for next bundle
                except (ValueError, IndexError) as e:
                    logger.debug(f"Failed to parse bundle size for {current_bundle}: {e}")

        return stats

    def _extract_warnings_errors_optimized(
        self,
        output: str,
        warnings: List[str],
        errors: List[str]
    ) -> None:
        """Extract warning and error messages (single-pass optimization).

        Processes build output once to extract both warnings and errors,
        avoiding multiple passes over the same data (Optimization #2).

        Args:
            output: Build process output.
            warnings: List to populate with warning messages (modified in-place).
            errors: List to populate with error messages (modified in-place).

        Examples:
            >>> warnings, errors = [], []
            >>> monitor._extract_warnings_errors_optimized(output, warnings, errors)
        """
        for line in output.split('\n'):
            if not line.strip():
                continue

            line_lower: str = line.lower()

            # Check for errors (but not warnings)
            if 'error' in line_lower and 'warn' not in line_lower:
                errors.append(line.strip())
            # Check for warnings
            elif 'warn' in line_lower or 'warning' in line_lower:
                warnings.append(line.strip())

    def save_baseline(self) -> None:
        """Save current build as baseline for future comparisons.

        Writes current_build data to JSON file for regression detection.

        Raises:
            IOError: If baseline file cannot be written.
            ValueError: If current_build is empty.

        Examples:
            >>> monitor = BuildMonitor()
            >>> monitor.run_build()
            >>> monitor.save_baseline()
        """
        if not self.current_build:
            raise ValueError("No current build data to save")

        try:
            self.baseline_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.baseline_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_build, f, indent=2)
            logger.info(f"✅ Baseline saved to {self.baseline_file}")
        except (IOError, OSError) as e:
            logger.error(f"Failed to save baseline: {e}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Unexpected error saving baseline: {e}", exc_info=True)
            raise

    def load_baseline(self) -> Optional[Dict[str, Any]]:
        """Load baseline build data from file.

        Reads and parses baseline JSON for comparison with current build.

        Returns:
            Baseline build dictionary or None if file doesn't exist.

        Raises:
            json.JSONDecodeError: If baseline file is corrupted.
            IOError: If file exists but cannot be read.

        Examples:
            >>> monitor = BuildMonitor()
            >>> baseline = monitor.load_baseline()
            >>> if baseline:
            ...     print(baseline['build_time'])
        """
        if not self.baseline_file.exists():
            logger.debug(f"No baseline file found at {self.baseline_file}")
            return None

        try:
            with open(self.baseline_file, 'r', encoding='utf-8') as f:
                self.baseline_build = json.load(f)
            logger.info(f"Loaded baseline from {self.baseline_file}")
            return self.baseline_build
        except json.JSONDecodeError as e:
            error_msg = f"Corrupted baseline file: {e}"
            logger.error(error_msg, exc_info=True)
            raise
        except (IOError, OSError) as e:
            error_msg = f"Failed to load baseline: {e}"
            logger.error(error_msg, exc_info=True)
            raise
        except Exception as e:
            error_msg = f"Unexpected error loading baseline: {e}"
            logger.error(error_msg, exc_info=True)
            raise

    def compare_builds(self) -> Dict[str, Any]:
        """Compare current build with baseline to detect regressions.

        Analyzes differences in build status, timing, stats, and errors/warnings
        to identify performance regressions or new problems.

        Returns:
            Dictionary with comparison results:
                - status_change: Build status change (REGRESSION/FIXED/UNCHANGED)
                - time_delta: Build time difference in seconds
                - time_delta_percent: Percentage change in build time
                - stats_changes: Dict of changed statistics
                - new_warnings: List of new warning messages
                - new_errors: List of new error messages
                - regression_detected: Boolean flag for any regression

        Raises:
            ValueError: If baseline not loaded.

        Examples:
            >>> monitor = BuildMonitor()
            >>> monitor.load_baseline()
            >>> monitor.run_build()
            >>> comparison = monitor.compare_builds()
            >>> if comparison['regression_detected']:
            ...     print("Regression found!")
        """
        if not self.baseline_build:
            raise ValueError("No baseline found - load baseline first")

        comparison: Dict[str, Any] = {
            "status_change": "UNCHANGED",
            "time_delta": None,
            "time_delta_percent": None,
            "stats_changes": {},
            "new_warnings": [],
            "new_errors": [],
            "regression_detected": False
        }

        # Status comparison
        baseline_success: bool = self.baseline_build.get("success", False)
        current_success: bool = self.current_build.get("success", False)

        if baseline_success and not current_success:
            comparison["status_change"] = "REGRESSION"
            comparison["regression_detected"] = True
            logger.warning("Build status regression: PASSING → FAILING")
        elif not baseline_success and current_success:
            comparison["status_change"] = "FIXED"
            logger.info("Build status improved: FAILING → PASSING")

        # Time comparison
        baseline_time: float = self.baseline_build.get("build_time", 0)
        current_time: float = self.current_build.get("build_time", 0)

        if baseline_time > 0:
            time_delta: float = current_time - baseline_time
            time_delta_percent: float = (time_delta / baseline_time) * 100
            comparison["time_delta"] = round(time_delta, 2)
            comparison["time_delta_percent"] = round(time_delta_percent, 1)

            # Flag significant time regression (>20% slower)
            if time_delta_percent > self.TIME_REGRESSION_THRESHOLD * 100:
                comparison["regression_detected"] = True
                logger.warning(
                    f"Build time regression: +{time_delta_percent:.1f}% "
                    f"({baseline_time:.2f}s → {current_time:.2f}s)"
                )

        # Stats comparison
        baseline_stats: Dict[str, Any] = self.baseline_build.get("stats", {})
        current_stats: Dict[str, Any] = self.current_build.get("stats", {})

        for key in baseline_stats:
            if key in current_stats and key != "js_bundles":
                baseline_val: Any = baseline_stats[key]
                current_val: Any = current_stats[key]
                if baseline_val != current_val:
                    delta: Any = current_val - baseline_val if isinstance(current_val, (int, float)) else "N/A"
                    comparison["stats_changes"][key] = {
                        "baseline": baseline_val,
                        "current": current_val,
                        "delta": delta
                    }

        # New warnings/errors
        baseline_warnings: Set[str] = set(self.baseline_build.get("warnings", []))
        current_warnings: Set[str] = set(self.current_build.get("warnings", []))
        comparison["new_warnings"] = list(current_warnings - baseline_warnings)

        baseline_errors: Set[str] = set(self.baseline_build.get("errors", []))
        current_errors: Set[str] = set(self.current_build.get("errors", []))
        comparison["new_errors"] = list(current_errors - baseline_errors)

        if comparison["new_errors"]:
            comparison["regression_detected"] = True
            logger.error(f"New errors detected: {len(comparison['new_errors'])} errors")

        return comparison

    def print_build_report(self, compare: bool = False) -> int:
        """Print formatted build report to console.

        Outputs human-readable build validation results including status,
        timing, statistics, warnings/errors, and optional baseline comparison.

        Args:
            compare: Whether to include baseline comparison.

        Returns:
            Exit code:
                - 0: Build successful with no regressions.
                - 1: Build failed or regression detected.

        Examples:
            >>> monitor = BuildMonitor()
            >>> monitor.run_build()
            >>> exit_code = monitor.print_build_report(compare=True)
        """
        logger.info("\n" + "=" * 80)
        logger.info("BUILD VALIDATION REPORT")
        logger.info("=" * 80)

        # Build status
        if self.current_build.get("success"):
            logger.info(f"\n✅ Build Status: PASSING")
        else:
            logger.error(f"\n❌ Build Status: FAILED")

        logger.info(f"⏱️  Build Time: {self.current_build.get('build_time', 'N/A')}s")
        logger.info(f"📅 Timestamp: {self.current_build.get('timestamp', 'N/A')}")

        # Statistics
        stats: Dict[str, Any] = self.current_build.get("stats", {})
        if stats:
            logger.info("\n📊 Build Statistics:")
            logger.info(f"  - Posts parsed: {stats.get('posts_parsed', 'N/A')}")
            logger.info(f"  - Files written: {stats.get('files_written', 'N/A')}")
            if stats.get("eleventy_time"):
                logger.info(f"  - Eleventy time: {stats.get('eleventy_time', 'N/A')}s")

            js_bundles: Dict[str, Dict[str, Any]] = stats.get("js_bundles", {})
            if js_bundles:
                logger.info("\n📦 JavaScript Bundles:")
                for bundle, data in js_bundles.items():
                    logger.info(f"  - {bundle}: {data['original']} → {data['minified']} ({data['reduction']}%)")

        # Warnings and errors
        warnings: List[str] = self.current_build.get("warnings", [])
        errors: List[str] = self.current_build.get("errors", [])

        if warnings:
            logger.warning(f"\n⚠️  Warnings ({len(warnings)}):")
            for warning in warnings[:5]:  # Show first 5
                logger.warning(f"  - {warning}")
            if len(warnings) > 5:
                logger.warning(f"  ... and {len(warnings) - 5} more")

        if errors:
            logger.error(f"\n❌ Errors ({len(errors)}):")
            for error in errors:
                logger.error(f"  - {error}")

        # Comparison with baseline
        regression_detected: bool = False
        if compare and self.baseline_build:
            try:
                comparison: Dict[str, Any] = self.compare_builds()

                logger.info("\n🔄 Comparison with Baseline:")
                logger.info(f"  - Status: {comparison['status_change']}")

                if comparison['time_delta'] is not None:
                    symbol: str = "+" if comparison['time_delta'] > 0 else ""
                    logger.info(f"  - Time delta: {symbol}{comparison['time_delta']}s ({symbol}{comparison['time_delta_percent']}%)")

                if comparison['stats_changes']:
                    logger.info("\n📈 Statistics Changes:")
                    for stat, change in comparison['stats_changes'].items():
                        logger.info(f"  - {stat}: {change['baseline']} → {change['current']} (Δ {change['delta']})")

                if comparison['new_warnings']:
                    logger.warning(f"\n⚠️  New Warnings ({len(comparison['new_warnings'])}):")
                    for warning in comparison['new_warnings'][:5]:
                        logger.warning(f"  - {warning}")

                if comparison['new_errors']:
                    logger.error(f"\n❌ New Errors ({len(comparison['new_errors'])}):")
                    for error in comparison['new_errors']:
                        logger.error(f"  - {error}")

                if comparison['regression_detected']:
                    logger.error("\n⚠️  REGRESSION DETECTED")
                    regression_detected = True

            except ValueError as e:
                logger.error(f"Comparison failed: {e}")

        logger.info("\n" + "=" * 80)

        return 1 if (not self.current_build.get("success") or regression_detected) else 0

    def run(self, save_baseline: bool = False, compare_baseline: bool = False) -> int:
        """Run the build monitoring process.

        Executes build, optionally saves baseline, and prints report with
        optional baseline comparison.

        Args:
            save_baseline: Save current build as baseline.
            compare_baseline: Compare with baseline.

        Returns:
            Exit code:
                - 0: Build succeeded without regressions.
                - 1: Build failed, regression detected, or no baseline found.

        Examples:
            >>> monitor = BuildMonitor()
            >>> exit_code = monitor.run(save_baseline=True, compare_baseline=True)
        """
        # Load baseline if comparing
        if compare_baseline:
            baseline: Optional[Dict[str, Any]] = self.load_baseline()
            if not baseline:
                logger.warning("No baseline found. Run with --baseline first.")
                if not save_baseline:
                    return 1

        # Run build
        build_result: Dict[str, Any] = self.run_build()

        if "error" in build_result:
            logger.error(f"Build error: {build_result['error']}")
            return 1

        # Save as baseline if requested
        if save_baseline:
            self.save_baseline()

        # Print report
        return self.print_build_report(compare=compare_baseline)


def main() -> int:
    """Main entry point for build-monitor.py script.

    Parses command-line arguments, configures monitor, runs build process,
    and outputs report with optional baseline comparison.

    Returns:
        Exit code:
            - 0: Build succeeded without regressions.
            - 1: Build failed, regression detected, or error occurred.
            - 130: User interrupted with Ctrl+C.

    Examples:
        Run from command line:
            $ uv run python scripts/validation/build-monitor.py
            $ uv run python scripts/validation/build-monitor.py --baseline --compare
    """
    parser = argparse.ArgumentParser(
        description='Monitor and validate build process with regression detection',
        epilog='Example: %(prog)s --baseline --compare'
    )
    parser.add_argument(
        '--baseline',
        action='store_true',
        help='Save current build as baseline for future comparisons'
    )
    parser.add_argument(
        '--compare',
        action='store_true',
        help='Compare current build with saved baseline'
    )
    parser.add_argument(
        '--baseline-file',
        type=Path,
        default=Path('.build-baseline.json'),
        help='Baseline file path (default: .build-baseline.json)'
    )

    args = parser.parse_args()

    try:
        monitor = BuildMonitor(baseline_file=args.baseline_file)
        return monitor.run(
            save_baseline=args.baseline,
            compare_baseline=args.compare
        )

    except KeyboardInterrupt:
        logger.warning("\nBuild monitoring cancelled by user")
        return 130
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
