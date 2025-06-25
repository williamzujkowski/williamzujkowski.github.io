---
layout: page
title: Projects & Open Source
description: Personal projects, open-source tools, and technical experiments. Exploring security automation, AI/ML applications, and developer productivity tools.
# permalink: /projects/ # Removed - content merged into About page
permalink: false
# Remove from navigation - content merged into About page
# eleventyNavigation:
#   key: Projects
#   title: Projects
#   order: 5
image: /assets/images/og/projects-og.png
---

# Open Source Projects

<div class="prose prose-lg prose-gray dark:prose-invert lg:prose-xl max-w-none">

<p class="lead text-xl text-gray-600 dark:text-gray-400 italic">
Building tools that solve real problems – from security automation to AI-powered content generation.
</p>

## 🤖 AI & LLM Projects

<div class="bg-gradient-to-r from-purple-50 to-pink-50 dark:from-purple-900/20 dark:to-pink-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">
    <a href="https://github.com/williamzujkowski/mcp-standards-server" class="text-primary-600 dark:text-primary-400 hover:underline">MCP Standards Server</a>
  </h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-purple-100 dark:bg-purple-800 text-purple-800 dark:text-purple-200 text-xs rounded">Active</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Python</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Model Context Protocol</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    A comprehensive Model Context Protocol (MCP) server providing intelligent NIST 800-53r5 compliance checking, automated code analysis, and standards enforcement for modern development workflows.
  </p>
  <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 mb-3">
    <li>Built using official MCP Python SDK</li>
    <li>Real-time standards compliance validation</li>
    <li>Automated security control mapping</li>
    <li>Integration with AI development tools</li>
  </ul>
  <div class="flex gap-3">
    <a href="https://github.com/williamzujkowski/mcp-standards-server" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">View on GitHub →</a>
  </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/llm-markdown-generator" class="text-primary-600 dark:text-primary-400 hover:underline">LLM Markdown Generator</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Leverages Large Language Models to generate markdown blog posts with customizable, 11ty-compatible front matter for various topics.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">LLM</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">11ty</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Automated content generation</li>
      <li>• SEO-optimized frontmatter</li>
      <li>• Multiple topic support</li>
    </ul>
    <a href="https://github.com/williamzujkowski/llm-markdown-generator" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Project →</a>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/vuln-post-generator" class="text-primary-600 dark:text-primary-400 hover:underline">Vulnerability Post Generator</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      A comprehensive system for generating high-quality vulnerability analysis blog posts using AI.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">AI</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Security</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• CVE analysis automation</li>
      <li>• Technical writing assistance</li>
      <li>• Structured content output</li>
    </ul>
    <a href="https://github.com/williamzujkowski/vuln-post-generator" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Project →</a>
  </div>

</div>

## 🔒 Security & Compliance Tools

<div class="bg-gradient-to-r from-red-50 to-orange-50 dark:from-red-900/20 dark:to-orange-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">
    <a href="https://github.com/williamzujkowski/dependency-risk-profiler" class="text-primary-600 dark:text-primary-400 hover:underline">Dependency Risk Profiler</a>
  </h4>
  <div class="flex flex-wrap gap-2 mb-3">
    <span class="px-2 py-1 bg-red-100 dark:bg-red-800 text-red-800 dark:text-red-200 text-xs rounded">Security</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Python</span>
    <span class="px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 text-xs rounded">Supply Chain</span>
  </div>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    A command-line tool that goes beyond traditional vulnerability scanners to assess the overall health and risk of a project's open-source dependencies.
  </p>
  <ul class="list-disc list-inside text-gray-700 dark:text-gray-300 space-y-1 mb-3">
    <li>Comprehensive dependency analysis</li>
    <li>License compatibility checking</li>
    <li>Maintenance status evaluation</li>
    <li>Supply chain risk scoring</li>
  </ul>
  <div class="flex gap-3">
    <a href="https://github.com/williamzujkowski/dependency-risk-profiler" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">View on GitHub →</a>
  </div>
</div>

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/repovac" class="text-primary-600 dark:text-primary-400 hover:underline">RepoVac</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      A tool for grabbing dependency lists from an entire organization's repositories.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">GitHub API</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">SBOM</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Organization-wide scanning</li>
      <li>• Dependency inventory</li>
      <li>• License tracking</li>
    </ul>
    <a href="https://github.com/williamzujkowski/repovac" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Project →</a>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/dont-panic" class="text-primary-600 dark:text-primary-400 hover:underline">Don't Panic</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Enriched alerting system providing detailed alerts without causing system-wide terror. Success often depends on finding your towel.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Monitoring</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Humor</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Context-aware alerting</li>
      <li>• Panic reduction algorithms</li>
      <li>• Towel location services</li>
    </ul>
    <a href="https://github.com/williamzujkowski/dont-panic" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Project →</a>
  </div>

</div>

## 📊 Data & Intelligence Pipelines

<div class="bg-gradient-to-r from-blue-50 to-cyan-50 dark:from-blue-900/20 dark:to-cyan-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">Vulnerability Intelligence Suite</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-3">
    A comprehensive vulnerability intelligence generation system built with modern data pipeline architecture.
  </p>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
    <div class="bg-white dark:bg-gray-800 p-4 rounded">
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">
        <a href="https://github.com/williamzujkowski/vulnerability-data-pipeline" class="text-primary-600 dark:text-primary-400 hover:underline">Data Pipeline</a>
      </h5>
      <p class="text-sm text-gray-700 dark:text-gray-300 mb-2">
        Ingests data from multiple vulnerability sources, normalizes into common format, and outputs prioritized vulnerabilities.
      </p>
      <div class="flex flex-wrap gap-1">
        <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
        <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">ETL</span>
      </div>
    </div>
    
    <div class="bg-white dark:bg-gray-800 p-4 rounded">
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">
        <a href="https://github.com/williamzujkowski/vulnerability-intelligence-generator" class="text-primary-600 dark:text-primary-400 hover:underline">Intelligence Generator</a>
      </h5>
      <p class="text-sm text-gray-700 dark:text-gray-300 mb-2">
        Uses LangGraph to orchestrate LLM-based analysis workflow, generating insightful intelligence reports.
      </p>
      <div class="flex flex-wrap gap-1">
        <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">LangGraph</span>
        <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">LLM</span>
      </div>
    </div>
  </div>
</div>

## 🛠️ Developer Tools & Utilities

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/pizza-calculator" class="text-primary-600 dark:text-primary-400 hover:underline">Pizza Calculator</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Essential tool for critical team decisions - calculating optimal pizza orders.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">JavaScript</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Essential</span>
    </div>
    <a href="https://github.com/williamzujkowski/pizza-calculator" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">View →</a>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/domainchecker" class="text-primary-600 dark:text-primary-400 hover:underline">Domain Checker</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      A tool for checking available domain names across multiple TLDs.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Python</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">DNS</span>
    </div>
    <a href="https://github.com/williamzujkowski/domainchecker" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">View →</a>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/codesnippets" class="text-primary-600 dark:text-primary-400 hover:underline">Code Snippets</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Collection of useful code snippets and patterns I've collected over the years.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Various</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Reference</span>
    </div>
    <a href="https://github.com/williamzujkowski/codesnippets" class="text-sm text-primary-600 dark:text-primary-400 hover:underline">View →</a>
  </div>

</div>

## 🌐 Web & Standards Projects

<div class="grid grid-cols-1 md:grid-cols-2 gap-6 my-6">
  
  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/standards" class="text-primary-600 dark:text-primary-400 hover:underline">Development Standards</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Comprehensive development standards for modern software projects, integrated with AI tools.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Documentation</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Standards</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Coding standards</li>
      <li>• Security guidelines</li>
      <li>• AI integration patterns</li>
    </ul>
    <a href="https://github.com/williamzujkowski/standards" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Project →</a>
  </div>

  <div class="bg-gray-50 dark:bg-gray-900 p-6 rounded-lg">
    <h4 class="text-lg font-bold text-gray-900 dark:text-gray-100 mb-3">
      <a href="https://github.com/williamzujkowski/williamzujkowski.github.io" class="text-primary-600 dark:text-primary-400 hover:underline">This Website</a>
    </h4>
    <p class="text-gray-700 dark:text-gray-300 mb-3">
      Personal website built with Eleventy, Tailwind CSS, and automated CI/CD via GitHub Actions.
    </p>
    <div class="flex flex-wrap gap-2 mb-3">
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">11ty</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">Tailwind</span>
      <span class="px-2 py-1 bg-gray-200 dark:bg-gray-700 text-xs rounded">GitHub Pages</span>
    </div>
    <ul class="text-sm text-gray-600 dark:text-gray-400 space-y-1">
      <li>• Static site generation</li>
      <li>• Dark mode support</li>
      <li>• Automated deployments</li>
    </ul>
    <a href="https://github.com/williamzujkowski/williamzujkowski.github.io" class="text-sm text-primary-600 dark:text-primary-400 hover:underline mt-2 inline-block">View Source →</a>
  </div>

</div>

## 🏠 Homelab & Personal Learning

<div class="bg-gradient-to-r from-green-50 to-emerald-50 dark:from-green-900/20 dark:to-emerald-900/20 p-6 rounded-lg my-6">
  <h4 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-3">Security-Focused Homelab</h4>
  <p class="text-gray-700 dark:text-gray-300 mb-4">
    Personal security operations center for learning, experimentation, and testing new security concepts.
  </p>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Infrastructure:</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• pfSense firewall with Suricata IDS/IPS</li>
        <li>• 5 VLANs for network segmentation</li>
        <li>• Proxmox virtualization cluster</li>
        <li>• Raspberry Pi monitoring nodes</li>
        <li>• Automated backup systems</li>
      </ul>
    </div>
    <div>
      <h5 class="font-medium text-gray-800 dark:text-gray-200 mb-2">Security Stack:</h5>
      <ul class="text-sm text-gray-700 dark:text-gray-300 space-y-1">
        <li>• Wazuh SIEM with custom rules</li>
        <li>• OpenSearch for log analysis</li>
        <li>• Grafana security dashboards</li>
        <li>• Automated vulnerability scanning</li>
        <li>• Honeypot deployment</li>
      </ul>
    </div>
  </div>
  
  <div class="mt-4 p-4 bg-green-100 dark:bg-green-800/20 rounded">
    <p class="text-sm text-green-800 dark:text-green-200">
      <strong>Learning Outcomes:</strong> This lab serves as a testing ground for Zero-Trust concepts, security automation, and understanding both defensive and offensive techniques in a controlled environment.
    </p>
  </div>
</div>

## 🚀 Current Focus Areas

<div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-6">
  
  <div class="bg-purple-50 dark:bg-purple-900/20 p-4 rounded-lg text-center">
    <div class="text-3xl mb-2">🤖</div>
    <h5 class="font-bold text-gray-900 dark:text-gray-100">AI Security</h5>
    <p class="text-sm text-gray-700 dark:text-gray-300 mt-1">
      LLM security, prompt injection defense, and AI supply chain security
    </p>
  </div>
  
  <div class="bg-blue-50 dark:bg-blue-900/20 p-4 rounded-lg text-center">
    <div class="text-3xl mb-2">🔐</div>
    <h5 class="font-bold text-gray-900 dark:text-gray-100">Zero Trust</h5>
    <p class="text-sm text-gray-700 dark:text-gray-300 mt-1">
      Implementing Zero Trust principles in personal and professional projects
    </p>
  </div>
  
  <div class="bg-green-50 dark:bg-green-900/20 p-4 rounded-lg text-center">
    <div class="text-3xl mb-2">🛠️</div>
    <h5 class="font-bold text-gray-900 dark:text-gray-100">Automation</h5>
    <p class="text-sm text-gray-700 dark:text-gray-300 mt-1">
      Security automation, compliance as code, and developer productivity tools
    </p>
  </div>

</div>

## Get Involved

<div class="bg-primary-50 dark:bg-primary-900/20 p-6 rounded-lg my-8 text-center">
  <p class="text-lg text-gray-800 dark:text-gray-200 mb-4">
    All my projects are open source and welcome contributions! Found a bug? Have an idea? Want to collaborate?
  </p>
  <div class="flex flex-wrap gap-4 justify-center">
    <a href="https://github.com/williamzujkowski" class="inline-flex items-center px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors">
      <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
        <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
      </svg>
      View All Projects on GitHub
    </a>
    <a href="/contact/" class="inline-flex items-center px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors">
      <svg class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
      </svg>
      Get in Touch
    </a>
  </div>
</div>

</div>