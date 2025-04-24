/**
 * heatmap.js - GitHub-style contribution heatmap
 */

(function () {
  // Map to convert contribution count to intensity level
  const INTENSITY_LEVELS = {
    0: 0, // No contributions
    1: 1, // 1-3 contributions
    4: 2, // 4-7 contributions
    8: 3, // 8-12 contributions
    13: 4, // 13+ contributions
  };

  /**
   * Initialize contribution heatmap
   */
  function initHeatmap() {
    const heatmap = document.getElementById("contribution-heatmap");
    if (!heatmap) return;

    fetchHeatmapData()
      .then((data) => renderHeatmap(heatmap, data))
      .catch((err) => {
        console.error("Error loading heatmap data:", err);
        renderFallbackHeatmap(heatmap);
      });
  }

  /**
   * Fetch contribution data
   */
  function fetchHeatmapData() {
    return new Promise((resolve, reject) => {
      // Try to load from data attribute first
      const dataElement = document.getElementById("heatmap-data");
      if (dataElement && dataElement.textContent) {
        try {
          const data = JSON.parse(dataElement.textContent);
          return resolve(data);
        } catch (e) {
          console.warn("Invalid heatmap data:", e);
        }
      }

      // Otherwise load from API
      fetch("/assets/data/contribution-heatmap.json")
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
        })
        .then((data) => resolve(data))
        .catch((err) => reject(err));
    });
  }

  /**
   * Render the contribution heatmap
   */
  function renderHeatmap(container, data) {
    // Clear container
    container.innerHTML = "";

    // Extract contribution data and dates
    const contributions = data.contributions || {};

    // Get all dates in the last year
    const today = new Date();
    const dates = [];
    for (let i = 364; i >= 0; i--) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      const dateStr = formatDate(date);
      dates.push({
        date: dateStr,
        count: contributions[dateStr] || 0,
        dayOfWeek: date.getDay(),
      });
    }

    // Group dates by week
    const weeks = [];
    let currentWeek = [];

    for (let i = 0; i < dates.length; i++) {
      const date = dates[i];

      // Start a new week on Sunday (day 0)
      if (date.dayOfWeek === 0 && currentWeek.length > 0) {
        weeks.push(currentWeek);
        currentWeek = [];
      }

      currentWeek.push(date);

      // Add the last week
      if (i === dates.length - 1) {
        weeks.push(currentWeek);
      }
    }

    // Create SVG element
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.classList.add("contribution-graph");
    svg.setAttribute("width", "100%");
    svg.setAttribute("height", "120px");
    svg.setAttribute("viewBox", `0 0 ${weeks.length * 14} 120`);

    // Add days of week labels
    const daysOfWeek = ["", "Mon", "", "Wed", "", "Fri", ""];
    daysOfWeek.forEach((day, i) => {
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.textContent = day;
      text.setAttribute("x", "0");
      text.setAttribute("y", i * 12 + 20);
      text.classList.add("heatmap-label");
      svg.appendChild(text);
    });

    // Add cells for each day
    weeks.forEach((week, weekIndex) => {
      week.forEach((day) => {
        const intensity = getIntensityLevel(day.count);

        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("x", weekIndex * 14 + 20);
        rect.setAttribute("y", day.dayOfWeek * 12 + 10);
        rect.setAttribute("width", 10);
        rect.setAttribute("height", 10);
        rect.setAttribute("rx", 2);
        rect.classList.add("contribution-cell");
        rect.classList.add(`contribution-level-${intensity}`);

        // Add tooltip data
        rect.setAttribute("data-date", day.date);
        rect.setAttribute("data-count", day.count);

        // Add title for tooltip
        const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
        title.textContent = `${day.count} contributions on ${formatDateForDisplay(day.date)}`;
        rect.appendChild(title);

        svg.appendChild(rect);
      });
    });

    // Add the SVG to the container
    container.appendChild(svg);

    // Add month labels
    const monthLabels = document.createElement("div");
    monthLabels.className = "month-labels";

    // Get unique months in the data
    const months = [];
    const monthNames = [
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

    dates.forEach((day) => {
      const date = new Date(day.date);
      const monthKey = `${date.getFullYear()}-${date.getMonth()}`;

      if (!months.some((m) => m.key === monthKey)) {
        months.push({
          key: monthKey,
          name: monthNames[date.getMonth()],
          position: weeks.findIndex((week) => {
            return week.some((d) => {
              const dDate = new Date(d.date);
              return (
                dDate.getFullYear() === date.getFullYear() &&
                dDate.getMonth() === date.getMonth()
              );
            });
          }),
        });
      }
    });

    // Only show a subset of months to avoid overcrowding
    const filteredMonths = months.filter(
      (_, i) => i % 2 === 0 || i === months.length - 1
    );

    filteredMonths.forEach((month) => {
      const label = document.createElement("div");
      label.className = "month-label";
      label.textContent = month.name;
      label.style.left = `${month.position * 14 + 20}px`;
      monthLabels.appendChild(label);
    });

    container.appendChild(monthLabels);

    // Add legend
    const legend = document.createElement("div");
    legend.className = "contribution-legend";

    const legendTitle = document.createElement("span");
    legendTitle.className = "legend-title";
    legendTitle.textContent = "Less";
    legend.appendChild(legendTitle);

    for (let i = 0; i < 5; i++) {
      const box = document.createElement("span");
      box.className = `legend-box contribution-level-${i}`;
      legend.appendChild(box);
    }

    const legendEndTitle = document.createElement("span");
    legendEndTitle.className = "legend-title";
    legendEndTitle.textContent = "More";
    legend.appendChild(legendEndTitle);

    container.appendChild(legend);
  }

  /**
   * Render a fallback heatmap when data can't be loaded
   */
  function renderFallbackHeatmap(container) {
    container.innerHTML =
      '<div class="fallback-message">Contribution data could not be loaded</div>';
  }

  /**
   * Get intensity level based on contribution count
   */
  function getIntensityLevel(count) {
    if (count === 0) return 0;

    for (const threshold of [13, 8, 4, 1]) {
      if (count >= threshold) {
        return INTENSITY_LEVELS[threshold];
      }
    }

    return 0;
  }

  /**
   * Format date as YYYY-MM-DD
   */
  function formatDate(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");
    return `${year}-${month}-${day}`;
  }

  /**
   * Format date for display
   */
  function formatDateForDisplay(dateStr) {
    const date = new Date(dateStr);
    const options = { weekday: "long", year: "numeric", month: "long", day: "numeric" };
    return date.toLocaleDateString(undefined, options);
  }

  // Initialize when DOM is ready
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHeatmap);
  } else {
    initHeatmap();
  }
})();
