#!/bin/bash
# Proxmox HA Manager Configuration
#
# Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
# Purpose: Enable HA and configure fencing for failover
# Requires: an operational Proxmox VE cluster with shared storage
#
# Illustrative excerpt, not a turnkey script.
#
# The previous version configured IPMI fence agents:
#
#     ha-manager add fence-pve1 --type=ipmilan --ip=... --username=... \
#         --password=... --lanplus=1
#
# None of that is real. Per ha-manager(1), the synopsis is
# `ha-manager add <sid> [OPTIONS]`; <sid> is a RESOURCE id of the form
# `vm:100` or `ct:100`, `--type` takes `<ct|vm>`, and --ip / --username /
# --password / --lanplus do not exist. `ha-manager add` registers a VM or
# container as an HA resource. It has nothing to do with fencing.
#
# Proxmox VE does not use external fence agents at all. From the HA wiki:
# "we wanted to integrate a simpler fencing method, which does not require
# additional external hardware. This can be done using watchdog timers."
# ha-manager resets the watchdog during normal operation; if it stops, the
# timer elapses and the node reboots itself. There is nothing to install and
# no credentials to store.

set -euo pipefail

# ---------------------------------------------------------------------------
# 1. HA services. Enabled with the cluster; this just confirms they are up.
# ---------------------------------------------------------------------------
systemctl status pve-ha-lrm --no-pager
systemctl status pve-ha-crm --no-pager
ha-manager status

# ---------------------------------------------------------------------------
# 2. Fencing = watchdog self-fencing.
#
# The default is the kernel softdog. A hardware watchdog is better, but all
# hardware watchdog modules are blocked by default for safety and must be
# named explicitly. Find yours (iTCO_wdt on most Intel server boards) and set
# it in /etc/default/pve-ha-manager, which watchdog-mux reads at startup.
# ---------------------------------------------------------------------------
# cat /etc/default/pve-ha-manager
#   # select watchdog module (default is softdog)
#   WATCHDOG_MODULE=iTCO_wdt
#
# systemctl restart watchdog-mux
systemctl status watchdog-mux --no-pager

# ---------------------------------------------------------------------------
# 3. Register the resources you actually want kept alive.
#
# This is what `ha-manager add` is for. Note the sid form.
# ---------------------------------------------------------------------------
ha-manager add vm:100 --state started --max_restart 2 --max_relocate 2
ha-manager add ct:200 --state started

# ---------------------------------------------------------------------------
# 4. Node preference (optional).
#
# Higher number = higher priority. nofailback=0 lets a service migrate back
# once its preferred node returns.
# ---------------------------------------------------------------------------
# HA Groups are deprecated: "HA Groups are deprecated and migrated to HA
# Node Affinity rules since Proxmox VE 9.0."
ha-manager rules add node-affinity critical-services \
    --resources vm:100,ct:200 \
    --nodes "pve1:2,pve2:1,pve3:1"

# On Proxmox VE 8 and earlier this was:
#   ha-manager groupadd critical_services \
#       --nodes "pve1:2,pve2:1,pve3:1" --nofailback 0
#   ha-manager set vm:100 --group critical_services

echo "HA configured. Fencing is watchdog-based -- verify with: ha-manager status"
