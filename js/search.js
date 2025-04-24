/**
 * search.js - Search functionality for the site
 * Simplified non-module version
 */

(function () {
  // DOM elements
  let searchInput;
  let searchResults;
  let searchResultsContainer;
  let searchResultsList;
  let searchOverlay;
  let closeSearchButton;
  let searchButton;
  let searchForm;

  // State
  let posts = [];
  let isSearchActive = false;
  let isLoading = false;

  /**
   * Initialize search functionality when DOM is ready
   */
  function init() {
    // Get DOM elements
    searchInput = document.getElementById("search-input");
    searchResults = document.getElementById("search-results");
    searchResultsContainer = document.getElementById("search-results-container");
    searchResultsList = document.getElementById("search-results-list");
    searchOverlay = document.getElementById("search-overlay");
    closeSearchButton = document.getElementById("close-search");
    searchButton = document.getElementById("search-button");
    searchForm = document.getElementById("search-form");

    // Exit if search is not available on this page
    if (!searchInput || !searchResults) return;

    // Set up event listeners
    searchInput.addEventListener("input", handleSearchInput);
    searchForm?.addEventListener("submit", handleSearchSubmit);
    closeSearchButton?.addEventListener("click", closeSearch);
    searchButton?.addEventListener("click", openSearch);
    searchOverlay?.addEventListener("click", closeSearch);

    document.addEventListener("keydown", function (e) {
      // Close search on Escape key
      if (e.key === "Escape" && isSearchActive) {
        closeSearch();
      }

      // Open search on / key (if not in an input)
      if (
        e.key === "/" &&
        !isSearchActive &&
        !["INPUT", "TEXTAREA"].includes(document.activeElement.tagName)
      ) {
        e.preventDefault();
        openSearch();
      }
    });

    // Load posts data
    fetchPosts();
  }

  /**
   * Fetch all posts for search
   */
  function fetchPosts() {
    isLoading = true;

    // Check if we already have posts in localStorage
    const cachedPosts = localStorage.getItem("blog_posts");
    if (cachedPosts) {
      try {
        posts = JSON.parse(cachedPosts);
        isLoading = false;
        return;
      } catch (e) {
        console.error("Error parsing cached posts:", e);
      }
    }

    // If no cached posts or parse error, fetch from the index
    fetch("/search-index.json")
      .then((response) => {
        if (!response.ok) throw new Error("Network response was not ok");
        return response.json();
      })
      .then((data) => {
        posts = data;
        isLoading = false;
        // Cache posts
        try {
          localStorage.setItem("blog_posts", JSON.stringify(posts));
        } catch (e) {
          console.error("Error caching posts:", e);
        }
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
        isLoading = false;
      });
  }

  /**
   * Handle search input
   */
  function handleSearchInput(e) {
    const query = e.target.value.trim().toLowerCase();

    if (query.length < 2) {
      clearResults();
      return;
    }

    const results = searchPosts(query);
    displayResults(results, query);
  }

  /**
   * Handle search form submission
   */
  function handleSearchSubmit(e) {
    e.preventDefault();
    const query = searchInput.value.trim();

    if (query.length < 2) return;

    const results = searchPosts(query);
    displayResults(results, query);
  }

  /**
   * Search posts by query
   */
  function searchPosts(query) {
    if (isLoading || !posts.length) return [];

    // Simple search implementation
    return posts.filter((post) => {
      const titleMatch = post.title.toLowerCase().includes(query);
      const contentMatch = post.content.toLowerCase().includes(query);
      const tagMatch =
        post.tags?.some((tag) => tag.toLowerCase().includes(query)) || false;

      return titleMatch || contentMatch || tagMatch;
    });
  }

  /**
   * Display search results
   */
  function displayResults(results, query) {
    clearResults();

    if (results.length === 0) {
      const noResults = document.createElement("li");
      noResults.className = "p-4 text-center text-text-secondary";
      noResults.textContent = `No results found for "${query}"`;
      searchResultsList.appendChild(noResults);
      return;
    }

    // Display each result
    results.forEach((post) => {
      const li = document.createElement("li");
      li.className = "border-b border-border last:border-0";

      const link = document.createElement("a");
      link.href = post.url;
      link.className = "block p-4 hover:bg-surface transition-colors duration-200";

      const title = document.createElement("h3");
      title.className = "text-base font-medium text-text mb-1";
      title.textContent = post.title;

      const date = document.createElement("span");
      date.className = "text-xs text-text-secondary block mb-2";
      date.textContent = new Date(post.date).toLocaleDateString();

      const excerpt = document.createElement("p");
      excerpt.className = "text-sm text-text-secondary";

      // Create excerpt by finding the query in the content
      const contentLower = post.content.toLowerCase();
      const queryIndex = contentLower.indexOf(query.toLowerCase());
      if (queryIndex !== -1) {
        const start = Math.max(0, queryIndex - 40);
        const end = Math.min(post.content.length, queryIndex + query.length + 40);
        let excerptText = post.content.substring(start, end);

        if (start > 0) excerptText = "..." + excerptText;
        if (end < post.content.length) excerptText += "...";

        excerpt.textContent = excerptText;
      } else {
        excerpt.textContent = post.content.substring(0, 100) + "...";
      }

      link.appendChild(title);
      link.appendChild(date);
      link.appendChild(excerpt);
      li.appendChild(link);
      searchResultsList.appendChild(li);
    });

    searchResultsContainer.classList.remove("hidden");
  }

  /**
   * Clear search results
   */
  function clearResults() {
    if (searchResultsList) {
      searchResultsList.innerHTML = "";
    }
  }

  /**
   * Open search modal
   */
  function openSearch() {
    if (!searchInput) return;

    searchInput.value = "";
    clearResults();

    searchResultsContainer.classList.add("hidden");
    searchOverlay.classList.remove("hidden");
    searchOverlay.classList.add("flex");

    setTimeout(() => {
      searchOverlay.classList.add("opacity-100");
      searchInput.focus();
    }, 10);

    isSearchActive = true;
    document.body.classList.add("overflow-hidden");
  }

  /**
   * Close search modal
   */
  function closeSearch() {
    if (!searchOverlay) return;

    searchOverlay.classList.remove("opacity-100");

    setTimeout(() => {
      searchOverlay.classList.add("hidden");
      searchOverlay.classList.remove("flex");
      searchResultsContainer.classList.add("hidden");
    }, 200);

    isSearchActive = false;
    document.body.classList.remove("overflow-hidden");
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
