/**
 * Generate a GitHub-style contribution heatmap based on blog post dates
 */
function generateContributionHeatmap(postDates) {
  // Constants for the heatmap
  const CELL_SIZE = 12;
  const CELL_PADDING = 2;
  const MONTH_LABELS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const DAY_LABELS = ['', 'Mon', '', 'Wed', '', 'Fri', ''];
  const INTENSITY_COLORS = [
    '#161b22', // No contributions - same as background
    '#0e4429', // Light - level 1
    '#006d32', // Medium - level 2
    '#26a641', // Heavy - level 3
    '#39d353'  // Very heavy - level 4
  ];
  const WEEKS_IN_YEAR = 53;
  const DAYS_IN_WEEK = 7;

  // Calculate date range: go back 1 year from today
  const endDate = new Date();
  const startDate = new Date();
  startDate.setFullYear(endDate.getFullYear() - 1);
  
  // Create an object to count posts per date
  const dateCounts = {};
  
  // Count posts per day
  postDates.forEach(date => {
    const dateStr = date.toISOString().split('T')[0];
    dateCounts[dateStr] = (dateCounts[dateStr] || 0) + 1;
  });
  
  // Fill in the date range with all dates, including those with no posts
  let currentDate = new Date(startDate);
  while (currentDate <= endDate) {
    const dateStr = currentDate.toISOString().split('T')[0];
    if (!dateCounts[dateStr]) {
      dateCounts[dateStr] = 0;
    }
    currentDate.setDate(currentDate.getDate() + 1);
  }

  // Determine max contributions for scaling the color intensity
  const counts = Object.values(dateCounts);
  const maxCount = Math.max(...counts, 1); // Ensure we don't divide by zero
  
  // Create SVG
  const svgWidth = (CELL_SIZE + CELL_PADDING) * WEEKS_IN_YEAR + 30; // Add extra for month labels
  const svgHeight = (CELL_SIZE + CELL_PADDING) * DAYS_IN_WEEK + 30; // Add extra for day labels
  
  let svg = `<svg width="100%" height="140" viewBox="0 0 ${svgWidth} ${svgHeight}" 
              class="contribution-graph" xmlns="http://www.w3.org/2000/svg">`;
  
  // Add day labels (Mon, Wed, Fri)
  svg += '<g transform="translate(0, 20)">';
  DAY_LABELS.forEach((day, i) => {
    if (day) { // Only add labels for Mon, Wed, Fri
      svg += `<text x="10" y="${(CELL_SIZE + CELL_PADDING) * i + CELL_SIZE / 2}" 
              font-size="9" fill="#8b949e" text-anchor="middle" dominant-baseline="middle">${day}</text>`;
    }
  });
  svg += '</g>';
  
  // Generate the cells for each date
  svg += '<g transform="translate(30, 20)">';
  
  // Iterate through each week
  for (let week = 0; week < WEEKS_IN_YEAR; week++) {
    // Iterate through each day of the week
    for (let day = 0; day < DAYS_IN_WEEK; day++) {
      const date = new Date(startDate);
      date.setDate(date.getDate() + (week * 7) + day);
      
      // Skip dates outside the range
      if (date < startDate || date > endDate) continue;
      
      const dateStr = date.toISOString().split('T')[0];
      const count = dateCounts[dateStr] || 0;
      
      // Determine color based on contribution count
      let colorIndex;
      if (count === 0) colorIndex = 0;
      else if (count <= maxCount * 0.25) colorIndex = 1;
      else if (count <= maxCount * 0.5) colorIndex = 2;
      else if (count <= maxCount * 0.75) colorIndex = 3;
      else colorIndex = 4;
      
      const x = week * (CELL_SIZE + CELL_PADDING);
      const y = day * (CELL_SIZE + CELL_PADDING);
      
      // Add tooltip data
      const tooltipDate = date.toLocaleDateString('en-US', { 
        weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' 
      });
      const tooltipCount = count === 1 ? "1 post" : `${count} posts`;
      
      svg += `<rect x="${x}" y="${y}" width="${CELL_SIZE}" height="${CELL_SIZE}" 
              fill="${INTENSITY_COLORS[colorIndex]}" rx="2" ry="2"
              data-date="${dateStr}" data-count="${count}"
              class="contribution-cell">
              <title>${tooltipDate}: ${tooltipCount}</title>
              </rect>`;
    }
  }
  svg += '</g>';
  
  // Add month labels
  svg += '<g transform="translate(30, 10)">';
  let currentMonth = -1;
  for (let week = 0; week < WEEKS_IN_YEAR; week++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + (week * 7));
    const month = date.getMonth();
    
    if (month !== currentMonth) {
      currentMonth = month;
      const x = week * (CELL_SIZE + CELL_PADDING);
      svg += `<text x="${x}" y="0" font-size="10" fill="#8b949e">${MONTH_LABELS[month]}</text>`;
    }
  }
  svg += '</g>';
  
  // Close SVG
  svg += '</svg>';
  
  return svg;
}

// Function to parse dates from Eleventy collection
function parsePostDates(posts) {
  return posts.map(post => new Date(post.date));
}

// Initialize the heatmap when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // Check if the contributions container exists
  const contributionsContainer = document.getElementById('contributions-heatmap');
  if (!contributionsContainer) return;
  
  // Check if postsData is available (will be injected by template)
  if (typeof postsData === 'undefined' || !Array.isArray(postsData)) return;
  
  // Parse dates and generate heatmap
  const dates = parsePostDates(postsData);
  const heatmapSvg = generateContributionHeatmap(dates);
  
  // Insert the heatmap into the container
  contributionsContainer.innerHTML = heatmapSvg;
  
  // Add legend
  const legend = document.createElement('div');
  legend.className = 'flex items-center justify-end gap-2 mt-2 text-xs text-text-secondary';
  legend.innerHTML = `
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
  `;
  
  contributionsContainer.appendChild(legend);
});