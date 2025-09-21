#!/usr/bin/env python3
"""
SCRIPT: run_all_tests.py
PURPOSE: Run complete test suite with reporting
CATEGORY: validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T20:35:00-04:00

DESCRIPTION:
    Runs all test categories and generates a comprehensive test report.
    Includes unit tests, integration tests, and smoke tests.

LLM_USAGE:
    python scripts/run_all_tests.py [options]

ARGUMENTS:
    --verbose (bool): Verbose output
    --category (str): Run specific category only (unit|integration|smoke)

EXAMPLES:
    python scripts/run_all_tests.py
    python scripts/run_all_tests.py --verbose
    python scripts/run_all_tests.py --category unit

OUTPUT:
    - Test execution results
    - JSON test report in reports/test_report.json
    - Markdown report in reports/test_report.md

DEPENDENCIES:
    - Python 3.8+
    - pytest and related packages
    - scripts/lib/common.py

MANIFEST_REGISTRY: scripts/run_all_tests.py
"""

import subprocess
import json
from pathlib import Path
from datetime import datetime
import argparse
import sys

sys.path.append(str(Path(__file__).parent))
from lib.common import TimeManager, Logger

def run_test_category(category, verbose=False):
    """Run a specific category of tests"""

    logger = Logger.get_logger('TestRunner')
    logger.info(f"Running {category} tests...")

    cmd = [sys.executable, "-m", "pytest", f"tests/{category}/"]
    if verbose:
        cmd.append("-v")
    else:
        cmd.append("-q")

    # Add JSON report if available
    cmd.extend(["--json-report", "--json-report-file", f"reports/test_{category}.json"])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True
    )

    # Parse test output for summary
    output_lines = result.stdout.split('\n')
    summary_line = None
    for line in output_lines:
        if 'passed' in line or 'failed' in line:
            summary_line = line
            break

    return {
        "category": category,
        "passed": result.returncode == 0,
        "return_code": result.returncode,
        "output": result.stdout,
        "errors": result.stderr,
        "summary": summary_line or "No tests found"
    }

def generate_test_report(results):
    """Generate comprehensive test report"""

    time_mgr = TimeManager()
    logger = Logger.get_logger('TestRunner')

    report = {
        "timestamp": time_mgr.get_current_timestamp(),
        "summary": {
            "total_categories": len(results),
            "passed_categories": sum(1 for r in results if r["passed"]),
            "failed_categories": sum(1 for r in results if not r["passed"])
        },
        "details": results
    }

    # Generate markdown report
    markdown_report = f"""# Test Report

**Generated:** {report['timestamp']}

## Summary

- **Total Test Categories:** {report['summary']['total_categories']}
- **Passed:** {report['summary']['passed_categories']}
- **Failed:** {report['summary']['failed_categories']}

## Category Results

"""

    for result in results:
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        markdown_report += f"### {result['category'].title()} Tests: {status}\n\n"

        if result["summary"]:
            markdown_report += f"**Summary:** {result['summary']}\n\n"

        if not result["passed"] and result["errors"]:
            markdown_report += "**Errors:**\n```\n"
            markdown_report += result['errors'][:1000]
            if len(result['errors']) > 1000:
                markdown_report += "\n... (truncated)"
            markdown_report += "\n```\n\n"
        elif not result["passed"] and result["output"]:
            markdown_report += "**Output:**\n```\n"
            markdown_report += result['output'][:1000]
            if len(result['output']) > 1000:
                markdown_report += "\n... (truncated)"
            markdown_report += "\n```\n\n"

    markdown_report += """
## Test Coverage

To generate coverage report:
```bash
pytest --cov=scripts --cov-report=html --cov-report=term
```

## Next Steps

1. Fix any failing tests
2. Add more test coverage for uncovered code
3. Set up continuous integration to run tests automatically
4. Configure test reporting in GitHub Actions
"""

    # Save reports
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    # Save JSON report
    json_path = reports_dir / "test_report.json"
    json_path.write_text(json.dumps(report, indent=2))

    # Save markdown report
    md_path = reports_dir / "test_report.md"
    md_path.write_text(markdown_report)

    logger.info(f"Test reports saved to {json_path} and {md_path}")

    return report

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Run all tests")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--category", choices=["unit", "integration", "smoke"],
                       help="Run specific category only")

    args = parser.parse_args()

    logger = Logger.get_logger('TestRunner')
    logger.info("Starting Comprehensive Test Suite")

    # Check if pytest is installed
    try:
        result = subprocess.run([sys.executable, "-m", "pytest", "--version"], capture_output=True, text=True)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, result.args)
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.error("pytest is not installed. Install with: pip install -r tests/requirements-test.txt")
        sys.exit(1)

    # Determine which tests to run
    if args.category:
        categories = [args.category]
    else:
        categories = ["unit", "integration", "smoke"]

    # Run tests
    results = []
    for category in categories:
        # Check if test directory exists
        test_dir = Path(f"tests/{category}")
        if not test_dir.exists():
            logger.warning(f"Test directory {test_dir} does not exist, skipping")
            continue

        # Check if there are test files
        test_files = list(test_dir.glob("test_*.py"))
        if not test_files:
            logger.warning(f"No test files found in {test_dir}, skipping")
            continue

        result = run_test_category(category, args.verbose)
        results.append(result)

    if not results:
        logger.error("No tests were run")
        sys.exit(1)

    # Generate report
    report = generate_test_report(results)

    # Print summary
    print("\n" + "="*50)
    if report["summary"]["failed_categories"] == 0:
        print("✅ ALL TEST CATEGORIES PASSED!")
        print(f"   {report['summary']['passed_categories']} categories tested successfully")
        sys.exit(0)
    else:
        print(f"❌ {report['summary']['failed_categories']} test categories failed")
        print(f"   See reports/test_report.md for details")
        sys.exit(1)

if __name__ == "__main__":
    main()