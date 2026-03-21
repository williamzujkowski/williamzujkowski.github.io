<script lang="ts">
  import { onMount } from 'svelte';

  interface NavLink {
    label: string;
    href: string;
    active: boolean;
  }

  let { links }: { links: NavLink[] } = $props();
  let isOpen = $state(false);

  function toggle() {
    isOpen = !isOpen;
  }

  function close() {
    isOpen = false;
  }

  onMount(() => {
    // Close menu on View Transitions navigation
    const handleSwap = () => close();
    document.addEventListener('astro:after-swap', handleSwap);

    // Close on Escape key
    const handleKeydown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen) close();
    };
    document.addEventListener('keydown', handleKeydown);

    return () => {
      document.removeEventListener('astro:after-swap', handleSwap);
      document.removeEventListener('keydown', handleKeydown);
    };
  });
</script>

<button
  type="button"
  onclick={toggle}
  class="md:hidden min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg text-[var(--text-muted)] hover:bg-[var(--surface)] transition-colors"
  aria-label={isOpen ? 'Close menu' : 'Open menu'}
  aria-expanded={isOpen}
>
  {#if isOpen}
    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
    </svg>
  {:else}
    <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
      <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
    </svg>
  {/if}
</button>

{#if isOpen}
  <div
    class="absolute top-16 left-0 right-0 md:hidden pb-3 border-b"
    style="background-color: var(--surface); border-color: var(--border)"
  >
    <div class="space-y-1 px-4 pt-2">
      {#each links as link}
        <a
          href={link.href}
          onclick={close}
          class="block px-4 py-3 min-h-[44px] rounded-lg text-base font-medium transition-colors no-underline"
          class:active-link={link.active}
          class:inactive-link={!link.active}
        >
          {link.label}
        </a>
      {/each}
    </div>
  </div>
{/if}

<style>
  .active-link {
    background-color: var(--surface);
    color: var(--accent);
  }
  .inactive-link {
    color: var(--text-muted);
  }
  .inactive-link:hover {
    background-color: var(--surface);
  }
</style>
