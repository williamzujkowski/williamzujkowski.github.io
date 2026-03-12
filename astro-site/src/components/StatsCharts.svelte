<script lang="ts">
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import { scaleBand, scaleLinear, scaleSequential } from 'd3-scale';
  import { timeFormat } from 'd3-time-format';
  import { max as d3Max } from 'd3-array';

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
    heatmapData: Record<string, number>;
  }

  interface Props {
    statsData: StatsData;
  }

  interface TooltipState {
    text: string;
    x: number;
    y: number;
    visible: boolean;
  }

  let { statsData }: Props = $props();

  // --- State ---
  let currentYear = $state('all');
  let isDark = $state(false);
  let barChartWidth = $state(600);
  let heatmapWidth = $state(600);
  let barChartEl: HTMLDivElement | undefined = $state(undefined);
  let heatmapEl: HTMLDivElement | undefined = $state(undefined);
  let tooltip = $state<TooltipState>({ text: '', x: 0, y: 0, visible: false });

  // Reduced motion
  const prefersReducedMotion = typeof window !== 'undefined'
    && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ANIM_DURATION = prefersReducedMotion ? 0 : 400;

  // Animation progress (0→1) for mount + year filter transitions
  const animProgress = tweened(0, { duration: ANIM_DURATION, easing: cubicOut });

  // --- Derived data ---
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
    const maxVal = d3Max(entries, (d) => d[1]) ?? 1;
    return { entries, max: maxVal };
  });

  // Top tags data
  let topTagsData = $derived.by(() => {
    const tc: Record<string, number> = {};
    filteredPosts.forEach((p) => p.tags.forEach((t) => { tc[t] = (tc[t] || 0) + 1; }));
    const entries = Object.entries(tc).sort((a, b) => b[1] - a[1]).slice(0, 10);
    const maxVal = entries[0]?.[1] ?? 1;
    return { entries, max: maxVal };
  });

  // Heatmap data
  const MONTHS = ['J', 'F', 'M', 'A', 'M', 'J', 'J', 'A', 'S', 'O', 'N', 'D'];
  const MONTH_NAMES = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  let heatmapResult = $derived.by(() => {
    const data: Record<string, number> = {};
    filteredPosts.forEach((p) => {
      const d = new Date(p.date);
      const key = `${d.getFullYear()}-${d.getMonth()}`;
      data[key] = (data[key] || 0) + 1;
    });
    const hYears = [...new Set(filteredPosts.map((p) => new Date(p.date).getFullYear()))].sort();
    const maxCount = d3Max(Object.values(data)) ?? 1;
    return { data, years: hYears, maxCount };
  });

  // --- D3 Scales ---
  const MARGIN = { top: 12, right: 12, bottom: 28, left: 36 };
  const BAR_CHART_HEIGHT = 220;

  let barScaleX = $derived(
    scaleBand<string>()
      .domain(monthlyData.entries.map(([m]) => m))
      .range([MARGIN.left, barChartWidth - MARGIN.right])
      .padding(0.15)
  );

  let barScaleY = $derived(
    scaleLinear()
      .domain([0, monthlyData.max])
      .range([BAR_CHART_HEIGHT - MARGIN.bottom, MARGIN.top])
      .nice()
  );

  // Sparse x-axis tick indices for bar chart
  let barTickIndices = $derived.by(() => {
    const len = monthlyData.entries.length;
    if (len <= 6) return monthlyData.entries.map((_, i) => i);
    const step = Math.max(1, Math.floor(len / 5));
    const indices: number[] = [0];
    for (let i = step; i < len - 1; i += step) indices.push(i);
    if (indices[indices.length - 1] !== len - 1) indices.push(len - 1);
    return indices;
  });

  // Horizontal bar scale (full width track = 100% of available)
  let hBarScaleX = $derived(
    scaleLinear()
      .domain([0, topTagsData.max])
      .range([0, 100]) // percentage
  );

  // Heatmap color scale using OKLCH
  function oklchLight(t: number): string {
    const l = 0.92 - t * 0.55;
    const c = 0.02 + t * 0.14;
    return `oklch(${l.toFixed(3)} ${c.toFixed(3)} 260)`;
  }

  function oklchDark(t: number): string {
    const l = 0.28 + t * 0.50;
    const c = 0.02 + t * 0.14;
    return `oklch(${l.toFixed(3)} ${c.toFixed(3)} 260)`;
  }

  let heatmapColorScale = $derived(
    scaleSequential()
      .domain([0, heatmapResult.maxCount])
      .interpolator(isDark ? oklchDark : oklchLight)
  );

  // OKLCH tag colors — evenly spaced hues
  function getTagColor(index: number, total: number): string {
    const hue = (index / Math.max(total, 1)) * 330 + 250; // start from indigo, wrap
    return isDark
      ? `oklch(0.74 0.14 ${hue % 360})`
      : `oklch(0.56 0.17 ${hue % 360})`;
  }

  // Heatmap cell sizing
  let heatmapCellSize = $derived(Math.max(18, Math.min(44, (heatmapWidth - 48) / 13)));
  let heatmapGap = $derived(Math.max(2, heatmapCellSize * 0.08));
  let heatmapLabelW = $derived(Math.max(28, heatmapCellSize * 0.9));

  // Heatmap SVG dimensions
  const HEATMAP_HEADER_H = 20;
  let heatmapTotalH = $derived(HEATMAP_HEADER_H + heatmapResult.years.length * (heatmapCellSize + heatmapGap) + 36);

  // Legend positioning
  let legendY = $derived(HEATMAP_HEADER_H + heatmapResult.years.length * (heatmapCellSize + heatmapGap) + 8);
  let legendCenterX = $derived(heatmapWidth / 2);
  const SWATCH_SIZE = 14;
  const LEGEND_GAP = 3;
  const LEGEND_STEPS = 5;
  let legendTotalW = $derived(LEGEND_STEPS * (SWATCH_SIZE + LEGEND_GAP) + 60);

  // --- Effects (animate on data change) ---
  // Track data identity to re-trigger animation on year filter change
  let prevYear = '';
  $effect(() => {
    const yr = currentYear;
    if (yr !== prevYear) {
      prevYear = yr;
      animProgress.set(0, { duration: 0 });
      animProgress.set(1);
    }
  });

  // --- Helpers ---
  const fmtMonth = timeFormat('%b %y');
  function formatMonth(ym: string): string {
    const [y, m] = ym.split('-');
    return `${MONTH_NAMES[parseInt(m) - 1]} '${y.slice(2)}`;
  }

  function showTooltip(event: MouseEvent, text: string): void {
    const container = (event.currentTarget as SVGElement).closest('.chart-container');
    if (!container) return;
    const rect = container.getBoundingClientRect();
    tooltip = {
      text,
      x: event.clientX - rect.left + 12,
      y: event.clientY - rect.top - 8,
      visible: true,
    };
  }

  function hideTooltip(): void {
    tooltip = { ...tooltip, visible: false };
  }

  function switchYear(year: string) {
    currentYear = year;
  }

  function checkTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  onMount(() => {
    checkTheme();
    // Trigger mount animation
    prevYear = currentYear;
    animProgress.set(1);

    const observer = new MutationObserver(() => checkTheme());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.target === barChartEl) barChartWidth = entry.contentRect.width;
        if (entry.target === heatmapEl) heatmapWidth = entry.contentRect.width;
      }
    });
    if (barChartEl) ro.observe(barChartEl);
    if (heatmapEl) ro.observe(heatmapEl);

    return () => { observer.disconnect(); ro.disconnect(); };
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

<!-- Posts Over Time (D3-scaled SVG) -->
<section class="chart-section" aria-label="Posts published over time">
  <h2 class="chart-title">Posts Over Time</h2>
  <div class="chart-container" bind:this={barChartEl}>
    <svg
      width={barChartWidth}
      height={BAR_CHART_HEIGHT}
      role="img"
      aria-label="Monthly post count bar chart"
    >
      <!-- Y-axis grid lines + labels -->
      {#each barScaleY.ticks(4) as tick}
        <line
          x1={MARGIN.left}
          x2={barChartWidth - MARGIN.right}
          y1={barScaleY(tick)}
          y2={barScaleY(tick)}
          class="grid-line"
        />
        {#if tick > 0}
          <text
            x={MARGIN.left - 6}
            y={barScaleY(tick)}
            class="axis-label"
            text-anchor="end"
            dominant-baseline="middle"
          >{tick}</text>
        {/if}
      {/each}

      <!-- Bars (animated via progress) -->
      {#each monthlyData.entries as [month, count], i}
        {@const tweenVal = count * $animProgress}
        {@const barY = barScaleY(tweenVal)}
        {@const barH = barScaleY(0) - barY}
        <rect
          x={barScaleX(month) ?? 0}
          y={barY}
          width={barScaleX.bandwidth()}
          height={Math.max(0, barH)}
          rx={2}
          class="bar-rect"
          role="graphics-symbol"
          aria-label="{formatMonth(month)}: {count} posts"
          onmouseenter={(e) => showTooltip(e, `${formatMonth(month)}: ${count} post${count !== 1 ? 's' : ''}`)}
          onmouseleave={hideTooltip}
        />
      {/each}

      <!-- X-axis labels (sparse) -->
      {#each barTickIndices as idx}
        {@const entry = monthlyData.entries[idx]}
        {#if entry}
          <text
            x={(barScaleX(entry[0]) ?? 0) + barScaleX.bandwidth() / 2}
            y={BAR_CHART_HEIGHT - 6}
            class="axis-label"
            text-anchor="middle"
          >{formatMonth(entry[0])}</text>
        {/if}
      {/each}
    </svg>

    <!-- Tooltip -->
    {#if tooltip.visible}
      <div class="chart-tooltip" style="left:{tooltip.x}px; top:{tooltip.y}px">
        {tooltip.text}
      </div>
    {/if}
  </div>
</section>

<!-- Top Tags (Hybrid HTML/SVG) -->
<section class="chart-section" aria-label="Most used tags">
  <h2 class="chart-title">Top Tags</h2>
  <div class="h-bar-chart" role="list">
    {#each topTagsData.entries as [tag, count], i}
      <a href="/tags/{tag}/" class="h-bar-row" role="listitem">
        <span class="h-bar-label">{tag}</span>
        <div class="h-bar-track">
          <div
            class="h-bar-fill"
            style="width: {hBarScaleX(count * $animProgress)}%; background-color: {getTagColor(i, topTagsData.entries.length)}"
          ></div>
        </div>
        <span class="h-bar-value">{count}</span>
      </a>
    {/each}
  </div>
</section>

<!-- Activity Heatmap (D3-scaled SVG) -->
<section class="chart-section" aria-label="Publishing activity heatmap">
  <h2 class="chart-title">Activity</h2>
  <div class="chart-container" bind:this={heatmapEl}>
    <svg
      width={heatmapWidth}
      height={heatmapTotalH}
      role="grid"
      aria-label="Publishing activity heatmap"
    >
      <!-- Month headers -->
      {#each MONTHS as m, mi}
        <text
          x={heatmapLabelW + mi * (heatmapCellSize + heatmapGap) + heatmapCellSize / 2}
          y={14}
          class="axis-label"
          text-anchor="middle"
        >{m}</text>
      {/each}

      <!-- Year rows -->
      {#each heatmapResult.years as year, yi}
        <text
          x={heatmapLabelW - 6}
          y={HEATMAP_HEADER_H + yi * (heatmapCellSize + heatmapGap) + heatmapCellSize / 2}
          class="axis-label heatmap-year"
          text-anchor="end"
          dominant-baseline="middle"
        >{year}</text>
        {#each Array(12) as _, mi}
          {@const count = heatmapResult.data[`${year}-${mi}`] || 0}
          {@const cellX = heatmapLabelW + mi * (heatmapCellSize + heatmapGap)}
          {@const cellY = HEATMAP_HEADER_H + yi * (heatmapCellSize + heatmapGap)}
          <rect
            x={cellX}
            y={cellY}
            width={heatmapCellSize}
            height={heatmapCellSize}
            rx={3}
            fill={count === 0 ? (isDark ? 'oklch(0.25 0.01 260)' : 'oklch(0.93 0.01 260)') : heatmapColorScale(count)}
            class="heatmap-cell"
            role="gridcell"
            aria-label="{MONTH_NAMES[mi]} {year}: {count} posts"
            onmouseenter={(e) => showTooltip(e, `${MONTH_NAMES[mi]} ${year}: ${count} post${count !== 1 ? 's' : ''}`)}
            onmouseleave={hideTooltip}
          />
          {#if count > 0}
            <text
              x={cellX + heatmapCellSize / 2}
              y={cellY + heatmapCellSize / 2}
              class="heatmap-count-text"
              text-anchor="middle"
              dominant-baseline="central"
            >{count}</text>
          {/if}
        {/each}
      {/each}

      <!-- Legend -->
      <text
        x={legendCenterX - legendTotalW / 2}
        y={legendY + SWATCH_SIZE / 2}
        class="axis-label"
        dominant-baseline="middle"
      >Less</text>
      {#each Array(LEGEND_STEPS) as _, si}
        {@const t = (si + 1) / LEGEND_STEPS}
        <rect
          x={legendCenterX - legendTotalW / 2 + 30 + si * (SWATCH_SIZE + LEGEND_GAP)}
          y={legendY}
          width={SWATCH_SIZE}
          height={SWATCH_SIZE}
          rx={2}
          fill={isDark ? oklchDark(t) : oklchLight(t)}
        />
      {/each}
      <text
        x={legendCenterX - legendTotalW / 2 + 30 + LEGEND_STEPS * (SWATCH_SIZE + LEGEND_GAP) + 4}
        y={legendY + SWATCH_SIZE / 2}
        class="axis-label"
        dominant-baseline="middle"
      >More</text>
    </svg>

    <!-- Tooltip -->
    {#if tooltip.visible}
      <div class="chart-tooltip" style="left:{tooltip.x}px; top:{tooltip.y}px">
        {tooltip.text}
      </div>
    {/if}
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

  /* ===== Chart Container ===== */
  .chart-container {
    position: relative;
    width: 100%;
    overflow: hidden;
  }
  .chart-container svg {
    display: block;
    max-width: 100%;
  }

  /* ===== SVG Elements ===== */
  .grid-line {
    stroke: var(--md-sys-color-outline-variant);
    stroke-dasharray: 2 3;
    stroke-width: 0.5;
  }
  .axis-label {
    font-size: 0.625rem;
    fill: var(--md-sys-color-on-surface-variant);
    font-family: inherit;
  }
  .heatmap-year {
    font-weight: 600;
    font-size: 0.6875rem;
  }
  .bar-rect {
    fill: var(--md-sys-color-primary);
    cursor: default;
    transition: opacity 0.15s;
  }
  .bar-rect:hover {
    opacity: 0.78;
  }
  .heatmap-cell {
    cursor: default;
    transition: transform 0.15s, opacity 0.15s;
  }
  .heatmap-cell:hover {
    opacity: 0.82;
    filter: brightness(1.15);
  }
  .heatmap-count-text {
    font-size: 0.5625rem;
    font-weight: 700;
    fill: var(--md-sys-color-on-surface);
    opacity: 0.75;
    pointer-events: none;
    font-family: inherit;
  }

  /* ===== Tooltip (M3 elevation) ===== */
  .chart-tooltip {
    position: absolute;
    pointer-events: none;
    z-index: 10;
    background: var(--md-sys-color-inverse-surface);
    color: var(--md-sys-color-inverse-on-surface);
    font-size: 0.75rem;
    font-weight: 500;
    padding: 0.375rem 0.625rem;
    border-radius: 0.375rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.2), 0 1px 2px rgba(0,0,0,0.15);
    white-space: nowrap;
    transform: translateY(-100%);
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
    transition: opacity 0.15s;
  }
  .h-bar-row:hover {
    opacity: 0.82;
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
    transition: background-color 0.3s;
  }
  .h-bar-value {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--md-sys-color-on-surface-variant);
    text-align: right;
  }

  /* ===== Mobile Responsive ===== */
  @media (max-width: 480px) {
    .stats-grid {
      grid-template-columns: repeat(3, 1fr);
    }
    .stat-value { font-size: 1.25rem; }
    .stat-label { font-size: 0.5625rem; }
    .h-bar-row { grid-template-columns: 5.5rem 1fr 1.75rem; }
    .h-bar-label { font-size: 0.75rem; }
    .chart-section { padding: 1rem; }
    .heatmap-count-text { font-size: 0.4375rem; }
  }

  @media (min-width: 640px) {
    .stats-grid { grid-template-columns: repeat(5, 1fr); gap: 1rem; }
    .stat-value { font-size: 2rem; }
    .stat-label { font-size: 0.75rem; }
    .stat-card { padding: 1.25rem; }
    .chart-section { padding: 1.5rem; }
    .chart-title { font-size: 1.25rem; }
  }

  @media (min-width: 1024px) {
    .stat-value { font-size: 2.5rem; }
    .h-bar-row { grid-template-columns: 9rem 1fr 2.5rem; }
  }
</style>
