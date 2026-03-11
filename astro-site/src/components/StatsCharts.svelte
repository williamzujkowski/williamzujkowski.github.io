<script lang="ts">
  import { onMount } from 'svelte';
  import {
    Chart,
    LineController,
    BarController,
    RadarController,
    DoughnutController,
    LineElement,
    BarElement,
    PointElement,
    ArcElement,
    RadialLinearScale,
    CategoryScale,
    LinearScale,
    Filler,
    Legend,
    Tooltip,
  } from 'chart.js';

  Chart.register(
    LineController, BarController, RadarController, DoughnutController,
    LineElement, BarElement, PointElement, ArcElement,
    RadialLinearScale, CategoryScale, LinearScale,
    Filler, Legend, Tooltip,
  );

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

  let { posts }: Props = $props();

  let currentYear = $state('all');
  let charts: Record<string, Chart> = {};

  // Canvas refs
  let postsOverTimeCanvas: HTMLCanvasElement;
  let topTagsCanvas: HTMLCanvasElement;
  let dayOfWeekCanvas: HTMLCanvasElement;
  let readingTimeCanvas: HTMLCanvasElement;
  let topicEvolutionCanvas: HTMLCanvasElement;
  let wordCountCanvas: HTMLCanvasElement;

  // Derived data
  let filteredPosts = $derived(
    currentYear === 'all' ? posts : posts.filter((p) => p.date.startsWith(currentYear))
  );

  let years = $derived(
    [...new Set(posts.map((p) => p.date.substring(0, 4)))].sort()
  );

  let totalWords = $derived(filteredPosts.reduce((s, p) => s + p.wordCount, 0));
  let uniqueTags = $derived(
    [...new Set(filteredPosts.flatMap((p) => p.tags.filter((t) => t !== 'posts')))]
  );
  let avgReading = $derived(
    filteredPosts.length > 0
      ? Math.round(filteredPosts.reduce((s, p) => s + p.readingTime, 0) / filteredPosts.length)
      : 0
  );

  // Streaks
  function calculateStreaks(fp: PostData[]) {
    if (fp.length === 0) return { longest: 0, current: 0, mostProductiveMonth: '-', mostProductiveCount: 0 };
    const monthCounts: Record<string, number> = {};
    fp.forEach((p) => {
      const m = p.date.substring(0, 7);
      monthCounts[m] = (monthCounts[m] || 0) + 1;
    });
    const sorted = Object.keys(monthCounts).sort();
    let longest = 1, cur = 1;
    for (let i = 1; i < sorted.length; i++) {
      const prev = new Date(sorted[i - 1] + '-01');
      const curr = new Date(sorted[i] + '-01');
      const diff = (curr.getFullYear() - prev.getFullYear()) * 12 + (curr.getMonth() - prev.getMonth());
      if (diff === 1) { cur++; longest = Math.max(longest, cur); } else { cur = 1; }
    }
    // Current streak
    const now = new Date();
    const cm = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    const pm = new Date(now.getFullYear(), now.getMonth() - 1, 1);
    const prevM = `${pm.getFullYear()}-${String(pm.getMonth() + 1).padStart(2, '0')}`;
    const last = sorted[sorted.length - 1];
    cur = 0;
    if (last === cm || last === prevM) {
      cur = 1;
      for (let i = sorted.length - 2; i >= 0; i--) {
        const p = new Date(sorted[i] + '-01');
        const c = new Date(sorted[i + 1] + '-01');
        const d = (c.getFullYear() - p.getFullYear()) * 12 + (c.getMonth() - p.getMonth());
        if (d === 1) cur++; else break;
      }
    }
    let mpMonth = '-', mpCount = 0;
    Object.entries(monthCounts).forEach(([m, c]) => {
      if (c > mpCount) { mpCount = c; mpMonth = m; }
    });
    if (mpMonth !== '-') {
      const d = new Date(mpMonth + '-01');
      mpMonth = d.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
    }
    return { longest, current: cur, mostProductiveMonth: mpMonth, mostProductiveCount: mpCount };
  }

  let streaks = $derived(calculateStreaks(filteredPosts));

  // Reading time insights
  function percentile(arr: number[], p: number): number {
    if (arr.length === 0) return 0;
    const s = [...arr].sort((a, b) => a - b);
    const idx = (p / 100) * (s.length - 1);
    const lo = Math.floor(idx), hi = Math.ceil(idx), w = idx - lo;
    return s[lo] * (1 - w) + s[hi] * w;
  }

  let readingTimes = $derived(filteredPosts.map((p) => p.readingTime));
  let medianReading = $derived(Math.round(percentile(readingTimes, 50)));
  let p25 = $derived(Math.round(percentile(readingTimes, 25)));
  let p75 = $derived(Math.round(percentile(readingTimes, 75)));
  let longestPost = $derived(readingTimes.length > 0 ? Math.max(...readingTimes) : 0);

  // Citation stats (estimated from content — no pre-calc available in Astro)
  let postsWithCode = $derived(filteredPosts.filter((p) => p.hasCode).length);
  let codePercent = $derived(
    filteredPosts.length > 0 ? ((postsWithCode / filteredPosts.length) * 100).toFixed(1) : '0'
  );

  // Year-over-year
  let showYoY = $derived(currentYear !== 'all');
  let yoyData = $derived.by(() => {
    if (currentYear === 'all') return null;
    const prevYear = String(parseInt(currentYear) - 1);
    const currPosts = posts.filter((p) => p.date.startsWith(currentYear));
    const prevPosts = posts.filter((p) => p.date.startsWith(prevYear));
    if (prevPosts.length === 0) return null;
    const cw = currPosts.reduce((s, p) => s + p.wordCount, 0);
    const pw = prevPosts.reduce((s, p) => s + p.wordCount, 0);
    return {
      currCount: currPosts.length, prevCount: prevPosts.length,
      currWords: cw, prevWords: pw,
      currAvg: currPosts.length > 0 ? Math.round(cw / currPosts.length) : 0,
      prevAvg: prevPosts.length > 0 ? Math.round(pw / prevPosts.length) : 0,
      prevYear,
      isPartial: parseInt(currentYear) === new Date().getFullYear(),
    };
  });

  function pctChange(curr: number, prev: number): string {
    if (prev === 0) return curr > 0 ? '+100' : '0';
    return ((curr - prev) / prev * 100).toFixed(0);
  }

  // Heatmap
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

  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const LIGHT_COLORS = ['#8b9dc3', '#5b6fa8', '#3d4f7f', '#2a3a5c', '#1a2642'];
  const DARK_COLORS = ['#5b6fa8', '#7b8fc8', '#9bafd8', '#bccfe8', '#d9e5f5'];
  const CHART_PALETTE = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#84cc16'];

  function getHeatmapColor(count: number, maxCount: number, isDark: boolean): string {
    if (count === 0) return isDark ? '#2a3241' : '#e8eaf0';
    const colors = isDark ? DARK_COLORS : LIGHT_COLORS;
    const idx = Math.min(Math.floor((count / maxCount) * 5), 4);
    return colors[idx];
  }

  // Tag cloud
  let tagCountsSorted = $derived.by(() => {
    const counts: Record<string, number> = {};
    filteredPosts.forEach((p) => {
      p.tags.filter((t) => t !== 'posts').forEach((t) => {
        counts[t] = (counts[t] || 0) + 1;
      });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  });

  // Theme detection
  let isDark = $state(false);

  function checkTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  function getThemeColors() {
    const textColor = isDark ? '#e5e7eb' : '#374151';
    const gridColor = isDark ? '#374151' : '#e5e7eb';
    const tooltipBg = isDark ? '#1f2937' : '#ffffff';
    return { textColor, gridColor, tooltipBg };
  }

  function destroyCharts() {
    Object.values(charts).forEach((c) => c?.destroy());
    charts = {};
  }

  function buildCharts() {
    destroyCharts();
    const fp = filteredPosts;
    if (fp.length === 0) return;
    const { textColor, gridColor, tooltipBg } = getThemeColors();
    const tooltipOpts = { backgroundColor: tooltipBg, titleColor: textColor, bodyColor: textColor, borderColor: gridColor, borderWidth: 1 };

    // Posts Over Time
    const monthCounts: Record<string, number> = {};
    fp.forEach((p) => { const m = p.date.substring(0, 7); monthCounts[m] = (monthCounts[m] || 0) + 1; });
    const sortedMonths = Object.keys(monthCounts).sort();

    if (postsOverTimeCanvas) {
      charts.postsOverTime = new Chart(postsOverTimeCanvas, {
        type: 'line',
        data: {
          labels: sortedMonths,
          datasets: [{ label: 'Posts Published', data: sortedMonths.map((m) => monthCounts[m]), borderColor: '#6366f1', backgroundColor: 'rgba(99,102,241,0.1)', fill: true, tension: 0.4 }],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: textColor } }, tooltip: tooltipOpts },
          scales: { x: { ticks: { color: textColor }, grid: { color: gridColor } }, y: { ticks: { color: textColor, stepSize: 1 }, grid: { color: gridColor } } },
        },
      });
    }

    // Top Tags
    const tc: Record<string, number> = {};
    fp.forEach((p) => p.tags.filter((t) => t !== 'posts').forEach((t) => { tc[t] = (tc[t] || 0) + 1; }));
    const topTags = Object.entries(tc).sort((a, b) => b[1] - a[1]).slice(0, 10);

    if (topTagsCanvas) {
      charts.topTags = new Chart(topTagsCanvas, {
        type: 'bar',
        data: {
          labels: topTags.map(([t]) => t),
          datasets: [{ label: 'Post Count', data: topTags.map(([, c]) => c), backgroundColor: CHART_PALETTE.slice(0, topTags.length) }],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { display: false }, tooltip: tooltipOpts },
          scales: { x: { ticks: { color: textColor }, grid: { display: false } }, y: { ticks: { color: textColor, stepSize: 1 }, grid: { color: gridColor } } },
        },
      });
    }

    // Day of Week
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const dowCounts = new Array(7).fill(0);
    fp.forEach((p) => { dowCounts[new Date(p.date).getDay()]++; });

    if (dayOfWeekCanvas) {
      charts.dayOfWeek = new Chart(dayOfWeekCanvas, {
        type: 'radar',
        data: {
          labels: dayNames,
          datasets: [{ label: 'Posts Published', data: dowCounts, borderColor: '#6366f1', backgroundColor: isDark ? 'rgba(99,102,241,0.2)' : 'rgba(99,102,241,0.1)', pointBackgroundColor: '#6366f1', pointBorderColor: '#fff' }],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: textColor } }, tooltip: tooltipOpts },
          scales: { r: { ticks: { color: textColor, stepSize: 1, backdropColor: 'transparent' }, grid: { color: gridColor }, pointLabels: { color: textColor } } },
        },
      });
    }

    // Reading Time Distribution
    const rtBuckets: Record<string, number> = { '1-3 min': 0, '4-6 min': 0, '7-9 min': 0, '10+ min': 0 };
    fp.forEach((p) => {
      if (p.readingTime <= 3) rtBuckets['1-3 min']++;
      else if (p.readingTime <= 6) rtBuckets['4-6 min']++;
      else if (p.readingTime <= 9) rtBuckets['7-9 min']++;
      else rtBuckets['10+ min']++;
    });

    if (readingTimeCanvas) {
      charts.readingTime = new Chart(readingTimeCanvas, {
        type: 'doughnut',
        data: {
          labels: Object.keys(rtBuckets),
          datasets: [{ data: Object.values(rtBuckets), backgroundColor: ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b'], borderColor: isDark ? '#1f2937' : '#ffffff', borderWidth: 2 }],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { color: textColor } }, tooltip: tooltipOpts },
        },
      });
    }

    // Topic Evolution
    const top5 = topTags.slice(0, 5).map(([t]) => t);
    const tagByMonth: Record<string, Record<string, number>> = {};
    fp.forEach((p) => {
      const m = p.date.substring(0, 7);
      if (!tagByMonth[m]) tagByMonth[m] = {};
      p.tags.filter((t) => top5.includes(t)).forEach((t) => { tagByMonth[m][t] = (tagByMonth[m][t] || 0) + 1; });
    });
    const allMonths = Object.keys(tagByMonth).sort();

    if (topicEvolutionCanvas && top5.length > 0) {
      charts.topicEvolution = new Chart(topicEvolutionCanvas, {
        type: 'line',
        data: {
          labels: allMonths,
          datasets: top5.map((tag, i) => ({
            label: tag,
            data: allMonths.map((m) => tagByMonth[m][tag] || 0),
            borderColor: CHART_PALETTE[i],
            backgroundColor: CHART_PALETTE[i] + '20',
            fill: false, tension: 0.4,
          })),
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: textColor }, position: 'top' }, tooltip: tooltipOpts },
          scales: { x: { ticks: { color: textColor }, grid: { color: gridColor } }, y: { ticks: { color: textColor, stepSize: 1 }, grid: { color: gridColor } } },
        },
      });
    }

    // Word Count
    const wcBuckets: Record<string, number> = { '0-1000': 0, '1001-2000': 0, '2001-3000': 0, '3001-4000': 0, '4000+': 0 };
    fp.forEach((p) => {
      if (p.wordCount <= 1000) wcBuckets['0-1000']++;
      else if (p.wordCount <= 2000) wcBuckets['1001-2000']++;
      else if (p.wordCount <= 3000) wcBuckets['2001-3000']++;
      else if (p.wordCount <= 4000) wcBuckets['3001-4000']++;
      else wcBuckets['4000+']++;
    });

    if (wordCountCanvas) {
      charts.wordCount = new Chart(wordCountCanvas, {
        type: 'bar',
        data: {
          labels: Object.keys(wcBuckets).map((l) => l + ' words'),
          datasets: [{ label: 'Number of Posts', data: Object.values(wcBuckets), backgroundColor: '#6366f1' }],
        },
        options: {
          responsive: true, maintainAspectRatio: false,
          plugins: { legend: { labels: { color: textColor } }, tooltip: tooltipOpts },
          scales: { x: { ticks: { color: textColor }, grid: { display: false } }, y: { ticks: { color: textColor, stepSize: 1 }, grid: { color: gridColor } } },
        },
      });
    }
  }

  function switchYear(year: string) {
    currentYear = year;
  }

  // Rebuild charts when filteredPosts or theme changes
  $effect(() => {
    // Access dependencies to track them
    void filteredPosts;
    void isDark;
    buildCharts();
  });

  onMount(() => {
    checkTheme();
    const observer = new MutationObserver(() => checkTheme());
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => { destroyCharts(); observer.disconnect(); };
  });
</script>

<!-- Year Tabs -->
<section aria-label="Year filter navigation">
  <nav class="max-w-6xl mx-auto mb-8">
    <div class="flex justify-center items-center gap-4 flex-wrap">
      <button
        class="px-6 py-3 min-h-[44px] rounded-lg font-medium transition-all duration-200"
        class:bg-[var(--md-sys-color-primary)]={currentYear === 'all'}
        class:text-[var(--md-sys-color-on-primary)]={currentYear === 'all'}
        class:shadow-md={currentYear === 'all'}
        class:bg-[var(--md-sys-color-surface-container)]={currentYear !== 'all'}
        class:text-[var(--md-sys-color-on-surface-variant)]={currentYear !== 'all'}
        aria-pressed={currentYear === 'all'}
        onclick={() => switchYear('all')}
      >All Time</button>
      {#each years as year}
        <button
          class="px-6 py-3 min-h-[44px] rounded-lg font-medium transition-all duration-200"
          class:bg-[var(--md-sys-color-primary)]={currentYear === year}
          class:text-[var(--md-sys-color-on-primary)]={currentYear === year}
          class:shadow-md={currentYear === year}
          class:bg-[var(--md-sys-color-surface-container)]={currentYear !== year}
          class:text-[var(--md-sys-color-on-surface-variant)]={currentYear !== year}
          aria-pressed={currentYear === year}
          onclick={() => switchYear(year)}
        >{year}</button>
      {/each}
    </div>
  </nav>
</section>

<!-- Summary Stats Cards -->
<section aria-labelledby="overview-heading" aria-live="polite">
  <h2 id="overview-heading" class="sr-only">Statistics Overview</h2>
  <div class="max-w-6xl mx-auto mb-12">
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="card p-6">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider">Total Posts</h3>
          <svg class="w-8 h-8 text-[var(--md-sys-color-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
        </div>
        <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length}</p>
      </div>
      <div class="card p-6">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider">Total Words</h3>
          <svg class="w-8 h-8 text-[var(--md-sys-color-primary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
        </div>
        <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{totalWords.toLocaleString()}</p>
      </div>
      <div class="card p-6">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider">Unique Tags</h3>
          <svg class="w-8 h-8 text-[var(--md-sys-color-tertiary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" /></svg>
        </div>
        <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{uniqueTags.length}</p>
      </div>
      <div class="card p-6">
        <div class="flex items-center justify-between mb-2">
          <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider">Avg Reading</h3>
          <svg class="w-8 h-8 text-[var(--md-sys-color-tertiary)]" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
        </div>
        <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{avgReading}m</p>
      </div>
    </div>
  </div>
</section>

<!-- Writing Streaks -->
<section aria-labelledby="streaks-heading" class="max-w-6xl mx-auto mb-12">
  <h2 id="streaks-heading" class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Writing Streaks</h2>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <div class="card p-6">
      <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Longest Streak</h3>
      <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{streaks.longest}</p>
      <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">consecutive months</p>
    </div>
    <div class="card p-6">
      <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Current Streak</h3>
      <p class="text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{streaks.current}</p>
      <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">consecutive months</p>
    </div>
    <div class="card p-6">
      <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Most Productive</h3>
      <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{streaks.mostProductiveMonth}</p>
      <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">{streaks.mostProductiveCount} post{streaks.mostProductiveCount !== 1 ? 's' : ''}</p>
    </div>
  </div>
</section>

<!-- Year-over-Year Comparison -->
{#if showYoY && yoyData}
  {@const yoy = yoyData}
  {#if yoy}
    <section aria-labelledby="yoy-heading" class="max-w-6xl mx-auto mb-12">
      <h2 id="yoy-heading" class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Year-over-Year Comparison</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {#each [
          { label: 'Posts', curr: yoy.currCount, prev: yoy.prevCount, suffix: '' },
          { label: 'Total Words', curr: yoy.currWords, prev: yoy.prevWords, suffix: '' },
          { label: 'Avg Post Length', curr: yoy.currAvg, prev: yoy.prevAvg, suffix: ' words' },
        ] as item}
          {@const diff = item.curr - item.prev}
          {@const pct = pctChange(item.curr, item.prev)}
          <div class="card p-6">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">{item.label}</h3>
            <div class="flex items-end gap-3">
              <p class="text-3xl font-bold text-[var(--md-sys-color-on-surface)]">{item.curr.toLocaleString()}{item.suffix}</p>
              <span class="text-lg font-semibold" style="color: {diff > 0 ? 'var(--md-sys-color-success)' : diff < 0 ? 'var(--md-sys-color-error)' : 'var(--md-sys-color-outline)'}">
                {diff > 0 ? '\u25B2' : diff < 0 ? '\u25BC' : '\u2014'} {Math.abs(Number(pct))}%
              </span>
            </div>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">vs {yoy.prevYear}: {item.prev.toLocaleString()}{item.suffix}</p>
          </div>
        {/each}
      </div>
      {#if yoy.isPartial}
        <p class="text-xs text-[var(--md-sys-color-outline)] mt-4 text-center">* {currentYear} is still in progress. Comparison reflects partial year data.</p>
      {/if}
    </section>
  {/if}
{/if}

<!-- Charts Section -->
<section aria-labelledby="charts-heading">
  <h2 id="charts-heading" class="sr-only">Data Visualizations</h2>
  <div class="max-w-6xl mx-auto space-y-12">

    <!-- Posts Over Time -->
    <div class="card p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Posts Over Time</h2>
      <div class="h-80 px-2">
        <canvas bind:this={postsOverTimeCanvas} aria-label="Line chart showing blog posts published over time" role="img"></canvas>
      </div>
    </div>

    <!-- Two Column: Top Tags + Day of Week -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Top Tags</h2>
        <div class="h-80 px-2">
          <canvas bind:this={topTagsCanvas} aria-label="Bar chart showing most frequently used blog post tags" role="img"></canvas>
        </div>
      </div>
      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Publishing by Day of Week</h2>
        <div class="h-80 px-2">
          <canvas bind:this={dayOfWeekCanvas} aria-label="Radar chart showing publishing patterns by day of week" role="img"></canvas>
        </div>
      </div>
    </div>

    <!-- Two Column: Citation Stats + Code Stats -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Content Statistics</h2>
        <div class="space-y-6">
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Total Words</h3>
            <p class="text-4xl font-bold text-[var(--md-sys-color-primary)]">{totalWords.toLocaleString()}</p>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">across {filteredPosts.length} posts</p>
          </div>
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Average Words per Post</h3>
            <p class="text-4xl font-bold text-[var(--md-sys-color-primary)]">{filteredPosts.length > 0 ? Math.round(totalWords / filteredPosts.length).toLocaleString() : 0}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Words per Minute (est.)</h3>
            <p class="text-4xl font-bold text-[var(--md-sys-color-primary)]">225</p>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">used for reading time calculation</p>
          </div>
        </div>
      </div>

      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Code Statistics</h2>
        <div class="space-y-6">
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Posts with Code</h3>
            <p class="text-4xl font-bold text-[var(--md-sys-color-tertiary)]">{postsWithCode}</p>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">of {filteredPosts.length} posts ({codePercent}%)</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Technical Content Focus</h3>
            <div class="w-full bg-[var(--md-sys-color-surface-container)] rounded-full h-4 mt-2">
              <div class="h-4 rounded-full transition-all duration-500" style="width: {codePercent}%; background-color: var(--md-sys-color-tertiary)"></div>
            </div>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">posts include code examples</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Reading Time Distribution + Insights -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Reading Time Distribution</h2>
        <div class="h-80 px-4">
          <canvas bind:this={readingTimeCanvas} aria-label="Doughnut chart showing distribution of reading times" role="img"></canvas>
        </div>
      </div>

      <div class="card p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Reading Time Insights</h2>
        <div class="space-y-4">
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Median Reading Time</h3>
            <p class="text-3xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? medianReading + 'm' : '-'}</p>
          </div>
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">25th Percentile</h3>
            <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? p25 + 'm' : '-'}</p>
          </div>
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">75th Percentile</h3>
            <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? p75 + 'm' : '-'}</p>
          </div>
          <div>
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Longest Post</h3>
            <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? longestPost + 'm' : '-'}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Publishing Activity Heatmap -->
    <div class="card p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Publishing Activity Heatmap</h2>
      <div class="overflow-x-auto" style="padding-top: 48px;">
        <div class="min-w-fit" role="region" aria-label="Publishing activity heatmap">
          <div class="grid gap-0.5">
            {#each heatmapResult.years as year}
              <div class="flex items-start gap-2">
                <div class="w-14 flex-shrink-0 text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] pt-2">{year}</div>
                <div class="grid gap-0.5 flex-1 min-w-0" style="grid-template-columns: repeat(12, 81px);">
                  {#each MONTHS as month, idx}
                    {@const count = heatmapResult.data[`${year}-${idx}`] || 0}
                    {@const bgColor = getHeatmapColor(count, heatmapResult.maxCount, isDark)}
                    <div class="group relative hover:z-50" style="width: 81px; height: 81px;" tabindex="0" role="button" aria-label="{month} {year}: {count} post{count !== 1 ? 's' : ''}">
                      <div class="w-full h-full rounded transition-all cursor-pointer" style="background-color: {bgColor}"></div>
                      <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-2 text-xs rounded opacity-0 group-hover:opacity-100 group-focus:opacity-100 transition-opacity whitespace-nowrap pointer-events-none z-10 shadow-lg" style="background-color: var(--md-sys-color-inverse-surface); color: var(--md-sys-color-inverse-on-surface);">
                        {month} {year}: {count} post{count !== 1 ? 's' : ''}
                      </div>
                    </div>
                  {/each}
                </div>
              </div>
            {/each}
          </div>
        </div>
      </div>
      <!-- Legend -->
      <div class="mt-6 flex items-center justify-center gap-2">
        <span class="text-sm text-[var(--md-sys-color-on-surface-variant)]">Less</span>
        <div class="flex gap-2">
          {#each (isDark ? DARK_COLORS : LIGHT_COLORS) as color}
            <div class="w-12 h-12 min-h-[44px] min-w-[44px] rounded flex-shrink-0" style="background-color: {color}"></div>
          {/each}
        </div>
        <span class="text-sm text-[var(--md-sys-color-on-surface-variant)]">More</span>
      </div>
    </div>

    <!-- Tag Cloud -->
    <div class="card p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Tag Cloud</h2>
      <div class="flex flex-wrap gap-3 justify-center min-h-[200px]" role="list" aria-label="Tag cloud">
        {#each tagCountsSorted as [tag, count], idx}
          {@const maxCount = tagCountsSorted[0]?.[1] || 1}
          {@const size = 0.8 + (count / maxCount) * 1.5}
          {@const color = CHART_PALETTE[idx % CHART_PALETTE.length]}
          <li class="list-none">
            <a href="/tags/{tag}/"
               class="inline-block px-4 py-2 min-h-[44px] rounded-full transition-transform hover:scale-110"
               style="font-size: {size}rem; background-color: {color}20; color: {color}; border: 2px solid {color}"
               aria-label="{tag} tag, {count} post{count !== 1 ? 's' : ''}">
              {tag} <span class="text-xs" style="color: var(--md-sys-color-on-surface-variant)">({count})</span>
            </a>
          </li>
        {/each}
      </div>
    </div>

    <!-- Topic Evolution -->
    <div class="card p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Topic Evolution Over Time</h2>
      <div class="h-96 px-2">
        <canvas bind:this={topicEvolutionCanvas} aria-label="Line chart showing evolution of top 5 tags over time" role="img"></canvas>
      </div>
    </div>

    <!-- Word Count Analysis -->
    <div class="card p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Word Count Analysis</h2>
      <div class="h-80 px-2">
        <canvas bind:this={wordCountCanvas} aria-label="Bar chart showing word count distribution" role="img"></canvas>
      </div>
    </div>

  </div>
</section>
