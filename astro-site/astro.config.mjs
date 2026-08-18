import { defineConfig, fontProviders } from 'astro/config';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize';
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

const svgTags = [
  'svg',
  'defs',
  'desc',
  'g',
  'marker',
  'path',
  'rect',
  'circle',
  'ellipse',
  'line',
  'polyline',
  'polygon',
  'text',
  'tspan',
  'textPath',
  'title',
  'style',
  'symbol',
  'foreignObject',
  'linearGradient',
  'radialGradient',
  'stop',
  'pattern',
  'clipPath',
  'mask',
  'use',
  'image',
  'switch',
];

const svgAttributes = [
  'accentHeight',
  'alignmentBaseline',
  'ariaHidden',
  'ariaLabel',
  'ariaLabelledBy',
  'ariaRoleDescription',
  'baselineShift',
  'className',
  'clipPath',
  'clipRule',
  'clipPathUnits',
  'colorInterpolation',
  'colorInterpolationFilters',
  'cx',
  'cy',
  'd',
  'direction',
  'display',
  'dominantBaseline',
  'dx',
  'dy',
  'fill',
  'fillOpacity',
  'fillRule',
  'filter',
  'floodColor',
  'floodOpacity',
  'fontFamily',
  'fontSize',
  'fontSizeAdjust',
  'fontStretch',
  'fontStyle',
  'fontVariant',
  'fontWeight',
  'gradientTransform',
  'gradientUnits',
  'height',
  'href',
  'id',
  'imageRendering',
  'letterSpacing',
  'markerEnd',
  'markerHeight',
  'markerMid',
  'markerStart',
  'markerUnits',
  'markerWidth',
  'mask',
  'maskContentUnits',
  'maskUnits',
  'opacity',
  'orient',
  'overflow',
  'paintOrder',
  'pathLength',
  'patternContentUnits',
  'patternTransform',
  'patternUnits',
  'points',
  'preserveAspectRatio',
  'r',
  'refX',
  'refY',
  'role',
  'rx',
  'ry',
  'shapeRendering',
  'src',
  'stopColor',
  'stopOpacity',
  'stroke',
  'strokeDasharray',
  'strokeDashoffset',
  'strokeLinecap',
  'strokeLinejoin',
  'strokeMiterlimit',
  'strokeOpacity',
  'strokeWidth',
  'style',
  'textAnchor',
  'textDecoration',
  'textLength',
  'transform',
  'transformOrigin',
  'vectorEffect',
  'viewBox',
  'width',
  'wordSpacing',
  'x',
  'x1',
  'x2',
  'xlinkActuate',
  'xlinkArcrole',
  'xlinkHref',
  'xlinkRole',
  'xlinkShow',
  'xlinkTitle',
  'xlinkType',
  'xmlLang',
  'xmlSpace',
  'xmlns',
  'xmlnsXLink',
  'xmlnsXlink',
  'y',
  'y1',
  'y2',
];

const contentAttributes = [
  'ariaChecked',
  'ariaDescribedBy',
  'ariaHidden',
  'ariaLabel',
  'ariaLabelledBy',
  'ariaRoleDescription',
  'className',
  'data*',
  'role',
  'style',
];

// Extends the library default rather than replacing it. The default schema does
// NOT permit `role`, and ~90 posts carry role="group" on .flow/.arch diagram
// blocks from the #414 a11y work — swapping to the default would strip that
// silently, with a passing build. See docs/security-posture.md.
const sanitizeSchema = {
  ...defaultSchema,
  tagNames: [...new Set([...(defaultSchema.tagNames || []), 'figure', 'figcaption', 'aside', ...svgTags])],
  attributes: {
    ...defaultSchema.attributes,
    '*': [...(defaultSchema.attributes?.['*'] || []), ...contentAttributes],
    a: ['className', 'data*', ...(defaultSchema.attributes?.a || []), 'ariaHidden', 'rel', 'target'],
    aside: contentAttributes,
    code: ['className', 'data*', 'style', ...(defaultSchema.attributes?.code || [])],
    div: [...contentAttributes, 'tabIndex', ...(defaultSchema.attributes?.div || [])],
    figcaption: contentAttributes,
    figure: contentAttributes,
    h1: [...contentAttributes, ...(defaultSchema.attributes?.h1 || [])],
    h2: [...contentAttributes, ...(defaultSchema.attributes?.h2 || [])],
    h3: [...contentAttributes, ...(defaultSchema.attributes?.h3 || [])],
    h4: [...contentAttributes, ...(defaultSchema.attributes?.h4 || [])],
    h5: [...contentAttributes, ...(defaultSchema.attributes?.h5 || [])],
    h6: [...contentAttributes, ...(defaultSchema.attributes?.h6 || [])],
    img: [...contentAttributes, 'height', 'loading', 'src', 'width', ...(defaultSchema.attributes?.img || [])],
    ol: [...contentAttributes, ...(defaultSchema.attributes?.ol || [])],
    li: [...contentAttributes, ...(defaultSchema.attributes?.li || [])],
    ul: [...contentAttributes, ...(defaultSchema.attributes?.ul || [])],
    p: [...contentAttributes, ...(defaultSchema.attributes?.p || [])],
    pre: [...contentAttributes, 'tabIndex', ...(defaultSchema.attributes?.pre || [])],
    section: [...contentAttributes, ...(defaultSchema.attributes?.section || [])],
    span: [...contentAttributes, ...(defaultSchema.attributes?.span || [])],
    summary: [...contentAttributes, ...(defaultSchema.attributes?.summary || [])],
    svg: [...contentAttributes, ...svgAttributes],
    defs: svgAttributes,
    desc: svgAttributes,
    g: svgAttributes,
    marker: svgAttributes,
    path: svgAttributes,
    rect: svgAttributes,
    circle: svgAttributes,
    ellipse: svgAttributes,
    line: svgAttributes,
    polyline: svgAttributes,
    polygon: svgAttributes,
    text: svgAttributes,
    tspan: svgAttributes,
    textPath: svgAttributes,
    title: svgAttributes,
    style: ['type'],
    symbol: svgAttributes,
    foreignObject: svgAttributes,
    linearGradient: svgAttributes,
    radialGradient: svgAttributes,
    stop: svgAttributes,
    pattern: svgAttributes,
    clipPath: svgAttributes,
    mask: svgAttributes,
    use: svgAttributes,
    image: svgAttributes,
    switch: svgAttributes,
  },
  ancestors: {
    ...(defaultSchema.ancestors || {}),
    style: ['svg'],
  },
  clobber: [],
  protocols: {
    ...defaultSchema.protocols,
    href: [...(defaultSchema.protocols?.href || []), 'tel'],
    xlinkHref: ['http', 'https'],
    src: ['http', 'https'],
  },
};

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

/** Wrap <table> elements in a scrollable div */
function rehypeScrollWrap() {
  return (tree) => {
    visit(tree, 'element', (node, index, parent) => {
      if (!parent || index == null) return;
      const isTable = node.tagName === 'table';
      if (!isTable) return;
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
    },
    shikiConfig: {
      theme: remarqueSyntaxTheme,
      transformers: [transformerCodeTitle()],
    },
    remarkPlugins: [
      [remarkSmartypants, { dashes: 'oldschool' }],
    ],
    rehypePlugins: [
      rehypeScrollWrap,
      // Tufte/gwern-style sidenotes (issue #272) — must run after remark's
      // GFM footnote transform (implicit: this is a rehype plugin, so it
      // only ever sees the hast tree remark-rehype already produced).
      // Order relative to the table wrapper above doesn't matter — disjoint
      // node types (footnote refs/definitions vs. <table>) — kept last for
      // now as the newest addition.
      rehypeSidenotes,
      rehypeRaw,
      [rehypeSanitize, sanitizeSchema],
    ],
  },
});
