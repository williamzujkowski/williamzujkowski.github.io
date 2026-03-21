<script lang="ts">
  import { onMount } from 'svelte';

  let isDark = $state(false);

  function syncState() {
    isDark = document.documentElement.classList.contains('dark');
  }

  onMount(() => {
    syncState();

    // Re-sync after View Transitions page swap
    document.addEventListener('astro:after-swap', syncState);
    return () => document.removeEventListener('astro:after-swap', syncState);
  });

  function toggle() {
    isDark = !isDark;
    document.documentElement.classList.toggle('dark', isDark);
    document.documentElement.classList.toggle('light', !isDark);
    localStorage.theme = isDark ? 'dark' : 'light';

    // Update theme-color meta tag
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) {
      meta.setAttribute('content', isDark ? '#131313' : '#4338ca');
    }
  }
</script>

<button
  type="button"
  onclick={toggle}
  class="min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg text-[var(--text-muted)] hover:bg-[var(--surface)] transition-colors"
  aria-label={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
>
  {#if isDark}
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
      />
    </svg>
  {:else}
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
      />
    </svg>
  {/if}
</button>
