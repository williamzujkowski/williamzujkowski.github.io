/**
 * static-fallbacks.js - Static fallbacks for dynamic content
 */

import { $ } from "../utils/dom.js";

export function initStaticFallbacks() {
  window.addEventListener("load", function () {
    // Replace heatmap loading indicator with static SVG
    const heatmapContainer = $("#contribution-heatmap");
    if (heatmapContainer) {
      heatmapContainer.innerHTML = `
        <!-- Static heatmap with sample data -->
        <svg width="100%" height="140" viewBox="0 0 850 150" class="contribution-graph" xmlns="http://www.w3.org/2000/svg">
          <!-- Day labels -->
          <g transform="translate(0, 20)">
            <text x="10" y="26" font-size="9" fill="#8b949e" text-anchor="middle">Mon</text>
            <text x="10" y="54" font-size="9" fill="#8b949e" text-anchor="middle">Wed</text>
            <text x="10" y="82" font-size="9" fill="#8b949e" text-anchor="middle">Fri</text>
          </g>

          <!-- Month labels -->
          <g transform="translate(30, 10)">
            <text x="0" y="0" font-size="10" fill="#8b949e">Jan</text>
            <text x="70" y="0" font-size="10" fill="#8b949e">Feb</text>
            <text x="140" y="0" font-size="10" fill="#8b949e">Mar</text>
            <text x="210" y="0" font-size="10" fill="#8b949e">Apr</text>
            <text x="280" y="0" font-size="10" fill="#8b949e">May</text>
            <text x="350" y="0" font-size="10" fill="#8b949e">Jun</text>
            <text x="420" y="0" font-size="10" fill="#8b949e">Jul</text>
            <text x="490" y="0" font-size="10" fill="#8b949e">Aug</text>
            <text x="560" y="0" font-size="10" fill="#8b949e">Sep</text>
            <text x="630" y="0" font-size="10" fill="#8b949e">Oct</text>
            <text x="700" y="0" font-size="10" fill="#8b949e">Nov</text>
            <text x="770" y="0" font-size="10" fill="#8b949e">Dec</text>
          </g>

          <!-- Sample activity pattern -->
          <g transform="translate(30, 20)">
            <!-- Create boxes for each day of the year -->
            <rect x="0" y="0" width="12" height="12" rx="2" fill="#006d32" />
            <rect x="14" y="14" width="12" height="12" rx="2" fill="#0e4429" />
            <rect x="28" y="28" width="12" height="12" rx="2" fill="#26a641" />
            <rect x="42" y="42" width="12" height="12" rx="2" fill="#39d353" />
            <rect x="56" y="56" width="12" height="12" rx="2" fill="#0e4429" />
            <rect x="70" y="70" width="12" height="12" rx="2" fill="#26a641" />
            <rect x="84" y="84" width="12" height="12" rx="2" fill="#006d32" />
            <!-- Additional cells would be added here for a complete visualization -->
          </g>
        </svg>

        <!-- Legend -->
        <div class="flex items-center justify-end gap-2 mt-2 text-xs text-text-secondary">
          <span>Less</span>
          <div class="flex">
            <div class="w-3 h-3 bg-[#161b22] border border-border"></div>
            <div class="w-3 h-3 bg-[#0e4429]"></div>
            <div class="w-3 h-3 bg-[#006d32]"></div>
            <div class="w-3 h-3 bg-[#26a641]"></div>
            <div class="w-3 h-3 bg-[#39d353]"></div>
          </div>
          <span>More</span>
          <span class="ml-2">Writing activity</span>
        </div>
      `;
    }

    // Replace activity feed loading indicator with static HTML
    const activityFeedContainer = $("#activity-feed");
    if (activityFeedContainer) {
      activityFeedContainer.innerHTML = `
        <!-- Static activity feed -->
        <div class="gh-activity-feed">
          <!-- December 2024 Activity -->
          <div class="gh-activity-month">
            <div class="gh-activity-month-header">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
                <path d="M4.75 0a.75.75 0 01.75.75V2h5V.75a.75.75 0 011.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0113.25 16H2.75A1.75 1.75 0 011 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 014.75 0zm0 3.5h8.5a.25.25 0 01.25.25V6h-9V3.75a.25.25 0 01.25-.25zm-2 3h10.5v7.75a.25.25 0 01-.25.25H2.75a.25.25 0 01-.25-.25V6.5z"></path>
              </svg>
              <span>Dec 2024</span>
            </div>

            <ul class="gh-activity-list">
              <li class="gh-activity-item">
                <div class="gh-activity-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
                    <path d="M11.93 8.5a4.002 4.002 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 010 1.5z"></path>
                  </svg>
                </div>
                <div class="gh-activity-content">
                  <div class="gh-activity-title">
                    Published <a href="/posts/2024-12-13-ai-the-new-frontier-in-cybersecurity-opportunities-and-ethical-dilemmas/" class="gh-activity-link">AI: The New Frontier in Cybersecurity</a>
                  </div>
                  <div class="gh-activity-date">Dec 13, 2024</div>
                </div>
              </li>
            </ul>
          </div>

          <!-- October 2024 Activity -->
          <div class="gh-activity-month">
            <div class="gh-activity-month-header">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
                <path d="M4.75 0a.75.75 0 01.75.75V2h5V.75a.75.75 0 011.5 0V2h1.25c.966 0 1.75.784 1.75 1.75v10.5A1.75 1.75 0 0113.25 16H2.75A1.75 1.75 0 011 14.25V3.75C1 2.784 1.784 2 2.75 2H4V.75A.75.75 0 014.75 0zm0 3.5h8.5a.25.25 0 01.25.25V6h-9V3.75a.25.25 0 01.25-.25zm-2 3h10.5v7.75a.25.25 0 01-.25.25H2.75a.25.25 0 01-.25-.25V6.5z"></path>
              </svg>
              <span>Oct 2024</span>
            </div>

            <ul class="gh-activity-list">
              <li class="gh-activity-item">
                <div class="gh-activity-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor">
                    <path d="M11.93 8.5a4.002 4.002 0 01-7.86 0H.75a.75.75 0 010-1.5h3.32a4.002 4.002 0 017.86 0h3.32a.75.75 0 010 1.5z"></path>
                  </svg>
                </div>
                <div class="gh-activity-content">
                  <div class="gh-activity-title">
                    Published <a href="/posts/2024-10-19-pizza-calculator/" class="gh-activity-link">Pizza Calculator</a>
                  </div>
                  <div class="gh-activity-date">Oct 19, 2024</div>
                </div>
              </li>
            </ul>
          </div>

          <!-- View more link -->
          <div class="text-center mt-6">
            <a href="/blog/" class="gh-btn inline-flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" width="16" height="16" fill="currentColor" class="mr-1.5">
                <path d="M8 0a8 8 0 100 16A8 8 0 008 0zM1.5 8a6.5 6.5 0 1113 0 6.5 6.5 0 01-13 0z"></path>
                <path d="M9 11.75a.75.75 0 01-.75.75h-.5a.75.75 0 010-1.5h.5a.75.75 0 01.75.75zM9 8a.75.75 0 01-.75.75h-.5a.75.75 0 010-1.5h.5A.75.75 0 019 8zM8.25 5.75a.75.75 0 00-.5 1.5h.5a.75.75 0 000-1.5h-.5z"></path>
              </svg>
              View all blog posts
            </a>
          </div>
        </div>
      `;
    }
  });
}
