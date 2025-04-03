---
title: Home
---

# Welcome to the Digital Frontier

<div class="terminal-box" id="main-terminal">
<div class="terminal-header-container">
  <p class="terminal-text terminal-header">NEURAL COMMAND CENTER</p>
  <div class="terminal-controls">
    <span class="terminal-control red"></span>
    <span class="terminal-control yellow"></span>
    <span class="terminal-control green"></span>
  </div>
</div>

<div class="terminal-section">
  <p class="terminal-label">IP</p>
  <p class="terminal-value"><span id="user-ip">-</span></p>
  
  <p class="terminal-label">TIME</p>
  <p class="terminal-value"><span id="current-time">-</span></p>
</div>

<div class="terminal-divider"></div>

<div class="terminal-section">
  <p class="terminal-text terminal-subheader">LATEST AI RESEARCH</p>
  <p class="terminal-paper-title" id="paper-title">-</p>
  <p class="terminal-paper-details" id="paper-authors">-</p>
  <p class="terminal-paper-details" id="paper-date">-</p>
  <p class="terminal-paper-link"><a id="paper-link" href="#" class="terminal-link">-</a></p>
</div>
</div>

<script>
// Simple API handlers with no animations or typing effects
document.addEventListener('DOMContentLoaded', function() {
  // Display current time
  const now = new Date();
  document.getElementById('current-time').textContent = 
    `${now.toLocaleTimeString()} | ${now.toLocaleDateString()}`;
  
  // Get user IP from ipify
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
      document.getElementById('user-ip').textContent = data.ip;
    })
    .catch(() => {
      document.getElementById('user-ip').textContent = "Unable to detect";
    });
  
  // Get latest AI research from arXiv
  const query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.NE";
  fetch(`https://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=1`)
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "text/xml");
      
      const entry = xmlDoc.getElementsByTagName('entry')[0];
      const title = entry.getElementsByTagName('title')[0].textContent.trim();
      const authors = Array.from(entry.getElementsByTagName('author'))
        .map(author => author.getElementsByTagName('name')[0].textContent)
        .join(', ');
      const published = new Date(entry.getElementsByTagName('published')[0].textContent);
      const link = entry.getElementsByTagName('id')[0].textContent;
      
      // Format and display data
      document.getElementById('paper-title').textContent = 
        title.length > 60 ? title.substring(0, 57) + '...' : title;
      
      const authorCount = authors.split(',').length;
      document.getElementById('paper-authors').textContent = 
        `Authors: ${authors.split(',').slice(0,2).join(',')}${authorCount > 2 ? ' + more' : ''}`;
      
      document.getElementById('paper-date').textContent = 
        `Published: ${published.toLocaleDateString()}`;
      
      const paperLink = document.getElementById('paper-link');
      paperLink.href = link;
      paperLink.textContent = "View on arXiv";
    })
    .catch(() => {
      document.getElementById('paper-title').textContent = "Unable to fetch paper";
    });
});
</script>

## About Me

I'm William Zujkowski, a technology enthusiast and developer with a passion for cybersecurity, AI, and cloud-native technologies. This digital space serves as my personal nexus for sharing knowledge, projects, and insights.

## Current Projects

- **Neural Network Research**: Exploring transformer architectures and their applications
- **Cloud Security Framework**: Developing robust security patterns for cloud-native applications
- **Advanced Encryption**: Implementing quantum-resistant cryptographic methods

## Skills & Expertise

- **Languages**: Python, JavaScript, Go, Rust
- **Platforms**: AWS, Azure, GCP, Kubernetes
- **Security**: Penetration Testing, Vulnerability Assessment, Secure Coding
- **AI/ML**: Deep Learning, NLP, Computer Vision
