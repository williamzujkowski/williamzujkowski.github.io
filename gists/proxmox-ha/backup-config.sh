#!/bin/bash
"""
Proxmox Backup Server Integration and Automated Backup

Source: https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/
Purpose: Configure PBS integration and automated backup schedules with offsite sync
Prerequisites: Proxmox Backup Server installed on separate hardware
Usage:
    bash backup-config.sh

License: MIT
"""

BACKUP_DIR="/mnt/backup/proxmox"
DATE=$(date +%Y%m%d_%H%M%S)

# Install Proxmox Backup Server on separate hardware
# Add PBS as backup storage
pvesm add pbs pbs-backup \
    --server 10.0.10.50 \
    --datastore homelab-backups \
    --username backup@pbs \
    --password <password> \
    --fingerprint <fingerprint>

# Configure backup schedule (daily at 2 AM)
pvesh create /cluster/backup --schedule "0 2 * * *" \
    --storage pbs-backup \
    --mode snapshot \
    --compress zstd \
    --all 1 \
    --enabled 1 \
    --mailnotification failure

# Create automated backup script
cat > /usr/local/bin/cluster-backup.sh <<'SCRIPT'
#!/bin/bash
BACKUP_DIR="/mnt/backup/proxmox"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup cluster configuration
tar -czf "$BACKUP_DIR/cluster-config_$DATE.tar.gz" \
    /etc/pve \
    /etc/corosync \
    /etc/ceph

# Backup Ceph configuration
ceph config dump > "$BACKUP_DIR/ceph-config_$DATE.txt"
ceph osd tree > "$BACKUP_DIR/ceph-osd-tree_$DATE.txt"

# Sync to offsite location
rclone sync "$BACKUP_DIR" remote:proxmox-backups/

# Retention: Keep 7 days local, 30 days offsite
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete
SCRIPT

chmod +x /usr/local/bin/cluster-backup.sh

# Add to crontab (daily at 3 AM)
(crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/cluster-backup.sh") | crontab -

echo "Backup configuration complete. PBS integrated, automated backups scheduled."
