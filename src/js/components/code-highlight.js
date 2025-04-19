/**
 * code-highlight.js - Enhanced code block functionality
 * 
 * This module provides syntax highlighting, line numbers, and copy functionality
 * for code blocks in blog posts and documentation pages.
 * 
 * @module components/code-highlight
 */

import { $, $$ } from "../utils/dom.js";

/**
 * Initializes code block highlighting and functionality.
 * 
 * This function transforms regular code blocks into enhanced code blocks with:
 * - A header showing the detected language
 * - Line numbers for each line of code
 * - A copy-to-clipboard button
 * - Improved styling and accessibility
 * 
 * @returns {void}
 */
export function initCodeHighlight() {
  // Find all code blocks
  const codeBlocks = $$("pre code");

  // Process each code block
  codeBlocks.forEach((codeBlock, index) => {
    const pre = codeBlock.parentNode;

    // Create wrapper for the code block
    const wrapper = document.createElement("div");
    wrapper.className = "relative group mb-6 mt-6";
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    // Add a header bar with language and copy button
    const header = document.createElement("div");
    header.className = "code-header";

    // Try to detect language from class
    let language = "plaintext";
    const classes = codeBlock.className.split(" ");
    for (const cls of classes) {
      if (cls.startsWith("language-")) {
        language = cls.replace("language-", "");
        break;
      }
    }

    // Create language indicator
    const langIndicator = document.createElement("div");
    langIndicator.textContent = language;
    langIndicator.setAttribute("aria-label", `Language: ${language}`);
    header.appendChild(langIndicator);

    // Create copy button with GitHub-style SVG icon
    const copyButton = document.createElement("button");
    copyButton.className = "copy-button";
    copyButton.innerHTML =
      '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg>';
    copyButton.setAttribute("aria-label", "Copy code");
    copyButton.setAttribute("title", "Copy code");
    copyButton.setAttribute("data-index", index);
    header.appendChild(copyButton);

    // Insert header before pre
    wrapper.insertBefore(header, pre);

    // Add styling to pre element
    pre.className = "rounded-t-none rounded-b-github overflow-auto m-0";

    // Add line numbers to code
    addLineNumbers(codeBlock);
  });

  // Set up event delegation for copy button clicks
  setupCopyButtonHandlers();
}

/**
 * Adds line numbers to a code block.
 * 
 * @param {HTMLElement} codeBlock - The code block element to add line numbers to
 * @returns {void}
 * @private
 */
function addLineNumbers(codeBlock) {
  const codeLines = codeBlock.innerHTML.split("\n");
  let numberedCode = "";

  codeLines.forEach((line, i) => {
    // Skip empty trailing line
    if (i === codeLines.length - 1 && line === "") return;
    
    // Add span with line number as data attribute
    numberedCode += `<span class="code-line" data-line-number="${i + 1}">${line}</span>\n`;
  });

  codeBlock.innerHTML = numberedCode;
}

/**
 * Sets up event handlers for copy buttons using event delegation.
 * 
 * @returns {void}
 * @private
 */
function setupCopyButtonHandlers() {
  // Handle copy button clicks via event delegation
  document.addEventListener("click", (e) => {
    if (e.target.closest(".copy-button")) {
      const button = e.target.closest(".copy-button");
      const index = button.getAttribute("data-index");
      const codeBlock = $$("pre code")[index];
      const text = codeBlock.textContent;

      // Copy to clipboard and provide visual feedback
      copyTextToClipboard(text, button);
    }
  });
}

/**
 * Copies text to clipboard and updates button appearance to provide feedback.
 * 
 * @param {string} text - The text to copy to clipboard
 * @param {HTMLElement} button - The button element that was clicked
 * @returns {void}
 * @private
 */
function copyTextToClipboard(text, button) {
  // SVG for success checkmark
  const successSvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>';
  
  // SVG for copy icon
  const copySvg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg>';

  // Copy to clipboard
  navigator.clipboard.writeText(text).then(() => {
    // Show success state
    button.innerHTML = successSvg;
    button.classList.add("text-green-400");
    button.setAttribute("aria-label", "Copied!");
    button.setAttribute("title", "Copied!");

    // Reset after a delay
    setTimeout(() => {
      button.innerHTML = copySvg;
      button.classList.remove("text-green-400");
      button.setAttribute("aria-label", "Copy code");
      button.setAttribute("title", "Copy code");
    }, 2000);
  }).catch(err => {
    console.error('Could not copy text: ', err);
    button.classList.add("text-red-400");
    button.setAttribute("aria-label", "Failed to copy");
    button.setAttribute("title", "Failed to copy");
    
    // Reset after a delay
    setTimeout(() => {
      button.innerHTML = copySvg;
      button.classList.remove("text-red-400");
      button.setAttribute("aria-label", "Copy code");
      button.setAttribute("title", "Copy code");
    }, 2000);
  });
}
