import { defineConfig, fontProviders } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import rehypeMermaid from 'rehype-mermaid';
import remarkSmartypants from 'remark-smartypants';
import { visit } from 'unist-util-visit';
import { createCssVariablesTheme } from 'shiki';
import rehypeSidenotes from './src/lib/rehype-sidenotes.mjs';

/**
 * Remarque syntax-highlighting theme (remarque-tokens 0.15.0, REMARQUE.md
 * "Syntax Highlighting" / "Astro / Shiki wiring"). Passed as an OBJECT, not
 * the `'css-variables'` string — Astro's markdown pipeline renames the
 * string form's variable prefix to `--astro-code-*`, which would silently
 * break the mapping to this package's `--color-syntax-*` tokens. Because
 * this is a single CSS-variables theme (not a light/dark pair), the actual
 * light vs. dark color swap happens in global.css's palette blocks (the
 * `--color-syntax-*` custom properties themselves are themed there) plus
 * the `.astro-code` CSS bridge below — not here.
 */
const remarqueSyntaxTheme = createCssVariablesTheme({
  name: 'remarque',
  variablePrefix: '--color-syntax-',
  fontStyle: true,
});

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
 * Mermaid diagrams -> theme-adaptive inline SVG (issue #283 item 3).
 *
 * rehype-mermaid renders with a SINGLE mermaid theme ('base') whose
 * `themeVariables` are pinned to a small set of distinctive, arbitrary
 * "placeholder" hex colors (never anything a diagram would emit by
 * chance — verified against actual rendered output for every diagram
 * type used in src/posts/**, see MERMAID_COLOR_MAP below). Because the
 * render strategy is 'inline-svg', those placeholder hexes land
 * directly in the page's HTML (inside the diagram's own <style> block
 * AND on individual element attributes — rough.js/handDrawn hatch-fill
 * paths bake a literal color attribute, they can't use CSS classes).
 *
 * rehypeMermaidThemeVars() then walks the whole hast tree and does an
 * exact string replacement of every placeholder hex back to the
 * matching site design token (`var(--color-*)`, defined in
 * src/styles/global.css and re-themed per-deck in
 * src/styles/theme-deck.css). The result is ONE inline SVG per diagram
 * that repaints correctly under light, dark, and all 12 theme-deck
 * palettes with no per-theme regeneration — replacing the old
 * <picture>-based light/dark <img> pair (rehypeMermaidDualTheme),
 * which baked exactly two color variants and did not see the deck
 * themes at all.
 *
 * A handful of colors are NOT sourced from mermaid `themeVariables` —
 * they're hardcoded directly into mermaid's own generated CSS/SVG,
 * independent of theme (e.g. `.node .katex path{fill:#000}` for LaTeX
 * notation, a dead `[data-look="neo"]` rule that never matches under
 * `look:'handDrawn'`, and `.section-N line{stroke:#ffffff}` in
 * timeline diagrams). MERMAID_LITERAL_MAP below patches the small,
 * confirmed set of these (#000, #000000, #ffffff) as a defense-in-depth
 * safety net — most *other* literal fallback attributes mermaid emits
 * (e.g. sequence-diagram actor rects carry both a literal
 * `fill="#eaeaea"` AND a `class="actor"` that a themed CSS rule
 * targets) are already overridden by the themed class rule per normal
 * CSS cascade (presentation attributes are lowest-priority), so they
 * don't need patching.
 */

/** mermaid themeVariable name -> [placeholder hex mermaid will emit, site CSS token] */
const MERMAID_COLOR_MAP = {
  // Core / shared across diagram types
  primaryColor: ['#1a2b01', 'var(--color-accent)'],
  primaryTextColor: ['#1a2b02', 'var(--color-fg)'],
  primaryBorderColor: ['#1a2b03', 'var(--color-border-bold)'],
  secondaryColor: ['#1a2b04', 'var(--color-bg-subtle)'],
  secondaryTextColor: ['#1a2b05', 'var(--color-fg)'],
  secondaryBorderColor: ['#1a2b06', 'var(--color-border-bold)'],
  tertiaryColor: ['#1a2b07', 'var(--color-bg-subtle)'],
  tertiaryTextColor: ['#1a2b08', 'var(--color-fg-muted)'],
  tertiaryBorderColor: ['#1a2b09', 'var(--color-border-bold)'],
  lineColor: ['#1a2b10', 'var(--color-fg-muted)'],
  textColor: ['#1a2b11', 'var(--color-fg)'],
  mainBkg: ['#1a2b12', 'var(--color-surface)'], // flowchart node fill
  background: ['#1a2b13', 'var(--color-bg)'],
  edgeLabelBackground: ['#1a2b14', 'var(--color-bg-subtle)'],
  titleColor: ['#1a2b15', 'var(--color-fg)'],
  defaultLinkColor: ['#1a2b16', 'var(--color-fg-muted)'],
  arrowheadColor: ['#1a2b17', 'var(--color-fg-muted)'],
  clusterBkg: ['#1a2b18', 'var(--color-bg-subtle)'], // flowchart subgraph fill
  clusterBorder: ['#1a2b19', 'var(--color-border-bold)'],
  errorBkgColor: ['#1a2b20', 'var(--color-error-subtle)'],
  errorTextColor: ['#1a2b21', 'var(--color-error)'],
  nodeBkg: ['#1a2b22', 'var(--color-surface)'],
  nodeBorder: ['#1a2b23', 'var(--color-border-bold)'],
  nodeTextColor: ['#1a2b24', 'var(--color-fg)'],

  // sequenceDiagram
  actorBkg: ['#2b3c01', 'var(--color-surface)'],
  actorBorder: ['#2b3c02', 'var(--color-border-bold)'],
  actorTextColor: ['#2b3c03', 'var(--color-fg)'],
  actorLineColor: ['#2b3c04', 'var(--color-border-bold)'], // lifeline
  signalColor: ['#2b3c05', 'var(--color-fg-muted)'], // message arrows
  signalTextColor: ['#2b3c06', 'var(--color-fg)'],
  labelBoxBkgColor: ['#2b3c07', 'var(--color-bg-subtle)'], // alt/opt/loop tag
  labelBoxBorderColor: ['#2b3c08', 'var(--color-border-bold)'],
  labelTextColor: ['#2b3c09', 'var(--color-fg)'],
  loopTextColor: ['#2b3c10', 'var(--color-fg)'],
  activationBkgColor: ['#2b3c11', 'var(--color-bg-subtle)'],
  activationBorderColor: ['#2b3c12', 'var(--color-border-bold)'],
  sequenceNumberColor: ['#2b3c13', 'var(--color-bg)'],
  noteBkgColor: ['#2b3c14', 'var(--color-bg-subtle)'],
  noteBorderColor: ['#2b3c15', 'var(--color-border-bold)'],
  noteTextColor: ['#2b3c16', 'var(--color-fg)'],

  // pie
  pie1: ['#3c4d01', 'var(--color-viz-1)'],
  pie2: ['#3c4d02', 'var(--color-viz-2)'],
  pie3: ['#3c4d03', 'var(--color-viz-3)'],
  pie4: ['#3c4d04', 'var(--color-viz-4)'],
  pie5: ['#3c4d05', 'var(--color-viz-5)'],
  pie6: ['#3c4d06', 'var(--color-viz-6)'],
  pie7: ['#3c4d07', 'var(--color-viz-1)'], // cycle the 6-color viz palette
  pie8: ['#3c4d08', 'var(--color-viz-2)'],
  pie9: ['#3c4d09', 'var(--color-viz-3)'],
  pie10: ['#3c4d10', 'var(--color-viz-4)'],
  pie11: ['#3c4d11', 'var(--color-viz-5)'],
  pie12: ['#3c4d12', 'var(--color-viz-6)'],
  pieOuterStrokeColor: ['#3c4d13', 'var(--color-border-bold)'],
  pieStrokeColor: ['#3c4d14', 'var(--color-bg)'], // slice separators
  pieTitleTextColor: ['#3c4d15', 'var(--color-fg)'],
  // Drawn INSIDE each slice, on top of the viz-N fill — fg-on-viz measures
  // as low as 2.0:1 in the dark palette (both are mid/light tones there).
  // bg-on-viz clears 4.4:1+ in both palettes (same reasoning as the
  // timeline cScaleLabel* tokens below).
  pieSectionTextColor: ['#3c4d16', 'var(--color-bg)'],
  pieLegendTextColor: ['#3c4d17', 'var(--color-fg)'],

  // gantt
  sectionBkgColor: ['#4d5e01', 'var(--color-bg-subtle)'],
  altSectionBkgColor: ['#4d5e02', 'var(--color-surface)'],
  sectionBkgColor2: ['#4d5e03', 'var(--color-bg-subtle)'],
  taskBkgColor: ['#4d5e04', 'var(--color-surface)'],
  taskTextColor: ['#4d5e05', 'var(--color-fg)'],
  taskTextOutsideColor: ['#4d5e06', 'var(--color-fg)'],
  taskTextClickableColor: ['#4d5e07', 'var(--color-accent)'],
  taskBorderColor: ['#4d5e08', 'var(--color-border-bold)'],
  // NOTE: fill stays neutral (not accent) because `taskTextColor` (fg) is
  // drawn directly on top — fg-on-accent measures only 1.32:1 in the dark
  // palette (both tokens are near-white there). The accent highlight
  // lives in the border instead, where it never has to host body text.
  activeTaskBkgColor: ['#4d5e09', 'var(--color-bg-subtle)'],
  activeTaskBorderColor: ['#4d5e10', 'var(--color-accent)'],
  doneTaskBkgColor: ['#4d5e11', 'var(--color-bg-subtle)'],
  doneTaskBorderColor: ['#4d5e12', 'var(--color-border-bold)'],
  critBkgColor: ['#4d5e13', 'var(--color-error-subtle)'],
  critBorderColor: ['#4d5e14', 'var(--color-error)'],
  todayLineColor: ['#4d5e15', 'var(--color-accent)'],
  gridColor: ['#4d5e16', 'var(--color-border)'],
  excludeBkgColor: ['#4d5e17', 'var(--color-bg-subtle)'],

  // timeline
  cScale0: ['#5e6f01', 'var(--color-viz-1)'],
  cScale1: ['#5e6f02', 'var(--color-viz-2)'],
  cScale2: ['#5e6f03', 'var(--color-viz-3)'],
  cScale3: ['#5e6f04', 'var(--color-viz-4)'],
  cScale4: ['#5e6f05', 'var(--color-viz-5)'],
  cScale5: ['#5e6f06', 'var(--color-viz-6)'],
  cScale6: ['#5e6f07', 'var(--color-viz-1)'],
  cScale7: ['#5e6f08', 'var(--color-viz-2)'],
  cScale8: ['#5e6f09', 'var(--color-viz-3)'],
  cScale9: ['#5e6f10', 'var(--color-viz-4)'],
  cScale10: ['#5e6f11', 'var(--color-viz-5)'],
  cScale11: ['#5e6f12', 'var(--color-viz-6)'],
  cScaleLabel0: ['#5e6f13', 'var(--color-bg)'], // text drawn atop a cScale swatch
  cScaleLabel1: ['#5e6f14', 'var(--color-bg)'],
  cScaleLabel2: ['#5e6f15', 'var(--color-bg)'],
  cScaleLabel3: ['#5e6f16', 'var(--color-bg)'],

  // quadrantChart
  quadrant1Fill: ['#6f7001', 'var(--color-bg-subtle)'],
  quadrant2Fill: ['#6f7002', 'var(--color-surface)'],
  quadrant3Fill: ['#6f7003', 'var(--color-bg-subtle)'],
  quadrant4Fill: ['#6f7004', 'var(--color-surface)'],
  quadrant1TextFill: ['#6f7005', 'var(--color-fg)'],
  quadrant2TextFill: ['#6f7006', 'var(--color-fg)'],
  quadrant3TextFill: ['#6f7007', 'var(--color-fg)'],
  quadrant4TextFill: ['#6f7008', 'var(--color-fg)'],
  quadrantPointFill: ['#6f7009', 'var(--color-accent)'], // plotted data points
  quadrantPointTextFill: ['#6f7010', 'var(--color-fg)'],
  quadrantXAxisTextFill: ['#6f7011', 'var(--color-fg-muted)'],
  quadrantYAxisTextFill: ['#6f7012', 'var(--color-fg-muted)'],
  quadrantInternalBorderStrokeFill: ['#6f7013', 'var(--color-border)'],
  quadrantExternalBorderStrokeFill: ['#6f7014', 'var(--color-border-bold)'],
  quadrantTitleFill: ['#6f7015', 'var(--color-fg)'],
};

/** Colors mermaid hardcodes outside of `themeVariables` — see block comment above. */
const MERMAID_LITERAL_MAP = {
  '#000000': 'var(--color-fg)',
  '#000': 'var(--color-fg)',
  '#ffffff': 'var(--color-bg)',
};

const mermaidThemeVariables = Object.fromEntries(
  Object.entries(MERMAID_COLOR_MAP).map(([k, [hex]]) => [k, hex])
);

/** Compiled once: [RegExp matching one placeholder hex (hex-boundary safe), replacement var()] */
const MERMAID_REPLACEMENTS = [
  ...Object.values(MERMAID_COLOR_MAP),
  ...Object.entries(MERMAID_LITERAL_MAP).map(([hex, token]) => [hex, token]),
].map(([hex, token]) => [
  new RegExp(`(?<![0-9a-fA-F])${hex}(?![0-9a-fA-F])`, 'gi'),
  token,
]);

function replaceMermaidColors(value) {
  let out = value;
  for (const [re, token] of MERMAID_REPLACEMENTS) out = out.replace(re, token);
  return out;
}

function rehypeMermaidThemeVars() {
  return (tree) => {
    visit(tree, (node) => {
      if (node.type === 'text' && typeof node.value === 'string') {
        node.value = replaceMermaidColors(node.value);
        return;
      }
      if (node.type !== 'element' || !node.properties) return;
      for (const [key, val] of Object.entries(node.properties)) {
        if (typeof val === 'string') {
          node.properties[key] = replaceMermaidColors(val);
        } else if (Array.isArray(val)) {
          node.properties[key] = val.map((v) =>
            typeof v === 'string' ? replaceMermaidColors(v) : v
          );
        }
      }
    });
  };
}

/** Wrap <table> and mermaid diagram containers in a scrollable div */
function rehypeScrollWrap() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index == null) return;
      // rehype-mermaid (strategy: 'inline-svg') emits a bare <svg id="mermaid-N" ...>
      // at the top level of each diagram — no wrapper div to key off of.
      const isMermaid =
        node.tagName === 'svg' &&
        typeof node.properties?.id === 'string' &&
        node.properties.id.startsWith('mermaid-');
      const isTable = node.tagName === 'table';
      if (!isMermaid && !isTable) return;
      const wrapper = {
        type: 'element',
        tagName: 'div',
        // tabIndex makes the scrollable region itself keyboard-focusable
        // (WCAG 2.1.1 / axe "scrollable-region-focusable") — pre-existing
        // gap, not introduced by sidenotes: no page in the a11y suite had
        // content wide enough to actually overflow `.scroll-wrap` until
        // the sidenotes pilot post's comparison table did. Fixed here
        // since it's a one-line addition to the same wrapper.
        properties: { className: ['scroll-wrap'], tabIndex: 0 },
        children: [node],
      };
      parent.children[index] = wrapper;
    });
  };
}

export default defineConfig({
  site: 'https://williamzujkowski.github.io',
  prefetch: true,
  integrations: [
    svelte(),
    // Keep hidden easter-egg pages (e.g. /pizza-ops/) out of the sitemap.
    // They're also noindex'd in BaseLayout; this just stops them being
    // advertised. Reachable only via the posts that link them.
    sitemap({ filter: (page) => !page.includes('/pizza-ops') }),
  ],
  // Astro 6 Fonts API — self-hosts fonts at build time via the Fontsource
  // provider (same font files previously shipped by the @fontsource-variable
  // packages, now fetched and optimized by Astro directly). `cssVariable`
  // intentionally matches the pre-existing design-token names in
  // src/styles/global.css (--font-display / --font-body / --font-mono) so
  // no downstream CSS had to change — Astro injects `:root { --font-x: ... }`
  // itself, so the hardcoded font stacks were removed from global.css.
  fonts: [
    {
      provider: fontProviders.fontsource(),
      name: 'Fraunces',
      cssVariable: '--font-display',
      fallbacks: ['Georgia', 'Times New Roman', 'serif'],
      weights: ['100 900'],
      styles: ['normal', 'italic'],
      subsets: ['latin'],
    },
    {
      // Body serif — Phosphor broadsheet (issue #274, 7-0 vote). Replaces
      // Inter outright (font-count budget; not stacked). Source Serif 4 is
      // the characterful text serif chosen to close the one genericness
      // flag from the frontend-design calibration (Inter-as-body).
      provider: fontProviders.fontsource(),
      name: 'Source Serif 4',
      cssVariable: '--font-body',
      fallbacks: ['Georgia', 'serif'],
      weights: ['200 900'],
      styles: ['normal', 'italic'],
      // 'greek' REQUIRED (not optional): 5 posts use bare Greek letters in
      // prose (π, ε, μ for math/privacy-budget notation) that the default
      // subset would silently drop to tofu/fallback glyphs.
      subsets: ['latin', 'greek'],
    },
    {
      provider: fontProviders.fontsource(),
      name: 'IBM Plex Mono',
      cssVariable: '--font-mono',
      fallbacks: ['ui-monospace', 'Courier New', 'monospace'],
      weights: [400, 500],
      styles: ['normal', 'italic'],
      subsets: ['latin'],
    },
    {
      // Zine accent voice — hand-lettered marginalia ONLY. Approved usage
      // (design-review ratified): .hand-note, 404 page, doodle captions.
      // Never body copy, never nav/meta.
      provider: fontProviders.fontsource(),
      name: 'Shantell Sans',
      cssVariable: '--font-accent',
      fallbacks: ['Comic Sans MS', 'cursive'],
      weights: ['400 500'],
      styles: ['normal'],
      subsets: ['latin'],
    },
  ],
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
      theme: remarqueSyntaxTheme,
      transformers: [transformerCodeTitle()],
    },
    remarkPlugins: [
      [remarkSmartypants, { dashes: 'oldschool' }],
    ],
    rehypePlugins: [
      [rehypeMermaid, {
        // Inline SVG (not img-svg/<picture>) so the diagram's own colors
        // live in the page DOM and can be repainted via CSS custom
        // properties — see rehypeMermaidThemeVars above (issue #283 item 3).
        // `dark` is intentionally gone: it's unsupported by inline-svg
        // anyway, and unnecessary now that ONE render adapts to every theme.
        strategy: 'inline-svg',
        // handDrawn (rough.js) look for the zine aesthetic; fixed seed keeps
        // builds reproducible. theme:'base' + themeVariables (above) pins
        // mermaid's palette to known placeholder hexes that
        // rehypeMermaidThemeVars rewrites to var(--color-*) tokens.
        mermaidConfig: {
          theme: 'base',
          look: 'handDrawn',
          handDrawnSeed: 42,
          themeVariables: mermaidThemeVariables,
        },
      }],
      rehypeMermaidThemeVars,
      rehypeScrollWrap,
      // Tufte/gwern-style sidenotes (issue #272) — must run after remark's
      // GFM footnote transform (implicit: this is a rehype plugin, so it
      // only ever sees the hast tree remark-rehype already produced).
      // Order relative to the mermaid/table plugins above doesn't matter —
      // disjoint node types (footnote refs/definitions vs. inline <svg>/
      // <table>) — kept last for now as the newest addition.
      rehypeSidenotes,
    ],
  },
});
