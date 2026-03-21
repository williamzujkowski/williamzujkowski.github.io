<script lang="ts">
  import { onMount } from 'svelte';
  import { tweened } from 'svelte/motion';
  import { cubicOut } from 'svelte/easing';

  const progress = tweened(0, { duration: 100, easing: cubicOut });

  function updateProgress() {
    const article = document.querySelector('article');
    if (!article) return;

    const rect = article.getBoundingClientRect();
    const articleTop = rect.top + window.scrollY;
    const articleHeight = rect.height;
    const scrollY = window.scrollY;
    const windowHeight = window.innerHeight;

    if (scrollY < articleTop) {
      progress.set(0);
    } else if (scrollY + windowHeight >= articleTop + articleHeight) {
      progress.set(100);
    } else {
      const scrolled = scrollY - articleTop;
      const total = articleHeight - windowHeight;
      progress.set(total > 0 ? Math.min(100, (scrolled / total) * 100) : 100);
    }
  }

  onMount(() => {
    updateProgress();
    window.addEventListener('scroll', updateProgress, { passive: true });
    window.addEventListener('resize', updateProgress, { passive: true });

    // Re-init after View Transitions page swap
    const handleSwap = () => {
      progress.set(0, { duration: 0 });
      requestAnimationFrame(updateProgress);
    };
    document.addEventListener('astro:after-swap', handleSwap);

    return () => {
      window.removeEventListener('scroll', updateProgress);
      window.removeEventListener('resize', updateProgress);
      document.removeEventListener('astro:after-swap', handleSwap);
    };
  });
</script>

<div
  class="progress-bar"
  role="progressbar"
  aria-label="Reading progress"
  aria-valuenow={Math.round($progress)}
  aria-valuemin={0}
  aria-valuemax={100}
>
  <div class="progress-fill" style="width: {$progress}%"></div>
</div>

<style>
  .progress-bar {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    z-index: 100;
    background: transparent;
    pointer-events: none;
  }
  .progress-fill {
    height: 100%;
    background: var(--accent);
    transition: width 0.1s ease-out;
    will-change: width;
  }
</style>
