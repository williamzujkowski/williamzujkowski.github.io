<script lang="ts">
  import { onMount, tick } from 'svelte';

  interface PagefindResult {
    id: string;
    url: string;
    excerpt: string;
    meta: {
      title?: string;
      image?: string;
    };
    sub_results?: {
      title: string;
      url: string;
      excerpt: string;
    }[];
  }

  interface PagefindResponse {
    results: { id: string; data: () => Promise<PagefindResult> }[];
  }

  interface PagefindModule {
    init: () => Promise<void>;
    search: (query: string) => Promise<PagefindResponse>;
  }

  let query = $state('');
  let ready = $state(false);
  let results = $state<PagefindResult[]>([]);
  let isOpen = $state(false);
  let isLoading = $state(false);
  let error = $state('');
  let matches = $state<PagefindResponse['results']>([]);
  const pageSize = 8;
  let generation = 0;
  let pagefindLoading: Promise<PagefindModule> | null = null;
  let loadAttempt = 0;
  let inputEl: HTMLInputElement;
  let pagefind: PagefindModule | null = null;
  let debounceTimer: ReturnType<typeof setTimeout>;
  let previouslyFocused: HTMLElement | null = null;
  let dialogEl: HTMLDivElement;
  let resultsEl: HTMLUListElement;
  let moreEl: HTMLButtonElement;
  let retryEl: HTMLButtonElement;
  let overlayEl: HTMLDivElement;
  let inertedEls: HTMLElement[] = [];

  // The dialog is mounted inside <header> (site-masthead-tools-right), not
  // portalled to <body> -- so we can't just inert() the whole header (that
  // would inert the dialog too, since it's a header descendant). Instead,
  // walk up from the overlay to <body>, inerting true siblings at every
  // level. That covers the header's other regions (nav, nameplate, the
  // theme deck/toggle) *and* <main>/<footer> as siblings of <header> --
  // without ever touching the dialog's own ancestor chain.
  function inertOutside(el: HTMLElement): HTMLElement[] {
    const inerted: HTMLElement[] = [];
    let node: HTMLElement | null = el;
    while (node && node !== document.body) {
      const parent: HTMLElement | null = node.parentElement;
      if (parent) {
        for (const sibling of Array.from(parent.children)) {
          if (sibling !== node && sibling instanceof HTMLElement && !sibling.hasAttribute('inert')) {
            sibling.setAttribute('inert', '');
            // Ownership marker: only clear elements THIS dialog inerted, so a
            // second modal claiming the same element later isn't un-inerted.
            sibling.setAttribute('data-search-inert', '');
            inerted.push(sibling);
          }
        }
      }
      node = parent;
    }
    return inerted;
  }

  function clearInert(els: HTMLElement[]) {
    for (const el of els) {
      if (el.hasAttribute('data-search-inert')) {
        el.removeAttribute('inert');
        el.removeAttribute('data-search-inert');
      }
    }
  }

  async function loadPagefind(): Promise<PagefindModule> {
    if (pagefind) return pagefind;
    if (!pagefindLoading) {
      // Cache only a successfully initialized module. A failed import needs a
      // fresh URL on retry because browsers cache failed module fetches.
      const attempt = loadAttempt++;
      const path = `${window.location.origin}/pagefind/pagefind.js${attempt ? `?retry=${attempt}` : ''}`;
      pagefindLoading = (async () => {
        const module = (await import(/* @vite-ignore */ path)) as PagefindModule;
        await module.init();
        pagefind = module;
        return module;
      })();
    }
    try {
      return await pagefindLoading;
    } finally {
      pagefindLoading = null;
    }
  }

  function invalidateSearch() {
    clearTimeout(debounceTimer);
    generation += 1;
    isLoading = false;
  }

  function search() {
    invalidateSearch();
    const request = generation;
    const term = query.trim();
    results = [];
    matches = [];
    error = '';
    if (term.length < 2) return;

    isLoading = true;
    debounceTimer = setTimeout(async () => {
      try {
        const pf = await loadPagefind();
        if (request !== generation || !isOpen) return;
        const response = await pf.search(term);
        if (request !== generation || !isOpen) return;
        const loaded = await Promise.all(response.results.slice(0, pageSize).map((r) => r.data()));
        if (request !== generation || !isOpen) return;
        matches = response.results;
        results = loaded;
      } catch {
        if (request === generation && isOpen) {
          error = 'Search is unavailable. Please try again.';
        }
      } finally {
        if (request === generation) isLoading = false;
      }
    }, 200);
  }

  async function loadMore() {
    if (isLoading) return;
    const request = generation;
    const firstNewResult = results.length;
    isLoading = true;
    error = '';
    try {
      const loaded = await Promise.all(matches.slice(results.length, results.length + pageSize).map((r) => r.data()));
      if (request !== generation || !isOpen) return;
      results = [...results, ...loaded];
      await tick();
      if (request === generation && isOpen) {
        resultsEl?.querySelectorAll<HTMLAnchorElement>('a')[firstNewResult]?.focus();
      }
    } catch {
      if (request === generation && isOpen) {
        const restoreFocus = document.activeElement === moreEl;
        error = 'More results could not be loaded. Please try again.';
        await tick();
        if (restoreFocus && request === generation && isOpen) retryEl?.focus();
      }
    } finally {
      if (request === generation) isLoading = false;
    }
  }

  function clearSearch() {
    query = '';
    search();
    inputEl?.focus();
  }

  function retrySearch() {
    // Retry disappears while loading. Keep keyboard focus inside the dialog.
    inputEl?.focus();
    if (results.length) void loadMore();
    else search();
  }

  function close() {
    invalidateSearch();
    isOpen = false;
    query = '';
    results = [];
    matches = [];
    error = '';
    clearInert(inertedEls);
    inertedEls = [];
    previouslyFocused?.focus();
    previouslyFocused = null;
  }

  async function open() {
    // Repeated shortcuts must preserve the original inert ownership and focus
    // target. Otherwise close() leaves the rest of the page inert.
    if (isOpen) {
      inputEl?.focus();
      return;
    }
    previouslyFocused = document.activeElement as HTMLElement | null;
    const opening = generation;
    isOpen = true;
    await tick();
    if (isOpen && opening === generation && overlayEl) {
      inertedEls = inertOutside(overlayEl);
      inputEl?.focus();
    }
  }

  function trapFocus(e: KeyboardEvent) {
    if (e.key !== 'Tab') return;
    const focusable = dialogEl?.querySelectorAll<HTMLElement>(
      'input, a[href], button:not(:disabled), [tabindex]:not([tabindex="-1"])'
    );
    if (!focusable || focusable.length === 0) return;
    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault();
      first.focus();
    }
  }

  onMount(() => {
    function handleKeydown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        open();
      }
      if (e.key === '/' && !isOpen && !['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement).tagName)) {
        e.preventDefault();
        open();
      }
      if (e.key === 'Escape' && isOpen) {
        close();
      }
    }
    document.addEventListener('keydown', handleKeydown);
    // SSR renders the trigger before its click handler is attached. Keep it
    // disabled until hydration completes so an early click cannot disappear.
    ready = true;

    // No astro:after-swap listener needed: without ClientRouter every
    // navigation is a full page load, which naturally tears this component
    // down (closed by construction) rather than leaving a stale dialog open.

    return () => {
      document.removeEventListener('keydown', handleKeydown);
      invalidateSearch();
      clearInert(inertedEls);
    };
  });
</script>

<!-- Search trigger button -->
<button
  type="button"
  onclick={open}
  disabled={!ready}
  class="search-trigger"
  aria-label="Search site"
>
  <svg class="search-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
  <kbd class="search-kbd">&sol;K</kbd>
</button>

<!-- Search dialog -->
{#if isOpen}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div bind:this={overlayEl} class="search-overlay">
    <!-- Backdrop -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="search-backdrop" onclick={close}></div>

    <!-- Dialog -->
    <div
      bind:this={dialogEl}
      class="search-dialog"
      role="dialog"
      aria-modal="true"
      aria-label="Search site"
      onkeydown={trapFocus}
    >
      <div class="search-input-row">
        <svg
          class="search-input-icon"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          bind:this={inputEl}
          bind:value={query}
          oninput={(event) => { query = event.currentTarget.value; search(); }}
          type="text"
          placeholder="Search site..."
          aria-label="Search site content"
          class="search-input"
        />
        {#if query}
          <button type="button" class="search-control" onclick={clearSearch}>Clear</button>
        {/if}
        <button type="button" class="search-control" onclick={close} aria-label="Close search">Close</button>
      </div>

      {#if results.length > 0}
        <ul bind:this={resultsEl} class="search-results">
          {#each results as result}
            <li>
              <a href={result.url} class="search-result-link" onclick={close}>
                <div class="search-result-title">
                  {result.meta?.title || 'Untitled'}
                </div>
                {#if result.excerpt}
                  <div class="search-result-excerpt">
                    {@html result.excerpt}
                  </div>
                {/if}
              </a>
            </li>
          {/each}
        </ul>
      {/if}
      <div class="search-state" role="status" aria-live="polite" aria-atomic="true">
        {#if isLoading}
          Searching...
        {:else if error}
          {error}
        {:else if results.length > 0}
          Showing {results.length} of {matches.length} results
        {:else if query.trim().length >= 2}
          No results for "{query.trim()}"
        {:else}
          Type at least two characters to search.
        {/if}
      </div>
      {#if error}
        <div class="search-actions">
          <button bind:this={retryEl} type="button" class="search-control" onclick={retrySearch}>Try again</button>
          <a href="/posts/" onclick={close}>Browse all posts</a>
        </div>
      {:else if matches.length > results.length}
        <div class="search-actions">
          <button bind:this={moreEl} type="button" class="search-control" onclick={loadMore} aria-disabled={isLoading}>Show more results</button>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Search trigger — Remarque tokens, no Tailwind (which isn't installed) */
  .search-trigger {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.375rem;
    min-width: 44px;
    min-height: 44px;
    padding: 0 0.5rem;
    background: transparent;
    border: none;
    border-radius: var(--radius-md, 0.5rem);
    color: var(--color-muted);
    cursor: pointer;
    transition: color var(--motion-fast, 180ms) var(--motion-easing, ease);
  }
  .search-trigger:hover {
    color: var(--color-fg);
    background: var(--color-surface);
  }
  .search-icon {
    width: 1.25rem;
    height: 1.25rem;
  }
  .search-kbd {
    display: none;
    /* font-family: mono — shared machine-voice rule in global.css (#274) */
    font-size: var(--text-micro);
    padding: 0.125rem 0.375rem;
    border: 1px solid var(--color-border);
    border-radius: 0.25rem;
    color: var(--color-muted);
    line-height: 1;
  }
  @media (min-width: 1024px) {
    .search-kbd { display: inline-block; }
  }

  /* Search dialog — migrated off dead Tailwind utilities to Remarque tokens (#206) */
  .search-overlay {
    position: fixed;
    inset: 0;
    z-index: 100;
    display: flex;
    align-items: flex-start;
    justify-content: center;
    padding-top: 10vh;
  }
  .search-backdrop {
    position: absolute;
    inset: 0;
    background: var(--color-overlay);
  }
  .search-dialog {
    position: relative;
    width: 100%;
    max-width: 32rem;
    margin: 0 1rem;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px var(--color-shadow);
    overflow: hidden;
    background-color: var(--color-surface);
    border: 1px solid var(--color-border-bold);
  }
  .search-input-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border-bottom: 1px solid var(--color-border-bold);
  }
  .search-input-icon {
    width: 1.25rem;
    height: 1.25rem;
    flex-shrink: 0;
    color: var(--color-muted);
  }
  .search-input {
    flex: 1 1 auto;
    min-width: 0;
    background: transparent;
    border: none;
    outline: none;
    font: inherit;
    color: var(--color-fg);
  }
  /* Visible keyboard-focus indicator — same convention as the site-wide
     `*:focus-visible` rule in global.css (2px solid accent, 2px offset).
     Restated here (rather than relying on the global rule) because this
     component's <style> is scoped and `.search-input { outline: none }`
     above would otherwise leave keyboard users with zero focus indication
     inside the dialog (#321). */
  .search-input:focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
    border-radius: 2px;
  }
  .search-control {
    min-width: 44px;
    min-height: 44px;
    padding: 0.375rem 0.625rem;
    border: 1px solid var(--color-border-bold);
    border-radius: var(--radius-md, 0.5rem);
    background: var(--color-surface);
    color: var(--color-fg);
    font: inherit;
    font-size: var(--text-meta);
    cursor: pointer;
  }
  .search-control[aria-disabled='true'] {
    cursor: wait;
  }
  .search-control:focus-visible {
    outline: 2px solid var(--color-accent);
    outline-offset: 2px;
  }
  .search-actions {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 0.75rem;
    padding: 0 1rem 1rem;
    text-align: center;
  }
  .search-results {
    max-height: min(20rem, 45dvh);
    overflow-y: auto;
    padding: 0.5rem;
    margin: 0;
    list-style: none;
  }
  .search-result-link {
    display: block;
    padding: 0.75rem 1rem;
    border-radius: var(--radius-md, 0.5rem);
    text-decoration: none;
    color: var(--color-fg);
    transition: background-color var(--motion-fast, 180ms) var(--motion-easing, ease);
  }
  .search-result-link:hover {
    background-color: var(--color-bg-subtle);
    text-decoration: none;
  }
  .search-result-title {
    font-weight: 500;
  }
  .search-result-excerpt {
    font-size: var(--text-meta);
    margin-top: 0.25rem;
    color: var(--color-muted);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .search-state {
    padding: 1rem;
    font-size: var(--text-meta);
    text-align: center;
    color: var(--color-muted);
  }

  /* Style Pagefind highlight marks */
  :global(mark) {
    background-color: var(--color-surface);
    color: var(--color-fg);
    border-radius: 2px;
    padding: 0 2px;
  }
</style>
