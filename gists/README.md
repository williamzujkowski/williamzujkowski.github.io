# Blog Code Examples - GitHub Gists

This directory contains all code examples referenced in blog posts as GitHub gists. Each file here corresponds to a gist link in the blog.

## Purpose

Blog posts maintain <25% code-to-content ratio by linking to full implementations rather than embedding verbose code blocks. This directory serves as:

1. **Source of truth** for all blog code examples
2. **Local reference** for readers who prefer browsing locally
3. **Gist sync source** for maintaining GitHub gists

## Organization

Code files are organized by blog post:

```
gists/
├── security-scanning/     # Automated Security Scanning Pipeline (13 files)
├── mitre-dashboard/       # MITRE ATT&CK Dashboard (8 files)
├── vlan-segmentation/     # Zero Trust VLAN Segmentation (15 files)
└── proxmox-ha/            # Proxmox High Availability (10 files)
```

Each category includes:
- **Code files** - Full implementations extracted from blog posts
- **README.md** - Category overview, quick start, troubleshooting

## Using These Files

### Option 1: Browse Locally

Clone the repository and explore the `gists/` directory:

```bash
git clone https://github.com/williamzujkowski/williamzujkowski.github.io.git
cd williamzujkowski.github.io/gists
ls -R
```

### Option 2: Use GitHub Gists

Each file has a corresponding GitHub gist linked from blog posts. Gists provide:
- Syntax highlighting
- Direct download links
- Embed capability
- Comment threads

### Option 3: Copy-Paste from Blog

Blog posts include essential snippets (5-10 lines) demonstrating core patterns. Full implementations link to gists.

## File Standards

All code files include:

**Header Format:**
```python
"""
Title: [Descriptive name]
Source: https://williamzujkowski.github.io/posts/[slug]/
Purpose: [What this does]
Usage: [How to run]
"""
```

**Quality Standards:**
- ✅ Tested and working code (extracted from actual homelab)
- ✅ Descriptive variable names
- ✅ Inline comments for complex logic
- ✅ Error handling included
- ✅ Prerequisites documented

## Quick Start by Category

### Security Scanning Pipeline

Automated vulnerability scanning with Grype, OSV-Scanner, and Trivy.

**Quick start:**
```bash
cd gists/security-scanning
cat README.md
```

**Most useful files:**
- `workflows/security-scan-workflow.yml` - GitHub Actions pipeline
- `configs/grype-config.yaml` - Grype configuration
- `scripts/scan-comparison.py` - Scan result comparison

### MITRE ATT&CK Dashboard

Threat intelligence aggregation and ATT&CK mapping dashboard.

**Quick start:**
```bash
cd gists/mitre-dashboard
cat README.md
```

**Most useful files:**
- `dashboard-core.py` - Main dashboard class
- `attack-data-loader.py` - MITRE ATT&CK data loading
- `threat-visualizer.py` - Plotly visualization

### VLAN Segmentation

Zero trust network segmentation using VLANs on Unifi Dream Machine Pro.

**Quick start:**
```bash
cd gists/vlan-segmentation
cat README.md
```

**Most useful files:**
- `udm-pro-vlan-config.sh` - VLAN creation script
- `iot-vlan-rules.json` - IoT isolation firewall rules
- `vlan-connectivity-tests.sh` - Validation test suite

### Proxmox High Availability

3-node Proxmox cluster with Ceph storage and HA failover.

**Quick start:**
```bash
cd gists/proxmox-ha
cat README.md
```

**Most useful files:**
- `cluster-create.sh` - Cluster initialization
- `ceph-osd-setup.sh` - Ceph storage configuration
- `vm-ha-config.sh` - VM high availability setup

## Maintenance

### Creating GitHub Gists

Use the automation script to create/update GitHub gists from local files:

```bash
python scripts/create-gists-from-folder.py
```

This generates:
- Individual GitHub gists for each file
- `gist-mapping.json` with URLs
- Updated blog post markdown with real gist links

### Updating Gists

1. Edit files in `/gists` directory
2. Test changes locally
3. Run sync script to update GitHub gists
4. Commit changes to repository

### Syncing Blog Posts

After creating/updating gists:

```bash
python scripts/update-blog-posts-with-gists.py
```

This replaces placeholder URLs with real gist URLs in blog posts.

## File Inventory

**Total:** 46 code files + 4 category READMEs = 50 files

| Category | Files | Lines | Purpose |
|----------|-------|-------|---------|
| Security Scanning | 13 | ~542 | Vulnerability scanning automation |
| MITRE Dashboard | 8 | ~443 | Threat intelligence aggregation |
| VLAN Segmentation | 15 | ~660 | Network segmentation |
| Proxmox HA | 10 | ~714 | High availability clustering |

## Contributing

Found an issue or have an improvement?

1. **File issues:** [GitHub Issues](https://github.com/williamzujkowski/williamzujkowski.github.io/issues)
2. **Suggest fixes:** Create PR with improvements
3. **Report bugs:** Include steps to reproduce

## License

MIT License - See individual files for details.

All code examples are from real homelab implementations documented in blog posts at [williamzujkowski.github.io](https://williamzujkowski.github.io).

## Related Documentation

- **Blog Posts:** [williamzujkowski.github.io/posts](https://williamzujkowski.github.io/posts/)
- **Architecture:** [ARCHITECTURE.md](../docs/ARCHITECTURE.md)
- **Standards:** [Standards Submodule](.standards/)
- **Uses Page:** [Hardware/Software Stack](https://williamzujkowski.github.io/uses/)

---

**Last Updated:** 2025-11-01
**Total Files:** 50 (46 code files + 4 READMEs)
**Source:** Extracted from blog posts via git history (commits b56c988, eae5dd2)
