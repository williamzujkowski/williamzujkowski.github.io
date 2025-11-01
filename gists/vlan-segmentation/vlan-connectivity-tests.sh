#!/bin/bash
"""
VLAN Segmentation Connectivity Test Suite

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Validate VLAN segmentation is working correctly
Prerequisites: nmap, ping access
Usage:
    bash vlan-connectivity-tests.sh

License: MIT
"""

# Test connectivity between VLANs
declare -A vlans=(
    [mgmt]="10.0.10.100"
    [trusted]="10.0.20.100"
    [servers]="10.0.30.100"
    [iot]="10.0.40.100"
    [guest]="10.0.50.100"
)

echo "VLAN Segmentation Test Results"
echo "=============================="
echo ""

for src_vlan in "${!vlans[@]}"; do
    src_ip="${vlans[$src_vlan]}"

    for dst_vlan in "${!vlans[@]}"; do
        dst_ip="${vlans[$dst_vlan]}"

        if [ "$src_vlan" == "$dst_vlan" ]; then
            continue
        fi

        # Test ping (ICMP)
        result=$(ping -c 1 -W 1 -I "$src_ip" "$dst_ip" 2>&1 | grep -c "1 received")

        if [ "$result" -eq 1 ]; then
            echo "✓ $src_vlan -> $dst_vlan: REACHABLE"
        else
            echo "✗ $src_vlan -> $dst_vlan: BLOCKED"
        fi
    done
    echo ""
done

# Test specific ports
echo "Port-Specific Tests"
echo "==================="
echo ""

# Should succeed: Trusted to IoT HTTP
echo -n "Trusted -> IoT:80 (HTTP): "
nc -zv -w 2 10.0.40.100 80 &>/dev/null && echo "✓ ALLOWED" || echo "✗ BLOCKED"

# Should fail: IoT to Management SSH
echo -n "IoT -> Management:22 (SSH): "
nc -zv -w 2 10.0.10.100 22 &>/dev/null && echo "⚠ VIOLATION" || echo "✓ BLOCKED"

# Should succeed: Servers to Internet HTTPS
echo -n "Servers -> Internet:443 (HTTPS): "
nc -zv -w 2 1.1.1.1 443 &>/dev/null && echo "✓ ALLOWED" || echo "✗ BLOCKED"

echo ""
echo "Tests complete"
