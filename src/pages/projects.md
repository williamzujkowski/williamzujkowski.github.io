---
layout: page
title: Projects & Portfolio
description: Security engineering projects, open-source contributions, and technical initiatives
permalink: /projects/
eleventyNavigation:
  key: Projects
  title: Projects
  order: 5
---

# Projects & Initiatives

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
From securing federal clouds to building homelab experiments – projects that push boundaries.
</p>

## Featured Projects

### 🏛️ Government & Enterprise

<div class="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-900/20 dark:to-indigo-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">cloud.gov Zero-Trust Implementation</h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 text-xs rounded">Active</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">FedRAMP</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Zero-Trust</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    Leading the implementation of Zero-Trust architecture for cloud.gov, serving 30+ federal agencies with secure cloud infrastructure.
  </p>
  <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 mb-3">
    <li>Designed micro-segmentation strategy for multi-tenant isolation</li>
    <li>Implemented continuous verification using risk-based authentication</li>
    <li>Automated compliance validation for 325 NIST controls</li>
    <li>Reduced incident response time by 30%</li>
  </ul>
  <p class="text-sm text-gray-600 dark:text-gray-400">
    <strong>Tech Stack:</strong> AWS GovCloud, Terraform, Python, Wazuh, OpenSearch, eBPF
  </p>
</div>

<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">NIH Enterprise Vulnerability Management</h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 text-xs rounded">Completed</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Healthcare</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">900+ Endpoints</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    Led vulnerability management program for National Institutes of Health, protecting critical medical research infrastructure.
  </p>
  <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 mb-3">
    <li>Managed scanning and remediation for 900+ endpoints</li>
    <li>Achieved 40% reduction in critical vulnerabilities</li>
    <li>Implemented automated patch management workflows</li>
    <li>Built executive dashboards for risk visibility</li>
  </ul>
  <p class="text-sm text-gray-600 dark:text-gray-400">
    <strong>Tech Stack:</strong> Nessus, Python, Ansible, ServiceNow, PowerBI
  </p>
</div>

<div class="bg-white dark:bg-gray-800 p-6 rounded-lg shadow-md my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">HPC Security for Molecular Dynamics Research</h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-green-100 dark:bg-green-800 text-green-800 dark:text-green-200 text-xs rounded">Completed</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">HPC</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">GPU Compute</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    Secured LoBoS high-performance computing cluster supporting computational chemistry and molecular dynamics research.
  </p>
  <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 mb-3">
    <li>Implemented secure multi-user GPU compute environment</li>
    <li>Designed network isolation for sensitive research data</li>
    <li>Automated security scanning for research containers</li>
    <li>Integrated with SLURM for secure job scheduling</li>
  </ul>
  <p class="text-sm text-gray-600 dark:text-gray-400">
    <strong>Tech Stack:</strong> SLURM, NVLINK GPUs, Ansible, Container Security, Python
  </p>
</div>

### 🛠️ Open Source & Tools

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="#" class="text-primary-600 dark:text-primary-400 hover:underline">FedRAMP Automation Toolkit</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Python toolkit for automating FedRAMP compliance tasks and control validation.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Terraform</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">YAML</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Automated control implementation tracking</li>
      <li>• SSP generation from infrastructure code</li>
      <li>• Continuous compliance monitoring</li>
    </ul>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="#" class="text-primary-600 dark:text-primary-400 hover:underline">Security Ansible Playbooks</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Collection of Ansible playbooks for security hardening and compliance.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Ansible</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">YAML</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Bash</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• CIS benchmark implementation</li>
      <li>• STIG compliance automation</li>
      <li>• Zero-Trust network configs</li>
    </ul>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="#" class="text-primary-600 dark:text-primary-400 hover:underline">Wazuh Integration Tools</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Custom integrations and rules for Wazuh SIEM in federal environments.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">XML</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">OpenSearch</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Custom decoders for gov systems</li>
      <li>• Automated threat hunting queries</li>
      <li>• Compliance reporting dashboards</li>
    </ul>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="#" class="text-primary-600 dark:text-primary-400 hover:underline">Container Security Scanner</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Automated container scanning pipeline for CI/CD integration.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Docker</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">GitHub Actions</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• CVE detection and reporting</li>
      <li>• SBOM generation</li>
      <li>• Policy-as-code enforcement</li>
    </ul>
  </div>

</div>

### 🤖 AI/ML Security Projects

<div class="bg-purple-50 dark:bg-purple-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">LLM Security Evaluation Framework</h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-purple-100 dark:bg-purple-800 text-purple-800 dark:text-purple-200 text-xs rounded">In Progress</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">AI Security</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Research</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    Building a framework for evaluating security vulnerabilities in Large Language Model deployments.
  </p>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div>
      <p class="font-medium text-gray-800 dark:text-gray-200 mb-2">Focus Areas:</p>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Prompt injection detection</li>
        <li>• Data leakage prevention</li>
        <li>• Model robustness testing</li>
        <li>• Adversarial input generation</li>
      </ul>
    </div>
    <div>
      <p class="font-medium text-gray-800 dark:text-gray-200 mb-2">Technologies:</p>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Python, LangChain</li>
        <li>• OpenAI API, Hugging Face</li>
        <li>• Vector databases</li>
        <li>• OWASP LLM Top 10</li>
      </ul>
    </div>
  </div>
</div>

### 🏠 Homelab & Personal Projects

<div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">Security-Focused Homelab</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    Personal security operations center for learning and experimentation.
  </p>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Infrastructure:</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• pfSense firewall with IDS/IPS</li>
        <li>• 5 VLANs for network segmentation</li>
        <li>• Proxmox virtualization cluster</li>
        <li>• Raspberry Pi monitoring nodes</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Security Stack:</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Wazuh SIEM with custom rules</li>
        <li>• OpenSearch for log analysis</li>
        <li>• Grafana security dashboards</li>
        <li>• Automated threat hunting</li>
      </ul>
    </div>
  </div>
  
  <div class="mt-4 p-4 bg-green-100 dark:bg-green-800/20 rounded">
    <p class="text-sm text-green-800 dark:text-green-200">
      <strong>Learning Outcomes:</strong> This lab has been instrumental in testing Zero-Trust concepts, developing automation scripts, and understanding attacker techniques in a safe environment.
    </p>
  </div>
</div>

## Upcoming Projects

<div class="my-8">
  <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-4">🚀 What's Next</h3>
  
  <div class="space-y-4">
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0 w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-full flex items-center justify-center">
        <span class="text-yellow-600 dark:text-yellow-400 text-sm">1</span>
      </div>
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">Quantum-Resistant Cryptography Demo</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">Implementing post-quantum algorithms for federal systems</p>
      </div>
    </div>
    
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0 w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-full flex items-center justify-center">
        <span class="text-yellow-600 dark:text-yellow-400 text-sm">2</span>
      </div>
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">Supply Chain Security Automation</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">SBOM generation and vulnerability tracking at scale</p>
      </div>
    </div>
    
    <div class="flex items-start space-x-3">
      <div class="flex-shrink-0 w-8 h-8 bg-yellow-100 dark:bg-yellow-900 rounded-full flex items-center justify-center">
        <span class="text-yellow-600 dark:text-yellow-400 text-sm">3</span>
      </div>
      <div>
        <p class="font-medium text-gray-900 dark:text-gray-100">AI-Powered Threat Hunting Platform</p>
        <p class="text-sm text-gray-600 dark:text-gray-400">Using ML for anomaly detection in government environments</p>
      </div>
    </div>
  </div>
</div>

## Get Involved

<div class="bg-primary-50 dark:bg-primary-900/20 p-6 rounded-lg my-8 text-center">
  <p class="text-lg text-gray-800 dark:text-gray-200 mb-4">
    Interested in collaborating on security projects or have questions about any of these initiatives?
  </p>
  <div class="flex flex-wrap gap-4 justify-center">
    <a href="/contact/" class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
      Get in Touch
      <svg class="w-5 h-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
    </a>
    <a href="https://github.com/williamzujkowski" class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors">
      View on GitHub
      <svg class="w-5 h-5 ml-2" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
      </svg>
    </a>
  </div>
</div>

</div>