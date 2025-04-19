/**
 * heatmap.js - GitHub-style Contribution Heatmap Generator
 *
 * This script creates a dynamic GitHub-style contribution heatmap based on blog post dates.
 * It generates an SVG visualization that shows contribution frequency with appropriate color coding.
 *
 * The data is expected to be available as a global variable 'contributionHeatmap', which
 * contains information about contributions (blog posts) per day.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Configuration
  const config = {
    cellSize: 11, // Size of each day cell in pixels
    cellRadius: 2, // Border radius of cells
    cellSpacing: 3, // Spacing between cells
    weekCount: 52, // Number of weeks to display (1 year)
    colors: {
      level0: "#161b22", // No contributions
      level1: "#0e4429", // 1 contribution
      level2: "#006d32", // 2 contributions
      level3: "#26a641", // 3 contributions
      level4: "#39d353", // 4+ contributions
    },
    months: [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ],
  };

  // Target element to render the heatmap
  const targetElement = document.getElementById("contribution-heatmap");
  if (!targetElement) return;

  // Check if data is available globally
  if (typeof contributionHeatmap === "undefined") {
    console.error(
      "Contribution data not found. Make sure contributionHeatmap is defined."
    );
    return;
  }

  // Create the heatmap
  createHeatmap(targetElement, contributionHeatmap, config);
});

/**
 * Creates the contribution heatmap visualization
 * @param {HTMLElement} container - The container element to render the heatmap
 * @param {Object} data - The contribution data
 * @param {Object} config - Configuration options
 */
function createHeatmap(container, data, config) {
  // Calculate dimensions
  const totalWidth = (config.cellSize + config.cellSpacing) * config.weekCount;
  const totalHeight = (config.cellSize + config.cellSpacing) * 7 + 30; // Extra space for month labels

  // Create SVG element
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("width", totalWidth);
  svg.setAttribute("height", totalHeight);
  svg.setAttribute("class", "contribution-graph");

  // Get the current date and calculate dates for the last year
  const today = new Date();
  const oneYearAgo = new Date(today);
  oneYearAgo.setFullYear(today.getFullYear() - 1);

  // Create a map of dates to contribution counts
  const contributionMap = createContributionMap(data);

  // Add month labels
  addMonthLabels(svg, oneYearAgo, config);

  // Add day of week labels
  addDayLabels(svg, config);

  // Generate cells for each day
  generateDayCells(svg, oneYearAgo, today, contributionMap, config);

  // Add legend
  addLegend(svg, config, totalWidth, totalHeight);

  // Add the SVG to the container
  container.innerHTML = "";
  container.appendChild(svg);
}

/**
 * Creates a mapping of ISO date strings to contribution counts
 * @param {Object} data - The contribution data
 * @returns {Map} A map of dates to contribution counts
 */
function createContributionMap(data) {
  const map = new Map();

  // Process the contribution data
  if (data && data.contributions) {
    data.contributions.forEach((item) => {
      if (item.date && item.count !== undefined) {
        map.set(item.date, item.count);
      }
    });
  }

  return map;
}

/**
 * Adds month labels to the top of the heatmap
 * @param {SVGElement} svg - The SVG element
 * @param {Date} startDate - The start date for the heatmap
 * @param {Object} config - Configuration options
 */
function addMonthLabels(svg, startDate, config) {
  const startMonth = startDate.getMonth();
  const monthLabels = document.createElementNS("http://www.w3.org/2000/svg", "g");

  // Loop through each month in the year
  for (let month = 0; month < 12; month++) {
    const monthIndex = (startMonth + month) % 12;

    // Calculate position for the month label
    const weeksSinceStart = Math.floor((month * 30.5) / 7);
    const x = weeksSinceStart * (config.cellSize + config.cellSpacing);

    // Create text element for month label
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.textContent = config.months[monthIndex];
    text.setAttribute("x", x);
    text.setAttribute("y", 10);
    text.setAttribute("font-size", "12");
    text.setAttribute("fill", "#8b949e");

    monthLabels.appendChild(text);
  }

  svg.appendChild(monthLabels);
}

/**
 * Adds day of week labels to the left side of the heatmap
 * @param {SVGElement} svg - The SVG element
 * @param {Object} config - Configuration options
 */
function addDayLabels(svg, config) {
  const dayLabels = ["", "Mon", "", "Wed", "", "Fri", ""]; // Only show Mon, Wed, Fri
  const dayLabelGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");

  // Create text element for each day label
  dayLabels.forEach((day, index) => {
    if (day) {
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.textContent = day;
      text.setAttribute("x", -30); // Position to the left of the heatmap
      text.setAttribute(
        "y",
        20 + (config.cellSize + config.cellSpacing) * index + config.cellSize / 2 + 4
      );
      text.setAttribute("font-size", "10");
      text.setAttribute("fill", "#8b949e");
      text.setAttribute("text-anchor", "start");

      dayLabelGroup.appendChild(text);
    }
  });

  svg.appendChild(dayLabelGroup);
}

/**
 * Generates cells for each day in the date range
 * @param {SVGElement} svg - The SVG element
 * @param {Date} startDate - The start date for the heatmap
 * @param {Date} endDate - The end date for the heatmap
 * @param {Map} contributionMap - Mapping of dates to contribution counts
 * @param {Object} config - Configuration options
 */
function generateDayCells(svg, startDate, endDate, contributionMap, config) {
  const cellGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  cellGroup.setAttribute("transform", "translate(0, 20)"); // Move down to make room for month labels

  // Clone the start date so we don't modify the original
  const currentDate = new Date(startDate);

  // Loop through each day between start and end dates
  while (currentDate <= endDate) {
    // Get the day of the week (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
    const dayOfWeek = currentDate.getDay();

    // Calculate the position of this day's cell
    const daysSinceStart = Math.floor(
      (currentDate - startDate) / (24 * 60 * 60 * 1000)
    );
    const weekIndex = Math.floor(daysSinceStart / 7);

    // Skip if we've exceeded the maximum number of weeks to display
    if (weekIndex >= config.weekCount) {
      currentDate.setDate(currentDate.getDate() + 1);
      continue;
    }

    const x = weekIndex * (config.cellSize + config.cellSpacing);
    const y = dayOfWeek * (config.cellSize + config.cellSpacing);

    // Format the date as ISO string (YYYY-MM-DD)
    const dateKey = currentDate.toISOString().split("T")[0];

    // Get contribution count for this day (default to 0)
    const count = contributionMap.get(dateKey) || 0;

    // Determine color based on contribution count
    let fillColor = config.colors.level0; // Default: no contributions
    if (count === 1) fillColor = config.colors.level1;
    else if (count === 2) fillColor = config.colors.level2;
    else if (count === 3) fillColor = config.colors.level3;
    else if (count >= 4) fillColor = config.colors.level4;

    // Create the cell
    const cell = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    cell.setAttribute("x", x);
    cell.setAttribute("y", y);
    cell.setAttribute("width", config.cellSize);
    cell.setAttribute("height", config.cellSize);
    cell.setAttribute("rx", config.cellRadius);
    cell.setAttribute("ry", config.cellRadius);
    cell.setAttribute("fill", fillColor);

    // Create tooltip data
    const formattedDate = formatDate(currentDate);
    const tooltipText = `${count} contribution${count !== 1 ? "s" : ""} on ${formattedDate}`;
    cell.setAttribute("data-date", formattedDate);
    cell.setAttribute("data-count", count);
    cell.setAttribute("data-tooltip", tooltipText);

    // Add hover effects and tooltip functionality
    cell.setAttribute("class", "contribution-cell");

    cellGroup.appendChild(cell);

    // Move to the next day
    currentDate.setDate(currentDate.getDate() + 1);
  }

  svg.appendChild(cellGroup);

  // Add tooltip functionality
  addTooltipFunctionality();
}

/**
 * Formats a date as a human-readable string
 * @param {Date} date - The date to format
 * @returns {string} Formatted date string (e.g., "Apr 5, 2025")
 */
function formatDate(date) {
  const months = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
  ];
  return `${months[date.getMonth()]} ${date.getDate()}, ${date.getFullYear()}`;
}

/**
 * Adds tooltip functionality to the heatmap cells
 */
function addTooltipFunctionality() {
  // Create tooltip element if it doesn't exist
  let tooltip = document.getElementById("contribution-tooltip");
  if (!tooltip) {
    tooltip = document.createElement("div");
    tooltip.id = "contribution-tooltip";
    tooltip.className = "contribution-tooltip";
    tooltip.style.position = "absolute";
    tooltip.style.padding = "8px 10px";
    tooltip.style.backgroundColor = "#1b1f23";
    tooltip.style.color = "#ffffff";
    tooltip.style.borderRadius = "6px";
    tooltip.style.fontSize = "12px";
    tooltip.style.boxShadow = "0 4px 10px rgba(0, 0, 0, 0.5)";
    tooltip.style.pointerEvents = "none";
    tooltip.style.opacity = "0";
    tooltip.style.transition = "opacity 0.15s ease-in-out";
    tooltip.style.zIndex = "1000";
    document.body.appendChild(tooltip);
  }

  // Add event listeners to cells
  const cells = document.querySelectorAll(".contribution-cell");
  cells.forEach((cell) => {
    cell.addEventListener("mouseenter", (e) => {
      const tooltipText = e.target.getAttribute("data-tooltip");
      tooltip.textContent = tooltipText;
      tooltip.style.opacity = "1";

      // Position the tooltip near the cell
      const rect = e.target.getBoundingClientRect();
      tooltip.style.left = `${rect.left + window.scrollX - tooltip.offsetWidth / 2 + rect.width / 2}px`;
      tooltip.style.top = `${rect.top + window.scrollY - tooltip.offsetHeight - 5}px`;
    });

    cell.addEventListener("mouseleave", () => {
      tooltip.style.opacity = "0";
    });
  });
}

/**
 * Adds a color legend to the bottom of the heatmap
 * @param {SVGElement} svg - The SVG element
 * @param {Object} config - Configuration options
 * @param {number} totalWidth - Total width of the SVG
 * @param {number} totalHeight - Total height of the SVG
 */
function addLegend(svg, config, totalWidth, totalHeight) {
  const legendGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
  legendGroup.setAttribute(
    "transform",
    `translate(${totalWidth - 250}, ${totalHeight - 20})`
  );

  // Add "Less" label
  const lessText = document.createElementNS("http://www.w3.org/2000/svg", "text");
  lessText.textContent = "Less";
  lessText.setAttribute("x", 0);
  lessText.setAttribute("y", 10);
  lessText.setAttribute("font-size", "10");
  lessText.setAttribute("fill", "#8b949e");
  legendGroup.appendChild(lessText);

  // Add color boxes
  const colors = [
    config.colors.level0,
    config.colors.level1,
    config.colors.level2,
    config.colors.level3,
    config.colors.level4,
  ];

  colors.forEach((color, index) => {
    const x = 30 + index * 15;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", x);
    rect.setAttribute("y", 0);
    rect.setAttribute("width", 10);
    rect.setAttribute("height", 10);
    rect.setAttribute("rx", 2);
    rect.setAttribute("ry", 2);
    rect.setAttribute("fill", color);

    legendGroup.appendChild(rect);
  });

  // Add "More" label
  const moreText = document.createElementNS("http://www.w3.org/2000/svg", "text");
  moreText.textContent = "More";
  moreText.setAttribute("x", 105);
  moreText.setAttribute("y", 10);
  moreText.setAttribute("font-size", "10");
  moreText.setAttribute("fill", "#8b949e");
  legendGroup.appendChild(moreText);

  svg.appendChild(legendGroup);
}

/**
 * Add CSS styles for the heatmap
 */
function addHeatmapStyles() {
  // Add styles if they don't already exist
  if (!document.getElementById("contribution-heatmap-styles")) {
    const styleElement = document.createElement("style");
    styleElement.id = "contribution-heatmap-styles";
    styleElement.textContent = `
      .contribution-cell {
        transition: 0.1s ease-in-out;
      }
      .contribution-cell:hover {
        stroke: #8b949e;
        stroke-width: 1px;
      }
      .contribution-tooltip {
        pointer-events: none;
      }
    `;
    document.head.appendChild(styleElement);
  }
}

// Initialize
addHeatmapStyles();
