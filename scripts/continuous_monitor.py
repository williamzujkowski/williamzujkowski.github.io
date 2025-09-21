#!/usr/bin/env python3
"""
SCRIPT: continuous_monitor.py
PURPOSE: Main continuous monitoring orchestrator
CATEGORY: monitoring
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T22:12:00-04:00

DESCRIPTION:
    Orchestrates continuous monitoring tasks including hourly checks,
    daily monitoring, and weekly summaries. Can run as a daemon or
    execute specific monitoring tasks.

LLM_USAGE:
    python scripts/continuous_monitor.py [options]

ARGUMENTS:
    --mode (str): Run mode (daemon|hourly|daily|weekly), default: daemon
    --once (bool): Run once and exit instead of continuous loop

EXAMPLES:
    # Run as daemon
    python scripts/continuous_monitor.py

    # Run hourly checks once
    python scripts/continuous_monitor.py --mode hourly --once

    # Run daily monitoring
    python scripts/continuous_monitor.py --mode daily --once

OUTPUT:
    - Monitoring logs to console
    - Reports in reports/ directory

DEPENDENCIES:
    - Python 3.8+
    - schedule package (optional for daemon mode)

MANIFEST_REGISTRY: scripts/continuous_monitor.py
"""

import subprocess
from pathlib import Path
import sys
import time
import argparse
sys.path.append(str(Path(__file__).parent))
from lib.common import Logger

class ContinuousMonitor:
    """Orchestrate continuous monitoring tasks"""

    def __init__(self):
        self.logger = Logger.get_logger('ContinuousMonitor')

    def run_hourly_checks(self):
        """Run quick health checks every hour"""
        self.logger.info("Running hourly checks...")

        checks = []

        # Check MANIFEST.json validity
        try:
            result = subprocess.run(
                ["python", "scripts/update_manifest.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            checks.append(("MANIFEST update", result.returncode == 0))
        except Exception as e:
            self.logger.error(f"MANIFEST check failed: {e}")
            checks.append(("MANIFEST update", False))

        # Check for duplicates
        try:
            result = subprocess.run(
                ["python", "scripts/check_duplicates.py"],
                capture_output=True,
                text=True,
                timeout=30
            )
            checks.append(("Duplicate check", result.returncode == 0))
        except Exception as e:
            self.logger.error(f"Duplicate check failed: {e}")
            checks.append(("Duplicate check", False))

        # Report results
        passed = sum(1 for _, status in checks if status)
        self.logger.info(f"Hourly checks complete: {passed}/{len(checks)} passed")
        return checks

    def run_daily_monitoring(self):
        """Run comprehensive daily monitoring"""
        self.logger.info("Running daily monitoring...")

        tasks = []

        # Generate health dashboard
        try:
            result = subprocess.run(
                ["python", "scripts/generate_health_dashboard.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            tasks.append(("Health dashboard", result.returncode == 0))
            self.logger.info("Health dashboard generated")
        except Exception as e:
            self.logger.error(f"Health dashboard failed: {e}")
            tasks.append(("Health dashboard", False))

        # Run tests
        try:
            result = subprocess.run(
                ["python", "scripts/run_all_tests.py"],
                capture_output=True,
                text=True,
                timeout=120
            )
            tasks.append(("Test suite", result.returncode == 0))
            self.logger.info("Test suite completed")
        except Exception as e:
            self.logger.error(f"Test suite failed: {e}")
            tasks.append(("Test suite", False))

        # Run vestigial audit
        try:
            result = subprocess.run(
                ["python", "scripts/vestigial_audit.py", "--report"],
                capture_output=True,
                text=True,
                timeout=60
            )
            tasks.append(("Vestigial audit", result.returncode == 0))
            self.logger.info("Vestigial audit completed")
        except Exception as e:
            self.logger.error(f"Vestigial audit failed: {e}")
            tasks.append(("Vestigial audit", False))

        # Generate compliance report
        try:
            result = subprocess.run(
                ["python", "scripts/generate_compliance_report.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            tasks.append(("Compliance report", result.returncode == 0))
            self.logger.info("Compliance report generated")
        except Exception as e:
            self.logger.error(f"Compliance report failed: {e}")
            tasks.append(("Compliance report", False))

        # Report results
        passed = sum(1 for _, status in tasks if status)
        self.logger.info(f"Daily monitoring complete: {passed}/{len(tasks)} tasks succeeded")
        return tasks

    def run_weekly_summary(self):
        """Generate weekly summary"""
        self.logger.info("Generating weekly summary...")

        try:
            result = subprocess.run(
                ["python", "scripts/generate_weekly_summary.py"],
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                self.logger.info("Weekly summary generated successfully")
                return True
            else:
                self.logger.error("Weekly summary generation failed")
                return False
        except Exception as e:
            self.logger.error(f"Weekly summary failed: {e}")
            return False

    def run_daemon(self):
        """Run as a daemon with scheduled tasks"""
        self.logger.info("Starting Continuous Monitoring System in daemon mode")

        try:
            import schedule

            # Schedule tasks
            schedule.every().hour.do(self.run_hourly_checks)
            schedule.every().day.at("02:00").do(self.run_daily_monitoring)
            schedule.every().monday.at("09:00").do(self.run_weekly_summary)

            # Run initial check
            self.run_hourly_checks()

            self.logger.info("Monitoring daemon started. Press Ctrl+C to stop.")

            # Keep running
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except ImportError:
            self.logger.error("schedule package not installed. Install with: pip install schedule")
            self.logger.info("Running single check instead...")
            self.run_hourly_checks()
        except KeyboardInterrupt:
            self.logger.info("Monitoring daemon stopped by user")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Continuous monitoring orchestrator")
    parser.add_argument("--mode", choices=["daemon", "hourly", "daily", "weekly"],
                       default="daemon", help="Run mode")
    parser.add_argument("--once", action="store_true",
                       help="Run once and exit instead of continuous loop")

    args = parser.parse_args()

    monitor = ContinuousMonitor()

    if args.mode == "hourly":
        monitor.run_hourly_checks()
    elif args.mode == "daily":
        monitor.run_daily_monitoring()
    elif args.mode == "weekly":
        monitor.run_weekly_summary()
    elif args.mode == "daemon":
        if args.once:
            monitor.logger.info("Running single monitoring cycle")
            monitor.run_hourly_checks()
        else:
            monitor.run_daemon()

if __name__ == "__main__":
    main()