/**
 * code-highlight.js - Enhanced code block functionality
 */

import { $, $$ } from "../utils/dom.js";

export function initCodeHighlight() {
  // Find all code blocks
  const codeBlocks = $$("pre code");

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
    header.appendChild(langIndicator);

    // Create copy button
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

    // Add styling to pre
    pre.className = "rounded-t-none rounded-b-github overflow-auto m-0";

    // Add line numbers
    const codeLines = codeBlock.innerHTML.split("\n");
    let numberedCode = "";

    codeLines.forEach((line, i) => {
      if (i === codeLines.length - 1 && line === "") return;
      numberedCode += `<span class="code-line" data-line-number="${i + 1}">${line}</span>\n`;
    });

    codeBlock.innerHTML = numberedCode;
  });

  // Handle copy button clicks
  document.addEventListener("click", (e) => {
    if (e.target.closest(".copy-button")) {
      const button = e.target.closest(".copy-button");
      const index = button.getAttribute("data-index");
      const codeBlock = $$("pre code")[index];
      const text = codeBlock.textContent;

      // Copy to clipboard
      navigator.clipboard.writeText(text).then(() => {
        button.innerHTML =
          '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.751.751 0 0 1 .018-1.042.751.751 0 0 1 1.042-.018L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z"></path></svg>';
        button.classList.add("text-green-400");

        // Reset after a delay
        setTimeout(() => {
          button.innerHTML =
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="14" height="14" fill="currentColor"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg>';
          button.classList.remove("text-green-400");
        }, 2000);
      });
    }
  });
}
