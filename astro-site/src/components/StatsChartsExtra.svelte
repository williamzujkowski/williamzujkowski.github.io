<script lang="ts">
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';
  import { scaleLinear } from 'd3-scale';
  import { max as d3Max } from 'd3-array';

  interface PostData {
    title: string;
    date: string;
    tags: string[];
    wordCount: number;
    readingTime: number;
    hasCode: boolean;
  }

  interface Props {
    posts: PostData[];
  }

  interface TooltipState {
    text: string;
    x: number;
    y: number;
    visible: boolean;
  }

  let { posts }: Props = $props();
  let currentYear = $state('all');

  let isDark = $state(false);
  let scatterWidth = $state(600);
  let scatterEl: HTMLDivElement | undefined = $state(undefined);
  let tooltip = $state<TooltipState>({ text: '', x: 0, y: 0, visible: false });

  const prefersReducedMotion =
    typeof window !== 'undefined' && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const ANIM_DURATION = prefersReducedMotion ? 0 : 400;
  const animProgress = tweened(0, { duration: ANIM_DURATION, easing: cubicOut });

  // --- Filtered data ---
  let filteredPosts = $derived(currentYear === 'all' ? posts : posts.filter((p) => p.date.startsWith(currentYear)));

  // --- Day of Week data ---
  const DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  let dayOfWeekData = $derived.by(() => {
    const counts = [0, 0, 0, 0, 0, 0, 0];
    filteredPosts.forEach((p) => {
      counts[new Date(p.date).getDay()]++;
    });
    const maxVal = d3Max(counts) ?? 1;
    return { counts, max: maxVal };
  });

  let dowScale = $derived(scaleLinear().domain([0, dayOfWeekData.max]).range([0, 100]));

  // --- Reading Time Distribution ---
  let readingTimeBuckets = $derived.by(() => {
    const buckets: { label: string; min: number; max: number; count: number }[] = [
      { label: '< 3 min', min: 0, max: 3, count: 0 },
      { label: '3-5 min', min: 3, max: 5, count: 0 },
      { label: '5-10 min', min: 5, max: 10, count: 0 },
      { label: '10-20 min', min: 10, max: 20, count: 0 },
      { label: '20+ min', min: 20, max: Infinity, count: 0 },
    ];
    filteredPosts.forEach((p) => {
      const b = buckets.find((b) => p.readingTime >= b.min && p.readingTime < b.max);
      if (b) b.count++;
    });
    const maxVal = d3Max(buckets, (b) => b.count) ?? 1;
    return { buckets, max: maxVal };
  });

  let rtScale = $derived(scaleLinear().domain([0, readingTimeBuckets.max]).range([0, 100]));

  // --- Scatter Plot: Word Count vs Reading Time ---
  const SCATTER_H = 260;
  const SCATTER_MARGIN = { top: 16, right: 20, bottom: 36, left: 50 };

  let scatterData = $derived.by(() => {
    const points = filteredPosts.map((p) => ({
      x: p.wordCount,
      y: p.readingTime,
      title: p.title,
      hasCode: p.hasCode,
    }));
    const maxX = d3Max(points, (d) => d.x) ?? 1000;
    const maxY = d3Max(points, (d) => d.y) ?? 10;
    return { points, maxX, maxY };
  });

  let scatterScaleX = $derived(
    scaleLinear()
      .domain([0, scatterData.maxX * 1.1])
      .range([SCATTER_MARGIN.left, scatterWidth - SCATTER_MARGIN.right])
      .nice(),
  );

  let scatterScaleY = $derived(
    scaleLinear()
      .domain([0, scatterData.maxY * 1.1])
      .range([SCATTER_H - SCATTER_MARGIN.bottom, SCATTER_MARGIN.top])
      .nice(),
  );

  // --- Colors ---
  function getBarColor(index: number): string {
    const hues = [250, 280, 310, 340, 10, 40, 70];
    const hue = hues[index % hues.length];
    return isDark ? `oklch(0.70 0.14 ${hue})` : `oklch(0.52 0.17 ${hue})`;
  }

  function getBucketColor(index: number): string {
    const hue = 250 + index * 25;
    return isDark ? `oklch(0.68 0.13 ${hue})` : `oklch(0.54 0.16 ${hue})`;
  }

  // --- Animation ---
  let prevYear = '';
  $effect(() => {
    const yr = currentYear;
    if (yr !== prevYear) {
      prevYear = yr;
      animProgress.set(0, { duration: 0 });
      animProgress.set(1);
    }
  });

  // --- Tooltip ---
  function showTooltip(event: MouseEvent, text: string): void {
    const container = (event.currentTarget as HTMLElement).closest('.chart-container, .chart-section');
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

  function checkTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  onMount(() => {
    checkTheme();
    prevYear = currentYear;
    animProgress.set(1);

    // Listen for year filter changes from sibling StatsCharts component
    const handleYearChange = (e: Event) => {
      currentYear = (e as CustomEvent<string>).detail;
    };
    document.addEventListener('stats:year-change', handleYearChange);

    const observer = new MutationObserver(() => checkTheme());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });

    const ro = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.target === scatterEl) scatterWidth = entry.contentRect.width;
      }
    });
    if (scatterEl) ro.observe(scatterEl);

    return () => {
      document.removeEventListener('stats:year-change', handleYearChange);
      observer.disconnect();
      ro.disconnect();
    };
  });
</script>

<!-- Day of Week Distribution -->
<section class="chart-section" aria-label="Publishing day of week distribution">
  <h2 class="chart-title">Day of Week</h2>
  <div class="h-bar-chart" role="list">
    {#each DAY_NAMES as day, i}
      {@const count = dayOfWeekData.counts[i]}
      <div class="h-bar-row" role="listitem">
        <span class="h-bar-label">{day}</span>
        <div class="h-bar-track">
          <div
            class="h-bar-fill"
            style="width: {dowScale(count * $animProgress)}%; background-color: {getBarColor(i)}"
          ></div>
        </div>
        <span class="h-bar-value">{count}</span>
      </div>
    {/each}
  </div>
</section>

<!-- Reading Time Distribution -->
<section class="chart-section" aria-label="Reading time distribution">
  <h2 class="chart-title">Reading Time</h2>
  <div class="h-bar-chart" role="list">
    {#each readingTimeBuckets.buckets as bucket, i}
      <div class="h-bar-row" role="listitem">
        <span class="h-bar-label">{bucket.label}</span>
        <div class="h-bar-track">
          <div
            class="h-bar-fill"
            style="width: {rtScale(bucket.count * $animProgress)}%; background-color: {getBucketColor(i)}"
          ></div>
        </div>
        <span class="h-bar-value">{bucket.count}</span>
      </div>
    {/each}
  </div>
</section>

<!-- Word Count vs Reading Time Scatter Plot -->
<section class="chart-section" aria-label="Word count vs reading time scatter plot" style="position: relative">
  <h2 class="chart-title">Words vs Reading Time</h2>
  <div class="chart-container" bind:this={scatterEl}>
    <svg
      width={scatterWidth}
      height={SCATTER_H}
      role="img"
      aria-label="Scatter plot showing relationship between word count and reading time"
    >
      <!-- Grid lines -->
      {#each scatterScaleY.ticks(5) as tick}
        <line
          x1={SCATTER_MARGIN.left}
          x2={scatterWidth - SCATTER_MARGIN.right}
          y1={scatterScaleY(tick)}
          y2={scatterScaleY(tick)}
          class="grid-line"
        />
        <text
          x={SCATTER_MARGIN.left - 8}
          y={scatterScaleY(tick)}
          class="axis-label"
          text-anchor="end"
          dominant-baseline="middle">{tick}m</text
        >
      {/each}

      {#each scatterScaleX.ticks(5) as tick}
        <line
          x1={scatterScaleX(tick)}
          x2={scatterScaleX(tick)}
          y1={SCATTER_MARGIN.top}
          y2={SCATTER_H - SCATTER_MARGIN.bottom}
          class="grid-line"
        />
        <text x={scatterScaleX(tick)} y={SCATTER_H - SCATTER_MARGIN.bottom + 16} class="axis-label" text-anchor="middle"
          >{tick >= 1000 ? tick / 1000 + 'k' : tick}</text
        >
      {/each}

      <!-- Axis labels -->
      <text x={scatterWidth / 2} y={SCATTER_H - 4} class="axis-label" text-anchor="middle">Words</text>
      <text
        x={12}
        y={SCATTER_H / 2}
        class="axis-label"
        text-anchor="middle"
        transform="rotate(-90, 12, {SCATTER_H / 2})">Reading Time</text
      >

      <!-- Data points -->
      {#each scatterData.points as point, i}
        {@const cx = scatterScaleX(point.x)}
        {@const cy = scatterScaleY(point.y)}
        {@const progress = $animProgress}
        <circle
          {cx}
          cy={SCATTER_H - SCATTER_MARGIN.bottom - (SCATTER_H - SCATTER_MARGIN.bottom - cy) * progress}
          r={point.hasCode ? 5 : 4}
          class="scatter-dot"
          fill={point.hasCode
            ? isDark
              ? 'oklch(0.75 0.15 160)'
              : 'oklch(0.50 0.18 160)'
            : isDark
              ? 'oklch(0.72 0.14 260)'
              : 'oklch(0.52 0.17 260)'}
          onmouseenter={(e) => showTooltip(e, `${point.title}\n${point.x.toLocaleString()} words · ${point.y} min`)}
          onmouseleave={hideTooltip}
        />
      {/each}
    </svg>

    <!-- Legend -->
    <div class="scatter-legend">
      <span class="legend-item">
        <span class="legend-dot" style="background: {isDark ? 'oklch(0.72 0.14 260)' : 'oklch(0.52 0.17 260)'}"></span>
        Prose
      </span>
      <span class="legend-item">
        <span class="legend-dot" style="background: {isDark ? 'oklch(0.75 0.15 160)' : 'oklch(0.50 0.18 160)'}"></span>
        Has Code
      </span>
    </div>

    <!-- Tooltip -->
    {#if tooltip.visible}
      <div class="chart-tooltip" style="left:{tooltip.x}px; top:{tooltip.y}px">
        {tooltip.text}
      </div>
    {/if}
  </div>
</section>

<style>
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
  .chart-container {
    position: relative;
    width: 100%;
    overflow: hidden;
  }
  .chart-container svg {
    display: block;
    max-width: 100%;
  }
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
  .h-bar-chart {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .h-bar-row {
    display: grid;
    grid-template-columns: 5rem 1fr 2rem;
    gap: 0.5rem;
    align-items: center;
    min-height: 2rem;
  }
  .h-bar-label {
    font-size: 0.8125rem;
    font-weight: 500;
    color: var(--md-sys-color-on-surface);
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
  .scatter-dot {
    cursor: default;
    opacity: 0.8;
    transition:
      opacity 0.15s,
      r 0.15s;
  }
  .scatter-dot:hover {
    opacity: 1;
    r: 7;
  }
  .scatter-legend {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    margin-top: 0.5rem;
    font-size: 0.75rem;
    color: var(--md-sys-color-on-surface-variant);
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.375rem;
  }
  .legend-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
  }
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
    box-shadow:
      0 2px 6px rgba(0, 0, 0, 0.2),
      0 1px 2px rgba(0, 0, 0, 0.15);
    white-space: pre-line;
    max-width: 250px;
    transform: translateY(-100%);
  }

  @media (max-width: 480px) {
    .h-bar-row {
      grid-template-columns: 4.5rem 1fr 1.75rem;
    }
    .h-bar-label {
      font-size: 0.75rem;
    }
    .chart-section {
      padding: 1rem;
    }
  }

  @media (min-width: 640px) {
    .chart-section {
      padding: 1.5rem;
    }
    .chart-title {
      font-size: 1.25rem;
    }
    .h-bar-row {
      grid-template-columns: 6rem 1fr 2.5rem;
    }
  }
</style>
