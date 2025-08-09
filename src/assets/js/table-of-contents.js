/**
 * Table of Contents Generator
 * Automatically generates a floating table of contents for blog posts
 */

(function() {
  'use strict';

  /**
   * Initialize table of contents
   */
  function initTableOfContents() {
    // Only run on blog post pages
    const article = document.querySelector('article .prose');
    if (!article) return;

    // Find all headings (h2 and h3 only for cleaner TOC)
    const headings = article.querySelectorAll('h2, h3');
    
    // Only create TOC if we have enough headings
    if (headings.length < 3) return;

    // Create TOC container
    const tocContainer = document.createElement('aside');
    tocContainer.className = 'toc-container';
    tocContainer.setAttribute('aria-label', 'Table of contents');
    tocContainer.innerHTML = `
      <div class="toc-content">
        <h2 class="toc-title">On this page</h2>
        <nav class="toc-nav">
          <ul class="toc-list"></ul>
        </nav>
      </div>
    `;

    const tocList = tocContainer.querySelector('.toc-list');

    // Process headings and build TOC
    let currentH2Item = null;
    
    headings.forEach((heading, index) => {
      // Generate ID if not present
      if (!heading.id) {
        heading.id = 'heading-' + heading.textContent.toLowerCase()
          .replace(/[^\w\s-]/g, '') // Remove special chars
          .replace(/\s+/g, '-')      // Replace spaces with hyphens
          .replace(/-+/g, '-')       // Replace multiple hyphens with single
          .trim();
      }

      const listItem = document.createElement('li');
      const link = document.createElement('a');
      link.href = '#' + heading.id;
      link.textContent = heading.textContent;
      link.className = 'toc-link';
      
      if (heading.tagName === 'H2') {
        // Main section
        listItem.className = 'toc-item toc-item-h2';
        listItem.appendChild(link);
        tocList.appendChild(listItem);
        currentH2Item = listItem;
      } else if (heading.tagName === 'H3' && currentH2Item) {
        // Subsection
        listItem.className = 'toc-item toc-item-h3';
        
        // Create or get the nested list
        let nestedList = currentH2Item.querySelector('ul');
        if (!nestedList) {
          nestedList = document.createElement('ul');
          nestedList.className = 'toc-list toc-list-nested';
          currentH2Item.appendChild(nestedList);
        }
        
        listItem.appendChild(link);
        nestedList.appendChild(listItem);
      }
    });

    // Insert TOC into the page (for desktop only)
    const articleContainer = document.querySelector('.container .max-w-3xl');
    if (articleContainer && window.innerWidth >= 1280) {
      articleContainer.style.position = 'relative';
      articleContainer.appendChild(tocContainer);
    }

    // Smooth scroll behavior
    tocContainer.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const targetId = link.getAttribute('href').slice(1);
        const targetElement = document.getElementById(targetId);
        
        if (targetElement) {
          const offset = 100; // Account for sticky header
          const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });

    // Highlight current section on scroll
    let activeHeading = null;
    const observerOptions = {
      rootMargin: '-100px 0px -66% 0px',
      threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        const id = entry.target.id;
        const tocLink = tocContainer.querySelector(`a[href="#${id}"]`);
        
        if (entry.isIntersecting) {
          // Remove previous active states
          tocContainer.querySelectorAll('.toc-link-active').forEach(link => {
            link.classList.remove('toc-link-active');
          });
          
          // Add active state to current link
          if (tocLink) {
            tocLink.classList.add('toc-link-active');
            
            // Also highlight parent H2 if this is an H3
            const parentItem = tocLink.closest('.toc-item-h3')?.closest('.toc-item-h2');
            if (parentItem) {
              const parentLink = parentItem.querySelector('.toc-link');
              if (parentLink) {
                parentLink.classList.add('toc-link-active');
              }
            }
          }
        }
      });
    });

    // Observe all headings
    headings.forEach(heading => {
      observer.observe(heading);
    });

    // Handle responsive behavior
    function handleResize() {
      if (window.innerWidth < 1280 && tocContainer.parentElement) {
        tocContainer.remove();
      } else if (window.innerWidth >= 1280 && !tocContainer.parentElement && articleContainer) {
        articleContainer.appendChild(tocContainer);
      }
    }

    window.addEventListener('resize', handleResize);
  }

  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTableOfContents);
  } else {
    initTableOfContents();
  }
})();