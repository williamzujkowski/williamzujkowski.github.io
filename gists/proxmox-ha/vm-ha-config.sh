#!/bin/bash
"""
VM High Availability Configuration

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Enable HA for VMs with automatic failover and migration settings
Prerequisites: HA manager configured, VMs running on shared storage
Usage:
    bash vm-ha-config.sh <vm_id>

License: MIT
"""

if [ -z "$1" ]; then
    echo "Usage: bash vm-ha-config.sh <vm_id>"
    echo "Example: bash vm-ha-config.sh 100"
    exit 1
fi

VM_ID="$1"

# Enable HA for a VM
ha-manager add vm:$VM_ID --state started --group default_group --max_restart 3 --max_relocate 3

# For critical services group
# ha-manager add vm:$VM_ID --group critical_services --state started --max_restart 3

# View HA resources
ha-manager status

# Simulate failover test
echo ""
echo "To test failover, run: ssh pve<node> poweroff"
echo "Watch migration with: watch -n 1 'ha-manager status'"

echo "VM $VM_ID configured for HA successfully."
