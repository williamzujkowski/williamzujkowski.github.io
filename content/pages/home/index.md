---
title: Home
---

<div class="host-info-box">
  <div class="host-info-header">
    <p class="host-info-title">SYSTEM INFORMATION</p>
    <div class="terminal-controls">
      <span class="terminal-control red"></span>
      <span class="terminal-control yellow"></span>
      <span class="terminal-control green"></span>
    </div>
  </div>

  <div class="connection-status">
    <span class="status-indicator"></span>
    <span class="status-text">CONNECTION ESTABLISHED</span>
    <span class="uptime" id="session-time">00:00:00</span>
  </div>

  <div class="host-info-section">
    <div class="host-info-item">
      <div class="host-info-key"><i class="info-icon">📡</i> IP ADDRESS:</div>
      <div class="host-info-data"><span id="user-ip">Detecting...</span></div>
    </div>
    
    <div class="host-info-item">
      <div class="host-info-key"><i class="info-icon">🕒</i> LOCAL TIME:</div>
      <div class="host-info-data"><span id="current-time">Loading...</span></div>
    </div>
    
    <div class="host-info-item">
      <div class="host-info-key"><i class="info-icon">📍</i> REGION:</div>
      <div class="host-info-data"><span id="user-location">Detecting...</span></div>
    </div>
    
    <div class="host-info-item">
      <div class="host-info-key"><i class="info-icon">💻</i> ENVIRONMENT:</div>
      <div class="host-info-data"><span id="user-browser">Analyzing...</span></div>
    </div>
  </div>
</div>

<div class="arxiv-container">
  <h2 class="arxiv-header">RECENT AI RESEARCH PAPERS</h2>
  <div class="loading-indicator" id="papers-loading">
    <div class="loading-spinner"></div>
    <p>Loading research papers...</p>
  </div>
  
  <div id="papers-container" class="arxiv-papers">
    <!-- Papers will be dynamically inserted here -->
  </div>
  
  <div class="arxiv-footer">
    <p>Papers sourced from <a href="https://arxiv.org/" class="arxiv-source-link" target="_blank">arXiv.org</a></p>
  </div>
</div>

<script>
// Enhanced data loading with performance optimizations
document.addEventListener('DOMContentLoaded', function() {
  // Initialize session timer
  const startTime = new Date();
  const updateSessionTime = () => {
    const now = new Date();
    const diff = Math.floor((now - startTime) / 1000);
    const hours = Math.floor(diff / 3600).toString().padStart(2, '0');
    const minutes = Math.floor((diff % 3600) / 60).toString().padStart(2, '0');
    const seconds = Math.floor(diff % 60).toString().padStart(2, '0');
    document.getElementById('session-time').textContent = `${hours}:${minutes}:${seconds}`;
  };

  // Display current time with animation effect
  const updateTime = () => {
    const now = new Date();
    const timeEl = document.getElementById('current-time');
    
    // Add fade effect
    if (timeEl.textContent !== "Loading...") {
      timeEl.classList.add('time-update');
      setTimeout(() => timeEl.classList.remove('time-update'), 500);
    }
    
    timeEl.textContent = now.toLocaleTimeString() + ' | ' + now.toLocaleDateString();
    updateSessionTime();
  };
  
  // Initial time update and set interval
  updateTime();
  setInterval(updateTime, 1000);
  
  // System information collection (non-blocking)
  setTimeout(() => {
    // Get user IP without blocking page load
    fetch('https://api.ipify.org?format=json')
      .then(response => response.json())
      .then(data => {
        document.getElementById('user-ip').textContent = data.ip || "Unknown";
      })
      .catch(() => {
        document.getElementById('user-ip').textContent = "Unable to detect";
      });
      
    // Enhanced browser and system detection
    const getBrowserInfo = () => {
      const ua = navigator.userAgent;
      let browserName = "Unknown";
      let osName = "Unknown OS";
      
      // Detect browser
      if (ua.match(/chrome|chromium|crios/i)) {
        browserName = ua.match(/edg/i) ? "Edge" : "Chrome";
      } else if (ua.match(/firefox|fxios/i)) {
        browserName = "Firefox";
      } else if (ua.match(/safari/i)) {
        browserName = "Safari";
      } else if (ua.match(/opr\//i)) {
        browserName = "Opera";
      }
      
      // Detect OS
      if (ua.match(/windows|win32|win64/i)) {
        osName = "Windows";
      } else if (ua.match(/macintosh|mac os x/i)) {
        osName = "MacOS";
      } else if (ua.match(/linux/i)) {
        osName = "Linux";
      } else if (ua.match(/android/i)) {
        osName = "Android";
      } else if (ua.match(/iphone|ipad|ipod/i)) {
        osName = "iOS";
      }
      
      return `${browserName} | ${osName}`;
    };
    
    document.getElementById('user-browser').textContent = getBrowserInfo();
    
    // Get location information from timezone
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (timezone) {
      const location = timezone.replace(/_/g, ' ').split('/');
      document.getElementById('user-location').textContent = location.length > 1 ? location[1] : timezone;
    } else {
      document.getElementById('user-location').textContent = "Unknown";
    }
  }, 100); // Small delay to prioritize initial page render
  
  // Function to create arXiv paper elements
  const createPaperElement = (paper, index) => {
    const paperElement = document.createElement('div');
    paperElement.className = 'arxiv-paper';
    
    // Create paper title
    const titleElement = document.createElement('p');
    titleElement.className = 'arxiv-paper-title';
    titleElement.textContent = paper.title;
    
    // Create metadata container
    const metaContainer = document.createElement('div');
    metaContainer.className = 'arxiv-paper-meta';
    
    // Add authors
    const authorsElement = document.createElement('p');
    authorsElement.className = 'arxiv-paper-authors';
    authorsElement.textContent = paper.authors;
    
    // Add date
    const dateElement = document.createElement('p');
    dateElement.className = 'arxiv-paper-date';
    dateElement.textContent = `Published: ${paper.date}`;
    
    // Add to meta container
    metaContainer.appendChild(authorsElement);
    metaContainer.appendChild(dateElement);
    
    // Create abstract
    const abstractElement = document.createElement('p');
    abstractElement.className = 'arxiv-paper-abstract';
    abstractElement.textContent = paper.abstract;
    
    // Create link container
    const linkContainer = document.createElement('div');
    linkContainer.className = 'arxiv-paper-link-container';
    
    // Create link
    const linkElement = document.createElement('a');
    linkElement.className = 'arxiv-paper-link';
    linkElement.href = paper.link;
    linkElement.textContent = 'View on arXiv';
    linkElement.target = '_blank';
    
    // Add link to container
    linkContainer.appendChild(linkElement);
    
    // Build paper element
    paperElement.appendChild(titleElement);
    paperElement.appendChild(metaContainer);
    paperElement.appendChild(abstractElement);
    paperElement.appendChild(linkContainer);
    
    // Add delay for staggered appearance
    paperElement.style.animationDelay = `${index * 0.2}s`;
    
    return paperElement;
  };
  
  // Use cached arXiv data or fetch new data
  const fetchArxivPapers = async () => {
    const papersContainer = document.getElementById('papers-container');
    const loadingIndicator = document.getElementById('papers-loading');
    
    try {
      // Check for cached papers
      const cachedData = localStorage.getItem('arxiv-papers');
      const cachedTime = localStorage.getItem('arxiv-timestamp');
      const now = new Date().getTime();
      
      // Use cache if it's less than 24 hours old
      if (cachedData && cachedTime && (now - parseInt(cachedTime)) < 24 * 60 * 60 * 1000) {
        const papers = JSON.parse(cachedData);
        
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
        
        // Add papers to container
        papers.forEach((paper, index) => {
          papersContainer.appendChild(createPaperElement(paper, index));
        });
        
        return;
      }
      
      // Fetch new papers
      const query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.NE";
      const response = await fetch(`https://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=3`);
      const data = await response.text();
      
      // Parse XML
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "text/xml");
      const entries = xmlDoc.getElementsByTagName('entry');
      
      // Process entries
      const papers = [];
      for (let i = 0; i < Math.min(entries.length, 3); i++) {
        const entry = entries[i];
        const title = entry.getElementsByTagName('title')[0].textContent.trim();
        const authorNodes = entry.getElementsByTagName('author');
        const authors = Array.from(authorNodes)
          .map(author => author.getElementsByTagName('name')[0].textContent);
        const authorText = authors.length > 2 
          ? `${authors.slice(0,2).join(', ')} et al.` 
          : authors.join(', ');
        const published = new Date(entry.getElementsByTagName('published')[0].textContent);
        const link = entry.getElementsByTagName('id')[0].textContent;
        const abstract = entry.getElementsByTagName('summary')[0]?.textContent.trim() || 'No abstract available';
        
        // Limit abstract length
        const truncatedAbstract = abstract.length > 300 
          ? abstract.substring(0, 297) + '...' 
          : abstract;
        
        // Add to papers array
        papers.push({
          title,
          authors: authorText,
          date: published.toLocaleDateString(),
          link,
          abstract: truncatedAbstract
        });
      }
      
      // Cache the papers
      localStorage.setItem('arxiv-papers', JSON.stringify(papers));
      localStorage.setItem('arxiv-timestamp', now.toString());
      
      // Hide loading indicator
      loadingIndicator.style.display = 'none';
      
      // Add papers to container
      papers.forEach((paper, index) => {
        papersContainer.appendChild(createPaperElement(paper, index));
      });
    } catch (error) {
      console.error('Error fetching arXiv papers:', error);
      loadingIndicator.innerHTML = '<p>Unable to load papers at this time.</p>';
    }
  };
  
  // Load papers with slight delay to improve initial page load
  setTimeout(fetchArxivPapers, 500);
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