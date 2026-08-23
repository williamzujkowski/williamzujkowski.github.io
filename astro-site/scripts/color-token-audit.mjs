#!/usr/bin/env node
/**
 * Remarque color-token audit.
 * Flags hardcoded hex / rgb() / hsl() / oklch() / named colors in CSS-ish
 * contexts. All colors MUST come from --color-* tokens.
 *
 * Allowed escape hatches:
 *   - `transparent`, `currentColor`, `inherit`, `unset`, `initial`, `none`
 *   - Inside a comment
 *   - Explicit allowlist comment: allow-raw-color
 *
 * Four blind spots were found by a negative-control audit (issue #511) and
 * are fixed here. Each had a live instance in the tree:
 *
 *   1. `var(--color-x, #hex)` — the old early-return skipped the whole
 *      declaration the moment it saw `var(--color-`, so a hardcoded fallback
 *      was invisible. Three shipped in PizzaOps.svelte.
 *   2. `.ts` was not scanned, so the six constants colouring every social
 *      card in src/og/card.ts were structurally unauditable. (The typography
 *      audit *did* scan .ts — the two disagreed about what "source" means.)
 *   3. A line starting with `*` was treated as a comment continuation, so a
 *      universal-selector rule (`* { color: red }`) was skipped. Comments are
 *      now stripped properly, preserving line numbers, instead of guessed at
 *      per line.
 *   4. The header claimed "named colors" were flagged; nothing implemented
 *      it. Now implemented.
 *
 * And: an empty walk used to print "All color values use var(--color-*)
 * tokens" and exit 0. Scanning zero files is now a failure, not a pass.
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '../src');

const exts = new Set(['.css', '.astro', '.svelte', '.ts']);
const violations = [];
let filesScanned = 0;

// Properties where hardcoded colors are forbidden
const COLOR_PROPS =
  /\b(color|background(-color)?|border(-[\w-]+)?-color|border(-[\w-]+)?|fill|stroke|outline(-color)?|text-decoration-color|caret-color|box-shadow|text-shadow|accent-color)\s*:/;

const HEX = /#[0-9a-fA-F]{3,8}\b/;
// color-mix() is deliberately absent: it COMPOSES colors, and its arguments
// are checked on their own merits. `color-mix(in oklch, var(--color-accent)
// 60%, transparent)` is correct usage, not a hardcoded color.
const FUNC_COLOR = /\b(rgb|rgba|hsl|hsla|oklch|lab|lch)\s*\(/;

const ALLOWED = new Set([
  'transparent', 'currentColor', 'currentcolor', 'inherit', 'unset', 'initial', 'none',
]);

// CSS named colors. `transparent`/`currentColor` are handled by ALLOWED above.
const NAMED_COLORS = new Set([
  'aliceblue','antiquewhite','aqua','aquamarine','azure','beige','bisque','black',
  'blanchedalmond','blue','blueviolet','brown','burlywood','cadetblue','chartreuse',
  'chocolate','coral','cornflowerblue','cornsilk','crimson','cyan','darkblue','darkcyan',
  'darkgoldenrod','darkgray','darkgreen','darkgrey','darkkhaki','darkmagenta',
  'darkolivegreen','darkorange','darkorchid','darkred','darksalmon','darkseagreen',
  'darkslateblue','darkslategray','darkslategrey','darkturquoise','darkviolet','deeppink',
  'deepskyblue','dimgray','dimgrey','dodgerblue','firebrick','floralwhite','forestgreen',
  'fuchsia','gainsboro','ghostwhite','gold','goldenrod','gray','green','greenyellow','grey',
  'honeydew','hotpink','indianred','indigo','ivory','khaki','lavender','lavenderblush',
  'lawngreen','lemonchiffon','lightblue','lightcoral','lightcyan','lightgoldenrodyellow',
  'lightgray','lightgreen','lightgrey','lightpink','lightsalmon','lightseagreen',
  'lightskyblue','lightslategray','lightslategrey','lightsteelblue','lightyellow','lime',
  'limegreen','linen','magenta','maroon','mediumaquamarine','mediumblue','mediumorchid',
  'mediumpurple','mediumseagreen','mediumslateblue','mediumspringgreen','mediumturquoise',
  'mediumvioletred','midnightblue','mintcream','mistyrose','moccasin','navajowhite','navy',
  'oldlace','olive','olivedrab','orange','orangered','orchid','palegoldenrod','palegreen',
  'paleturquoise','palevioletred','papayawhip','peachpuff','peru','pink','plum','powderblue',
  'purple','rebeccapurple','red','rosybrown','royalblue','saddlebrown','salmon','sandybrown',
  'seagreen','seashell','sienna','silver','skyblue','slateblue','slategray','slategrey','snow',
  'springgreen','steelblue','tan','teal','thistle','tomato','turquoise','violet','wheat',
  'white','whitesmoke','yellow','yellowgreen',
]);

/**
 * Blank out /* *​/ and // comments while preserving line count and columns, so
 * reported line numbers stay accurate. Replaces guessing per line, which
 * mistook `* { … }` rule lines for comment continuations.
 */
function stripComments(src) {
  let out = src.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
  out = out.replace(/(^|[^:])\/\/[^\n]*/g, (m, p1) => p1 + ' '.repeat(m.length - p1.length));
  return out;
}

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    if (entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full);
    else if (exts.has(extname(full))) scan(full);
  }
}

// A hex string literal assigned in JS/TS is a colour definition even though
// it is not a CSS declaration — src/og/card.ts holds the palette for every
// social card the site emits. satori has no CSS cascade, so var() cannot
// resolve there and literals are structurally required; the point of scanning
// them is that the exemption must be WRITTEN DOWN, not implicit.
const TS_HEX_LITERAL = /=\s*['"`]#[0-9a-fA-F]{3,8}['"`]/;

function scan(file) {
  filesScanned += 1;
  const raw = readFileSync(file, 'utf8');
  const lines = stripComments(raw).split('\n');
  const rawLines = raw.split('\n');
  const isTs = extname(file) === '.ts';

  lines.forEach((line, i) => {
    if (isTs && TS_HEX_LITERAL.test(line)) {
      if (!/allow-raw-color/.test(rawLines[i] ?? '')) {
        violations.push({
          file: file.replace(root + '/', ''),
          line: i + 1,
          offense: line.match(/#[0-9a-fA-F]{3,8}/)[0],
          snippet: (rawLines[i] ?? '').trim(),
        });
      }
      return;
    }
    // Lines that DEFINE a --color-* token may hold raw values.
    if (/^\s*--color-[\w-]+\s*:/.test(line)) return;
    // Explicit, reviewed escape hatch (checked against the ORIGINAL line so a
    // marker inside a trailing comment still counts).
    if (/allow-raw-color/.test(rawLines[i] ?? '')) return;
    if (!COLOR_PROPS.test(line)) return;

    const value = line.slice(line.indexOf(':') + 1);

    // Strip only the TOKEN NAME out of any var() reference, leaving the
    // fallback behind. `var(--color-error, #c0392b)` -> `var( #c0392b)`.
    const bare = value.replace(/var\(\s*--[\w-]+\s*/g, 'var(');

    const trimmed = bare.trim().replace(/;.*$/, '').trim();
    if (ALLOWED.has(trimmed)) return;

    let offense = null;
    if (HEX.test(bare)) offense = bare.match(HEX)[0];
    else if (FUNC_COLOR.test(bare)) offense = bare.match(FUNC_COLOR)[0] + '…)';
    else {
      // Whole CSS identifiers only. Matching substrings made `white-space:
      // nowrap` look like the colour `white`. Case-sensitive lowercase, so a
      // JS constant like `stroke: BLUE` in a .ts file is not mistaken for the
      // CSS keyword `blue`.
      for (const m of bare.matchAll(/(?<![\w-])([a-z]{3,})(?![\w-])/g)) {
        if (NAMED_COLORS.has(m[1])) { offense = m[1]; break; }
      }
    }

    if (offense) {
      violations.push({
        file: file.replace(root + '/', ''),
        line: i + 1,
        offense,
        snippet: (rawLines[i] ?? '').trim(),
      });
    }
  });
}

if (!existsSync(root)) {
  console.error(`Remarque Color-Token Audit\n\n  Source root not found: ${root}`);
  process.exit(1);
}
walk(root);

console.log('Remarque Color-Token Audit\n');

// An empty walk is not a clean pass — it means the scan never happened.
if (filesScanned === 0) {
  console.error(
    `  Scanned 0 files under ${root}. That is a broken audit, not a clean one.\n`,
  );
  process.exit(1);
}

if (violations.length === 0) {
  console.log(`  All color values use var(--color-*) tokens. (${filesScanned} files scanned)`);
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line} → ${v.offense}`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} hardcoded color(s) found in ${filesScanned} files.`);
process.exit(1);
