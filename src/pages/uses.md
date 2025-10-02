---
title: "Uses"
layout: page
permalink: /uses/
description: "Hardware, software, and services I use and recommend."
eleventyNavigation:
  key: Uses
  order: 6
---

# What I Use

The tools, hardware, and software that power my daily work in security, development, and homelab experimentation. This list evolves as I learn and my needs change.

**Note:** Employer-internal tools and proprietary systems are intentionally omitted for OPSEC. Everything listed here is personal gear, open-source software, or publicly available tools I use in my homelab and side projects.

---

## 🖥️ Hardware

### Workstation
- **Desktop PC** – Intel i9-9900K, 64GB RAM, RTX 3090, 2TB+4TB NVMe, 8TB HDD. Runs VMs, containers, local LLM experiments, and occasional gaming.
- **Laptop** – [Framework Laptop](https://frame.work/) running [Ubuntu 24.04 LTS](https://ubuntu.com/). Repairable, modular, perfect for coffee shop coding and SSH sessions.
- **Displays** – 34" Ultrawide 4K monitor for multitasking without alt-tab hell.

### Peripherals
- **Keyboard** – [Wooting 80HE](https://wooting.io/wooting-80he). Hall effect switches, analog input, keyboard #5 (definitely the last one).
- **Mouse** – [Glorious Model O](https://www.gloriousgaming.com/collections/model-o-mice). Lightweight, great for long coding sessions.
- **Headset** – [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7). Wireless for pacing during calls.
- **Coffee** – [10 Cup Classic Chemex](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex). Critical infrastructure. Productivity dies without it.

### Homelab Infrastructure
- **Firewall** – [Ubiquiti Dream Machine Pro](https://store.ui.com/us/en/products/udm-pro). Handles network security, VLANs, and guest isolation.
- **Hypervisor** – Dell R940 running [Proxmox](https://www.proxmox.com/) with 256GB RAM, 14TB RAID 50.
- **Cluster Nodes** – 3× Raspberry Pi 5 (16GB) for [K3s](https://k3s.io/) experiments and ARM-based testing.
- **Pi-hole** – Raspberry Pi 4 (8GB) running [Pi-hole](https://pi-hole.net/) for network-wide ad blocking.
- **Storage** – [TrueNAS](https://www.truenas.com/) server with 40TB raw storage for backups and media.
- **Networking** – [Ubiquiti](https://ui.com/) switches and access points with VLANs for device isolation.

---

## 💻 Desktop Setup

### Operating System
- **Primary OS** – [Ubuntu 24.04 LTS](https://ubuntu.com/) on Framework, custom PC runs mix of Ubuntu and Windows for gaming.
- **Virtualization** – [Proxmox](https://www.proxmox.com/) for homelab VMs, [Docker Desktop](https://www.docker.com/products/docker-desktop/) and [Podman](https://podman.io/) for containers.

---

## 🖥️ Terminal & Editor

### Terminal
- **Terminal Emulator** – [Ghostty](https://github.com/ghostty-org/ghostty). GPU-accelerated, fast, sane defaults, ended my terminal quest.
- **Shell** – [Zsh](https://www.zsh.org/) with [Oh My Zsh](https://ohmyz.sh/). Plugins: git, docker, kubectl, aws.
- **Multiplexer** – [tmux](https://github.com/tmux/tmux). Essential for persistent sessions and window management.

### Editor
- **Primary Editor** – [VS Code](https://code.visualstudio.com/). Extensions: Python, Go, Terraform, Docker, [GitLens](https://github.com/gitkraken/vscode-gitlens).
- **Theme** – [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme). Tried 20+ themes, always come back to this.

---

## 🔒 SRE/Security Utilities

### Network Analysis
- [Wireshark](https://www.wireshark.org/) – Deep packet inspection and protocol analysis.
- [tcpdump](https://www.tcpdump.org/) – Command-line packet capture for quick troubleshooting.
- [nmap](https://nmap.org/) – Network discovery and port scanning.

### Vulnerability Scanning
- [Nessus](https://www.tenable.com/products/nessus) – Comprehensive vulnerability scanner for homelab security audits.
- [Grype](https://github.com/anchore/grype) – Container image vulnerability scanning for supply chain security.
- [OSV Scanner](https://github.com/google/osv-scanner) – Open-source vulnerability scanning for dependencies.

### Security Tools
- [Wazuh](https://wazuh.com/) – Open-source SIEM for log analysis and threat detection.
- [OWASP ZAP](https://www.zaproxy.org/) – Web application security scanner.
- [Gobuster](https://github.com/OJ/gobuster) – Directory and file enumeration for web testing.
- [John the Ripper](https://www.openwall.com/john/) – Password cracking for security testing (legally).
- [Hashcat](https://hashcat.net/) – GPU-accelerated password recovery tool.

### Authentication & Secrets
- [Bitwarden](https://bitwarden.com/) – Self-hosted password manager (migrated from LastPass).
- [YubiKey 5C NFC](https://www.yubico.com/product/yubikey-5c-nfc/) – Hardware 2FA tokens (own two, lesson learned).
- [HashiCorp Vault](https://www.vaultproject.io/) – Secrets management for homelab automation.

---

## 📝 Note-Taking / PKM

- [Obsidian](https://obsidian.md/) – Markdown-based personal knowledge management with Git version control.
- Replaced Notion for offline access and ownership of notes.
- All notes versioned in Git for backup and history.

---

## 🌐 Browsers

- **Primary** – Firefox (privacy-focused, development tools).
- **Secondary** – Chromium (compatibility testing, some dev tools).

---

## 🤖 AI / Prompting

- **Local LLMs** – Running on RTX 3090 for experiments and learning.
- [Claude](https://claude.ai/) – For research, writing assistance, and technical discussions.
- Open-source models via [Ollama](https://ollama.ai/) and similar frameworks.

---

## ✍️ Blogging & Website

- **Static Site Generator** – [Eleventy (11ty)](https://www.11ty.dev/). Fast, flexible, JavaScript-based.
- **Styling** – [Tailwind CSS](https://tailwindcss.com/). Utility-first CSS framework.
- **Hosting** – [GitHub Pages](https://pages.github.com/). Free, fast, integrated with repo.
- **Version Control** – [GitHub](https://github.com/) for public repos, [GitLab](https://gitlab.com/) for private.
- **CI/CD** – [GitHub Actions](https://github.com/features/actions) for automated builds and deployments.

---

## 🏠 Homelab Services

Self-hosted services running 24/7:

- **Monitoring** – [Wazuh](https://wazuh.com/), [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/), [Netdata](https://www.netdata.cloud/).
- **Media** – [Jellyfin](https://jellyfin.org/) for streaming (open-source Plex alternative).
- **Automation** – [Home Assistant](https://www.home-assistant.io/) for smart home orchestration.
- **Documentation** – [BookStack](https://www.bookstackapp.com/) wiki for homelab notes and runbooks.
- **Code** – [GitLab CE](https://about.gitlab.com/install/ce-or-ee/) for private repositories.
- **Backups** – [Restic](https://restic.net/) to local NAS + [Backblaze B2](https://www.backblaze.com/cloud-storage) for offsite.
- **VPN** – [WireGuard](https://www.wireguard.com/) self-hosted, [ProtonVPN](https://protonvpn.com/) as backup.
- **Mesh VPN** – [Tailscale](https://tailscale.com/) for simple cross-device connectivity.
- **DNS** – [Cloudflare](https://1.1.1.1/) public DNS (1.1.1.1), [Pi-hole](https://pi-hole.net/) for local filtering.

---

## 🛠️ Command Line Tools

Essential CLI utilities I use daily:

```bash
# Development
git             # Version control - https://git-scm.com/
gh              # GitHub CLI - https://cli.github.com/
python3         # Scripting and automation - https://www.python.org/
go              # Performance-critical tools - https://go.dev/
rust            # Learning memory-safe development - https://www.rust-lang.org/

# Infrastructure
terraform       # Infrastructure as Code - https://www.terraform.io/
ansible         # Configuration management - https://www.ansible.com/
docker          # Containerization - https://www.docker.com/
kubectl         # Kubernetes management - https://kubernetes.io/
k3s             # Lightweight Kubernetes - https://k3s.io/

# Utilities
tmux            # Terminal multiplexer - https://github.com/tmux/tmux
fzf             # Fuzzy finder - https://github.com/junegunn/fzf
ripgrep         # Fast code searching - https://github.com/BurntSushi/ripgrep
bat             # Better cat with syntax highlighting - https://github.com/sharkdp/bat
htop            # System resource monitoring - https://htop.dev/
ncdu            # Disk usage analyzer - https://dev.yorhel.nl/ncdu
```

---

## 📚 Learning Resources

- **Platforms** – [Pluralsight](https://www.pluralsight.com/), [O'Reilly Learning](https://www.oreilly.com/), YouTube.
- **Security Labs** – [HackTheBox](https://www.hackthebox.com/), [TryHackMe](https://tryhackme.com/), personal homelab.
- **Threat Intelligence** – [AlienVault OTX](https://otx.alienvault.com/), [abuse.ch](https://abuse.ch/) feeds.

---

## 🎯 Misc

- **API Testing** – [Bruno](https://www.usebruno.com/). Offline-first, no forced sign-in.
- **Monitoring** – [UptimeRobot](https://uptimerobot.com/) for external uptime checks.
- **Build Automation** – [Jenkins](https://www.jenkins.io/) self-hosted for homelab CI/CD.

---

## 💭 Philosophy

My tool selection priorities:

1. **Open Source First** – Support the community, own your tools.
2. **Privacy Conscious** – Your data should be yours.
3. **Automation Friendly** – If I do it twice, it gets scripted.
4. **Learning Focused** – Tools that teach, not just do the job.
5. **Boring Technology** – Reliability matters more than features for critical infrastructure.

---

*This list changes as I learn and my needs evolve. Last updated: 2025-10-02*

*Questions or recommendations? [Contact me](/about/#contact) – always happy to discuss tools, trade war stories, or hear about better alternatives.*
