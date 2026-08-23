#!/usr/bin/env node
/**
 * Accent-font lint (#283 item 1).
 *
 * `--font-accent` (Shantell Sans) is a hand-lettered marginalia voice,
 * ratified for `.hand-note` only (see astro.config.mjs's font-provider
 * comment: "Zine accent voice — hand-lettered marginalia ONLY... Never
 * body copy, never nav/meta."). This script fails the build if the
 * token shows up anywhere else in src/, so a stray `font-family:
 * var(--font-accent)` on a new component doesn't sneak into body copy.
 *
 * Allowlist:
 *   - src/styles/zine.css   — only inside the `.hand-note` rule block
 *   - src/layouts/BaseLayout.astro — the `<Font cssVariable="--font-accent" />`
 *     loader line. This is the Astro Fonts API companion to the
 *     provider registration in astro.config.mjs: without it the font
 *     never loads, so zine.css's `.hand-note` rule would be dead CSS.
 *   - astro.config.mjs      — the font-provider registration
 *     (`cssVariable: '--font-accent'`). Lives outside src/ so a plain
 *     `src/` walk never sees it; checked explicitly for completeness.
 */
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, '..');
const srcRoot = resolve(siteRoot, 'src');

const TOKEN = /--font-accent\b/;

/**
 * Blank out comments while preserving line numbers. Without this, a comment
 * that merely MENTIONS .hand-note and contains a brace opened the allowlist
 * gate for everything after it (issue #511):
 *
 *     /* .hand-note styling below { *\/
 *     p { font-family: var(--font-accent); }   <- silently allowed
 */
function stripComments(src) {
  let out = src.replace(/\/\*[\s\S]*?\*\//g, (m) => m.replace(/[^\n]/g, ' '));
  return out.replace(/(^|[^:])\/\/[^\n]*/g, (m, p1) => p1 + ' '.repeat(m.length - p1.length));
}

// The token is one way in; naming the family directly is the other, and it
// achieves the exact outcome the token restriction exists to prevent.
// src/og/** is exempt: satori loads the .ttf itself and has no CSS cascade,
// so the OG card's hand-note kicker cannot go through --font-accent.
const DIRECT_FAMILY = /font-family\s*:[^;{}]*shantell/i;
const exts = new Set(['.css', '.astro', '.svelte', '.ts', '.tsx', '.js', '.mjs']);
const violations = [];
let filesScanned = 0;

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    if (entry === 'node_modules' || entry.startsWith('.')) continue;
    const full = join(dir, entry);
    const s = statSync(full);
    if (s.isDirectory()) walk(full);
    else if (exts.has(extname(full))) scanGeneric(full);
  }
}

// Generic scan: every `--font-accent` occurrence is a violation unless a
// file-specific exception below says otherwise.
function scanGeneric(file) {
  filesScanned += 1;
  const rel = relative(siteRoot, file).replace(/\\/g, '/');
  const src = readFileSync(file, 'utf8');
  const lines = src.split('\n');

  if (rel === 'src/styles/zine.css') {
    scanZineCss(rel, stripComments(src).split('\n'), lines);
    return;
  }
  if (rel === 'src/layouts/BaseLayout.astro') {
    scanBaseLayout(rel, lines);
    return;
  }

  const stripped = stripComments(src).split('\n');
  stripped.forEach((line, i) => {
    if (TOKEN.test(line)) {
      violations.push({ file: rel, line: i + 1, snippet: (lines[i] ?? line).trim() });
    } else if (DIRECT_FAMILY.test(line) && !rel.startsWith('src/og/')) {
      violations.push({
        file: rel,
        line: i + 1,
        snippet: (lines[i] ?? line).trim(),
        note: 'names the accent family directly, bypassing --font-accent',
      });
    }
  });
}

// zine.css: allow --font-accent only while inside a `.hand-note` rule block.
function scanZineCss(rel, lines, rawLines) {
  let depth = 0;
  let handNoteDepth = -1; // brace depth at which the current .hand-note block opened

  lines.forEach((raw, i) => {
    const line = raw;

    if (TOKEN.test(line)) {
      const insideHandNote = handNoteDepth !== -1 && depth >= handNoteDepth;
      if (!insideHandNote) {
        violations.push({ file: rel, line: i + 1, snippet: (rawLines[i] ?? line).trim() });
      }
    }

    // Track brace depth and whether we just opened a .hand-note selector.
    // Selector lines look like `.hand-note {` or `.hand-note, .other {`.
    const opens = (line.match(/{/g) || []).length;
    const closes = (line.match(/}/g) || []).length;

    if (opens > 0 && /\.hand-note\b/.test(line)) {
      handNoteDepth = depth;
    }

    depth += opens;
    depth -= closes;

    if (handNoteDepth !== -1 && depth <= handNoteDepth) {
      handNoteDepth = -1;
    }
  });
}

// BaseLayout.astro: allow only the <Font cssVariable="--font-accent" /> loader.
const FONT_LOADER = /<Font\s+cssVariable=["']--font-accent["']/;
function scanBaseLayout(rel, lines) {
  lines.forEach((line, i) => {
    if (TOKEN.test(line) && !FONT_LOADER.test(line)) {
      violations.push({ file: rel, line: i + 1, snippet: line.trim() });
    }
  });
}

// astro.config.mjs lives outside src/; check it explicitly since it's part
// of the documented allowlist (the font-provider registration).
function checkAstroConfig() {
  const file = resolve(siteRoot, 'astro.config.mjs');
  let src;
  try {
    src = readFileSync(file, 'utf8');
  } catch {
    return; // nothing to check if the file doesn't exist
  }
  const lines = src.split('\n');
  const REGISTRATION = /cssVariable:\s*['"]--font-accent['"]/;
  lines.forEach((line, i) => {
    if (TOKEN.test(line) && !REGISTRATION.test(line)) {
      violations.push({ file: 'astro.config.mjs', line: i + 1, snippet: line.trim() });
    }
  });
}

if (!existsSync(srcRoot)) {
  console.error(`Accent-Font Audit\n\n  Source root not found: ${srcRoot}`);
  process.exit(1);
}
walk(srcRoot);
checkAstroConfig();

console.log('Accent-Font Audit (--font-accent restricted to .hand-note)\n');

// An empty walk is not a clean pass — it means the scan never happened.
if (filesScanned === 0) {
  console.error(`  Scanned 0 files under ${srcRoot}. That is a broken audit, not a clean one.\n`);
  process.exit(1);
}

if (violations.length === 0) {
  console.log(`  --font-accent usage is confined to the approved allowlist. (${filesScanned} files scanned)`);
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line}${v.note ? ` — ${v.note}` : ''}`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} --font-accent usage(s) found outside the allowlist.`);
console.error('Approved: src/styles/zine.css (.hand-note rule), src/layouts/BaseLayout.astro (Font loader), astro.config.mjs (registration).');
process.exit(1);
