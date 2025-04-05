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
  // Initialize search function if it exists
  const searchInput = document.getElementById('search-input');
  if (searchInput) {
    initSearch();
  }

  // Add scroll to top button
  addScrollToTopButton();

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

// Initialize search functionality
function initSearch() {
  const searchInput = document.getElementById('search-input');
  if (!searchInput) return;

  searchInput.addEventListener('input', function () {
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
  button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
    <path d="M3.22 9.78c-.293-.293-.293-.767 0-1.06l4.25-4.25a.75.75 0 011.06 0l4.25 4.25a.75.75 0 01-1.06 1.06L8 6.06 4.28 9.78c-.293.293-.767.293-1.06 0z"></path>
  </svg>`;
  button.className = 'scroll-top-btn';
  button.setAttribute('aria-label', 'Scroll to top');
  document.body.appendChild(button);

  // Show/hide button based on scroll position with throttling
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    if (scrollTimeout) {
      window.cancelAnimationFrame(scrollTimeout);
    }

    scrollTimeout = window.requestAnimationFrame(() => {
      if (window.pageYOffset > 300) {
        button.classList.add('visible');
      } else {
        button.classList.remove('visible');
      }
    });
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
}

// Force dark mode for GitHub style
function forceDarkMode() {
  document.documentElement.classList.add('dark');
  document.body.classList.add('dark-mode');
  
  // Store preference in localStorage
  localStorage.setItem('theme', 'dark');
}