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

## 🎯 My Setup Philosophy

Before we dive into the hardware porn, here's the method to my madness:

**The Evolution Principle**: Every tool on this list has replaced something else. I started simple, hit limitations, overcomplicated things, then gradually found my way back to sensible solutions. This isn't my first setup – it's probably my seventh.

**The "Good Enough" Threshold**: I've learned to ask "Does this solve my actual problem?" instead of "Is this the absolute best?" The graveyard of abandoned tools taught me that "better" often means "different problems I don't want."

**The Learning Investment**: I pick tools that teach me something while solving problems. If I'm going to spend time learning a new workflow, it better expand my capabilities, not just change the color scheme.

**The Future Self Test**: Will I understand my own setup in six months? If it requires a PhD in configuration management to maintain, it's probably not sustainable.

**The 3 AM Rule**: Can I troubleshoot this when I'm half-asleep and everything's broken? If it takes 47 steps to get logs, it's too complex for production.

My priorities have shifted over the years:
- **Early 20s**: Latest and greatest everything
- **Mid 20s**: Maximum customization (rice everything!)
- **Late 20s**: Reliability over features
- **Now**: Time is more valuable than optimization

The result? A setup that's powerful enough for professional work, stable enough to trust, and simple enough that I actually use it instead of constantly tweaking it.

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
  - **Evolution moment**: This replaced a ThinkPad that lasted 8 years but wasn't repairable. The Framework philosophy of "fix it yourself" appealed to my inner control freak. Plus, USB-C on both sides? Revolutionary for someone who's never plugged in a cable correctly on the first try.
  
### Homelab (The Money Pit)
- **Firewall**: [Dream Machine Professional](https://store.ui.com/us/en/products/udm-pro)
  - Started with a consumer router. Then pfSense on an old PC. Now this. My network security has evolved; my wallet has devolved.
  - **The journey**: Netgear → "I should learn pfSense" (six months of configuration hell) → "Maybe I'll just buy something that works" → UDM Pro. Sometimes the enterprise solution is worth the premium for your sanity.
  
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
  - **The descent**: Started with a basic Dell membrane → "Maybe a mechanical?" → Cherry MX Blues → "Actually these are too loud" → Browns → "What about tactile switches?" → Custom build with lubed switches → "Okay but what about analog input?" → Hall effects. Each upgrade was "definitely the last one."
  
- **Mouse**: [Glorious Gaming Model O](https://www.gloriousgaming.com/collections/model-o-mice)
  - Lightest mouse I've owned. Great for those 14-hour coding sessions where every gram counts. Or so I tell myself.
  
- **Headset**: [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7?srsltid=AfmBOopkaAbInJC_P6KtAgs8SJ9Ugnrxm1a5v1zcAh7jo8ne2kP8d9yb)
  - Wireless for pacing during calls (I'm a pacer, it's a problem)
  - Battery dies at the worst possible moments. Always during important meetings. Always.
  
- **Coffee**: [10 Cup Classic Chemex](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex)
  - Started with a Keurig. Then French press. Then pour-over. Now this.
  - Yes, I'm that person who weighs beans and times the bloom. Judge away.
  - **Critical infrastructure** – This dies, productivity dies.
  - **The coffee evolution**: Folgers instant → Keurig ("I'm so sophisticated!") → French press ("This is the way") → V60 pour-over → Chemex → Currently eyeing a $3000 espresso machine I definitely don't need. The rabbit hole never ends, it just gets more caffeinated.

## 💻 Desktop Software

### Development
- **Editor**: [VS Code](https://code.visualstudio.com/)
  - Yes, I know about Neovim. Yes, I tried it. Yes, I went back to VS Code. Fight me.
  - Extensions: Python, Go, Terraform, Docker, [GitLens](https://github.com/gitkraken/vscode-gitlens), and 47 others I forgot I installed
  - Half my extensions conflict with each other. I'm afraid to remove any.
  - Theme: [Tokyo Night](https://github.com/enkia/tokyo-night-vscode-theme) – Changed themes 20 times. Always come back to this.
  - **The vim confession**: Spent 6 months learning vim, got decent at it, spent another 3 months perfecting my nvim config. Then I needed to quickly fix something on a colleague's machine that only had VS Code. Realized I was more productive in 5 minutes of VS Code than 9 months of vim perfectionism. Sometimes the pragmatic choice wins.
  
- **Terminal**: [Ghostty](https://github.com/ghostty-org/ghostty)
  - Tried Alacritty, Kitty, iTerm2, and about 10 others
  - Picked this one because it was fast and I was tired of configuring terminals
  - **Terminal fatigue**: The great terminal quest of 2023. Started because "the default terminal is slow." Spent 3 weeks testing every GPU-accelerated terminal, tweaking configs, optimizing startup times. Ghostty won by being fast AND having sane defaults. Lesson learned: sometimes "fast enough" and "works out of the box" beats "theoretically optimal."
  
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
  - **Reality check**: Set this up to "understand enterprise security better." Turns out my homelab generates more false positives than actual threats. Every SSH login from my phone looks suspicious. Every Docker container restart triggers an alert. I've learned more about alert fatigue than actual threats.
  
- **Password Manager**: [Bitwarden](https://bitwarden.com/) (self-hosted)
  - Migrated from LastPass during the Great Breach Exodus
  - Self-hosted because I trust myself more than companies (debatable decision)
  - **Migration saga**: LastPass → "I'll just use a spreadsheet temporarily" (lasted 2 days) → 1Password trial → KeePass ("This is too complicated") → Bitwarden cloud → "Wait, I can self-host this?" → Current setup. Each migration taught me more about backup strategies than I wanted to know.
  
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

## 💥 Spectacular Failures & Hard Lessons

Before we get to the recent wins, let's talk about the expensive mistakes:

### The VMware Overkill Era (2022-2023)
**What I thought**: "Enterprise hypervisor = professional setup"
**Reality**: Spent $600/year on vSphere licenses for features I used exactly once
**Lesson**: Enterprise doesn't automatically mean better for homelab
**Result**: Moved to Proxmox, saved money, gained functionality

### The Kubernetes Everything Phase (2023)
**What I thought**: "I should containerize my entire life"
**Reality**: Spent 3 months setting up K8s to run... a single WordPress blog
**The wake-up call**: Realized I was using a nuclear reactor to power a nightlight
**Lesson**: Match complexity to the problem, not your resume goals
**Result**: Most services now run in Docker Compose. It's boring. It works.

### The Security Theater Spiral (Early 2024)
**What I thought**: "More security tools = more secure"
**Reality**: 47 different scanning tools generating 10,000 alerts/day
**The breakdown**: Spent more time managing security tools than securing anything
**Lesson**: Defense in depth ≠ tool in every category
**Result**: Focused on fundamentals: patching, backups, monitoring basics

### The Perfect Monitoring Delusion (Mid 2024)
**What I thought**: "I need enterprise-grade observability"
**Reality**: Spent 2 months building a monitoring stack more complex than some companies use in production
**The irony**: The monitoring system needed monitoring
**Lesson**: You can't optimize what you don't understand, and you can't understand what you over-engineer
**Result**: Simplified to Grafana + Prometheus + basic alerting. Sleep better now.

### The "I'll Build My Own" Mistakes
**DNS Server**: "How hard can it be?" Very hard. Pi-hole exists for a reason.
**Backup Solution**: "I'll script something custom." Narrator: He did not account for error handling.
**Load Balancer**: "HAProxy is just a config file." Three weeks later: nginx with simple config.

**Meta-lesson**: The open source community has solved most problems better than you will in your spare time.

## 🔄 Recent Changes

### Added (Last 3 Months)
- [Tailscale](https://tailscale.com/) – WireGuard was great until I had to manage it across 10 devices. Tailscale just works.
- [Bruno](https://www.usebruno.com/) – Postman wanted me to sign in to save collections locally. Bruno doesn't. Sold.

### Removed (With Lessons Learned)
- **LastPass** → Self-hosted Bitwarden
  - The breaches were the final straw. Now I control my own password destiny (and backup anxiety)
  
- **VMware ESXi** → Proxmox
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

**The language journey**: Started with Python in college (still love it). Added JavaScript because "web development pays well." Learned Go because "performance matters" (it does, sometimes). Tried Rust because "memory safety" (gave up twice, succeeded on attempt #3). Bash because "I'll just automate this one thing" (500 lines later...). Each language taught me something about problem-solving, even when I didn't stick with it.

**Q: How do you keep up with all these tools?**  
A: That's the neat part – I don't! I learn tools in three ways:
1. Something breaks catastrophically 
2. Someone on r/selfhosted makes it sound life-changing
3. 2 AM rabbit holes that start with "I wonder if there's a better way to..."

**Q: What's your backup strategy?**  
A: Automated hourly snapshots locally, daily to NAS, weekly to B2 cloud. Test restores monthly(ish... okay, when I remember). Already lost data twice – both times were "temporary" folders that weren't temporary. Now everything gets backed up.

**Q: Biggest homelab mistake?**
A: Tie between:
- Buying enterprise gear without checking power consumption (RIP electric bill, RIP marriage approval)
- Setting up 47 services before configuring backups (learned about RAID 0 vs RAID 1 the hard way)
- That time I ran `rm -rf /` on the wrong SSH session (thank god for snapshots... that I'd set up the week before)
- Thinking "enterprise-grade" automatically meant "homelab-appropriate" (spoiler: 42U of server rack doesn't fit in a studio apartment)

**Q: Coffee or tea?**  
A: Coffee for coding (chemex or death). Tea for reading docs. Energy drinks for "production is down" moments. Water for pretending to be healthy. Whiskey for successful deployments and failed deployments alike.

**Q: Is all this really necessary?**
A: Absolutely not. Could I do my job with a laptop and cloud services? Yes. But where's the fun in that? This is my adult version of Legos, except more expensive and occasionally on fire.

**The honest answer**: The homelab started as "learning for work." Then it became "learning for learning." Now it's mostly "this is relaxing and I like fixing things." It's hobby infrastructure disguised as professional development. The tax deduction helps justify it, but really I just enjoy building systems that work (eventually).

---

## The Real Talk Section

Let's be honest about what this page really is: a monument to decision fatigue and midnight impulse purchases. Half these tools will be obsolete in two years. The other half I'll replace because someone on Hacker News wrote a convincing blog post at exactly the wrong time (when I'm frustrated with my current setup).

Here's what I've learned after years of tool-hopping and thousands of dollars in "learning experiences":

### The Evolution of My Priorities

**In my early 20s**: "This tool has 47 features!"
**Now**: "This tool has 3 features and they all work reliably."

**Then**: "I need the latest version of everything"
**Now**: "I need the LTS version of everything"

**Then**: "I'll configure this perfectly"
**Now**: "Default settings exist for a reason"

**Then**: "More monitoring = better understanding"
**Now**: "If I can't fix it in 10 minutes at 2 AM, it's too complex"

### The Hard Truths

- **The 80/20 rule is real**: I use 20% of these tools 80% of the time. The rest are for specific situations that happen twice a year.
- **Simple usually wins**: Every time I've replaced a simple tool with a "more powerful" one, I've eventually gone back.
- **The grass isn't greener**: It's just different grass with different bugs and a steeper learning curve.
- **Money doesn't solve problems**: But it does create new, more expensive ones with better documentation.
- **Perfect is the enemy of done**: I've spent more hours optimizing my setup than actually using it productively.

### The Personal Journey

This setup represents about 8 years of evolution, mistakes, and learning. Each tool has a story – usually involving something breaking at the worst possible time and me scrambling to find a solution at 3 AM.

The homelab started as "I should learn enterprise technologies." It became "I want to understand how this stuff really works." Now it's mostly "This is my creative outlet and I enjoy building things."

Some nights I'm troubleshooting a Docker networking issue until 2 AM, cursing every decision that led me here. Other nights I'm setting up a new service in 10 minutes because I finally understand the patterns. Both experiences taught me something.

But you know what? This ridiculous setup – overpriced, overcomplicated, and absolutely overkill – makes me happy. It lets me learn, experiment, break things (in my own environment), and yes, occasionally feel like I actually know what I'm doing.

**The real secret nobody tells you?** Everyone's infrastructure is held together with bash scripts, cron jobs, and hope. The difference between enterprise and homelab isn't the technology – it's the budget for redundancy and the number of people to call when things break.

Mine just has RGB lighting and runs in a closet instead of a datacenter.

*Got questions about any of these tools? Want to argue about why your setup is better? Found a typo that's been bothering you? [Hit me up!](/about/#contact) I promise to defend my choices with completely objective and not-at-all-emotional arguments.*

</div>