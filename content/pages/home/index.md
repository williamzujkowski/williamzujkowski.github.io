---
title: Home
---

<div class="host-info-box">
  <div class="host-info-header">
    <p class="host-info-title">NEURAL COMMAND CENTER</p>
    <div class="terminal-controls">
      <span class="terminal-control red"></span>
      <span class="terminal-control yellow"></span>
      <span class="terminal-control green"></span>
    </div>
  </div>

  <div class="host-info-section">
    <div class="host-info-item">
      <p class="host-info-label">IP</p>
      <p class="host-info-value"><span id="user-ip">-</span></p>
    </div>
    
    <div class="host-info-item">
      <p class="host-info-label">TIME</p>
      <p class="host-info-value"><span id="current-time">-</span></p>
    </div>
    
    <div class="host-info-item">
      <p class="host-info-label">LOCATION</p>
      <p class="host-info-value"><span id="user-location">-</span></p>
    </div>
    
    <div class="host-info-item">
      <p class="host-info-label">BROWSER</p>
      <p class="host-info-value"><span id="user-browser">-</span></p>
    </div>
  </div>
</div>

<div class="arxiv-container">
  <h2 class="arxiv-header">LATEST AI RESEARCH</h2>
  
  <div id="papers-container" class="arxiv-papers">
    <div class="arxiv-paper">
      <p class="arxiv-paper-title" id="paper-title-1">-</p>
      <div class="arxiv-paper-meta">
        <p class="arxiv-paper-authors" id="paper-authors-1">-</p>
        <p class="arxiv-paper-date" id="paper-date-1">-</p>
      </div>
      <p class="arxiv-paper-abstract" id="paper-abstract-1">-</p>
      <div class="arxiv-paper-link-container">
        <a id="paper-link-1" href="#" class="arxiv-paper-link">View on arXiv</a>
      </div>
    </div>
    
    <div class="arxiv-paper">
      <p class="arxiv-paper-title" id="paper-title-2">-</p>
      <div class="arxiv-paper-meta">
        <p class="arxiv-paper-authors" id="paper-authors-2">-</p>
        <p class="arxiv-paper-date" id="paper-date-2">-</p>
      </div>
      <p class="arxiv-paper-abstract" id="paper-abstract-2">-</p>
      <div class="arxiv-paper-link-container">
        <a id="paper-link-2" href="#" class="arxiv-paper-link">View on arXiv</a>
      </div>
    </div>
    
    <div class="arxiv-paper">
      <p class="arxiv-paper-title" id="paper-title-3">-</p>
      <div class="arxiv-paper-meta">
        <p class="arxiv-paper-authors" id="paper-authors-3">-</p>
        <p class="arxiv-paper-date" id="paper-date-3">-</p>
      </div>
      <p class="arxiv-paper-abstract" id="paper-abstract-3">-</p>
      <div class="arxiv-paper-link-container">
        <a id="paper-link-3" href="#" class="arxiv-paper-link">View on arXiv</a>
      </div>
    </div>
  </div>
</div>

<script>
// Enhanced data loading
document.addEventListener('DOMContentLoaded', function() {
  // Display current time
  const updateTime = () => {
    const now = new Date();
    document.getElementById('current-time').textContent = 
      `${now.toLocaleTimeString()} | ${now.toLocaleDateString()}`;
  };
  
  // Initial time update and set interval
  updateTime();
  setInterval(updateTime, 1000);
  
  // Get user IP from ipify
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
      document.getElementById('user-ip').textContent = data.ip;
    })
    .catch(() => {
      document.getElementById('user-ip').textContent = "Unable to detect";
    });
  
  // Get browser info
  const browserInfo = () => {
    const ua = navigator.userAgent;
    let browserName = "Unknown";
    
    if (ua.match(/chrome|chromium|crios/i)) {
      browserName = "Chrome";
    } else if (ua.match(/firefox|fxios/i)) {
      browserName = "Firefox";
    } else if (ua.match(/safari/i)) {
      browserName = "Safari";
    } else if (ua.match(/opr\//i)) {
      browserName = "Opera";
    } else if (ua.match(/edg/i)) {
      browserName = "Edge";
    }
    
    return `${browserName} | ${navigator.platform}`;
  };
  
  document.getElementById('user-browser').textContent = browserInfo();
  
  // Try to get approximate location based on timezone
  const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  document.getElementById('user-location').textContent = timezone || "Unknown";
  
  // Get latest AI research from arXiv with abstracts
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
        const abstract = entry.getElementsByTagName('summary')[0]?.textContent.trim() || 'No abstract available';
        
        // Format and display data for this paper
        const titleEl = document.getElementById(`paper-title-${i+1}`);
        const authorsEl = document.getElementById(`paper-authors-${i+1}`);
        const dateEl = document.getElementById(`paper-date-${i+1}`);
        const abstractEl = document.getElementById(`paper-abstract-${i+1}`);
        const linkEl = document.getElementById(`paper-link-${i+1}`);
        
        titleEl.textContent = title;
        
        // Format authors (show first two, then "et al" if more)
        const authorList = authors.split(',');
        const authorText = authorList.length > 2 
          ? `${authorList.slice(0,2).join(', ')} et al.` 
          : authors;
        authorsEl.textContent = authorText;
        
        dateEl.textContent = `Published: ${published.toLocaleDateString()}`;
        
        // Limit abstract length
        abstractEl.textContent = abstract.length > 300 
          ? abstract.substring(0, 297) + '...' 
          : abstract;
        
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