/**
 * Blog search, filtering, and animation functionality
 * Enhanced with security measures to prevent XSS and injection attacks
 */

// Security constants
const MAX_QUERY_LENGTH = 100; // Maximum length for search query
const SEARCH_TIMEOUT = 500; // Timeout for search operations in ms
const ANIMATION_STAGGER_BASE = 100; // Base delay for staggered animations
const ANIMATION_STAGGER_INCREMENT = 70; // Increment for staggered animations
const FADE_DELAY_BASE = 50; // Base delay for fade animations
const FADE_DELAY_INCREMENT = 30; // Increment for fade animations

document.addEventListener("DOMContentLoaded", () => {
  // DOM element references
  const searchInput = document.getElementById("search-input");
  const resetButton = document.getElementById("reset-search");
  const clearFiltersBtn = document.getElementById("clear-filters");
  const noResultsMessage = document.getElementById("no-results-message");
  const resultCount = document.getElementById("search-results-count");
  const searchableElements = document.querySelectorAll(".searchable");
  const tagButtons = document.querySelectorAll(".tag-btn");
  const postGrid = document.querySelector(".grid");

  // Initialize security measures
  if (searchInput) {
    setupSearchInputSecurity(searchInput);
  }

  // Add animation classes to posts for staggered entrance
  searchableElements.forEach((element, index) => {
    element.style.opacity = "0";
    element.style.transform = "translateY(20px)";
    element.style.transition = "opacity 0.6s ease, transform 0.6s ease";

    // Stagger the animations
    setTimeout(
      () => {
        element.style.opacity = "1";
        element.style.transform = "translateY(0)";
      },
      ANIMATION_STAGGER_BASE + index * ANIMATION_STAGGER_INCREMENT
    );
  });

  /**
   * Set up security measures for the search input
   *
   * @param {HTMLInputElement} inputElement - The search input element
   */
  function setupSearchInputSecurity(inputElement) {
    // Set maximum length attribute to prevent excessively long inputs
    inputElement.setAttribute("maxlength", MAX_QUERY_LENGTH.toString());

    // Add pattern attribute for basic input validation
    inputElement.setAttribute("pattern", "[A-Za-z0-9\\s\\-_,.]+");

    // Add input validation on paste
    inputElement.addEventListener("paste", function (e) {
      // Get pasted data
      let pastedData = (e.clipboardData || window.clipboardData).getData("text");

      // Sanitize and validate the pasted data
      pastedData = sanitizeSearchQuery(pastedData);
      if (!isValidSearchQuery(pastedData)) {
        // Prevent the paste operation if invalid
        e.preventDefault();
        console.warn(
          "Potentially unsafe content blocked from being pasted into search"
        );
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
   * Perform search across all searchable elements
   *
   * @param {string} rawQuery - The raw search query to process
   */
  function performSearch(rawQuery) {
    // Sanitize and validate the query
    const sanitizedQuery = sanitizeSearchQuery(rawQuery);
    if (!isValidSearchQuery(sanitizedQuery)) {
      console.warn("Invalid search query rejected");
      return;
    }

    const query = sanitizedQuery.toLowerCase();
    let visibleCount = 0;

    // Add a transition effect to grid
    if (postGrid) {
      postGrid.classList.add("searching");
    }

    // Set timeout to ensure we don't block the UI thread
    const searchTimeout = setTimeout(() => {
      try {
        searchableElements.forEach((element) => {
          // Safely access element content
          const titleElement = element.querySelector(".gh-post-title");
          const excerptElement = element.querySelector(".gh-post-excerpt");

          // Use optional chaining and nullish coalescing for safety
          const title = titleElement ? titleElement.textContent.toLowerCase() : "";
          const content = excerptElement
            ? excerptElement.textContent.toLowerCase()
            : "";
          const tags = element.dataset.tags ? element.dataset.tags.toLowerCase() : "";

          // Search in title, content, and tags
          if (
            title.includes(query) ||
            content.includes(query) ||
            tags.includes(query) ||
            query === ""
          ) {
            element.style.display = "";
            visibleCount++;

            // Highlight matching text if there's a query
            if (query !== "") {
              highlightText(element, query);
            } else {
              removeHighlights(element);
            }

            // Add a fade-in animation with staggering
            element.style.opacity = "0";
            element.style.transform = "translateY(10px)";

            setTimeout(
              () => {
                element.style.opacity = "1";
                element.style.transform = "translateY(0)";
              },
              FADE_DELAY_BASE + visibleCount * FADE_DELAY_INCREMENT
            );
          } else {
            element.style.display = "none";
          }
        });

        // Update count and show/hide no results message
        updateResultsUI(visibleCount, query);

        // Remove transition class
        if (postGrid) {
          setTimeout(() => {
            postGrid.classList.remove("searching");
          }, 300);
        }
      } catch (error) {
        console.error("Error in search operation:", error);
        // Ensure UI is still usable if search fails
        resetSearchUI();
      }
    }, 200);

    // Set a timeout to prevent long-running searches
    setTimeout(() => {
      clearTimeout(searchTimeout);
    }, SEARCH_TIMEOUT);
  }

  /**
   * Update the results UI based on search results
   *
   * @param {number} visibleCount - Number of visible search results
   * @param {string} query - The current search query
   */
  function updateResultsUI(visibleCount, query) {
    // Update result count display if it exists
    if (resultCount) {
      resultCount.textContent = visibleCount.toString();
    }

    // Show/hide no results message
    if (visibleCount === 0 && query !== "") {
      if (noResultsMessage) {
        noResultsMessage.classList.remove("hidden");
        noResultsMessage.style.opacity = "0";
        setTimeout(() => {
          noResultsMessage.style.opacity = "1";
        }, FADE_DELAY_BASE);
      }
    } else {
      if (noResultsMessage) {
        noResultsMessage.classList.add("hidden");
      }
    }
  }

  /**
   * Reset the search UI to a usable state
   * Used when errors occur during search
   */
  function resetSearchUI() {
    // Make all elements visible
    searchableElements.forEach((element) => {
      element.style.display = "";
      element.style.opacity = "1";
      element.style.transform = "translateY(0)";
      removeHighlights(element);
    });

    // Update count
    if (resultCount) {
      resultCount.textContent = searchableElements.length.toString();
    }

    // Hide no results message
    if (noResultsMessage) {
      noResultsMessage.classList.add("hidden");
    }

    // Remove transition class from grid
    if (postGrid) {
      postGrid.classList.remove("searching");
    }
  }

  /**
   * Highlight matching text in search results securely
   *
   * @param {HTMLElement} element - The element containing text to highlight
   * @param {string} query - The search query to highlight
   */
  function highlightText(element, query) {
    // First remove any existing highlights
    removeHighlights(element);

    // Only highlight in the excerpt to avoid changing the title
    const excerpt = element.querySelector(".gh-post-excerpt");
    if (!excerpt) return;

    try {
      const content = excerpt.textContent;
      if (!content) return;

      // Create a new document fragment to safely build the HTML
      const fragment = document.createDocumentFragment();

      // Use a safe regex with the safely escaped query
      const safeQuery = escapeRegExp(query);

      // Limit regex complexity to prevent ReDoS attacks
      if (safeQuery.length > 50) {
        // For long queries, just use simple text node
        fragment.appendChild(document.createTextNode(content));
        excerpt.innerHTML = "";
        excerpt.appendChild(fragment);
        return;
      }

      // Protect against excessively complex regex operations
      const regex = new RegExp(`(${safeQuery})`, "gi");
      const parts = content.split(regex);

      // Build highlighted content safely using DOM methods instead of innerHTML
      parts.forEach((part, index) => {
        if (index % 2 === 1) {
          // This is a match
          const mark = document.createElement("mark");
          mark.className = "gh-search-highlight";
          mark.textContent = part;
          fragment.appendChild(mark);
        } else {
          // This is non-matching text
          fragment.appendChild(document.createTextNode(part));
        }
      });

      // Replace content with the safely built fragment
      excerpt.innerHTML = "";
      excerpt.appendChild(fragment);
    } catch (error) {
      console.error("Error highlighting text:", error);
      // Fall back to plain text on error
      if (excerpt) {
        excerpt.textContent = excerpt.textContent;
      }
    }
  }

  /**
   * Remove highlights from search results
   *
   * @param {HTMLElement} element - The element containing highlights to remove
   */
  function removeHighlights(element) {
    const excerpt = element.querySelector(".gh-post-excerpt");
    if (!excerpt) return;

    try {
      // Check if there are any highlights to remove
      if (excerpt.querySelector("mark")) {
        // Use textContent to strip HTML and just keep the text
        const plainText = excerpt.textContent;

        // Create a text node with the plain content
        const textNode = document.createTextNode(plainText);

        // Replace all content with the plain text node
        excerpt.innerHTML = "";
        excerpt.appendChild(textNode);
      }
    } catch (error) {
      console.error("Error removing highlights:", error);
    }
  }

  /**
   * Escape regex special characters to prevent ReDoS attacks
   *
   * @param {string} string - The string to escape
   * @returns {string} The escaped string
   */
  function escapeRegExp(string) {
    // Basic escaping of special regex characters
    return string.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  /**
   * Reset all filters and search state
   */
  function resetAllFilters() {
    if (!searchInput) return;

    try {
      // Clear search input
      searchInput.value = "";
      performSearch("");

      // Reset tag buttons
      if (tagButtons) {
        tagButtons.forEach((btn) => {
          if (btn.dataset.tag === "") {
            btn.classList.add("selected");
          } else {
            btn.classList.remove("selected");
          }
        });
      }

      // Add a subtle animation to the grid
      if (postGrid) {
        postGrid.classList.add("reset-animation");
        setTimeout(() => {
          postGrid.classList.remove("reset-animation");
        }, 500);
      }
    } catch (error) {
      console.error("Error resetting filters:", error);
      // Fallback to basic reset if something goes wrong
      if (searchInput) searchInput.value = "";
      resetSearchUI();
    }
  }

  // Search input event with debounce
  let debounceTimeout;
  if (searchInput) {
    searchInput.addEventListener("input", function () {
      // Clear previous timeout to implement debounce
      clearTimeout(debounceTimeout);

      // Set new timeout
      debounceTimeout = setTimeout(() => {
        // Get input value safely
        const inputValue = this.value || "";

        // Perform search with sanitization
        performSearch(inputValue);

        // Reset tag buttons if search is empty
        if (inputValue === "" && tagButtons) {
          tagButtons.forEach((btn) => {
            if (btn.dataset.tag === "") {
              btn.classList.add("selected");
            } else {
              btn.classList.remove("selected");
            }
          });
        }
      }, 300); // 300ms debounce
    });
  }

  // Reset search button in no results message
  if (resetButton) {
    resetButton.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent default button behavior
      resetAllFilters();
      // Focus on search input
      if (searchInput) searchInput.focus();
    });
  }

  // Clear filters button
  if (clearFiltersBtn) {
    clearFiltersBtn.addEventListener("click", function (e) {
      e.preventDefault(); // Prevent default button behavior
      resetAllFilters();

      // Add animation to the button
      this.classList.add("active");
      setTimeout(() => {
        this.classList.remove("active");
      }, 300);
    });
  }

  // Tag buttons
  if (tagButtons && tagButtons.length > 0) {
    tagButtons.forEach((button) => {
      button.addEventListener("click", function (e) {
        e.preventDefault(); // Prevent default button behavior

        // Get tag value safely
        const tag = this.dataset.tag || "";

        // Add a pulse animation to the clicked tag
        this.classList.add("pulse-animation");
        setTimeout(() => this.classList.remove("pulse-animation"), 500);

        // Update search input and perform search with sanitization
        if (searchInput) {
          if (tag === "") {
            searchInput.value = "";
            performSearch("");
          } else {
            // Sanitize the tag value before using it
            const sanitizedTag = sanitizeSearchQuery(tag);
            searchInput.value = sanitizedTag;
            performSearch(sanitizedTag);
          }
        }

        // Add selected class to the clicked tag
        if (tagButtons) {
          tagButtons.forEach((btn) => btn.classList.remove("selected"));
          this.classList.add("selected");
        }
      });
    });
  }
});
