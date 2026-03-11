<script lang="ts">
  import { onMount } from 'svelte';

  onMount(() => {
    // Add copy buttons to all code blocks
    document.querySelectorAll('pre').forEach((pre) => {
      if (pre.querySelector('.copy-btn')) return;

      const wrapper = document.createElement('div');
      wrapper.style.position = 'relative';
      pre.parentNode?.insertBefore(wrapper, pre);
      wrapper.appendChild(pre);

      const btn = document.createElement('button');
      btn.className = 'copy-btn';
      btn.setAttribute('aria-label', 'Copy code');
      btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>`;

      btn.addEventListener('click', async () => {
        const code = pre.querySelector('code')?.textContent ?? pre.textContent ?? '';
        try {
          await navigator.clipboard.writeText(code);
          btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>`;
          setTimeout(() => {
            btn.innerHTML = `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>`;
          }, 2000);
        } catch {
          // Fallback for older browsers
          const textarea = document.createElement('textarea');
          textarea.value = code;
          textarea.style.position = 'fixed';
          textarea.style.left = '-9999px';
          document.body.appendChild(textarea);
          textarea.select();
          document.execCommand('copy');
          document.body.removeChild(textarea);
        }
      });

      wrapper.appendChild(btn);
    });
  });
</script>

<style>
  :global(.copy-btn) {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    padding: 0.375rem;
    border-radius: var(--md-sys-shape-corner-small, 0.5rem);
    background-color: var(--md-sys-color-surface-container-high, #e8e4e4);
    color: var(--md-sys-color-on-surface-variant, #444748);
    border: 1px solid var(--md-sys-color-outline-variant, #c4c7c8);
    cursor: pointer;
    opacity: 0;
    transition: opacity 150ms ease;
    z-index: 1;
  }

  :global(div:hover > .copy-btn) {
    opacity: 1;
  }

  :global(.copy-btn:hover) {
    background-color: var(--md-sys-color-surface-container-highest, #e2dede);
  }
</style>
