---
layout: page
title: Homelab & Security Resources
description: The best open source tools, homelab projects, and books that actually taught me something. No fluff, just the good stuff.
permalink: /resources/
eleventyNavigation:
  key: Resources
  title: Resources
  order: 5
image: /assets/images/og/resources-og.png
---

# The Good Stuff: Tools, Toys, and Rabbit Holes

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
The tools that survived my testing, the projects that actually work, and the books that are worth your time.
No vendor pitches, no compliance frameworks – just the open source goodness that makes homelabbing addictive.
</p>

<div class="bg-yellow-50 dark:bg-yellow-900/20 border-l-4 border-yellow-400 p-6 my-8">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🧭 Your Learning Journey Map</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    I've been down this rabbit hole since 2005, and trust me – the path isn't linear. You'll circle back, get distracted by shiny new tools,
    and occasionally question your life choices at 3 AM when Docker won't start (I've done this at least 47 times). That's normal. Here's what I wish someone had told me when I started.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
    <div class="bg-white dark:bg-gray-800 p-3 rounded">
      <strong class="text-green-600 dark:text-green-400">🌱 Start Here</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Docker, basic monitoring, and one programming language. Don't try to learn everything at once.</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded">
      <strong class="text-blue-600 dark:text-blue-400">🚀 Build Momentum</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Add orchestration, monitoring, and start breaking things intentionally. Security mindset begins here.</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded">
      <strong class="text-purple-600 dark:text-purple-400">🔬 Go Deep</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Specialize in what interests you. Red team, blue team, DevOps, or just really cool home automation.</p>
    </div>
  </div>
</div>

## 🚀 Hot Right Now: Tools I'm Excited About

These are the tools that have me staying up way too late "just testing one more thing."

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/slimtoolkit/slim" class="text-primary-600 dark:text-primary-400 hover:underline">Slim.AI</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Container minification that actually works. Turned my 1.2GB containers into 43MB. Black magic.
    </p>
    <div class="text-sm text-gray-600 dark:text-gray-500 space-y-1">
      <p><strong>When I discovered it:</strong> October 2024</p>
      <p><strong>Version tested:</strong> v1.40.8</p>
      <p><strong>Real measurement:</strong> Reduced my Python app from 1.2GB → 43MB (96% reduction)</p>
      <p><strong>Timeline:</strong> Found this after spending 3 weeks manually optimizing Dockerfiles. Could've saved myself 20+ hours.</p>
      <p><strong>Why I love it:</strong> Smaller attack surface + faster deploys = happy me</p>
      <p><strong>Gotcha:</strong> Sometimes breaks dynamic code loading. Test thoroughly before production.</p>
    </div>
  </div>

  <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/tailscale/tailscale" class="text-primary-600 dark:text-primary-400 hover:underline">Tailscale</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      WireGuard VPN that just works. No port forwarding, no crying.
    </p>
    <div class="text-sm text-gray-600 dark:text-gray-500 space-y-1">
      <p><strong>Adoption date:</strong> March 2024</p>
      <p><strong>Setup time:</strong> Literally 2 minutes 23 seconds (I timed it because I didn't believe it)</p>
      <p><strong>Before/after:</strong> Spent 4 weekends in 2023 fighting OpenVPN configs. Now VPN "just works."</p>
      <p><strong>Why I love it:</strong> Connected my homelab to my phone in under 3 minutes. TWO COMMANDS.</p>
      <p><strong>Pro tip:</strong> Start with the free tier (up to 3 users, 100 devices), then upgrade when you inevitably add every device you own.</p>
    </div>
  </div>

  <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/crowdsecurity/crowdsec" class="text-primary-600 dark:text-primary-400 hover:underline">CrowdSec</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Collaborative IPS that actually learns from attacks. Like fail2ban grew a brain.
    </p>
    <div class="text-sm text-gray-600 dark:text-gray-500 space-y-1">
      <p><strong>Discovery:</strong> August 2024 during weekend security audit</p>
      <p><strong>First blocked attack:</strong> 47 minutes after installation (WordPress brute force from 185.220.xxx.xxx)</p>
      <p><strong>Current stats:</strong> Blocking ~200 IPs/day, 95%+ from community intel</p>
      <p><strong>Why I love it:</strong> Community-powered threat intel that actually works. Like having 50,000+ security teams watching your back.</p>
      <p><strong>Learning curve:</strong> Start with default scenarios (takes ~15 minutes), then customize. The community hub is gold.</p>
    </div>
  </div>

  <div class="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/netdata/netdata" class="text-primary-600 dark:text-primary-400 hover:underline">Netdata</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Real-time monitoring that doesn't need a PhD to configure. Pretty graphs included.
    </p>
    <div class="text-sm text-gray-600 dark:text-gray-500 space-y-1">
      <p><strong>Found:</strong> July 2024 during memory leak hunt</p>
      <p><strong>Problem solved:</strong> 5 minutes to identify leak that took 3 days to find manually (Python process eating 8GB+)</p>
      <p><strong>Resource usage:</strong> <1% CPU, ~100MB RAM for full monitoring stack</p>
      <p><strong>First impression:</strong> "This can't be this easy." Spoiler: it was. One-line install, zero config needed.</p>
      <p><strong>Warning:</strong> You'll become addicted to watching real-time metrics. Don't say I didn't warn you.</p>
    </div>
  </div>
</div>

## 🏠 Homelab Essentials: The Foundation

<div class="bg-blue-50 dark:bg-blue-950/50 border-l-4 border-blue-400 dark:border-blue-500 p-6 my-6">
  <h4 class="text-lg font-bold text-gray-900 dark:text-white mb-3">📚 Learning Path: From Zero to Hero</h4>
  <p class="text-gray-700 dark:text-gray-200 mb-4">
    Here's the order I'd tackle these if I were starting over. Each tool builds on the last, and you'll use these concepts everywhere.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-sm">
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-green-600 dark:text-green-400">Week 1-2</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Docker basics, simple containers</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-blue-600 dark:text-blue-400">Week 3-4</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Docker Compose, multi-container apps</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-purple-600 dark:text-purple-400">Month 2</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Orchestration (K3s or Nomad)</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-orange-600 dark:text-orange-400">Month 3+</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Infrastructure as Code</p>
    </div>
  </div>
</div>

### Container & Orchestration

<div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg my-6">
  <p class="text-sm text-gray-700 dark:text-gray-300 mb-4 italic">
    <strong>My Journey:</strong> 2017: Started with Docker | 2019: Tried K8s, overwhelmed, gave up | 2021: K3s made Kubernetes click | 2024: Running 30+ containers across 12 K3s nodes
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">🐳 Container Platforms</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-green-400 pl-3">
          <p><a href="https://www.portainer.io/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Portainer</a> - Docker management that doesn't suck</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🌱 <strong>Start here:</strong> Web UI makes Docker approachable. Perfect for beginners who need visual feedback.</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Adoption:</strong> Day 2 of learning Docker (2017). Needed visual feedback to understand what containers were actually doing. Still use it 7 years later for quick operations.</p>
        </div>
        <div class="border-l-2 border-blue-400 pl-3">
          <p><a href="https://k3s.io/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">K3s</a> - Kubernetes for humans (only 40MB!)</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🚀 <strong>My go-to:</strong> All the K8s power, none of the complexity. Runs on a Pi!</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Adoption:</strong> 2021-present | <strong>Version:</strong> v1.28.3+k3s1 | <strong>Why it clicked:</strong> Full K8s in 40MB vs 2GB+ for full K8s. Runs on Raspberry Pi. That simplicity made concepts finally make sense.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p><a href="https://podman.io/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Podman</a> - Docker without the daemon drama</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🔒 <strong>Security win:</strong> Rootless containers out of the box. Steep learning curve though.</p>
        </div>
        <div class="border-l-2 border-orange-400 pl-3">
          <p><a href="https://www.nomadproject.io/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Nomad</a> - Simple orchestration that actually is simple</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">💡 <strong>Hidden gem:</strong> When K8s feels like overkill. Single binary, zero fuss.</p>
        </div>
      </div>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">🔧 Infrastructure as Code</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-green-400 pl-3">
          <p><a href="https://www.ansible.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Ansible</a> - Automate all the things</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🌱 <strong>Start here:</strong> YAML you can actually read. Great for server setup and maintenance.</p>
        </div>
        <div class="border-l-2 border-blue-400 pl-3">
          <p><a href="https://www.terraform.io/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Terraform</a> - For when you want to code your infrastructure</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🚀 <strong>Game changer:</strong> Destroyed and rebuilt my lab 50+ times learning this. Worth every retry.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p><a href="https://www.pulumi.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Pulumi</a> - Terraform but with real programming languages</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">💻 <strong>For devs:</strong> If you prefer Python/TypeScript over HCL. Powerful but opinionated.</p>
        </div>
        <div class="border-l-2 border-orange-400 pl-3">
          <p><a href="https://github.com/hashicorp/packer" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Packer</a> - Golden images done right</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🏗️ <strong>Advanced move:</strong> Standardize your VM builds. Pairs beautifully with Terraform.</p>
        </div>
      </div>
    </div>
  </div>
</div>

### Self-Hosted Services That Don't Suck

<div class="bg-blue-50 dark:bg-blue-950/50 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-white mb-4">🎯 Actually Useful Services</h4>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Monitoring & Logs</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/getsentry/self-hosted" class="text-primary-600 dark:text-primary-400 hover:underline">Sentry</a> - Error tracking</li>
        <li><a href="https://github.com/grafana/loki" class="text-primary-600 dark:text-primary-400 hover:underline">Loki</a> - Log aggregation</li>
        <li><a href="https://uptimekuma.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Uptime Kuma</a> - Status monitoring</li>
        <li><a href="https://healthchecks.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Healthchecks</a> - Cron monitoring</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Dev Tools</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://gitea.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Gitea</a> - Lightweight Git hosting</li>
        <li><a href="https://www.drone.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Drone CI</a> - Container-native CI/CD</li>
        <li><a href="https://www.sonatype.com/products/sonatype-nexus-repository" class="text-primary-600 dark:text-primary-400 hover:underline">Nexus</a> - Artifact repository</li>
        <li><a href="https://verdaccio.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Verdaccio</a> - Private npm registry</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Actually Fun</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.home-assistant.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Home Assistant</a> - Home automation</li>
        <li><a href="https://jellyfin.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Jellyfin</a> - Media server</li>
        <li><a href="https://nextcloud.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Nextcloud</a> - Your own cloud</li>
        <li><a href="https://github.com/paperless-ngx/paperless-ngx" class="text-primary-600 dark:text-primary-400 hover:underline">Paperless-ngx</a> - Document management</li>
      </ul>
    </div>
  </div>
</div>

## 💀 The Graveyard: Tools That Didn't Make the Cut

<div class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-400 p-6 my-8">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🪦 Learn from My Mistakes</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    Not every tool is a winner. Here are some that looked promising but didn't survive contact with reality.
    Learning what doesn't work is just as valuable as finding what does.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-medium text-red-600 dark:text-red-400 mb-2">OpenShift (for homelab)</h5>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        <strong>Tried:</strong> Q2 2022, abandoned after 2 months<br>
        <strong>Cost:</strong> $0 but ~40 hours wasted<br>
        <strong>Why I tried it:</strong> Red Hat magic, enterprise features, impressive demos<br>
        <strong>Why it failed:</strong> Minimum 4 cores + 16GB RAM per node. Ate 64GB of my 128GB total RAM. K3s does 90% for 10% of resources.<br>
        <strong>What I learned:</strong> Enterprise tools don't scale down. Use tools designed for your scale.
      </p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-medium text-red-600 dark:text-red-400 mb-2">Jenkins (for simple CI/CD)</h5>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        <strong>Why I tried it:</strong> Industry standard, huge plugin ecosystem<br>
        <strong>Why it failed:</strong> Configuration nightmare. Spent more time maintaining Jenkins than using it. GitLab CI or Drone CI work better for small projects.
      </p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-medium text-red-600 dark:text-red-400 mb-2">Full ELK Stack (personal use)</h5>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        <strong>Why I tried it:</strong> Industry standard logging<br>
        <strong>Why it failed:</strong> Java memory hog for homelab scale. Loki + Grafana gives 80% of the value with 20% of the complexity.
      </p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-medium text-red-600 dark:text-red-400 mb-2">OSSEC (before Wazuh)</h5>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        <strong>Why I tried it:</strong> Free SIEM solution<br>
        <strong>Why it failed:</strong> Configuration by editing XML files. In 2023. Wazuh is what OSSEC should have become.
      </p>
    </div>
  </div>
  <div class="mt-4 p-3 bg-yellow-100 dark:bg-yellow-900/30 rounded border border-yellow-300 dark:border-yellow-700">
    <p class="text-sm text-yellow-800 dark:text-yellow-200">
      <strong>💡 The pattern:</strong> Complex enterprise tools often don't scale down well to homelab environments.
      Look for tools designed for simplicity first, then scale up if needed.
    </p>
  </div>
</div>

## 🔒 Security Tools That Actually Work

### Offensive Tools (For Defense, Obviously)

<div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">⚔️ Know Your Enemy</h4>
  <div class="bg-yellow-100 dark:bg-yellow-900/30 p-4 mb-4 rounded border border-yellow-300 dark:border-yellow-700">
    <p class="text-sm text-yellow-800 dark:text-yellow-200">
      <strong>🚨 Ethics First:</strong> Only use these on systems you own or have explicit permission to test.
      Set up isolated lab environments. I use VMs and containers to keep experiments contained.
    </p>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">Recon & Scanning</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-red-400 pl-3">
          <p><a href="https://github.com/projectdiscovery/nuclei" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Nuclei</a> - Template-based vulnerability scanner</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🎯 <strong>My daily driver since May 2023</strong></p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Template count:</strong> 6,847+ community templates as of Oct 2024</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Found in my homelab:</strong> 3 CVEs I didn't know I had (CVE-2023-38646 in Cacti, CVE-2023-28432 in MinIO, CVE-2024-21626 in runc). All patched within 24h.</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Speed:</strong> Scans my entire homelab (15 hosts, 200+ services) in ~8 minutes</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Tip:</strong> Start with severity:high filter, build custom templates later.</p>
        </div>
        <div class="border-l-2 border-orange-400 pl-3">
          <p><a href="https://github.com/projectdiscovery/subfinder" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Subfinder</a> - Subdomain discovery on steroids</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🔍 <strong>Eye-opening:</strong> You'll be shocked how many subdomains your targets have. Combine with Aquatone for visual recon.</p>
        </div>
        <div class="border-l-2 border-pink-400 pl-3">
          <p><a href="https://github.com/michenriksen/aquatone" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Aquatone</a> - Visual recon for web apps</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">📸 <strong>Screenshots save time:</strong> Quickly identify interesting targets visually. Great for reports too.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p><a href="https://github.com/OWASP/Amass" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Amass</a> - Network mapping that's scary good</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🗺️ <strong>Deep dive tool:</strong> When you need to map the entire infrastructure. Slow but thorough.</p>
        </div>
      </div>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">Exploitation Frameworks</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-red-400 pl-3">
          <p><a href="https://github.com/rapid7/metasploit-framework" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">Metasploit</a> - The classic, still relevant</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🏛️ <strong>Still the gold standard:</strong> Heavy but comprehensive. Start here for learning exploitation fundamentals.</p>
        </div>
        <div class="border-l-2 border-blue-400 pl-3">
          <p><a href="https://github.com/calebstewart/pwncat" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">pwncat</a> - Netcat on steroids</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🐱 <strong>Modern approach:</strong> Python-based, extensible. Great for post-exploitation and maintaining access.</p>
        </div>
        <div class="border-l-2 border-green-400 pl-3">
          <p><a href="https://github.com/carlospolop/PEASS-ng" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">PEASS-ng</a> - Privilege escalation scripts</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">⬆️ <strong>Instant results:</strong> Automates the tedious enumeration phase. Run this first when you get a foothold.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p><a href="https://github.com/Flangvik/SharpCollection" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">SharpCollection</a> - .NET tools for red teams</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1">🔧 <strong>Windows specialist:</strong> When you're dealing with modern Windows environments. Bypasses many AV solutions.</p>
        </div>
      </div>
    </div>
  </div>
</div>

### Defensive Arsenal

<div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🛡️ Blue Team Power Tools</h4>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">SIEM & Monitoring</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-2">
        <li>
          <a href="https://wazuh.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Wazuh</a> - Free SIEM that's actually good<br>
          <span class="text-xs text-gray-600 dark:text-gray-500">
            <strong>Deployed:</strong> January 2023 | <strong>Learning curve:</strong> 2 weeks to basic functioning, 3 months to proficiency |
            <strong>Current:</strong> 8 agents monitoring containers, VMs, bare metal | <strong>Alerts/day:</strong> ~200 (tuned down from 2,000+ initially) |
            <strong>Most valuable:</strong> Caught unauthorized SSH attempt from Brazil within 30 seconds
          </span>
        </li>
        <li><a href="https://www.graylog.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Graylog</a> - Log management done right</li>
        <li><a href="https://github.com/SigmaHQ/sigma" class="text-primary-600 dark:text-primary-400 hover:underline">Sigma</a> - Detection rules that work everywhere</li>
        <li><a href="https://thehive-project.org/" class="text-primary-600 dark:text-primary-400 hover:underline">TheHive</a> - Incident response platform</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Network Defense</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://suricata.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Suricata</a> - IDS/IPS that scales</li>
        <li><a href="https://zeek.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Zeek</a> - Network analysis framework</li>
        <li><a href="https://github.com/ntop/ntopng" class="text-primary-600 dark:text-primary-400 hover:underline">ntopng</a> - Traffic analysis with pretty graphs</li>
        <li><a href="https://arkime.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Arkime</a> - Full packet capture and search</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Threat Hunting</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/Velocidex/velociraptor" class="text-primary-600 dark:text-primary-400 hover:underline">Velociraptor</a> - Hunt across your fleet</li>
        <li><a href="https://github.com/osquery/osquery" class="text-primary-600 dark:text-primary-400 hover:underline">osquery</a> - SQL-powered OS instrumentation</li>
        <li><a href="https://github.com/GhostPack/Seatbelt" class="text-primary-600 dark:text-primary-400 hover:underline">Seatbelt</a> - Security checks for Windows</li>
        <li><a href="https://github.com/davehull/Kansa" class="text-primary-600 dark:text-primary-400 hover:underline">Kansa</a> - PowerShell IR framework</li>
      </ul>
    </div>
  </div>
</div>

### Container & Cloud Security

<div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">☁️ Modern Problems, Modern Solutions</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Container Security</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/aquasecurity/trivy" class="text-primary-600 dark:text-primary-400 hover:underline">Trivy</a> - Vulnerability scanner that finds everything</li>
        <li><a href="https://falco.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Falco</a> - Runtime security for containers</li>
        <li><a href="https://github.com/deepfence/SecretScanner" class="text-primary-600 dark:text-primary-400 hover:underline">SecretScanner</a> - Find secrets in containers/images</li>
        <li><a href="https://github.com/controlplaneio/kubesec" class="text-primary-600 dark:text-primary-400 hover:underline">Kubesec</a> - Security risk analysis for K8s</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Cloud Security</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/prowler-cloud/prowler" class="text-primary-600 dark:text-primary-400 hover:underline">Prowler</a> - AWS security assessment</li>
        <li><a href="https://github.com/toniblyx/prowler" class="text-primary-600 dark:text-primary-400 hover:underline">ScoutSuite</a> - Multi-cloud security auditing</li>
        <li><a href="https://github.com/cloudquery/cloudquery" class="text-primary-600 dark:text-primary-400 hover:underline">CloudQuery</a> - Cloud asset inventory</li>
        <li><a href="https://github.com/turbot/steampipe" class="text-primary-600 dark:text-primary-400 hover:underline">Steampipe</a> - Query cloud with SQL</li>
      </ul>
    </div>
  </div>
</div>

## 🎮 Fun Homelab Projects

Because learning should be fun, here are some projects that'll teach you tons:

<div class="bg-gradient-to-r from-indigo-50 to-purple-50 dark:from-indigo-900/20 dark:to-purple-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">Weekend Warriors</h4>
  <div class="space-y-4">
    <div class="border-l-4 border-indigo-500 pl-4">
      <h5 class="font-bold text-gray-800 dark:text-gray-200">🍯 Build a Honeypot Network</h5>
      <p class="text-gray-700 dark:text-gray-300">Deploy <a href="https://github.com/telekom-security/tpotce" class="text-primary-600 dark:text-primary-400 hover:underline">T-Pot</a> and watch the internet try to hack you. Grab popcorn.</p>
    </div>
    <div class="border-l-4 border-purple-500 pl-4">
      <h5 class="font-bold text-gray-800 dark:text-gray-200">🔐 Red Team Lab</h5>
      <p class="text-gray-700 dark:text-gray-300">Set up <a href="https://github.com/Orange-Cyberdefense/GOAD" class="text-primary-600 dark:text-primary-400 hover:underline">GOAD</a> (Game of Active Directory) and practice your pentest skills.</p>
    </div>
    <div class="border-l-4 border-pink-500 pl-4">
      <h5 class="font-bold text-gray-800 dark:text-gray-200">📡 WiFi Pineapple DIY</h5>
      <p class="text-gray-700 dark:text-gray-300">Build your own with a Raspberry Pi and <a href="https://github.com/wifiphisher/wifiphisher" class="text-primary-600 dark:text-primary-400 hover:underline">Wifiphisher</a>. Test your network's security.</p>
    </div>
    <div class="border-l-4 border-blue-500 pl-4">
      <h5 class="font-bold text-gray-800 dark:text-gray-200">🎯 Malware Analysis Lab</h5>
      <p class="text-gray-700 dark:text-gray-300">Set up <a href="https://remnux.org/" class="text-primary-600 dark:text-primary-400 hover:underline">REMnux</a> and <a href="https://github.com/mandiant/flare-vm" class="text-primary-600 dark:text-primary-400 hover:underline">FLARE-VM</a> for safe malware analysis.</p>
    </div>
  </div>
</div>

## 📚 Books That Actually Taught Me Something

<div class="bg-purple-50 dark:bg-purple-900/20 border-l-4 border-purple-400 p-6 my-8">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">📖 My Reading Philosophy</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    I'm a hands-on learner, so books that combine theory with practical exercises work best for me.
    These aren't affiliate links – just books that made me better at what I do.
    I've listed them roughly in the order I'd recommend reading them, with personal notes about what makes each special.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-sm">
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-green-600 dark:text-green-400">📚 Start Here</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Foundation books that build core knowledge</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-blue-600 dark:text-blue-400">🔬 Go Deeper</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Technical deep dives for specific skills</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-purple-600 dark:text-purple-400">🧠 Perspective</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Stories and context that change how you think</p>
    </div>
  </div>
</div>

### Security Essentials

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">Technical Deep Dives</h5>
    <div class="space-y-4">
      <div class="border-l-2 border-green-400 pl-3">
        <p>📚 <strong>START HERE:</strong> <a href="https://www.amazon.com/Web-Application-Hackers-Handbook-Exploiting/dp/1118026470" class="text-primary-600 dark:text-primary-400 hover:underline">The Web Application Hacker's Handbook</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1"><strong>Read:</strong> 2012, re-read: 2023 | <strong>Impact:</strong> Taught me to think like an attacker. Still reference Chapter 9 (attacking authentication) regularly.</p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1"><strong>Time investment:</strong> ~40 hours spread over 3 months | <strong>Value:</strong> Foundational. Everything else builds on this.</p>
      </div>
      <div class="border-l-2 border-blue-400 pl-3">
        <p>📕 <a href="https://www.amazon.com/Practical-Malware-Analysis-Hands-Dissecting/dp/1593272901" class="text-primary-600 dark:text-primary-400 hover:underline">Practical Malware Analysis</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1"><strong>Read:</strong> 2014-2015, ~80 hours total | <strong>Setup time:</strong> 8 hours building isolated analysis environment</p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1"><strong>Learned:</strong> Reverse engineering, PE file structure, behavioral analysis | <strong>Still use:</strong> IDA Free for quick binary analysis</p>
      </div>
      <div class="border-l-2 border-purple-400 pl-3">
        <p>📗 <a href="https://www.amazon.com/Network-Security-Through-Data-Analysis/dp/1491962844" class="text-primary-600 dark:text-primary-400 hover:underline">Network Security Through Data Analysis</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">Turn packet captures into intelligence. This book taught me to think like data, not just look at it. Great for building SIEM detection rules.</p>
      </div>
      <div class="border-l-2 border-orange-400 pl-3">
        <p>📙 <a href="https://www.amazon.com/Rtfm-Red-Team-Field-Manual/dp/1494295504" class="text-primary-600 dark:text-primary-400 hover:underline">RTFM: Red Team Field Manual</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">Cheat codes for pentesters. Keep this handy during engagements. Not for learning fundamentals, but great for quick reference when you're in the thick of it.</p>
      </div>
    </div>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">Mind-Expanding Reads</h5>
    <div class="space-y-4">
      <div class="border-l-2 border-green-400 pl-3">
        <p>📚 <strong>START HERE:</strong> <a href="https://www.amazon.com/Cuckoos-Egg-Tracking-Computer-Espionage/dp/1416507787" class="text-primary-600 dark:text-primary-400 hover:underline">The Cuckoo's Egg</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">The OG hacker hunt story. Written in 1989 but feels modern. Shows that good investigative techniques are timeless. Made me appreciate the detective work in security.</p>
      </div>
      <div class="border-l-2 border-red-400 pl-3">
        <p>📕 <a href="https://www.amazon.com/Sandworm-Cyberwar-Kremlins-Dangerous-Hackers/dp/0385544405" class="text-primary-600 dark:text-primary-400 hover:underline">Sandworm</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">Nation-state hacking that'll keep you up at night. Understanding geopolitical cyber warfare helps you think bigger than just technical vulnerabilities.</p>
      </div>
      <div class="border-l-2 border-blue-400 pl-3">
        <p>📗 <a href="https://www.amazon.com/Ghost-Wires-Adventures-Worlds-Wanted/dp/0316037729" class="text-primary-600 dark:text-primary-400 hover:underline">Ghost in the Wires</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">Kevin Mitnick's wild ride. Shows that social engineering often beats technical attacks. Changed how I think about human factors in security.</p>
      </div>
      <div class="border-l-2 border-purple-400 pl-3">
        <p>📙 <a href="https://www.amazon.com/Cult-Dead-Cow-Original-Supergroup/dp/154176238X" class="text-primary-600 dark:text-primary-400 hover:underline">Cult of the Dead Cow</a></p>
        <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">The hackers who shaped the internet. Great for understanding the culture and ethics that drive security research. Made me appreciate the history behind modern tools.</p>
      </div>
    </div>
  </div>
</div>

### Homelab & DevOps

<div class="bg-blue-50 dark:bg-blue-950/50 p-6 rounded-lg my-6">
  <h5 class="font-bold text-gray-900 dark:text-white mb-3">Level Up Your Lab</h5>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <ul class="text-gray-700 dark:text-gray-200 space-y-2">
      <li>🔧 <a href="https://www.amazon.com/Phoenix-Project-DevOps-Helping-Business/dp/1942788290" class="text-primary-600 dark:text-primary-400 hover:underline">The Phoenix Project</a>
        <br><span class="text-sm text-gray-600">DevOps explained through a story that hits too close to home</span></li>
      <li>⚙️ <a href="https://www.amazon.com/Site-Reliability-Engineering-Production-Systems/dp/149192912X" class="text-primary-600 dark:text-primary-400 hover:underline">Site Reliability Engineering</a>
        <br><span class="text-sm text-gray-600">How Google does it (free online too!)</span></li>
    </ul>
    <ul class="text-gray-700 dark:text-gray-300 space-y-2">
      <li>🐳 <a href="https://www.amazon.com/Docker-Deep-Dive-Poulton-Nigel/dp/1916585256" class="text-primary-600 dark:text-primary-400 hover:underline">Docker Deep Dive</a>
        <br><span class="text-sm text-gray-600">Actually understand containers</span></li>
      <li>☸️ <a href="https://www.amazon.com/Kubernetes-Book-Version-November-2018-ebook/dp/B072TS9ZQZ" class="text-primary-600 dark:text-primary-400 hover:underline">The Kubernetes Book</a>
        <br><span class="text-sm text-gray-600">K8s without the pain</span></li>
    </ul>
  </div>
</div>

## 🎓 Learning Platforms That Don't Suck

<div class="bg-indigo-50 dark:bg-indigo-900/20 border-l-4 border-indigo-400 p-6 my-8">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🎯 My Learning Strategy</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    I learn best by doing, failing, and trying again. Start with free platforms to find what clicks for you,
    then invest money in areas where you want to go deeper. Here's the progression that worked for me:
  </p>
  <div class="grid grid-cols-1 md:grid-cols-4 gap-3 text-sm">
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-green-600 dark:text-green-400">Month 1-2</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Free platforms, basic CTFs</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-blue-600 dark:text-blue-400">Month 3-6</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Paid platform, focused learning</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-purple-600 dark:text-purple-400">Month 6+</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Build your own labs, teach others</p>
    </div>
    <div class="bg-white dark:bg-gray-800 p-3 rounded border">
      <strong class="text-orange-600 dark:text-orange-400">Always</strong>
      <p class="text-gray-600 dark:text-gray-400 mt-1">Keep learning from failures</p>
    </div>
  </div>
</div>

### Free Stuff That's Actually Good

<div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg my-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">Hands-On Labs</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-green-400 pl-3">
          <p>🎯 <a href="https://overthewire.org/wargames/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">OverTheWire</a> - Start with Bandit, thank me later</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Started:</strong> November 2010, still recommend</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Time spent:</strong> 3 weeks on Bandit alone (all 33 levels)</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Lessons:</strong> Linux basics, SSH, bash scripting, basic crypto</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Progression:</strong> Bandit → Leviathan → Natas → Krypton</p>
        </div>
        <div class="border-l-2 border-blue-400 pl-3">
          <p>🏴 <a href="https://picoctf.org/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">PicoCTF</a> - Beginner-friendly CTF</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Great for confidence:</strong> Designed for high schoolers but perfect for adults learning fundamentals. Hint system prevents frustration.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p>🔓 <a href="https://portswigger.net/web-security" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">PortSwigger Academy</a> - Free web security training</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Industry standard:</strong> Made by the Burp Suite team. Interactive labs that teach real vulnerabilities.</p>
        </div>
        <div class="border-l-2 border-orange-400 pl-3">
          <p>🎮 <a href="https://www.hackthissite.org/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">HackThisSite</a> - Old school but gold</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Nostalgic value:</strong> Where I learned basic web vulnerabilities. Interface is dated but content is solid.</p>
        </div>
      </div>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">YouTube University</h5>
      <div class="space-y-3">
        <div class="border-l-2 border-red-400 pl-3">
          <p>📺 <a href="https://www.youtube.com/@ippsec" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">IppSec</a> - HTB walkthroughs that teach</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Watch while doing:</strong> Don't just watch – pause and try techniques yourself. His methodology is gold.</p>
        </div>
        <div class="border-l-2 border-blue-400 pl-3">
          <p>🎬 <a href="https://www.youtube.com/@_JohnHammond" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">John Hammond</a> - CTFs and malware analysis</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Great teacher:</strong> Explains his thinking process clearly. Good for understanding tool usage and methodology.</p>
        </div>
        <div class="border-l-2 border-green-400 pl-3">
          <p>🎥 <a href="https://www.youtube.com/@NetworkChuck" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">NetworkChuck</a> - Makes networking fun</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Enthusiasm wins:</strong> His energy is infectious. Great for homelab inspiration and practical networking.</p>
        </div>
        <div class="border-l-2 border-purple-400 pl-3">
          <p>📹 <a href="https://www.youtube.com/@LiveOverflow" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">LiveOverflow</a> - Deep technical dives</p>
          <p class="text-xs text-gray-600 dark:text-gray-500 mt-1"><strong>Next level:</strong> When you're ready to understand the "why" behind exploits. Requires patience but worth it.</p>
        </div>
      </div>
    </div>
  </div>
</div>

### Worth Paying For

<div class="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg my-6">
  <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-4">💰 When to Invest Your Money</h5>
  <div class="space-y-4">
    <div class="border-l-2 border-green-400 pl-4">
      <p><a href="https://tryhackme.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">TryHackMe</a> - Guided learning path ($10/month)</p>
      <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">
        <strong>Joined:</strong> March 2020, active 2020-2023<br>
        <strong>Subscription cost:</strong> $10/month for 3 years = $360 total<br>
        <strong>Rooms completed:</strong> 180+ (checked my profile)<br>
        <strong>Best learning path:</strong> Pre Security → Complete Beginner → Offensive Pentesting<br>
        <strong>Time to value:</strong> Felt confident testing my homelab after ~2 months<br>
        <strong>Perfect for beginners:</strong> The guided paths prevent you from getting lost. Good mix of theory and practice.
      </p>
    </div>
    <div class="border-l-2 border-red-400 pl-4">
      <p><a href="https://www.hackthebox.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">HackTheBox</a> - More challenging ($20/month)</p>
      <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">
        <strong>Joined:</strong> June 2021, current VIP subscriber<br>
        <strong>Cost:</strong> $20/month, $240/year<br>
        <strong>Boxes completed:</strong> 47 easy, 23 medium, 8 hard (as of Oct 2024)<br>
        <strong>Reality check:</strong> Medium boxes took 6-12 hours each. Hard boxes took 15-20 hours. This isn't quick.<br>
        <strong>Worth it because:</strong> Forces you to try harder. No hand-holding. Real-world-ish.<br>
        <strong>Secret:</strong> The forums and Discord are where the real learning happens.
      </p>
    </div>
    <div class="border-l-2 border-blue-400 pl-4">
      <p><a href="https://academy.tcm-sec.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">TCM Security</a> - Practical courses (varies)</p>
      <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">
        <strong>Real-world focused:</strong> Heath Adams knows his stuff. Courses feel like mentorship.
        <br><strong>Best for:</strong> PNPT certification path or if you want structured learning without fluff.
      </p>
    </div>
    <div class="border-l-2 border-purple-400 pl-4">
      <p><a href="https://www.pentesterlab.com/" class="text-primary-600 dark:text-primary-400 hover:underline font-medium">PentesterLab</a> - Web security focus ($20/month)</p>
      <p class="text-sm text-gray-600 dark:text-gray-500 mt-1">
        <strong>Deep web security:</strong> If you want to really understand web app pentesting, this is it.
        <br><strong>Heads up:</strong> Can be dry. Better after you have some experience with web vulns.
      </p>
    </div>
  </div>
  <div class="mt-4 p-3 bg-blue-100 dark:bg-blue-950/50 rounded border border-blue-300 dark:border-blue-600">
    <p class="text-sm text-blue-900 dark:text-blue-100 mb-2">
      <strong>💡 My recommendation:</strong> Start with TryHackMe for 3-6 months, then add HackTheBox.
      Don't jump around – depth beats breadth when you're learning fundamentals.
    </p>
    <p class="text-sm text-blue-900 dark:text-blue-100">
      <strong>💰 Cost vs benefit:</strong> $360 total for 3 years of TryHackMe = $120/year, cheaper than 2 tech books but way more practical.
      Medium HTB boxes = 6-12 hours but you learn more than 50 easy boxes. Time investment matters more than money.
    </p>
  </div>
</div>

## 🚨 Security News & Intel

Stay paranoid, stay informed:

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Daily Reads</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://krebsonsecurity.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Krebs on Security</a></li>
      <li><a href="https://www.bleepingcomputer.com/" class="text-primary-600 dark:text-primary-400 hover:underline">BleepingComputer</a></li>
      <li><a href="https://thehackernews.com/" class="text-primary-600 dark:text-primary-400 hover:underline">The Hacker News</a></li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Threat Intel</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://otx.alienvault.com/" class="text-primary-600 dark:text-primary-400 hover:underline">AlienVault OTX</a></li>
      <li><a href="https://abuse.ch/" class="text-primary-600 dark:text-primary-400 hover:underline">abuse.ch</a></li>
      <li><a href="https://www.virustotal.com/" class="text-primary-600 dark:text-primary-400 hover:underline">VirusTotal</a></li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Vulnerability Feeds</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.exploit-db.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Exploit-DB</a></li>
      <li><a href="https://vuldb.com/" class="text-primary-600 dark:text-primary-400 hover:underline">VulDB</a></li>
      <li><a href="https://nvd.nist.gov/" class="text-primary-600 dark:text-primary-400 hover:underline">NVD</a></li>
    </ul>
  </div>
</div>

## 🔥 The Bleeding Edge

Tools so new they might break everything (that's half the fun):

<div class="bg-gradient-to-r from-red-50 to-pink-50 dark:from-red-900/20 dark:to-pink-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">⚠️ Use at Your Own Risk</h4>
  <ul class="text-gray-700 dark:text-gray-300 space-y-2">
    <li>🔬 <a href="https://github.com/BishopFox/sliver" class="text-primary-600 dark:text-primary-400 hover:underline">Sliver</a> - Adversary emulation framework (Cobalt Strike alternative)</li>
    <li>🎯 <a href="https://github.com/kgretzky/evilginx2" class="text-primary-600 dark:text-primary-400 hover:underline">Evilginx2</a> - Advanced phishing with 2FA bypass</li>
    <li>🔍 <a href="https://github.com/yogeshojha/rengine" class="text-primary-600 dark:text-primary-400 hover:underline">reNgine</a> - Automated recon framework</li>
    <li>🛠️ <a href="https://github.com/fox-it/bloodhound.py" class="text-primary-600 dark:text-primary-400 hover:underline">BloodHound.py</a> - Active Directory recon</li>
    <li>⚡ <a href="https://github.com/ly4k/Certipy" class="text-primary-600 dark:text-primary-400 hover:underline">Certipy</a> - Active Directory certificate abuse</li>
  </ul>
</div>

## 🚀 Your Next Steps

<div class="bg-gradient-to-r from-green-50 to-blue-50 dark:from-green-900/20 dark:to-blue-900/20 p-8 rounded-lg my-8">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">📋 Start Your Journey</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-6">
    Feeling overwhelmed? That's normal. Here's exactly what I'd do if I were starting today:
  </p>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-bold text-green-600 dark:text-green-400 mb-3">🌱 Week 1-2: Foundation</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Set up a basic homelab VM</li>
        <li>• Install Docker and run Portainer</li>
        <li>• Start OverTheWire Bandit</li>
        <li>• Join TryHackMe (free tier)</li>
        <li>• Read "The Cuckoo's Egg"</li>
      </ul>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-bold text-blue-600 dark:text-blue-400 mb-3">🚀 Month 2-3: Build Momentum</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Deploy your first monitoring stack</li>
        <li>• Complete THM Pre Security path</li>
        <li>• Try your first vulnerability scanner</li>
        <li>• Start learning one programming language</li>
        <li>• Document everything you break</li>
      </ul>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-bold text-purple-600 dark:text-purple-400 mb-3">🔬 Month 4-6: Specialize</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Choose: Red team, blue team, or DevOps</li>
        <li>• Upgrade to paid learning platforms</li>
        <li>• Build projects, not just tutorials</li>
        <li>• Start teaching others what you learn</li>
        <li>• Join communities and ask questions</li>
      </ul>
    </div>
    <div class="bg-white dark:bg-gray-800 p-4 rounded border">
      <h5 class="font-bold text-orange-600 dark:text-orange-400 mb-3">🎯 Month 6+: Master</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Contribute to open source projects</li>
        <li>• Write about your learnings</li>
        <li>• Mentor newcomers</li>
        <li>• Build real solutions to real problems</li>
        <li>• Never stop being curious</li>
      </ul>
    </div>
  </div>

  <div class="mt-6 p-4 bg-yellow-100 dark:bg-yellow-900/30 rounded border border-yellow-300 dark:border-yellow-700">
    <p class="text-sm text-yellow-800 dark:text-yellow-200">
      <strong>🔥 Hot take:</strong> The best way to learn is to fail publicly and document the journey.
      Start a blog, make GitHub repos, and don't be afraid to look stupid. We've all been there.
    </p>
  </div>
</div>

## 🎉 Join the Chaos

<div class="bg-primary-50 dark:bg-primary-900/20 p-6 rounded-lg my-8 text-center">
  <p class="text-lg text-gray-800 dark:text-gray-200 mb-4">
    This list grows every time I find something that makes me go "Oh, that's clever!"
  </p>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    Got a tool that changed your life? Found something that should be on this list?
    Want to argue about why vim is better than nano? (It is.)
  </p>
  <a href="/about/#contact" class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
    Share Your Discoveries
    <svg class="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
    </svg>
  </a>
</div>

<div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 p-6 rounded-lg my-8">
  <h4 class="text-lg font-bold text-red-800 dark:text-red-200 mb-3">⚠️ Final Reminder</h4>
  <div class="text-red-700 dark:text-red-300 space-y-2">
    <p><strong>Ethics first:</strong> Only hack what you own or have explicit permission to test.</p>
    <p><strong>Learn responsibly:</strong> Understand the impact of your actions.</p>
    <p><strong>Back up everything:</strong> Seriously. Back up your backups. Then back up those.</p>
    <p><strong>Document your journey:</strong> Your future self will thank you.</p>
    <p><strong>Have fun:</strong> If you're not enjoying it, you're doing it wrong.</p>
  </div>
</div>

</div>