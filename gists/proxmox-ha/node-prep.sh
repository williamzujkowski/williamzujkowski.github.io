#!/bin/bash
"""
Proxmox Node Preparation Script

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Prepare each Proxmox node for cluster membership with proper networking and packages
Prerequisites: Fresh Proxmox VE 8.x installation
Usage:
    bash node-prep.sh

License: MIT
"""

# On each node: Update and prepare
apt update && apt full-upgrade -y
apt install -y bridge-utils ifupdown2

# Disable enterprise repository (for homelab)
rm /etc/apt/sources.list.d/pve-enterprise.list

# Add no-subscription repository
echo "deb http://download.proxmox.com/debian/pve bookworm pve-no-subscription" > \
    /etc/apt/sources.list.d/pve-no-subscription.list

apt update

# Configure static IP addresses
cat >> /etc/network/interfaces <<EOF
auto vmbr0
iface vmbr0 inet static
    address 10.0.10.11/24
    gateway 10.0.10.1
    bridge-ports eno1
    bridge-stp off
    bridge-fd 0

auto vmbr1
iface vmbr1 inet static
    address 10.0.100.11/24
    bridge-ports eno2
    bridge-stp off
    bridge-fd 0
    # Ceph storage network
EOF

systemctl restart networking

echo "Node preparation complete. Ready for cluster join."
