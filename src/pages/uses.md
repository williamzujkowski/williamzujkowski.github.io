---
layout: page
title: Uses
description: The tools, hardware, and software I use daily for security work and personal projects. My complete tech stack for cybersecurity, development, and homelab.
permalink: /uses/
eleventyNavigation:
  key: Uses
  title: Uses
  order: 4
image: /assets/images/og/uses-og.png
---

# What I Use

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
The gear that keeps me productive, paranoid, and properly caffeinated.
</p>

Let's be real: you're either here because you're shopping for new tech or you're procrastinating. Either way, welcome! This is the constantly evolving list of tools that help me break things professionally and fix them before anyone notices.

## 🖥️ Hardware

### Primary Workstation
- **Desktop**: Custom-built PC (because pre-builts are for people with better things to do)
  - **CPU**: AMD Ryzen 9 5900X (12 cores because VMs breed like rabbits)
  - **RAM**: 64GB DDR4 (50% for work, 50% for Chrome's insatiable hunger)
  - **GPU**: NVIDIA RTX 3090 ("for AI research" *launches game*)
  - **Storage**: 2TB NVMe for OS, 4TB NVMe for VMs, 8TB HDD for "I'll organize this later"
  - **Monitors**: 34" Ultrawide 4k display (because 10 terminal windows need room to breathe)
  
### Laptop
- **Primary**: Framework Laptop
  - Ubuntu 24.04LTS (Great for security tools)
  - Perfect for coffee shop coding and sshing into my other machines
  
### Homelab
- **Firewall**: Protectli Vault FW4B running pfSense
- **Virtualization**: 1x Dell R940
  - Proxmox cluster
  - 256GB RAM total (VMs for days)
- **Storage**: TrueNAS server with 40TB raw storage
- **Networking**: Ubiquiti switches and APs (VLANs everywhere)

### Accessories
- **Keyboard**: [Zinc Wooting 80HE](https://wooting.io/wooting-80he)
- **Mouse**: [Glorious Gaming Model O](https://www.gloriousgaming.com/collections/model-o-mice)
- **Headset**: [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7?srsltid=AfmBOopkaAbInJC_P6KtAgs8SJ9Ugnrxm1a5v1zcAh7jo8ne2kP8d9yb) (wireless for pacing during calls)
- **Coffee**: [10 Cup Classic Chemex](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex)  (critical infrastructure)

## 💻 Desktop Software

### Development
- **Editor**: VS Code (I can exit it without googling)
  - Extensions: Python, Go, Terraform, Docker, GitLens, and 47 others I forgot I installed
  - Theme: Tokyo Night (because dark mode is a lifestyle, not a choice)
- **Terminal**: Ghostty
- **Shell**: Zsh with Oh My Zsh
  - Plugins: git, docker, kubectl, aws

### Security Tools
- **Network Analysis**: Wireshark, tcpdump, nmap
- **Vulnerability Scanning**: Nessus, OSV, Grype
- **SIEM**: Local Wazuh instance for learning
- **Password Manager**: Bitwarden (self-hosted)
- **2FA**: YubiKey 5C NFC (two of them, because redundancy)

### Virtualization & Containers
- **Hypervisor**: Proxmox (homelab)
- **Containers**: Docker Desktop, Podman
- **Orchestration**: K3s for learning Kubernetes
- **IaC**: Terraform, Ansible


## 🛠️ Command Line Tools

My most-used CLI tools:

```bash
# Security
nmap            # Network discovery
zap           # Web server scanner
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
A: Yes. Linux for when I want control, macOS for when I want things to work, and Windows for when I hate myself (kidding! ...mostly).

**Q: Favorite programming language?**  
A: Python for quick scripts, Go for tools, Rust for learning. Bash for gluing it all together.

**Q: How do you keep up with all these tools?**  
A: Bold of you to assume I keep up. I learn tools when something breaks or when someone on Reddit makes it sound cool. The secret? Most tools do the same thing with different syntax.

**Q: What's your backup strategy?**  
A: Automated hourly snapshots locally, daily to NAS, weekly to cloud. Test restores monthly.

**Q: Coffee or tea?**  
A: Coffee for coding, tea for reading, energy drinks for incidents, water for recovery, and whiskey for post-mortems (after hours, of course).

---

## The Truth About All This

Look, half these tools will be obsolete in two years. The other half I'll replace because someone on Hacker News said there's something better. But right now? This setup lets me break things efficiently, fix them before anyone notices, and occasionally feel like I know what I'm doing.

The real secret? It's not about having the perfect tools – it's about knowing when to use them and when to just turn it off and on again.

*Got questions about any of these tools? Want to argue about why your setup is better? Found a typo that's been bothering you? [Hit me up!](/about/#contact) I promise to defend my choices with completely objective and not-at-all-emotional arguments.*

</div>