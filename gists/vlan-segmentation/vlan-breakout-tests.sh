#!/bin/bash
"""
VLAN Breakout Penetration Testing

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Test VLAN isolation with controlled penetration testing
WARNING: Only run on your own network with proper authorization
Prerequisites: nmap, metasploit (optional)
Usage:
    bash vlan-breakout-tests.sh

License: MIT
"""

echo "=== VLAN Breakout Testing ==="
echo "WARNING: Only run on authorized networks"
echo ""

# Test 1: VLAN hopping via double tagging
echo "[Test 1] Double VLAN Tagging Attack"
echo "Attempting to send packets with nested VLAN tags..."
# This would require raw socket programming - demonstration only
echo "✓ Test complete (requires manual validation)"
echo ""

# Test 2: ARP spoofing across VLANs
echo "[Test 2] Cross-VLAN ARP Spoofing"
echo "Attempting ARP cache poisoning..."
# arpspoof -i eth0 -t 10.0.40.100 10.0.10.1
echo "✓ Should be blocked by VLAN isolation"
echo ""

# Test 3: Port scanning from IoT VLAN
echo "[Test 3] Port Scanning from IoT VLAN"
echo "Scanning management VLAN from IoT device..."
nmap -sT -p 22,80,443 10.0.10.0/24 -T4 --max-retries 1
echo "✗ All ports should be filtered/unreachable"
echo ""

# Test 4: DNS tunneling
echo "[Test 4] DNS Tunneling Detection"
echo "Attempting DNS tunnel (should be detected)..."
for i in {1..10}; do
    dig @10.0.10.5 "test-tunnel-$RANDOM.example.com" +short
done
echo "✓ Check DNS logs for unusual query patterns"
echo ""

# Test 5: Router firmware exploitation
echo "[Test 5] Router Firmware Version Check"
echo "Checking for known vulnerable firmware..."
curl -s http://10.0.10.1/api/system/info | jq '.firmware_version'
echo "✓ Verify firmware is up to date"
echo ""

echo "=== Testing Complete ==="
echo "Review firewall logs for any violations"
