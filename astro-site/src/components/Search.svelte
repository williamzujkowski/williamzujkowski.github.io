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

  async function loadPagefind(): Promise<PagefindModule | null> {
    if (pagefind) return pagefind;
    if (typeof window === 'undefined') return null;
    try {
      const path = `${window.location.origin}/pagefind/pagefind.js`;
      pagefind = await import(/* @vite-ignore */ path) as PagefindModule;
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
      const loaded = await Promise.all(
        response.results.slice(0, 8).map((r) => r.data())
      );
      results = loaded;
      isLoading = false;
    }, 200);
  }

  function close() {
    isOpen = false;
    query = '';
    results = [];
  }

  function open() {
    isOpen = true;
    setTimeout(() => inputEl?.focus(), 50);
  }

  onMount(() => {
    function handleKeydown(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        open();
      }
      if (
        e.key === '/' &&
        !isOpen &&
        !['INPUT', 'TEXTAREA', 'SELECT'].includes(
          (e.target as HTMLElement).tagName
        )
      ) {
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
  class="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg text-[var(--md-sys-color-on-surface-variant)] hover:bg-[var(--md-sys-color-surface-container-high)] transition-colors"
  aria-label="Search site"
>
  <svg
    class="w-5 h-5"
    fill="none"
    viewBox="0 0 24 24"
    stroke="currentColor"
    stroke-width="2"
  >
    <path
      stroke-linecap="round"
      stroke-linejoin="round"
      d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
    />
  </svg>
  <kbd class="hidden lg:inline-block ml-1.5 text-[10px] px-1.5 py-0.5 rounded border font-sans"
    style="color: var(--md-sys-color-on-surface-variant); border-color: var(--md-sys-color-outline-variant); opacity: 0.7"
  >&sol;K</kbd>
</button>

<!-- Search dialog -->
{#if isOpen}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="fixed inset-0 z-[100] flex items-start justify-center pt-[10vh]"
    onkeydown={(e) => e.key === 'Escape' && close()}
  >
    <!-- Backdrop -->
    <!-- svelte-ignore a11y_no_static_element_interactions -->
    <div class="absolute inset-0 bg-black/50" onclick={close}></div>

    <!-- Dialog -->
    <div
      class="relative w-full max-w-lg mx-4 rounded-2xl shadow-2xl overflow-hidden"
      style="background-color: var(--md-sys-color-surface-container); border: 1px solid var(--md-sys-color-outline-variant)"
      role="dialog"
      aria-label="Search site"
    >
      <div
        class="flex items-center gap-3 p-4 border-b"
        style="border-color: var(--md-sys-color-outline-variant)"
      >
        <svg
          class="w-5 h-5 flex-shrink-0"
          style="color: var(--md-sys-color-on-surface-variant)"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          stroke-width="2"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <input
          bind:this={inputEl}
          bind:value={query}
          oninput={search}
          type="text"
          placeholder="Search site..."
          class="flex-grow bg-transparent outline-none"
          style="color: var(--md-sys-color-on-surface)"
        />
        <kbd
          class="hidden sm:inline-block text-xs px-1.5 py-0.5 rounded border"
          style="color: var(--md-sys-color-on-surface-variant); border-color: var(--md-sys-color-outline-variant)"
          >ESC</kbd
        >
      </div>

      {#if results.length > 0}
        <ul class="max-h-80 overflow-y-auto p-2">
          {#each results as result}
            <li>
              <a
                href={result.url}
                class="block px-4 py-3 rounded-lg no-underline hover:no-underline transition-colors"
                style="color: var(--md-sys-color-on-surface)"
                onmouseenter={(e) =>
                  ((e.currentTarget as HTMLElement).style.backgroundColor =
                    'var(--md-sys-color-surface-container-high)')}
                onmouseleave={(e) =>
                  ((e.currentTarget as HTMLElement).style.backgroundColor =
                    'transparent')}
                onclick={close}
              >
                <div class="font-medium">
                  {result.meta?.title || 'Untitled'}
                </div>
                {#if result.excerpt}
                  <div
                    class="text-sm mt-1 line-clamp-2"
                    style="color: var(--md-sys-color-on-surface-variant)"
                  >
                    {@html result.excerpt}
                  </div>
                {/if}
              </a>
            </li>
          {/each}
        </ul>
      {:else if isLoading}
        <div
          class="p-8 text-center"
          style="color: var(--md-sys-color-on-surface-variant)"
        >
          Searching...
        </div>
      {:else if query.length >= 2}
        <div
          class="p-8 text-center"
          style="color: var(--md-sys-color-on-surface-variant)"
        >
          No results for "{query}"
        </div>
      {:else}
        <div
          class="p-8 text-center text-sm"
          style="color: var(--md-sys-color-on-surface-variant)"
        >
          Type to search...
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Style Pagefind highlight marks */
  :global(mark) {
    background-color: var(--md-sys-color-tertiary-container);
    color: var(--md-sys-color-on-tertiary-container);
    border-radius: 2px;
    padding: 0 2px;
  }
</style>
