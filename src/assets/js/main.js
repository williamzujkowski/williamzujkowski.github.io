/**
 * Main JavaScript for the website
 */

document.addEventListener('DOMContentLoaded', function () {
    // Mobile navigation toggle
    initMobileNav();

    // Add smooth scrolling for anchor links
    initSmoothScroll();

    // Handle dark/light mode toggle if added later
    // initThemeToggle();

    // Initialize code highlighting if Prism.js is available
    if (typeof Prism !== 'undefined') {
        Prism.highlightAll();
    }

    // Add active class to current navigation item
    highlightCurrentNavItem();

    // Handle forms with client-side validation
    setupFormValidation();

    // Initialize lazy loading for images
    initLazyLoading();

    // Log initialization for debugging
    console.log('Website initialized successfully');
});

/**
 * Initialize mobile navigation
 */
function initMobileNav() {
    const menuToggle = document.querySelector('.menu-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (!menuToggle || !siteNav) return;

    menuToggle.setAttribute('aria-expanded', 'false');

    menuToggle.addEventListener('click', function () {
        const isExpanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !isExpanded);

        // Handle body scroll
        document.body.classList.toggle('nav-open');

        // Trap focus within mobile menu when open
        if (!isExpanded) {
            trapFocus(siteNav);
        }
    });

    // Close menu when clicking outside
    document.addEventListener('click', function (event) {
        const isNavOpen = menuToggle.getAttribute('aria-expanded') === 'true';
        const clickedInsideNav = siteNav.contains(event.target);
        const clickedOnToggle = menuToggle.contains(event.target);

        if (isNavOpen && !clickedInsideNav && !clickedOnToggle) {
            menuToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('nav-open');
        }
    });

    // Close menu when ESC key is pressed
    document.addEventListener('keydown', function (event) {
        if (event.key === 'Escape' && menuToggle.getAttribute('aria-expanded') === 'true') {
            menuToggle.setAttribute('aria-expanded', 'false');
            document.body.classList.remove('nav-open');
            menuToggle.focus();
        }
    });

    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            if (window.innerWidth > 768 && menuToggle.getAttribute('aria-expanded') === 'true') {
                menuToggle.setAttribute('aria-expanded', 'false');
                document.body.classList.remove('nav-open');
            }
        }, 250);
    });
}

/**
 * Add smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                e.preventDefault();

                const headerOffset = 100;
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                try {
                    window.scrollTo({
                        top: offsetPosition,
                        behavior: 'smooth'
                    });

                    // Update URL hash
                    window.history.pushState(null, null, targetId);
                } catch (error) {
                    // Fallback for browsers that don't support smooth scrolling
                    window.scrollTo(0, offsetPosition);
                }
            }
        });
    });
}

/**
 * Trap focus within an element (for accessibility)
 */
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    // Set initial focus
    firstElement.focus();

    // Trap focus inside the element
    element.addEventListener('keydown', function (e) {
        if (e.key === 'Tab') {
            if (e.shiftKey && document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            } else if (!e.shiftKey && document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    });
}

/**
 * Highlight current navigation item based on URL
 */
function highlightCurrentNavItem() {
    const currentPath = window.location.pathname;
    const navItems = document.querySelectorAll('.nav-item');

    navItems.forEach(item => {
        const link = item.querySelector('a');
        if (!link) return;

        const href = link.getAttribute('href');

        // Check if the current path matches the nav item's href
        if (href === currentPath ||
            (href !== '/' && currentPath.startsWith(href)) ||
            (href === '/' && currentPath === '/')) {
            item.classList.add('active');
        } else {
            item.classList.remove('active');
        }
    });
}

/**
 * Setup form validation
 */
function setupFormValidation() {
    const forms = document.querySelectorAll('form[data-validate="true"]');

    forms.forEach(form => {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    e.preventDefault();
                    isValid = false;

                    // Add error class
                    field.classList.add('error');

                    // Create error message if it doesn't exist
                    let errorMessage = field.nextElementSibling;
                    if (!errorMessage || !errorMessage.classList.contains('error-message')) {
                        errorMessage = document.createElement('div');
                        errorMessage.classList.add('error-message');
                        errorMessage.textContent = 'This field is required';
                        field.parentNode.insertBefore(errorMessage, field.nextSibling);
                    }
                } else {
                    // Remove error class and message
                    field.classList.remove('error');
                    const errorMessage = field.nextElementSibling;
                    if (errorMessage && errorMessage.classList.contains('error-message')) {
                        errorMessage.remove();
                    }
                }
            });

            return isValid;
        });
    });
}

/**
 * Initialize lazy loading for images
 */
function initLazyLoading() {
    // Check if the browser supports native lazy loading
    if ('loading' in HTMLImageElement.prototype) {
        // Use native lazy loading
        const lazyImages = document.querySelectorAll('img.lazy');
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    } else {
        // Use intersection observer as fallback
        if ('IntersectionObserver' in window) {
            const lazyImageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const lazyImage = entry.target;
                        lazyImage.src = lazyImage.dataset.src;
                        lazyImage.classList.remove('lazy');
                        lazyImageObserver.unobserve(lazyImage);
                    }
                });
            });

            const lazyImages = document.querySelectorAll('img.lazy');
            lazyImages.forEach(lazyImage => {
                lazyImageObserver.observe(lazyImage);
            });
        } else {
            // Fallback for older browsers
            let lazyLoadThrottleTimeout;

            function lazyLoad() {
                const lazyImages = document.querySelectorAll('img.lazy');

                if (lazyLoadThrottleTimeout) {
                    clearTimeout(lazyLoadThrottleTimeout);
                }

                lazyLoadThrottleTimeout = setTimeout(() => {
                    const scrollTop = window.pageYOffset;

                    lazyImages.forEach(img => {
                        if (img.offsetTop < window.innerHeight + scrollTop) {
                            img.src = img.dataset.src;
                            img.classList.remove('lazy');
                        }
                    });

                    if (lazyImages.length === 0) {
                        document.removeEventListener('scroll', lazyLoad);
                        window.removeEventListener('resize', lazyLoad);
                        window.removeEventListener('orientationChange', lazyLoad);
                    }
                }, 20);
            }

            document.addEventListener('scroll', lazyLoad);
            window.addEventListener('resize', lazyLoad);
            window.addEventListener('orientationChange', lazyLoad);
        }
    }
}

/**
 * Handle errors gracefully
 */
window.addEventListener('error', function (e) {
    console.error('JavaScript error occurred:', e.message);
    // You can add additional error handling here, like logging to a service

    // Prevent the error from breaking the entire site
    return true;
});

/**
 * Add a simple console message for curious visitors
 */
console.log(`
  %c Welcome to my website! 🚀 
  %c Made with 11ty and hosted on GitHub Pages
  `,
    'font-size: 1.2em; font-weight: bold; color: #3b82f6;',
    'font-size: 1em; color: #6b7280;'
);