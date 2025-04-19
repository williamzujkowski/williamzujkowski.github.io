/**
 * search.js - Client-side search functionality for blog posts
 *
 * This module implements real-time search with content highlighting and animations
 * for improved user experience. It includes security features such as input
 * sanitization and validation.
 *
 * @module search
 */

/**
 * Maximum allowed query length to prevent DoS attacks
 * @type {number}
 */
const MAX_QUERY_LENGTH = 100;

/**
 * Maximum allowed time for search operation (ms)
 * @type {number}
 */
const SEARCH_TIMEOUT = 500;

/**
 * Initialize search functionality when DOM is ready
 */
document.addEventListener("DOMContentLoaded", initSearch);

/**
 * Initialize search functionality
 *
 * Sets up event listeners and data extraction for the search feature.
 * Includes security measures for input validation.
 *
 * @returns {void}
 */
function initSearch() {
  const searchInput = document.getElementById("search-input");
  const searchCountElement = document.getElementById("search-results-count");
  const searchableElements = document.querySelectorAll(".searchable");
  const noResultsMessage = document.getElementById("no-results-message");
  const resetButton = document.getElementById("reset-search");

  // Exit if no search input or searchable elements
  if (!searchInput || !searchableElements.length) return;

  // Set up search input security measures
  setupSearchInputSecurity(searchInput);

  // Extract and prepare post data from DOM for search
  const postsData = extractPostData(searchableElements);

  // Set up event listeners with debounce for performance
  searchInput.addEventListener(
    "input",
    debounce(function () {
      // Sanitize and validate input before processing
      const sanitizedQuery = sanitizeSearchQuery(this.value);
      if (isValidSearchQuery(sanitizedQuery)) {
        // Set a timeout to prevent long-running searches
        const searchTimeout = setTimeout(() => {
          console.warn("Search operation timed out");
          if (countElement) {
            countElement.parentElement.classList.remove("searching");
          }
        }, SEARCH_TIMEOUT);

        // Perform the search
        performSearch(sanitizedQuery, postsData, searchCountElement, noResultsMessage);

        // Clear the timeout if search completed
        clearTimeout(searchTimeout);
      }
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
 * Set up security measures for search input
 *
 * @param {HTMLInputElement} inputElement - The search input element
 * @returns {void}
 */
function setupSearchInputSecurity(inputElement) {
  // Set maximum length attribute to prevent excessively long inputs
  inputElement.setAttribute("maxlength", MAX_QUERY_LENGTH.toString());

  // Add pattern attribute for basic input validation
  inputElement.setAttribute("pattern", "[A-Za-z0-9\\s\\-_,.]+");

  // Add input validation on paste
  inputElement.addEventListener("paste", function (e) {
    // Get pasted data
    let pastedText = "";
    if (window.clipboardData && window.clipboardData.getData) {
      // IE
      pastedText = window.clipboardData.getData("Text");
    } else if (e.clipboardData && e.clipboardData.getData) {
      pastedText = e.clipboardData.getData("text/plain");
    }

    // If the pasted content exceeds the max length, truncate it
    if (pastedText.length > MAX_QUERY_LENGTH) {
      e.preventDefault();
      const truncatedText = pastedText.substring(0, MAX_QUERY_LENGTH);

      // Use execCommand for older browsers or fallback to standard input handling
      if (document.execCommand) {
        document.execCommand("insertText", false, truncatedText);
      } else {
        // Fallback - replace the current selection
        const start = this.selectionStart;
        const end = this.selectionEnd;
        const text = this.value;
        this.value = text.slice(0, start) + truncatedText + text.slice(end);
        // Put caret at right position
        this.selectionStart = this.selectionEnd = start + truncatedText.length;
      }
    }
  });
}

/**
 * Sanitize search query to prevent XSS and injection attacks
 *
 * @param {string} query - Raw search query from input
 * @returns {string} Sanitized query
 */
function sanitizeSearchQuery(query) {
  if (!query) return "";

  // Trim and convert to string if not already
  const stringQuery = String(query).trim();

  // Truncate if longer than maximum allowed length
  if (stringQuery.length > MAX_QUERY_LENGTH) {
    return stringQuery.substring(0, MAX_QUERY_LENGTH);
  }

  // Remove HTML tags and potentially dangerous characters
  return stringQuery
    .replace(/<[^>]*>/g, "") // Remove HTML tags
    .replace(/[<>"'`=;()]/g, ""); // Remove special characters used in XSS attacks
}

/**
 * Validate search query for security
 *
 * @param {string} query - Sanitized search query
 * @returns {boolean} True if query is valid, false otherwise
 */
function isValidSearchQuery(query) {
  // Empty queries are valid (shows all results)
  if (!query) return true;

  // Check for potential code injection patterns
  const suspiciousPatterns = [
    /javascript:/i, // JavaScript protocol
    /data:/i, // Data protocol
    /on\w+=/i, // Event handlers
    /;.*}/i, // Potential script termination
    /\)\s*{/i, // Function execution
  ];

  for (const pattern of suspiciousPatterns) {
    if (pattern.test(query)) {
      console.warn("Potentially malicious search query detected");
      return false;
    }
  }

  return true;
}

/**
 * Extract post data from DOM elements
 *
 * @param {NodeList} elements - Searchable DOM elements
 * @returns {Array} Array of post data objects
 */
function extractPostData(elements) {
  const data = [];

  elements.forEach((element) => {
    // Safely extract post data
    try {
      const title = element.querySelector(".gh-post-title")?.textContent || "";
      const excerpt = element.querySelector(".gh-post-excerpt")?.textContent || "";
      const tags = element.dataset.tags || "";
      const url = element.querySelector(".gh-post-title")?.getAttribute("href") || "";

      // Validate URL to prevent malicious links
      const validUrl = url.startsWith("/") || url.startsWith("http");

      data.push({
        element,
        title: title.toLowerCase(),
        excerpt: excerpt.toLowerCase(),
        tags: tags.toLowerCase(),
        url: validUrl ? url : "#", // Use safe fallback if invalid URL
      });
    } catch (error) {
      console.error("Error extracting post data:", error);
      // Skip this element if there's an error
    }
  });

  return data;
}

/**
 * Perform search on posts data
 *
 * @param {string} query - Sanitized search query
 * @param {Array} postsData - Array of post data objects
 * @param {Element} countElement - Element to display result count
 * @param {Element} noResultsElement - Element to show when no results
 * @returns {void}
 */
function performSearch(query, postsData, countElement, noResultsElement) {
  // No need to toLowerCase() again since we did it in extractPostData
  let visibleCount = 0;

  // Add searching class for potential loading indicator
  if (countElement) {
    countElement.parentElement.classList.add("searching");
  }

  // Process each post
  postsData.forEach((post) => {
    try {
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
    } catch (error) {
      console.error("Error processing search for post:", error);
      // Continue with next post if there's an error
    }
  });

  // Update results count
  updateResultsCount(countElement, visibleCount);

  // Show/hide no results message
  toggleNoResultsMessage(noResultsElement, visibleCount, query);
}

/**
 * Update search results count element
 *
 * @param {Element} countElement - Element to update
 * @param {number} count - Number of visible results
 * @returns {void}
 */
function updateResultsCount(countElement, count) {
  if (!countElement) return;

  try {
    // Use textContent instead of innerHTML for security
    countElement.textContent = count;
    countElement.parentElement.classList.remove("searching");
  } catch (error) {
    console.error("Error updating results count:", error);
  }
}

/**
 * Toggle no results message visibility
 *
 * @param {Element} messageElement - No results message element
 * @param {number} resultsCount - Number of visible results
 * @param {string} query - Current search query
 * @returns {void}
 */
function toggleNoResultsMessage(messageElement, resultsCount, query) {
  if (!messageElement) return;

  try {
    if (resultsCount === 0 && query !== "") {
      messageElement.classList.remove("hidden");
      messageElement.style.opacity = "0";
      setTimeout(() => {
        messageElement.style.opacity = "1";
      }, 10);
    } else {
      messageElement.classList.add("hidden");
    }
  } catch (error) {
    console.error("Error toggling no results message:", error);
  }
}

/**
 * Highlight matching text in search results
 *
 * Uses a secure approach to highlight text to prevent XSS.
 *
 * @param {Object} post - Post data object
 * @param {string} query - Sanitized search query
 * @returns {void}
 */
function highlightMatches(post, query) {
  const excerptElement = post.element.querySelector(".gh-post-excerpt");
  if (!excerptElement) return;

  try {
    // Safely extract text content
    const excerptText = excerptElement.textContent;

    // Create safe regex for highlighting
    const safeQuery = escapeRegExp(query);
    const regex = new RegExp(`(${safeQuery})`, "gi");

    // Create a document fragment for safe HTML insertion
    const fragment = document.createDocumentFragment();
    const parts = excerptText.split(regex);

    parts.forEach((part, i) => {
      // Even indices are non-matches, odd indices are matches
      if (i % 2 === 0) {
        fragment.appendChild(document.createTextNode(part));
      } else {
        // This is a match, create a highlighted element
        const mark = document.createElement("mark");
        mark.className = "bg-accent/20 text-white px-1 rounded";
        mark.textContent = part;
        fragment.appendChild(mark);
      }
    });

    // Clear and append the new content
    excerptElement.textContent = "";
    excerptElement.appendChild(fragment);
  } catch (error) {
    console.error("Error highlighting matches:", error);
    // Revert to original text content if highlighting fails
    excerptElement.textContent = excerptElement.textContent;
  }
}

/**
 * Remove highlighting from post excerpts
 *
 * @param {Object} post - Post data object
 * @returns {void}
 */
function removeHighlights(post) {
  const excerptElement = post.element.querySelector(".gh-post-excerpt");
  if (!excerptElement) return;

  try {
    // Safely remove highlighting by setting text content
    if (excerptElement.querySelector("mark")) {
      excerptElement.textContent = excerptElement.textContent;
    }
  } catch (error) {
    console.error("Error removing highlights:", error);
  }
}

/**
 * Apply fade-in animation to element with error handling
 *
 * @param {Element} element - DOM element to animate
 * @returns {void}
 */
function applyFadeIn(element) {
  try {
    element.style.opacity = "0";
    element.style.transform = "translateY(10px)";

    setTimeout(() => {
      element.style.opacity = "1";
      element.style.transform = "translateY(0)";
      element.style.transition = "opacity 0.3s ease, transform 0.3s ease";
    }, 10);
  } catch (error) {
    console.error("Error applying fade-in animation:", error);
    // Ensure element is visible even if animation fails
    element.style.opacity = "1";
  }
}

/**
 * Escape special characters for regex to prevent ReDoS attacks
 *
 * @param {string} string - String to escape
 * @returns {string} Escaped string
 */
function escapeRegExp(string) {
  try {
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  } catch (error) {
    console.error("Error escaping RegExp:", error);
    // Return a safe empty string if escape fails
    return "";
  }
}

/**
 * Debounce function to limit how often a function is called
 *
 * Improves performance and reduces server load for rapid input.
 *
 * @param {Function} func - Function to debounce
 * @param {number} wait - Milliseconds to wait between calls
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
  let timeout;
  return function (...args) {
    const context = this;
    clearTimeout(timeout);
    timeout = setTimeout(() => {
      timeout = null;
      try {
        func.apply(context, args);
      } catch (error) {
        console.error("Error in debounced function:", error);
      }
    }, wait);
  };
}
