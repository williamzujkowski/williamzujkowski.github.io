---
title: Home
---

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
  <div id="papers-container">
    <div class="paper-item">
      <p class="terminal-paper-title" id="paper-title-1">-</p>
      <p class="terminal-paper-details" id="paper-authors-1">-</p>
      <p class="terminal-paper-details" id="paper-date-1">-</p>
      <p class="terminal-paper-link"><a id="paper-link-1" href="#" class="terminal-link">-</a></p>
    </div>
    
    <div class="terminal-mini-divider"></div>
    
    <div class="paper-item">
      <p class="terminal-paper-title" id="paper-title-2">-</p>
      <p class="terminal-paper-details" id="paper-authors-2">-</p>
      <p class="terminal-paper-details" id="paper-date-2">-</p>
      <p class="terminal-paper-link"><a id="paper-link-2" href="#" class="terminal-link">-</a></p>
    </div>
    
    <div class="terminal-mini-divider"></div>
    
    <div class="paper-item">
      <p class="terminal-paper-title" id="paper-title-3">-</p>
      <p class="terminal-paper-details" id="paper-authors-3">-</p>
      <p class="terminal-paper-details" id="paper-date-3">-</p>
      <p class="terminal-paper-link"><a id="paper-link-3" href="#" class="terminal-link">-</a></p>
    </div>
  </div>
</div>
</div>

<script>
// Simple one-time data loading
document.addEventListener('DOMContentLoaded', function() {
  // Display static time
  const now = new Date();
  document.getElementById('current-time').textContent = 
    `${now.toLocaleTimeString()} | ${now.toLocaleDateString()}`;
  
  // Get user IP from ipify (one-time fetch)
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
      document.getElementById('user-ip').textContent = data.ip;
    })
    .catch(() => {
      document.getElementById('user-ip').textContent = "Unable to detect";
    });
  
  // Get latest AI research from arXiv (one-time fetch)
  const query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.NE";
  fetch(`https://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=3`)
    .then(response => response.text())
    .then(data => {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "text/xml");
      
      // Process all entries (up to 3)
      const entries = xmlDoc.getElementsByTagName('entry');
      
      for (let i = 0; i < Math.min(entries.length, 3); i++) {
        const entry = entries[i];
        const title = entry.getElementsByTagName('title')[0].textContent.trim();
        const authors = Array.from(entry.getElementsByTagName('author'))
          .map(author => author.getElementsByTagName('name')[0].textContent)
          .join(', ');
        const published = new Date(entry.getElementsByTagName('published')[0].textContent);
        const link = entry.getElementsByTagName('id')[0].textContent;
        
        // Format and display data for this paper
        const titleEl = document.getElementById(`paper-title-${i+1}`);
        const authorsEl = document.getElementById(`paper-authors-${i+1}`);
        const dateEl = document.getElementById(`paper-date-${i+1}`);
        const linkEl = document.getElementById(`paper-link-${i+1}`);
        
        titleEl.textContent = title.length > 50 ? title.substring(0, 47) + '...' : title;
        
        const authorCount = authors.split(',').length;
        authorsEl.textContent = `${authors.split(',').slice(0,1).join(',')}${authorCount > 1 ? ' et al.' : ''}`;
        
        dateEl.textContent = `${published.toLocaleDateString()}`;
        
        linkEl.href = link;
        linkEl.textContent = "View on arXiv";
      }
    })
    .catch(() => {
      document.getElementById('paper-title-1').textContent = "Unable to fetch papers";
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
