/**
 * Basic search functionality for blog posts
 * Using a simple keyword matching approach
 */

document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const searchResults = document.getElementById('search-results');
  const searchCountElement = document.getElementById('search-results-count');
  const searchableElements = document.querySelectorAll('.searchable');
  const noResultsMessage = document.getElementById('no-results-message');
  
  if (!searchInput || !searchableElements.length) return;
  
  let postsData = [];
  
  // Extract post data from DOM for search
  searchableElements.forEach(element => {
    const title = element.querySelector('.gh-post-title')?.textContent || '';
    const excerpt = element.querySelector('.gh-post-excerpt')?.textContent || '';
    const tags = element.dataset.tags || '';
    const url = element.querySelector('.gh-post-title')?.getAttribute('href') || '';
    
    postsData.push({
      element,
      title: title.toLowerCase(),
      excerpt: excerpt.toLowerCase(),
      tags: tags.toLowerCase(),
      url
    });
  });
  
  // Search function
  function performSearch(query) {
    query = query.toLowerCase().trim();
    let visibleCount = 0;
    
    if (searchCountElement) {
      searchCountElement.parentElement.classList.add('searching');
    }
    
    postsData.forEach(post => {
      const matchesTitle = post.title.includes(query);
      const matchesExcerpt = post.excerpt.includes(query);
      const matchesTags = post.tags.includes(query);
      
      if (query === '' || matchesTitle || matchesExcerpt || matchesTags) {
        post.element.style.display = '';
        applyFadeIn(post.element);
        visibleCount++;
        
        // Highlight matching text
        if (query !== '') {
          highlightMatches(post, query);
        } else {
          removeHighlights(post);
        }
      } else {
        post.element.style.display = 'none';
      }
    });
    
    // Update search count
    if (searchCountElement) {
      searchCountElement.textContent = visibleCount;
      searchCountElement.parentElement.classList.remove('searching');
    }
    
    // Show/hide no results message
    if (noResultsMessage) {
      if (visibleCount === 0 && query !== '') {
        noResultsMessage.classList.remove('hidden');
        noResultsMessage.style.opacity = '0';
        setTimeout(() => {
          noResultsMessage.style.opacity = '1';
        }, 10);
      } else {
        noResultsMessage.classList.add('hidden');
      }
    }
  }
  
  // Highlight matching text in search results
  function highlightMatches(post, query) {
    const excerptElement = post.element.querySelector('.gh-post-excerpt');
    if (!excerptElement) return;
    
    const excerptText = excerptElement.textContent;
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    excerptElement.innerHTML = excerptText.replace(
      regex, 
      '<mark class="bg-accent/20 text-white px-1 rounded">$1</mark>'
    );
  }
  
  // Remove highlights
  function removeHighlights(post) {
    const excerptElement = post.element.querySelector('.gh-post-excerpt');
    if (!excerptElement) return;
    
    if (excerptElement.innerHTML.includes('<mark')) {
      excerptElement.textContent = excerptElement.textContent;
    }
  }
  
  // Add fade-in animation
  function applyFadeIn(element) {
    element.style.opacity = '0';
    element.style.transform = 'translateY(10px)';
    
    setTimeout(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
      element.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
    }, 10);
  }
  
  // Escape special characters for regex
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  // Debounce function to limit how often search is performed
  function debounce(func, wait) {
    let timeout;
    return function(...args) {
      clearTimeout(timeout);
      timeout = setTimeout(() => func.apply(this, args), wait);
    };
  }
  
  // Event listener for search input with debounce
  searchInput.addEventListener('input', debounce(function() {
    performSearch(this.value);
  }, 300));
  
  // Reset search if there's a reset button
  const resetButton = document.getElementById('reset-search');
  if (resetButton) {
    resetButton.addEventListener('click', function() {
      searchInput.value = '';
      performSearch('');
      searchInput.focus();
    });
  }
});