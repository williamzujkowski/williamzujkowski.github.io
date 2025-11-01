#!/bin/bash
"""
UDM Pro VLAN Creation and Configuration

Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
Purpose: Create VLANs with proper tagging and trunk port configuration on Ubiquiti Dream Machine Pro
Prerequisites: SSH access to UDM Pro, admin credentials
Usage:
    bash udm-pro-vlan-config.sh

License: MIT
"""

# SSH into UDM Pro
# ssh admin@10.0.0.1

# Enable advanced features
set system advanced enable

# Configure VLANs
configure
set interfaces ethernet eth1 vif 10 description "Management"
set interfaces ethernet eth1 vif 10 address 10.0.10.1/24
set interfaces ethernet eth1 vif 20 description "Trusted"
set interfaces ethernet eth1 vif 20 address 10.0.20.1/24
set interfaces ethernet eth1 vif 30 description "Servers"
set interfaces ethernet eth1 vif 30 address 10.0.30.1/24
set interfaces ethernet eth1 vif 40 description "IoT"
set interfaces ethernet eth1 vif 40 address 10.0.40.1/24
set interfaces ethernet eth1 vif 50 description "Guest"
set interfaces ethernet eth1 vif 50 address 10.0.50.1/24
set interfaces ethernet eth1 vif 60 description "Lab"
set interfaces ethernet eth1 vif 60 address 10.0.60.1/24
set interfaces ethernet eth1 vif 70 description "DMZ"
set interfaces ethernet eth1 vif 70 address 10.0.70.1/24
commit
save

echo "VLANs configured successfully on UDM Pro"
