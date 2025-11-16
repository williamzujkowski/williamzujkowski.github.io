/**
 * SCROLL ANIMATIONS - INTERSECTION OBSERVER
 * GPU-accelerated animations for modern design system
 *
 * Features:
 * - Fade in elements on scroll
 * - Stagger animations with 50ms delay
 * - Respects prefers-reduced-motion
 * - Lazy loading support
 */

(function() {
  'use strict';

  // Check for reduced motion preference
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (prefersReducedMotion) {
    // Immediately show all elements, no animations
    document.querySelectorAll('[data-animate]').forEach(el => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
    return;
  }

  // Intersection Observer options
  const observerOptions = {
    root: null, // viewport
    rootMargin: '0px 0px -100px 0px', // Trigger 100px before entering viewport
    threshold: 0.1 // 10% visible
  };

  // Animation callback
  function handleIntersection(entries, observer) {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        const element = entry.target;
        const animationType = element.dataset.animate || 'fade-in';
        const delay = element.dataset.animationDelay || 0;

        // Add animation class with delay
        setTimeout(() => {
          element.classList.add('animate-' + animationType);
          element.classList.add('animated');
        }, parseInt(delay));

        // Unobserve after animation
        observer.unobserve(element);
      }
    });
  }

  // Create observer
  const observer = new IntersectionObserver(handleIntersection, observerOptions);

  // Observe all elements with data-animate attribute
  document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('[data-animate]');

    animatedElements.forEach((element, index) => {
      // Set initial state (hidden)
      element.style.opacity = '0';
      element.style.transform = 'translateY(20px)';
      element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';

      // Stagger animations: 50ms delay per element
      if (!element.dataset.animationDelay) {
        element.dataset.animationDelay = index * 50;
      }

      // Observe element
      observer.observe(element);
    });

    // Auto-add data-animate to common elements
    const autoAnimateSelectors = [
      'article.post-preview',
      '.feature-card',
      '.what-i-do dl > div',
      'section > h2',
    ];

    autoAnimateSelectors.forEach(selector => {
      const elements = document.querySelectorAll(selector);
      elements.forEach((el, idx) => {
        if (!el.hasAttribute('data-animate')) {
          el.setAttribute('data-animate', 'fade-in-up');
          el.style.opacity = '0';
          el.style.transform = 'translateY(20px)';
          el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
          el.dataset.animationDelay = idx * 50;
          observer.observe(el);
        }
      });
    });
  });

  // Define animation end states
  const style = document.createElement('style');
  style.textContent = `
    .animate-fade-in.animated,
    .animate-fade-in-up.animated {
      opacity: 1 !important;
      transform: translateY(0) !important;
    }

    .animate-fade-in-left.animated {
      opacity: 1 !important;
      transform: translateX(0) !important;
    }

    .animate-fade-in-right.animated {
      opacity: 1 !important;
      transform: translateX(0) !important;
    }

    .animate-scale.animated {
      opacity: 1 !important;
      transform: scale(1) !important;
    }

    /* Parallax effect for hero image */
    .parallax-image {
      will-change: transform;
      transition: transform 0.1s ease-out;
    }

    @media (prefers-reduced-motion: reduce) {
      .parallax-image {
        transform: none !important;
      }
    }
  `;
  document.head.appendChild(style);

  // Parallax scroll effect (enhanced for hero image)
  let ticking = false;

  function handleParallax() {
    const parallaxElements = document.querySelectorAll('.parallax-image');
    const scrolled = window.pageYOffset;

    parallaxElements.forEach(el => {
      const speed = parseFloat(el.dataset.parallaxSpeed) || 0.3;
      const yPos = -(scrolled * speed);

      // Only apply parallax if element is in viewport
      const rect = el.getBoundingClientRect();
      const isInViewport = rect.top < window.innerHeight && rect.bottom > 0;

      if (isInViewport) {
        el.style.transform = `translateY(${yPos}px) scale(1.05)`;
      }
    });

    ticking = false;
  }

  function requestParallaxTick() {
    if (!ticking && !prefersReducedMotion) {
      requestAnimationFrame(handleParallax);
      ticking = true;
    }
  }

  // Throttled scroll listener for parallax
  window.addEventListener('scroll', requestParallaxTick, { passive: true });

  // Add parallax class to hero image automatically
  document.addEventListener('DOMContentLoaded', () => {
    const heroImages = document.querySelectorAll('.hero img, .profile-image img');
    heroImages.forEach(img => {
      if (!img.classList.contains('parallax-image')) {
        img.classList.add('parallax-image');
        img.dataset.parallaxSpeed = '0.3';
      }
    });
  });

})();
