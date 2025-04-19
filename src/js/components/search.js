/**
 * search.js - Blog search component
 *
 * Implements client-side search for blog posts with highlighting
 * and animation effects for better user experience.
 */

import { $, $$, debounce } from "../utils/dom.js";

/**
 * Initialize the search component
 */
export function initSearch() {
  const searchInput = $("#search-input");
  const searchCountElement = $("#search-results-count");
  const searchableElements = $$(".searchable");
  const noResultsMessage = $("#no-results-message");
  const resetButton = $("#reset-search");

  // Exit if no search input or searchable elements
  if (!searchInput || !searchableElements.length) return;

  // Extract and prepare post data from DOM for search
  const postsData = extractPostData(searchableElements);

  // Set up event listeners
  searchInput.addEventListener(
    "input",
    debounce(function () {
      performSearch(this.value, postsData, searchCountElement, noResultsMessage);
    }, 300)
  );

  // Reset search if there's a reset button
  if (resetButton) {
    resetButton.addEventListener("click", function () {
      searchInput.value = "";
      performSearch("", postsData, searchCountElement, noResultsMessage);
      searchInput.focus();
    });
  }
}

/**
 * Extract post data from DOM elements
 * @param {NodeList} elements - Searchable DOM elements
 * @returns {Array} Array of post data objects
 */
function extractPostData(elements) {
  const data = [];

  elements.forEach((element) => {
    const title = element.querySelector(".gh-post-title")?.textContent || "";
    const excerpt = element.querySelector(".gh-post-excerpt")?.textContent || "";
    const tags = element.dataset.tags || "";
    const url = element.querySelector(".gh-post-title")?.getAttribute("href") || "";

    data.push({
      element,
      title: title.toLowerCase(),
      excerpt: excerpt.toLowerCase(),
      tags: tags.toLowerCase(),
      url,
    });
  });

  return data;
}

/**
 * Perform search on posts data
 * @param {string} query - Search query
 * @param {Array} postsData - Array of post data objects
 * @param {Element} countElement - Element to display result count
 * @param {Element} noResultsElement - Element to show when no results
 */
function performSearch(query, postsData, countElement, noResultsElement) {
  query = query.toLowerCase().trim();
  let visibleCount = 0;

  // Add searching class for potential loading indicator
  if (countElement) {
    countElement.parentElement.classList.add("searching");
  }

  // Process each post
  postsData.forEach((post) => {
    const matchesTitle = post.title.includes(query);
    const matchesExcerpt = post.excerpt.includes(query);
    const matchesTags = post.tags.includes(query);
    const isMatch = query === "" || matchesTitle || matchesExcerpt || matchesTags;

    if (isMatch) {
      post.element.style.display = "";
      applyFadeIn(post.element);
      visibleCount++;

      // Highlight matching text if there's a query
      if (query !== "") {
        highlightMatches(post, query);
      } else {
        removeHighlights(post);
      }
    } else {
      post.element.style.display = "none";
    }
  });

  // Update results count
  updateResultsCount(countElement, visibleCount);

  // Show/hide no results message
  toggleNoResultsMessage(noResultsElement, visibleCount, query);

  // Add reset animation to post grid
  const postGrid = $(".gh-post-grid");
  if (postGrid) {
    postGrid.classList.add("reset-animation");
    setTimeout(() => {
      postGrid.classList.remove("reset-animation");
    }, 500);
  }
}

/**
 * Update search results count element
 * @param {Element} countElement - Element to update
 * @param {number} count - Number of visible results
 */
function updateResultsCount(countElement, count) {
  if (!countElement) return;

  countElement.textContent = count;
  countElement.parentElement.classList.remove("searching");
}

/**
 * Toggle no results message visibility
 * @param {Element} messageElement - No results message element
 * @param {number} resultsCount - Number of visible results
 * @param {string} query - Current search query
 */
function toggleNoResultsMessage(messageElement, resultsCount, query) {
  if (!messageElement) return;

  if (resultsCount === 0 && query !== "") {
    messageElement.classList.remove("hidden");
    messageElement.style.opacity = "0";
    setTimeout(() => {
      messageElement.style.opacity = "1";
    }, 10);
  } else {
    messageElement.classList.add("hidden");
  }
}

/**
 * Highlight matching text in search results
 * @param {Object} post - Post data object
 * @param {string} query - Search query
 */
function highlightMatches(post, query) {
  const excerptElement = post.element.querySelector(".gh-post-excerpt");
  if (!excerptElement) return;

  const excerptText = excerptElement.textContent;
  const regex = new RegExp(`(${escapeRegExp(query)})`, "gi");
  excerptElement.innerHTML = excerptText.replace(
    regex,
    '<mark class="gh-search-highlight">$1</mark>'
  );
}

/**
 * Remove highlighting from post excerpts
 * @param {Object} post - Post data object
 */
function removeHighlights(post) {
  const excerptElement = post.element.querySelector(".gh-post-excerpt");
  if (!excerptElement) return;

  if (excerptElement.innerHTML.includes("<mark")) {
    excerptElement.textContent = excerptElement.textContent;
  }
}

/**
 * Apply fade-in animation to element
 * @param {Element} element - DOM element to animate
 */
function applyFadeIn(element) {
  element.style.opacity = "0";
  element.style.transform = "translateY(10px)";

  setTimeout(() => {
    element.style.opacity = "1";
    element.style.transform = "translateY(0)";
    element.style.transition = "opacity 0.3s ease, transform 0.3s ease";
  }, 10);
}

/**
 * Escape special characters for regex
 * @param {string} string - String to escape
 * @returns {string} Escaped string
 */
function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}
