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

  // Always use dark mode
  forceDarkMode();

  // Add progressive image loading
  addProgressiveImageLoading();
});


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

// Force dark mode
function forceDarkMode() {
  // Always use dark mode
  document.documentElement.classList.add('dark');
  localStorage.setItem('theme', 'dark');
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
  const elementsToAnimate = document.querySelectorAll('.repo-card, .about-me-section, .skill-item, h2, .github-pins');

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
          newImg.onload = function () {
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
  document.addEventListener('load', function () {
    const loadedImages = document.querySelectorAll('img.img-loading');
    loadedImages.forEach(img => {
      if (img.complete && img.naturalHeight !== 0) {
        img.classList.remove('img-loading');
        img.classList.add('img-loaded');
      }
    });
  }, true);
}
