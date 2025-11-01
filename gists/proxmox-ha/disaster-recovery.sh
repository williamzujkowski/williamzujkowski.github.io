#!/bin/bash
"""
Proxmox HA Disaster Recovery Procedures

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: DR procedures for cluster rebuild, node recovery, and data restoration
Prerequisites: Valid backups, documented configuration
Usage:
    # Full cluster rebuild: bash disaster-recovery.sh rebuild
    # Single node recovery: bash disaster-recovery.sh node <node_name>
    # Restore from backup: bash disaster-recovery.sh restore <backup_file>

License: MIT
"""

BACKUP_DIR="/mnt/backup/proxmox"

function rebuild_cluster() {
    echo "=== Full Cluster Rebuild ==="

    # 1. Prepare new nodes
    for node in pve1 pve2 pve3; do
        echo "Preparing $node..."
        ssh $node "bash /root/node-prep.sh"
    done

    # 2. Create new cluster
    echo "Creating cluster on pve1..."
    ssh pve1 "pvecm create homelab-cluster --link0 10.0.10.11 --link1 10.0.100.11"

    # 3. Join other nodes
    for node in pve2 pve3; do
        echo "Joining $node to cluster..."
        ssh $node "bash /root/cluster-create.sh join 10.0.10.11"
    done

    # 4. Restore cluster configuration
    echo "Restoring cluster configuration..."
    LATEST_BACKUP=$(ls -t $BACKUP_DIR/cluster-config_*.tar.gz | head -1)
    tar -xzf "$LATEST_BACKUP" -C /

    # 5. Reinstall Ceph
    echo "Reinstalling Ceph..."
    bash /root/ceph-install.sh
    bash /root/ceph-osd-setup.sh

    # 6. Restore VMs from PBS
    echo "Restoring VMs from Proxmox Backup Server..."
    # Manual step: Use PBS web interface to restore VMs

    echo "Cluster rebuild complete. Verify all services."
}

function recover_node() {
    NODE_NAME="$1"
    echo "=== Node Recovery: $NODE_NAME ==="

    # 1. Remove failed node from cluster
    pvecm delnode $NODE_NAME

    # 2. Reinstall Proxmox on node

    # 3. Rejoin to cluster
    ssh $NODE_NAME "pvecm add 10.0.10.11 --link0 <node_ip> --link1 <storage_ip>"

    # 4. Restore Ceph OSDs
    ssh $NODE_NAME "bash /root/ceph-osd-setup.sh"

    # 5. Restore fencing configuration
    ha-manager add fence-$NODE_NAME --type=ipmilan --ip=<ipmi_ip> --username=admin --password=<password> --lanplus=1

    echo "Node recovery complete for $NODE_NAME"
}

function restore_from_backup() {
    BACKUP_FILE="$1"
    echo "=== Restoring from Backup: $BACKUP_FILE ==="

    # Extract backup
    tar -xzf "$BACKUP_FILE" -C /tmp/restore

    # Restore Proxmox configuration
    cp -r /tmp/restore/etc/pve /etc/
    cp -r /tmp/restore/etc/corosync /etc/

    # Restart services
    systemctl restart pve-cluster corosync
    systemctl restart pvedaemon pveproxy pvestatd

    echo "Restore complete. Verify cluster status with 'pvecm status'"
}

function validate_recovery() {
    echo "=== Post-Recovery Validation ==="

    # Check cluster quorum
    pvecm status

    # Verify all nodes online
    pvecm nodes

    # Check Ceph health
    ceph -s
    ceph health detail

    # Verify HA resources
    ha-manager status

    # Test failover
    echo "Manual test: Migrate a test VM to verify HA functionality"
}

# Main script logic
case "$1" in
    rebuild)
        rebuild_cluster
        validate_recovery
        ;;
    node)
        if [ -z "$2" ]; then
            echo "Usage: bash disaster-recovery.sh node <node_name>"
            exit 1
        fi
        recover_node "$2"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "Usage: bash disaster-recovery.sh restore <backup_file>"
            exit 1
        fi
        restore_from_backup "$2"
        validate_recovery
        ;;
    *)
        echo "Proxmox HA Disaster Recovery"
        echo ""
        echo "Usage:"
        echo "  bash disaster-recovery.sh rebuild           - Full cluster rebuild"
        echo "  bash disaster-recovery.sh node <name>       - Recover single node"
        echo "  bash disaster-recovery.sh restore <file>    - Restore from backup"
        echo ""
        echo "Available backups:"
        ls -lh $BACKUP_DIR/cluster-config_*.tar.gz | tail -5
        exit 1
        ;;
esac
