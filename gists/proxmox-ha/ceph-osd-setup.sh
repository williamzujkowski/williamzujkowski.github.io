#!/bin/bash
"""
Ceph OSD Creation and Pool Configuration

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Create OSDs on each node and configure storage pools with replication
Prerequisites: Ceph installed, monitors running, dedicated disks available
Usage:
    bash ceph-osd-setup.sh

License: MIT
"""

# On each node, for each disk:
# Identify disks
lsblk
ceph-volume lvm list

# Create OSDs (replace /dev/sdX with actual disks)
# On pve1
pveceph osd create /dev/sdb
pveceph osd create /dev/sdc
pveceph osd create /dev/sdd

# On pve2
ssh pve2 "pveceph osd create /dev/sdb"
ssh pve2 "pveceph osd create /dev/sdc"
ssh pve2 "pveceph osd create /dev/sdd"

# On pve3
ssh pve3 "pveceph osd create /dev/sdb"
ssh pve3 "pveceph osd create /dev/sdc"
ssh pve3 "pveceph osd create /dev/sdd"

# Verify OSDs are up
ceph osd tree
ceph osd status

# Create pool for VM storage
pveceph pool create vm-storage --min_size 2 --size 3

# Create pool for backups
pveceph pool create backup-storage --min_size 2 --size 3

# Add to Proxmox storage
pvesm add rbd vm-storage --pool vm-storage --content images,rootdir
pvesm add rbd backup-storage --pool backup-storage --content backup

# Performance tuning
ceph osd pool set vm-storage pg_num 128
ceph osd pool set vm-storage pgp_num 128

# Enable RBD cache
ceph config set client rbd_cache true
ceph config set client rbd_cache_size 67108864

# Enable scrubbing during off-peak hours
ceph config set osd osd_scrub_begin_hour 2
ceph config set osd osd_scrub_end_hour 6

# Check cluster health
ceph -s
ceph health detail

echo "Ceph OSD setup complete. Storage pools created."
