/**
 * url-validator.js - Utility for checking link health
 *
 * This module provides a development tool to scan and validate all external links
 * on a page to ensure they're working correctly. It identifies broken links and
 * provides a report of their status. This tool is primarily for development use
 * and is not intended for production deployments.
 *
 * @module url-validator
 */

/**
 * Initialize the URL validator when the DOM is loaded
 */
document.addEventListener("DOMContentLoaded", () => {
  const urlValidatorButton = document.getElementById("validate-urls");
  if (!urlValidatorButton) return;

  const validationResultsContainer = document.getElementById("validation-results");

  // Set up the click handler for the validation button
  urlValidatorButton.addEventListener("click", () =>
    validateUrls(validationResultsContainer)
  );
});

/**
 * Validates all external URLs found on the current page
 *
 * Collects all unique external links from the page, tests them using the
 * Microlink API, and displays a report of the results.
 *
 * @param {HTMLElement} resultsContainer - The element where results will be displayed
 * @returns {Promise<void>} A promise that resolves when validation is complete
 */
async function validateUrls(resultsContainer) {
  if (!resultsContainer) return;

  // Show progress indicator
  showProgressIndicator(resultsContainer, "Validating URLs. This may take a while...");

  // Find and filter all external links on the page
  const links = collectExternalLinks();

  // Process links with controlled concurrency
  const results = await processLinksWithConcurrency(links, resultsContainer);

  // Display formatted results
  displayResults(resultsContainer, results);
}

/**
 * Collects all external links from the current page
 *
 * @returns {string[]} Array of unique external URLs
 */
function collectExternalLinks() {
  const linkElements = document.querySelectorAll("a[href]");

  return Array.from(linkElements)
    .map((link) => link.href)
    .filter((href) => href.startsWith("http")) // Only external links
    .filter((href, index, self) => self.indexOf(href) === index); // Unique links only
}

/**
 * Processes links with limited concurrency to avoid rate limiting
 *
 * @param {string[]} links - Array of URLs to validate
 * @param {HTMLElement} resultsContainer - Element to update with progress
 * @param {number} [concurrencyLimit=3] - Maximum number of concurrent requests
 * @returns {Promise<Object[]>} Array of validation results
 */
async function processLinksWithConcurrency(
  links,
  resultsContainer,
  concurrencyLimit = 3
) {
  // Split links into chunks for controlled concurrency
  const chunks = [];
  for (let i = 0; i < links.length; i += concurrencyLimit) {
    chunks.push(links.slice(i, i + concurrencyLimit));
  }

  // Store all results
  const results = [];

  // Process chunks sequentially to avoid rate limits
  for (const chunk of chunks) {
    // Update progress indicator
    showProgressIndicator(
      resultsContainer,
      `Validating URLs: ${results.length} of ${links.length} complete...`
    );

    // Process links in each chunk concurrently
    const chunkResults = await Promise.all(chunk.map((url) => checkUrl(url)));
    results.push(...chunkResults);

    // Small delay to avoid rate limits
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  return results;
}

/**
 * Checks if a URL is valid using the Microlink API
 *
 * @param {string} url - The URL to validate
 * @returns {Promise<Object>} Object containing validation results
 */
async function checkUrl(url) {
  try {
    const response = await fetch(
      `https://api.microlink.io/?url=${encodeURIComponent(url)}&meta=false`
    );
    const data = await response.json();

    if (data.status === "success") {
      return { url, status: "valid", statusCode: 200 };
    } else {
      return {
        url,
        status: "invalid",
        statusCode: data.statusCode || "unknown",
        message: data.message || "Unknown error",
      };
    }
  } catch (error) {
    return { url, status: "error", message: error.message };
  }
}

/**
 * Shows a progress indicator in the results container
 *
 * @param {HTMLElement} container - Container element for the indicator
 * @param {string} message - Message to display
 */
function showProgressIndicator(container, message) {
  container.innerHTML = `<div class="p-4 bg-surface rounded-github mb-4">${message}</div>`;
}

/**
 * Displays formatted validation results
 *
 * @param {HTMLElement} container - Container to display results in
 * @param {Object[]} results - Array of validation result objects
 */
function displayResults(container, results) {
  // Count results by status
  const validCount = results.filter((r) => r.status === "valid").length;
  const invalidCount = results.length - validCount;

  // Filter invalid URLs for the report
  const invalidUrls = results.filter((r) => r.status !== "valid");

  // Generate report HTML
  const resultHtml = `
    <div class="p-4 bg-surface rounded-github mb-4">
      <h3 class="text-white text-lg font-semibold mb-2">URL Validation Results</h3>
      <div class="flex gap-4 mb-4">
        <div class="bg-accent/20 p-2 rounded-github">
          <span class="text-white font-medium">Valid: ${validCount}</span>
        </div>
        <div class="bg-red-500/20 p-2 rounded-github">
          <span class="text-white font-medium">Invalid: ${invalidCount}</span>
        </div>
      </div>

      <div class="mb-4">
        <h4 class="text-white font-medium mb-2">Invalid URLs:</h4>
        <div class="max-h-60 overflow-y-auto border border-border rounded-github p-2 bg-gray-light">
          <ul class="pl-4 list-disc">
            ${
              invalidUrls.length > 0
                ? invalidUrls
                    .map(
                      (r) => `<li class="mb-2 text-sm">
                               <span class="text-red-400">${r.url}</span>
                               <div class="text-text-secondary text-xs">
                                 Status: ${r.statusCode || "unknown"},
                                 Error: ${r.message || "No specific error"}
                               </div>
                             </li>`
                    )
                    .join("")
                : "<li>No invalid URLs found!</li>"
            }
          </ul>
        </div>
      </div>
    </div>
  `;

  container.innerHTML = resultHtml;
}
