#!/bin/bash
"""
Proxmox HA Manager Configuration

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Enable HA manager and configure fencing for failover
Prerequisites: Proxmox cluster operational, shared storage configured
Usage:
    bash ha-manager-setup.sh

License: MIT
"""

# HA is enabled by default with cluster setup
# Verify HA services are running
systemctl status pve-ha-lrm
systemctl status pve-ha-crm

# Check HA status
ha-manager status

# Install fence agents
apt install -y fence-agents-all

# Configure IPMI-based fencing for each node
ha-manager add fence-pve1 --type=ipmilan \
    --ip=10.0.10.21 \
    --username=admin \
    --password=secure-password \
    --lanplus=1

ha-manager add fence-pve2 --type=ipmilan \
    --ip=10.0.10.22 \
    --username=admin \
    --password=secure-password \
    --lanplus=1

ha-manager add fence-pve3 --type=ipmilan \
    --ip=10.0.10.23 \
    --username=admin \
    --password=secure-password \
    --lanplus=1

# Test fencing
fence_ipmilan -a 10.0.10.21 -l admin -p secure-password -o status

# Configure HA groups (optional)
ha-manager groupadd critical_services --nodes "pve1:2,pve2:1,pve3:1" --nofailback 0

echo "HA Manager configured successfully. Fencing agents active."
