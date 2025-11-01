#!/usr/bin/env -S uv run python3
"""
SCRIPT: link-monitor.py
PURPOSE: Link Monitor
CATEGORY: link_validation
LLM_READY: True
VERSION: 1.0.0
UPDATED: 2025-09-20T15:08:08-04:00

DESCRIPTION:
    Link Monitor. This script is part of the link validation
    category and provides automated functionality for the static site.

LLM_USAGE:
    python scripts/link-monitor.py [options]

ARGUMENTS:
    --help: Show help message
    --verbose: Enable verbose output
    [Additional arguments specific to this script]

EXAMPLES:
    # Basic usage
    python scripts/link-monitor.py

    # With verbose output
    python scripts/link-monitor.py --verbose

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

MANIFEST_REGISTRY: scripts/link-monitor.py
"""

import json
import asyncio
import aiohttp
from pathlib import Path
from typing import Dict, List, Set, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib
import argparse
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@dataclass
class LinkStatus:
    """Current status of a monitored link"""
    url: str
    last_check: str
    status: str  # healthy, degraded, broken
    response_time_ms: float
    consecutive_failures: int
    last_failure: Optional[str]
    notes: str

@dataclass
class MonitoringAlert:
    """Alert for link issues"""
    severity: str  # critical, warning, info
    url: str
    issue: str
    first_detected: str
    occurrences: int
    suggested_action: str

class LinkMonitor:
    """Monitors link health over time"""

    def __init__(self, config_file: Path = None):
        self.config = self._load_config(config_file)
        self.session = None
        self.link_status = {}
        self.alerts = []
        self.stats = {
            'checks_performed': 0,
            'healthy_links': 0,
            'degraded_links': 0,
            'broken_links': 0,
            'alerts_sent': 0
        }

    def _load_config(self, config_file: Path) -> Dict:
        """Load monitoring configuration"""
        default_config = {
            'check_interval_minutes': 60,
            'timeout_seconds': 10,
            'max_consecutive_failures': 3,
            'response_time_threshold_ms': 2000,
            'alert_email': None,
            'alert_webhook': None,
            'monitored_domains': [],
            'excluded_domains': ['localhost', '127.0.0.1'],
            'priority_urls': [],
            'state_file': 'link-monitor-state.json'
        }

        if config_file and config_file.exists():
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                default_config.update(user_config)

        return default_config

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self._load_state()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
        self._save_state()

    def _load_state(self):
        """Load previous monitoring state"""
        state_file = Path(self.config['state_file'])
        if state_file.exists():
            with open(state_file, 'r') as f:
                data = json.load(f)
                self.link_status = {
                    url: LinkStatus(**status)
                    for url, status in data.get('link_status', {}).items()
                }
                self.stats = data.get('stats', self.stats)

    def _save_state(self):
        """Save monitoring state"""
        state_file = Path(self.config['state_file'])
        data = {
            'link_status': {
                url: asdict(status)
                for url, status in self.link_status.items()
            },
            'stats': self.stats,
            'last_save': datetime.now().isoformat()
        }
        with open(state_file, 'w') as f:
            json.dump(data, f, indent=2)

    async def check_link(self, url: str) -> LinkStatus:
        """Check a single link's health"""
        start_time = asyncio.get_event_loop().time()
        status = self.link_status.get(url, LinkStatus(
            url=url,
            last_check=datetime.now().isoformat(),
            status='unknown',
            response_time_ms=0,
            consecutive_failures=0,
            last_failure=None,
            notes=''
        ))

        try:
            timeout = aiohttp.ClientTimeout(total=self.config['timeout_seconds'])
            async with self.session.get(url, timeout=timeout, allow_redirects=True) as response:
                response_time_ms = (asyncio.get_event_loop().time() - start_time) * 1000

                if response.status == 200:
                    if response_time_ms > self.config['response_time_threshold_ms']:
                        status.status = 'degraded'
                        status.notes = f"Slow response: {response_time_ms:.0f}ms"
                    else:
                        status.status = 'healthy'
                        status.notes = ''
                    status.consecutive_failures = 0
                else:
                    status.status = 'degraded'
                    status.notes = f"HTTP {response.status}"
                    status.consecutive_failures += 1

                status.response_time_ms = response_time_ms

        except asyncio.TimeoutError:
            status.status = 'degraded'
            status.notes = 'Timeout'
            status.consecutive_failures += 1
            status.last_failure = datetime.now().isoformat()
        except Exception as e:
            status.status = 'broken'
            status.notes = str(e)
            status.consecutive_failures += 1
            status.last_failure = datetime.now().isoformat()

        # Mark as broken if too many consecutive failures
        if status.consecutive_failures >= self.config['max_consecutive_failures']:
            status.status = 'broken'

        status.last_check = datetime.now().isoformat()
        self.link_status[url] = status
        self.stats['checks_performed'] += 1

        return status

    async def check_all_links(self, urls: List[str]) -> List[LinkStatus]:
        """Check all links concurrently"""
        # Prioritize certain URLs
        priority_urls = [u for u in urls if u in self.config.get('priority_urls', [])]
        regular_urls = [u for u in urls if u not in priority_urls]

        # Check priority URLs first
        priority_tasks = [self.check_link(url) for url in priority_urls]
        priority_results = await asyncio.gather(*priority_tasks)

        # Then check regular URLs
        regular_tasks = [self.check_link(url) for url in regular_urls]
        regular_results = await asyncio.gather(*regular_tasks)

        return priority_results + regular_results

    def analyze_results(self, results: List[LinkStatus]) -> List[MonitoringAlert]:
        """Analyze results and generate alerts"""
        alerts = []

        # Count statuses
        healthy = sum(1 for r in results if r.status == 'healthy')
        degraded = sum(1 for r in results if r.status == 'degraded')
        broken = sum(1 for r in results if r.status == 'broken')

        self.stats['healthy_links'] = healthy
        self.stats['degraded_links'] = degraded
        self.stats['broken_links'] = broken

        # Generate alerts
        for result in results:
            if result.status == 'broken':
                alert = MonitoringAlert(
                    severity='critical',
                    url=result.url,
                    issue=f"Link broken: {result.notes}",
                    first_detected=result.last_failure or datetime.now().isoformat(),
                    occurrences=result.consecutive_failures,
                    suggested_action="Investigate and repair or remove link"
                )
                alerts.append(alert)

            elif result.status == 'degraded':
                if result.consecutive_failures >= 2:
                    alert = MonitoringAlert(
                        severity='warning',
                        url=result.url,
                        issue=f"Link degraded: {result.notes}",
                        first_detected=result.last_failure or datetime.now().isoformat(),
                        occurrences=result.consecutive_failures,
                        suggested_action="Monitor closely, may become broken"
                    )
                    alerts.append(alert)

                elif result.response_time_ms > self.config['response_time_threshold_ms'] * 2:
                    alert = MonitoringAlert(
                        severity='warning',
                        url=result.url,
                        issue=f"Very slow response: {result.response_time_ms:.0f}ms",
                        first_detected=datetime.now().isoformat(),
                        occurrences=1,
                        suggested_action="Consider caching or finding alternative"
                    )
                    alerts.append(alert)

        self.alerts = alerts
        return alerts

    async def send_alerts(self, alerts: List[MonitoringAlert]):
        """Send alerts via configured channels"""
        if not alerts:
            return

        critical_alerts = [a for a in alerts if a.severity == 'critical']
        warning_alerts = [a for a in alerts if a.severity == 'warning']

        # Generate alert message
        message = self._format_alert_message(critical_alerts, warning_alerts)

        # Send email if configured
        if self.config.get('alert_email'):
            await self._send_email_alert(message)

        # Send webhook if configured
        if self.config.get('alert_webhook'):
            await self._send_webhook_alert(message)

        self.stats['alerts_sent'] += len(alerts)

    def _format_alert_message(self, critical: List[MonitoringAlert],
                             warnings: List[MonitoringAlert]) -> str:
        """Format alert message"""
        lines = []
        lines.append("# Link Monitoring Alert")
        lines.append(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Monitored: {len(self.link_status)}")
        lines.append(f"Healthy: {self.stats['healthy_links']}")
        lines.append(f"Degraded: {self.stats['degraded_links']}")
        lines.append(f"Broken: {self.stats['broken_links']}")

        if critical:
            lines.append(f"\n## Critical Alerts ({len(critical)})")
            for alert in critical[:10]:  # Limit to 10
                lines.append(f"\n- **{alert.url}**")
                lines.append(f"  Issue: {alert.issue}")
                lines.append(f"  Action: {alert.suggested_action}")

        if warnings:
            lines.append(f"\n## Warnings ({len(warnings)})")
            for alert in warnings[:10]:  # Limit to 10
                lines.append(f"\n- {alert.url}")
                lines.append(f"  Issue: {alert.issue}")

        return '\n'.join(lines)

    async def _send_email_alert(self, message: str):
        """Send email alert"""
        # Implementation depends on email configuration
        print(f"Email alert would be sent to: {self.config['alert_email']}")
        print(message)

    async def _send_webhook_alert(self, message: str):
        """Send webhook alert"""
        webhook_url = self.config['alert_webhook']
        if webhook_url:
            try:
                async with self.session.post(webhook_url, json={'text': message}) as response:
                    if response.status == 200:
                        print("Webhook alert sent successfully")
            except Exception as e:
                print(f"Failed to send webhook: {e}")

    def generate_report(self, output_file: Path):
        """Generate monitoring report"""
        report = {
            'generated': datetime.now().isoformat(),
            'stats': self.stats,
            'link_status_summary': {
                'healthy': [],
                'degraded': [],
                'broken': []
            },
            'alerts': [asdict(a) for a in self.alerts],
            'response_times': {}
        }

        # Categorize links
        for url, status in self.link_status.items():
            status_dict = asdict(status)
            if status.status == 'healthy':
                report['link_status_summary']['healthy'].append(url)
            elif status.status == 'degraded':
                report['link_status_summary']['degraded'].append(status_dict)
            else:
                report['link_status_summary']['broken'].append(status_dict)

            if status.response_time_ms > 0:
                report['response_times'][url] = status.response_time_ms

        # Write report
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        # Also create markdown report
        md_file = output_file.with_suffix('.md')
        self._generate_markdown_report(report, md_file)

    def _generate_markdown_report(self, report: Dict, output_file: Path):
        """Generate markdown monitoring report"""
        lines = []
        lines.append("# Link Monitoring Report")
        lines.append(f"\n**Generated:** {report['generated']}")
        lines.append("\n## Summary Statistics")
        lines.append(f"- **Checks Performed:** {report['stats']['checks_performed']}")
        lines.append(f"- **Healthy Links:** {report['stats']['healthy_links']}")
        lines.append(f"- **Degraded Links:** {report['stats']['degraded_links']}")
        lines.append(f"- **Broken Links:** {report['stats']['broken_links']}")
        lines.append(f"- **Alerts Sent:** {report['stats']['alerts_sent']}")

        if report['link_status_summary']['broken']:
            lines.append("\n## Broken Links (Requires Immediate Attention)")
            for item in report['link_status_summary']['broken']:
                lines.append(f"\n### {item['url']}")
                lines.append(f"- **Status:** {item['status']}")
                lines.append(f"- **Issue:** {item['notes']}")
                lines.append(f"- **Consecutive Failures:** {item['consecutive_failures']}")
                lines.append(f"- **Last Check:** {item['last_check']}")

        if report['link_status_summary']['degraded']:
            lines.append("\n## Degraded Links (Monitor Closely)")
            for item in report['link_status_summary']['degraded'][:20]:
                lines.append(f"- {item['url']}: {item['notes']}")

        # Top slow links
        if report['response_times']:
            lines.append("\n## Slowest Links")
            sorted_times = sorted(report['response_times'].items(),
                                key=lambda x: x[1], reverse=True)[:10]
            for url, time_ms in sorted_times:
                lines.append(f"- {url}: {time_ms:.0f}ms")

        with open(output_file, 'w') as f:
            f.write('\n'.join(lines))

async def continuous_monitor(monitor: LinkMonitor, urls: List[str],
                            interval_minutes: int):
    """Run continuous monitoring"""
    print(f"Starting continuous monitoring of {len(urls)} links")
    print(f"Check interval: {interval_minutes} minutes")

    while True:
        print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running checks...")

        # Check all links
        results = await monitor.check_all_links(urls)

        # Analyze and generate alerts
        alerts = monitor.analyze_results(results)

        # Send alerts if any
        if alerts:
            print(f"Found {len(alerts)} alerts")
            await monitor.send_alerts(alerts)

        # Save state
        monitor._save_state()

        # Generate report
        report_file = Path(f"monitoring-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json")
        monitor.generate_report(report_file)
        print(f"Report saved to {report_file}")

        # Wait for next check
        print(f"Next check in {interval_minutes} minutes...")
        await asyncio.sleep(interval_minutes * 60)

async def main():
    parser = argparse.ArgumentParser(description='Monitor link health continuously')
    parser.add_argument('--links', type=Path, default=Path('links.json'),
                       help='JSON file with links to monitor')
    parser.add_argument('--config', type=Path, default=Path('monitor-config.json'),
                       help='Monitor configuration file')
    parser.add_argument('--interval', type=int, default=60,
                       help='Check interval in minutes')
    parser.add_argument('--once', action='store_true',
                       help='Run once and exit')
    parser.add_argument('--output', type=Path, default=Path('monitoring-report.json'),
                       help='Output report file')

    args = parser.parse_args()

    # Load links
    if not args.links.exists():
        print(f"Links file not found: {args.links}")
        return 1

    with open(args.links, 'r') as f:
        links_data = json.load(f)
        urls = list(set(link['url'] for link in links_data.get('links', [])))

    print(f"Loaded {len(urls)} unique URLs to monitor")

    # Run monitor
    async with LinkMonitor(args.config) as monitor:
        if args.once:
            # Single run
            results = await monitor.check_all_links(urls)
            alerts = monitor.analyze_results(results)
            if alerts:
                await monitor.send_alerts(alerts)
            monitor.generate_report(args.output)
            print(f"Report saved to {args.output}")
        else:
            # Continuous monitoring
            await continuous_monitor(monitor, urls, args.interval)

    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))