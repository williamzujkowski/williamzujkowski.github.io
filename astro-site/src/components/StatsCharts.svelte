<script lang="ts">
  import { onMount } from 'svelte';
  import * as Plot from '@observablehq/plot';

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

  // Chart container refs
  let postsOverTimeEl: HTMLDivElement;
  let topTagsEl: HTMLDivElement;
  let dayOfWeekEl: HTMLDivElement;
  let readingTimeEl: HTMLDivElement;
  let topicEvolutionEl: HTMLDivElement;
  let wordCountEl: HTMLDivElement;
  let scatterEl: HTMLDivElement;

  // Derived data
  let filteredPosts = $derived(
    currentYear === 'all' ? statsData.posts : statsData.posts.filter((p) => p.date.startsWith(currentYear))
  );

  let years = $derived(
    [...new Set(statsData.posts.map((p) => p.date.substring(0, 4)))].sort()
  );

  let totalWords = $derived(filteredPosts.reduce((s, p) => s + p.wordCount, 0));
  let uniqueTags = $derived(
    [...new Set(filteredPosts.flatMap((p) => p.tags))]
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

  // Reading time percentiles
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

  // Code stats
  let postsWithCode = $derived(filteredPosts.filter((p) => p.hasCode).length);
  let codePercent = $derived(
    filteredPosts.length > 0 ? ((postsWithCode / filteredPosts.length) * 100).toFixed(1) : '0'
  );

  // Year-over-year
  let showYoY = $derived(currentYear !== 'all');
  let yoyData = $derived.by(() => {
    if (currentYear === 'all') return null;
    const prevYear = String(parseInt(currentYear) - 1);
    const currPosts = statsData.posts.filter((p) => p.date.startsWith(currentYear));
    const prevPosts = statsData.posts.filter((p) => p.date.startsWith(prevYear));
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
  const LIGHT_HEATMAP = ['#e8eaf0', '#8b9dc3', '#5b6fa8', '#3d4f7f', '#2a3a5c', '#1a2642'];
  const DARK_HEATMAP = ['#2a3241', '#5b6fa8', '#7b8fc8', '#9bafd8', '#bccfe8', '#d9e5f5'];
  const CHART_PALETTE = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444', '#14b8a6', '#f97316', '#84cc16'];
  const TAG_TEXT_COLORS_LIGHT = ['#4338ca', '#6d28d9', '#be185d', '#92400e', '#065f46', '#1d4ed8', '#b91c1c', '#0f766e', '#c2410c', '#4d7c0f'];
  const TAG_TEXT_COLORS_DARK = ['#a5b4fc', '#c4b5fd', '#f9a8d4', '#fcd34d', '#6ee7b7', '#93c5fd', '#fca5a5', '#5eead4', '#fdba74', '#bef264'];

  function getHeatmapColor(count: number, maxCount: number): string {
    const colors = isDark ? DARK_HEATMAP : LIGHT_HEATMAP;
    if (count === 0) return colors[0];
    const idx = Math.min(Math.floor((count / maxCount) * 5) + 1, 5);
    return colors[idx];
  }

  // Tag cloud
  let tagCountsSorted = $derived.by(() => {
    const counts: Record<string, number> = {};
    filteredPosts.forEach((p) => {
      p.tags.forEach((t) => { counts[t] = (counts[t] || 0) + 1; });
    });
    return Object.entries(counts).sort((a, b) => b[1] - a[1]);
  });

  // Theme
  function checkTheme() {
    isDark = document.documentElement.classList.contains('dark');
  }

  // Observable Plot chart builders
  function getPlotTheme() {
    return {
      color: isDark ? '#e5e7eb' : '#374151',
      backgroundColor: 'transparent',
    };
  }

  function renderChart(el: HTMLDivElement | undefined, plotFn: () => SVGSVGElement | HTMLElement) {
    if (!el) return;
    el.innerHTML = '';
    const svg = plotFn();
    el.appendChild(svg);
  }

  function buildPostsOverTime() {
    const fp = filteredPosts;
    const monthCounts: Record<string, number> = {};
    fp.forEach((p) => { const m = p.date.substring(0, 7); monthCounts[m] = (monthCounts[m] || 0) + 1; });
    const data = Object.entries(monthCounts)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([month, count]) => ({ month: new Date(month + '-01'), count }));

    if (data.length === 0) return;

    renderChart(postsOverTimeEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 300,
      width: postsOverTimeEl?.clientWidth ?? 700,
      x: { label: null, type: 'time' },
      y: { label: 'Posts', grid: true },
      marks: [
        Plot.areaY(data, { x: 'month', y: 'count', fill: '#6366f1', fillOpacity: 0.15, curve: 'catmull-rom' }),
        Plot.lineY(data, { x: 'month', y: 'count', stroke: '#6366f1', strokeWidth: 2.5, curve: 'catmull-rom' }),
        Plot.dot(data, { x: 'month', y: 'count', fill: '#6366f1', r: 4 }),
        Plot.tip(data, Plot.pointerX({ x: 'month', y: 'count', title: (d: { month: Date; count: number }) => `${d.month.toLocaleDateString('en-US', { year: 'numeric', month: 'short' })}: ${d.count} post${d.count !== 1 ? 's' : ''}` })),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildTopTags() {
    const tc: Record<string, number> = {};
    filteredPosts.forEach((p) => p.tags.forEach((t) => { tc[t] = (tc[t] || 0) + 1; }));
    const data = Object.entries(tc)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([tag, count], i) => ({ tag, count, color: CHART_PALETTE[i % CHART_PALETTE.length] }));

    if (data.length === 0) return;

    renderChart(topTagsEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 300,
      width: topTagsEl?.clientWidth ?? 500,
      x: { label: null },
      y: { label: 'Posts', grid: true },
      marks: [
        Plot.barY(data, { x: 'tag', y: 'count', fill: 'color', sort: { x: '-y' }, tip: true }),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildDayOfWeek() {
    const dayNames = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const counts = new Array(7).fill(0);
    filteredPosts.forEach((p) => { counts[new Date(p.date).getDay()]++; });
    const data = dayNames.map((name, i) => ({ day: name, count: counts[i] }));

    renderChart(dayOfWeekEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 300,
      width: dayOfWeekEl?.clientWidth ?? 500,
      x: { label: null, padding: 0.3 },
      y: { label: 'Posts', grid: true },
      marks: [
        Plot.barY(data, { x: 'day', y: 'count', fill: '#8b5cf6', tip: true }),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildReadingTime() {
    const buckets: Record<string, number> = { '1-3': 0, '4-6': 0, '7-9': 0, '10+': 0 };
    filteredPosts.forEach((p) => {
      if (p.readingTime <= 3) buckets['1-3']++;
      else if (p.readingTime <= 6) buckets['4-6']++;
      else if (p.readingTime <= 9) buckets['7-9']++;
      else buckets['10+']++;
    });
    const data = Object.entries(buckets).map(([range, count]) => ({ range: range + ' min', count }));

    renderChart(readingTimeEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 300,
      width: readingTimeEl?.clientWidth ?? 500,
      x: { label: null, padding: 0.3 },
      y: { label: 'Posts', grid: true },
      marks: [
        Plot.barY(data, { x: 'range', y: 'count', fill: '#ec4899', tip: true }),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildTopicEvolution() {
    const top5 = Object.entries(
      filteredPosts.reduce<Record<string, number>>((acc, p) => {
        p.tags.forEach((t) => { acc[t] = (acc[t] || 0) + 1; });
        return acc;
      }, {})
    ).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([t]) => t);

    if (top5.length === 0) return;

    const tagByM: Record<string, Record<string, number>> = {};
    filteredPosts.forEach((p) => {
      const m = p.date.substring(0, 7);
      if (!tagByM[m]) tagByM[m] = {};
      p.tags.filter((t) => top5.includes(t)).forEach((t) => {
        tagByM[m][t] = (tagByM[m][t] || 0) + 1;
      });
    });

    const data: { month: Date; tag: string; count: number }[] = [];
    Object.entries(tagByM).sort(([a], [b]) => a.localeCompare(b)).forEach(([m, tags]) => {
      top5.forEach((tag) => {
        data.push({ month: new Date(m + '-01'), tag, count: tags[tag] || 0 });
      });
    });

    renderChart(topicEvolutionEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 350,
      width: topicEvolutionEl?.clientWidth ?? 700,
      x: { label: null, type: 'time' },
      y: { label: 'Posts', grid: true },
      color: { legend: true, range: CHART_PALETTE.slice(0, 5) },
      marks: [
        Plot.lineY(data, { x: 'month', y: 'count', stroke: 'tag', strokeWidth: 2, curve: 'catmull-rom', tip: true }),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildWordCount() {
    const buckets: Record<string, number> = { '0-1k': 0, '1-2k': 0, '2-3k': 0, '3-4k': 0, '4k+': 0 };
    filteredPosts.forEach((p) => {
      if (p.wordCount <= 1000) buckets['0-1k']++;
      else if (p.wordCount <= 2000) buckets['1-2k']++;
      else if (p.wordCount <= 3000) buckets['2-3k']++;
      else if (p.wordCount <= 4000) buckets['3-4k']++;
      else buckets['4k+']++;
    });
    const data = Object.entries(buckets).map(([range, count]) => ({ range: range + ' words', count }));

    renderChart(wordCountEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 300,
      width: wordCountEl?.clientWidth ?? 500,
      x: { label: null, padding: 0.3 },
      y: { label: 'Posts', grid: true },
      marks: [
        Plot.barY(data, { x: 'range', y: 'count', fill: '#14b8a6', tip: true }),
        Plot.ruleY([0]),
      ],
    }));
  }

  function buildScatter() {
    const data = filteredPosts.map((p) => ({
      wordCount: p.wordCount,
      readingTime: p.readingTime,
      title: p.title,
      hasCode: p.hasCode,
    }));

    if (data.length === 0) return;

    renderChart(scatterEl, () => Plot.plot({
      ...getPlotTheme(),
      height: 350,
      width: scatterEl?.clientWidth ?? 700,
      x: { label: 'Word Count', grid: true },
      y: { label: 'Reading Time (min)', grid: true },
      color: { legend: true, domain: [false, true], range: ['#6366f1', '#10b981'], tickFormat: (d: boolean) => d ? 'With Code' : 'No Code' },
      marks: [
        Plot.dot(data, {
          x: 'wordCount', y: 'readingTime', fill: 'hasCode',
          fillOpacity: 0.7, r: 6, stroke: 'white', strokeWidth: 1,
          tip: true,
          title: (d: { title: string; wordCount: number; readingTime: number }) => `${d.title}\n${d.wordCount.toLocaleString()} words, ${d.readingTime} min`,
        }),
        Plot.linearRegressionY(data, { x: 'wordCount', y: 'readingTime', stroke: '#ef4444', strokeWidth: 1.5, strokeDasharray: '6 4' }),
      ],
    }));
  }

  function buildAllCharts() {
    if (filteredPosts.length === 0) return;
    buildPostsOverTime();
    buildTopTags();
    buildDayOfWeek();
    buildReadingTime();
    buildTopicEvolution();
    buildWordCount();
    buildScatter();
  }

  function switchYear(year: string) {
    currentYear = year;
  }

  $effect(() => {
    void filteredPosts;
    void isDark;
    buildAllCharts();
  });

  onMount(() => {
    checkTheme();
    const observer = new MutationObserver(() => {
      checkTheme();
    });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ['class'] });
    return () => observer.disconnect();
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
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6">
      <div class="card p-5 md:p-6">
        <h3 class="text-xs md:text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Total Posts</h3>
        <p class="text-3xl md:text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length}</p>
      </div>
      <div class="card p-5 md:p-6">
        <h3 class="text-xs md:text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Total Words</h3>
        <p class="text-3xl md:text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{totalWords.toLocaleString()}</p>
      </div>
      <div class="card p-5 md:p-6">
        <h3 class="text-xs md:text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Unique Tags</h3>
        <p class="text-3xl md:text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{uniqueTags.length}</p>
      </div>
      <div class="card p-5 md:p-6">
        <h3 class="text-xs md:text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Avg Reading</h3>
        <p class="text-3xl md:text-4xl font-bold text-[var(--md-sys-color-on-surface)]">{avgReading}m</p>
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
              <span class="text-lg font-semibold" style="color: {diff > 0 ? 'var(--md-sys-color-success, #10b981)' : diff < 0 ? 'var(--md-sys-color-error)' : 'var(--md-sys-color-outline)'}">
                {diff > 0 ? '\u25B2' : diff < 0 ? '\u25BC' : '\u2014'} {Math.abs(Number(pct))}%
              </span>
            </div>
            <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mt-1">vs {yoy.prevYear}: {item.prev.toLocaleString()}{item.suffix}</p>
          </div>
        {/each}
      </div>
      {#if yoy.isPartial}
        <p class="text-xs text-[var(--md-sys-color-on-surface-variant)] mt-4 text-center">* {currentYear} is still in progress. Comparison reflects partial year data.</p>
      {/if}
    </section>
  {/if}
{/if}

<!-- Charts Section -->
<section aria-labelledby="charts-heading">
  <h2 id="charts-heading" class="sr-only">Data Visualizations</h2>
  <div class="max-w-6xl mx-auto space-y-12">

    <!-- Posts Over Time -->
    <div class="card p-6 md:p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Posts Over Time</h2>
      <div bind:this={postsOverTimeEl} class="w-full overflow-x-auto" role="img" aria-label="Area chart showing blog posts published over time"></div>
    </div>

    <!-- Two Column: Top Tags + Day of Week -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card p-6 md:p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Top Tags</h2>
        <div bind:this={topTagsEl} class="w-full overflow-x-auto" role="img" aria-label="Bar chart showing most used tags"></div>
      </div>
      <div class="card p-6 md:p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Publishing by Day</h2>
        <div bind:this={dayOfWeekEl} class="w-full overflow-x-auto" role="img" aria-label="Bar chart showing publishing patterns by day of week"></div>
      </div>
    </div>

    <!-- NEW: Word Count vs Reading Time Scatter -->
    <div class="card p-6 md:p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Word Count vs Reading Time</h2>
      <p class="text-sm text-[var(--md-sys-color-on-surface-variant)] mb-4">Each dot is a post. Dashed line shows the linear trend. Color indicates whether the post contains code examples.</p>
      <div bind:this={scatterEl} class="w-full overflow-x-auto" role="img" aria-label="Scatter plot showing word count versus reading time for each post"></div>
    </div>

    <!-- Content + Code Stats side by side -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="card p-6 md:p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Reading Time Distribution</h2>
        <div bind:this={readingTimeEl} class="w-full overflow-x-auto" role="img" aria-label="Bar chart showing reading time distribution"></div>
      </div>

      <div class="card p-6 md:p-8">
        <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Reading Time Insights</h2>
        <div class="space-y-4">
          <div class="border-b border-[var(--md-sys-color-outline-variant)] pb-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Median</h3>
            <p class="text-3xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? medianReading + ' min' : '-'}</p>
          </div>
          <div class="flex gap-6">
            <div class="flex-1">
              <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">25th %ile</h3>
              <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? p25 + 'm' : '-'}</p>
            </div>
            <div class="flex-1">
              <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">75th %ile</h3>
              <p class="text-2xl font-bold text-[var(--md-sys-color-on-surface)]">{filteredPosts.length > 0 ? p75 + 'm' : '-'}</p>
            </div>
          </div>
          <div class="border-t border-[var(--md-sys-color-outline-variant)] pt-4">
            <h3 class="text-sm font-medium text-[var(--md-sys-color-on-surface-variant)] uppercase tracking-wider mb-2">Technical Content</h3>
            <p class="text-2xl font-bold text-[var(--md-sys-color-tertiary)]">{postsWithCode} of {filteredPosts.length} posts</p>
            <div class="w-full bg-[var(--md-sys-color-surface-container)] rounded-full h-3 mt-2">
              <div class="h-3 rounded-full transition-all duration-500" style="width: {codePercent}%; background-color: var(--md-sys-color-tertiary)"></div>
            </div>
            <p class="text-xs text-[var(--md-sys-color-on-surface-variant)] mt-1">{codePercent}% include code blocks</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Publishing Activity Heatmap -->
    <div class="card p-6 md:p-8">
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
                    {@const bgColor = getHeatmapColor(count, heatmapResult.maxCount)}
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
      <div class="mt-6 flex items-center justify-center gap-2">
        <span class="text-sm text-[var(--md-sys-color-on-surface-variant)]">Less</span>
        <div class="flex gap-2">
          {#each (isDark ? DARK_HEATMAP.slice(1) : LIGHT_HEATMAP.slice(1)) as color}
            <div class="w-12 h-12 min-h-[44px] min-w-[44px] rounded flex-shrink-0" style="background-color: {color}"></div>
          {/each}
        </div>
        <span class="text-sm text-[var(--md-sys-color-on-surface-variant)]">More</span>
      </div>
    </div>

    <!-- Tag Cloud -->
    <div class="card p-6 md:p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Tag Cloud</h2>
      <div class="flex flex-wrap gap-3 justify-center min-h-[200px]" role="list" aria-label="Tag cloud">
        {#each tagCountsSorted as [tag, count], idx}
          {@const maxCount = tagCountsSorted[0]?.[1] || 1}
          {@const size = 0.8 + (count / maxCount) * 1.5}
          {@const color = CHART_PALETTE[idx % CHART_PALETTE.length]}
          {@const textColor = isDark ? TAG_TEXT_COLORS_DARK[idx % TAG_TEXT_COLORS_DARK.length] : TAG_TEXT_COLORS_LIGHT[idx % TAG_TEXT_COLORS_LIGHT.length]}
          {@const borderColor = isDark ? TAG_TEXT_COLORS_DARK[idx % TAG_TEXT_COLORS_DARK.length] : color}
          <li class="list-none">
            <a href="/tags/{tag}/"
               class="inline-block px-4 py-2 min-h-[44px] rounded-full transition-transform hover:scale-110"
               style="font-size: {size}rem; background-color: {color}20; color: {textColor}; border: 2px solid {borderColor}"
               title="{tag}: {count} post{count !== 1 ? 's' : ''}">
              {tag} <span class="text-xs" style="color: {textColor}">({count})</span>
            </a>
          </li>
        {/each}
      </div>
    </div>

    <!-- Topic Evolution -->
    <div class="card p-6 md:p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Topic Evolution Over Time</h2>
      <div bind:this={topicEvolutionEl} class="w-full overflow-x-auto" role="img" aria-label="Line chart showing evolution of top 5 tags over time"></div>
    </div>

    <!-- Word Count Analysis -->
    <div class="card p-6 md:p-8">
      <h2 class="text-2xl font-bold text-[var(--md-sys-color-on-surface)] mb-6">Word Count Distribution</h2>
      <div bind:this={wordCountEl} class="w-full overflow-x-auto" role="img" aria-label="Bar chart showing word count distribution"></div>
    </div>

  </div>
</section>
