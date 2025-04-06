/**
 * Site enhancement functionality
 * - Back to top button
 * - Image lazy loading
 * - Reading time estimation
 * - Animated page transitions
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
});

// Add page entrance animation after navigation
window.addEventListener('pageshow', (event) => {
  // Add transition class
  document.body.classList.add('page-transition-enter');
  
  // Remove after animation completes
  setTimeout(() => {
    document.body.classList.remove('page-transition-enter');
  }, 500);
});