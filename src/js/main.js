// Show page loader
const pageLoader = document.createElement('div');
pageLoader.className = 'page-loader';
pageLoader.innerHTML = `
  <div class="loader-spinner"></div>
  <div class="loader-text">Loading...</div>
`;
document.body.appendChild(pageLoader);

// Hide loader when page is fully loaded
window.addEventListener('load', () => {
  setTimeout(() => {
    pageLoader.classList.add('page-loader-hidden');
    setTimeout(() => {
      pageLoader.remove();
    }, 500);
  }, 300);
});

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
    animateTerminalCommands();
  }
  
  // Initialize search function
  initSearch();
  
  // Add scroll to top button
  addScrollToTopButton();
  
  // Add keyboard navigation for accessibility
  addKeyboardNavigation();
  
  // Add parallax effect to cards on mouse move
  addCardParallaxEffect();
  
  // Add scroll reveal animations
  addScrollRevealAnimations();
  
  // Initialize theme toggle
  initThemeToggle();
  
  // Add progressive image loading
  addProgressiveImageLoading();
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

// Initialize search functionality
function initSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;
  
  searchInput.addEventListener('input', function() {
    const query = this.value.toLowerCase();
    const searchableElements = document.querySelectorAll('.searchable');
    
    searchableElements.forEach(element => {
      const text = element.textContent.toLowerCase();
      if (text.includes(query) || query === '') {
        element.style.display = '';
      } else {
        element.style.display = 'none';
      }
    });
    
    // Update count of visible items
    const visibleCount = document.querySelectorAll('.searchable:not([style="display: none;"])').length;
    const resultCount = document.getElementById('search-results-count');
    if (resultCount) {
      resultCount.textContent = visibleCount;
    }
  });
}

// Add scroll to top button
function addScrollToTopButton() {
  // Create the button
  const button = document.createElement('button');
  button.innerHTML = '&uarr;';
  button.className = 'scroll-top-btn';
  button.setAttribute('aria-label', 'Scroll to top');
  button.style.display = 'none';
  document.body.appendChild(button);
  
  // Show/hide button based on scroll position
  window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
      button.style.display = 'block';
    } else {
      button.style.display = 'none';
    }
  });
  
  // Scroll to top when clicked
  button.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    });
  });
}

// Add keyboard navigation for accessibility
function addKeyboardNavigation() {
  // Skip to content link
  const skipLink = document.createElement('a');
  skipLink.href = '#main-content';
  skipLink.className = 'skip-link';
  skipLink.textContent = 'Skip to content';
  document.body.prepend(skipLink);
  
  // Add tabindex to main elements
  const mainContent = document.querySelector('main');
  if (mainContent) {
    mainContent.id = 'main-content';
    mainContent.setAttribute('tabindex', '-1');
  }
  
  // Add aria attributes to navigation
  const navItems = document.querySelectorAll('nav a');
  navItems.forEach(item => {
    if (window.location.pathname === item.getAttribute('href')) {
      item.setAttribute('aria-current', 'page');
    }
  });
  
  // Add keyboard support for theme toggle
  const themeToggle = document.querySelector('.theme-toggle');
  if (themeToggle) {
    themeToggle.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        toggleTheme();
      }
    });
  }
}

// Initialize and handle theme toggle
function initThemeToggle() {
  // Create theme toggle button
  const themeToggle = document.createElement('button');
  themeToggle.className = 'theme-toggle';
  themeToggle.setAttribute('aria-label', 'Toggle dark/light mode');
  themeToggle.setAttribute('title', 'Toggle dark/light mode');
  themeToggle.setAttribute('type', 'button');
  themeToggle.setAttribute('tabindex', '0');
  themeToggle.innerHTML = `
    <span class="theme-toggle-icon">
      <svg class="sun-icon" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5"></circle>
        <line x1="12" y1="1" x2="12" y2="3"></line>
        <line x1="12" y1="21" x2="12" y2="23"></line>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
        <line x1="1" y1="12" x2="3" y2="12"></line>
        <line x1="21" y1="12" x2="23" y2="12"></line>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
      </svg>
      <svg class="moon-icon" xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
      </svg>
    </span>
  `;
  
  // Add click event listener to toggle theme
  themeToggle.addEventListener('click', toggleTheme);
  
  // Add to the header
  const headerSocial = document.querySelector('.header-social');
  if (headerSocial) {
    headerSocial.insertBefore(themeToggle, headerSocial.firstChild);
  }
  
  // Set initial theme based on user preference or system setting
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    document.documentElement.classList.toggle('dark', savedTheme === 'dark');
  }
}

// Toggle between light and dark themes
function toggleTheme() {
  const isDark = document.documentElement.classList.toggle('dark');
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
  
  // Announce theme change to screen readers
  const announcement = document.createElement('div');
  announcement.setAttribute('aria-live', 'polite');
  announcement.classList.add('sr-only');
  announcement.textContent = `Theme switched to ${isDark ? 'dark' : 'light'} mode`;
  document.body.appendChild(announcement);
  
  // Remove announcement after it's been read
  setTimeout(() => {
    document.body.removeChild(announcement);
  }, 3000);
}

// Animate terminal commands with typewriter effect
function animateTerminalCommands() {
  // Get all command elements
  const commands = document.querySelectorAll('.command');
  
  // Apply typewriter effect to each command
  commands.forEach((command, index) => {
    const text = command.textContent;
    const delay = index * 1500; // Stagger the animations
    
    // Clear the text content
    command.textContent = '';
    
    // Set up the animation with setTimeout
    setTimeout(() => {
      let i = 0;
      const typeSpeed = 50; // ms per character
      
      function typeWriter() {
        if (i < text.length) {
          command.textContent += text.charAt(i);
          i++;
          setTimeout(typeWriter, Math.random() * 100 + typeSpeed);
        }
      }
      
      typeWriter();
    }, delay);
  });
}

// Add parallax effect to cards on mouse move
function addCardParallaxEffect() {
  const cards = document.querySelectorAll('.repo-card, .post-item');
  
  cards.forEach(card => {
    card.addEventListener('mousemove', e => {
      // Get position of mouse in card
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left; // x position within the card
      const y = e.clientY - rect.top; // y position within the card
      
      // Calculate rotation based on mouse position
      // The multiplier affects the intensity of the effect
      const multiplier = 10;
      const rotateY = ((x / rect.width) - 0.5) * multiplier;
      const rotateX = ((y / rect.height) - 0.5) * -multiplier;
      
      // Apply the transform
      card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
      
      // Add a soft highlight effect where the mouse is
      const highlight = `radial-gradient(circle at ${x}px ${y}px, rgba(255,255,255,0.15), rgba(255,255,255,0) 100px)`;
      card.style.backgroundImage = highlight;
    });
    
    // Reset transforms when mouse leaves
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.backgroundImage = '';
      // Add a smooth transition back to normal
      card.style.transition = 'transform 0.5s ease-out, background-image 0.5s ease-out';
      
      // Remove the transition property after the animation completes
      setTimeout(() => {
        card.style.transition = '';
      }, 500);
    });
  });
}

// Add scroll reveal animations
function addScrollRevealAnimations() {
  const elementsToAnimate = document.querySelectorAll('.post-item, .repo-card, .terminal-box, h2, .github-pins, .recent-posts');
  
  // Create an Intersection Observer
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      // If the element is in the viewport
      if (entry.isIntersecting) {
        // Add a class to fade it in
        entry.target.classList.add('revealed');
        // Unobserve the element after it's been revealed
        observer.unobserve(entry.target);
      }
    });
  }, {
    root: null, // Use the viewport as the root
    threshold: 0.1, // Trigger when at least 10% of the element is visible
    rootMargin: '0px 0px -50px 0px' // Trigger a bit before the element enters the viewport
  });
  
  // Add a base class for the initial state and observe each element
  elementsToAnimate.forEach((element, index) => {
    // Add a staggered delay based on index
    element.style.transitionDelay = `${index * 0.1}s`;
    element.classList.add('scroll-reveal');
    observer.observe(element);
  });
}

// Progressive image loading
function addProgressiveImageLoading() {
  // Get all images that are not inline SVGs (they don't need lazy loading)
  const images = document.querySelectorAll('img:not([src^="data:image/svg"])');
  
  // Create an IntersectionObserver
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        
        // Only process images with data-src attribute
        const dataSrc = img.getAttribute('data-src');
        if (dataSrc) {
          // Create a new image to preload
          const newImg = new Image();
          
          // When the image is loaded, replace the src and remove the blur effect
          newImg.onload = function() {
            img.src = dataSrc;
            img.classList.add('img-loaded');
            img.removeAttribute('data-src');
          };
          
          // Start loading the image
          newImg.src = dataSrc;
          
          // Stop observing the image
          observer.unobserve(img);
        }
      }
    });
  }, {
    rootMargin: '50px 0px', // Load images a bit before they enter the viewport
    threshold: 0.1
  });
  
  // Observe all selected images
  images.forEach(img => {
    // Skip images that are already loaded
    if (!img.complete || img.naturalHeight === 0) {
      const currentSrc = img.getAttribute('src');
      
      // If the image has a src but no data-src, set it
      if (currentSrc && !img.hasAttribute('data-src')) {
        img.setAttribute('data-src', currentSrc);
        
        // Set a low-res placeholder or blur-up placeholder
        img.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150"%3E%3Crect width="300" height="150" fill="%23cccccc"%3E%3C/rect%3E%3C/svg%3E';
        
        // Add a loading class for blur effect
        img.classList.add('img-loading');
        
        // Observe the image
        imageObserver.observe(img);
      }
    }
  });
  
  // Process images that have already been loaded
  document.addEventListener('load', function() {
    const loadedImages = document.querySelectorAll('img.img-loading');
    loadedImages.forEach(img => {
      if (img.complete && img.naturalHeight !== 0) {
        img.classList.remove('img-loading');
        img.classList.add('img-loaded');
      }
    });
  }, true);
}
