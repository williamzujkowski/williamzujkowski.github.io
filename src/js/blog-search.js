/**
 * Blog search, filtering, and animation functionality
 */
document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('search-input');
  const resetButton = document.getElementById('reset-search');
  const clearFiltersBtn = document.getElementById('clear-filters');
  const noResultsMessage = document.getElementById('no-results-message');
  const resultCount = document.getElementById('search-results-count');
  const searchableElements = document.querySelectorAll('.searchable');
  const tagButtons = document.querySelectorAll('.tag-btn');
  const postGrid = document.querySelector('.grid');
  
  // Add animation classes to posts for staggered entrance
  searchableElements.forEach((element, index) => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    
    // Stagger the animations
    setTimeout(() => {
      element.style.opacity = '1';
      element.style.transform = 'translateY(0)';
    }, 100 + (index * 70));
  });
  
  // Enhanced search function that checks title, content, and tags
  function performSearch(query) {
    query = query.toLowerCase().trim();
    let visibleCount = 0;
    
    // Add a transition effect to grid
    if (postGrid) {
      postGrid.classList.add('searching');
    }
    
    setTimeout(() => {
      searchableElements.forEach(element => {
        const title = element.querySelector('.gh-post-title').textContent.toLowerCase();
        const content = element.querySelector('.gh-post-excerpt')?.textContent.toLowerCase() || '';
        const tags = element.dataset.tags?.toLowerCase() || '';
        
        // Search in title, content, and tags
        if (title.includes(query) || content.includes(query) || tags.includes(query) || query === '') {
          element.style.display = '';
          visibleCount++;
          
          // Highlight matching text if there's a query
          if (query !== '') {
            highlightText(element, query);
          } else {
            removeHighlights(element);
          }
          
          // Add a fade-in animation with staggering
          element.style.opacity = '0';
          element.style.transform = 'translateY(10px)';
          
          setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
          }, 50 + (visibleCount * 30));
          
        } else {
          element.style.display = 'none';
        }
      });
      
      // Update count and show/hide no results message
      if (resultCount) resultCount.textContent = visibleCount;
      if (visibleCount === 0 && query !== '') {
        if (noResultsMessage) noResultsMessage.classList.remove('hidden');
        if (noResultsMessage) noResultsMessage.style.opacity = '0';
        setTimeout(() => {
          if (noResultsMessage) noResultsMessage.style.opacity = '1';
        }, 50);
      } else {
        if (noResultsMessage) noResultsMessage.classList.add('hidden');
      }
      
      // Remove transition class
      if (postGrid) {
        setTimeout(() => {
          postGrid.classList.remove('searching');
        }, 300);
      }
    }, 200);
  }
  
  // Highlight matching text
  function highlightText(element, query) {
    // First remove any existing highlights
    removeHighlights(element);
    
    // Only highlight in the excerpt to avoid changing the title
    const excerpt = element.querySelector('.gh-post-excerpt');
    if (!excerpt) return;
    
    const content = excerpt.textContent;
    const regex = new RegExp(`(${escapeRegExp(query)})`, 'gi');
    excerpt.innerHTML = content.replace(regex, '<mark class="gh-search-highlight">$1</mark>');
  }
  
  // Remove highlights
  function removeHighlights(element) {
    const excerpt = element.querySelector('.gh-post-excerpt');
    if (!excerpt) return;
    
    const markedContent = excerpt.innerHTML;
    if (markedContent.includes('<mark')) {
      const content = excerpt.textContent;
      excerpt.innerHTML = content;
    }
  }
  
  // Escape regex special characters
  function escapeRegExp(string) {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
  
  // Reset all filters
  function resetAllFilters() {
    if (!searchInput) return;
    searchInput.value = '';
    performSearch('');
    
    // Reset tag buttons
    if (tagButtons) {
      tagButtons.forEach(btn => {
        if (btn.dataset.tag === '') {
          btn.classList.add('selected');
        } else {
          btn.classList.remove('selected');
        }
      });
    }
    
    // Add a subtle animation to the grid
    if (postGrid) {
      postGrid.classList.add('reset-animation');
      setTimeout(() => {
        postGrid.classList.remove('reset-animation');
      }, 500);
    }
  }
  
  // Search input event with debounce
  let debounceTimeout;
  if (searchInput) {
    searchInput.addEventListener('input', function() {
      clearTimeout(debounceTimeout);
      debounceTimeout = setTimeout(() => {
        performSearch(this.value);
        
        // Reset tag buttons if search is empty
        if (this.value === '' && tagButtons) {
          tagButtons.forEach(btn => {
            if (btn.dataset.tag === '') {
              btn.classList.add('selected');
            } else {
              btn.classList.remove('selected');
            }
          });
        }
      }, 300); // 300ms debounce
    });
  }
  
  // Reset search button in no results message
  if (resetButton) {
    resetButton.addEventListener('click', function() {
      resetAllFilters();
      // Focus on search input
      if (searchInput) searchInput.focus();
    });
  }
  
  // Clear filters button
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener('click', function() {
      resetAllFilters();
      
      // Add animation to the button
      this.classList.add('active');
      setTimeout(() => {
        this.classList.remove('active');
      }, 300);
    });
  }
  
  // Tag buttons
  if (tagButtons && tagButtons.length > 0) {
    tagButtons.forEach(button => {
      button.addEventListener('click', function() {
        const tag = this.dataset.tag;
        
        // Add a pulse animation to the clicked tag
        this.classList.add('pulse-animation');
        setTimeout(() => this.classList.remove('pulse-animation'), 500);
        
        // Update search input and perform search
        if (searchInput) {
          if (tag === '') {
            searchInput.value = '';
            performSearch('');
          } else {
            searchInput.value = tag;
            performSearch(tag);
          }
        }
        
        // Add selected class to the clicked tag
        if (tagButtons) {
          tagButtons.forEach(btn => btn.classList.remove('selected'));
          this.classList.add('selected');
        }
      });
    });
  }
});