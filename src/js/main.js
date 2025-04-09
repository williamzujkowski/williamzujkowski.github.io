/**
 * main.js - Primary JavaScript functionality
 * Core website initialization and features
 */

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
  // Add keyboard navigation for accessibility
  addKeyboardNavigation();

  // Force dark mode
  forceDarkMode();
  
  // Add animations to page elements
  addPageAnimations();
});

// Add staggered animations to page elements
function addPageAnimations() {
  // Elements to animate on page load
  const elementsToAnimate = [
    '.gh-profile-header',
    '.gh-pinned-repos h2',
    '.gh-repo-card',
    '.gh-section-header',
    '.gh-post-item'
  ];
  
  // Apply animations with staggered delay
  elementsToAnimate.forEach((selector, index) => {
    const elements = document.querySelectorAll(selector);
    elements.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.animation = `fadeIn 0.6s ease-out forwards, slideUp 0.6s ease-out forwards`;
      el.style.animationDelay = `${0.1 + (index * 0.1) + (i * 0.05)}s`;
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
}

// Force dark mode for GitHub style
function forceDarkMode() {
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark-mode');
  
  // Store preference in localStorage
  localStorage.setItem('theme', 'dark');
}