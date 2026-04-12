import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import rehypeMermaid from 'rehype-mermaid';
import remarkSmartypants from 'remark-smartypants';
import { visit } from 'unist-util-visit';

/**
 * Shiki transformer: extract title="filename" from code fence meta
 * and render a filename tab inside the code block.
 *
 * Usage in markdown: ```python title="main.py"
 * Renders: <div class="code-block"><div class="code-title">main.py</div><pre>...</pre></div>
 */
function transformerCodeTitle() {
  return {
    name: 'code-title',
    pre(node) {
      const meta = this.options.meta?.__raw;
      if (!meta) return;
      const match = meta.match(/title="([^"]+)"/);
      if (!match) return;
      const title = match[1]
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      // Add a data attribute so CSS can render the title via ::before
      node.properties['data-title'] = title;
    },
  };
}

/**
 * Convert <picture> elements (from rehype-mermaid dark mode) into
 * two <img> elements with class-based toggling so both OS preference
 * AND the manual .dark/.light toggle work.
 *
 * Input:  <picture><source media="(prefers-color-scheme: dark)" srcset="dark.svg"><img src="light.svg"></picture>
 * Output: <div class="mermaid-themed"><img class="mermaid-light" src="light.svg"><img class="mermaid-dark" src="dark.svg"></div>
 */
function rehypeMermaidDualTheme() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index == null) return;
      if (node.tagName !== 'picture') return;

      // Find the <source> (dark) and <img> (light) children
      const source = node.children.find(
        (c) => c.type === 'element' && c.tagName === 'source'
      );
      const img = node.children.find(
        (c) => c.type === 'element' && c.tagName === 'img'
      );
      if (!source || !img) return;

      // Only process mermaid pictures (check if source has prefers-color-scheme media)
      const media = source.properties?.media?.toString() || '';
      if (!media.includes('prefers-color-scheme')) return;

      const lightImg = {
        type: 'element',
        tagName: 'img',
        properties: {
          ...img.properties,
          className: ['mermaid-light'],
          loading: 'lazy',
          decoding: 'async',
        },
        children: [],
      };

      const darkImg = {
        type: 'element',
        tagName: 'img',
        properties: {
          alt: img.properties?.alt || '',
          src: source.properties?.srcset,
          width: source.properties?.width,
          height: source.properties?.height,
          className: ['mermaid-dark'],
          loading: 'lazy',
          decoding: 'async',
        },
        children: [],
      };

      const wrapper = {
        type: 'element',
        tagName: 'div',
        properties: { className: ['mermaid-themed'] },
        children: [lightImg, darkImg],
      };

      parent.children[index] = wrapper;
    });
  };
}

/** Wrap <table> and mermaid diagram containers in a scrollable div */
function rehypeScrollWrap() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index == null) return;
      const isMermaid =
        node.tagName === 'div' &&
        node.properties?.className?.includes?.('mermaid-themed');
      const isTable = node.tagName === 'table';
      if (!isMermaid && !isTable) return;
      const wrapper = {
        type: 'element',
        tagName: 'div',
        properties: { className: ['scroll-wrap'] },
        children: [node],
      };
      parent.children[index] = wrapper;
    });
  };
}

export default defineConfig({
  site: 'https://williamzujkowski.github.io',
  prefetch: true,
  integrations: [svelte(), sitemap()],
  vite: {
    build: {
      rollupOptions: {
        external: ['/pagefind/pagefind.js'],
      },
    },
  },
  markdown: {
    syntaxHighlight: {
      type: 'shiki',
      excludeLangs: ['mermaid'],
    },
    shikiConfig: {
      themes: {
        light: 'github-light',
        dark: 'github-dark',
      },
      transformers: [transformerCodeTitle()],
    },
    remarkPlugins: [
      [remarkSmartypants, { dashes: 'oldschool' }],
    ],
    rehypePlugins: [
      [rehypeMermaid, {
        strategy: 'img-svg',
        mermaidConfig: { theme: 'default' },
        dark: { theme: 'dark' },
      }],
      rehypeMermaidDualTheme,
      rehypeScrollWrap,
    ],
  },
});
