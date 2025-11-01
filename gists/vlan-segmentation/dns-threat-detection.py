#!/usr/bin/env python3
"""
DNS Query Analyzer for Threat Detection

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Analyze DNS queries from IoT VLAN for suspicious patterns
Prerequisites: Python 3.6+, access to Pi-hole logs
Usage:
    python dns-threat-detection.py --log /var/log/pihole.log --vlan 10.0.40

License: MIT
"""

import re
import argparse
from collections import Counter
from datetime import datetime

def analyze_dns_queries(log_file, vlan_subnet):
    """Find IoT devices querying suspicious domains"""

    # Whitelisted domains (known good)
    whitelist = ['google.com', 'amazonaws.com', 'cloudflare.com', 'apple.com']

    suspicious_patterns = [
        r'\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3}',  # IP-like domains
        r'[a-f0-9]{16,}',  # Long hex strings
        r'\.tk$|\.ml$|\.ga$|\.cf$',  # Free TLDs
    ]

    queries = []
    suspicious = []

    with open(log_file, 'r') as f:
        for line in f.readlines()[-10000:]:  # Last 10k lines
            if vlan_subnet in line:
                parts = line.split()
                if len(parts) >= 6:
                    ip = parts[4]
                    domain = parts[5]

                    # Check if domain is whitelisted
                    if not any(wl in domain for wl in whitelist):
                        queries.append((ip, domain))

                        # Check for suspicious patterns
                        for pattern in suspicious_patterns:
                            if re.search(pattern, domain):
                                suspicious.append((ip, domain, pattern))

    return queries, suspicious

def detect_high_volume(queries, threshold=100):
    """Detect devices with abnormally high query volumes"""
    ip_counts = Counter([ip for ip, _ in queries])
    high_volume = [(ip, count) for ip, count in ip_counts.items() if count > threshold]
    return high_volume

def generate_report(queries, suspicious, high_volume):
    """Generate threat detection report"""
    print(f"=== DNS Threat Detection Report ===")
    print(f"Generated: {datetime.now()}")
    print(f"\nTotal queries analyzed: {len(queries)}")
    print(f"Suspicious patterns found: {len(suspicious)}")
    print(f"High-volume devices: {len(high_volume)}\n")

    if suspicious:
        print("Suspicious Domains:")
        for ip, domain, pattern in suspicious[:20]:
            print(f"  {ip} -> {domain} (pattern: {pattern})")

    if high_volume:
        print("\nHigh Query Volume:")
        for ip, count in high_volume:
            print(f"  {ip}: {count} queries")

def main():
    parser = argparse.ArgumentParser(description='Analyze DNS queries for threats')
    parser.add_argument('--log', default='/var/log/pihole.log', help='Pi-hole log file')
    parser.add_argument('--vlan', default='10.0.40', help='VLAN subnet to analyze')
    parser.add_argument('--threshold', type=int, default=100, help='Query volume threshold')

    args = parser.parse_args()

    queries, suspicious = analyze_dns_queries(args.log, args.vlan)
    high_volume = detect_high_volume(queries, args.threshold)
    generate_report(queries, suspicious, high_volume)

if __name__ == '__main__':
    main()
