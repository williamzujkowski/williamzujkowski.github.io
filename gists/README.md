# Blog Code Examples - GitHub Gists

This directory mirrors the code examples that blog posts link to as GitHub gists.

**These are illustrative excerpts, not turnkey scripts.** They are written to be *read* alongside a post — to show the shape of an approach and the parts that matter. Expect placeholders (`<password>`, `10.0.10.11`), elided error handling, and steps that assume a homelab you do not have. Do not paste them into a terminal and expect them to run.

What they *are* held to: every factual claim about a real tool must be correct. A config key that the tool ignores, a CLI flag that does not exist, or a comparison that inverts the security outcome is a defect even in an excerpt, because the reader learns it either way.

## Purpose

Blog posts maintain <25% code-to-content ratio by linking to full implementations rather than embedding verbose code blocks. This directory serves as:

1. **Local reference** for the published gists (the gists themselves are canonical —
   if the two disagree, the gist wins)
2. **Browsable copy** for readers who prefer reading in one place
3. **Review surface** for auditing the examples as a set

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

**Header Format** — use the comment syntax of the file's own language.
Prescribing one universal header is how fourteen shell scripts ended up
opening with a Python docstring, which bash reads as a command name.

Python:
```python
"""
Title: [Descriptive name]
Source: https://williamzujkowski.github.io/posts/[slug]/
Purpose: [What this demonstrates]
Requires: [What the reader must supply or verify]
"""
```

Shell, YAML, TOML, conf:
```bash
#!/bin/bash
# Title: [Descriptive name]
# Source: https://williamzujkowski.github.io/posts/[slug]/
# Purpose: [What this demonstrates]
# Requires: [What the reader must supply or verify]
```

Where a reader's intuition about the tool would be wrong, say so in the header.
The corrected `grype-config.yaml` is the model:

```yaml
# IMPORTANT: grype ignore rules DO NOT EXPIRE.
# There is NO `expiration` field. A date written here is silently ignored and
# the suppression is permanent.
```

**What these are held to:**
- Every config key, CLI flag and API parameter exists in the real tool
- Comparisons, filters and thresholds do what the surrounding prose says
- Placeholders look like placeholders (`<password>`, not `secure-password`)
- Destructive steps say so before the command
- Prerequisites and assumptions are stated in the header

**What they are not:**
- Tested end to end, or extracted verbatim from a running system
- Complete — error handling and edge cases are elided on purpose
- Safe to run unmodified

Every shell file now uses `#` headers, and every `.sh` here passes `bash -n`.
That is a low bar and it is the point: an excerpt that does not parse is not
demonstrating anything.

## Quick Start by Category

### Security Scanning Pipeline

Automated vulnerability scanning with Grype, OSV-Scanner, and Trivy.

**Quick start:**
```bash
cd gists/security-scanning
cat README.md
```

**Most useful files:**
- `workflows/security-scan-workflow-complete.yml` - GitHub Actions pipeline
- `configs/grype-config.yaml` - Grype configuration
- `scripts/vulnerability-scan-comparison.py` - Scan result comparison

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

There is no sync automation. Two scripts used to do this
(`create-gists-from-folder.py`, `update-blog-posts-with-gists.py`); both were
deleted, and nothing replaced them — which is why five local files have since
drifted from their published gists without anything noticing.

### Updating an example

The published gist is canonical, so change it there first:

```bash
# read what is published
gh api gists/<id> --jq '.files["<filename>"].content'

# after editing the gist in the browser or via `gh gist edit <id>`,
# pull the published bytes back into this mirror
gh api gists/<id> --jq '.files["<filename>"].content' > gists/<path>
```

Then commit the mirror update. Editing only the local copy leaves the
published gist — the thing readers actually see — untouched.

### Checking for drift

```bash
uv run python scripts/gist-drift-check.py
```

Compares every entry in `gist-mapping.json` against its published gist and
exits non-zero on any mismatch. All gists are public, so this needs no
credentials beyond an authenticated `gh` for the rate limit. Worth running
before touching anything in here.

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

These examples accompany posts at [williamzujkowski.github.io](https://williamzujkowski.github.io). They are drawn from real homelab work, then trimmed for reading — treat them as illustrations of an approach, not as a distribution.

## Related Documentation

- **Blog Posts:** [williamzujkowski.github.io/posts](https://williamzujkowski.github.io/posts/)
- **Agent guidance:** [AGENTS.md](../AGENTS.md)
- **Security posture:** [docs/security-posture.md](../docs/security-posture.md)
- **Uses Page:** [Hardware/Software Stack](https://williamzujkowski.github.io/uses/)

---

**Last Updated:** 2025-11-01
**Total Files:** 50 (46 code files + 4 READMEs)
**Source:** Extracted from blog posts via git history (commits b56c988, eae5dd2)
