<script lang="ts">
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
</script>

<button
  type="button"
  onclick={toggle}
  class="md:hidden min-w-[44px] min-h-[44px] flex items-center justify-center rounded-lg text-[var(--md-sys-color-on-surface-variant)] hover:bg-[var(--md-sys-color-surface-container-high)] transition-colors"
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
  <div class="absolute top-16 left-0 right-0 md:hidden pb-3 border-b" style="background-color: var(--md-sys-color-surface-container); border-color: var(--md-sys-color-outline-variant)">
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
    background-color: var(--md-sys-color-primary-container);
    color: var(--md-sys-color-on-primary-container);
  }
  .inactive-link {
    color: var(--md-sys-color-on-surface-variant);
  }
  .inactive-link:hover {
    background-color: var(--md-sys-color-surface-container-high);
  }
</style>
