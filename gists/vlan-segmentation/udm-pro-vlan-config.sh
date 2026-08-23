#!/bin/bash
# UDM Pro VLAN Configuration
#
# Source: https://williamzujkowski.github.io/posts/zero-trust-vlan-segmentation-homelab/
# Purpose: Define the seven-VLAN homelab layout the post describes
#
# Illustrative reference, not a runnable script -- and deliberately so, because
# on a UDM Pro there is no CLI to run.
#
# The previous version of this file was EdgeRouter (EdgeOS) syntax:
#
#     configure
#     set interfaces ethernet eth1 vif 10 address 10.0.10.1/24
#     commit ; save
#
# That is verbatim the shape in Ubiquiti's own EdgeRouter VLAN article, for a
# different product family. A UDM Pro runs UniFi OS: SSH gives a Linux root
# shell (disabled by default after setup, and Ubiquiti advises against it
# outside Support-directed troubleshooting). There is no Vyatta configuration
# mode, so `configure` / `set` / `commit` / `save` are not commands that exist
# there. The file also issued `set system advanced enable` BEFORE `configure`,
# which could not work even on EdgeOS, where `set` only exists inside
# configuration mode.
#
# VLANs are defined in the UniFi Network application:
#   Settings > Networks > New Virtual Network
# setting Name, VLAN ID, Gateway IP/Subnet, and DHCP mode/range for each.
#
#   VLAN ID   Name         Gateway
#   -------   ----------   ---------------
#   10        Management   10.0.10.1/24
#   20        Trusted      10.0.20.1/24
#   30        Servers      10.0.30.1/24
#   40        IoT          10.0.40.1/24
#   50        Guest        10.0.50.1/24
#   60        Lab          10.0.60.1/24
#   70        DMZ          10.0.70.1/24
#
# If you want this automated rather than clicked, the supported route is the
# UniFi Network API, not SSH:
#   POST /proxy/network/api/s/<site>/rest/networkconf
# with a JSON body carrying name, vlan, ip_subnet and dhcpd settings.

cat <<'EOF'
VLANs on a UDM Pro are created in the UniFi Network application:
  Settings > Networks > New Virtual Network

  10 Management  10.0.10.1/24      50 Guest   10.0.50.1/24
  20 Trusted     10.0.20.1/24      60 Lab     10.0.60.1/24
  30 Servers     10.0.30.1/24      70 DMZ     10.0.70.1/24
  40 IoT         10.0.40.1/24

There is no EdgeOS-style CLI on UniFi OS. For automation use the
UniFi Network API endpoint /rest/networkconf.
EOF
