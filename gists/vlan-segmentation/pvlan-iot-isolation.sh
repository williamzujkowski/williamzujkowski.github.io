#!/bin/bash
# Private VLAN isolation for the IoT VLAN
#
# Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
# Purpose: Stop IoT devices from talking to each other while still reaching
#          the gateway
#
# Illustrative reference. The commands below are Cisco IOS configuration-mode
# lines for a Catalyst switch -- paste them at a `configure terminal` prompt.
# They are not shell commands and this file will not "run".
#
# The previous version could not work on any device. It wrapped Cisco
# `switchport private-vlan ...` keywords inside Vyatta/EdgeOS operators
# (`configure`, `set interfaces ethernet eth1 vif 40 ...`, `commit`, `save`).
# Cisco IOS has no `set interfaces` and no `commit`/`save`; EdgeOS and VyOS
# have no `private-vlan` node. No platform accepts both.
#
# It was also malformed as Cisco. `switchport private-vlan host-association`
# takes TWO NUMERIC VLAN IDs -- <primary> <secondary> -- not the literal word
# `isolated`; and `switchport private-vlan mapping` takes <primary>
# <secondary-list>, not `promiscuous`. Port mode is a separate command from
# the mapping. Nothing in the old file ever associated a primary with a
# secondary, so no private VLAN existed to isolate anything.
#
# VLAN 40 is the primary; VLAN 41 is the isolated secondary.

cat <<'IOS'
! Private VLANs require VTP transparent mode on VTP v1/v2.
! (VTP v3 supports them in all modes.)
vtp mode transparent

! Define the secondary first, then the primary, then associate them.
vlan 41
 private-vlan isolated
vlan 40
 private-vlan primary
 private-vlan association 41

! Layer 3 gateway for the private-VLAN domain.
interface Vlan40
 ip address 10.0.40.1 255.255.255.0
 private-vlan mapping 41

! IoT device ports: host ports in the isolated secondary.
! host-association takes <primary> <secondary>, both numeric.
interface range GigabitEthernet1/0/2 - 5
 switchport mode private-vlan host
 switchport private-vlan host-association 40 41

! Uplink toward the router: promiscuous port.
! Mode first, then the mapping -- two separate commands.
interface GigabitEthernet1/0/1
 switchport mode private-vlan promiscuous
 switchport private-vlan mapping 40 41
IOS

echo
echo "Devices on Gi1/0/2-5 reach the promiscuous uplink but not each other."
