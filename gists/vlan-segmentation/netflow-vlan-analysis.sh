#!/bin/bash
"""
NetFlow VLAN Traffic Analysis Configuration

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Configure NetFlow v9 for VLAN traffic monitoring and analysis
Prerequisites: nfdump, nfcapd installed
Usage:
    bash netflow-vlan-analysis.sh

License: MIT
"""

# Enable NetFlow on UDM Pro
configure
set system flow-accounting interface eth1
set system flow-accounting netflow version 9
set system flow-accounting netflow server 10.0.10.5 port 2055
set system flow-accounting netflow timeout expiry-interval 60
set system flow-accounting netflow timeout flow-generic 3600
commit
save

# Start nfcapd collector on monitoring server
nfcapd -D -l /var/cache/nfdump -p 2055 -T all -P /var/run/nfcapd.pid

# Analyze cross-VLAN traffic (IoT VLAN attempting to reach other VLANs)
echo "=== Cross-VLAN Traffic Analysis ==="
nfdump -R /var/cache/nfdump -s srcip/bytes -n 20 \
  'src net 10.0.40.0/24 and not (dst net 10.0.40.0/24 or dst port 53 or dst port 123)'

# Top bandwidth consumers
echo "=== Top Bandwidth Consumers ==="
nfdump -R /var/cache/nfdump -s srcip/bytes -n 10

# Suspicious port scans
echo "=== Potential Port Scans ==="
nfdump -R /var/cache/nfdump 'flags S and packets < 5' -s srcip -n 10

echo "NetFlow analysis complete"
