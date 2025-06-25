// Search functionality for blog posts
(function() {
    'use strict';
    
    // Wait for DOM to be ready
    document.addEventListener('DOMContentLoaded', function() {
        const searchInput = document.getElementById('search-input');
        const searchResults = document.getElementById('search-results');
        const searchClear = document.getElementById('search-clear');
        const postsContainer = document.getElementById('posts-container');
        
        if (!searchInput || !postsContainer) return;
        
        // Get all posts data
        const posts = Array.from(postsContainer.querySelectorAll('article[data-search]')).map(article => {
            return {
                element: article,
                title: article.getAttribute('data-title') || '',
                description: article.getAttribute('data-description') || '',
                tags: article.getAttribute('data-tags') || '',
                date: article.getAttribute('data-date') || '',
                content: article.getAttribute('data-search') || ''
            };
        });
        
        // Search function
        function performSearch(query) {
            if (!query || query.length < 2) {
                showAllPosts();
                hideSearchResults();
                return;
            }
            
            const searchTerms = query.toLowerCase().split(' ').filter(term => term.length > 0);
            const results = [];
            
            posts.forEach(post => {
                const searchableText = `${post.title} ${post.description} ${post.tags} ${post.content}`.toLowerCase();
                let score = 0;
                
                searchTerms.forEach(term => {
                    // Title matches are worth more
                    if (post.title.toLowerCase().includes(term)) {
                        score += 10;
                    }
                    // Description matches
                    if (post.description.toLowerCase().includes(term)) {
                        score += 5;
                    }
                    // Tag matches
                    if (post.tags.toLowerCase().includes(term)) {
                        score += 3;
                    }
                    // Content matches
                    if (post.content.toLowerCase().includes(term)) {
                        score += 1;
                    }
                });
                
                if (score > 0) {
                    results.push({ post, score });
                }
            });
            
            // Sort by score
            results.sort((a, b) => b.score - a.score);
            
            // Display results
            displaySearchResults(results, query);
        }
        
        // Display search results
        function displaySearchResults(results, query) {
            if (results.length === 0) {
                showNoResults(query);
                return;
            }
            
            // Hide all posts first
            posts.forEach(post => {
                post.element.style.display = 'none';
                post.element.classList.remove('search-highlight');
            });
            
            // Show matching posts
            results.forEach(({ post }) => {
                post.element.style.display = 'block';
                post.element.classList.add('search-highlight');
            });
            
            // Update results count
            if (searchResults) {
                searchResults.innerHTML = `
                    <div class="mb-6 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                        <p class="text-sm text-gray-700 dark:text-gray-300">
                            Found <strong>${results.length}</strong> ${results.length === 1 ? 'post' : 'posts'} matching 
                            "<strong>${escapeHtml(query)}</strong>"
                        </p>
                    </div>
                `;
                searchResults.style.display = 'block';
            }
        }
        
        // Show no results message
        function showNoResults(query) {
            posts.forEach(post => {
                post.element.style.display = 'none';
            });
            
            if (searchResults) {
                searchResults.innerHTML = `
                    <div class="mb-6 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg">
                        <p class="text-sm text-gray-700 dark:text-gray-300">
                            No posts found matching "<strong>${escapeHtml(query)}</strong>"
                        </p>
                        <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
                            Try different keywords or browse all posts below
                        </p>
                    </div>
                `;
                searchResults.style.display = 'block';
            }
        }
        
        // Show all posts
        function showAllPosts() {
            posts.forEach(post => {
                post.element.style.display = 'block';
                post.element.classList.remove('search-highlight');
            });
        }
        
        // Hide search results
        function hideSearchResults() {
            if (searchResults) {
                searchResults.style.display = 'none';
                searchResults.innerHTML = '';
            }
            if (searchClear) {
                searchClear.style.display = 'none';
            }
        }
        
        // Escape HTML
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Debounce function
        function debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        }
        
        // Event listeners
        const debouncedSearch = debounce(performSearch, 300);
        
        searchInput.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            debouncedSearch(query);
            
            // Show/hide clear button
            if (searchClear) {
                searchClear.style.display = query.length > 0 ? 'block' : 'none';
            }
        });
        
        // Clear search
        if (searchClear) {
            searchClear.addEventListener('click', function() {
                searchInput.value = '';
                showAllPosts();
                hideSearchResults();
                searchInput.focus();
            });
        }
        
        // Handle direct navigation with search query
        const urlParams = new URLSearchParams(window.location.search);
        const searchQuery = urlParams.get('q');
        if (searchQuery) {
            searchInput.value = searchQuery;
            performSearch(searchQuery);
        }
    });
})();