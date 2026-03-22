import { defineConfig } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import rehypeMermaid from 'rehype-mermaid';
import { visit } from 'unist-util-visit';

/** Wrap <table> and mermaid <svg> in a scrollable div */
function rehypeScrollWrap() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index == null) return;
      const isMermaidSvg =
        node.tagName === 'svg' &&
        node.properties?.id?.toString().startsWith('mermaid');
      const isTable = node.tagName === 'table';
      if (!isMermaidSvg && !isTable) return;
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
    },
    rehypePlugins: [
      [rehypeMermaid, {
        strategy: 'inline-svg',
        mermaidConfig: { theme: 'default' },
      }],
      rehypeScrollWrap,
    ],
  },
});
