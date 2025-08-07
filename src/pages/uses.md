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
- **Primary**: [Framework Laptop](https://frame.work/)
  - [Ubuntu 24.04LTS](https://ubuntu.com/) (Great for security tools)
  - Perfect for coffee shop coding and sshing into my other machines
  
### Homelab
- **Firewall**: [Protectli Vault FW4B](https://protectli.com/vault-4-port/) running [pfSense](https://www.pfsense.org/)
- **Virtualization**: 1x Dell R940
  - [Proxmox](https://www.proxmox.com/) cluster
  - 256GB RAM total (VMs for days)
- **Storage**: [TrueNAS](https://www.truenas.com/) server with 40TB raw storage
- **Networking**: [Ubiquiti](https://ui.com/) switches and APs (VLANs everywhere)

### Accessories
- **Keyboard**: [Zinc Wooting 80HE](https://wooting.io/wooting-80he)
- **Mouse**: [Glorious Gaming Model O](https://www.gloriousgaming.com/collections/model-o-mice)
- **Headset**: [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7?srsltid=AfmBOopkaAbInJC_P6KtAgs8SJ9Ugnrxm1a5v1zcAh7jo8ne2kP8d9yb) (wireless for pacing during calls)
- **Coffee**: [10 Cup Classic Chemex](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex)  (critical infrastructure)

## 💻 Desktop Software

### Development
- **Editor**: [VS Code](https://code.visualstudio.com/) (I can exit it without googling)
  - Extensions: Python, Go, Terraform, Docker, [GitLens](https://github.com/gitkraken/vscode-gitlens), and 47 others I forgot I installed
  - Theme: [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme) (because dark mode is a lifestyle, not a choice)
- **Terminal**: [Ghostty](https://github.com/ghostty-org/ghostty)
- **Shell**: [Zsh](https://www.zsh.org/) with [Oh My Zsh](https://ohmyz.sh/)
  - Plugins: git, docker, kubectl, aws

### Security Tools
- **Network Analysis**: [Wireshark](https://www.wireshark.org/), [tcpdump](https://www.tcpdump.org/), [nmap](https://nmap.org/)
- **Vulnerability Scanning**: [Nessus](https://www.tenable.com/products/nessus), [OSV](https://github.com/google/osv-scanner), [Grype](https://github.com/anchore/grype)
- **SIEM**: Local [Wazuh](https://wazuh.com/) instance for learning
- **Password Manager**: [Bitwarden](https://bitwarden.com/) (self-hosted)
- **2FA**: [YubiKey 5C NFC](https://www.yubico.com/product/yubikey-5c-nfc/) (two of them, because redundancy)

### Virtualization & Containers
- **Hypervisor**: [Proxmox](https://www.proxmox.com/) (homelab)
- **Containers**: [Docker Desktop](https://www.docker.com/products/docker-desktop/), [Podman](https://podman.io/)
- **Orchestration**: [K3s](https://k3s.io/) for learning Kubernetes
- **IaC**: [Terraform](https://www.terraform.io/), [Ansible](https://www.ansible.com/)


## 🛠️ Command Line Tools

My most-used CLI tools:

```bash
# Security
nmap            # Network discovery - https://nmap.org/
zap             # Web server scanner - https://www.zaproxy.org/
gobuster        # Directory/file enumeration - https://github.com/OJ/gobuster
john            # Password cracking (legally!) - https://www.openwall.com/john/
hashcat         # GPU-accelerated password recovery - https://hashcat.net/

# Development
git             # Version control - https://git-scm.com/
gh              # GitHub CLI - https://cli.github.com/
python3         # Scripting and automation - https://www.python.org/
go              # For performance-critical tools - https://go.dev/
rust            # Learning for memory-safe tools - https://www.rust-lang.org/

# Infrastructure
terraform       # Infrastructure as Code - https://www.terraform.io/
ansible         # Configuration management - https://www.ansible.com/
docker          # Containerization - https://www.docker.com/
kubectl         # Kubernetes management - https://kubernetes.io/

# Utilities
tmux            # Terminal multiplexer - https://github.com/tmux/tmux
fzf             # Fuzzy finder - https://github.com/junegunn/fzf
ripgrep         # Fast searching - https://github.com/BurntSushi/ripgrep
bat             # Better cat - https://github.com/sharkdp/bat
htop            # System monitoring - https://htop.dev/
ncdu            # Disk usage analyzer - https://dev.yorhel.nl/ncdu
```

## ☁️ Services & SaaS

### Development
- **Code Hosting**: [GitHub](https://github.com/) (public), [GitLab](https://gitlab.com/) (private)
- **CI/CD**: [GitHub Actions](https://github.com/features/actions), self-hosted [Jenkins](https://www.jenkins.io/)
- **Monitoring**: [Netdata](https://www.netdata.cloud/) (self-hosted), [UptimeRobot](https://uptimerobot.com/)

### Security
- **Threat Intel**: [AlienVault OTX](https://otx.alienvault.com/), [abuse.ch](https://abuse.ch/) feeds
- **DNS**: [Cloudflare](https://1.1.1.1/) (1.1.1.1), [Pi-hole](https://pi-hole.net/) (local)
- **VPN**: [WireGuard](https://www.wireguard.com/) (self-hosted), [ProtonVPN](https://protonvpn.com/) (backup)

### Learning
- **Courses**: [Pluralsight](https://www.pluralsight.com/), [Linux Academy](https://linuxacademy.com/), YouTube University
- **Labs**: [HackTheBox](https://www.hackthebox.com/), [TryHackMe](https://tryhackme.com/), personal lab
- **Reading**: [O'Reilly Learning](https://www.oreilly.com/), research papers

## 🎮 Homelab Services

Self-hosted services running 24/7:

- **Monitoring**: [Wazuh](https://wazuh.com/), [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/)
- **Media**: [Jellyfin](https://jellyfin.org/) (like Plex but open source)
- **Automation**: [Home Assistant](https://www.home-assistant.io/) (smart home)
- **Documentation**: [BookStack](https://www.bookstackapp.com/) wiki
- **Code**: [GitLab CE](https://about.gitlab.com/install/ce-or-ee/)
- **Secrets**: [Vault](https://www.vaultproject.io/) by HashiCorp
- **Backups**: [Restic](https://restic.net/) to local NAS + [B2](https://www.backblaze.com/cloud-storage)

## 🎯 Philosophy

My tool choices are guided by:

1. **Open Source First**: Support the community that taught me
2. **Privacy Conscious**: Your data is your data
3. **Automation Friendly**: If I do it twice, it gets scripted
4. **Learning Focused**: Tools that teach, not just do
5. **Reliability**: Boring technology for critical stuff

## 🔄 Recent Changes

### Added (Last 3 Months)
- [Tailscale](https://tailscale.com/) for zero-config VPN
- [Bruno](https://www.usebruno.com/) as Postman alternative

### Removed
- LastPass (moved to self-hosted Bitwarden)
- VMware ESXi (Proxmox does everything I need)
- Notion ([Obsidian](https://obsidian.md/) + Git is simpler)

## 💡 Pro Tips

1. **Version Control Everything**: Even my Obsidian notes are in Git
2. **Automate Backups**: 3-2-1 rule saved me more than once
3. **Document Your Setup**: Future you will thank present you
4. **Test Your Backups**: Schrödinger's backup isn't a backup
5. **Keep Learning**: The best tool is the one you understand

## 🤔 Frequently Asked Questions

**Q: Windows, Linux, or macOS?**  
A: Yes. Linux for when I want control, macOS for when I want things to work, and Windows for the last few games that don't support linux via proton.

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