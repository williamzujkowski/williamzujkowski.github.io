---
layout: page
title: Security Resources
description: Curated collection of cybersecurity tools, learning resources, and references for security professionals
permalink: /resources/
eleventyNavigation:
  key: Resources
  title: Resources
  order: 5
image: /assets/images/og/resources-og.png
---

# Security Resources Hub

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
A curated collection of tools, references, and learning materials that have shaped my 15+ years in cybersecurity. Updated regularly as I discover new resources.
</p>

## 🛠️ Essential Security Tools

### Network Security

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🔍 Scanning & Discovery</h4>
    <ul class="space-y-2 text-gray-700 dark:text-gray-300">
      <li><a href="https://nmap.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Nmap</a> - Network discovery and security auditing</li>
      <li><a href="https://github.com/robertdavidgraham/masscan" class="text-primary-600 dark:text-primary-400 hover:underline">Masscan</a> - Fast port scanner</li>
      <li><a href="https://github.com/projectdiscovery/naabu" class="text-primary-600 dark:text-primary-400 hover:underline">Naabu</a> - Fast port scanner written in Go</li>
      <li><a href="https://www.wireshark.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Wireshark</a> - Network protocol analyzer</li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🛡️ Defensive Tools</h4>
    <ul class="space-y-2 text-gray-700 dark:text-gray-300">
      <li><a href="https://suricata.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Suricata</a> - IDS/IPS engine</li>
      <li><a href="https://zeek.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Zeek</a> - Network security monitor</li>
      <li><a href="https://www.snort.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Snort</a> - Network intrusion prevention</li>
      <li><a href="https://www.pfsense.org/" class="text-primary-600 dark:text-primary-400 hover:underline">pfSense</a> - Open source firewall</li>
    </ul>
  </div>
</div>

### Vulnerability Management

<div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🎯 Scanning & Assessment</h4>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Open Source</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.openvas.org/" class="text-primary-600 dark:text-primary-400 hover:underline">OpenVAS</a></li>
        <li><a href="https://github.com/future-architect/vuls" class="text-primary-600 dark:text-primary-400 hover:underline">Vuls</a></li>
        <li><a href="https://github.com/anchore/grype" class="text-primary-600 dark:text-primary-400 hover:underline">Grype</a></li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Web Application</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.zaproxy.org/" class="text-primary-600 dark:text-primary-400 hover:underline">OWASP ZAP</a></li>
        <li><a href="https://portswigger.net/burp/communitydownload" class="text-primary-600 dark:text-primary-400 hover:underline">Burp Suite</a></li>
        <li><a href="https://github.com/sullo/nikto" class="text-primary-600 dark:text-primary-400 hover:underline">Nikto</a></li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Container Security</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/aquasecurity/trivy" class="text-primary-600 dark:text-primary-400 hover:underline">Trivy</a></li>
        <li><a href="https://github.com/quay/clair" class="text-primary-600 dark:text-primary-400 hover:underline">Clair</a></li>
        <li><a href="https://falco.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Falco</a></li>
      </ul>
    </div>
  </div>
</div>

### SIEM & Log Analysis

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">📊 Open Source SIEM</h4>
    <ul class="space-y-2 text-gray-700 dark:text-gray-300">
      <li><a href="https://wazuh.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Wazuh</a> - Unified XDR and SIEM</li>
      <li><a href="https://www.elastic.co/security" class="text-primary-600 dark:text-primary-400 hover:underline">Elastic Security</a> - Elastic Stack for security</li>
      <li><a href="https://www.graylog.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Graylog</a> - Log management platform</li>
      <li><a href="https://siemonster.com/" class="text-primary-600 dark:text-primary-400 hover:underline">SIEMonster</a> - Affordable SIEM</li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">🔎 Log Analysis Tools</h4>
    <ul class="space-y-2 text-gray-700 dark:text-gray-300">
      <li><a href="https://github.com/Cyb3rWard0g/HELK" class="text-primary-600 dark:text-primary-400 hover:underline">HELK</a> - Hunting ELK stack</li>
      <li><a href="https://github.com/SigmaHQ/sigma" class="text-primary-600 dark:text-primary-400 hover:underline">Sigma</a> - Generic signature format</li>
      <li><a href="https://github.com/Neo23x0/sigma" class="text-primary-600 dark:text-primary-400 hover:underline">Chainsaw</a> - Windows event log analysis</li>
      <li><a href="https://uncoder.io/" class="text-primary-600 dark:text-primary-400 hover:underline">Uncoder.io</a> - Query translator</li>
    </ul>
  </div>
</div>

### Incident Response

<div class="bg-red-50 dark:bg-red-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🚨 IR Toolkit</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Memory Analysis</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.volatilityfoundation.org/" class="text-primary-600 dark:text-primary-400 hover:underline">Volatility</a> - Memory forensics</li>
        <li><a href="https://github.com/ufrisk/MemProcFS" class="text-primary-600 dark:text-primary-400 hover:underline">MemProcFS</a> - Memory process file system</li>
        <li><a href="https://github.com/google/rekall" class="text-primary-600 dark:text-primary-400 hover:underline">Rekall</a> - Memory analysis framework</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Forensics Tools</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.sleuthkit.org/" class="text-primary-600 dark:text-primary-400 hover:underline">The Sleuth Kit</a> - Disk forensics</li>
        <li><a href="https://github.com/log2timeline/plaso" class="text-primary-600 dark:text-primary-400 hover:underline">Plaso</a> - Timeline generation</li>
        <li><a href="https://github.com/ANSSI-FR/DFIR-ORC" class="text-primary-600 dark:text-primary-400 hover:underline">DFIR ORC</a> - Forensic artifact collection</li>
      </ul>
    </div>
  </div>
</div>

## 📚 Learning Resources

### Getting Started in Security

<div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🎯 Beginner Path</h4>
  <ol class="list-decimal list-inside text-gray-700 dark:text-gray-300 space-y-2">
    <li><strong>Fundamentals</strong>
      <ul class="list-disc list-inside ml-6 mt-1">
        <li><a href="https://www.professormesser.com/security-plus/sy0-601/sy0-601-video/sy0-601-comptia-security-plus-course/" class="text-primary-600 dark:text-primary-400 hover:underline">Professor Messer Security+</a> - Free video course</li>
        <li><a href="https://www.cybrary.it/" class="text-primary-600 dark:text-primary-400 hover:underline">Cybrary</a> - Free cybersecurity training</li>
      </ul>
    </li>
    <li><strong>Hands-On Practice</strong>
      <ul class="list-disc list-inside ml-6 mt-1">
        <li><a href="https://tryhackme.com/" class="text-primary-600 dark:text-primary-400 hover:underline">TryHackMe</a> - Guided security challenges</li>
        <li><a href="https://www.hackthebox.com/" class="text-primary-600 dark:text-primary-400 hover:underline">HackTheBox</a> - Pentesting labs</li>
      </ul>
    </li>
    <li><strong>Build Projects</strong>
      <ul class="list-disc list-inside ml-6 mt-1">
        <li>Set up a home SIEM with Wazuh</li>
        <li>Create a honeypot with Raspberry Pi</li>
        <li>Build a vulnerability scanner</li>
      </ul>
    </li>
  </ol>
</div>

### Continuous Learning

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">📰 News & Updates</h4>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://krebsonsecurity.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Krebs on Security</a></li>
      <li><a href="https://www.darkreading.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Dark Reading</a></li>
      <li><a href="https://thehackernews.com/" class="text-primary-600 dark:text-primary-400 hover:underline">The Hacker News</a></li>
      <li><a href="https://www.bleepingcomputer.com/" class="text-primary-600 dark:text-primary-400 hover:underline">BleepingComputer</a></li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">🎙️ Podcasts</h4>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://darknetdiaries.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Darknet Diaries</a></li>
      <li><a href="https://twit.tv/shows/security-now" class="text-primary-600 dark:text-primary-400 hover:underline">Security Now</a></li>
      <li><a href="https://malicious.life/" class="text-primary-600 dark:text-primary-400 hover:underline">Malicious Life</a></li>
      <li><a href="https://risky.biz/" class="text-primary-600 dark:text-primary-400 hover:underline">Risky Business</a></li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">📺 YouTube Channels</h4>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.youtube.com/@_JohnHammond" class="text-primary-600 dark:text-primary-400 hover:underline">John Hammond</a></li>
      <li><a href="https://www.youtube.com/@ippsec" class="text-primary-600 dark:text-primary-400 hover:underline">IppSec</a></li>
      <li><a href="https://www.youtube.com/@LiveOverflow" class="text-primary-600 dark:text-primary-400 hover:underline">LiveOverflow</a></li>
      <li><a href="https://www.youtube.com/@NetworkChuck" class="text-primary-600 dark:text-primary-400 hover:underline">NetworkChuck</a></li>
    </ul>
  </div>
</div>

### Training Platforms

<div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🎓 Online Training</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Free/Affordable</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.youtube.com/c/ProfessorMesser" class="text-primary-600 dark:text-primary-400 hover:underline">Professor Messer</a> - CompTIA training</li>
        <li><a href="https://www.sans.org/cyber-ranges/" class="text-primary-600 dark:text-primary-400 hover:underline">SANS Cyber Ranges</a> - Free challenges</li>
        <li><a href="https://portswigger.net/web-security" class="text-primary-600 dark:text-primary-400 hover:underline">PortSwigger Academy</a> - Web security</li>
        <li><a href="https://picoctf.org/" class="text-primary-600 dark:text-primary-400 hover:underline">PicoCTF</a> - Beginner CTF</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Premium</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://www.offensive-security.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Offensive Security</a> - OSCP, OSEP</li>
        <li><a href="https://www.sans.org/" class="text-primary-600 dark:text-primary-400 hover:underline">SANS</a> - Industry gold standard</li>
        <li><a href="https://academy.tcm-sec.com/" class="text-primary-600 dark:text-primary-400 hover:underline">TCM Security</a> - Practical courses</li>
        <li><a href="https://pentesterlab.com/" class="text-primary-600 dark:text-primary-400 hover:underline">PentesterLab</a> - Web pentesting</li>
      </ul>
    </div>
  </div>
</div>

## 🏛️ Frameworks & Standards

### Security Frameworks

<div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg my-6">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">📋 Essential Frameworks</h4>
  <dl class="space-y-4">
    <div>
      <dt class="font-medium text-gray-800 dark:text-gray-200">NIST Cybersecurity Framework</dt>
      <dd class="text-gray-700 dark:text-gray-300 ml-4">
        <a href="https://www.nist.gov/cyberframework" class="text-primary-600 dark:text-primary-400 hover:underline">Official Site</a> - 
        Identify, Protect, Detect, Respond, Recover
      </dd>
    </div>
    <div>
      <dt class="font-medium text-gray-800 dark:text-gray-200">MITRE ATT&CK</dt>
      <dd class="text-gray-700 dark:text-gray-300 ml-4">
        <a href="https://attack.mitre.org/" class="text-primary-600 dark:text-primary-400 hover:underline">ATT&CK Matrix</a> - 
        Adversary tactics and techniques
      </dd>
    </div>
    <div>
      <dt class="font-medium text-gray-800 dark:text-gray-200">CIS Controls</dt>
      <dd class="text-gray-700 dark:text-gray-300 ml-4">
        <a href="https://www.cisecurity.org/controls" class="text-primary-600 dark:text-primary-400 hover:underline">CIS Controls v8</a> - 
        Prioritized security actions
      </dd>
    </div>
    <div>
      <dt class="font-medium text-gray-800 dark:text-gray-200">Zero Trust Architecture</dt>
      <dd class="text-gray-700 dark:text-gray-300 ml-4">
        <a href="https://www.nist.gov/publications/zero-trust-architecture" class="text-primary-600 dark:text-primary-400 hover:underline">NIST SP 800-207</a> - 
        Never trust, always verify
      </dd>
    </div>
  </dl>
</div>

### Compliance Standards

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-blue-50 dark:bg-blue-900/20 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">🏛️ Government</h4>
    <ul class="text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.fedramp.gov/" class="text-primary-600 dark:text-primary-400 hover:underline">FedRAMP</a> - Federal cloud security</li>
      <li><a href="https://public.cyber.mil/stigs/" class="text-primary-600 dark:text-primary-400 hover:underline">DISA STIGs</a> - Security technical guides</li>
      <li><a href="https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final" class="text-primary-600 dark:text-primary-400 hover:underline">NIST 800-53</a> - Security controls</li>
      <li><a href="https://www.cisa.gov/cdm" class="text-primary-600 dark:text-primary-400 hover:underline">CDM</a> - Continuous diagnostics</li>
    </ul>
  </div>
  
  <div class="bg-green-50 dark:bg-green-900/20 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">🏢 Industry</h4>
    <ul class="text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.pcisecuritystandards.org/" class="text-primary-600 dark:text-primary-400 hover:underline">PCI DSS</a> - Payment card security</li>
      <li><a href="https://www.hipaajournal.com/" class="text-primary-600 dark:text-primary-400 hover:underline">HIPAA</a> - Healthcare security</li>
      <li><a href="https://www.iso.org/isoiec-27001-information-security.html" class="text-primary-600 dark:text-primary-400 hover:underline">ISO 27001</a> - Information security</li>
      <li><a href="https://www.aicpa.org/soc" class="text-primary-600 dark:text-primary-400 hover:underline">SOC 2</a> - Service organization controls</li>
    </ul>
  </div>
</div>

## 🤖 AI & Security Resources

### AI Security Tools

<div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🧠 AI/ML Security</h4>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Defensive Tools</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://github.com/Trusted-AI/adversarial-robustness-toolbox" class="text-primary-600 dark:text-primary-400 hover:underline">ART</a> - Adversarial Robustness Toolbox</li>
        <li><a href="https://github.com/cleverhans-lab/cleverhans" class="text-primary-600 dark:text-primary-400 hover:underline">CleverHans</a> - Adversarial examples library</li>
        <li><a href="https://github.com/protectai/rebuff" class="text-primary-600 dark:text-primary-400 hover:underline">Rebuff</a> - Prompt injection detection</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Resources</h5>
      <ul class="text-gray-700 dark:text-gray-300 space-y-1">
        <li><a href="https://owasp.org/www-project-top-10-for-large-language-model-applications/" class="text-primary-600 dark:text-primary-400 hover:underline">OWASP LLM Top 10</a></li>
        <li><a href="https://aivillage.org/" class="text-primary-600 dark:text-primary-400 hover:underline">AI Village</a> - AI security community</li>
        <li><a href="https://github.com/cncf/tag-security/tree/main/supply-chain-security/compromises" class="text-primary-600 dark:text-primary-400 hover:underline">AI Supply Chain Security</a></li>
      </ul>
    </div>
  </div>
</div>

## 🏠 Homelab Resources

### Getting Started

<div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg my-6">
  <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">🔧 Homelab Essentials</h4>
  <div class="space-y-4">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200">Virtualization</h5>
      <ul class="text-gray-700 dark:text-gray-300 ml-4 space-y-1">
        <li><a href="https://www.proxmox.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Proxmox VE</a> - Type 1 hypervisor</li>
        <li><a href="https://www.vmware.com/products/workstation-player.html" class="text-primary-600 dark:text-primary-400 hover:underline">VMware Workstation</a> - Desktop virtualization</li>
        <li><a href="https://www.virtualbox.org/" class="text-primary-600 dark:text-primary-400 hover:underline">VirtualBox</a> - Free, cross-platform</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200">Networking</h5>
      <ul class="text-gray-700 dark:text-gray-300 ml-4 space-y-1">
        <li><a href="https://docs.netgate.com/pfsense/en/latest/" class="text-primary-600 dark:text-primary-400 hover:underline">pfSense Docs</a> - Firewall setup</li>
        <li><a href="https://pi-hole.net/" class="text-primary-600 dark:text-primary-400 hover:underline">Pi-hole</a> - DNS sinkhole</li>
        <li><a href="https://www.gns3.com/" class="text-primary-600 dark:text-primary-400 hover:underline">GNS3</a> - Network simulation</li>
      </ul>
    </div>
  </div>
</div>

## 🎯 Career Resources

### Certification Paths

<div class="bg-yellow-50 dark:bg-yellow-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">🏆 Recommended Cert Paths</h4>
  <div class="space-y-3">
    <div class="border-l-4 border-green-500 pl-4">
      <h5 class="font-medium">Entry Level</h5>
      <p class="text-gray-700 dark:text-gray-300">CompTIA A+ → Network+ → Security+</p>
    </div>
    <div class="border-l-4 border-blue-500 pl-4">
      <h5 class="font-medium">Blue Team</h5>
      <p class="text-gray-700 dark:text-gray-300">CySA+ → GCIH → GNFA → GCFA</p>
    </div>
    <div class="border-l-4 border-red-500 pl-4">
      <h5 class="font-medium">Red Team</h5>
      <p class="text-gray-700 dark:text-gray-300">PenTest+ → OSCP → OSEP → OSEE</p>
    </div>
    <div class="border-l-4 border-purple-500 pl-4">
      <h5 class="font-medium">Cloud Security</h5>
      <p class="text-gray-700 dark:text-gray-300">AWS CCP → AWS SAA → AWS Security Specialty</p>
    </div>
  </div>
</div>

### Job Hunting

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">💼 Job Boards</h4>
    <ul class="text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.indeed.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Indeed</a> - General job board</li>
      <li><a href="https://www.clearancejobs.com/" class="text-primary-600 dark:text-primary-400 hover:underline">ClearanceJobs</a> - Cleared positions</li>
      <li><a href="https://www.usajobs.gov/" class="text-primary-600 dark:text-primary-400 hover:underline">USAJobs</a> - Federal positions</li>
      <li><a href="https://www.cyberseek.org/" class="text-primary-600 dark:text-primary-400 hover:underline">CyberSeek</a> - Career pathways</li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="font-bold text-gray-900 dark:text-gray-100 mb-3">🤝 Communities</h4>
    <ul class="text-gray-700 dark:text-gray-300 space-y-1">
      <li><a href="https://www.reddit.com/r/cybersecurity/" class="text-primary-600 dark:text-primary-400 hover:underline">r/cybersecurity</a> - Reddit community</li>
      <li><a href="https://discord.gg/infosec" class="text-primary-600 dark:text-primary-400 hover:underline">InfoSec Discord</a> - Chat community</li>
      <li>Local BSides conferences</li>
      <li><a href="https://www.meetup.com/" class="text-primary-600 dark:text-primary-400 hover:underline">Meetup</a> - Local groups</li>
    </ul>
  </div>
</div>

## 📖 Recommended Books

### Essential Reading

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Fundamentals</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li>The Web Application Hacker's Handbook</li>
      <li>Network Security Through Data Analysis</li>
      <li>Applied Cryptography</li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Incident Response</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li>The Art of Memory Forensics</li>
      <li>Incident Response & Computer Forensics</li>
      <li>Blue Team Field Manual</li>
    </ul>
  </div>
  
  <div class="bg-gray-50 dark:bg-gray-900 p-4 rounded-lg">
    <h5 class="font-bold text-gray-900 dark:text-gray-100 mb-2">Leadership</h5>
    <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
      <li>The Phoenix Project</li>
      <li>Tribe of Hackers</li>
      <li>The Cuckoo's Egg</li>
    </ul>
  </div>
</div>

## 🔄 Stay Updated

<div class="bg-primary-50 dark:bg-primary-900/20 p-6 rounded-lg my-8 text-center">
  <p class="text-lg text-gray-800 dark:text-gray-200 mb-4">
    This page is updated monthly with new tools and resources I discover.
  </p>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    Have a resource that should be included? Found a broken link?
  </p>
  <a href="/about/#contact" class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
    Suggest a Resource
    <svg class="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
    </svg>
  </a>
</div>

</div>