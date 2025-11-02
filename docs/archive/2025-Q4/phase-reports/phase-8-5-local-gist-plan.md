# Local Gist Creation Plan - Phase 8.5

**Date:** 2025-11-01
**Objective:** Create 46 GitHub gists from local `/gists` folder structure
**Status:** Planning Complete - Ready for Execution
**Adaptation:** Modified from separate repository approach to local folder storage

---

## Executive Summary

This plan adapts the original gist creation strategy for local repository storage. Instead of creating a separate `blog-code-examples` repository, all 46 code files will be organized in `/gists` folder within the main repository, then individual GitHub gists will be created from these files.

**Key Changes from Original Plan:**
- ✅ Local `/gists` folder (not separate repository)
- ✅ Simplified workflow (no git clone needed)
- ✅ Still creates actual GitHub gists for blog post links
- ✅ Automation scripts adapted for local file access

---

## Directory Structure

```
/gists/
├── README.md                           # Overview, gist creation guide
├── security-scanning/                  # Post 1: 13 files
│   ├── README.md                       # Security scanning overview
│   ├── workflows/
│   │   ├── security-scan.yml          # Complete GitHub Actions workflow (109 lines)
│   │   ├── scheduled-scan.yml         # Daily scheduled scans (44 lines)
│   │   ├── sbom-scan.yml              # SBOM generation (38 lines)
│   │   └── auto-remediate.yml         # Auto-remediation workflow (47 lines)
│   ├── configs/
│   │   ├── grype.yaml                 # Grype configuration (21 lines)
│   │   ├── osv-scanner.toml           # OSV-Scanner config (22 lines)
│   │   └── security.rego              # Trivy OPA policy (20 lines)
│   ├── scripts/
│   │   ├── compare-scans.py           # Vulnerability comparison (59 lines)
│   │   └── send-scans-to-wazuh.sh     # Wazuh integration (19 lines)
│   └── integrations/
│       ├── slack-notification.yml     # Slack webhook payload (27 lines)
│       ├── wazuh-rules.xml            # Wazuh detection rules (18 lines)
│       ├── tasks.json                 # VS Code tasks (37 lines)
│       └── vulnerability-metrics.sql  # PostgreSQL analytics (25 lines)
│
├── mitre-dashboard/                    # Post 2: 8 files
│   ├── README.md                       # MITRE dashboard overview
│   ├── dashboard-core.py               # Main ThreatIntelligenceDashboard class (~60 lines)
│   ├── attack-data-loader.py           # ATTACKDataLoader with STIX processing (~50 lines)
│   ├── alienvault-otx-collector.py     # AlienVault OTX pulse integration (~40 lines)
│   ├── cisa-alert-mapper.py            # CISA KEV mapper (~35 lines)
│   ├── threat-profiler.py              # Threat actor profiling (~45 lines)
│   ├── technique-matcher.py            # Technique matching logic (~30 lines)
│   ├── heatmap-generator.py            # Technique heatmap visualization (~40 lines)
│   └── wazuh-alerting.py               # Alert generation (~35 lines)
│
├── vlan-segmentation/                  # Post 3: 15 files
│   ├── README.md                       # VLAN segmentation overview
│   ├── udm-pro-vlan-config.sh          # UDM Pro VLAN setup (~40 lines)
│   ├── vlan-dhcp-config.json           # DHCP reservations (~35 lines)
│   ├── management-vlan-rules.json      # Management firewall rules (~30 lines)
│   ├── iot-vlan-rules.json             # IoT isolation rules (~35 lines)
│   ├── server-vlan-rules.json          # Server VLAN rules (~30 lines)
│   ├── mdns-reflector-config.conf      # mDNS configuration (~25 lines)
│   ├── pvlan-iot-isolation.sh          # Private VLAN setup (~30 lines)
│   ├── radius-dynamic-vlan.conf        # Dynamic VLAN assignment (~35 lines)
│   ├── pihole-vlan-filtering.sh        # Pi-hole DNS filtering (~25 lines)
│   ├── dns-threat-detection.py         # DNS query analyzer (~55 lines)
│   ├── netflow-vlan-analysis.sh        # NetFlow configuration (~30 lines)
│   ├── vlan-traffic-monitor.py         # Traffic pattern analysis (~50 lines)
│   ├── vlan-connectivity-tests.sh      # Connectivity tests (~40 lines)
│   ├── vlan-breakout-tests.sh          # Penetration testing (~45 lines)
│   ├── vlan-troubleshooting.sh         # Troubleshooting guide (~35 lines)
│   └── vlan-performance-tuning.sh      # Performance optimization (~30 lines)
│
└── proxmox-ha/                         # Post 4: 10 files
    ├── README.md                       # Proxmox HA overview
    ├── node-prep.sh                    # Node preparation (~35 lines)
    ├── cluster-create.sh               # Cluster creation (~25 lines)
    ├── corosync.conf                   # Corosync configuration (~40 lines)
    ├── ceph-install.sh                 # Ceph installation (~30 lines)
    ├── ceph-osd-setup.sh               # OSD configuration (~40 lines)
    ├── ha-manager-setup.sh             # HA manager configuration (~35 lines)
    ├── vm-ha-config.sh                 # VM HA settings (~30 lines)
    ├── backup-config.sh                # Backup configuration (~45 lines)
    ├── prometheus-config.yml           # Prometheus setup (~50 lines)
    └── disaster-recovery.sh            # DR procedures (~55 lines)
```

**Total:** 46 code files + 4 READMEs = 50 files

---

## Complete File Inventory (46 Files)

### Post 1: Automated Security Scanning Pipeline (13 files, ~854 lines)

| # | Filename | Lines | Description | Gist Slug |
|---|----------|-------|-------------|-----------|
| 1 | security-scan.yml | 109 | Complete GitHub Actions security workflow | security-scan-workflow-complete |
| 2 | scheduled-scan.yml | 44 | Daily scheduled security scans | scheduled-security-scans |
| 3 | sbom-scan.yml | 38 | SBOM generation workflow | sbom-generation-workflow |
| 4 | auto-remediate.yml | 47 | Auto-remediation workflow | auto-remediate-vulnerabilities |
| 5 | grype.yaml | 21 | Grype configuration | grype-config |
| 6 | osv-scanner.toml | 22 | OSV-Scanner configuration | osv-scanner-config |
| 7 | security.rego | 20 | Trivy OPA policy | trivy-opa-policy |
| 8 | compare-scans.py | 59 | Vulnerability comparison script | vulnerability-scan-comparison |
| 9 | send-scans-to-wazuh.sh | 19 | Wazuh integration | wazuh-vulnerability-ingestion |
| 10 | slack-notification.yml | 27 | Slack webhook payload | security-scan-slack-notification |
| 11 | wazuh-rules.xml | 18 | Wazuh detection rules | wazuh-vulnerability-rules |
| 12 | tasks.json | 37 | VS Code tasks | vscode-security-scan-tasks |
| 13 | vulnerability-metrics.sql | 25 | PostgreSQL analytics | vulnerability-metrics-sql |

### Post 2: MITRE ATT&CK Dashboard (8 files, ~443 lines)

| # | Filename | Lines | Description | Gist Slug |
|---|----------|-------|-------------|-----------|
| 14 | dashboard-core.py | 60 | Main ThreatIntelligenceDashboard class | mitre-dashboard-core |
| 15 | attack-data-loader.py | 50 | ATTACKDataLoader with STIX processing | attack-data-loader |
| 16 | alienvault-otx-collector.py | 40 | AlienVault OTX pulse integration | alienvault-otx-collector |
| 17 | cisa-alert-mapper.py | 35 | CISA KEV mapper | cisa-alert-mapper |
| 18 | threat-profiler.py | 45 | Threat actor profiling | threat-actor-profiler |
| 19 | technique-matcher.py | 30 | Technique matching logic | technique-matcher |
| 20 | heatmap-generator.py | 40 | Technique heatmap visualization | mitre-heatmap-generator |
| 21 | wazuh-alerting.py | 35 | Wazuh MITRE alerting | wazuh-mitre-alerting |

### Post 3: Zero Trust VLAN Segmentation (15 files, ~660 lines)

| # | Filename | Lines | Description | Gist Slug |
|---|----------|-------|-------------|-----------|
| 22 | udm-pro-vlan-config.sh | 40 | UDM Pro VLAN setup | udm-pro-vlan-config |
| 23 | vlan-dhcp-config.json | 35 | DHCP reservations | vlan-dhcp-config |
| 24 | management-vlan-rules.json | 30 | Management firewall rules | management-vlan-rules |
| 25 | iot-vlan-rules.json | 35 | IoT isolation rules | iot-vlan-rules |
| 26 | server-vlan-rules.json | 30 | Server VLAN rules | server-vlan-rules |
| 27 | mdns-reflector-config.conf | 25 | mDNS configuration | mdns-reflector-config |
| 28 | pvlan-iot-isolation.sh | 30 | Private VLAN setup | pvlan-iot-isolation |
| 29 | radius-dynamic-vlan.conf | 35 | Dynamic VLAN assignment | radius-dynamic-vlan |
| 30 | pihole-vlan-filtering.sh | 25 | Pi-hole DNS filtering | pihole-vlan-filtering |
| 31 | dns-threat-detection.py | 55 | DNS query analyzer | dns-threat-detection |
| 32 | netflow-vlan-analysis.sh | 30 | NetFlow configuration | netflow-vlan-analysis |
| 33 | vlan-traffic-monitor.py | 50 | Traffic pattern analysis | vlan-traffic-monitor |
| 34 | vlan-connectivity-tests.sh | 40 | Connectivity tests | vlan-connectivity-tests |
| 35 | vlan-breakout-tests.sh | 45 | Penetration testing | vlan-breakout-tests |
| 36 | vlan-troubleshooting.sh | 35 | Troubleshooting guide | vlan-troubleshooting |
| 37 | vlan-performance-tuning.sh | 30 | Performance optimization | vlan-performance-tuning |

### Post 4: Proxmox High Availability (10 files, ~714 lines)

| # | Filename | Lines | Description | Gist Slug |
|---|----------|-------|-------------|-----------|
| 38 | node-prep.sh | 35 | Node preparation | proxmox-node-prep |
| 39 | cluster-create.sh | 25 | Cluster creation | proxmox-cluster-create |
| 40 | corosync.conf | 40 | Corosync configuration | proxmox-corosync-config |
| 41 | ceph-install.sh | 30 | Ceph installation | proxmox-ceph-install |
| 42 | ceph-osd-setup.sh | 40 | OSD configuration | proxmox-ceph-osd-setup |
| 43 | ha-manager-setup.sh | 35 | HA manager configuration | proxmox-ha-manager-config |
| 44 | vm-ha-config.sh | 30 | VM HA settings | proxmox-vm-ha-config |
| 45 | backup-config.sh | 45 | Backup configuration | proxmox-backup-config |
| 46 | prometheus-config.yml | 50 | Prometheus setup | proxmox-prometheus-config |
| 47 | disaster-recovery.sh | 55 | DR procedures | proxmox-disaster-recovery |

**Note:** File #47 brings total to 47, not 46 (slight discrepancy from original estimate)

---

## Simplified Workflow (Local Folder Approach)

### Step 1: Create Local Files
```bash
# Files already exist in /gists directory structure
# Just need to verify organization
ls -R /gists/
```

### Step 2: Create GitHub Gists
```bash
# For each file, create gist using gh CLI:
gh gist create -d "Description" -f filename /gists/category/filename

# Example:
gh gist create -d "Complete GitHub Actions security scanning workflow" \
  -f security-scan.yml \
  /gists/security-scanning/workflows/security-scan.yml
```

### Step 3: Capture Gist URLs
```bash
# Gist URL returned by gh CLI:
https://gist.github.com/williamzujkowski/a1b2c3d4e5f6
```

### Step 4: Update Mapping File
```bash
# Save mapping to gists/gist-mapping.json
{
  "security-scanning/workflows/security-scan.yml": "https://gist.github.com/williamzujkowski/a1b2c3d4e5f6"
}
```

### Step 5: Update Blog Posts
```bash
# Replace placeholder URLs in blog posts with actual gist URLs
# Example:
# Before: https://gist.github.com/williamzujkowski/security-scan-workflow-complete
# After:  https://gist.github.com/williamzujkowski/a1b2c3d4e5f6
```

---

## Automation Script Design

### Script: `scripts/create-gists-from-folder.py`

```python
#!/usr/bin/env python3
"""
Create GitHub gists from local /gists folder structure.

This script:
1. Scans /gists directory for code files
2. Reads each file and creates a GitHub gist via gh CLI
3. Generates URL mapping file (gist-mapping.json)
4. Optionally updates blog posts with real gist URLs
"""

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Tuple
import time

# Gist metadata organized by post category
GIST_METADATA = {
    # Post 1: Security Scanning (13 files)
    "security-scanning/workflows/security-scan.yml": {
        "description": "Complete GitHub Actions security scanning workflow with Grype, OSV-Scanner, Trivy",
        "slug": "security-scan-workflow-complete"
    },
    "security-scanning/workflows/scheduled-scan.yml": {
        "description": "Daily scheduled security scans with matrix strategy and SIEM integration",
        "slug": "scheduled-security-scans"
    },
    "security-scanning/workflows/sbom-scan.yml": {
        "description": "SBOM generation workflow with CycloneDX and GitHub release upload",
        "slug": "sbom-generation-workflow"
    },
    "security-scanning/workflows/auto-remediate.yml": {
        "description": "Weekly scheduled auto-remediation with OSV scanning and PR creation",
        "slug": "auto-remediate-vulnerabilities"
    },
    "security-scanning/configs/grype.yaml": {
        "description": "Grype vulnerability scanner configuration with ignore rules and severity thresholds",
        "slug": "grype-config"
    },
    "security-scanning/configs/osv-scanner.toml": {
        "description": "OSV-Scanner configuration with ignore rules and parallel scanning",
        "slug": "osv-scanner-config"
    },
    "security-scanning/configs/security.rego": {
        "description": "Trivy OPA policy with critical deny rules and high severity warnings",
        "slug": "trivy-opa-policy"
    },
    "security-scanning/scripts/compare-scans.py": {
        "description": "Python script for vulnerability scan comparison and alerting",
        "slug": "vulnerability-scan-comparison"
    },
    "security-scanning/scripts/send-scans-to-wazuh.sh": {
        "description": "Bash script for Wazuh vulnerability ingestion via syslog",
        "slug": "wazuh-vulnerability-ingestion"
    },
    "security-scanning/integrations/slack-notification.yml": {
        "description": "Slack webhook payload with formatted blocks and repository details",
        "slug": "security-scan-slack-notification"
    },
    "security-scanning/integrations/wazuh-rules.xml": {
        "description": "Wazuh detection rules for vulnerability scanning",
        "slug": "wazuh-vulnerability-rules"
    },
    "security-scanning/integrations/tasks.json": {
        "description": "VS Code tasks.json with Grype, OSV, and combined scan tasks",
        "slug": "vscode-security-scan-tasks"
    },
    "security-scanning/integrations/vulnerability-metrics.sql": {
        "description": "PostgreSQL analytics for vulnerability metrics and trends",
        "slug": "vulnerability-metrics-sql"
    },

    # Post 2: MITRE Dashboard (8 files)
    "mitre-dashboard/dashboard-core.py": {
        "description": "Main ThreatIntelligenceDashboard class with Flask backend",
        "slug": "mitre-dashboard-core"
    },
    "mitre-dashboard/attack-data-loader.py": {
        "description": "ATTACKDataLoader with STIX processing and technique extraction",
        "slug": "attack-data-loader"
    },
    "mitre-dashboard/alienvault-otx-collector.py": {
        "description": "AlienVault OTX pulse integration with IoC extraction",
        "slug": "alienvault-otx-collector"
    },
    "mitre-dashboard/cisa-alert-mapper.py": {
        "description": "CISA Known Exploited Vulnerabilities mapper linking CVEs to MITRE techniques",
        "slug": "cisa-alert-mapper"
    },
    "mitre-dashboard/threat-profiler.py": {
        "description": "Threat actor profiling with technique frequency analysis",
        "slug": "threat-actor-profiler"
    },
    "mitre-dashboard/technique-matcher.py": {
        "description": "Technique matching logic correlating observed TTPs with MITRE framework",
        "slug": "technique-matcher"
    },
    "mitre-dashboard/heatmap-generator.py": {
        "description": "Technique heatmap generation using Plotly visualization",
        "slug": "mitre-heatmap-generator"
    },
    "mitre-dashboard/wazuh-alerting.py": {
        "description": "Wazuh integration for MITRE technique-based alerting",
        "slug": "wazuh-mitre-alerting"
    },

    # Post 3: VLAN Segmentation (15 files)
    "vlan-segmentation/udm-pro-vlan-config.sh": {
        "description": "UDM Pro VLAN creation, tagging, and trunk port configuration",
        "slug": "udm-pro-vlan-config"
    },
    "vlan-segmentation/vlan-dhcp-config.json": {
        "description": "DHCP server configuration with reservations and custom options",
        "slug": "vlan-dhcp-config"
    },
    "vlan-segmentation/management-vlan-rules.json": {
        "description": "UDM Pro firewall rules for management VLAN with logging",
        "slug": "management-vlan-rules"
    },
    "vlan-segmentation/iot-vlan-rules.json": {
        "description": "Full IoT isolation rules with default-deny policy",
        "slug": "iot-vlan-rules"
    },
    "vlan-segmentation/server-vlan-rules.json": {
        "description": "Server VLAN firewall rules with update policies",
        "slug": "server-vlan-rules"
    },
    "vlan-segmentation/mdns-reflector-config.conf": {
        "description": "Avahi mDNS reflector configuration for cross-VLAN service discovery",
        "slug": "mdns-reflector-config"
    },
    "vlan-segmentation/pvlan-iot-isolation.sh": {
        "description": "Private VLAN setup for IoT isolation with promiscuous/isolated ports",
        "slug": "pvlan-iot-isolation"
    },
    "vlan-segmentation/radius-dynamic-vlan.conf": {
        "description": "FreeRADIUS dynamic VLAN assignment based on 802.1X authentication",
        "slug": "radius-dynamic-vlan"
    },
    "vlan-segmentation/pihole-vlan-filtering.sh": {
        "description": "Pi-hole DNS filtering with VLAN-specific blocklists",
        "slug": "pihole-vlan-filtering"
    },
    "vlan-segmentation/dns-threat-detection.py": {
        "description": "Full DNS query analyzer with threat detection and alerting",
        "slug": "dns-threat-detection"
    },
    "vlan-segmentation/netflow-vlan-analysis.sh": {
        "description": "NetFlow v9 configuration for VLAN traffic monitoring",
        "slug": "netflow-vlan-analysis"
    },
    "vlan-segmentation/vlan-traffic-monitor.py": {
        "description": "VLAN traffic monitor with anomaly detection and multiple alert channels",
        "slug": "vlan-traffic-monitor"
    },
    "vlan-segmentation/vlan-connectivity-tests.sh": {
        "description": "VLAN segmentation test suite with ping sweep and port scanning",
        "slug": "vlan-connectivity-tests"
    },
    "vlan-segmentation/vlan-breakout-tests.sh": {
        "description": "VLAN breakout testing with nmap and metasploit",
        "slug": "vlan-breakout-tests"
    },
    "vlan-segmentation/vlan-troubleshooting.sh": {
        "description": "Common troubleshooting commands for VLAN issues",
        "slug": "vlan-troubleshooting"
    },
    "vlan-segmentation/vlan-performance-tuning.sh": {
        "description": "Hardware offloading and VLAN performance tuning",
        "slug": "vlan-performance-tuning"
    },

    # Post 4: Proxmox HA (10 files)
    "proxmox-ha/node-prep.sh": {
        "description": "Node preparation script with hostname, networking, SSH keys",
        "slug": "proxmox-node-prep"
    },
    "proxmox-ha/cluster-create.sh": {
        "description": "Cluster creation with pvecm and node joining",
        "slug": "proxmox-cluster-create"
    },
    "proxmox-ha/corosync.conf": {
        "description": "Corosync configuration with ring redundancy",
        "slug": "proxmox-corosync-config"
    },
    "proxmox-ha/ceph-install.sh": {
        "description": "Ceph installation script with monitor deployment",
        "slug": "proxmox-ceph-install"
    },
    "proxmox-ha/ceph-osd-setup.sh": {
        "description": "OSD creation and pool configuration with replication settings",
        "slug": "proxmox-ceph-osd-setup"
    },
    "proxmox-ha/ha-manager-setup.sh": {
        "description": "HA manager configuration with resource groups",
        "slug": "proxmox-ha-manager-config"
    },
    "proxmox-ha/vm-ha-config.sh": {
        "description": "VM HA configuration with priority settings and failover tests",
        "slug": "proxmox-vm-ha-config"
    },
    "proxmox-ha/backup-config.sh": {
        "description": "Proxmox Backup Server integration with retention policies",
        "slug": "proxmox-backup-config"
    },
    "proxmox-ha/prometheus-config.yml": {
        "description": "Prometheus configuration for Proxmox metrics with alerting",
        "slug": "proxmox-prometheus-config"
    },
    "proxmox-ha/disaster-recovery.sh": {
        "description": "DR procedures with cluster rebuild and node recovery",
        "slug": "proxmox-disaster-recovery"
    }
}


def create_gist(filepath: Path, description: str, slug: str) -> str:
    """
    Create GitHub gist using gh CLI.

    Args:
        filepath: Path to file to gist
        description: Gist description
        slug: Gist slug for reference

    Returns:
        Gist URL string
    """
    # Construct gh CLI command
    cmd = [
        "gh", "gist", "create",
        str(filepath),
        "--desc", description,
        "--public"
    ]

    print(f"  Creating gist: {slug}...")
    print(f"    File: {filepath.name}")
    print(f"    Description: {description}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        gist_url = result.stdout.strip()
        print(f"    ✅ Created: {gist_url}")
        return gist_url

    except subprocess.CalledProcessError as e:
        print(f"    ❌ Error: {e.stderr}")
        raise


def scan_gist_files(base_dir: Path) -> List[Path]:
    """
    Scan /gists directory for code files.

    Args:
        base_dir: Base gists directory (/gists)

    Returns:
        List of code file paths (excluding READMEs)
    """
    code_files = []

    # Exclude READMEs and only include actual code files
    exclude_patterns = ["README.md", ".DS_Store", "__pycache__"]

    for filepath in base_dir.rglob("*"):
        if filepath.is_file():
            # Skip excluded patterns
            if any(pattern in str(filepath) for pattern in exclude_patterns):
                continue

            # Get relative path from base_dir
            rel_path = filepath.relative_to(base_dir)
            code_files.append(rel_path)

    return sorted(code_files)


def main():
    """Main gist creation workflow."""
    print("🚀 GitHub Gist Creation Tool")
    print("=" * 60)

    # Configuration
    BASE_DIR = Path("/home/william/git/williamzujkowski.github.io/gists")
    MAPPING_FILE = BASE_DIR / "gist-mapping.json"

    # Verify base directory exists
    if not BASE_DIR.exists():
        print(f"❌ Error: {BASE_DIR} does not exist")
        return 1

    # Scan for code files
    print(f"\n📂 Scanning {BASE_DIR} for code files...")
    code_files = scan_gist_files(BASE_DIR)
    print(f"   Found {len(code_files)} code files")

    # Create gists
    created_gists = {}
    failed_gists = []

    print(f"\n📎 Creating {len(GIST_METADATA)} gists...")
    print("=" * 60)

    for i, (rel_path, metadata) in enumerate(GIST_METADATA.items(), 1):
        filepath = BASE_DIR / rel_path

        print(f"\n[{i}/{len(GIST_METADATA)}] {rel_path}")

        # Check if file exists
        if not filepath.exists():
            print(f"  ⚠️  File not found: {filepath}")
            failed_gists.append(rel_path)
            continue

        try:
            gist_url = create_gist(
                filepath,
                metadata["description"],
                metadata["slug"]
            )

            created_gists[rel_path] = {
                "url": gist_url,
                "slug": metadata["slug"],
                "description": metadata["description"]
            }

            # Rate limiting: 1 second delay between gist creations
            time.sleep(1)

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed_gists.append(rel_path)

    # Save mapping
    print(f"\n💾 Saving gist mapping to {MAPPING_FILE}...")
    with open(MAPPING_FILE, "w") as f:
        json.dump(created_gists, f, indent=2)
    print(f"   ✅ Mapping saved")

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Created:  {len(created_gists)} gists")
    print(f"❌ Failed:   {len(failed_gists)} gists")
    print(f"📝 Mapping:  {MAPPING_FILE}")

    if failed_gists:
        print("\n⚠️  Failed gists:")
        for path in failed_gists:
            print(f"  - {path}")
        return 1

    print("\n✅ All gists created successfully!")
    print("\nNext steps:")
    print("1. Review gist-mapping.json")
    print("2. Update blog posts with real gist URLs")
    print("3. Validate all links work")
    print("4. Run npm run build")

    return 0


if __name__ == "__main__":
    exit(main())
```

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1 | Organize local /gists folder | 1h | 1h |
| 2 | Extract code from git history | 2h | 3h |
| 3 | Create code files in /gists | 3h | 6h |
| 4 | Add documentation headers | 2h | 8h |
| 5 | Run gist creation script | 1h | 9h |
| 6 | Update blog posts with URLs | 2h | 11h |
| 7 | Validation & testing | 1h | 12h |
| **Total** | **Complete workflow** | **12h** | - |

**Simplified from original 13 hours** by eliminating separate repository overhead.

---

## Step-by-Step Execution Guide

### Phase 1: Verify Local Directory Structure (15 minutes)

```bash
# Check current /gists directory
cd /home/william/git/williamzujkowski.github.io
ls -R gists/

# Verify directory structure matches plan
tree -L 2 gists/
```

### Phase 2: Extract Code from Git History (2 hours)

```bash
# Use git show to extract original code from pre-optimization commits
# Security scanning (commit b56c988)
git show b56c988:src/posts/2025-10-06-automated-security-scanning-pipeline.md > /tmp/security-post.md

# MITRE dashboard (commit before eae5dd2)
git show eae5dd2~1:src/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard.md > /tmp/mitre-post.md

# VLAN segmentation (commit before eae5dd2)
git show eae5dd2~1:src/posts/2025-09-08-zero-trust-vlan-segmentation-homelab.md > /tmp/vlan-post.md

# Proxmox HA (commit before eae5dd2)
git show eae5dd2~1:src/posts/2025-09-29-proxmox-high-availability-homelab.md > /tmp/proxmox-post.md

# Manual extraction: Parse Markdown code blocks and save to appropriate files
```

### Phase 3: Create Code Files in /gists (3 hours)

```bash
# Create all necessary subdirectories
mkdir -p gists/security-scanning/{workflows,configs,scripts,integrations}
mkdir -p gists/mitre-dashboard
mkdir -p gists/vlan-segmentation
mkdir -p gists/proxmox-ha

# For each extracted code block:
# 1. Add descriptive header comment
# 2. Save to appropriate file in /gists
# 3. Verify syntax (if applicable)

# Example for security-scan.yml:
cat > gists/security-scanning/workflows/security-scan.yml <<'EOF'
# Complete GitHub Actions Security Scanning Workflow
# Source: https://williamzujkowski.com/blog/automated-security-scanning-pipeline
# Tools: Grype, OSV-Scanner, Trivy, SARIF
# Features: Quality gates, Slack notifications, SIEM integration

name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
  schedule:
    - cron: '0 0 * * *'

# ... (rest of workflow)
EOF
```

### Phase 4: Add Documentation Headers (2 hours)

```bash
# For each file, add standardized header:
# - Purpose/description
# - Source blog post link
# - Prerequisites
# - Usage instructions
# - License

# Example template:
cat > gists/security-scanning/configs/grype.yaml <<'EOF'
# Grype Vulnerability Scanner Configuration
#
# Source: https://williamzujkowski.com/blog/automated-security-scanning-pipeline
# Tool: Anchore Grype
# Purpose: Configure vulnerability scanning with ignore rules and severity thresholds
#
# Usage:
#   grype dir:. --config .grype.yaml
#
# Prerequisites:
#   - Grype installed: curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh
#
# License: MIT

# ... (actual configuration)
EOF
```

### Phase 5: Run Gist Creation Script (1 hour)

```bash
# Ensure gh CLI is authenticated
gh auth status

# Run gist creation script
python scripts/create-gists-from-folder.py

# Expected output:
# 🚀 GitHub Gist Creation Tool
# ============================================================
# 📂 Scanning /gists for code files...
#    Found 46 code files
# 📎 Creating 46 gists...
# ============================================================
# [1/46] security-scanning/workflows/security-scan.yml
#   Creating gist: security-scan-workflow-complete...
#   ✅ Created: https://gist.github.com/williamzujkowski/a1b2c3d4e5f6
# ...
# 📊 SUMMARY
# ============================================================
# ✅ Created:  46 gists
# ❌ Failed:   0 gists
# 📝 Mapping:  /gists/gist-mapping.json

# Verify mapping file
cat gists/gist-mapping.json | jq 'keys | length'  # Should be 46
```

### Phase 6: Update Blog Posts (2 hours)

```bash
# Create script to update blog post URLs
cat > scripts/update-blog-gist-urls.py <<'EOF'
#!/usr/bin/env python3
"""Update blog posts with real gist URLs from mapping file."""

import json
import re
from pathlib import Path

MAPPING_FILE = Path("/home/william/git/williamzujkowski.github.io/gists/gist-mapping.json")
POSTS_DIR = Path("/home/william/git/williamzujkowski.github.io/src/posts")

BLOG_POSTS = {
    "2025-10-06-automated-security-scanning-pipeline.md": "security-scanning",
    "2025-09-14-threat-intelligence-mitre-attack-dashboard.md": "mitre-dashboard",
    "2025-09-08-zero-trust-vlan-segmentation-homelab.md": "vlan-segmentation",
    "2025-09-29-proxmox-high-availability-homelab.md": "proxmox-ha"
}

def load_mapping():
    with open(MAPPING_FILE) as f:
        return json.load(f)

def update_post(post_path: Path, mapping: dict, category: str):
    """Replace placeholder gist URLs with actual URLs."""
    content = post_path.read_text()

    # Find all placeholder gist URLs
    pattern = r'https://gist\.github\.com/williamzujkowski/([a-z0-9-]+)'

    replacements = 0
    for rel_path, gist_data in mapping.items():
        if category in rel_path:
            slug = gist_data["slug"]
            url = gist_data["url"]

            # Replace placeholder with actual URL
            old_url = f"https://gist.github.com/williamzujkowski/{slug}"
            if old_url in content:
                content = content.replace(old_url, url)
                replacements += 1
                print(f"  ✅ Replaced {slug}")

    # Write updated content
    post_path.write_text(content)
    return replacements

def main():
    mapping = load_mapping()

    for post_filename, category in BLOG_POSTS.items():
        post_path = POSTS_DIR / post_filename
        print(f"\n📝 Updating {post_filename}...")

        replacements = update_post(post_path, mapping, category)
        print(f"   {replacements} URLs updated")

    print("\n✅ All blog posts updated")

if __name__ == "__main__":
    main()
EOF

# Run update script
python scripts/update-blog-gist-urls.py
```

### Phase 7: Validation & Testing (1 hour)

```bash
# Validate all gist links work
python scripts/validate-gist-links.py

# Build site to check for broken links
npm run build

# Manual testing:
# 1. Open each blog post in browser
# 2. Click every gist link (verify opens in new tab)
# 3. Check syntax highlighting works
# 4. Test "Raw" download button
# 5. Verify mobile rendering
```

---

## Success Criteria

**Phase 8.5 Complete When:**
- ✅ All 46 code files created in `/gists` directory
- ✅ All 46 GitHub gists created successfully
- ✅ `gist-mapping.json` contains all URL mappings
- ✅ All blog posts updated with real gist URLs
- ✅ `npm run build` passes without errors
- ✅ All gist links verified functional
- ✅ Documentation complete (READMEs in each category)

**Measurement:**
- 0 broken gist links
- 100% code coverage (all 46 files mapped to gists)
- <2 seconds average gist load time
- All code files have descriptive headers
- Mapping file is version controlled

---

## Risk Mitigation

### Risk: GitHub API Rate Limits
**Mitigation:**
- 1 second delay between gist creations (60 gists/hour)
- Use personal access token with higher limits
- `gh` CLI has better rate limiting than raw API

### Risk: Missing Code Files
**Mitigation:**
- Extract from correct git commits (verified hashes)
- Manual review of each extracted code block
- Compare line counts with original estimate

### Risk: Broken Blog Post Links
**Mitigation:**
- Create all gists before updating blog posts
- Keep mapping file for rollback if needed
- Automated link validation before deployment

### Risk: File Organization Errors
**Mitigation:**
- Clear directory structure documented
- Script validates file paths exist
- Manual verification of first 5 gists

---

## Next Steps

1. **Immediate (Today):**
   - Verify `/gists` directory structure
   - Extract code from git history
   - Create first 5 code files (security-scanning workflows)

2. **Short-term (This Week):**
   - Create all 46 code files in `/gists`
   - Add documentation headers
   - Run gist creation script
   - Update first blog post (security scanning)

3. **Medium-term (Next Week):**
   - Update remaining 3 blog posts
   - Comprehensive validation
   - Deploy to production
   - Monitor for broken links

4. **Long-term (This Month):**
   - Add tests to code examples
   - Create usage tutorials
   - Monitor gist view analytics
   - Gather reader feedback

---

## Conclusion

This adapted plan simplifies the original approach by using local `/gists` folder storage instead of a separate repository. The workflow is streamlined to:

1. Create code files locally in organized directory structure
2. Use automation script to batch-create GitHub gists
3. Generate URL mapping file
4. Update blog posts with real gist URLs
5. Validate everything works

**Key Advantages of Local Approach:**
- ✅ No separate repository overhead
- ✅ Easier to maintain in same git repo
- ✅ Simplified workflow (no git clone needed)
- ✅ Still creates shareable GitHub gists for blog posts
- ✅ Single source of truth in main repository

**Total Effort:** 12 hours (vs 13 hours for separate repository)

**Expected Outcomes:**
- 46 high-quality GitHub gists
- Zero broken links in blog posts
- Better reader experience (copy-paste ready code)
- Portfolio of reusable homelab configurations
- Improved blog post credibility

---

**Ready for execution.** Recommend starting with Phase 2 (code extraction) today.
