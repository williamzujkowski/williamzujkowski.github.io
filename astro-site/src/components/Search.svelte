<script lang="ts">
  import { onMount } from 'svelte';

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
  let results = $state<PagefindResult[]>([]);
  let isOpen = $state(false);
  let isLoading = $state(false);
  let inputEl: HTMLInputElement;
  let pagefind: PagefindModule | null = null;
  let debounceTimer: ReturnType<typeof setTimeout>;
  let previouslyFocused: HTMLElement | null = null;
  let dialogEl: HTMLDivElement;

  async function loadPagefind(): Promise<PagefindModule | null> {
    if (pagefind) return pagefind;
    if (typeof window === 'undefined') return null;
    try {
      const path = `${window.location.origin}/pagefind/pagefind.js`;
      pagefind = (await import(/* @vite-ignore */ path)) as PagefindModule;
      await pagefind.init();
      return pagefind;
    } catch {
      // Pagefind not available (dev mode) — search silently disabled
      return null;
    }
  }

  async function search() {
    clearTimeout(debounceTimer);
    if (query.length < 2) {
      results = [];
      return;
    }
    isLoading = true;
    debounceTimer = setTimeout(async () => {
      const pf = await loadPagefind();
      if (!pf) {
        isLoading = false;
        return;
      }
      const response = await pf.search(query);
      const loaded = await Promise.all(response.results.slice(0, 8).map((r) => r.data()));
      results = loaded;
      isLoading = false;
    }, 200);
  }

  function close() {
    isOpen = false;
    query = '';
    results = [];
    previouslyFocused?.focus();
    previouslyFocused = null;
  }

  function open() {
    isOpen = true;
    previouslyFocused = document.activeElement as HTMLElement | null;
    setTimeout(() => inputEl?.focus(), 50);
  }

  function trapFocus(e: KeyboardEvent) {
    if (e.key !== 'Tab') return;
    const focusable = dialogEl?.querySelectorAll<HTMLElement>(
      'input, a[href], button, [tabindex]:not([tabindex="-1"])'
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

    // Close search on View Transitions navigation
    const handleSwap = () => close();
    document.addEventListener('astro:after-swap', handleSwap);

    return () => {
      document.removeEventListener('keydown', handleKeydown);
      document.removeEventListener('astro:after-swap', handleSwap);
    };
  });
</script>

<!-- Search trigger button -->
<button
  type="button"
  onclick={open}
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
  <div class="search-overlay">
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
          oninput={search}
          type="text"
          placeholder="Search site..."
          class="search-input"
        />
        <kbd class="search-esc">ESC</kbd>
      </div>

      {#if results.length > 0}
        <ul class="search-results">
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
      {:else if isLoading}
        <div class="search-state">Searching...</div>
      {:else if query.length >= 2}
        <div class="search-state">
          No results for "{query}"
        </div>
      {:else}
        <div class="search-state is-hint">
          Type to search...
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
    font-family: var(--font-mono);
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
    background: rgba(0, 0, 0, 0.5);
  }
  .search-dialog {
    position: relative;
    width: 100%;
    max-width: 32rem;
    margin: 0 1rem;
    border-radius: 1rem;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
    overflow: hidden;
    background-color: var(--color-surface);
    border: 1px solid var(--color-border);
  }
  .search-input-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem;
    border-bottom: 1px solid var(--color-border);
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
  .search-esc {
    display: none;
    font-family: var(--font-mono);
    font-size: var(--text-micro, 0.75rem);
    padding: 0.125rem 0.375rem;
    border: 1px solid var(--color-border);
    border-radius: 0.25rem;
    color: var(--color-muted);
    line-height: 1;
  }
  @media (min-width: 640px) {
    .search-esc { display: inline-block; }
  }
  .search-results {
    max-height: 20rem;
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
    font-size: 0.875rem;
    margin-top: 0.25rem;
    color: var(--color-muted);
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  .search-state {
    padding: 2rem;
    text-align: center;
    color: var(--color-muted);
  }
  .search-state.is-hint {
    font-size: 0.875rem;
  }

  /* Style Pagefind highlight marks */
  :global(mark) {
    background-color: var(--color-surface);
    color: var(--color-fg);
    border-radius: 2px;
    padding: 0 2px;
  }
</style>
