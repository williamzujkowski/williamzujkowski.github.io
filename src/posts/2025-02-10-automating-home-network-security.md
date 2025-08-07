---
title: "Automating Home Network Security with Python and Open Source Tools"
date: 2025-02-10
description: "Practical automation scripts and tools I've built to keep my home network secure without constant manual intervention"
tags: [python, automation, security, homelab, open-source, networking]
author: "William Zujkowski"
---

**Reading time:** 9 minutes

## The Problem: Security Doesn't Scale Without Automation

Managing home network security is like being a one-person SOC (Security Operations Center). You've got multiple devices, various family members with different tech literacy levels, and new threats emerging daily. Manual security management simply doesn't scale – especially when you're also trying to be present for bedtime stories.

This post shares the Python scripts and automation workflows I've developed to maintain security without sacrificing family time.

## The Foundation: Network Discovery and Asset Management

First challenge: knowing what's actually on your network. New devices appear constantly – kids' friends' phones, that new smart gadget someone bought, the mysterious device that might be the neighbor's printer.

True story: Years ago, I spent an hour hunting down an "ESP_8266_UNKNOWN" device on my network. I was ready to declare a security incident when my wife walked in: "Oh, that's probably the smart light bulb I installed in the guest bathroom."

Silence.

"You installed a what now?"

That's when I realized we needed automation – not just for security, but for marital harmony.

### Automated Device Discovery

Here's the script that saves my sanity (runs hourly, alerts immediately):

```python
#!/usr/bin/env python3
import nmap
import json
import sqlite3
from datetime import datetime
from pathlib import Path

class NetworkAssetManager:
    def __init__(self, db_path="network_assets.db"):
        self.db_path = db_path
        self.nm = nmap.PortScanner()
        self.setup_database()
    
    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                mac_address TEXT PRIMARY KEY,
                ip_address TEXT,
                hostname TEXT,
                vendor TEXT,
                first_seen TIMESTAMP,
                last_seen TIMESTAMP,
                trusted BOOLEAN DEFAULT 0,
                notes TEXT
            )
        ''')
        conn.commit()
        conn.close()
    
    def scan_network(self, network="192.168.1.0/24"):
        """Scan network and identify all devices"""
        print(f"Scanning {network}...")
        self.nm.scan(hosts=network, arguments='-sn')
        
        devices = []
        for host in self.nm.all_hosts():
            if 'mac' in self.nm[host]['addresses']:
                device = {
                    'ip': host,
                    'mac': self.nm[host]['addresses']['mac'],
                    'hostname': self.nm[host].hostname(),
                    'vendor': self.nm[host]['vendor'].get(
                        self.nm[host]['addresses']['mac'], 'Unknown'
                    )
                }
                devices.append(device)
                self.update_device(device)
        
        return devices
    
    def update_device(self, device):
        """Update or insert device in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO devices (mac_address, ip_address, hostname, vendor, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(mac_address) DO UPDATE SET
                ip_address = excluded.ip_address,
                hostname = excluded.hostname,
                last_seen = excluded.last_seen
        ''', (
            device['mac'],
            device['ip'],
            device['hostname'],
            device['vendor'],
            datetime.now(),
            datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def get_new_devices(self, hours=1):
        """Get devices first seen in the last N hours"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM devices
            WHERE first_seen > datetime('now', '-{} hours')
            AND trusted = 0
        '''.format(hours))
        
        new_devices = cursor.fetchall()
        conn.close()
        
        return new_devices

# Alert on new devices
if __name__ == "__main__":
    manager = NetworkAssetManager()
    manager.scan_network()
    
    new_devices = manager.get_new_devices()
    if new_devices:
        print(f"⚠️  Found {len(new_devices)} new devices!")
        # Send notification (covered in the notification section)
```

## DNS Monitoring and Ad Blocking

One of the most effective security measures is controlling DNS. I use Pi-hole for ad blocking but enhanced it with security monitoring.

### Detecting Suspicious DNS Queries

This script monitors DNS logs for suspicious patterns:

```python
import re
import sqlite3
from collections import defaultdict
from datetime import datetime, timedelta

class DNSSecurityMonitor:
    def __init__(self, pihole_db="/etc/pihole/pihole-FTL.db"):
        self.pihole_db = pihole_db
        self.suspicious_patterns = [
            r'.*\.tk$',  # Suspicious TLD
            r'.*\.ml$',
            r'.*\.ga$',
            r'[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}',  # IP in domain
            r'.*\..*\..*\..*\..*\.',  # Excessive subdomains
            r'.*(bitcoin|crypto|miner).*',  # Crypto mining
            r'^[a-f0-9]{32}\..*',  # Potential DGA domains
        ]
        
        # Known malware C2 domains (simplified list)
        self.known_bad_domains = self.load_threat_intel()
    
    def check_dns_queries(self, time_window_minutes=60):
        """Analyze recent DNS queries for suspicious activity"""
        conn = sqlite3.connect(self.pihole_db)
        cursor = conn.cursor()
        
        # Get recent queries
        timestamp = int((datetime.now() - timedelta(minutes=time_window_minutes)).timestamp())
        
        cursor.execute('''
            SELECT domain, client, COUNT(*) as count
            FROM queries
            WHERE timestamp > ?
            GROUP BY domain, client
        ''', (timestamp,))
        
        alerts = []
        
        for domain, client, count in cursor.fetchall():
            # Check against patterns
            for pattern in self.suspicious_patterns:
                if re.match(pattern, domain, re.IGNORECASE):
                    alerts.append({
                        'type': 'suspicious_pattern',
                        'domain': domain,
                        'client': client,
                        'pattern': pattern,
                        'count': count
                    })
            
            # Check against threat intel
            if domain in self.known_bad_domains:
                alerts.append({
                    'type': 'known_malware',
                    'domain': domain,
                    'client': client,
                    'count': count,
                    'severity': 'high'
                })
            
            # Check for DNS tunneling (high frequency of unique subdomains)
            if self.detect_dns_tunneling(domain, count):
                alerts.append({
                    'type': 'possible_dns_tunnel',
                    'domain': domain,
                    'client': client,
                    'count': count
                })
        
        conn.close()
        return alerts
    
    def detect_dns_tunneling(self, domain, query_count):
        """Detect potential DNS tunneling based on query patterns"""
        # High number of queries to single domain with varying subdomains
        if query_count > 100:
            # Additional logic to check subdomain randomness
            return True
        return False
    
    def load_threat_intel(self):
        """Load threat intelligence feeds"""
        # In production, this would fetch from multiple sources
        # For now, a simple set of known bad domains
        return {
            'malware-c2-server.com',
            'evil-phishing-site.net',
            # Add more from threat feeds
        }
```

## Automated Vulnerability Scanning

Keeping devices patched is crucial. This script runs weekly to identify vulnerable services:

```python
import nmap
import vulners
import json
from datetime import datetime

class HomeVulnerabilityScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.vulners_api = vulners.Vulners()
    
    def scan_device(self, ip_address):
        """Perform vulnerability scan on a single device"""
        print(f"Scanning {ip_address}...")
        
        # Service detection scan
        self.nm.scan(ip_address, '1-65535', '-sV')
        
        vulnerabilities = []
        
        for port in self.nm[ip_address]['tcp']:
            service_info = self.nm[ip_address]['tcp'][port]
            
            if 'product' in service_info and 'version' in service_info:
                # Search for CVEs
                search_query = f"{service_info['product']} {service_info['version']}"
                
                try:
                    results = self.vulners_api.search(search_query, limit=5)
                    
                    for vuln in results:
                        if vuln['cvss']['score'] >= 7.0:  # High severity
                            vulnerabilities.append({
                                'port': port,
                                'service': service_info['product'],
                                'version': service_info['version'],
                                'cve': vuln.get('id'),
                                'cvss': vuln['cvss']['score'],
                                'description': vuln.get('description', '')[:200]
                            })
                except:
                    pass
        
        return vulnerabilities
    
    def generate_report(self, scan_results):
        """Generate actionable vulnerability report"""
        report = {
            'scan_date': datetime.now().isoformat(),
            'total_devices': len(scan_results),
            'vulnerable_devices': sum(1 for r in scan_results if r['vulnerabilities']),
            'critical_findings': []
        }
        
        for result in scan_results:
            if result['vulnerabilities']:
                for vuln in result['vulnerabilities']:
                    if vuln['cvss'] >= 9.0:
                        report['critical_findings'].append({
                            'device': result['ip'],
                            'vulnerability': vuln
                        })
        
        return report
```

## Smart Firewall Rules Management

Static firewall rules don't adapt to changing threats. Here's how I automate rule updates:

```python
import subprocess
import ipaddress
from datetime import datetime, timedelta

class DynamicFirewall:
    def __init__(self):
        self.rules_db = "firewall_rules.db"
        self.setup_database()
    
    def add_temporary_block(self, ip_address, duration_hours=24, reason=""):
        """Add temporary firewall block"""
        expiry = datetime.now() + timedelta(hours=duration_hours)
        
        # Add to pfSense (using pfSsh.php)
        command = f"""
        pfSsh.php playback addtable bruteforce {ip_address}
        """
        
        subprocess.run(['ssh', 'pfsense', command])
        
        # Log the action
        conn = sqlite3.connect(self.rules_db)
        conn.execute('''
            INSERT INTO temporary_blocks (ip_address, reason, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        ''', (ip_address, reason, datetime.now(), expiry))
        conn.commit()
        conn.close()
    
    def auto_block_failed_auth(self, threshold=5):
        """Automatically block IPs with excessive failed authentications"""
        # Parse auth logs
        failed_attempts = defaultdict(int)
        
        with open('/var/log/auth.log', 'r') as f:
            for line in f:
                if 'Failed password' in line:
                    # Extract IP address
                    ip_match = re.search(r'from (\d+\.\d+\.\d+\.\d+)', line)
                    if ip_match:
                        failed_attempts[ip_match.group(1)] += 1
        
        # Block IPs exceeding threshold
        for ip, count in failed_attempts.items():
            if count >= threshold:
                self.add_temporary_block(
                    ip, 
                    duration_hours=48,
                    reason=f"Failed auth attempts: {count}"
                )
    
    def update_geo_blocks(self):
        """Update geo-blocking rules based on threat intelligence"""
        # Fetch current threat landscape
        high_risk_countries = self.get_high_risk_countries()
        
        for country_code in high_risk_countries:
            # Update pfBlockerNG lists
            self.update_pf_blocker_list(country_code)
```

## Notification System

All this automation is useless if you don't know what's happening. Here's my notification system:

```python
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class SecurityNotifier:
    def __init__(self, config):
        self.config = config
        self.notification_history = []
    
    def send_alert(self, alert_type, message, severity="medium"):
        """Send security alert through multiple channels"""
        
        # Determine notification method based on severity
        if severity == "critical":
            self.send_sms(message)
            self.send_email(f"CRITICAL: {alert_type}", message)
            self.send_pushover(message, priority=2)
        elif severity == "high":
            self.send_email(f"Alert: {alert_type}", message)
            self.send_pushover(message, priority=1)
        else:
            self.send_email(f"Notice: {alert_type}", message)
        
        # Log notification
        self.notification_history.append({
            'timestamp': datetime.now(),
            'type': alert_type,
            'severity': severity,
            'message': message
        })
    
    def send_pushover(self, message, priority=0):
        """Send push notification to phone"""
        requests.post("https://api.pushover.net/1/messages.json", data={
            "token": self.config['pushover_token'],
            "user": self.config['pushover_user'],
            "message": message,
            "priority": priority
        })
    
    def daily_summary(self):
        """Send daily security summary"""
        summary = self.generate_daily_summary()
        
        html_content = f"""
        <html>
        <body>
        <h2>Daily Security Summary</h2>
        <p>Report for {datetime.now().strftime('%Y-%m-%d')}</p>
        
        <h3>Network Status</h3>
        <ul>
        <li>Total Devices: {summary['total_devices']}</li>
        <li>New Devices: {summary['new_devices']}</li>
        <li>Security Events: {summary['security_events']}</li>
        </ul>
        
        <h3>Blocked Threats</h3>
        <ul>
        <li>Malicious IPs: {summary['blocked_ips']}</li>
        <li>Suspicious DNS: {summary['blocked_dns']}</li>
        <li>Failed Auth: {summary['failed_auth']}</li>
        </ul>
        
        <h3>Action Items</h3>
        {self.format_action_items(summary['action_items'])}
        </body>
        </html>
        """
        
        self.send_email("Daily Security Summary", html_content, html=True)
```

## Putting It All Together

The real power comes from orchestrating these scripts. Here's my master automation script:

```python
#!/usr/bin/env python3
"""
Home Security Automation Orchestrator
Runs various security checks and responds to threats
"""

import schedule
import time
from threading import Thread

class SecurityOrchestrator:
    def __init__(self):
        self.asset_manager = NetworkAssetManager()
        self.dns_monitor = DNSSecurityMonitor()
        self.vuln_scanner = HomeVulnerabilityScanner()
        self.firewall = DynamicFirewall()
        self.notifier = SecurityNotifier(config)
    
    def hourly_tasks(self):
        """Run every hour"""
        # Network discovery
        self.asset_manager.scan_network()
        new_devices = self.asset_manager.get_new_devices()
        
        if new_devices:
            message = f"Found {len(new_devices)} new devices on network"
            self.notifier.send_alert("New Devices", message, "medium")
        
        # DNS monitoring
        dns_alerts = self.dns_monitor.check_dns_queries()
        for alert in dns_alerts:
            if alert['type'] == 'known_malware':
                self.firewall.add_temporary_block(alert['client'])
                self.notifier.send_alert("Malware Blocked", 
                    f"Blocked {alert['client']} accessing {alert['domain']}", 
                    "high")
    
    def daily_tasks(self):
        """Run daily"""
        # Update firewall rules
        self.firewall.auto_block_failed_auth()
        self.firewall.update_geo_blocks()
        
        # Send summary
        self.notifier.daily_summary()
    
    def weekly_tasks(self):
        """Run weekly"""
        # Vulnerability scanning
        devices = self.asset_manager.get_all_devices()
        scan_results = []
        
        for device in devices:
            if device['trusted']:
                vulns = self.vuln_scanner.scan_device(device['ip'])
                scan_results.append({
                    'ip': device['ip'],
                    'vulnerabilities': vulns
                })
        
        report = self.vuln_scanner.generate_report(scan_results)
        if report['critical_findings']:
            self.notifier.send_alert("Critical Vulnerabilities Found",
                json.dumps(report, indent=2), "critical")
    
    def run(self):
        """Start the orchestrator"""
        # Schedule tasks
        schedule.every().hour.do(self.hourly_tasks)
        schedule.every().day.at("09:00").do(self.daily_tasks)
        schedule.every().monday.at("10:00").do(self.weekly_tasks)
        
        # Run scheduler
        while True:
            schedule.run_pending()
            time.sleep(60)

if __name__ == "__main__":
    orchestrator = SecurityOrchestrator()
    orchestrator.run()
```

## Lessons Learned

### 1. Start with Visibility
You can't secure what you can't see. Network discovery and asset management should be your first automation project.

### 2. Alert Fatigue is Real
Fine-tune your alerts. Too many notifications and you'll start ignoring them. I learned this the hard way when my phone wouldn't stop buzzing.

### 3. Family-Friendly Automation
Your security automation shouldn't impact family life. My scripts include:
- Whitelisting for family devices
- "Quiet hours" for non-critical alerts
- Easy override mechanisms

### 4. Test in Isolation
Always test security automation in an isolated environment first. I once accidentally blocked my entire home network. The family was... not amused.

### 5. Document Everything
Future you (or your family when you're not home) needs to understand how to disable things. I maintain a simple wiki with:
- What each script does
- How to temporarily disable automation
- Emergency contacts

## Tools and Resources

Here are the key tools I use:
- **nmap**: Network discovery and port scanning
- **Pi-hole**: DNS filtering and logging
- **pfSense**: Firewall and routing
- **Python libraries**: python-nmap, vulners, schedule
- **Notification**: Pushover for mobile alerts

## What's Next?

Security automation is an ongoing journey. My upcoming projects include:
- Machine learning for anomaly detection
- Automated incident response playbooks
- Integration with threat intelligence feeds
- Voice alerts for critical events ("Alexa, announce security alert")

## Conclusion

Automating home network security has transformed my approach to protecting my family's digital life. Instead of constantly checking logs and running manual scans, I can focus on improving defenses while automation handles the routine work.

The best part? When my kids ask what I do for work, I can show them our "home security robot" in action. Nothing beats seeing their faces light up when they understand that Dad's job is basically being a cyber superhero.

Remember: the goal isn't to build Fort Knox, it's to raise the bar high enough that attackers move on to easier targets. Automation helps you maintain that bar without burning out.

---

*Have questions about any of these scripts? Want to share your own automation ideas? Drop me a line – I love connecting with fellow security automation enthusiasts!*