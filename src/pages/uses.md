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

**Fair warning**: Half of this stuff was bought at 2 AM after convincing myself it was "essential." The other half actually is essential, but I can't always tell which is which anymore.

## 🖥️ Hardware

### Primary Workstation
- **Desktop**: Custom-built PC (because pre-builts are for people with better things to do)
  - **Processor**: Intel(R) Core(TM) i9-9900K CPU @ 3.60GHz – Yes, it's older. No, I don't need the latest. It compiles code and runs 47 Docker containers just fine, thank you.
  - **RAM**: 64GB DDR4 – Started with 32GB. Then I tried running Kubernetes locally. Then I discovered Chrome could eat RAM faster than Kubernetes. Now here we are.
  - **GPU**: NVIDIA RTX 3090 – Bought "for local LLM experiments." Currently splits time 70% actual AI work, 20% "just testing this game's performance," 10% sitting idle while I use CPU for everything.
  - **Storage**: 2TB NVMe for OS, 4TB NVMe for VMs, 8TB HDD for "I'll organize this later" – Spoiler: I never organize it later. There are VM snapshots from 2022 I'm afraid to delete.
  - **Monitors**: 34" Ultrawide 4k display – Justified as "productivity enhancement." Reality: I just like having tmux, VS Code, browser, and Slack visible without alt-tabbing. Peak laziness efficiency.
  
### Laptop
- **Primary**: [Framework Laptop](https://frame.work/)
  - [Ubuntu 24.04LTS](https://ubuntu.com/) – Went through the distro-hopping phase years ago. Arch, Gentoo, obscure ones nobody's heard of. Now? Ubuntu just works and I have actual work to do.
  - Perfect for coffee shop coding and sshing into my other machines
  - **The real story**: Bought into the repairability dream after my last laptop's keyboard died 2 days past warranty. So far I've only swapped ports twice, but the peace of mind is worth it.
  
### Homelab (The Money Pit)
- **Firewall**: Dream Machine Professional running [pfSense](https://www.pfsense.org/)
  - Started with a consumer router. Then pfSense on an old PC. Now this. My network security has evolved; my wallet has devolved.
  
- **Virtualization** (aka "The Space Heater Collection"): 
  - 1x Dell R940
    - [Proxmox](https://www.proxmox.com/) cluster
    - 256GB RAM – Because apparently I thought I was building a datacenter
    - 14TB RAID 50 – Half full of "temporary" test VMs from 2023
    - **Truth**: Bought from a company liquidation. Saved thousands! Spent hundreds on power bills. Math is hard.
  
  - 3x Raspberry Pi 5 16GB
    - For "ARM-based shenanigans" (translation: I wanted to play with K3s clustering)
    - One runs production services, two are "for testing" (they've been idle for months)
  
  - 1x Raspberry Pi 4 8GB
    - [Pi-hole](https://pi-hole.net/) – The family peace keeper. Blocks ads = happy spouse.
    - Most important device in the house. If this dies, I hear about it immediately.

- **Storage**: [TrueNAS](https://www.truenas.com/) server with 40TB raw storage
  - 30TB of Linux ISOs (*wink*), 5TB of actual backups, 5TB of "I should probably delete this"
  
- **Networking**: [Ubiquiti](https://ui.com/) switches and APs
  - VLANs everywhere because I trust nothing, including my own IoT devices
  - Guest network is more locked down than some corporate networks I've seen

### Accessories (The Rabbit Holes)
- **Keyboard**: [Zinc Wooting 80HE](https://wooting.io/wooting-80he)
  - Fell down the mechanical keyboard rabbit hole. This is keyboard #5. I told myself I'd stop here. (I won't.)
  - Hall effect switches because "I need the precision." Really I just like the magnetic click sound.
  
- **Mouse**: [Glorious Gaming Model O](https://www.gloriousgaming.com/collections/model-o-mice)
  - Lightest mouse I've owned. Great for those 14-hour coding sessions where every gram counts. Or so I tell myself.
  
- **Headset**: [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7?srsltid=AfmBOopkaAbInJC_P6KtAgs8SJ9Ugnrxm1a5v1zcAh7jo8ne2kP8d9yb)
  - Wireless for pacing during calls (I'm a pacer, it's a problem)
  - Battery dies at the worst possible moments. Always during important meetings. Always.
  
- **Coffee**: [10 Cup Classic Chemex](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex)
  - Started with a Keurig. Then French press. Then pour-over. Now this.
  - Yes, I'm that person who weighs beans and times the bloom. Judge away.
  - **Critical infrastructure** – This dies, productivity dies.

## 💻 Desktop Software

### Development
- **Editor**: [VS Code](https://code.visualstudio.com/)
  - Yes, I know about Neovim. Yes, I tried it. Yes, I went back to VS Code. Fight me.
  - Extensions: Python, Go, Terraform, Docker, [GitLens](https://github.com/gitkraken/vscode-gitlens), and 47 others I forgot I installed
  - Half my extensions conflict with each other. I'm afraid to remove any.
  - Theme: [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme) – Changed themes 20 times. Always come back to this.
  
- **Terminal**: [Ghostty](https://github.com/ghostty-org/ghostty)
  - Tried Alacritty, Kitty, iTerm2, and about 10 others
  - Picked this one because it was fast and I was tired of configuring terminals
  
- **Shell**: [Zsh](https://www.zsh.org/) with [Oh My Zsh](https://ohmyz.sh/)
  - Spent a weekend customizing the perfect prompt. Changed it back to default a month later.
  - Plugins: git, docker, kubectl, aws, and 15 others that probably slow everything down

### Security Tools
- **Network Analysis**: [Wireshark](https://www.wireshark.org/), [tcpdump](https://www.tcpdump.org/), [nmap](https://nmap.org/)
  - Wireshark for when I need the GUI comfort blanket
  - tcpdump for when I'm trying to look cool in the terminal
  - nmap for "why isn't this port responding?" (it's always the firewall)
  
- **Vulnerability Scanning**: [Nessus](https://www.tenable.com/products/nessus), [OSV](https://github.com/google/osv-scanner), [Grype](https://github.com/anchore/grype)
  - Nessus finds everything wrong with my network. I fix 10%. This is the way.
  - Grype for container scanning because I'm paranoid about supply chain attacks
  
- **SIEM**: Local [Wazuh](https://wazuh.com/) instance
  - "For learning" = I check it once a month, get scared by the alerts, close tab
  
- **Password Manager**: [Bitwarden](https://bitwarden.com/) (self-hosted)
  - Migrated from LastPass during the Great Breach Exodus
  - Self-hosted because I trust myself more than companies (debatable decision)
  
- **2FA**: [YubiKey 5C NFC](https://www.yubico.com/product/yubikey-5c-nfc/)
  - Two of them because I WILL lose one eventually
  - Already had one close call involving a washing machine. Don't ask.

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
- [Tailscale](https://tailscale.com/) – WireGuard was great until I had to manage it across 10 devices. Tailscale just works.
- [Bruno](https://www.usebruno.com/) – Postman wanted me to sign in to save collections locally. Bruno doesn't. Sold.

### Removed (With Lessons Learned)
- **LastPass** → Self-hosted Bitwarden
  - The breaches were the final straw. Now I control my own password destiny (and backup anxiety)
  
- **VMware ESXi** → Proxmox
  - Broadcom acquisition pricing made this decision for me
  - Proxmox does 100% of what I need for 0% of the cost
  
- **Notion** → [Obsidian](https://obsidian.md/) + Git
  - Notion is great until you're offline and need your notes
  - Markdown files + Git = simple, searchable, greppable, mine forever

## 💡 Hard-Won Lessons

1. **Version Control Everything**
   - Even my Obsidian notes are in Git. Learned this after losing 3 months of documentation to a corrupted drive.
   - Commit messages for personal notes are hilarious in retrospect: "why won't this work", "maybe this?", "IT WORKS!"

2. **Automate Backups (Then Test Them)**
   - 3-2-1 rule: 3 copies, 2 different media, 1 offsite
   - Learned this after my "bulletproof" RAID array wasn't bulletproof against me typing the wrong command
   
3. **Document Your Setup**
   - Future you will thank present you
   - Past me is an idiot who never documents anything. Present me suffers. The cycle continues.
   
4. **Test Your Backups**
   - A backup you haven't restored is Schrödinger's backup
   - Found out the hard way that my "automated backups" were backing up empty directories for 6 months
   
5. **The Tool Trap**
   - The best tool isn't the newest or most featured
   - It's the one you'll actually use consistently
   - My abandoned tools graveyard is vast and expensive

## 🤔 Frequently Asked Questions

**Q: Windows, Linux, or macOS?**  
A: Linux on everything that matters. Windows on the gaming rig that I tell myself is "also for testing Windows-specific security tools." Used macOS for a year – nice hardware, but I missed my package manager too much.

**Q: Favorite programming language?**  
A: Python when I need something done yesterday. Go when I need it to run everywhere. Rust when I want to feel smart (then dumb, then smart again). Bash for crimes against maintainability. Currently learning Zig because apparently I hate free time.

**Q: How do you keep up with all these tools?**  
A: That's the neat part – I don't! I learn tools in three ways:
1. Something breaks catastrophically 
2. Someone on r/selfhosted makes it sound life-changing
3. 2 AM rabbit holes that start with "I wonder if there's a better way to..."

**Q: What's your backup strategy?**  
A: Automated hourly snapshots locally, daily to NAS, weekly to B2 cloud. Test restores monthly(ish... okay, when I remember). Already lost data twice – both times were "temporary" folders that weren't temporary. Now everything gets backed up.

**Q: Biggest homelab mistake?**  
A: Tie between:
- Buying enterprise gear without checking power consumption (RIP electric bill)
- Setting up 47 services before configuring backups
- That time I ran `rm -rf /` on the wrong SSH session (thank god for snapshots)

**Q: Coffee or tea?**  
A: Coffee for coding (chemex or death). Tea for reading docs. Energy drinks for "production is down" moments. Water for pretending to be healthy. Whiskey for successful deployments and failed deployments alike.

**Q: Is all this really necessary?**  
A: Absolutely not. Could I do my job with a laptop and AWS? Yes. But where's the fun in that? This is my adult version of Legos, except more expensive and occasionally on fire.

---

## The Real Talk Section

Let's be honest about what this page really is: a monument to decision fatigue and midnight impulse purchases. Half these tools will be obsolete in two years. The other half I'll replace because someone on Hacker News wrote a convincing blog post at exactly the wrong time (when I'm frustrated with my current setup).

Here's what I've learned after years of tool-hopping:

- **The 80/20 rule is real**: I use 20% of these tools 80% of the time. The rest are for specific situations that happen twice a year.
- **Simple usually wins**: Every time I've replaced a simple tool with a "more powerful" one, I've eventually gone back.
- **The grass isn't greener**: It's just different grass with different bugs.
- **Money doesn't solve problems**: But it does create new, more expensive ones.

But you know what? This ridiculous setup – overpriced, overcomplicated, and absolutely overkill – makes me happy. It lets me learn, experiment, break things (in my own environment), and yes, occasionally feel like I actually know what I'm doing.

The real secret nobody tells you? **Everyone's setup is held together with bash scripts, cron jobs, and hope.** Mine just has RGB lighting.

*Got questions about any of these tools? Want to argue about why your setup is better? Found a typo that's been bothering you? [Hit me up!](/about/#contact) I promise to defend my choices with completely objective and not-at-all-emotional arguments.*

</div>