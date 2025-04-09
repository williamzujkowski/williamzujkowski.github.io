/**
 * site-enhancements.js - Additional UI enhancing functionality
 *
 * Features:
 * - Back to top button
 * - Image lazy loading
 * - Reading time estimation
 * - Animated page transitions
 * - Tooltip functionality
 * - Focus management for accessibility
 */

document.addEventListener('DOMContentLoaded', () => {
  // Implement back to top button
  initScrollToTopButton();
  
  // Image lazy loading with IntersectionObserver
  initLazyLoading();
  
  // Calculate and display reading time for blog posts
  calculateReadingTime();
  
  // Add smooth page transitions
  initPageTransitions();
  
  // Add tooltip functionality
  initTooltips();
  
  // Add accessibility focus improvements
  enhanceAccessibility();
  
  // Add entrance animation when page loads
  document.body.classList.add('page-transition-enter');
});

/**
 * Initialize back-to-top button functionality
 */
function initScrollToTopButton() {
  // First try to find an existing button in the DOM
  let button = document.getElementById('back-to-top');
  
  // If no button exists, create it
  if (!button) {
    button = document.createElement('button');
    button.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
      <path d="M3.22 9.78c-.293-.293-.293-.767 0-1.06l4.25-4.25a.75.75 0 011.06 0l4.25 4.25a.75.75 0 01-1.06 1.06L8 6.06 4.28 9.78c-.293.293-.767.293-1.06 0z"></path>
    </svg>`;
    button.className = 'scroll-top-btn';
    button.id = 'back-to-top';
    button.setAttribute('aria-label', 'Scroll to top');
    document.body.appendChild(button);
  }

  // Initially hide the button
  button.classList.add('hidden');
  
  // Show/hide button based on scroll position with throttling
  let scrollTimeout;
  window.addEventListener('scroll', () => {
    if (scrollTimeout) {
      window.cancelAnimationFrame(scrollTimeout);
    }

    scrollTimeout = window.requestAnimationFrame(() => {
      if (window.pageYOffset > 300) {
        button.classList.remove('hidden');
        button.classList.add('visible');
      } else {
        button.classList.remove('visible');
        button.classList.add('hidden');
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

/**
 * Initialize lazy loading for images
 */
function initLazyLoading() {
  if ('IntersectionObserver' in window) {
    const lazyImageObserver = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const lazyImage = entry.target;
          
          // If it has a data-src attribute, set the src to that value
          if (lazyImage.dataset.src) {
            lazyImage.src = lazyImage.dataset.src;
            lazyImage.removeAttribute('data-src');
          }
          
          // If it has a data-srcset attribute, set the srcset to that value
          if (lazyImage.dataset.srcset) {
            lazyImage.srcset = lazyImage.dataset.srcset;
            lazyImage.removeAttribute('data-srcset');
          }
          
          lazyImage.classList.add('loaded');
          lazyImageObserver.unobserve(lazyImage);
        }
      });
    });
    
    // Observe all images with data-src attribute
    document.querySelectorAll('img[data-src]').forEach((img) => {
      lazyImageObserver.observe(img);
    });
  } else {
    // Fallback for browsers that don't support IntersectionObserver
    document.querySelectorAll('img[data-src]').forEach((img) => {
      img.src = img.dataset.src;
      img.removeAttribute('data-src');
      if (img.dataset.srcset) {
        img.srcset = img.dataset.srcset;
        img.removeAttribute('data-srcset');
      }
    });
  }
}

/**
 * Calculate and display reading time for blog posts
 */
function calculateReadingTime() {
  const articleContent = document.querySelector('.prose');
  const readingTimeElement = document.getElementById('reading-time');
  
  if (articleContent && readingTimeElement) {
    const text = articleContent.textContent;
    const wordCount = text.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute
    
    readingTimeElement.textContent = `${readingTime} min read`;
    readingTimeElement.classList.remove('hidden');
  }
}

/**
 * Add smooth page transitions for internal links
 */
function initPageTransitions() {
  document.querySelectorAll('a[href^="/"]:not([href^="#"]):not([target="_blank"])').forEach(link => {
    link.addEventListener('click', e => {
      // Only process internal links
      if (link.hostname === window.location.hostname) {
        e.preventDefault();
        const destination = link.href;
        
        // Add exit animation class to body
        document.body.classList.add('page-transition-exit');
        
        // Navigate after transition
        setTimeout(() => {
          window.location.href = destination;
        }, 300);
      }
    });
  });
}

/**
 * Initialize tooltips for elements with data-tooltip attribute
 */
function initTooltips() {
  document.querySelectorAll('[data-tooltip]').forEach(element => {
    // Create tooltip element
    const tooltip = document.createElement('div');
    tooltip.className = 'absolute z-50 p-2 bg-gray-light text-text text-xs rounded-github border border-border shadow-md opacity-0 transition-opacity duration-200 pointer-events-none -translate-y-full -mt-1 left-1/2 -translate-x-1/2';
    tooltip.textContent = element.getAttribute('data-tooltip');
    element.classList.add('relative');
    
    // Add tooltip to DOM
    element.appendChild(tooltip);
    
    // Show tooltip on hover
    element.addEventListener('mouseenter', () => {
      tooltip.classList.remove('opacity-0');
      tooltip.classList.add('opacity-100');
    });
    
    // Hide tooltip when not hovering
    element.addEventListener('mouseleave', () => {
      tooltip.classList.remove('opacity-100');
      tooltip.classList.add('opacity-0');
    });
  });
}

/**
 * Enhance accessibility with better focus states
 */
function enhanceAccessibility() {
  document.querySelectorAll('a, button, input, select, textarea').forEach(element => {
    if (!element.classList.contains('focus-handled')) {
      element.classList.add(
        'focus:outline-none', 
        'focus-visible:ring-2', 
        'focus-visible:ring-accent', 
        'focus-visible:ring-offset-1', 
        'focus-visible:ring-offset-background', 
        'focus-handled'
      );
    }
  });
}

// Add page entrance animation after navigation
window.addEventListener('pageshow', (event) => {
  // Add transition class
  document.body.classList.add('page-transition-enter');
  
  // Remove after animation completes
  setTimeout(() => {
    document.body.classList.remove('page-transition-enter');
  }, 500);
});