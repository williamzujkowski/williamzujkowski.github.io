# Proxmox High Availability Setup for Homelab

Building production-grade high availability Proxmox clusters on homelab hardware with shared storage, live migration, automated failover, and lessons from three failed attempts.

## Overview

This configuration provides N-1 redundancy with automatic VM failover in under 2 minutes. After implementing this architecture, my homelab achieved 99.7% uptime over 18 months.

**Source Blog Post:** [Proxmox High Availability Setup for Homelab Reliability](https://williamzujkowski.github.io/posts/proxmox-high-availability-homelab/)

## Features

- **3-node cluster** with quorum-based decision making
- **Ceph distributed storage** with 3x replication
- **Automated failover** via HA Manager
- **IPMI-based fencing** to prevent split-brain
- **Live migration** with zero downtime
- **Prometheus monitoring** with Grafana dashboards
- **Automated backups** to Proxmox Backup Server
- **Disaster recovery** procedures

## Architecture

```
Cluster Nodes:
├── pve1 (Dell R940) - Primary
├── pve2 (Dell R730) - Secondary
└── pve3 (Custom)    - Witness

Shared Storage:
└── Ceph Cluster (9 OSDs total, 3 per node)

Network:
├── Management Network: 10.0.10.0/24 (1Gb)
└── Storage Network:    10.0.100.0/24 (10Gb)

HA Services:
├── Corosync (cluster communication)
├── PVE HA Manager (failover orchestration)
└── Fencing Agents (split-brain prevention)
```

## Files

| File | Purpose | Lines |
|------|---------|-------|
| `node-prep.sh` | Node preparation and networking | ~35 |
| `cluster-create.sh` | Cluster creation and joining | ~25 |
| `corosync.conf` | Cluster communication config | ~40 |
| `ceph-install.sh` | Ceph installation and monitors | ~30 |
| `ceph-osd-setup.sh` | OSD creation and pool config | ~40 |
| `ha-manager-setup.sh` | HA manager and fencing | ~35 |
| `vm-ha-config.sh` | VM HA enablement | ~30 |
| `backup-config.sh` | PBS integration and automation | ~45 |
| `prometheus-config.yml` | Monitoring configuration | ~50 |
| `disaster-recovery.sh` | DR procedures and rebuild | ~55 |

## Quick Start

### 1. Prepare Nodes

```bash
# On all nodes
bash node-prep.sh
```

### 2. Create Cluster

```bash
# On pve1
bash cluster-create.sh create

# On pve2 and pve3
bash cluster-create.sh join 10.0.10.11
```

### 3. Install Ceph

```bash
# On pve1
bash ceph-install.sh
bash ceph-osd-setup.sh
```

### 4. Configure HA

```bash
bash ha-manager-setup.sh
```

### 5. Enable HA for VMs

```bash
bash vm-ha-config.sh 100  # VM ID 100
```

### 6. Configure Backups

```bash
bash backup-config.sh
```

### 7. Setup Monitoring

```bash
# Install Prometheus exporter
apt install -y prometheus-pve-exporter

# Configure Prometheus
cp prometheus-config.yml /etc/prometheus/prometheus.yml
systemctl restart prometheus
```

## Hardware Requirements

**Minimum (3 nodes required for quorum):**
- Node 1: 32GB RAM, 8 cores, 3x dedicated disks for Ceph
- Node 2: 24GB RAM, 6 cores, 3x dedicated disks for Ceph
- Node 3: 16GB RAM, 4 cores, 3x dedicated disks for Ceph (witness node)

**Network:**
- 2 separate networks (management + storage)
- 10Gb preferred for Ceph storage network
- 1Gb acceptable for management/corosync

**Storage:**
- 3× identical disks per node for Ceph OSDs
- NVMe recommended for journal/metadata
- Dedicated disks for Ceph (not shared with OS)

## Why Three Nodes?

Proxmox HA requires an odd number of nodes for quorum:

- **2 nodes:** Can't survive any failures (no quorum) ❌
- **3 nodes:** Survives 1 node failure ✓
- **5 nodes:** Survives 2 node failures (overkill for homelab)

## Testing Failover

### Simulated Node Failure

```bash
# Test 1: Graceful shutdown
ssh pve2 "poweroff"

# Watch HA manager migrate VMs
watch -n 1 'ha-manager status'

# Expected: VMs migrate to pve1/pve3 within 2 minutes
```

### Simulated Network Partition

```bash
# Test 2: Network isolation
ssh pve2 "iptables -A INPUT -j DROP; iptables -A OUTPUT -j DROP"

# Watch cluster response
pvecm status

# Expected: Fencing agent powers off pve2
```

### Simulated Ceph Failure

```bash
# Test 3: Stop Ceph OSD
systemctl stop ceph-osd@0

# Check Ceph status
ceph -s

# Expected: Data still accessible (redundancy)
```

## Results After 18 Months

- **Uptime:** 99.7% (2.6 days total downtime)
- **Failover time:** Average 87 seconds (target <2 min)
- **Successful failovers:** 12 automatic, 0 failed
- **False positives:** 2 (network glitches, no actual failure)
- **Maintenance windows:** 4 (rolling updates, zero user impact)

## Lessons Learned

1. **Network redundancy is critical**: Corosync ring redundancy saved us twice
2. **Fencing is mandatory**: Without IPMI fencing, split-brain scenarios are inevitable
3. **Ceph needs tuning**: Default settings caused performance issues
4. **Start small, scale up**: 3 nodes is sufficient for most homelabs
5. **Monitor everything**: Prometheus alerts caught issues before users noticed

## Monitoring Strategy

**Key Metrics:**
- Cluster quorum status (critical)
- Node availability (warning)
- Ceph health status (critical)
- VM migration events (informational)
- Backup success/failure (critical)

**Alerting Rules:**
- Cluster quorum lost → page immediately
- Node down >2 minutes → SMS alert
- Ceph degraded >5 minutes → email
- Backup failure → email
- Migration failure → page immediately

## Backup Strategy

**Daily backups:**
- All VMs snapshot to Proxmox Backup Server
- Cluster configuration to NAS
- Ceph configuration to NAS

**Retention:**
- Local: 7 days
- PBS: 30 days
- Offsite (rclone): 90 days

**Recovery Time Objectives:**
- Single VM restore: <10 minutes
- Single node rebuild: <2 hours
- Full cluster rebuild: <6 hours

## Disaster Recovery

**Scenario 1: Single Node Failure**
```bash
bash disaster-recovery.sh node pve2
```

**Scenario 2: Full Cluster Loss**
```bash
bash disaster-recovery.sh rebuild
```

**Scenario 3: Configuration Corruption**
```bash
bash disaster-recovery.sh restore /mnt/backup/proxmox/cluster-config_20251101_020000.tar.gz
```

## Common Issues

**Issue:** Cluster loses quorum randomly
**Solution:** Check network stability, increase corosync timeout

**Issue:** Ceph HEALTH_WARN status
**Solution:** Review `ceph health detail`, often scrubbing or recovery

**Issue:** VM won't migrate
**Solution:** Verify VM is on shared storage, check HA group configuration

**Issue:** Fencing fails
**Solution:** Test IPMI connectivity, verify credentials, check network path

## Maintenance Mode

```bash
# Migrate all VMs off node for maintenance
for vm in $(qm list | grep running | awk '{print $1}'); do
    ha-manager migrate $vm pve2
done

# Enter maintenance mode
ha-manager set pve1 --state maintenance

# Perform maintenance (updates, reboot, etc.)
apt update && apt full-upgrade -y
reboot

# Exit maintenance mode
ha-manager set pve1 --state online
```

## Cost Analysis

**Hardware (used Dell servers):** $2,400
**Network (10Gb switches):** $300
**UPS (redundant):** $400
**Total:** ~$3,100

**Value vs. Cloud:**
- 3 VMs x $50/month = $150/month
- Break-even: 21 months
- After 18 months: $600 saved

## Prerequisites

- Proxmox VE 8.x
- 3 physical servers with IPMI
- Managed switches with VLAN support
- Network access between all nodes
- Basic Linux administration skills

## License

MIT License - Free for personal and commercial use

## Related Resources

- [Proxmox HA Documentation](https://pve.proxmox.com/wiki/High_Availability)
- [Ceph Documentation](https://docs.ceph.com/)
- [Proxmox Backup Server](https://pbs.proxmox.com/)
- [Corosync Documentation](https://corosync.github.io/corosync/)

---

**Author:** William Zujkowski
**Blog:** https://williamzujkowski.github.io/
