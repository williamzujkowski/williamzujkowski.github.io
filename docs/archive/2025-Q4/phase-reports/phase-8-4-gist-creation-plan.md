# GitHub Gist Creation Plan - Phase 8.4.4

**Date:** 2025-10-31
**Objective:** Create 46 GitHub gists from extracted code blocks across 4 blog posts
**Status:** Planning Complete - Ready for Execution

---

## Executive Summary

46 GitHub gist placeholders exist in 4 optimized blog posts. This plan provides a systematic approach to create actual gists with full code implementations extracted from pre-optimization git history.

### Gist Distribution

| Post | Gists | Commit Reference | Lines of Code |
|------|-------|------------------|---------------|
| Security Scanning Pipeline | 13 | `b56c988` | ~854 lines |
| MITRE ATT&CK Dashboard | 8 | `eae5dd2` (or earlier) | ~443 lines |
| VLAN Segmentation | 15 | `eae5dd2` (or earlier) | ~660 lines |
| Proxmox HA | 10 | `eae5dd2` (or earlier) | ~714 lines |
| **Total** | **46** | - | **~2,671 lines** |

---

## Strategy Decision: Gist vs Repository

### Option A: Individual GitHub Gists (Current Plan)
**Pros:**
- Direct 1:1 mapping with existing placeholder URLs
- Each code snippet is self-contained
- Easy to embed in blog posts
- Simple to share individual files

**Cons:**
- 46 separate gists to create and manage
- No versioning across related files
- Difficult to update multiple gists at once
- No organizational structure

### Option B: Centralized Code Repository (RECOMMENDED)
**Pros:**
- Single source of truth for all blog code examples
- Git versioning for all changes
- Organized directory structure by topic
- Easier bulk updates
- Better discoverability
- Can add tests, documentation, CI/CD

**Cons:**
- Requires URL format change in blog posts
- Initial setup more complex

### Recommendation: HYBRID APPROACH

**Create `blog-code-examples` repository** with organized structure, then:
1. Create individual gists from repository files (automated)
2. Update blog posts with gist URLs
3. Maintain single repo as source of truth
4. Periodically sync gists from repo files

**Why hybrid works:**
- Best of both worlds: organization + individual sharing
- Gist URLs work for readers
- Repository provides maintenance structure
- Automation keeps gists in sync with repo

---

## Repository Structure (blog-code-examples)

```
blog-code-examples/
├── README.md                           # Index of all code examples
├── security-scanning/                  # Post 1: 13 files
│   ├── workflows/
│   │   ├── security-scan.yml          # Complete GitHub Actions workflow (109 lines)
│   │   ├── scheduled-scan.yml         # Daily scheduled scans (44 lines)
│   │   ├── sbom-scan.yml              # SBOM generation (38 lines)
│   │   └── auto-remediate.yml         # Auto-remediation workflow (47 lines)
│   ├── configs/
│   │   ├── .grype.yaml                # Grype configuration (21 lines)
│   │   ├── osv-scanner.toml           # OSV-Scanner config (22 lines)
│   │   └── security.rego              # Trivy OPA policy (20 lines)
│   ├── scripts/
│   │   ├── compare-scans.py           # Vulnerability comparison (59 lines)
│   │   └── send-scans-to-wazuh.sh     # Wazuh integration (19 lines)
│   ├── integrations/
│   │   ├── slack-notification.yml     # Slack webhook payload (27 lines)
│   │   ├── wazuh-rules.xml            # Wazuh detection rules (18 lines)
│   │   ├── tasks.json                 # VS Code tasks (37 lines)
│   │   └── vulnerability-metrics.sql  # PostgreSQL analytics (25 lines)
│   └── README.md                      # Security scanning guide
│
├── mitre-dashboard/                    # Post 2: 8 files
│   ├── collectors/
│   │   ├── mitre_collector.py         # MITRE ATT&CK data collector
│   │   ├── alienvault_otx.py          # AlienVault OTX integration
│   │   └── cisa_kev.py                # CISA KEV mapper
│   ├── processors/
│   │   ├── threat_profiler.py         # Threat actor profiling
│   │   └── technique_matcher.py       # Technique matching logic
│   ├── visualization/
│   │   ├── dashboard.py               # Main dashboard
│   │   └── heatmap_generator.py       # Technique heatmap
│   ├── alerting/
│   │   └── wazuh_alerting.py          # Alert generation
│   └── README.md                      # MITRE dashboard guide
│
├── vlan-segmentation/                  # Post 3: 15 files
│   ├── configs/
│   │   ├── udm-vlan-setup.sh          # UDM Pro VLAN configuration
│   │   ├── dhcp-config.json           # DHCP reservations
│   │   ├── firewall-rules.json        # Firewall rule examples
│   │   ├── mdns-reflector.conf        # mDNS configuration
│   │   ├── pvlan-isolation.sh         # Private VLAN setup
│   │   └── radius-vlan-mapping.conf   # Dynamic VLAN assignment
│   ├── scripts/
│   │   ├── pihole-blocklists.sh       # Pi-hole DNS filtering
│   │   ├── netflow-setup.sh           # NetFlow configuration
│   │   ├── traffic-analysis.py        # Traffic pattern analysis
│   │   ├── connectivity-test.sh       # VLAN connectivity tests
│   │   ├── pentest-vlan.sh            # Penetration testing
│   │   └── troubleshooting.sh         # Common troubleshooting
│   ├── monitoring/
│   │   ├── grafana-dashboard.json     # Network monitoring dashboard
│   │   └── performance-tuning.sh      # Performance optimization
│   └── README.md                      # VLAN segmentation guide
│
├── proxmox-ha/                         # Post 4: 10 files
│   ├── cluster/
│   │   ├── node-prep.sh               # Node preparation
│   │   ├── cluster-create.sh          # Cluster creation
│   │   └── corosync.conf              # Corosync configuration
│   ├── storage/
│   │   ├── ceph-install.sh            # Ceph installation
│   │   ├── ceph-osd-setup.sh          # OSD configuration
│   │   └── ceph-pool-create.sh        # Pool creation
│   ├── ha/
│   │   ├── ha-manager-setup.sh        # HA manager configuration
│   │   ├── fencing-config.sh          # Fencing setup
│   │   ├── vm-ha-config.sh            # VM HA settings
│   │   └── failover-test.sh           # Failover testing
│   ├── backup/
│   │   └── backup-config.sh           # Backup configuration
│   ├── monitoring/
│   │   ├── prometheus-config.yml      # Prometheus setup
│   │   ├── grafana-dashboard.json     # Monitoring dashboard
│   │   └── alerting-rules.yml         # Alert configuration
│   ├── maintenance/
│   │   ├── maintenance-mode.sh        # Maintenance procedures
│   │   ├── rolling-updates.sh         # Update process
│   │   └── disaster-recovery.sh       # DR procedures
│   └── README.md                      # Proxmox HA guide
│
├── .github/
│   └── workflows/
│       └── sync-gists.yml             # Automated gist syncing
├── scripts/
│   ├── create-gists.py                # Batch gist creation
│   ├── update-gists.py                # Gist update automation
│   └── validate-gists.py              # Gist validation
└── LICENSE                            # MIT License
```

**Total Files:** 46 code files + 4 READMEs + 3 automation scripts = 53 files

---

## Gist Inventory (Complete Catalog)

### Post 1: Automated Security Scanning Pipeline (13 gists)

#### 1.1 security-scan-workflow-complete
**File:** `security-scanning/workflows/security-scan.yml`
**Lines:** 109
**Description:** Complete GitHub Actions workflow with OSV-Scanner, Grype, Trivy, SARIF uploads, quality gates, Slack notifications
**URL:** https://gist.github.com/williamzujkowski/security-scan-workflow-complete

#### 1.2 security-scan-slack-notification
**File:** `security-scanning/integrations/slack-notification.yml`
**Lines:** 27
**Description:** Slack webhook payload with formatted blocks, repository details, failed run links
**URL:** https://gist.github.com/williamzujkowski/security-scan-slack-notification

#### 1.3 vscode-security-scan-tasks
**File:** `security-scanning/integrations/tasks.json`
**Lines:** 37
**Description:** VS Code tasks.json with Grype, OSV, combined scan tasks, JSON output formatting
**URL:** https://gist.github.com/williamzujkowski/vscode-security-scan-tasks

#### 1.4 grype-config
**File:** `security-scanning/configs/.grype.yaml`
**Lines:** 21
**Description:** Grype configuration with ignore rules, severity thresholds, scan scope, output formatting
**URL:** https://gist.github.com/williamzujkowski/grype-config

#### 1.5 osv-scanner-config
**File:** `security-scanning/configs/osv-scanner.toml`
**Lines:** 22
**Description:** OSV-Scanner configuration with ignore rules, dev dependencies, private registries, parallel scanning
**URL:** https://gist.github.com/williamzujkowski/osv-scanner-config

#### 1.6 trivy-opa-policy
**File:** `security-scanning/configs/security.rego`
**Lines:** 20
**Description:** Trivy OPA policy with critical deny rules, package version blocks, high severity warnings
**URL:** https://gist.github.com/williamzujkowski/trivy-opa-policy

#### 1.7 scheduled-security-scans
**File:** `security-scanning/workflows/scheduled-scan.yml`
**Lines:** 44
**Description:** Daily cron schedule, matrix strategy, Grype+Trivy scanning, baseline comparison, SIEM integration
**URL:** https://gist.github.com/williamzujkowski/scheduled-security-scans

#### 1.8 vulnerability-scan-comparison
**File:** `security-scanning/scripts/compare-scans.py`
**Lines:** 59
**Description:** Python script for JSON parsing, vulnerability extraction, set-based comparison, new/fixed alerts
**URL:** https://gist.github.com/williamzujkowski/vulnerability-scan-comparison

#### 1.9 sbom-generation-workflow
**File:** `security-scanning/workflows/sbom-scan.yml`
**Lines:** 38
**Description:** SBOM workflow with CycloneDX generation, Grype scanning, GitHub release upload, S3 storage
**URL:** https://gist.github.com/williamzujkowski/sbom-generation-workflow

#### 1.10 auto-remediate-vulnerabilities
**File:** `security-scanning/workflows/auto-remediate.yml`
**Lines:** 47
**Description:** Weekly scheduled auto-remediation with OSV scanning, npm audit fix, re-scan verification, PR creation
**URL:** https://gist.github.com/williamzujkowski/auto-remediate-vulnerabilities

#### 1.11 wazuh-vulnerability-ingestion
**File:** `security-scanning/scripts/send-scans-to-wazuh.sh`
**Lines:** 19
**Description:** Bash script for Grype scanning, jq transformation, syslog formatting, netcat delivery to Wazuh
**URL:** https://gist.github.com/williamzujkowski/wazuh-vulnerability-ingestion

#### 1.12 wazuh-vulnerability-rules
**File:** `security-scanning/integrations/wazuh-rules.xml`
**Lines:** 18
**Description:** Wazuh detection rules with base vulnerability rule, critical/high severity levels, custom alerts
**URL:** https://gist.github.com/williamzujkowski/wazuh-vulnerability-rules

#### 1.13 vulnerability-metrics-sql
**File:** `security-scanning/integrations/vulnerability-metrics.sql`
**Lines:** 25
**Description:** PostgreSQL analytics for vulnerability counts, mean time to remediate, weekly trends, historical comparison
**URL:** https://gist.github.com/williamzujkowski/vulnerability-metrics-sql

---

### Post 2: MITRE ATT&CK Dashboard (8 gists)

#### 2.1 mitre-data-collector
**File:** `mitre-dashboard/collectors/mitre_collector.py`
**Lines:** ~50
**Description:** MITRE ATT&CK framework data collector with API integration, technique extraction, caching
**URL:** https://gist.github.com/williamzujkowski/mitre-data-collector

#### 2.2 alienvault-otx-integration
**File:** `mitre-dashboard/collectors/alienvault_otx.py`
**Lines:** ~40
**Description:** AlienVault OTX pulse integration with threat intelligence fetching, IoC extraction
**URL:** https://gist.github.com/williamzujkowski/alienvault-otx-integration

#### 2.3 cisa-kev-mapper
**File:** `mitre-dashboard/collectors/cisa_kev.py`
**Lines:** ~35
**Description:** CISA Known Exploited Vulnerabilities mapper linking CVEs to MITRE techniques
**URL:** https://gist.github.com/williamzujkowski/cisa-kev-mapper

#### 2.4 threat-actor-profiler
**File:** `mitre-dashboard/processors/threat_profiler.py`
**Lines:** ~45
**Description:** Threat actor profiling with technique frequency analysis, campaign detection
**URL:** https://gist.github.com/williamzujkowski/threat-actor-profiler

#### 2.5 technique-matcher
**File:** `mitre-dashboard/processors/technique_matcher.py`
**Lines:** ~30
**Description:** Technique matching logic correlating observed TTPs with MITRE framework
**URL:** https://gist.github.com/williamzujkowski/technique-matcher

#### 2.6 mitre-dashboard-visualization
**File:** `mitre-dashboard/visualization/dashboard.py`
**Lines:** ~60
**Description:** Main dashboard with Flask backend, technique heatmap, threat actor timeline
**URL:** https://gist.github.com/williamzujkowski/mitre-dashboard-visualization

#### 2.7 technique-heatmap-generator
**File:** `mitre-dashboard/visualization/heatmap_generator.py`
**Lines:** ~40
**Description:** Heatmap generation using Plotly, technique frequency visualization
**URL:** https://gist.github.com/williamzujkowski/technique-heatmap-generator

#### 2.8 wazuh-mitre-alerting
**File:** `mitre-dashboard/alerting/wazuh_alerting.py`
**Lines:** ~35
**Description:** Wazuh integration for MITRE technique-based alerting, severity mapping
**URL:** https://gist.github.com/williamzujkowski/wazuh-mitre-alerting

---

### Post 3: Zero Trust VLAN Segmentation (15 gists)

#### 3.1 udm-vlan-setup
**File:** `vlan-segmentation/configs/udm-vlan-setup.sh`
**Lines:** ~40
**Description:** UDM Pro VLAN creation, tagging, trunk port configuration via CLI
**URL:** https://gist.github.com/williamzujkowski/udm-vlan-setup

#### 3.2 dhcp-config
**File:** `vlan-segmentation/configs/dhcp-config.json`
**Lines:** ~35
**Description:** DHCP server configuration with reservations, custom options, lease times
**URL:** https://gist.github.com/williamzujkowski/dhcp-config

#### 3.3 firewall-rules
**File:** `vlan-segmentation/configs/firewall-rules.json`
**Lines:** ~50
**Description:** UDM Pro firewall rules for inter-VLAN traffic, explicit deny-all, service exceptions
**URL:** https://gist.github.com/williamzujkowski/firewall-rules

#### 3.4 mdns-reflector
**File:** `vlan-segmentation/configs/mdns-reflector.conf`
**Lines:** ~25
**Description:** Avahi mDNS reflector configuration for cross-VLAN service discovery
**URL:** https://gist.github.com/williamzujkowski/mdns-reflector

#### 3.5 pvlan-isolation
**File:** `vlan-segmentation/configs/pvlan-isolation.sh`
**Lines:** ~30
**Description:** Private VLAN setup for IoT isolation, promiscuous/isolated port configuration
**URL:** https://gist.github.com/williamzujkowski/pvlan-isolation

#### 3.6 radius-vlan-mapping
**File:** `vlan-segmentation/configs/radius-vlan-mapping.conf`
**Lines:** ~35
**Description:** FreeRADIUS dynamic VLAN assignment based on 802.1X authentication
**URL:** https://gist.github.com/williamzujkowski/radius-vlan-mapping

#### 3.7 pihole-blocklists
**File:** `vlan-segmentation/scripts/pihole-blocklists.sh`
**Lines:** ~25
**Description:** Pi-hole DNS filtering with VLAN-specific blocklists, whitelist management
**URL:** https://gist.github.com/williamzujkowski/pihole-blocklists

#### 3.8 netflow-setup
**File:** `vlan-segmentation/scripts/netflow-setup.sh`
**Lines:** ~30
**Description:** NetFlow v9 configuration for VLAN traffic monitoring, collector setup
**URL:** https://gist.github.com/williamzujkowski/netflow-setup

#### 3.9 traffic-analysis
**File:** `vlan-segmentation/scripts/traffic-analysis.py`
**Lines:** ~55
**Description:** Python script for analyzing NetFlow data, detecting anomalies, policy violations
**URL:** https://gist.github.com/williamzujkowski/traffic-analysis

#### 3.10 connectivity-test
**File:** `vlan-segmentation/scripts/connectivity-test.sh`
**Lines:** ~40
**Description:** Bash script for testing inter-VLAN connectivity, ping sweep, port scanning
**URL:** https://gist.github.com/williamzujkowski/connectivity-test

#### 3.11 pentest-vlan
**File:** `vlan-segmentation/scripts/pentest-vlan.sh`
**Lines:** ~45
**Description:** Penetration testing script for VLAN hopping attacks, double tagging tests
**URL:** https://gist.github.com/williamzujkowski/pentest-vlan

#### 3.12 troubleshooting
**File:** `vlan-segmentation/scripts/troubleshooting.sh`
**Lines:** ~35
**Description:** Common troubleshooting commands for VLAN issues, packet capture, routing tables
**URL:** https://gist.github.com/williamzujkowski/troubleshooting

#### 3.13 grafana-dashboard-vlan
**File:** `vlan-segmentation/monitoring/grafana-dashboard.json`
**Lines:** ~80
**Description:** Grafana dashboard for VLAN monitoring, traffic graphs, firewall hit counts
**URL:** https://gist.github.com/williamzujkowski/grafana-dashboard-vlan

#### 3.14 performance-tuning
**File:** `vlan-segmentation/monitoring/performance-tuning.sh`
**Lines:** ~30
**Description:** Network performance tuning, MTU optimization, interrupt coalescence
**URL:** https://gist.github.com/williamzujkowski/performance-tuning

#### 3.15 vlan-network-diagram (Mermaid)
**File:** `vlan-segmentation/diagrams/network-topology.md`
**Lines:** ~40
**Description:** Mermaid diagram showing complete VLAN topology with VLANs, subnets, firewall rules
**URL:** https://gist.github.com/williamzujkowski/vlan-network-diagram

---

### Post 4: Proxmox High Availability (10 gists)

#### 4.1 proxmox-node-prep
**File:** `proxmox-ha/cluster/node-prep.sh`
**Lines:** ~35
**Description:** Node preparation script with hostname, networking, SSH keys, time sync
**URL:** https://gist.github.com/williamzujkowski/proxmox-node-prep

#### 4.2 proxmox-cluster-create
**File:** `proxmox-ha/cluster/cluster-create.sh`
**Lines:** ~25
**Description:** Cluster creation with pvecm, node joining, quorum configuration
**URL:** https://gist.github.com/williamzujkowski/proxmox-cluster-create

#### 4.3 corosync-config
**File:** `proxmox-ha/cluster/corosync.conf`
**Lines:** ~40
**Description:** Corosync configuration with ring redundancy, multicast/unicast setup
**URL:** https://gist.github.com/williamzujkowski/corosync-config

#### 4.4 ceph-install
**File:** `proxmox-ha/storage/ceph-install.sh`
**Lines:** ~30
**Description:** Ceph installation script, monitor deployment, manager setup
**URL:** https://gist.github.com/williamzujkowski/ceph-install

#### 4.5 ceph-osd-pool-setup
**File:** `proxmox-ha/storage/ceph-osd-setup.sh`
**Lines:** ~40
**Description:** OSD creation, pool configuration, replication settings, PG calculation
**URL:** https://gist.github.com/williamzujkowski/ceph-osd-pool-setup

#### 4.6 ha-manager-config
**File:** `proxmox-ha/ha/ha-manager-setup.sh`
**Lines:** ~35
**Description:** HA manager configuration, resource groups, fencing policies
**URL:** https://gist.github.com/williamzujkowski/ha-manager-config

#### 4.7 vm-ha-config
**File:** `proxmox-ha/ha/vm-ha-config.sh`
**Lines:** ~30
**Description:** VM HA configuration, priority settings, migration policies, failover tests
**URL:** https://gist.github.com/williamzujkowski/vm-ha-config

#### 4.8 proxmox-backup-config
**File:** `proxmox-ha/backup/backup-config.sh`
**Lines:** ~45
**Description:** Proxmox Backup Server integration, retention policies, encryption setup
**URL:** https://gist.github.com/williamzujkowski/proxmox-backup-config

#### 4.9 prometheus-grafana-monitoring
**File:** `proxmox-ha/monitoring/prometheus-config.yml`
**Lines:** ~50
**Description:** Prometheus configuration for Proxmox metrics, alerting rules, Grafana dashboard JSON
**URL:** https://gist.github.com/williamzujkowski/prometheus-grafana-monitoring

#### 4.10 disaster-recovery
**File:** `proxmox-ha/maintenance/disaster-recovery.sh`
**Lines:** ~55
**Description:** DR procedures, cluster rebuild, backup restoration, node recovery
**URL:** https://gist.github.com/williamzujkowski/disaster-recovery

---

## Batch Processing Strategy

### Phase 1: Repository Setup (1 hour)
- Create `blog-code-examples` repository
- Setup directory structure
- Add README with navigation
- Add LICENSE (MIT)

### Phase 2: Code Extraction (3-4 hours)
**Automated extraction script:**

```python
#!/usr/bin/env python3
"""Extract code blocks from git history for gist creation."""

import subprocess
import re
import json
from pathlib import Path

POSTS = {
    "security-scanning": {
        "commit": "b56c988",
        "file": "src/posts/2025-10-06-automated-security-scanning-pipeline.md",
        "output_dir": "security-scanning"
    },
    "mitre-dashboard": {
        "commit": "eae5dd2~1",  # Before optimization
        "file": "src/posts/2025-09-14-threat-intelligence-mitre-attack-dashboard.md",
        "output_dir": "mitre-dashboard"
    },
    "vlan-segmentation": {
        "commit": "eae5dd2~1",
        "file": "src/posts/2025-09-08-zero-trust-vlan-segmentation-homelab.md",
        "output_dir": "vlan-segmentation"
    },
    "proxmox-ha": {
        "commit": "eae5dd2~1",
        "file": "src/posts/2025-09-29-proxmox-high-availability-homelab.md",
        "output_dir": "proxmox-ha"
    }
}

def extract_code_blocks(commit, filepath):
    """Extract file content from specific commit."""
    cmd = f"git show {commit}:{filepath}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def parse_code_blocks(content):
    """Parse Markdown code blocks with language hints."""
    blocks = []
    pattern = r'```(\w+)\n(.*?)\n```'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        language = match.group(1)
        code = match.group(2)
        blocks.append({
            "language": language,
            "code": code,
            "lines": len(code.split('\n'))
        })

    return blocks

def main():
    for post_name, config in POSTS.items():
        print(f"\n📦 Extracting code from {post_name}...")

        content = extract_code_blocks(config["commit"], config["file"])
        blocks = parse_code_blocks(content)

        print(f"   Found {len(blocks)} code blocks")
        print(f"   Total lines: {sum(b['lines'] for b in blocks)}")

        # Save to JSON for manual mapping
        output = Path(f"extracted/{post_name}.json")
        output.parent.mkdir(exist_ok=True)

        with open(output, 'w') as f:
            json.dump(blocks, f, indent=2)

        print(f"   ✅ Saved to {output}")

if __name__ == "__main__":
    main()
```

**Execution:**
```bash
# Extract all code blocks from git history
python scripts/extract-blog-code.py

# Review extracted code
for post in extracted/*.json; do
  echo "=== $(basename $post) ==="
  jq '.[] | "\(.language): \(.lines) lines"' $post
done
```

### Phase 3: Manual Code Organization (4-5 hours)
- Map extracted code blocks to gist names
- Add headers, documentation, usage examples
- Create README for each category
- Add error handling where missing
- Ensure code is production-ready

### Phase 4: Gist Creation (2-3 hours)

**Automated gist creation script:**

```python
#!/usr/bin/env python3
"""Batch create GitHub gists from repository files."""

import subprocess
import json
from pathlib import Path

GIST_MAPPING = {
    # Post 1: Security Scanning
    "security-scanning/workflows/security-scan.yml": {
        "description": "Complete GitHub Actions security scanning workflow with Grype, OSV-Scanner, Trivy",
        "public": True
    },
    "security-scanning/configs/.grype.yaml": {
        "description": "Grype vulnerability scanner configuration with ignore rules and severity thresholds",
        "public": True
    },
    # ... (46 total entries)
}

def create_gist(filepath, description, public=True):
    """Create GitHub gist using gh CLI."""
    visibility = "public" if public else "secret"

    cmd = [
        "gh", "gist", "create",
        str(filepath),
        "--desc", description,
        f"--{visibility}"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        gist_url = result.stdout.strip()
        return gist_url
    else:
        raise Exception(f"Failed to create gist: {result.stderr}")

def main():
    created_gists = {}

    for filepath, config in GIST_MAPPING.items():
        print(f"\n📎 Creating gist for {filepath}...")

        try:
            gist_url = create_gist(
                Path(filepath),
                config["description"],
                config["public"]
            )

            created_gists[filepath] = gist_url
            print(f"   ✅ {gist_url}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # Save mapping for blog post updates
    with open("gist-urls.json", "w") as f:
        json.dump(created_gists, f, indent=2)

    print(f"\n✅ Created {len(created_gists)} gists")
    print(f"   Mapping saved to gist-urls.json")

if __name__ == "__main__":
    main()
```

**Execution:**
```bash
# Create all gists
python scripts/create-gists.py

# Verify gist creation
jq -r '.[] | .' gist-urls.json | while read url; do
  echo "Testing: $url"
  curl -s -o /dev/null -w "%{http_code}\n" "$url"
done
```

### Phase 5: Blog Post Updates (1-2 hours)
- Replace placeholder URLs with actual gist URLs
- Verify all links work
- Test rendering in browser
- Validate build passes

### Phase 6: Validation & Testing (1 hour)
- Click every gist link (46 total)
- Verify code renders correctly
- Check syntax highlighting
- Test on mobile devices
- Run build validation

---

## Gist Template Structure

Each gist should follow this format:

```markdown
# [Descriptive Title]

**Source:** [Blog Post Title](https://williamzujkowski.com/blog/post-slug)
**Category:** [Security Scanning | MITRE Dashboard | VLAN Segmentation | Proxmox HA]
**Language:** [Python | Bash | YAML | JSON | etc.]

## Purpose

[1-2 sentences explaining what this code does and why it's useful]

## Usage

```[language]
# Example usage
command --flag value
```

## Prerequisites

- Requirement 1
- Requirement 2
- Requirement 3

## Implementation

```[language]
[Full code implementation here]
```

## Configuration

[Any required environment variables, config files, or setup steps]

## Notes

- **Security:** [Any security considerations]
- **Performance:** [Performance notes if relevant]
- **Compatibility:** [Tested on X, should work on Y]

## Related Gists

- [Related Gist 1](url)
- [Related Gist 2](url)

## License

MIT License - Free to use, modify, and distribute
```

---

## Automation: Gist Sync Workflow

Create GitHub Actions workflow to keep gists in sync with repository:

```yaml
# .github/workflows/sync-gists.yml
name: Sync Gists

on:
  push:
    branches: [main]
    paths:
      - 'security-scanning/**'
      - 'mitre-dashboard/**'
      - 'vlan-segmentation/**'
      - 'proxmox-ha/**'

jobs:
  sync-gists:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install PyGithub requests

      - name: Sync changed files to gists
        env:
          GITHUB_TOKEN: ${{ secrets.GIST_TOKEN }}
        run: python scripts/update-gists.py

      - name: Verify gist updates
        run: python scripts/validate-gists.py
```

**Update script (`scripts/update-gists.py`):**

```python
#!/usr/bin/env python3
"""Update existing gists when repository files change."""

import os
import json
from pathlib import Path
from github import Github

def load_gist_mapping():
    """Load filepath -> gist_id mapping."""
    with open("gist-mapping.json") as f:
        return json.load(f)

def update_gist(gh, gist_id, filepath):
    """Update gist content from repository file."""
    gist = gh.get_gist(gist_id)

    content = Path(filepath).read_text()
    filename = Path(filepath).name

    gist.edit(files={filename: {"content": content}})
    print(f"✅ Updated {filename} in gist {gist_id}")

def main():
    token = os.environ["GITHUB_TOKEN"]
    gh = Github(token)

    mapping = load_gist_mapping()

    # Get changed files from git
    import subprocess
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
        capture_output=True,
        text=True
    )

    changed_files = result.stdout.strip().split('\n')

    for filepath in changed_files:
        if filepath in mapping:
            gist_id = mapping[filepath]
            update_gist(gh, gist_id, filepath)
        else:
            print(f"⚠️  No gist mapping for {filepath}")

if __name__ == "__main__":
    main()
```

---

## Timeline Estimate

| Phase | Task | Time | Cumulative |
|-------|------|------|------------|
| 1 | Repository setup | 1h | 1h |
| 2 | Code extraction (automated) | 1h | 2h |
| 3 | Manual code organization | 5h | 7h |
| 4 | Gist creation (automated) | 2h | 9h |
| 5 | Blog post URL updates | 2h | 11h |
| 6 | Validation & testing | 1h | 12h |
| 7 | Documentation & README | 1h | 13h |
| **Total** | **Complete workflow** | **13h** | - |

**Breakdown by complexity:**
- **Automation:** 4 hours (scripts, workflows)
- **Manual work:** 7 hours (organization, validation)
- **Documentation:** 2 hours (READMEs, gist templates)

**Parallelization opportunity:** Phases 2-3 can be done per-post in parallel (4 parallel streams)
- **With 4 workers:** 13 hours → ~8 hours wall clock time

---

## Quality Assurance Checklist

### Pre-Creation Validation
- [ ] All code extracted from correct git commits
- [ ] Code blocks mapped to correct gist names
- [ ] File organization matches repository structure
- [ ] README files created for each category
- [ ] License file added to repository

### Gist Creation Validation
- [ ] All 46 gists created successfully
- [ ] Each gist has descriptive title
- [ ] Each gist includes usage instructions
- [ ] Syntax highlighting works correctly
- [ ] Code is properly formatted

### Blog Post Integration
- [ ] All placeholder URLs replaced with actual gist URLs
- [ ] Gist links open correctly in new tabs
- [ ] Markdown rendering doesn't break
- [ ] Code snippets display properly
- [ ] Mobile rendering tested

### Functional Testing
- [ ] Click every gist link (46 total)
- [ ] Verify code can be copied
- [ ] Test "Raw" download links
- [ ] Check embed functionality
- [ ] Validate revision history works

### Build Validation
- [ ] `npm run build` passes
- [ ] No broken links detected
- [ ] JavaScript minification works
- [ ] CSS processing succeeds
- [ ] Site deploys successfully

### Documentation Validation
- [ ] Repository README is comprehensive
- [ ] Each category has README
- [ ] Gist descriptions are clear
- [ ] Usage examples are accurate
- [ ] License is specified

---

## Recommendations

### Immediate Actions
1. **Create `blog-code-examples` repository** - Single source of truth
2. **Extract code from git history** - Use automated script
3. **Organize into directory structure** - Follow proposed hierarchy
4. **Create gists in batches** - 10-15 at a time to avoid rate limits
5. **Update blog posts** - Replace placeholder URLs
6. **Setup sync workflow** - Automate future updates

### Best Practices
1. **Version control:** Repository tracks all changes
2. **Atomic commits:** One gist per commit for traceability
3. **Testing:** Test every gist before updating blog posts
4. **Documentation:** Comprehensive READMEs for discoverability
5. **Automation:** CI/CD keeps gists in sync

### Future Enhancements
1. **Add tests:** Unit tests for Python scripts, integration tests for workflows
2. **CI/CD validation:** Automated testing of code examples
3. **Version badges:** Show tested versions in gist descriptions
4. **Usage tracking:** Analytics on which gists are most popular
5. **Contribution guide:** Allow community improvements

---

## Success Criteria

**Phase 8.4.4 Complete When:**
- ✅ All 46 gists created with actual code
- ✅ Blog posts updated with real gist URLs
- ✅ Repository structure established
- ✅ Automation scripts working
- ✅ Build validation passes
- ✅ All links verified functional
- ✅ Documentation comprehensive
- ✅ Sync workflow deployed

**Measurement:**
- 0 broken gist links
- 100% code coverage (all extracted blocks mapped to gists)
- <2 seconds average gist load time
- Repository has complete README
- Automation reduces future maintenance to <1 hour per update

---

## Risk Mitigation

### Risk: GitHub API Rate Limits
**Mitigation:**
- Use personal access token with higher limits
- Batch create gists with delays (1-2 seconds between creates)
- Use `gh` CLI instead of raw API (higher limits)

### Risk: Code Extraction Errors
**Mitigation:**
- Manual review of extracted code blocks
- Compare line counts with original optimization report
- Test code in isolated environment before gist creation

### Risk: Broken Blog Post Links
**Mitigation:**
- Create all gists before updating blog posts
- Keep mapping file (filepath → gist URL)
- Automated link validation script
- Rollback plan if gist creation fails

### Risk: Gist Content Errors
**Mitigation:**
- Test code before creating gist
- Include usage examples in gist
- Add error handling where missing
- Review gist after creation

### Risk: Maintenance Burden
**Mitigation:**
- Automate gist syncing with GitHub Actions
- Single repository as source of truth
- Clear documentation for future updates
- Version control for all changes

---

## Next Steps

1. **Immediate (Today):**
   - Create `blog-code-examples` repository
   - Setup directory structure
   - Run code extraction script

2. **Short-term (This Week):**
   - Organize extracted code into repository
   - Create first batch of gists (security-scanning: 13 gists)
   - Update security scanning blog post
   - Validate and test

3. **Medium-term (Next Week):**
   - Create remaining 33 gists (posts 2-4)
   - Update all blog posts
   - Deploy sync automation
   - Comprehensive validation

4. **Long-term (This Month):**
   - Add tests to code examples
   - Create contribution guide
   - Monitor gist usage analytics
   - Gather community feedback

---

## Conclusion

This plan provides a systematic approach to creating 46 GitHub gists from extracted blog code. The hybrid repository + gist strategy offers the best of both worlds: organized maintenance via repository, easy sharing via individual gists.

**Key Success Factors:**
1. **Automation:** Scripts reduce manual work by 60%
2. **Organization:** Repository structure ensures maintainability
3. **Quality:** Comprehensive testing and validation
4. **Sustainability:** Sync workflow prevents drift
5. **Documentation:** Clear guides for users and contributors

**Expected Outcomes:**
- 46 high-quality, tested code examples
- Zero broken links in blog posts
- Automated sync for future updates
- Better reader experience (copy-paste ready code)
- Portfolio of reusable homelab configurations

**Total Effort:** 13 hours (or ~8 hours with parallelization)
**Total Value:** Permanent improvement to blog quality, reader satisfaction, code sharing

---

**Ready for execution.** Recommend starting with Phase 1 (repository setup) and Phase 2 (code extraction) today.
