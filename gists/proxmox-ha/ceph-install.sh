#!/bin/bash
"""
Ceph Installation and Monitor Setup

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Install Ceph distributed storage and create monitors on all nodes
Prerequisites: Proxmox cluster created, storage network configured
Usage:
    bash ceph-install.sh

License: MIT
"""

# On all nodes
pveceph install --repository no-subscription --version quincy

# Wait for installation to complete
sleep 30

# Initialize Ceph on Node 1
pveceph init --network 10.0.100.0/24

# Create monitors on all nodes
for node in pve1 pve2 pve3; do
    ssh $node "pveceph mon create"
    sleep 10
done

# Verify monitors are running
ceph mon stat
ceph -s

echo "Ceph installation complete. Monitors active on all nodes."
