---
title: Home
---

<div class="page-wrapper">
  <div class="main-column">
    <div class="profile-card">
      <div class="profile-header">
        <h2 class="profile-name">William Zujkowski</h2>
        <div class="profile-title">Technology Enthusiast & Developer</div>
      </div>
      <div class="profile-content">
        <p>A passionate developer focused on cybersecurity, AI, and cloud-native technologies. This digital space serves as my personal nexus for sharing knowledge, projects, and insights.</p>
      </div>
    </div>

    <div class="section-card">
      <div class="section-header">
        <div class="section-icon">🔍</div>
        <h2 class="section-title">CURRENT PROJECTS</h2>
      </div>
      <div class="projects-grid">
        <div class="project-item fade-in-element">
          <div class="project-icon">🧠</div>
          <div class="project-content">
            <h3 class="project-title">Neural Network Research</h3>
            <p class="project-description">Exploring transformer architectures and their applications in natural language processing and computer vision.</p>
            <div class="tech-tags">
              <span class="tech-tag">PyTorch</span>
              <span class="tech-tag">TensorFlow</span>
              <span class="tech-tag">NLP</span>
            </div>
          </div>
        </div>
        
        <div class="project-item fade-in-element" style="animation-delay: 0.2s;">
          <div class="project-icon">🔐</div>
          <div class="project-content">
            <h3 class="project-title">Cloud Security Framework</h3>
            <p class="project-description">Developing robust security patterns for cloud-native applications with emphasis on zero-trust architecture.</p>
            <div class="tech-tags">
              <span class="tech-tag">Kubernetes</span>
              <span class="tech-tag">Docker</span>
              <span class="tech-tag">IAM</span>
            </div>
          </div>
        </div>
        
        <div class="project-item fade-in-element" style="animation-delay: 0.4s;">
          <div class="project-icon">🔒</div>
          <div class="project-content">
            <h3 class="project-title">Advanced Encryption</h3>
            <p class="project-description">Implementing quantum-resistant cryptographic methods to prepare for post-quantum computing era.</p>
            <div class="tech-tags">
              <span class="tech-tag">Cryptography</span>
              <span class="tech-tag">Rust</span>
              <span class="tech-tag">Quantum</span>
            </div>
          </div>
        </div>
      </div>
      <div class="section-footer">
        <p>More projects available on <a href="https://github.com/williamzujkowski" class="github-link" target="_blank">GitHub <span class="external-link-icon">↗</span></a></p>
      </div>
    </div>

    <div class="section-card">
      <div class="section-header">
        <div class="section-icon">⚡</div>
        <h2 class="section-title">SKILLS & EXPERTISE</h2>
      </div>
      <div class="skills-container">
        <div class="skill-category fade-in-element">
          <h3 class="skill-category-name">Languages</h3>
          <div class="skill-items">
            <span class="skill-tag">Python</span>
            <span class="skill-tag">JavaScript</span>
            <span class="skill-tag">Go</span>
            <span class="skill-tag">Rust</span>
            <span class="skill-tag">TypeScript</span>
          </div>
          <div class="skill-meter">
            <div class="meter-label">Proficiency</div>
            <div class="meter-bar">
              <div class="meter-fill" style="width: 90%;"></div>
            </div>
          </div>
        </div>
        
        <div class="skill-category fade-in-element" style="animation-delay: 0.2s;">
          <h3 class="skill-category-name">Platforms</h3>
          <div class="skill-items">
            <span class="skill-tag">AWS</span>
            <span class="skill-tag">Azure</span>
            <span class="skill-tag">GCP</span>
            <span class="skill-tag">Kubernetes</span>
            <span class="skill-tag">Docker</span>
          </div>
          <div class="skill-meter">
            <div class="meter-label">Proficiency</div>
            <div class="meter-bar">
              <div class="meter-fill" style="width: 85%;"></div>
            </div>
          </div>
        </div>
        
        <div class="skill-category fade-in-element" style="animation-delay: 0.4s;">
          <h3 class="skill-category-name">Security</h3>
          <div class="skill-items">
            <span class="skill-tag">Penetration Testing</span>
            <span class="skill-tag">Vulnerability Assessment</span>
            <span class="skill-tag">Secure Coding</span>
            <span class="skill-tag">Zero Trust</span>
          </div>
          <div class="skill-meter">
            <div class="meter-label">Proficiency</div>
            <div class="meter-bar">
              <div class="meter-fill" style="width: 95%;"></div>
            </div>
          </div>
        </div>
        
        <div class="skill-category fade-in-element" style="animation-delay: 0.6s;">
          <h3 class="skill-category-name">AI/ML</h3>
          <div class="skill-items">
            <span class="skill-tag">Deep Learning</span>
            <span class="skill-tag">NLP</span>
            <span class="skill-tag">Computer Vision</span>
            <span class="skill-tag">Transformers</span>
            <span class="skill-tag">RAG</span>
          </div>
          <div class="skill-meter">
            <div class="meter-label">Proficiency</div>
            <div class="meter-bar">
              <div class="meter-fill" style="width: 88%;"></div>
            </div>
          </div>
        </div>
      </div>
      <div class="section-footer">
        <p>Continuous learning and improvement in emerging technologies</p>
      </div>
    </div>
  </div>
  
  <div class="side-column">
    <div class="host-info-box">
      <div class="host-info-header">
        <p class="host-info-title">CLIENT CONNECTION</p>
        <div class="terminal-controls">
          <span class="terminal-control red"></span>
          <span class="terminal-control yellow"></span>
          <span class="terminal-control green"></span>
        </div>
      </div>

      <div class="connection-status">
        <span class="status-indicator"></span>
        <span class="status-text">SESSION ACTIVE</span>
        <span class="uptime" id="session-time">00:00:00</span>
      </div>

      <div class="host-info-section">
        <div class="host-info-grid">
          <div class="grid-item animated-border">
            <div class="grid-item-icon">📡</div>
            <div class="grid-item-label">IP ADDRESS</div>
            <div class="grid-item-value"><span id="user-ip">Detecting...</span></div>
          </div>
          
          <div class="grid-item animated-border">
            <div class="grid-item-icon">🕒</div>
            <div class="grid-item-label">LOCAL TIME</div>
            <div class="grid-item-value"><span id="current-time">Loading...</span></div>
          </div>
          
          <div class="grid-item animated-border">
            <div class="grid-item-icon">📍</div>
            <div class="grid-item-label">LOCATION</div>
            <div class="grid-item-value"><span id="user-location">Detecting...</span></div>
          </div>
          
          <div class="grid-item animated-border">
            <div class="grid-item-icon">💻</div>
            <div class="grid-item-label">SYSTEM</div>
            <div class="grid-item-value"><span id="user-browser">Analyzing...</span></div>
          </div>
        </div>
      </div>
      
      <div class="connection-footer">
        <div class="connection-metrics">
          <div class="metric">
            <span class="metric-label">PING</span>
            <span class="metric-value" id="ping-value">--</span>
          </div>
          <div class="metric">
            <span class="metric-label">HTTPS</span>
            <span class="metric-value secure">SECURE</span>
          </div>
        </div>
      </div>
    </div>

    <div class="arxiv-container">
      <div class="arxiv-header">
        <div class="paper-icon">📝</div>
        <h2 class="arxiv-title">LATEST AI RESEARCH</h2>
      </div>
      
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
    // Define ping measurement function first
    const simulatePingMeasurement = () => {
      // Simulate a ping time between 40ms and 150ms
      const pingStart = performance.now();
      
      setTimeout(() => {
        const pingTime = Math.floor(Math.random() * 100) + 40;
        document.getElementById('ping-value').textContent = pingTime + "ms";
        
        // Add color based on ping value
        const pingElement = document.getElementById('ping-value');
        if (pingTime < 60) {
          pingElement.classList.add('ping-good');
        } else if (pingTime < 100) {
          pingElement.classList.add('ping-medium');
        } else {
          pingElement.classList.add('ping-high');
        }
      }, 1200); // Simulated delay for ping measurement
    };
  
    // Get user IP without blocking page load
    fetch('https://api.ipify.org?format=json')
      .then(response => response.json())
      .then(data => {
        document.getElementById('user-ip').textContent = data.ip || "Unknown";
        // Simulate ping measurement
        simulatePingMeasurement();
      })
      .catch(() => {
        document.getElementById('user-ip').textContent = "Unable to detect";
        document.getElementById('ping-value').textContent = "N/A";
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
  
  // Function to create arXiv paper elements with enhanced styling
  const createPaperElement = (paper, index) => {
    const paperElement = document.createElement('div');
    paperElement.className = 'arxiv-paper';
    
    // Create paper title with icon
    const titleWrapper = document.createElement('div');
    titleWrapper.className = 'paper-title-wrapper';
    
    // Add category badge
    const categoryBadge = document.createElement('div');
    categoryBadge.className = 'paper-category';
    const aiCategories = {
      'cs.AI': 'AI',
      'cs.LG': 'ML',
      'cs.NE': 'Neural',
      'cs.CL': 'NLP',
      'cs.CV': 'Vision'
    };
    
    // Extract category from link or use default
    let category = 'AI';
    for (const [cat, label] of Object.entries(aiCategories)) {
      if (paper.link.includes(cat)) {
        category = label;
        break;
      }
    }
    categoryBadge.textContent = category;
    
    const titleElement = document.createElement('h3');
    titleElement.className = 'arxiv-paper-title';
    titleElement.textContent = paper.title;
    
    titleWrapper.appendChild(categoryBadge);
    titleWrapper.appendChild(titleElement);
    
    // Create metadata container
    const metaContainer = document.createElement('div');
    metaContainer.className = 'arxiv-paper-meta';
    
    // Add authors with icon
    const authorsWrapper = document.createElement('div');
    authorsWrapper.className = 'paper-meta-item';
    
    const authorsIcon = document.createElement('span');
    authorsIcon.className = 'meta-icon';
    authorsIcon.textContent = '👤';
    
    const authorsText = document.createElement('span');
    authorsText.className = 'meta-text';
    authorsText.textContent = paper.authors;
    
    authorsWrapper.appendChild(authorsIcon);
    authorsWrapper.appendChild(authorsText);
    
    // Add date with icon
    const dateWrapper = document.createElement('div');
    dateWrapper.className = 'paper-meta-item';
    
    const dateIcon = document.createElement('span');
    dateIcon.className = 'meta-icon';
    dateIcon.textContent = '📅';
    
    const dateText = document.createElement('span');
    dateText.className = 'meta-text';
    dateText.textContent = paper.date;
    
    dateWrapper.appendChild(dateIcon);
    dateWrapper.appendChild(dateText);
    
    // Add to meta container
    metaContainer.appendChild(authorsWrapper);
    metaContainer.appendChild(dateWrapper);
    
    // Create abstract with icon
    const abstractWrapper = document.createElement('div');
    abstractWrapper.className = 'paper-abstract-wrapper';
    
    const abstractIcon = document.createElement('span');
    abstractIcon.className = 'abstract-icon';
    abstractIcon.textContent = '📄';
    
    const abstractText = document.createElement('p');
    abstractText.className = 'arxiv-paper-abstract';
    abstractText.textContent = paper.abstract;
    
    // Add a read more toggle
    const readMoreBtn = document.createElement('span');
    readMoreBtn.className = 'read-more-toggle';
    readMoreBtn.textContent = 'Read more';
    readMoreBtn.addEventListener('click', function() {
      if (abstractText.classList.contains('expanded')) {
        abstractText.classList.remove('expanded');
        readMoreBtn.textContent = 'Read more';
      } else {
        abstractText.classList.add('expanded');
        readMoreBtn.textContent = 'Show less';
      }
    });
    
    abstractWrapper.appendChild(abstractIcon);
    abstractWrapper.appendChild(abstractText);
    abstractWrapper.appendChild(readMoreBtn);
    
    // Create link container
    const linkContainer = document.createElement('div');
    linkContainer.className = 'arxiv-paper-link-container';
    
    // Create link
    const linkElement = document.createElement('a');
    linkElement.className = 'arxiv-paper-link';
    linkElement.href = paper.link;
    linkElement.innerHTML = '<span class="link-icon">🔗</span> View on arXiv';
    linkElement.target = '_blank';
    
    // Add link to container
    linkContainer.appendChild(linkElement);
    
    // Build paper element
    paperElement.appendChild(titleWrapper);
    paperElement.appendChild(metaContainer);
    paperElement.appendChild(abstractWrapper);
    paperElement.appendChild(linkContainer);
    
    // Add delay for staggered appearance
    paperElement.style.animationDelay = `${index * 0.2}s`;
    
    return paperElement;
  };
  
  // Use cached arXiv data or fetch new data with improved caching
  const fetchArxivPapers = async () => {
    const papersContainer = document.getElementById('papers-container');
    const loadingIndicator = document.getElementById('papers-loading');
    
    try {
      // Check for cached papers with better cache management
      const cachedData = localStorage.getItem('arxiv-papers');
      const cachedTime = localStorage.getItem('arxiv-timestamp');
      const now = new Date().getTime();
      
      // Use cache if it's less than 12 hours old (reduced from 24)
      if (cachedData && cachedTime && (now - parseInt(cachedTime)) < 12 * 60 * 60 * 1000) {
        const papers = JSON.parse(cachedData);
        
        // Hide loading indicator
        loadingIndicator.style.display = 'none';
        
        // Add papers to container
        papers.forEach((paper, index) => {
          papersContainer.appendChild(createPaperElement(paper, index));
        });
        
        // Refresh cache in background if older than 6 hours
        if ((now - parseInt(cachedTime)) > 6 * 60 * 60 * 1000) {
          setTimeout(() => refreshPapersCache(), 2000);
        }
        
        return;
      }
      
      // Fetch new papers
      await fetchNewPapers();
      
    } catch (error) {
      console.error('Error fetching arXiv papers:', error);
      
      // Try to use cache even if it's old when fetch fails
      const cachedData = localStorage.getItem('arxiv-papers');
      if (cachedData) {
        const papers = JSON.parse(cachedData);
        loadingIndicator.style.display = 'none';
        papers.forEach((paper, index) => {
          papersContainer.appendChild(createPaperElement(paper, index));
        });
      } else {
        loadingIndicator.innerHTML = '<p>Unable to load papers at this time.</p>';
      }
    }
  };
  
  // Function to fetch new papers from arXiv
  const fetchNewPapers = async () => {
    const papersContainer = document.getElementById('papers-container');
    const loadingIndicator = document.getElementById('papers-loading');
    const now = new Date().getTime();
    
    // Fetch new papers - add more AI-related categories
    const query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.NE+OR+cat:cs.CL+OR+cat:cs.CV";
    const response = await fetch(`https://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=3`);
    const data = await response.text();
    
    // Parse XML
    const parser = new DOMParser();
    const xmlDoc = parser.parseFromString(data, "text/xml");
    const entries = xmlDoc.getElementsByTagName('entry');
    
    // Process entries with improved metadata
    const papers = [];
    for (let i = 0; i < Math.min(entries.length, 3); i++) {
      const entry = entries[i];
      
      // Extract title, clean up formatting
      let title = entry.getElementsByTagName('title')[0].textContent.trim();
      // Remove line breaks and excessive spaces
      title = title.replace(/\s+/g, ' ');
      // Remove common arXiv title prefixes
      title = title.replace(/^\[.*?\]\s*/, '');
      
      // Improved author formatting
      const authorNodes = entry.getElementsByTagName('author');
      const authors = Array.from(authorNodes)
        .map(author => author.getElementsByTagName('name')[0].textContent);
      const authorText = authors.length > 2 
        ? `${authors.slice(0,2).join(', ')} et al.` 
        : authors.join(', ');
      
      // Better date formatting
      const published = new Date(entry.getElementsByTagName('published')[0].textContent);
      const dateOptions = { year: 'numeric', month: 'short', day: 'numeric' };
      const formattedDate = published.toLocaleDateString(undefined, dateOptions);
      
      // Extract URL and full abstract
      const link = entry.getElementsByTagName('id')[0].textContent;
      const abstract = entry.getElementsByTagName('summary')[0]?.textContent.trim() || 'No abstract available';
      
      // Process abstract - keep full text but clean formatting
      const cleanedAbstract = abstract
        .replace(/\s+/g, ' ')  // Remove excess whitespace
        .replace(/\$.*?\$/g, '') // Remove LaTeX formulae for cleaner display
        .trim();
      
      // Add to papers array with improved data
      papers.push({
        title,
        authors: authorText,
        date: formattedDate,
        link,
        abstract: cleanedAbstract
      });
    }
    
    // Cache the papers
    localStorage.setItem('arxiv-papers', JSON.stringify(papers));
    localStorage.setItem('arxiv-timestamp', now.toString());
    
    // Hide loading indicator
    loadingIndicator.style.display = 'none';
    
    // Clear existing papers
    papersContainer.innerHTML = '';
    
    // Add papers to container
    papers.forEach((paper, index) => {
      papersContainer.appendChild(createPaperElement(paper, index));
    });
  };
  
  // Function to refresh cache in background with improved handling
  const refreshPapersCache = async () => {
    try {
      // Use the same expanded query as the main function
      const query = "cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.NE+OR+cat:cs.CL+OR+cat:cs.CV";
      const response = await fetch(`https://export.arxiv.org/api/query?search_query=${query}&sortBy=submittedDate&sortOrder=descending&max_results=3`);
      const data = await response.text();
      
      // Parse XML
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, "text/xml");
      const entries = xmlDoc.getElementsByTagName('entry');
      
      // Process entries with the same improved metadata handling
      const papers = [];
      for (let i = 0; i < Math.min(entries.length, 3); i++) {
        const entry = entries[i];
        
        // Extract title, clean up formatting
        let title = entry.getElementsByTagName('title')[0].textContent.trim();
        title = title.replace(/\s+/g, ' ').replace(/^\[.*?\]\s*/, '');
        
        // Improved author formatting
        const authorNodes = entry.getElementsByTagName('author');
        const authors = Array.from(authorNodes)
          .map(author => author.getElementsByTagName('name')[0].textContent);
        const authorText = authors.length > 2 
          ? `${authors.slice(0,2).join(', ')} et al.` 
          : authors.join(', ');
        
        // Better date formatting
        const published = new Date(entry.getElementsByTagName('published')[0].textContent);
        const dateOptions = { year: 'numeric', month: 'short', day: 'numeric' };
        const formattedDate = published.toLocaleDateString(undefined, dateOptions);
        
        const link = entry.getElementsByTagName('id')[0].textContent;
        const abstract = entry.getElementsByTagName('summary')[0]?.textContent.trim() || 'No abstract available';
        
        // Process abstract - clean formatting
        const cleanedAbstract = abstract
          .replace(/\s+/g, ' ')
          .replace(/\$.*?\$/g, '')
          .trim();
        
        // Add to papers array
        papers.push({
          title,
          authors: authorText,
          date: formattedDate,
          link,
          abstract: cleanedAbstract
        });
      }
      
      // Update cache with fresh data and extended timestamp
      localStorage.setItem('arxiv-papers', JSON.stringify(papers));
      localStorage.setItem('arxiv-timestamp', new Date().getTime().toString());
      
      // Update analytics for cache performance (could be expanded in future)
      localStorage.setItem('arxiv-cache-refresh-count', 
        (parseInt(localStorage.getItem('arxiv-cache-refresh-count') || '0') + 1).toString());
      
      console.log('ArXiv papers cache refreshed in background');
    } catch (error) {
      console.error('Background cache refresh failed:', error);
      // Log failures but don't disrupt user experience
      localStorage.setItem('arxiv-last-error', new Date().toISOString() + ': ' + error.message);
    }
  };
  
  // Load papers with slight delay to improve initial page load
  setTimeout(fetchArxivPapers, 300);
});
</script>