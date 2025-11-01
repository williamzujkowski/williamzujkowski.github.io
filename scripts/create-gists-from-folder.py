#!/usr/bin/env -S uv run python3
"""
Create GitHub gists from local /gists directory.

This script scans the /gists folder, creates GitHub gists for each code file,
and generates a mapping file (gist-mapping.json) for blog post URL updates.

Usage:
    python scripts/create-gists-from-folder.py [--dry-run] [--test-only]

Options:
    --dry-run: Print actions without creating gists
    --test-only: Only create gists for first 3 files (testing mode)

Prerequisites:
    - gh CLI installed and authenticated (gh auth login)
    - /gists directory with code files

License: MIT
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional


# Gist metadata organized by post category (45 files total)
GIST_METADATA = {
    # Post 1: Security Scanning (13 files)
    "security-scanning/workflows/security-scan-workflow-complete.yml": {
        "description": "Complete GitHub Actions security scanning workflow with Grype, OSV-Scanner, Trivy",
        "slug": "security-scan-workflow-complete"
    },
    "security-scanning/workflows/scheduled-security-scans.yml": {
        "description": "Daily scheduled security scans with matrix strategy and SIEM integration",
        "slug": "scheduled-security-scans"
    },
    "security-scanning/workflows/sbom-generation-workflow.yml": {
        "description": "SBOM generation workflow with CycloneDX and GitHub release upload",
        "slug": "sbom-generation-workflow"
    },
    "security-scanning/workflows/auto-remediate-vulnerabilities.yml": {
        "description": "Weekly scheduled auto-remediation with OSV scanning and PR creation",
        "slug": "auto-remediate-vulnerabilities"
    },
    "security-scanning/configs/grype-config.yaml": {
        "description": "Grype vulnerability scanner configuration with ignore rules and severity thresholds",
        "slug": "grype-config"
    },
    "security-scanning/configs/osv-scanner-config.toml": {
        "description": "OSV-Scanner configuration with ignore rules and parallel scanning",
        "slug": "osv-scanner-config"
    },
    "security-scanning/configs/trivy-opa-policy.rego": {
        "description": "Trivy OPA policy with critical deny rules and high severity warnings",
        "slug": "trivy-opa-policy"
    },
    "security-scanning/scripts/vulnerability-scan-comparison.py": {
        "description": "Python script for vulnerability scan comparison and alerting",
        "slug": "vulnerability-scan-comparison"
    },
    "security-scanning/scripts/wazuh-vulnerability-ingestion.sh": {
        "description": "Bash script for Wazuh vulnerability ingestion via syslog",
        "slug": "wazuh-vulnerability-ingestion"
    },
    "security-scanning/integrations/security-scan-slack-notification.yml": {
        "description": "Slack webhook payload with formatted blocks and repository details",
        "slug": "security-scan-slack-notification"
    },
    "security-scanning/integrations/wazuh-vulnerability-rules.xml": {
        "description": "Wazuh detection rules for vulnerability scanning",
        "slug": "wazuh-vulnerability-rules"
    },
    "security-scanning/integrations/vscode-security-scan-tasks.json": {
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
    "mitre-dashboard/alienvault-collector.py": {
        "description": "AlienVault OTX pulse integration with IoC extraction",
        "slug": "alienvault-collector"
    },
    "mitre-dashboard/cisa-alert-mapper.py": {
        "description": "CISA Known Exploited Vulnerabilities mapper linking CVEs to MITRE techniques",
        "slug": "cisa-alert-mapper"
    },
    "mitre-dashboard/threat-actor-profiler.py": {
        "description": "Threat actor profiling with technique frequency analysis",
        "slug": "threat-actor-profiler"
    },
    "mitre-dashboard/dashboard-main.py": {
        "description": "Main dashboard entry point with Flask application setup",
        "slug": "dashboard-main"
    },
    "mitre-dashboard/threat-visualizer.py": {
        "description": "Technique heatmap generation using Plotly visualization",
        "slug": "threat-visualizer"
    },
    "mitre-dashboard/threat-alerting.py": {
        "description": "Wazuh integration for MITRE technique-based alerting",
        "slug": "threat-alerting"
    },

    # Post 3: VLAN Segmentation (14 files)
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


def check_gh_auth() -> bool:
    """Check if gh CLI is authenticated."""
    try:
        result = subprocess.run(
            ["gh", "auth", "status"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ Error: gh CLI not found. Install with: sudo apt install gh")
        return False


def create_gist(filepath: Path, description: str, slug: str, dry_run: bool = False) -> Optional[str]:
    """
    Create GitHub gist using gh CLI.

    Args:
        filepath: Path to file to gist
        description: Gist description
        slug: Gist slug for reference
        dry_run: If True, print command without executing

    Returns:
        Gist URL string or None on failure
    """
    # Construct gh CLI command
    cmd = [
        "gh", "gist", "create",
        "--public",
        "--desc", description,
        "--filename", filepath.name,
        str(filepath)
    ]

    if dry_run:
        print(f"  [DRY RUN] Would create gist: {slug}")
        print(f"    File: {filepath.name}")
        print(f"    Description: {description}")
        print(f"    Command: {' '.join(cmd)}")
        return f"https://gist.github.com/williamzujkowski/DRY_RUN_{slug}"

    print(f"  Creating gist: {slug}...")
    print(f"    File: {filepath.name}")
    print(f"    Description: {description[:80]}...")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
            timeout=30
        )

        gist_url = result.stdout.strip()
        print(f"    ✅ Created: {gist_url}")
        return gist_url

    except subprocess.TimeoutExpired:
        print(f"    ❌ Error: Timeout creating gist (30s)")
        return None
    except subprocess.CalledProcessError as e:
        print(f"    ❌ Error: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"    ❌ Unexpected error: {e}")
        return None


def main():
    """Main gist creation workflow."""
    parser = argparse.ArgumentParser(
        description="Create GitHub gists from /gists directory"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without creating gists"
    )
    parser.add_argument(
        "--test-only",
        action="store_true",
        help="Only create gists for first 3 files (testing mode)"
    )
    args = parser.parse_args()

    print("🚀 GitHub Gist Creation Tool")
    print("=" * 60)

    # Configuration
    BASE_DIR = Path("/home/william/git/williamzujkowski.github.io/gists")
    MAPPING_FILE = BASE_DIR / "gist-mapping.json"

    # Verify base directory exists
    if not BASE_DIR.exists():
        print(f"❌ Error: {BASE_DIR} does not exist")
        print(f"   Create it with: mkdir -p {BASE_DIR}")
        return 1

    # Check gh authentication (skip in dry-run)
    if not args.dry_run:
        print("\n🔑 Checking gh CLI authentication...")
        if not check_gh_auth():
            print("❌ Error: gh CLI not authenticated")
            print("   Run: gh auth login")
            return 1
        print("   ✅ Authenticated")

    # Determine how many gists to create
    total_count = len(GIST_METADATA)
    if args.test_only:
        total_count = min(3, total_count)
        print(f"\n⚠️  TEST MODE: Only creating first {total_count} gists")

    # Create gists
    created_gists = {}
    failed_gists = []
    start_time = time.time()

    print(f"\n📎 Creating {total_count} gists...")
    if args.dry_run:
        print("   (DRY RUN MODE - no actual gists will be created)")
    print("=" * 60)

    for i, (rel_path, metadata) in enumerate(list(GIST_METADATA.items())[:total_count], 1):
        filepath = BASE_DIR / rel_path

        print(f"\n[{i}/{total_count}] {rel_path}")

        # Check if file exists
        if not filepath.exists():
            print(f"  ⚠️  File not found: {filepath}")
            failed_gists.append({"path": rel_path, "error": "File not found"})
            continue

        try:
            gist_url = create_gist(
                filepath,
                metadata["description"],
                metadata["slug"],
                dry_run=args.dry_run
            )

            if gist_url:
                created_gists[rel_path] = {
                    "url": gist_url,
                    "slug": metadata["slug"],
                    "description": metadata["description"]
                }

                # Rate limiting: 1 second delay between gist creations (skip in dry-run)
                if not args.dry_run and i < total_count:
                    time.sleep(1)
            else:
                failed_gists.append({"path": rel_path, "error": "Gist creation failed"})

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed_gists.append({"path": rel_path, "error": str(e)})

    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)

    # Save mapping
    if not args.dry_run:
        print(f"\n💾 Saving gist mapping to {MAPPING_FILE}...")
        try:
            with open(MAPPING_FILE, "w") as f:
                json.dump(created_gists, f, indent=2)
            print(f"   ✅ Mapping saved ({len(created_gists)} entries)")
        except Exception as e:
            print(f"   ❌ Error saving mapping: {e}")
            return 1
    else:
        print(f"\n💾 [DRY RUN] Would save mapping to {MAPPING_FILE}")

    # Summary
    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Created:  {len(created_gists)}/{total_count} gists")
    print(f"❌ Failed:   {len(failed_gists)}/{total_count} gists")
    print(f"⏱️  Time:     {minutes}m {seconds}s")
    if not args.dry_run:
        print(f"📝 Mapping:  {MAPPING_FILE}")

    if failed_gists:
        print("\n⚠️  Failed gists:")
        for failure in failed_gists:
            print(f"  - {failure['path']}")
            print(f"    Error: {failure['error']}")
        return 1

    if args.dry_run:
        print("\n✅ Dry run completed successfully!")
        print("   Remove --dry-run flag to create actual gists")
    else:
        print("\n✅ All gists created successfully!")
        print("\nNext steps:")
        print("1. Review gist-mapping.json")
        print("2. Update blog posts with real gist URLs")
        print("3. Validate all links work")
        print("4. Run npm run build")

    return 0


if __name__ == "__main__":
    sys.exit(main())
