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
import { readFileSync, readdirSync, statSync } from 'node:fs';
import { join, extname, relative } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const here = dirname(fileURLToPath(import.meta.url));
const siteRoot = resolve(here, '..');
const srcRoot = resolve(siteRoot, 'src');

const TOKEN = /--font-accent\b/;
const exts = new Set(['.css', '.astro', '.svelte', '.ts', '.tsx', '.js', '.mjs']);
const violations = [];

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
  const rel = relative(siteRoot, file).replace(/\\/g, '/');
  const src = readFileSync(file, 'utf8');
  const lines = src.split('\n');

  if (rel === 'src/styles/zine.css') {
    scanZineCss(rel, lines);
    return;
  }
  if (rel === 'src/layouts/BaseLayout.astro') {
    scanBaseLayout(rel, lines);
    return;
  }

  lines.forEach((line, i) => {
    if (TOKEN.test(line)) {
      violations.push({ file: rel, line: i + 1, snippet: line.trim() });
    }
  });
}

// zine.css: allow --font-accent only while inside a `.hand-note` rule block.
function scanZineCss(rel, lines) {
  let depth = 0;
  let handNoteDepth = -1; // brace depth at which the current .hand-note block opened

  lines.forEach((raw, i) => {
    const line = raw;

    if (TOKEN.test(line)) {
      const insideHandNote = handNoteDepth !== -1 && depth >= handNoteDepth;
      if (!insideHandNote) {
        violations.push({ file: rel, line: i + 1, snippet: line.trim() });
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

walk(srcRoot);
checkAstroConfig();

console.log('Accent-Font Audit (--font-accent restricted to .hand-note)\n');
if (violations.length === 0) {
  console.log('  --font-accent usage is confined to the approved allowlist.');
  process.exit(0);
}
for (const v of violations) {
  console.log(`  [FAIL] ${v.file}:${v.line}`);
  console.log(`         ${v.snippet}`);
}
console.error(`\n${violations.length} --font-accent usage(s) found outside the allowlist.`);
console.error('Approved: src/styles/zine.css (.hand-note rule), src/layouts/BaseLayout.astro (Font loader), astro.config.mjs (registration).');
process.exit(1);
