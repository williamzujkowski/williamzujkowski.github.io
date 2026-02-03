---
title: "Uses"
layout: page
permalink: /uses/
description: "Hardware, software, and services I use."
eleventyNavigation:
  key: Uses
  order: 6
---

# Uses

This is my digital toolbox – the stuff that's survived the test of real-world use and hasn't let me down. I'm picky about my tools because bad choices cost time, and time is what I use to tinker with cool stuff. Everything here has a story, usually involving at least one failure before I figured it out.

What started with a $50 Raspberry Pi in 2015 has evolved into a ~$12,000 homelab and workflow that actually works for me. This is a living document: I update it when I change something significant or learn a better way.

---

## 🖥️ Hardware

### Workstation

* **Desktop PC** — Intel i9-9900K (2019), 64 GB RAM, [RTX 3090](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090/) (2021), 1TB NVMe + 8TB HDD storage

  **Why this build:** Needed something that could handle local LLM experiments (hence the 3090's 24GB VRAM) plus VM workloads (hence the 64GB RAM). Built in 2019 for ~$2,400, upgraded GPU in 2021 when I realized 11GB VRAM on my old 2080 Ti limited me to 7B models. The 3090's 24GB handles 7B-34B models comfortably in full VRAM.

  **Trade-off:** Could've gone AMD Threadripper for better multi-threading, but CUDA support for ML work made NVIDIA the obvious choice. The 3090 was expensive ($1,500 during the shortage), but it saves me hundreds per month in cloud GPU costs.

  **Failure story:** Originally bought a 2080 Ti in 2020. Fried it overclocking to squeeze 15% more performance for LLM inference. Learned my lesson about pushing hardware past its limits. RIP $1,200.

* **Laptop** — [Framework Laptop](https://frame.work/) (DIY Edition, 2022) with [Ubuntu 24.04 LTS](https://ubuntu.com/)

  **Why Framework:** After three laptops that became e-waste because one component failed, I wanted something actually repairable. Framework's modular design means I can upgrade RAM, storage, ports, even the mainboard without replacing the whole machine.

  **Cost reality:** $1,400 for the DIY edition with an i7-1260P, 32GB RAM, and 1TB NVMe. More expensive than a Dell with similar specs, but I value the right-to-repair philosophy.

  **Ubuntu choice:** Tried Fedora for six months, kept breaking after updates. Ubuntu LTS is boring, which is exactly what I want on a laptop I depend on.

* **Displays** — 34" LG 34WK95U ultrawide (3440x1440, ~$800)

  **Why ultrawide:** Tried dual 27" monitors for years. The bezel gap drove me insane. One seamless ultrawide lets me have three vertical code panes side-by-side without visual interruption. Game changer for monitoring dashboards.

### Peripherals

* **Keyboard** — [Wooting 80HE](https://wooting.io/wooting-80he) (~$185)

  **Analog hall effect keys:** Thought it was marketing hype until I tried it. The ability to set actuation points per-key and have analog input changed how I interact with my machine. It's absurdly customizable. Now I can't go back to traditional mechanical switches.

* **Mouse** — [Glorious Model O](https://www.gloriousgaming.com/collections/model-o-mice) (~$50)

  **Lightweight champion:** 67 grams. After years of heavy gaming mice giving me wrist pain, going ultralight was a revelation. Simple, reliable, cheap.

* **Headset** — [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7) (~$150)

  **Wireless that actually works:** Battery lasts 30+ hours, comfortable for all-day wear, and the mic doesn't sound like I'm in a cave. Works seamlessly across my PC, Xbox, and Switch.

* **Coffee** — [Chemex 10-cup](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex) (~$50) + [Baratza Encore grinder](https://baratza.com/grinder/encore/) (~$170)

  **Because good security engineering requires good coffee.** This is non-negotiable. Chemex makes clean, smooth coffee without the bitterness you get from French press. The ritual of manual pour-over also gives me time to think through problems.

### Homelab Infrastructure

**The Journey:** Started with a $50 Raspberry Pi 4 in 2015. Thought "this is all I need." Ten years and ~$8,000 in equipment later, here we are.

* **Firewall** — [Ubiquiti Dream Machine Pro](https://ui.com/consoles/dream-machine-pro) (~$380)

  **Why UDM Pro:** Spent years with pfSense on repurposed hardware. Worked great until it didn't. UDM Pro isn't as flexible, but it's stable, fast, and I don't have to maintain another box. Trade-off accepted.

  **What I actually use:** VLAN segmentation (IoT devices on isolated network), IDS/IPS for threat detection, DPI for traffic analysis. Handles gigabit routing without breaking a sweat.

* **Hypervisor** — Dell R940 running [Proxmox](https://www.proxmox.com/) (~$3,500 used, 2022)

  **Why enterprise gear:** Needed serious compute for VM testing. Considered building custom, but used enterprise hardware is cheap if you can handle the noise. This thing sounds like a jet engine at full throttle. Worth it.

  **Specs:** 4x Intel Xeon Gold 6130 (64 cores / 128 threads total), 768GB RAM, 8TB NVMe + 12TB HDD storage.

  **What I run:** ~30 VMs for testing, ~15 LXC containers for services. Proxmox because it's free, well-documented, and I understand it. Tried ESXi for three months in 2020, licensing made me cry.

  **Power cost:** ~$150/month at idle. Expensive hobby, but cheaper than renting equivalent cloud resources for learning.

* **Cluster Nodes** — 3x [Raspberry Pi 5](https://www.raspberrypi.com/products/raspberry-pi-5/) (16GB, ~$80 each) + 1x [Raspberry Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) (8GB, 2020)

  **K3s testing cluster:** Learning Kubernetes on real hardware beats reading docs. The Pi 5s run a lightweight K3s cluster for ARM testing. It's slow, but that's the point – if it works here, it'll work anywhere.

  **Pi-hole on the Pi 4:** Network-wide ad blocking. Set-and-forget for five years running. Blocks ~25% of DNS queries before they hit the network.

* **Storage** — [TrueNAS Core](https://www.truenas.com/) (~$1,200 for custom build, 2020)

  **~40TB raw, ~30TB usable** (RAIDZ2 configuration)

  **Why TrueNAS:** ZFS is bulletproof. I've had drives fail, but never lost data. Snapshots saved me twice when I accidentally deleted things I shouldn't have. Once from a bad script, once from fat-fingering an rm command.

  **Backup strategy:** Critical data goes to [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html) (~$50/month) via [restic](https://restic.net/). Follows the 3-2-1 rule: 3 copies, 2 different media, 1 offsite.

* **Networking** — [Ubiquiti](https://ui.com/) UniFi Switch 24 PoE (~$380) + 2x U6 Pro APs (~$150 each)

  **Why Ubiquiti ecosystem:** Centralized management, reliable, PoE for clean AP installation. Not the cheapest, not the most feature-rich, but it just works. I've had zero downtime in three years.

  **Network design:** 5 VLANs (Management, Home, Lab, IoT, Guest). IoT devices can't reach anything else. Learned this lesson after a smart bulb tried to phone home to China 47,000 times in one day.

**Related posts:**

* [Implementing DNS-over-HTTPS (DoH) for Home Networks](/posts/implementing-dns-over-https-doh-for-home-networks/)
* [IoT Security in Your Home Lab: Lessons from OWASP IoTGoat](/posts/iot-security-in-your-home-lab-lessons-from-owasp-iotgoat/)

---

## 🧰 Software & Development

### Operating Systems & Virtualization

* [Ubuntu 24.04 LTS](https://ubuntu.com/) as primary OS

  **Boring and stable:** After distro-hopping for years (Arch, Fedora, NixOS, Pop!_OS), I settled on Ubuntu LTS. It's boring. Boring is good. I spend my time solving problems, not fixing my OS.

  **What I learned:** The "best" distro is the one that doesn't make you think about it.

* [Proxmox](https://www.proxmox.com/) for virtualization

  **Proxmox vs ESXi:** VMware's licensing changes in 2024 validated my 2022 choice. Proxmox is open-source, has a great community, and doesn't lock me into vendor licensing. I've been running it for three years without major issues.

  **Learning curve:** Took about 2 weeks to get comfortable. Worth it.

* [Docker](https://www.docker.com/) / [Podman](https://podman.io/) for containers

  **Docker for development, Podman for production:** Docker is ubiquitous and has better docs. Podman is daemonless and more secure. I use both depending on context.

  **Container philosophy:** If a service isn't in a container, it's doing it wrong. Makes deployment reproducible and rollbacks trivial.

* [K3s](https://k3s.io/) for lightweight Kubernetes

  **Learning K8s the hard way:** Tried learning full Kubernetes in 2021. Overwhelmed. K3s is stripped-down, easier to understand, perfect for homelab. Once you understand K3s, regular K8s makes sense.

  **Reality check:** K8s is overkill for 90% of homelab use cases. I use it because I want to learn it, not because I need it.

### Terminal & Editor

* [Ghostty](https://github.com/ghostty-org/ghostty) terminal

  **Recent switch:** Moved from Alacritty in October 2024. Ghostty is stupid fast (GPU-accelerated), uses less memory, and the developer is responsive. Still in beta but already more stable than some "production" terminals I've used.

  **Why not GNOME Terminal:** Startup time. Ghostty launches in ~40ms vs ~400ms for GNOME Terminal. When you open dozens of terminals daily, that adds up.

* [Zsh](https://www.zsh.org/) shell + [oh-my-zsh](https://ohmyz.sh/) + plugins

  **Why not bash:** Tab completion and git integration. My most-used plugins: `git`, `docker`, `kubectl`, `z` (directory jumping), `fzf` integration.

  **Tried fish:** Great shell, but bash compatibility matters for scripts I copy from Stack Overflow. Zsh gives me better UX while staying bash-compatible.

* [tmux](https://github.com/tmux/tmux) multiplexer

  **Essential for remote work:** SSH sessions that survive disconnects. I can start a long-running task, disconnect, reconnect hours later, and it's still running. Game changer.

  **Learning curve:** Steep. Took me 3 months to stop fighting it. Now it's muscle memory. Worth the investment.

* [VS Code](https://code.visualstudio.com/) with extensions for Python, Go, Terraform, Docker

  **Controversial take:** I know, "real developers use vim." I tried. For 3 months in 2019. I was 30% slower in vim. Life's too short. VS Code with vim keybindings is my compromise.

  **Essential extensions:** Python (Microsoft), Docker, GitLens, Remote-SSH, Markdown All-in-One, Trailing Spaces.

  **Remote-SSH is magic:** Edit files on remote machines like they're local. No more nano/vi in SSH sessions.

* [Tokyo Night theme](https://github.com/enkia/tokyo-night-vscode-theme)

  **Eye comfort:** After years of high-contrast themes giving me headaches, Tokyo Night's softer palette is easier on my eyes during long coding sessions. Small quality-of-life improvement that matters.

---

## 🔐 Security & Monitoring (Homelab)

* [Wireshark](https://www.wireshark.org/), tcpdump, [nmap](https://nmap.org/) for network inspection

  **The classics:** These tools have been around forever because they work. Wireshark for deep packet inspection, tcpdump for quick captures, nmap for discovery. I use them weekly.

  **Learning investment:** Spent ~40 hours over a year learning Wireshark filters. Now I can find issues in minutes that used to take hours.

* [Nessus](https://www.tenable.com/products/nessus) for vulnerability assessment

  **Using:** Nessus Essentials (free version, up to 16 IPs). Tried OpenVAS for a year in 2020—spent more time fixing false positives than finding vulns. Nessus just works.

  **Trade-off:** Free version is limited to 16 hosts, but that covers my critical infrastructure. For a full homelab scan, I rotate scans across subnets or use Grype/OSV for container/package scanning.

  **What I scan:** Everything. Monthly full scans of all homelab assets. Found critical vulns in IoT devices that vendors never patched.

* [Grype](https://github.com/anchore/grype) and [OSV-Scanner](https://github.com/google/osv-scanner) for supply chain scanning

  **Free alternatives:** For container/code scanning, these are excellent. I also use [Trivy](https://github.com/aquasecurity/trivy). Run all three because overlapping coverage catches more issues.

  **Discovery:** Found a critical vuln in a homelab container with Grype that Nessus missed. Now I always run multiple scanners.

* [Wazuh](https://wazuh.com/) for log analysis and detection

  **Open-source SIEM:** Wazuh aggregates logs from everything and correlates events. Detected a brute-force SSH attack in real-time in 2023. Would've missed it without centralized logging.

  **Setup time:** ~8 hours to configure properly. Worth every minute. Now I have visibility into everything happening on my network.

* [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/), [Netdata](https://www.netdata.cloud/) for metrics and dashboards

  **Observability stack:** Prometheus scrapes metrics, Grafana visualizes them, Netdata gives real-time insights. I have dashboards for everything: server health, network traffic, container metrics, power consumption.

  **Prevented issues:** Caught a failing disk before data loss, identified a memory leak in a service, spotted unusual traffic patterns.

* [OWASP ZAP](https://www.zaproxy.org/) and [gobuster](https://github.com/OJ/gobuster) for web/app testing

  **Pentesting tools:** ZAP for automated web app scanning, gobuster for directory/subdomain discovery. Use these for testing anything web-facing before exposing it to the internet.

* [Bitwarden](https://bitwarden.com/) (self-hosted) for password management

  **Why self-hosted:** I trust Bitwarden's security model, but I prefer controlling the infrastructure. Running [Vaultwarden](https://github.com/dani-garcia/vaultwarden) (lightweight Bitwarden server) on my homelab since 2021.

  **Migration:** Moved from LastPass after their 2021 breach. Haven't looked back.

* [YubiKey 5C NFC](https://www.yubico.com/products/yubikey-5c-nfc/) for hardware 2FA (~$55)

  **Physical security keys:** I use YubiKeys for every account that supports FIDO2/WebAuthn. Phishing-resistant 2FA is non-negotiable.

  **Rule:** If a service doesn't support 2FA in 2025, it doesn't get my data. Full stop.

* [HashiCorp Vault](https://www.vaultproject.io/) for secrets in automation and CI

  **Secrets management:** Hardcoded secrets are evil. Vault centralizes secret storage and provides audit logs of who accessed what when.

  **Learning curve:** Steep. Took me two weeks to grok the concepts. Absolutely worth it for automated workflows.

**Related posts:**

* [Building a Smart Vulnerability Prioritization System with EPSS and CISA KEV](/posts/building-a-smart-vulnerability-prioritization-system-with-epss-and-cisa-kev/)
* [Vulnerability Management at Scale with Open Source Tools](/posts/vulnerability-management-at-scale-with-open-source-tools/)
* [Building Your Own MITRE ATT&CK Threat Intelligence Dashboard](/posts/building-your-own-mitre-attck-threat-intelligence-dashboard/)
* [eBPF for Security Monitoring: A Practical Guide](/posts/ebpf-for-security-monitoring-a-practical-guide/)

---

## 🤖 AI & Prompting

* **Local LLMs on RTX 3090** (24GB VRAM)

  **Models that actually fit:** Llama 3.1 8B (~4GB Q4), Mistral 7B (~4GB Q4), CodeLlama 34B (~20GB Q4), Qwen 2.5 Coder 32B (~18GB Q4).

  **Why local:** Privacy, unlimited usage, learning how they work under the hood. For security research and analyzing potentially sensitive data, local inference is the only acceptable option.

  **Hardware reality:** 24GB VRAM handles 7B-34B models fully in GPU memory with Q4 quantization. Larger models (70B+) require CPU offloading (storing part of model in system RAM), which drops performance from 20+ tokens/second to 2-5 tokens/second. For 70B tasks, I use API access or accept the slower offloaded inference.

  **Performance sweet spot:** CodeLlama 34B at Q4 quantization (~20GB) gives excellent quality at 12-15 tokens/second. 8B models hit 40+ tokens/second. Good enough for 90% of my use cases.

* [Ollama](https://ollama.com/) for model management

  **Game changer:** Makes running local LLMs actually usable. Tried llama.cpp directly – too much friction. Ollama is Docker-simple.

  **Install to running LLM in 2 commands:**
  ```bash
  curl https://ollama.ai/install.sh | sh
  ollama run llama3.1:8b  # Or codellama:34b for larger models
  ```

* **Use cases that actually work:**
  - **Code review:** Catches obvious bugs, suggests improvements. Not perfect, but faster than waiting for human review.
  - **Security policy analysis:** Summarizing 50-page compliance docs into actionable items.
  - **Homelab troubleshooting:** Explains obscure error messages better than Google sometimes.
  - **Learning new tech:** Asks better questions than docs sometimes. Great for "explain like I'm five" moments.
  - **Blog post editing:** Catches typos and awkward phrasing I miss.

* **Use cases that don't work:**
  - Anything requiring real-time data (models are frozen in time).
  - Complex multi-step reasoning (hallucinations increase with complexity).
  - Critical decisions where hallucinations matter (always verify).
  - Code generation for complex systems (good for boilerplate, bad for architecture).

* **Reality check:** LLMs are tools, not magic. They're autocomplete on steroids. Useful when you understand their limitations, dangerous when you don't.

**Related posts:**

* [Supercharging Development with Claude-Flow](/posts/2025-08-07-supercharging-development-claude-flow/)
* [Down the MCP Rabbit Hole: Building a Standards Server](/posts/down-the-mcp-rabbit-hole-building-a-standards-server/)
* [Exploring Claude CLI Context and Compliance](/posts/exploring-claude-cli-context-and-compliance-with-my-standards-repository/)
* [AI as Cognitive Infrastructure](/posts/ai-as-cognitive-infrastructure-the-invisible-architecture-reshaping-human-thought/)

---

## ☁️ Services

* **Code Hosting:** GitHub (public), [GitLab CE](https://about.gitlab.com/install/) (self-hosted private)

  **Why both:** GitHub for open-source visibility, GitLab for private repos I don't want in someone else's cloud. GitLab CE is free and feature-complete.

* **CI/CD:** GitHub Actions (public), [Jenkins](https://www.jenkins.io/) (homelab automation)

  **GitHub Actions:** Free for public repos, simple YAML config, integrates perfectly with GitHub. Handles my blog deployment.

  **Jenkins:** Overkill for most things, but I use it for homelab automation that GitHub Actions can't reach. Runs backup jobs, system updates, monitoring checks.

* **Monitoring:** [UptimeRobot](https://uptimerobot.com/) (free tier)

  **External health checks:** Monitors my public-facing services from outside my network. Notifies me via email/SMS if something goes down. Free tier is generous (50 monitors, 5-minute intervals).

* **VPN:** [WireGuard](https://www.wireguard.com/), [Tailscale](https://tailscale.com/), [ProtonVPN](https://protonvpn.com/)

  **WireGuard for homelab access:** Fast, modern, secure. Self-hosted on my UDM Pro. Connect to my homelab from anywhere.

  **Tailscale for mesh networking:** Zero-config VPN that just works. Free for personal use (up to 20 devices). Magic.

  **ProtonVPN for privacy:** When I need to hide my traffic from my ISP or access region-locked content. Swiss privacy laws, no logs, trustworthy.

* **DNS:** [Cloudflare 1.1.1.1](https://1.1.1.1/) upstream, [Pi-hole](https://pi-hole.net/) local filtering

  **Layered approach:** Pi-hole blocks ads/tracking at the DNS level (25% of queries), Cloudflare DNS for privacy (faster than ISP DNS, no logging).

  **Why not Google DNS:** I don't need Google knowing every domain I visit.

---

## 🗂️ Self-Hosted Services

Running these on Proxmox VMs/containers because I control my data:

* [Wazuh](https://wazuh.com/), [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/), [Netdata](https://www.netdata.cloud/) — Security + monitoring stack
* [Jellyfin](https://jellyfin.org/) — Media server (FOSS alternative to Plex, no tracking)
* [Home Assistant](https://www.home-assistant.io/) — Home automation (controls lights, sensors, cameras)
* [BookStack](https://www.bookstackapp.com/) — Documentation/wiki (beautiful, markdown-based, easy to use)
* [GitLab CE](https://about.gitlab.com/install/) — Private git repos
* [restic](https://restic.net/) backups → [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html) — Encrypted offsite backups

**Why self-host:** Privacy, learning, control. Also, it's fun. I've learned more about networking, security, and system administration from running these services than from any course.

**Cost:** ~$50/month for Backblaze B2, ~$150/month for power. Compared to equivalent SaaS subscriptions (~$300/month), I'm break-even while learning and owning my data.

---

## 🧪 CLI Tools

### Development
* [git](https://git-scm.com/) — Version control (use it hourly)
* [gh](https://cli.github.com/) — GitHub CLI (faster than web UI for PRs/issues)
* [python3](https://www.python.org/) — Scripting & automation (80% of my scripts)
* [go](https://go.dev/) — Systems programming (learning, not expert)
* [rust](https://www.rust-lang.org/) — Memory-safe development (aspirational, still learning)

### Infrastructure
* [terraform](https://www.terraform.io/) — IaC (declarative infrastructure, version-controlled)
* [ansible](https://www.ansible.com/) — Configuration management (automate everything)
* [docker](https://www.docker.com/) — Containers (daily driver)
* [kubectl](https://kubernetes.io/docs/reference/kubectl/) — Kubernetes (learning)
* [k3s](https://k3s.io/) — Lightweight Kubernetes (actually using)

### Utilities That Changed My Workflow
* [tmux](https://github.com/tmux/tmux) — Multiplexer (can't work without it)
* [fzf](https://github.com/junegunn/fzf) — Fuzzy finder (instant file/history search)
* [ripgrep](https://github.com/BurntSushi/ripgrep) — Code search (10x faster than grep)
* [bat](https://github.com/sharkdp/bat) — Syntax-highlighted cat (small QoL improvement)
* [htop](https://htop.dev/) — Process monitor (better than top)
* [ncdu](https://dev.yorhel.nl/ncdu) — Disk usage (find space hogs instantly)

**Pattern:** I gradually replace standard tools with modern alternatives when they significantly improve my workflow. Not change for change's sake, but real productivity gains.

---

## 📚 Learning

* **Platforms:** [Pluralsight](https://www.pluralsight.com/) ($299/year), [O'Reilly](https://www.oreilly.com/) ($499/year), YouTube (free)

  **ROI:** These subscriptions pay for themselves if I learn one skill that saves 10 hours. They've saved me hundreds of hours.

  **YouTube underrated:** Free, high-quality content. I've learned more from [NetworkChuck](https://www.youtube.com/@NetworkChuck), [LiveOverflow](https://www.youtube.com/@LiveOverflow), and [IppSec](https://www.youtube.com/@ippsec) than from some paid courses.

* **Security labs:** [HackTheBox](https://www.hackthebox.com/) (~$150/year), [TryHackMe](https://tryhackme.com/) (~$100/year), personal homelab (priceless)

  **Hands-on learning:** Reading about security is fine. Breaking things is better. These platforms provide safe, legal environments to practice offensive security.

  **Homelab advantage:** I can test things these platforms don't cover. My lab, my rules.

* **Threat intel:** [AlienVault OTX](https://otx.alienvault.com/), [abuse.ch feeds](https://abuse.ch/), [CISA KEV](https://www.cisa.gov/known-exploited-vulnerabilities)

  **Free threat intelligence:** These feeds tell me what bad actors are exploiting right now. I integrate them into Wazuh for automated detection.

---

## 🧭 Principles

1. **Open Source First** — Transparent, inspectable tools

   **Learned this the hard way:** Vendor locked me out of my own monitoring data in 2018. Never again. Open source means I control my data and can fix it myself if needed.

   **Exception:** I'll use proprietary tools when they're significantly better (Nessus) or when no viable FOSS alternative exists. Pragmatism over ideology.

2. **Privacy & Safety** — Minimize data exhaust; enforce 2FA everywhere

   **Rule:** If a service doesn't support 2FA in 2025, it doesn't get my data. Full stop. Bitwarden + YubiKey for everything.

   **Data minimization:** Services that don't need my real info get [SimpleLogin](https://simplelogin.io/) aliases and fake data. Compartmentalization reduces blast radius.

3. **Automate Boring Things** — Script repeatable tasks

   **Trigger:** If I do something manually 3 times, it gets automated. Life's too short for repetitive tasks.

   **Examples:** Database backups (automated), certificate renewal (automated), system updates (automated), blog deployment (automated), VM snapshots (automated).

4. **Document As You Go** — Wikis > memory

   **Reality check:** I don't remember why I made a change 3 months ago without notes. Future me always thanks past me for documentation.

   **Tools:** BookStack for procedures, git commit messages for code changes, inline comments for complex logic.

   **Learned:** If I can't explain it to someone else, I don't understand it well enough.

5. **Reliability > Novelty** — Boring tech for critical paths

   **Translation:** New and shiny is fun for labs. Production runs on battle-tested boring tech. Docker, PostgreSQL, nginx, Ubuntu LTS – they work because they've been broken and fixed 1,000 times.

   **Exception:** I break this rule in the homelab constantly. That's what it's for. Break things, learn, iterate. Just don't do it in production.

   **Wisdom:** The best tech stack is the one you understand, not the one on Hacker News.

---

*Last updated: 2025-11-12*
