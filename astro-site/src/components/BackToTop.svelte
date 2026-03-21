<script lang="ts">
  import { onMount } from 'svelte';
  import { fly } from 'svelte/transition';

  let visible = $state(false);

  onMount(() => {
    const check = () => {
      visible = window.scrollY > 400;
    };
    window.addEventListener('scroll', check, { passive: true });
    return () => window.removeEventListener('scroll', check);
  });

  function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }
</script>

{#if visible}
  <button
    type="button"
    onclick={scrollToTop}
    class="fixed bottom-6 right-6 z-50 min-w-[44px] min-h-[44px] flex items-center justify-center rounded-full transition-all"
    style="background-color: var(--accent); color: var(--inverse-text); box-shadow: 0 4px 8px rgba(0,0,0,0.15)"
    aria-label="Back to top"
    transition:fly={{ y: 20, duration: 200 }}
  >
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M5 15l7-7 7 7" />
    </svg>
  </button>
{/if}
