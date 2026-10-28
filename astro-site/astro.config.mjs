import { defineConfig, fontProviders } from 'astro/config';
import { unified } from '@astrojs/markdown-remark';
import svelte from '@astrojs/svelte';
import sitemap from '@astrojs/sitemap';
import rehypeRaw from 'rehype-raw';
import rehypeSanitize, { defaultSchema } from 'rehype-sanitize';
import remarkSmartypants from 'remark-smartypants';
import { visit } from 'unist-util-visit';
import { createCssVariablesTheme } from 'shiki';
import { writeFile } from 'node:fs/promises';
import rehypeSidenotes from './src/lib/rehype-sidenotes.mjs';
import rehypeSourceMarginalia from './src/lib/rehype-source-marginalia.mjs';
import rehypeTaskListLabels from './src/lib/rehype-task-list-labels.mjs';
import rehypeDropCap from './src/lib/rehype-drop-cap.mjs';
import rehypeExternalRel from './src/lib/rehype-external-rel.mjs';
import rehypeSmartQuotes from './src/lib/rehype-smart-quotes.mjs';
import { tagRedirects } from './src/lib/tag-taxonomy.mjs';

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

// Must match the UNICODES in scripts/subset-fonts.sh; ranges outside it fall back as before.
const LATIN_TRIMMED = ['U+0020-007E', 'U+00A0-00FF', 'U+0131', 'U+0152-0153', 'U+2010-2027', 'U+2030-203A', 'U+2122', 'U+2190-2193', 'U+2212', 'U+20AC'];
const GREEK = ['U+0370-0377', 'U+037A-037F', 'U+0384-038A', 'U+038C', 'U+038E-03A1', 'U+03A3-03FF'];

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
 * and set it as data-title on the <pre>, which remarque-tokens/code-title
 * draws as the block's filename line.
 *
 * Usage in markdown: ```python title="main.py"
 * Renders: <pre data-title="main.py">...</pre>
 */
function transformerCodeTitle() {
  return {
    name: 'code-title',
    pre(node) {
      const meta = this.options.meta?.__raw;
      if (!meta) return;
      const match = meta.match(/title="([^"]+)"/);
      if (!match) return;
      // remarque-tokens/code-title renders data-title via ::before. The
      // serializer escapes the attribute, so the raw text goes in here;
      // escaping it too printed a literal "&amp;" in the filename line.
      node.properties['data-title'] = match[1];
    },
  };
}

/** Plain text of a hast node, for building accessible names. */
function hastText(node) {
  if (node.type === 'text') return node.value;
  return (node.children || []).map(hastText).join('');
}

/**
 * Wrap <table> elements in remarque's scroll region (.remarque-table-wrap,
 * plus the site's own .scroll-wrap, which carries the layout and the edge
 * cue): role="region", an accessible name and tabindex="0", so a table wider
 * than the column can be scrolled from the keyboard.
 *
 * The name is the table's <caption>, else the heading it sits under. A GFM
 * table has neither caption nor columns a reader would call a name, so the
 * nearest preceding heading is what tells a screen-reader user which table
 * this is; with no heading either it falls back to the header row. A name
 * already given to an earlier table gets its number appended, which keeps
 * axe's landmark-unique rule satisfied.
 */
function rehypeScrollWrap() {
  return (tree) => {
    let tableNumber = 0;
    let heading = '';
    const used = new Set();
    visit(tree, 'element', (node, index, parent) => {
      if (/^h[1-6]$/.test(node.tagName)) {
        heading = hastText(node).replace(/\s+/g, ' ').trim();
        return;
      }
      if (!parent || index == null) return;
      if (node.tagName !== 'table') return;
      tableNumber += 1;
      const caption = node.children.find((child) => child.tagName === 'caption');
      const captionText = caption ? hastText(caption).replace(/\s+/g, ' ').trim() : '';
      const headerRow = [];
      const thead = node.children.find((child) => child.tagName === 'thead') ?? node;
      visit(thead, 'element', (cell) => {
        if (cell.tagName === 'th') headerRow.push(hastText(cell).trim());
      });
      const columns = headerRow.filter(Boolean).join(', ');
      let ariaLabel = captionText || (heading ? `Table: ${heading}` : columns ? `Table ${tableNumber}: ${columns}` : `Table ${tableNumber}`);
      if (used.has(ariaLabel)) ariaLabel = `${ariaLabel} (table ${tableNumber})`;
      used.add(ariaLabel);
      const wrapper = {
        type: 'element',
        tagName: 'div',
        properties: { className: ['remarque-table-wrap', 'scroll-wrap'], tabIndex: 0, role: 'region', ariaLabel },
        children: [node],
      };
      parent.children[index] = wrapper;
    });
  };
}

export default defineConfig({
  site: 'https://williamzujkowski.github.io',
  // `true`, not Astro 7's default 'jsx'. 'jsx' applies React's whitespace
  // rules on purpose (withastro/astro#17310), so a line break between text and
  // an inline element on the next source line is deleted: `via\n<a>` rendered
  // as "via<a>" in the footer of every page and in 16 places on About/Now/Uses.
  // `true` is the lossless HTML compressor: it keeps that break, and on this
  // site changed no visible text. Gzipped HTML: false 2.91 MB, true 2.86 MB,
  // 'jsx' 2.84 MB (Astro 7.4). tests/e2e/reflow.spec.ts fails if any word is
  // glued to a link again.
  compressHTML: true,
  // Retired tag pages (issue #698). Static output writes each as a
  // meta-refresh page with rel=canonical; tagRedirects() throws on a chain
  // or self-map, which fails the build.
  redirects: tagRedirects(),
  prefetch: true,
  integrations: [
    svelte(),
    {
      name: 'publication-cutoff-manifest',
      hooks: {
        'astro:build:done': async ({ logger, dir }) => {
          const cutoff = process.env.PUBLICATION_AS_OF ?? new Date().toISOString();
          await writeFile(new URL('publication-cutoff.json', dir), `${JSON.stringify({ cutoff })}\n`);
          logger.info(`publication cutoff recorded: ${cutoff}`);
        },
      },
    },
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
      // Display face. Trimmed local files (issue #661): same Fraunces, minus
      // the SOFT/WONK axes (pinned to the font's defaults) and unused glyphs.
      // Regenerate: scripts/subset-fonts.sh (see src/fonts/README.md).
      provider: fontProviders.local(),
      name: 'Fraunces',
      cssVariable: '--font-display',
      fallbacks: ['Georgia', 'Times New Roman', 'serif'],
      options: {
        variants: [
          { weight: '100 900', style: 'normal', src: ['./src/fonts/fraunces-normal.woff2'], unicodeRange: LATIN_TRIMMED },
          { weight: '100 900', style: 'italic', src: ['./src/fonts/fraunces-italic.woff2'], unicodeRange: LATIN_TRIMMED },
        ],
      },
    },
    {
      // Body serif — Phosphor broadsheet (issue #274, 7-0 vote). Replaces
      // Inter outright (font-count budget; not stacked). Local files (issue
      // #661): wght trimmed, glyphs trimmed to LATIN_TRIMMED; opsz kept.
      // Greek is REQUIRED (not optional): 5 posts use bare Greek letters in
      // prose (π, ε, μ for math/privacy-budget notation) that the latin
      // face would silently drop to tofu/fallback glyphs. Greek MUST share the
      // latin weight ranges (Chrome groups faces by weight range; see the script).
      provider: fontProviders.local(),
      name: 'Source Serif 4',
      cssVariable: '--font-body',
      fallbacks: ['Georgia', 'serif'],
      options: {
        variants: [
          { weight: '400 900', style: 'normal', src: ['./src/fonts/source-serif-4-normal.woff2'], unicodeRange: LATIN_TRIMMED },
          { weight: '400 700', style: 'italic', src: ['./src/fonts/source-serif-4-italic.woff2'], unicodeRange: LATIN_TRIMMED },
          { weight: '400 900', style: 'normal', src: ['./src/fonts/source-serif-4-greek-normal.woff2'], unicodeRange: GREEK },
          { weight: '400 700', style: 'italic', src: ['./src/fonts/source-serif-4-greek-italic.woff2'], unicodeRange: GREEK },
        ],
      },
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
      // Never body copy, never nav/meta. Local static wght-400 instance
      // (issue #661): Fontsource ships the whole variable axis (170 KB).
      provider: fontProviders.local(),
      name: 'Shantell Sans',
      cssVariable: '--font-accent',
      fallbacks: ['Comic Sans MS', 'cursive'],
      options: {
        variants: [
          { weight: 400, style: 'normal', src: ['./src/fonts/shantell-sans-400.woff2'], unicodeRange: LATIN_TRIMMED },
        ],
      },
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
    processor: unified({
      remarkPlugins: [
        [remarkSmartypants, { dashes: 'oldschool' }],
      ],
      rehypePlugins: [
        rehypeScrollWrap,
        // Convert GFM footnote references and definitions into inline sidenotes.
        rehypeSidenotes,
        // Opt-in per post (`marginNotes: true`): Sources entries as margin notes.
        rehypeSourceMarginalia,
        rehypeRaw,
        // Raw-HTML captions and diagram labels that smartypants never saw.
        rehypeSmartQuotes,
        rehypeTaskListLabels,
        [rehypeSanitize, sanitizeSchema],
        // Lowercase lead paragraphs skip the drop cap (global.css).
        rehypeDropCap,
        // rel="external" on off-site links, for .remarque-prose--external-marks.
        rehypeExternalRel,
      ],
    }),
  },
});
