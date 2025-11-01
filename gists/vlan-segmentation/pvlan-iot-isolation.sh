#!/bin/bash
"""
Private VLAN (PVLAN) IoT Isolation

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Isolate IoT devices from each other while allowing gateway access
Prerequisites: Managed switch with PVLAN support
Usage:
    bash pvlan-iot-isolation.sh

License: MIT
"""

# Create isolated ports within IoT VLAN
configure
set interfaces ethernet eth1 vif 40 private-vlan isolated
set interfaces ethernet eth2 switchport private-vlan host-association 40 isolated
set interfaces ethernet eth3 switchport private-vlan host-association 40 isolated
set interfaces ethernet eth4 switchport private-vlan host-association 40 isolated
set interfaces ethernet eth5 switchport private-vlan host-association 40 isolated

# Create promiscuous port for gateway (allows communication with all isolated ports)
set interfaces ethernet eth1 switchport private-vlan mapping 40 promiscuous

commit
save

echo "PVLAN isolation configured for IoT VLAN"
echo "Devices on eth2-eth5 can reach gateway but not each other"
