document.addEventListener('DOMContentLoaded', () => {
  // Add cursor blink effect to terminal prompts
  const prompts = document.querySelectorAll('.prompt');
  prompts.forEach(prompt => {
    const cursor = document.createElement('span');
    cursor.classList.add('cursor');
    cursor.innerHTML = '_';
    prompt.appendChild(cursor);
  });

  // Simulate client information if on home page
  const terminalBox = document.querySelector('.terminal-box');
  if (terminalBox) {
    simulateClientInfo();
  }
});

// Simulate client information display
function simulateClientInfo() {
  const clientIp = '192.168.1.' + Math.floor(Math.random() * 255);
  const browserInfo = getBrowserInfo();
  const locations = ['New York', 'San Francisco', 'London', 'Tokyo', 'Berlin', 'Sydney'];
  const randomLocation = locations[Math.floor(Math.random() * locations.length)];
  
  // Add to the DOM if element exists
  const clientInfoElem = document.querySelector('.client-info');
  if (clientInfoElem) {
    // This is just for display - not actual tracking
    clientInfoElem.innerHTML = `
      <div class="info-grid">
        <div class="info-item">
          <span class="info-label">IP:</span>
          <span class="info-value">${clientIp}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Browser:</span>
          <span class="info-value">${browserInfo}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Location:</span>
          <span class="info-value">${randomLocation}</span>
        </div>
        <div class="info-item">
          <span class="info-label">Ping:</span>
          <span class="info-value ping-value">--</span>
        </div>
      </div>
    `;
    
    // Simulate ping measurement
    simulatePing();
  }
}

// Get browser information
function getBrowserInfo() {
  const ua = navigator.userAgent;
  let browser = 'Unknown';
  
  if (ua.indexOf('Firefox') > -1) {
    browser = 'Firefox';
  } else if (ua.indexOf('SamsungBrowser') > -1) {
    browser = 'Samsung';
  } else if (ua.indexOf('Opera') > -1 || ua.indexOf('OPR') > -1) {
    browser = 'Opera';
  } else if (ua.indexOf('Trident') > -1) {
    browser = 'IE';
  } else if (ua.indexOf('Edge') > -1) {
    browser = 'Edge';
  } else if (ua.indexOf('Chrome') > -1) {
    browser = 'Chrome';
  } else if (ua.indexOf('Safari') > -1) {
    browser = 'Safari';
  }
  
  return browser;
}

// Simulate ping measurement
function simulatePing() {
  const pingElem = document.querySelector('.ping-value');
  if (!pingElem) return;
  
  function updatePing() {
    // Random ping between 15-80ms
    const ping = Math.floor(Math.random() * 65) + 15;
    pingElem.textContent = ping + 'ms';
    
    // Change color based on ping value
    if (ping < 30) {
      pingElem.style.color = '#00ff9d'; // Green
    } else if (ping < 50) {
      pingElem.style.color = '#ffcc00'; // Yellow
    } else {
      pingElem.style.color = '#ff3366'; // Red
    }
  }
  
  // Initial update
  updatePing();
  
  // Update every 3-8 seconds
  setInterval(updatePing, Math.floor(Math.random() * 5000) + 3000);
}
