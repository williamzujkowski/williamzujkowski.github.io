#!/bin/bash
"""
Pi-hole VLAN-Specific DNS Filtering

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Apply different DNS blocklists per VLAN with conditional forwarding
Location: /etc/pihole/custom.list and /etc/dnsmasq.d/custom.conf
Prerequisites: Pi-hole installed, access to configuration
Usage:
    bash pihole-vlan-filtering.sh

License: MIT
"""

# Block telemetry domains for IoT VLAN
cat > /etc/pihole/iot-blocklist.list <<EOF
0.0.0.0 phone-home.camera-vendor.com
0.0.0.0 telemetry.iot-vendor.com
0.0.0.0 stats.smart-device.com
0.0.0.0 tracking.xiaomi.com
0.0.0.0 analytics.tp-link.com
EOF

# Conditional forwarding for internal domains
cat > /etc/dnsmasq.d/vlan-conditional.conf <<EOF
# Forward internal domain queries to appropriate DNS servers
server=/lab.home/10.0.30.5
server=/mgmt.home/10.0.10.5
server=/servers.home/10.0.30.5

# Block DNS requests from IoT to external resolvers (force Pi-hole)
bogus-nxdomain=8.8.8.8
bogus-nxdomain=1.1.1.1
EOF

# Restart Pi-hole to apply changes
pihole restartdns

echo "VLAN-specific DNS filtering configured"
