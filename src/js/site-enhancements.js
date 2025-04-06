/**
 * Site enhancement functionality
 * - Back to top button
 * - Image lazy loading
 * - Reading time estimation
 * - Animated page transitions
 * - Tailwind utility features
 * - Social media toggling
 */

document.addEventListener('DOMContentLoaded', () => {
  // Back to top button functionality
  const backToTopButton = document.getElementById('back-to-top');
  
  if (backToTopButton) {
    // Initially hide the button
    backToTopButton.classList.add('hidden');
    
    // Show/hide the button based on scroll position
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        backToTopButton.classList.remove('hidden');
        backToTopButton.classList.add('visible');
      } else {
        backToTopButton.classList.remove('visible');
        backToTopButton.classList.add('hidden');
      }
    });
    
    // Scroll to top when clicked
    backToTopButton.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  }
  
  // Image lazy loading with IntersectionObserver
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
  
  // Calculate and display reading time for blog posts
  const articleContent = document.querySelector('.prose');
  const readingTimeElement = document.getElementById('reading-time');
  
  if (articleContent && readingTimeElement) {
    const text = articleContent.textContent;
    const wordCount = text.split(/\s+/).length;
    const readingTime = Math.ceil(wordCount / 200); // 200 words per minute
    
    readingTimeElement.textContent = `${readingTime} min read`;
    readingTimeElement.classList.remove('hidden');
  }
  
  // Smooth page transitions
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
  
  // Add entrance animation when page loads
  document.body.classList.add('page-transition-enter');
  
  // Add tooltip functionality using Tailwind classes
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
  
  // Add focus-visible improvements for keyboard navigation
  document.querySelectorAll('a, button, input, select, textarea').forEach(element => {
    if (!element.classList.contains('focus-handled')) {
      element.classList.add('focus:outline-none', 'focus-visible:ring-2', 'focus-visible:ring-accent', 'focus-visible:ring-offset-1', 'focus-visible:ring-offset-background', 'focus-handled');
    }
  });
});

// Since disabled social media icons are now completely hidden in the template,
// we no longer need the JavaScript toggle functionality here

// Add page entrance animation after navigation
window.addEventListener('pageshow', (event) => {
  // Add transition class
  document.body.classList.add('page-transition-enter');
  
  // Remove after animation completes
  setTimeout(() => {
    document.body.classList.remove('page-transition-enter');
  }, 500);
});