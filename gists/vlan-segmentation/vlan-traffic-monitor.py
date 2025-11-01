#!/usr/bin/env python3
"""
VLAN Traffic Monitor with Anomaly Detection

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Monitor cross-VLAN traffic patterns and detect anomalies
Prerequisites: Python 3.6+, root access for log reading
Usage:
    sudo python vlan-traffic-monitor.py

License: MIT
"""

import subprocess
import json
from datetime import datetime
from collections import defaultdict

def analyze_cross_vlan_traffic():
    """Detect unexpected cross-VLAN traffic"""

    # Expected patterns (whitelist)
    allowed_flows = {
        ('10.0.20.0/24', '10.0.30.0/24', 443),  # Trusted to Servers HTTPS
        ('10.0.20.0/24', '10.0.40.0/24', 80),   # Trusted to IoT HTTP
        ('10.0.20.0/24', '10.0.40.0/24', 443),  # Trusted to IoT HTTPS
        ('10.0.40.0/24', '10.0.10.5', 53),      # IoT to DNS
    }

    violations = []

    # Parse firewall logs
    try:
        with open('/var/log/firewall.log', 'r') as f:
            for line in f.readlines()[-1000:]:  # Last 1000 lines
                if 'ACCEPT' not in line:
                    continue

                # Extract source, destination, port
                parts = line.split()
                if len(parts) < 10:
                    continue

                src = parts[5]
                dst = parts[7]
                port = int(parts[9]) if parts[9].isdigit() else 0

                # Check if flow is allowed
                flow = (src, dst, port)
                if flow not in allowed_flows and not is_same_vlan(src, dst):
                    violations.append({
                        'timestamp': datetime.now().isoformat(),
                        'source': src,
                        'destination': dst,
                        'port': port,
                        'severity': 'high'
                    })

    except FileNotFoundError:
        print("Firewall log not found")
        return []

    return violations

def is_same_vlan(ip1, ip2):
    """Check if two IPs are in the same /24 VLAN"""
    vlan1 = '.'.join(ip1.split('.')[:3])
    vlan2 = '.'.join(ip2.split('.')[:3])
    return vlan1 == vlan2

def alert(message, severity='warning'):
    """Send alert via multiple channels"""
    timestamp = datetime.now().isoformat()
    alert_msg = f"[{severity.upper()}] {timestamp}: {message}"

    print(alert_msg)

    # Log to syslog
    subprocess.run(['logger', '-t', 'vlan-monitor', alert_msg])

    # Could add: Slack, email, Wazuh integration here

def monitor_loop():
    """Main monitoring loop"""
    print("Starting VLAN traffic monitor...")

    while True:
        violations = analyze_cross_vlan_traffic()

        if violations:
            for violation in violations:
                msg = f"Unexpected traffic: {violation['source']} -> {violation['destination']}:{violation['port']}"
                alert(msg, violation['severity'])

        # Sleep 60 seconds between checks
        import time
        time.sleep(60)

if __name__ == '__main__':
    monitor_loop()
