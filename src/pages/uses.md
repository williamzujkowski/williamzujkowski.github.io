---

title: "Uses"
layout: page
permalink: /uses/
description: "Hardware, software, and services I use."
eleventyNavigation:
key: Uses
order: 6
--------

# Uses

This page lists the **hardware, software, and services** I personally use for security engineering, development, homelab experiments, and AI projects. It is intended as a living reference: tools and preferences evolve as I learn and refine my workflow.

---

## 🖥️ Hardware

### Workstation

* **Desktop PC** — Intel i9‑9900K, 64 GB RAM, [RTX 3090](https://www.nvidia.com/en-us/geforce/graphics-cards/30-series/rtx-3090/), NVMe storage + large HDDs. Used for virtualization, local LLM experiments, and gaming.
* **Laptop** — [Framework Laptop](https://frame.work/) with [Ubuntu 24.04 LTS](https://ubuntu.com/). Repairable, modular, lightweight.
* **Displays** — 34" ultrawide 4K for multi‑pane editing and monitoring.

### Peripherals

* **Keyboard** — [Wooting 80HE](https://wooting.io/wooting-80he)
* **Mouse** — [Glorious Model O](https://www.gloriousgaming.com/collections/model-o-mice)
* **Headset** — [SteelSeries Arctis 7X+](https://steelseries.com/gaming-headsets/arctis-7)
* **Coffee** — [Chemex 10‑cup](https://chemexcoffeemaker.com/products/ten-cup-classic-chemex)

### Homelab Infrastructure

* **Firewall** — [Ubiquiti Dream Machine Pro](https://ui.com/consoles/dream-machine-pro) with VLAN segmentation.
* **Hypervisor** — Dell R940 running [Proxmox](https://www.proxmox.com/).
* **Cluster Nodes** — 3× Raspberry Pi 5 (16 GB) for [K3s](https://k3s.io/)/ARM testing; [Pi‑hole](https://pi-hole.net/) on Pi 4.
* **Storage** — [TrueNAS](https://www.truenas.com/) (~40 TB raw) for backups and media.
* **Networking** — [Ubiquiti](https://ui.com/) switches/APs for wired and wireless lab segments.

**Related posts:**

* Implementing DNS-over-HTTPS (DoH) for Home Networks → [/posts/implementing-dns-over-https-doh-for-home-networks/](/posts/implementing-dns-over-https-doh-for-home-networks/)
* IoT Security in Your Home Lab: Lessons from OWASP IoTGoat → [/posts/iot-security-in-your-home-lab-lessons-from-owasp-iotgoat/](/posts/iot-security-in-your-home-lab-lessons-from-owasp-iotgoat/)

---

## 🧰 Software & Development

### Operating Systems & Virtualization

* [Ubuntu 24.04 LTS](https://ubuntu.com/) as primary OS.
* [Proxmox](https://www.proxmox.com/) for virtualization.
* [Docker](https://www.docker.com/) / [Podman](https://podman.io/) for containers.
* [K3s](https://k3s.io/) for lightweight Kubernetes.

### Terminal & Editor

* [Ghostty](https://github.com/ghostty-org/ghostty) terminal
* [Zsh](https://www.zsh.org/) shell + plugins
* [tmux](https://github.com/tmux/tmux) multiplexer
* [VS Code](https://code.visualstudio.com/) with extensions for Python, Go, Terraform, Docker
* [Tokyo Night theme](https://github.com/enkia/tokyo-night-vscode-theme)

---

## 🔐 Security & Monitoring (Homelab)

* [Wireshark](https://www.wireshark.org/), tcpdump, [nmap](https://nmap.org/) for network inspection.
* [Nessus](https://www.tenable.com/products/nessus) for vulnerability assessment.
* [Grype](https://github.com/anchore/grype) and [OSV-Scanner](https://github.com/google/osv-scanner) for supply chain scanning.
* [Wazuh](https://wazuh.com/) for log analysis and detection.
* [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/), [Netdata](https://www.netdata.cloud/) for metrics and dashboards.
* [OWASP ZAP](https://www.zaproxy.org/) and [gobuster](https://github.com/OJ/gobuster) for web/app testing.
* [Bitwarden](https://bitwarden.com/) (self‑hosted) for password management.
* [YubiKey 5C NFC](https://www.yubico.com/products/yubikey-5c-nfc/) for hardware 2FA.
* [HashiCorp Vault](https://www.vaultproject.io/) for secrets in automation and CI.

**Related posts:**

* Building a Smart Vulnerability Prioritization System with EPSS and CISA KEV → [/posts/building-a-smart-vulnerability-prioritization-system-with-epss-and-cisa-kev/](/posts/building-a-smart-vulnerability-prioritization-system-with-epss-and-cisa-kev/)
* Vulnerability Management at Scale with Open Source Tools → [/posts/vulnerability-management-at-scale-with-open-source-tools/](/posts/vulnerability-management-at-scale-with-open-source-tools/)
* Building Your Own MITRE ATT&CK Threat Intelligence Dashboard → [/posts/building-your-own-mitre-attck-threat-intelligence-dashboard/](/posts/building-your-own-mitre-attck-threat-intelligence-dashboard/)
* eBPF for Security Monitoring: A Practical Guide → [/posts/ebpf-for-security-monitoring-a-practical-guide/](/posts/ebpf-for-security-monitoring-a-practical-guide/)

---

## 🤖 AI & Prompting

* Local LLMs on RTX 3090.
* [Ollama](https://ollama.com/) for open‑source models.
* Use cases: code review, agent experiments, security automation.

**Related posts:**

* Supercharging Development with Claude-Flow → [/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/](/posts/supercharging-development-with-claude-flow-ai-swarm-intelligence-for-modern-engineering/)
* Down the MCP Rabbit Hole: Building a Standards Server → [/posts/down-the-mcp-rabbit-hole-building-a-standards-server/](/posts/down-the-mcp-rabbit-hole-building-a-standards-server/)
* Exploring Claude CLI Context and Compliance → [/posts/exploring-claude-cli-context-and-compliance-with-my-standards-repository/](/posts/exploring-claude-cli-context-and-compliance-with-my-standards-repository/)
* AI as Cognitive Infrastructure → [/posts/ai-as-cognitive-infrastructure-the-invisible-architecture-reshaping-human-thought/](/posts/ai-as-cognitive-infrastructure-the-invisible-architecture-reshaping-human-thought/)

---

## ☁️ Services

* Code Hosting: GitHub (public), [GitLab CE](https://about.gitlab.com/install/) (private).
* CI/CD: GitHub Actions, [Jenkins](https://www.jenkins.io/) for lab automation.
* Monitoring: [UptimeRobot](https://uptimerobot.com/).
* VPN: [WireGuard](https://www.wireguard.com/), [Tailscale](https://tailscale.com/), [ProtonVPN](https://protonvpn.com/).
* DNS: [Cloudflare 1.1.1.1](https://1.1.1.1/), [Pi-hole](https://pi-hole.net/) local filtering.

---

## 🗂️ Self‑Hosted Services

* [Wazuh](https://wazuh.com/), [Grafana](https://grafana.com/), [Prometheus](https://prometheus.io/), [Netdata](https://www.netdata.cloud/)
* [Jellyfin](https://jellyfin.org/) media server
* [Home Assistant](https://www.home-assistant.io/) automation
* [BookStack](https://www.bookstackapp.com/) documentation/wiki
* [GitLab CE](https://about.gitlab.com/install/) private repos
* [restic](https://restic.net/) backups → [Backblaze B2](https://www.backblaze.com/b2/cloud-storage.html)

---

## 🧪 CLI Tools

```bash
# Development
[git](https://git-scm.com/)        # Version control
[gh](https://cli.github.com/)      # GitHub CLI
[python3](https://www.python.org/) # Scripting & automation
[go](https://go.dev/)              # Systems programming
[rust](https://www.rust-lang.org/) # Memory‑safe development

# Infrastructure
[terraform](https://www.terraform.io/)  # IaC
[ansible](https://www.ansible.com/)     # Configuration management
[docker](https://www.docker.com/)       # Containers
[kubectl](https://kubernetes.io/docs/reference/kubectl/) # Kubernetes
[k3s](https://k3s.io/)                  # Lightweight Kubernetes

# Utilities
[tmux](https://github.com/tmux/tmux)    # Multiplexer
[fzf](https://github.com/junegunn/fzf)  # Fuzzy finder
[ripgrep](https://github.com/BurntSushi/ripgrep) # Code search
[bat](https://github.com/sharkdp/bat)   # Syntax‑highlighted cat
[htop](https://htop.dev/)               # Process monitor
[ncdu](https://dev.yorhel.nl/ncdu)      # Disk usage
```

---

## 📚 Learning

* Platforms: Pluralsight, O’Reilly, YouTube.
* Security labs: HackTheBox, TryHackMe, personal homelab.
* Threat intel: AlienVault OTX, abuse.ch feeds.

---

## 🧭 Principles

1. **Open Source First** — transparent, inspectable tools.
2. **Privacy & Safety** — minimize data exhaust; enforce 2FA.
3. **Automate Boring Things** — script repeatable tasks.
4. **Document As You Go** — wikis > memory.
5. **Reliability > Novelty** — boring tech for critical paths.

---

*Last updated: 2025-10-03*
