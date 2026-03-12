<script lang="ts">
  import { onMount } from 'svelte';

  interface PostData {
    title: string;
    date: string;
    tags: string[];
    wordCount: number;
    readingTime: number;
    hasCode: boolean;
  }

  interface StatsData {
    posts: PostData[];
    monthlyCounts: Record<string, number>;
    topTags: [string, number][];
    tagCounts: Record<string, number>;
    dayOfWeekCounts: number[];
    readingTimeBuckets: Record<string, number>;
    wordCountBuckets: Record<string, number>;
    tagByMonth: Record<string, Record<string, number>>;
    top5Tags: string[];
    heatmapData: Record<string, number>;
    scatterData: { wordCount: number; readingTime: number; title: string }[];
  }

  interface Props {
    statsData: StatsData;
  }

  let { statsData }: Props = $props();

  let currentYear = $state('all');
  let isDark = $state(false);

  let filteredPosts = $derived(
    currentYear === 'all' ? statsData.posts : statsData.posts.filter((p) => p.date.startsWith(currentYear))
  );

  let years = $derived(
    [...new Set(statsData.posts.map((p) => p.date.substring(0, 4)))].sort()
  );

  let totalWords = $derived(filteredPosts.reduce((s, p) => s + p.wordCount, 0));
  let uniqueTags = $derived([...new Set(filteredPosts.flatMap((p) => p.tags))]);
  let avgReading = $derived(
    filteredPosts.length > 0
      ? Math.round(filteredPosts.reduce((s, p) => s + p.readingTime, 0) / filteredPosts.length)
      : 0
  );
  let postsWithCode = $derived(filteredPosts.filter((p) => p.hasCode).length);
  let codePercent = $derived(
    filteredPosts.length > 0 ? ((postsWithCode / filteredPosts.length) * 100).toFixed(0) : '0'
  );

  // Monthly bar chart data
  let monthlyData = $derived.by(() => {
    const counts: Record<string, number> = {};
    filteredPosts.forEach((p) => {
      const m = p.date.substring(0, 7);
      counts[m] = (counts[m] || 0) + 1;
    });
    const entries = Object.entries(counts).sort(([a], [b]) => a.localeCompare(b));
    const max = Math.max(...entries.map(([, c]) => c), 1);
    return { entries, max };
  });

  // Top tags data
  let topTagsData = $derived.by(() => {
    const tc: Record<string, number> = {};
    filteredPosts.forEach((p) => p.tags.forEach((t) => { tc[t] = (tc[t] || 0) + 1; }));
    const entries = Object.entries(tc).sort((a, b) => b[1] - a[1]).slice(0, 10);
    const max = entries[0]?.[1] || 1;
    return { entries, max };
  });

  // Heatmap data
  const MONTHS = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
  const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const LIGHT_HEATMAP = ['#e8eaf0', '#8b9dc3', '#5b6fa8', '#3d4f7f', '#2a3a5c', '#1a2642'];
  const DARK_HEATMAP = ['#2a3241', '#5b6fa8', '#7b8fc8', '#9bafd8', '#bccfe8', '#d9e5f5'];
  const BAR_COLORS = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#84cc16'];

  let heatmapResult = $derived.by(() => {
    const data: Record<string, number> = {};
    filteredPosts.forEach((p) => {
      const d = new Date(p.date);
      const key = `${d.getFullYear()}-${d.getMonth()}`;
      data[key] = (data[key] || 0) + 1;
    });
    const hYears = [...new Set(filteredPosts.map((p) => new Date(p.date).getFullYear()))].sort();
    const maxCount = Math.max(...Object.values(data), 1);
    return { data, years: hYears, maxCount };
  });

  function getHeatmapColor(count: number, maxCount: number): string {
    const colors = isDark ? DARK_HEATMAP : LIGHT_HEATMAP;
    if (count === 0) return colors[0];
    const idx = Math.min(Math.floor((count / maxCount) * 5) + 1, 5);
    return colors[idx];
  }

  function formatMonth(ym: string): string {
    const [y, m] = ym.split('-');
    return `${MONTH_NAMES[parseInt(m) - 1]} ${y.slice(2)}`;
  }

  function switchYear(year: string) {
    currentYear = year;
  }

  function checkTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  onMount(() => {
    checkTheme();
    const observer = new MutationObserver(() => checkTheme());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => observer.disconnect();
  });
</script>

<!-- Year Filter -->
<nav aria-label="Year filter" class="filter-nav">
  <button
    class="filter-btn" class:active={currentYear === 'all'}
    aria-pressed={currentYear === 'all'}
    onclick={() => switchYear('all')}
  >All</button>
  {#each years as year}
    <button
      class="filter-btn" class:active={currentYear === year}
      aria-pressed={currentYear === year}
      onclick={() => switchYear(year)}
    >{year}</button>
  {/each}
</nav>

<!-- Summary Stats -->
<section class="stats-grid" aria-label="Summary statistics" aria-live="polite">
  <div class="stat-card">
    <span class="stat-label">Posts</span>
    <span class="stat-value">{filteredPosts.length}</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">Words</span>
    <span class="stat-value">{totalWords >= 1000 ? Math.round(totalWords / 1000) + 'k' : totalWords}</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">Tags</span>
    <span class="stat-value">{uniqueTags.length}</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">Avg Read</span>
    <span class="stat-value">{avgReading}m</span>
  </div>
  <div class="stat-card">
    <span class="stat-label">Code Posts</span>
    <span class="stat-value">{codePercent}%</span>
  </div>
</section>

<!-- Posts Over Time (CSS Bar Chart) -->
<section class="chart-section" aria-label="Posts published over time">
  <h2 class="chart-title">Posts Over Time</h2>
  <div class="bar-chart-vertical" role="img" aria-label="Monthly post count bar chart">
    {#each monthlyData.entries as [month, count]}
      <div class="bar-col" title="{formatMonth(month)}: {count} post{count !== 1 ? 's' : ''}">
        <div class="bar-fill" style="height: {(count / monthlyData.max) * 100}%"></div>
        <span class="bar-label">{count}</span>
      </div>
    {/each}
  </div>
  <div class="bar-chart-axis">
    {#each monthlyData.entries as [month], i}
      {#if i === 0 || i === monthlyData.entries.length - 1 || i === Math.floor(monthlyData.entries.length / 2)}
        <span style="position:absolute; left:{(i / (monthlyData.entries.length - 1)) * 100}%; transform:translateX(-50%)">{formatMonth(month)}</span>
      {/if}
    {/each}
  </div>
</section>

<!-- Top Tags (CSS Horizontal Bars) -->
<section class="chart-section" aria-label="Most used tags">
  <h2 class="chart-title">Top Tags</h2>
  <div class="h-bar-chart" role="list">
    {#each topTagsData.entries as [tag, count], i}
      <a href="/tags/{tag}/" class="h-bar-row" role="listitem">
        <span class="h-bar-label">{tag}</span>
        <div class="h-bar-track">
          <div class="h-bar-fill" style="width: {(count / topTagsData.max) * 100}%; background-color: {BAR_COLORS[i % BAR_COLORS.length]}"></div>
        </div>
        <span class="h-bar-value">{count}</span>
      </a>
    {/each}
  </div>
</section>

<!-- Activity Heatmap -->
<section class="chart-section" aria-label="Publishing activity heatmap">
  <h2 class="chart-title">Activity</h2>
  <div class="heatmap">
    <div class="heatmap-header">
      <div class="heatmap-year-label"></div>
      {#each MONTHS as m}
        <div class="heatmap-month-label">{m}</div>
      {/each}
    </div>
    {#each heatmapResult.years as year}
      <div class="heatmap-row">
        <div class="heatmap-year-label">{year}</div>
        {#each Array(12) as _, idx}
          {@const count = heatmapResult.data[`${year}-${idx}`] || 0}
          <div
            class="heatmap-cell"
            style="background-color: {getHeatmapColor(count, heatmapResult.maxCount)}"
            title="{MONTH_NAMES[idx]} {year}: {count} post{count !== 1 ? 's' : ''}"
            role="gridcell"
            aria-label="{MONTH_NAMES[idx]} {year}: {count} posts"
          >
            {#if count > 0}
              <span class="heatmap-count">{count}</span>
            {/if}
          </div>
        {/each}
      </div>
    {/each}
    <div class="heatmap-legend">
      <span>Less</span>
      {#each (isDark ? DARK_HEATMAP.slice(1) : LIGHT_HEATMAP.slice(1)) as color}
        <div class="heatmap-legend-swatch" style="background-color: {color}"></div>
      {/each}
      <span>More</span>
    </div>
  </div>
</section>

<style>
  /* ===== Base ===== */
  .filter-nav {
    display: flex;
    justify-content: center;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }
  .filter-btn {
    padding: 0.5rem 1rem;
    min-height: 44px;
    border-radius: 0.5rem;
    font-weight: 500;
    font-size: 0.875rem;
    background: var(--md-sys-color-surface-container);
    color: var(--md-sys-color-on-surface-variant);
    border: none;
    cursor: pointer;
    transition: all 0.15s;
  }
  .filter-btn.active {
    background: var(--md-sys-color-primary);
    color: var(--md-sys-color-on-primary);
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  }

  /* ===== Stats Grid ===== */
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.75rem;
    margin-bottom: 2rem;
  }
  .stat-card {
    background: var(--md-sys-color-surface-container);
    border-radius: 0.75rem;
    padding: 1rem;
    text-align: center;
  }
  .stat-label {
    display: block;
    font-size: 0.625rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--md-sys-color-on-surface-variant);
    margin-bottom: 0.25rem;
  }
  .stat-value {
    display: block;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--md-sys-color-on-surface);
  }

  /* ===== Chart Section ===== */
  .chart-section {
    background: var(--md-sys-color-surface-container);
    border-radius: 0.75rem;
    padding: 1.25rem;
    margin-bottom: 1.5rem;
  }
  .chart-title {
    font-size: 1.125rem;
    font-weight: 700;
    color: var(--md-sys-color-on-surface);
    margin: 0 0 1rem;
  }

  /* ===== Vertical Bar Chart (Posts Over Time) ===== */
  .bar-chart-vertical {
    display: flex;
    align-items: flex-end;
    gap: 2px;
    height: 160px;
    width: 100%;
    overflow-x: auto;
    padding-bottom: 0.25rem;
  }
  .bar-col {
    flex: 1;
    min-width: 8px;
    max-width: 28px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    height: 100%;
    cursor: default;
  }
  .bar-fill {
    width: 100%;
    background: var(--md-sys-color-primary);
    border-radius: 2px 2px 0 0;
    min-height: 2px;
    transition: height 0.3s ease;
  }
  .bar-col:hover .bar-fill {
    opacity: 0.8;
  }
  .bar-label {
    display: none;
  }
  .bar-col:hover .bar-label {
    display: block;
    font-size: 0.625rem;
    color: var(--md-sys-color-on-surface-variant);
    position: absolute;
    top: -1.25rem;
  }
  .bar-col {
    position: relative;
  }
  .bar-chart-axis {
    position: relative;
    height: 1.25rem;
    margin-top: 0.25rem;
    font-size: 0.625rem;
    color: var(--md-sys-color-on-surface-variant);
  }

  /* ===== Horizontal Bar Chart (Top Tags) ===== */
  .h-bar-chart {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .h-bar-row {
    display: grid;
    grid-template-columns: 7rem 1fr 2rem;
    gap: 0.5rem;
    align-items: center;
    text-decoration: none;
    color: inherit;
    min-height: 2rem;
  }
  .h-bar-row:hover {
    opacity: 0.85;
  }
  .h-bar-label {
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .h-bar-track {
    height: 1.25rem;
    background: var(--md-sys-color-surface-container-high);
    border-radius: 0.375rem;
    overflow: hidden;
  }
  .h-bar-fill {
    height: 100%;
    border-radius: 0.375rem;
    transition: width 0.4s ease;
  }
  .h-bar-value {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface-variant);
    text-align: right;
  }

  /* ===== Heatmap ===== */
  .heatmap {
    overflow-x: auto;
  }
  .heatmap-header, .heatmap-row {
    display: grid;
    grid-template-columns: 2.5rem repeat(12, 1fr);
    gap: 3px;
  }
  .heatmap-header {
    margin-bottom: 3px;
  }
  .heatmap-month-label {
    font-size: 0.625rem;
    text-align: center;
    color: var(--md-sys-color-on-surface-variant);
    font-weight: 500;
  }
  .heatmap-year-label {
    font-size: 0.6875rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface-variant);
    display: flex;
    align-items: center;
  }
  .heatmap-cell {
    aspect-ratio: 1;
    border-radius: 3px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s;
    cursor: default;
    min-height: 24px;
  }
  .heatmap-cell:hover {
    transform: scale(1.15);
    z-index: 1;
  }
  .heatmap-count {
    font-size: 0.625rem;
    font-weight: 700;
    color: var(--md-sys-color-on-surface);
    opacity: 0.8;
  }
  .heatmap-legend {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    margin-top: 0.75rem;
    font-size: 0.625rem;
    color: var(--md-sys-color-on-surface-variant);
  }
  .heatmap-legend-swatch {
    width: 1rem;
    height: 1rem;
    border-radius: 2px;
  }
  .heatmap-row {
    margin-bottom: 3px;
  }

  /* ===== Mobile Responsive ===== */
  @media (max-width: 480px) {
    .stats-grid {
      grid-template-columns: repeat(3, 1fr);
    }
    .stats-grid .stat-card:nth-child(4),
    .stats-grid .stat-card:nth-child(5) {
      grid-column: span 1;
    }
    .stat-value {
      font-size: 1.25rem;
    }
    .stat-label {
      font-size: 0.5625rem;
    }
    .h-bar-row {
      grid-template-columns: 5.5rem 1fr 1.75rem;
    }
    .h-bar-label {
      font-size: 0.75rem;
    }
    .chart-section {
      padding: 1rem;
    }
    .heatmap-year-label {
      font-size: 0.5625rem;
    }
    .heatmap-cell {
      min-height: 18px;
    }
    .heatmap-count {
      font-size: 0.5rem;
    }
    .bar-chart-vertical {
      height: 120px;
    }
  }

  @media (min-width: 640px) {
    .stats-grid {
      grid-template-columns: repeat(5, 1fr);
      gap: 1rem;
    }
    .stat-value {
      font-size: 2rem;
    }
    .stat-label {
      font-size: 0.75rem;
    }
    .stat-card {
      padding: 1.25rem;
    }
    .chart-section {
      padding: 1.5rem;
    }
    .chart-title {
      font-size: 1.25rem;
    }
    .bar-chart-vertical {
      height: 200px;
    }
    .heatmap-cell {
      min-height: 32px;
    }
  }

  @media (min-width: 1024px) {
    .stat-value {
      font-size: 2.5rem;
    }
    .bar-chart-vertical {
      height: 240px;
    }
    .heatmap-cell {
      min-height: 44px;
    }
    .h-bar-row {
      grid-template-columns: 9rem 1fr 2.5rem;
    }
  }
</style>
