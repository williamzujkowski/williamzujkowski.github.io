/**
 * URL validation tool to check the health of links
 * This is primarily for development use, not included in production
 */

document.addEventListener("DOMContentLoaded", () => {
  const urlValidatorButton = document.getElementById("validate-urls");

  if (!urlValidatorButton) return;

  const validationResultsContainer = document.getElementById("validation-results");

  // Helper function to check if a URL is valid using fetch
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

  async function validateUrls() {
    if (!validationResultsContainer) return;

    // Clear previous results
    validationResultsContainer.innerHTML =
      '<div class="p-4 bg-surface rounded-github mb-4">Validating URLs. This may take a while...</div>';

    // Find all links on the page
    const linkElements = document.querySelectorAll("a[href]");
    const links = Array.from(linkElements)
      .map((link) => link.href)
      .filter((href) => href.startsWith("http")) // Only external links
      .filter((href, index, self) => self.indexOf(href) === index); // Unique links only

    // Use a limited concurrency to avoid overwhelming the API
    const concurrencyLimit = 3;
    const chunks = [];

    // Split links into chunks
    for (let i = 0; i < links.length; i += concurrencyLimit) {
      chunks.push(links.slice(i, i + concurrencyLimit));
    }

    // Store all results
    const results = [];

    // Process chunks sequentially to avoid rate limits
    for (const chunk of chunks) {
      validationResultsContainer.innerHTML = `<div class="p-4 bg-surface rounded-github mb-4">Validating URLs: ${results.length} of ${links.length} complete...</div>`;

      // Process links in each chunk concurrently
      const chunkResults = await Promise.all(chunk.map((url) => checkUrl(url)));
      results.push(...chunkResults);

      // Small delay to avoid rate limits
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    // Count results
    const validCount = results.filter((r) => r.status === "valid").length;
    const invalidCount = results.length - validCount;

    // Display results
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
                results
                  .filter((r) => r.status !== "valid")
                  .map(
                    (r) => `<li class="mb-2 text-sm">
                                 <span class="text-red-400">${r.url}</span>
                                 <div class="text-text-secondary text-xs">
                                   Status: ${r.statusCode || "unknown"},
                                   Error: ${r.message || "No specific error"}
                                 </div>
                               </li>`
                  )
                  .join("") || "<li>No invalid URLs found!</li>"
              }
            </ul>
          </div>
        </div>
      </div>
    `;

    validationResultsContainer.innerHTML = resultHtml;
  }

  // Add event listener to validation button
  urlValidatorButton.addEventListener("click", validateUrls);
});
