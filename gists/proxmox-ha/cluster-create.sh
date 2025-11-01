#!/bin/bash
"""
Proxmox Cluster Creation Script

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Create Proxmox cluster on primary node and join additional nodes
Prerequisites: Node preparation completed on all nodes
Usage:
    # On Node 1: bash cluster-create.sh create
    # On Node 2/3: bash cluster-create.sh join 10.0.10.11

License: MIT
"""

if [ "$1" == "create" ]; then
    # On Node 1 (create cluster)
    pvecm create homelab-cluster --link0 10.0.10.11 --link1 10.0.100.11

    # Verify cluster status
    pvecm status
    pvecm nodes

    echo "Cluster created. Join other nodes with: bash cluster-create.sh join 10.0.10.11"

elif [ "$1" == "join" ] && [ -n "$2" ]; then
    # On Node 2/3 (join cluster)
    PRIMARY_IP="$2"
    MY_IP=$(hostname -I | awk '{print $1}')
    STORAGE_IP=$(echo $MY_IP | sed 's/10.0.10/10.0.100/')

    pvecm add $PRIMARY_IP --link0 $MY_IP --link1 $STORAGE_IP

    # Verify join successful
    pvecm status
    pvecm nodes

    echo "Node joined cluster successfully"

else
    echo "Usage:"
    echo "  Create cluster: bash cluster-create.sh create"
    echo "  Join cluster:   bash cluster-create.sh join <primary_ip>"
    exit 1
fi
