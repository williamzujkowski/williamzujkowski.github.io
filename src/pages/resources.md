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

## 🚀 Hot Right Now: Tools I'm Excited About

These are the tools that have me staying up way too late "just testing one more thing."

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/slimtoolkit/slim" class="text-primary-600 dark:text-primary-400 hover:underline">Slim.AI</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Container minification that actually works. Turned my 1.2GB containers into 40MB. Black magic.
    </p>
    <p class="text-sm text-gray-600 dark:text-gray-500">
      Why I love it: Smaller attack surface + faster deploys = happy me
    </p>
  </div>

  <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/tailscale/tailscale" class="text-primary-600 dark:text-primary-400 hover:underline">Tailscale</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      WireGuard VPN that just works. No port forwarding, no crying.
    </p>
    <p class="text-sm text-gray-600 dark:text-gray-500">
      Why I love it: Connected my homelab to my phone in 2 minutes. TWO MINUTES.
    </p>
  </div>

  <div class="bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/crowdsecurity/crowdsec" class="text-primary-600 dark:text-primary-400 hover:underline">CrowdSec</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Collaborative IPS that actually learns from attacks. Like fail2ban grew a brain.
    </p>
    <p class="text-sm text-gray-600 dark:text-gray-500">
      Why I love it: Community-powered threat intel that actually works
    </p>
  </div>

  <div class="bg-gradient-to-br from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/netdata/netdata" class="text-primary-600 dark:text-primary-400 hover:underline">Netdata</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-2">
      Real-time monitoring that doesn't need a PhD to configure. Pretty graphs included.
    </p>
    <p class="text-sm text-gray-600 dark:text-gray-500">
      Why I love it: Found a memory leak in 5 minutes that I'd been hunting for days
    </p>
  </div>
</div>

## 🏠 Homelab Essentials: The Foundation

### Container & Orchestration

<div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg my-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">🐳 Container Platforms</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-2">
        <li><a href="https://www.portainer.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Portainer</a> - Docker management that doesn't suck</li>
        <li><a href="https://k3s.io/" class="text-primary-600 dark:text-primary-400 hover:underline">K3s</a> - Kubernetes for humans (only 40MB!)</li>
        <li><a href="https://podman.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Podman</a> - Docker without the daemon drama</li>
        <li><a href="https://www.nomadproject.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Nomad</a> - Simple orchestration that actually is simple</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-3">🔧 Infrastructure as Code</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-2">
        <li><a href="https://www.ansible.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Ansible</a> - Automate all the things</li>
        <li><a href="https://www.terraform.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Terraform</a> - For when you want to code your infrastructure</li>
        <li><a href="https://www.pulumi.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Pulumi</a> - Terraform but with real programming languages</li>
        <li><a href="https://github.com/hashicorp/packer" class="text-primary-600 dark:text-primary-400 hover:underline">Packer</a> - Golden images done right</li>
      </ul>
    </div>
  </div>
</div>

### Self-Hosted Services That Don't Suck

<div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🎯 Actually Useful Services</h4>
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

## 🔒 Security Tools That Actually Work

### Offensive Tools (For Defense, Obviously)

<div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">⚔️ Know Your Enemy</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Recon & Scanning</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/projectdiscovery/nuclei" class="text-primary-600 dark:text-primary-400 hover:underline">Nuclei</a> - Template-based vulnerability scanner</li>
        <li><a href="https://github.com/projectdiscovery/subfinder" class="text-primary-600 dark:text-primary-400 hover:underline">Subfinder</a> - Subdomain discovery on steroids</li>
        <li><a href="https://github.com/michenriksen/aquatone" class="text-primary-600 dark:text-primary-400 hover:underline">Aquatone</a> - Visual recon for web apps</li>
        <li><a href="https://github.com/OWASP/Amass" class="text-primary-600 dark:text-primary-400 hover:underline">Amass</a> - Network mapping that's scary good</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Exploitation Frameworks</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/rapid7/metasploit-framework" class="text-primary-600 dark:text-primary-400 hover:underline">Metasploit</a> - The classic, still relevant</li>
        <li><a href="https://github.com/calebstewart/pwncat" class="text-primary-600 dark:text-primary-400 hover:underline">pwncat</a> - Netcat on steroids</li>
        <li><a href="https://github.com/carlospolop/PEASS-ng" class="text-primary-600 dark:text-primary-400 hover:underline">PEASS-ng</a> - Privilege escalation scripts</li>
        <li><a href="https://github.com/Flangvik/SharpCollection" class="text-primary-600 dark:text-primary-400 hover:underline">SharpCollection</a> - .NET tools for red teams</li>
      </ul>
    </div>
  </div>
</div>

### Defensive Arsenal

<div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🛡️ Blue Team Power Tools</h4>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">SIEM & Monitoring</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://wazuh.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Wazuh</a> - Free SIEM that's actually good</li>
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

Not affiliate links, just books worth your money:

### Security Essentials

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">Technical Deep Dives</h5>
    <ul class="text-gray-700 dark:text-gray-300 space-y-2">
      <li>📘 <a href="https://www.amazon.com/Web-Application-Hackers-Handbook-Exploiting/dp/1118026470" class="text-primary-600 dark:text-primary-400 hover:underline">The Web Application Hacker's Handbook</a>
        <br><span class="text-sm text-gray-600">Still the bible for web security</span></li>
      <li>📕 <a href="https://www.amazon.com/Practical-Malware-Analysis-Hands-Dissecting/dp/1593272901" class="text-primary-600 dark:text-primary-400 hover:underline">Practical Malware Analysis</a>
        <br><span class="text-sm text-gray-600">How to dissect malware without infecting yourself</span></li>
      <li>📗 <a href="https://www.amazon.com/Network-Security-Through-Data-Analysis/dp/1491962844" class="text-primary-600 dark:text-primary-400 hover:underline">Network Security Through Data Analysis</a>
        <br><span class="text-sm text-gray-600">Turn packet captures into intelligence</span></li>
      <li>📙 <a href="https://www.amazon.com/Rtfm-Red-Team-Field-Manual/dp/1494295504" class="text-primary-600 dark:text-primary-400 hover:underline">RTFM: Red Team Field Manual</a>
        <br><span class="text-sm text-gray-600">Cheat codes for pentesters</span></li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">Mind-Expanding Reads</h5>
    <ul class="text-gray-700 dark:text-gray-300 space-y-2">
      <li>📘 <a href="https://www.amazon.com/Cuckoos-Egg-Tracking-Computer-Espionage/dp/1416507787" class="text-primary-600 dark:text-primary-400 hover:underline">The Cuckoo's Egg</a>
        <br><span class="text-sm text-gray-600">The OG hacker hunt story</span></li>
      <li>📕 <a href="https://www.amazon.com/Sandworm-Cyberwar-Kremlins-Dangerous-Hackers/dp/0385544405" class="text-primary-600 dark:text-primary-400 hover:underline">Sandworm</a>
        <br><span class="text-sm text-gray-600">Nation-state hacking that'll keep you up at night</span></li>
      <li>📗 <a href="https://www.amazon.com/Ghost-Wires-Adventures-Worlds-Wanted/dp/0316037729" class="text-primary-600 dark:text-primary-400 hover:underline">Ghost in the Wires</a>
        <br><span class="text-sm text-gray-600">Kevin Mitnick's wild ride</span></li>
      <li>📙 <a href="https://www.amazon.com/Cult-Dead-Cow-Original-Supergroup/dp/154176238X" class="text-primary-600 dark:text-primary-400 hover:underline">Cult of the Dead Cow</a>
        <br><span class="text-sm text-gray-600">The hackers who shaped the internet</span></li>
    </ul>
  </div>
</div>

### Homelab & DevOps

<div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg my-6">
  <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">Level Up Your Lab</h5>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <ul class="text-gray-700 dark:text-gray-300 space-y-2">
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

### Free Stuff That's Actually Good

<div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg my-6">
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Hands-On Labs</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li>🎯 <a href="https://overthewire.org/wargames/" class="text-primary-600 dark:text-primary-400 hover:underline">OverTheWire</a> - Start with Bandit, thank me later</li>
        <li>🏴 <a href="https://picoctf.org/" class="text-primary-600 dark:text-primary-400 hover:underline">PicoCTF</a> - Beginner-friendly CTF</li>
        <li>🔓 <a href="https://portswigger.net/web-security" class="text-primary-600 dark:text-primary-400 hover:underline">PortSwigger Academy</a> - Free web security training</li>
        <li>🎮 <a href="https://www.hackthissite.org/" class="text-primary-600 dark:text-primary-400 hover:underline">HackThisSite</a> - Old school but gold</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">YouTube University</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li>📺 <a href="https://www.youtube.com/@ippsec" class="text-primary-600 dark:text-primary-400 hover:underline">IppSec</a> - HTB walkthroughs that teach</li>
        <li>🎬 <a href="https://www.youtube.com/@_JohnHammond" class="text-primary-600 dark:text-primary-400 hover:underline">John Hammond</a> - CTFs and malware analysis</li>
        <li>🎥 <a href="https://www.youtube.com/@NetworkChuck" class="text-primary-600 dark:text-primary-400 hover:underline">NetworkChuck</a> - Makes networking fun</li>
        <li>📹 <a href="https://www.youtube.com/@LiveOverflow" class="text-primary-600 dark:text-primary-400 hover:underline">LiveOverflow</a> - Deep technical dives</li>
      </ul>
    </div>
  </div>
</div>

### Worth Paying For

<div class="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg my-6">
  <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-3">💰 If You're Going to Spend Money</h5>
  <ul class="text-gray-700 dark:text-gray-300 space-y-2">
    <li><a href="https://tryhackme.com/" class="text-primary-600 dark:text-primary-400 hover:underline">TryHackMe</a> - Guided learning path, great for beginners ($10/month)</li>
    <li><a href="https://www.hackthebox.com/" class="text-primary-600 dark:text-primary-400 hover:underline">HackTheBox</a> - More challenging, great community ($20/month)</li>
    <li><a href="https://academy.tcm-sec.com/" class="text-primary-600 dark:text-primary-400 hover:underline">TCM Security</a> - Practical, real-world focused courses</li>
    <li><a href="https://www.pentesterlab.com/" class="text-primary-600 dark:text-primary-400 hover:underline">PentesterLab</a> - Web security focus ($20/month)</li>
  </ul>
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

<div class="text-center text-gray-600 dark:text-gray-400 my-8">
  <p class="italic">Remember: With great tools comes great responsibility. Only hack what you own, </p>
  <p class="italic">and always have backups. Seriously. Backups of your backups.</p>
</div>

</div>