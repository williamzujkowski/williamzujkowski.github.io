<script lang="ts">
  import { onMount } from 'svelte';

  interface SearchResult {
    title: string;
    description: string;
    url: string;
    tags: string[];
    date: string;
  }

  let query = $state('');
  let results = $state<SearchResult[]>([]);
  let isOpen = $state(false);
  let posts: SearchResult[] = [];
  let inputEl: HTMLInputElement;

  onMount(async () => {
    // Build search index from all post links on the page or fetch from a JSON endpoint
    const allLinks = document.querySelectorAll('article a[href^="/posts/"]');
    const seen = new Set<string>();

    allLinks.forEach((link) => {
      const href = link.getAttribute('href') ?? '';
      if (seen.has(href)) return;
      seen.add(href);

      const article = link.closest('article');
      if (!article) return;

      const title = link.textContent?.trim() ?? '';
      const desc = article.querySelector('p')?.textContent?.trim() ?? '';
      const tagEls = article.querySelectorAll('.chip');
      const tags = Array.from(tagEls).map((el) => el.textContent?.trim() ?? '');

      posts.push({ title, description: desc, url: href, tags, date: '' });
    });

    // Keyboard shortcut: / to open search
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && !isOpen && !['INPUT', 'TEXTAREA', 'SELECT'].includes((e.target as HTMLElement).tagName)) {
        e.preventDefault();
        isOpen = true;
        setTimeout(() => inputEl?.focus(), 50);
      }
      if (e.key === 'Escape' && isOpen) {
        isOpen = false;
        query = '';
        results = [];
      }
    });
  });

  function search() {
    if (query.length < 2) {
      results = [];
      return;
    }
    const q = query.toLowerCase();
    results = posts
      .filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q) ||
          p.tags.some((t) => t.toLowerCase().includes(q))
      )
      .slice(0, 8);
  }

  function close() {
    isOpen = false;
    query = '';
    results = [];
  }
</script>

<!-- Search trigger button -->
<button
  type="button"
  onclick={() => { isOpen = true; setTimeout(() => inputEl?.focus(), 50); }}
  class="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg text-[var(--md-sys-color-on-surface-variant)] hover:bg-[var(--md-sys-color-surface-container-high)] transition-colors"
  aria-label="Search posts"
>
  <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
    <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
  </svg>
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
      aria-label="Search posts"
    >
      <div class="flex items-center gap-3 p-4 border-b" style="border-color: var(--md-sys-color-outline-variant)">
        <svg class="w-5 h-5 text-[var(--md-sys-color-on-surface-variant)] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
          <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          bind:this={inputEl}
          bind:value={query}
          oninput={search}
          type="text"
          placeholder="Search posts..."
          class="flex-grow bg-transparent outline-none text-[var(--md-sys-color-on-surface)] placeholder:text-[var(--md-sys-color-on-surface-variant)]"
        />
        <kbd class="hidden sm:inline-block text-xs px-1.5 py-0.5 rounded border text-[var(--md-sys-color-on-surface-variant)]" style="border-color: var(--md-sys-color-outline-variant)">ESC</kbd>
      </div>

      {#if results.length > 0}
        <ul class="max-h-80 overflow-y-auto p-2">
          {#each results as result}
            <li>
              <a
                href={result.url}
                class="block px-4 py-3 rounded-lg no-underline hover:no-underline transition-colors"
                style="color: var(--md-sys-color-on-surface)"
                onmouseenter={(e) => (e.currentTarget as HTMLElement).style.backgroundColor = 'var(--md-sys-color-surface-container-high)'}
                onmouseleave={(e) => (e.currentTarget as HTMLElement).style.backgroundColor = 'transparent'}
                onclick={close}
              >
                <div class="font-medium">{result.title}</div>
                {#if result.description}
                  <div class="text-sm mt-1 line-clamp-1" style="color: var(--md-sys-color-on-surface-variant)">
                    {result.description}
                  </div>
                {/if}
              </a>
            </li>
          {/each}
        </ul>
      {:else if query.length >= 2}
        <div class="p-8 text-center" style="color: var(--md-sys-color-on-surface-variant)">
          No results for "{query}"
        </div>
      {:else}
        <div class="p-8 text-center text-sm" style="color: var(--md-sys-color-on-surface-variant)">
          Type to search posts...
        </div>
      {/if}
    </div>
  </div>
{/if}
