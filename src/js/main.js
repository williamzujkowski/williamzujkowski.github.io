/**
 * main.js - Optimized primary JavaScript functionality
 * Core website initialization and features
 */

// Create and append page loader inline in HTML to avoid flash
document.write(`
  <div class="page-loader" id="page-loader">
    <div class="loader-spinner"></div>
    <div class="loader-text">Loading...</div>
  </div>
`);

// Use requestIdleCallback with fallback for non-critical operations
const requestIdleCallback = window.requestIdleCallback || 
  ((cb) => {
    const start = Date.now();
    return setTimeout(() => {
      cb({
        didTimeout: false,
        timeRemaining: () => Math.max(0, 50 - (Date.now() - start))
      });
    }, 1);
  });

// Queue for prioritizing animations
const animationQueue = [];

// Hide loader when page is fully loaded - high priority
window.addEventListener('load', () => {
  const pageLoader = document.getElementById('page-loader');
  if (pageLoader) {
    pageLoader.classList.add('page-loader-hidden');
    setTimeout(() => pageLoader.remove(), 500);
  }
});

// Ready state detection - high priority
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initHighPriority);
} else {
  initHighPriority();
}

// High priority functions to run immediately
function initHighPriority() {
  // Force dark mode
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark-mode');
  localStorage.setItem('theme', 'dark');
  
  // Add skip link for accessibility
  const skipLink = document.createElement('a');
  skipLink.href = '#main-content';
  skipLink.className = 'skip-link';
  skipLink.textContent = 'Skip to content';
  document.body.prepend(skipLink);

  // Schedule medium priority tasks
  requestAnimationFrame(() => {
    // Setup main content for accessibility
    const mainContent = document.querySelector('main');
    if (mainContent) {
      mainContent.id = 'main-content';
      mainContent.setAttribute('tabindex', '-1');
    }
    
    // Schedule lower priority tasks
    requestIdleCallback(initLowPriority);
  });
}

// Low priority functions to run when idle
function initLowPriority() {
  // Add aria attributes to navigation
  const navItems = document.querySelectorAll('nav a');
  navItems.forEach(item => {
    if (window.location.pathname === item.getAttribute('href')) {
      item.setAttribute('aria-current', 'page');
    }
  });
  
  // Queue animations for visible elements only
  addOptimizedAnimations();
}

// Add optimized animations only to visible elements
function addOptimizedAnimations() {
  // Only animate elements in viewport
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          animateElement(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, {
      rootMargin: '50px',
      threshold: 0.1
    });
    
    // Elements to animate on page load
    const elementsToAnimate = [
      '.gh-profile-header',
      '.gh-section-header',
      '.gh-post-item'
    ];
    
    // Observe elements
    elementsToAnimate.forEach(selector => {
      document.querySelectorAll(selector).forEach(el => {
        observer.observe(el);
      });
    });
  } else {
    // Fallback for browsers without IntersectionObserver
    // Use basic animation with reduced delays
    animateFallback();
  }
}

// Animate a specific element
function animateElement(el, index = 0) {
  el.style.opacity = '0';
  el.style.animation = `fadeIn 0.6s ease-out forwards, slideUp 0.6s ease-out forwards`;
  el.style.animationDelay = `${0.05 + (index * 0.05)}s`;
}

// Fallback animation method
function animateFallback() {
  const elementsToAnimate = [
    '.gh-profile-header',
    '.gh-section-header',
    '.gh-post-item'
  ];
  
  elementsToAnimate.forEach(selector => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.animation = `fadeIn 0.5s ease-out forwards, slideUp 0.5s ease-out forwards`;
      el.style.animationDelay = `${0.05 + (i * 0.05)}s`;
    });
  });
}