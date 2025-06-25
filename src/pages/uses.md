---
layout: page
title: Uses
description: The tools, hardware, and software I use daily for security work and personal projects. My complete tech stack for cybersecurity, development, and homelab.
permalink: /uses/
eleventyNavigation:
  key: Uses
  title: Uses
  order: 7
image: /assets/images/og/uses-og.png
---

# What I Use

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
A living document of the tools and tech stack that powers my work and play.
</p>

Inspired by [uses.tech](https://uses.tech/), this page details the hardware, software, and services I rely on daily. As a security engineer who loves tinkering, this list changes frequently as I discover new tools or optimize my workflow.

## 🖥️ Hardware

### Primary Workstation
- **Desktop**: Custom-built PC (because pre-builts never have enough USB ports)
  - **CPU**: AMD Ryzen 9 5900X (12 cores for all those VMs)
  - **RAM**: 64GB DDR4 (Chrome tabs are hungry)
  - **GPU**: NVIDIA RTX 3090 (for AI experiments, definitely not gaming)
  - **Storage**: 2TB NVMe for OS, 4TB NVMe for VMs, 8TB HDD for backups
  - **Monitors**: 34" Ultrawide 4k display (security dashboards need space)
  
### Laptop
- **Primary**: Framework Laptop
  - Ubuntu 24.04LTS (Great for security tools)
  - Perfect for coffee shop coding and on-site work
  
### Homelab
- **Firewall**: Protectli Vault FW4B running pfSense
- **Virtualization**: 1x Dell R940
  - Proxmox cluster
  - 256GB RAM total (VMs for days)
- **Storage**: TrueNAS server with 40TB raw storage
- **Networking**: Ubiquiti switches and APs (VLANs everywhere)

### Accessories
- **Keyboard**: ZSA Moonlander (split ortholinear, because ergonomics)
- **Mouse**: Logitech MX Master 3
- **Webcam**: Logitech Brio (for those "camera on" meetings)
- **Headset**: SteelSeries Arctis 7 (wireless for pacing during calls)
- **Coffee**: Breville Barista Express (critical infrastructure)

## 💻 Desktop Software

### Development
- **Editor**: VS Code (sorry Vim, it's not you, it's me)
  - Extensions: Python, Go, Terraform, Docker, GitLens
  - Theme: Tokyo Night (easy on the eyes during late-night incidents)
- **Terminal**: Ghostty
- **Shell**: Zsh with Oh My Zsh
  - Theme: Powerlevel10k
  - Plugins: git, docker, kubectl, aws

### Security Tools
- **Network Analysis**: Wireshark, tcpdump, nmap
- **Vulnerability Scanning**: Nessus, OpenVAS
- **SIEM**: Local Wazuh instance for learning
- **Password Manager**: Bitwarden (self-hosted)
- **2FA**: YubiKey 5C NFC (two of them, because redundancy)

### Virtualization & Containers
- **Hypervisor**: Proxmox (homelab)
- **Containers**: Docker Desktop, Podman
- **Orchestration**: K3s for learning Kubernetes
- **IaC**: Terraform, Ansible

### Productivity
- **Notes**: Obsidian (markdown everything)
- **Tasks**: Todoist (keeping track of all the things)
- **Communication**: Signal, Discord, Slack
- **Browser**: Firefox (primary), Chrome (testing), Brave (privacy)

## 🛠️ Command Line Tools

My most-used CLI tools:

```bash
# Security
nmap            # Network discovery
nikto           # Web server scanner
gobuster        # Directory/file enumeration
john            # Password cracking (legally!)
hashcat         # GPU-accelerated password recovery

# Development
git             # Version control
gh              # GitHub CLI
python3         # Scripting and automation
go              # For performance-critical tools
rust            # Learning for memory-safe tools

# Infrastructure
terraform       # Infrastructure as Code
ansible         # Configuration management
docker          # Containerization
kubectl         # Kubernetes management

# Utilities
tmux            # Terminal multiplexer
fzf             # Fuzzy finder
ripgrep         # Fast searching
bat             # Better cat
htop            # System monitoring
ncdu            # Disk usage analyzer
```

## ☁️ Services & SaaS

### Development
- **Code Hosting**: GitHub (public), GitLab (private)
- **CI/CD**: GitHub Actions, self-hosted Jenkins
- **Monitoring**: Netdata (self-hosted), UptimeRobot

### Security
- **Threat Intel**: AlienVault OTX, abuse.ch feeds
- **DNS**: Cloudflare (1.1.1.1), Pi-hole (local)
- **VPN**: WireGuard (self-hosted), ProtonVPN (backup)

### Learning
- **Courses**: Pluralsight, Linux Academy, YouTube University
- **Labs**: HackTheBox, TryHackMe, personal lab
- **Reading**: O'Reilly Learning, research papers

## 🎮 Homelab Services

Self-hosted services running 24/7:

- **Monitoring**: Wazuh, Grafana, Prometheus
- **Media**: Jellyfin (like Plex but open source)
- **Automation**: Home Assistant (smart home)
- **Documentation**: BookStack wiki
- **Code**: GitLab CE
- **Secrets**: Vault by HashiCorp
- **Backups**: Restic to local NAS + B2

## 📱 Mobile

- **Phone**: Pixel 7 Pro (GrapheneOS for privacy)
- **Tablet**: iPad Pro (for reading documentation)
- **Apps**: 
  - Termux (terminal on Android)
  - Bitwarden
  - ProtonMail
  - Signal
  - Authy (backup 2FA)

## 🎯 Philosophy

My tool choices are guided by:

1. **Open Source First**: Support the community that taught me
2. **Privacy Conscious**: Your data is your data
3. **Automation Friendly**: If I do it twice, it gets scripted
4. **Learning Focused**: Tools that teach, not just do
5. **Reliability**: Boring technology for critical stuff

## 🔄 Recent Changes

### Added (Last 3 Months)
- Ollama for local LLM experiments
- Tailscale for zero-config VPN
- Bruno as Postman alternative

### Removed
- LastPass (moved to self-hosted Bitwarden)
- VMware ESXi (Proxmox does everything I need)
- Notion (Obsidian + Git is simpler)

## 💡 Pro Tips

1. **Version Control Everything**: Even my Obsidian notes are in Git
2. **Automate Backups**: 3-2-1 rule saved me more than once
3. **Document Your Setup**: Future you will thank present you
4. **Test Your Backups**: Schrödinger's backup isn't a backup
5. **Keep Learning**: The best tool is the one you understand

## 🤔 Frequently Asked Questions

**Q: Windows, Linux, or macOS?**  
A: Yes. Windows for gaming, Linux for work, macOS for iOS development. WSL2 bridges the gap beautifully.

**Q: Favorite programming language?**  
A: Python for quick scripts, Go for tools, Rust for learning. Bash for gluing it all together.

**Q: How do you keep up with all these tools?**  
A: I don't. I learn what I need when I need it. The fundamentals transfer between tools.

**Q: What's your backup strategy?**  
A: Automated hourly snapshots locally, daily to NAS, weekly to cloud. Test restores monthly.

**Q: Coffee or tea?**  
A: Coffee for coding, tea for reading, water for incidents (hydration is key).

---

*This page is updated regularly as my setup evolves. Last major update: January 2025*

*Have questions about any of these tools? Want to share your setup? [Let's connect!](/contact/)*

</div>